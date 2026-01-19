# Technical Reference: Railway Deployment Fixes

**Version:** 1.0  
**Date:** January 19, 2026  
**Commit:** 46342f2

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Railway Deployment                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Docker Container                                     │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │                                                      │  │
│  │  HEALTHCHECK (every 30s)                            │  │
│  │  ↓                                                   │  │
│  │  Uvicorn Server (Port 8000)                         │  │
│  │  ├─ /health (no DB required)                        │  │
│  │  ├─ / (root endpoint)                               │  │
│  │  ├─ /api/auth/* (10 route modules)                  │  │
│  │  └─ /api/whatsapp/* (Twilio integration)            │  │
│  │  ↑                                                   │  │
│  │  Startup Event (with retries)                       │  │
│  │  ├─ Database connection (retry: 3x, delay: 2s)     │  │
│  │  ├─ Create tables (SQLAlchemy)                      │  │
│  │  └─ Load route modules (10 total)                   │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│           ↓                    ↓                            │
│    ┌─────────────────┐  ┌─────────────────┐               │
│    │ Railway MySQL   │  │ Railway Redis   │               │
│    │ shortline proxy │  │ caboose proxy   │               │
│    │ Port: 19278     │  │ Port: 39766     │               │
│    └─────────────────┘  └─────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Dockerfile Changes

### Original Problem
```dockerfile
# Wrong: creates app/backend/app structure in container
COPY app/backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt
COPY app/backend/app ./backend/app
WORKDIR /app/backend
CMD ["python", "-m", "uvicorn", "app.main:app", ...]
```

This resulted in:
- Container structure: `/app/backend/app/main.py`
- But Python tries to import from: `app.main:app`
- Result: Import fails → 502 error

### Solution
```dockerfile
# Correct: simple flat structure
COPY app/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/backend/app ./app

# Added health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "65"]
```

Now:
- Container structure: `/app/main.py` (at root level)
- Python imports: `app.main:app` ✓ Works!

---

## Database Initialization Flow

### Before: Blocking (caused 502 errors)
```python
@app.on_event("startup")
async def startup_event():
    try:
        from app.db.database import Base, engine
        Base.metadata.create_all(bind=engine)  # Blocks here if DB not available!
        # Load routes...
    except Exception as e:
        raise  # App crashes
```

**Problem:** If MySQL isn't ready, the entire startup event times out (usually >30s), Railway considers it a failed deployment.

### After: Non-blocking with retries
```python
@app.on_event("startup")
async def startup_event():
    try:
        from app.db.database import Base, engine
        from sqlalchemy import text
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))  # Test connection
                Base.metadata.create_all(bind=engine)  # Create tables
                break  # Success
            except Exception as db_error:
                if attempt < max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)  # Wait before retry
                else:
                    logger.error(f"Failed after {max_retries} attempts")
                    # DON'T raise - let app start anyway
        
        # Load routes...
    except Exception as e:
        logger.error(f"Startup error: {e}")
        # Don't crash - app continues
```

**Benefits:**
1. **Retry mechanism:** Handles temporary MySQL connection issues
2. **Graceful degradation:** App starts even if DB unavailable
3. **Health endpoint:** `/health` endpoint works without DB
4. **Time-bounded:** 3 retries × 2 seconds = 6 seconds max wait

### Timeline with Railway MySQL Startup

```
Time    Event
─────────────────────────────────────────────────────
0s      Container starts
0s      Uvicorn initializes
1s      Startup event begins
1s      Attempt 1 to connect to MySQL → FAILS (still booting)
2s      Wait 2 seconds
3s      Attempt 2 to connect to MySQL → FAILS (still initializing)
5s      Wait 2 seconds
7s      Attempt 3 to connect to MySQL → SUCCESS! ✓
7s      Create database tables
8s      Load all route modules
9s      "Application startup complete!"
10s     Health check passes
11s+    All endpoints available ✓
```

---

## Configuration Management

### Before: Hardcoded Credentials
```python
class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:PASSWORD@host:port/db"
    TWILIO_ACCOUNT_SID: str = "AC..."
    # Credentials are baked into the image
    # If they change, must rebuild image
    # Security risk: credentials visible in image
```

### After: Environment Variables First
```python
class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:PASSWORD@host:port/db"  # Fallback only
    )
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "AC...")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
```

**Benefits:**
1. Railway can inject environment variables at runtime
2. No rebuild needed to change credentials
3. Same image works in dev, staging, production
4. Credentials not visible in Dockerfile

### How Railway Injects Variables

```
Railway Dashboard
  ↓
Settings → Variables
  ↓
DATABASE_URL=mysql+pymysql://...
TWILIO_ACCOUNT_SID=AC...
  ↓
Environment passed to container
  ↓
Config reads: os.getenv("DATABASE_URL")
  ↓
✓ Correct credentials loaded
```

---

## Health Check Implementation

### Why Needed?
- Railway uses health checks to determine container status
- If container doesn't respond to health check, Railway assumes it's down
- Without health check, Railway might restart container unnecessarily

### Implementation in Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

**Parameters:**
- `--interval=30s` - Check every 30 seconds
- `--timeout=10s` - Wait 10 seconds for response
- `--start-period=40s` - Give container 40 seconds to start before first check
- `--retries=3` - Container marked unhealthy after 3 failed checks

### Health Endpoint in app.main.py
```python
@app.get("/health")
def health_check():
    """Health check endpoint - doesn't require database."""
    return {"status": "ok"}
```

**Why separate from root endpoint?**
- `/` endpoint might need database for complex queries
- `/health` is lightweight, always responds
- Railway can check health even if app is degraded

### Health Check Timeline
```
Time    Action
─────────────────────────────────────────────────
0-40s   Startup period (no checks)
40s     First health check: /health → {"status":"ok"} ✓
70s     Second health check: /health → {"status":"ok"} ✓
100s    Third health check: /health → {"status":"ok"} ✓
        ...continues every 30s...
        If 3 consecutive checks fail:
        Container marked as unhealthy → Railway restarts it
```

---

## Environment Variable Setup for Railway

### Required Variables in Railway Dashboard

Go to: **Project Settings → Variables**

```
DATABASE_URL=mysql+pymysql://root:PASSWORD@shortline.proxy.rlwy.net:19278/railway
REDIS_URL=redis://default:PASSWORD@caboose.proxy.rlwy.net:39766
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+...
SECRET_KEY=your-secret-key
DEBUG=False
```

### Optional Variables
```
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256
TWILIO_WEBHOOK_VERIFY_TOKEN=...
```

---

## Connection Pooling

### Database Connection Pool
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,           # Verify connections are alive
    pool_size=10,                 # Keep 10 connections open
    max_overflow=20,              # Allow 20 additional overflow connections
    echo=settings.DEBUG,          # Log SQL queries if DEBUG=True
)
```

**Why these settings?**
- `pool_pre_ping=True`: Prevents "lost connection" errors
- `pool_size=10`: Handles up to 10 concurrent database operations
- `max_overflow=20`: Can handle traffic spikes (up to 30 total)
- `echo=DEBUG`: Helpful for debugging, disabled in production

### Timeout Settings
```bash
CMD ["python", "-m", "uvicorn", 
     "app.main:app", 
     "--host", "0.0.0.0", 
     "--port", "8000", 
     "--timeout-keep-alive", "65"]
```

- `--timeout-keep-alive=65`: Keep HTTP connections alive for 65 seconds
- Prevents premature connection closure during long operations

---

## Procfile and railway.json

### Procfile
```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 65
```

**Why needed?**
- Railway checks for Procfile to determine startup command
- `$PORT` variable is provided by Railway (usually 8000)
- Ensures consistent startup across platforms

### railway.json
```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 65",
    "restartPolicyMaxRetries": 5
  }
}
```

**Why needed?**
- Explicit configuration for Railway
- Specifies to use Dockerfile (not Nix packages)
- Defines restart policy (5 retries on failure)

---

## .dockerignore

```
.git              # Don't copy git history
.env              # Don't expose .env file
.venv             # Don't copy local virtual env
__pycache__       # Don't copy Python cache
*.pyc, *.pyo      # Don't copy compiled Python files
.pytest_cache     # Don't copy test cache
.coverage         # Don't copy coverage reports
docker-compose    # Don't copy local compose file
README.md         # Don't copy documentation (not needed in prod)
scripts/          # Don't copy scripts
```

**Benefits:**
- Smaller Docker image
- Faster builds
- No unnecessary files in production

---

## Error Resolution Flowchart

```
502 Bad Gateway on Railway
        ↓
    ┌───┴───┐
    │       │
Check  Check
Logs   Endpoints
    │       │
    ↓       ↓
Error?   /health
   │     responds?
   │        │
   ├→YES→ Check /
   │      responds?
   │        │
   │      ├→YES→ Check /docs
   │      │      responds?
   │      │        │
   │      │      └→YES→ ✅ FIXED!
   │      │
   │      └→NO→ Database
   │            issue?
   │
   └→NO→ Check env
        variables
         │
         └→ Set
            missing vars
            & redeploy
```

---

## Verification Sequence

### Test 1: Service Availability
```bash
curl -i https://your-app.up.railway.app/health
# HTTP/1.1 200 OK
# {"status":"ok"}
```

### Test 2: Root Endpoint
```bash
curl -i https://your-app.up.railway.app/
# HTTP/1.1 200 OK
# {"message":"Barron Production Management System",...}
```

### Test 3: API Documentation
```bash
curl -i https://your-app.up.railway.app/docs
# HTTP/1.1 200 OK
# (Swagger UI HTML)
```

### Test 4: Authentication Endpoint
```bash
curl -i -X POST https://your-app.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
# HTTP/1.1 200 OK (or 422 if validation fails - that's fine)
```

---

## Performance Metrics

### Expected Response Times (after fixes)

| Endpoint | Response Time | Notes |
|----------|--------------|-------|
| `/health` | 5-10ms | No database query |
| `/` | 15-50ms | Simple endpoint |
| `/docs` | 100-200ms | Swagger UI generation |
| `/api/auth/register` | 200-500ms | Database write |
| `/api/orders` | 100-300ms | Database query |

### Expected Startup Time

| Phase | Time | Notes |
|-------|------|-------|
| Container boot | 5-10s | Docker + Python init |
| Database connection (3 retries) | 3-6s | Retry logic |
| Table creation | 2-5s | SQLAlchemy |
| Route initialization | 1-2s | Import modules |
| Ready for requests | 15-25s | Total startup |

---

## Debugging Commands

### View Railway Logs
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# View logs
railway logs --follow

# Or use Railway Dashboard → Deployments → Logs
```

### Test Connection from Local Machine
```bash
# Test database accessibility
mysql -h shortline.proxy.rlwy.net -P 19278 -u root -p

# Test Redis accessibility
redis-cli -h caboose.proxy.rlwy.net -p 39766
```

### Inspect Container Environment
```bash
# View all running containers
railway ps

# SSH into container
railway shell

# Inside container, check env vars
echo $DATABASE_URL
echo $TWILIO_ACCOUNT_SID
```

---

## Success Indicators

✅ **All of these should be true:**

- [ ] Deployment completes without errors
- [ ] `/health` endpoint responds `{"status":"ok"}`
- [ ] `/` endpoint responds with Barron PMS message
- [ ] `/docs` endpoint shows Swagger UI
- [ ] Railway logs show "Application startup complete!"
- [ ] Railway logs show all 10 routes loaded
- [ ] Railway logs show Twilio service initialized
- [ ] No 502 errors in Railway logs
- [ ] Container health status shows as "healthy"

---

**Document Version:** 1.0  
**Last Updated:** January 19, 2026  
**Status:** ✅ Ready for Reference
