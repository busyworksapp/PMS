# 🗄️ DATABASE INITIALIZATION GUIDE

## Current Configuration

Your system is configured to use **Railway MySQL**:

### Connection Details:
```
Host: shortline.proxy.rlwy.net
Port: 19278
Username: root
Database: railway
Password: [configured in .env]
```

---

## ✅ Environment Files Created

### File 1: `app/backend/.env`
- **Location:** `c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend\.env`
- **Purpose:** Backend application configuration
- **Contains:** Database URL, Redis URL, API secrets

### File 2: `.env` (root)
- **Location:** `c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\.env`
- **Purpose:** Global environment configuration
- **Optional:** For reference and deployment

---

## 📊 DATABASE INITIALIZATION PROCESS

### How Tables Are Created:

The system uses **automatic table creation** on first API call:

```
1. Backend starts (port 8001)
   ↓
2. First API request arrives (e.g., /api/auth/register)
   ↓
3. SQLAlchemy imports and initializes
   ↓
4. Deferred startup event triggers create_app()
   ↓
5. Base.metadata.create_all(bind=engine) executes
   ↓
6. All tables created in Railway MySQL database
   ↓
7. Table creation logged, data persists
```

---

## 🚀 TRIGGER TABLE CREATION

### Method 1: Create User via Swagger (Recommended)

1. **Open Swagger:** http://127.0.0.1:8001/docs
2. **Find:** POST /api/auth/register
3. **Click:** "Try it out"
4. **Paste this JSON:**
```json
{
  "username": "admin",
  "password": "admin123",
  "email": "admin@barron.com",
  "fullname": "System Administrator",
  "employee_number": "ADM001",
  "role": "admin",
  "department_id": null
}
```
5. **Click:** Execute
6. **Result:** 
   - ✅ User created
   - ✅ All 15 tables created in Railway
   - ✅ Response: 200 OK with user data

---

### Method 2: Make Any API Call

Any REST API call will trigger table creation:

```bash
# Health Check
curl http://127.0.0.1:8001/health

# Create Department
curl -X POST http://127.0.0.1:8001/api/master/departments \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Dept","description":"Test"}'
```

---

### Method 3: Direct Database Connection (Optional)

If you want to verify database connectivity independently:

```python
# Test connection with Python
import mysql.connector

connection = mysql.connector.connect(
    host="shortline.proxy.rlwy.net",
    port=19278,
    user="root",
    password="fYJdZhXYpLzfiLFhgjvjkUWUzDKKCaYa",
    database="railway"
)

cursor = connection.cursor()
cursor.execute("SELECT 1")
result = cursor.fetchone()
print("✅ Connected!" if result else "❌ Failed")
connection.close()
```

---

## 📋 TABLES THAT WILL BE CREATED

When the system makes its first database call, these 15 tables are automatically created:

```
1. users                      - User accounts and authentication
2. departments                - Organization departments
3. products                   - Product/item catalog
4. production_stages          - Production workflow stages
5. machines                   - Equipment inventory
6. machine_specifications     - Machine technical specs (JSON)
7. orders                     - Customer jobs/orders
8. order_items                - Line items in orders
9. order_schedules            - Job assignments to machines
10. internal_rejects          - Quality defect tickets
11. customer_returns          - Customer return tracking
12. maintenance_tickets       - Equipment maintenance requests
13. sop_failure_tickets       - SOP violation tickets
14. non_conformance_reports   - NCR records
15. bills_of_materials        - BOM/cost structure
16. bom_components            - BOM line items
17. dynamic_forms             - Dynamic form configurations
18. form_fields               - Form field definitions
19. audit_logs                - Complete action audit trail
```

---

## ✨ STEP-BY-STEP: CREATE USER → INITIALIZE DATABASE

### Step 1: Verify Backend is Running
```
Status: ✅ Running on http://127.0.0.1:8001
```

### Step 2: Open Swagger Documentation
**Go to:** http://127.0.0.1:8001/docs

You should see:
- Auth section with register endpoint
- Master data endpoints
- Orders, defects, maintenance endpoints
- All endpoints fully documented

### Step 3: Create Admin User (This triggers DB initialization)

**POST /api/auth/register** with:
```json
{
  "username": "admin",
  "password": "admin123",
  "email": "admin@barron.com",
  "fullname": "System Administrator",
  "employee_number": "ADM001",
  "role": "admin",
  "department_id": null
}
```

**Expected Response (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@barron.com",
  "is_active": true,
  "role": "admin"
}
```

✅ **ALL TABLES NOW CREATED IN RAILWAY!**

### Step 4: Verify Database Connection

**Login as User:**
```json
POST /api/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

✅ **DATABASE CONFIRMED WORKING!**

### Step 5: Access Dashboard

**Go to:** http://localhost:3000/templates/login.html
- Username: `admin`
- Password: `admin123`
- Click Login

✅ **FULL SYSTEM OPERATIONAL!**

---

## 🔧 WHAT IF DATABASE DOESN'T CONNECT?

### Issue: Connection Refused

**Cause:** Railway database unreachable

**Solution:**
1. Verify Railway account status
2. Check database credentials in `.env`
3. Verify network connectivity
4. Check firewall settings

```bash
# Test connectivity
ping shortline.proxy.rlwy.net
```

### Issue: Authentication Failed

**Cause:** Wrong password in DATABASE_URL

**Solution:**
1. Check Railway dashboard for credentials
2. Update `.env` with correct password
3. Restart backend

### Issue: Database Not Found

**Cause:** Database name "railway" doesn't exist

**Solution:**
1. Create database in Railway
2. Or use default database name from Railway
3. Update DATABASE_URL

---

## 📝 CONFIGURATION REFERENCE

### `.env` File Location
```
c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend\.env
```

### Environment Variables
```
DATABASE_URL=mysql+pymysql://root:PASSWORD@shortline.proxy.rlwy.net:19278/railway
REDIS_URL=redis://default:PASSWORD@caboose.proxy.rlwy.net:39766
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
APP_NAME=Barron Production Management System
DEBUG=False
```

### Change Configuration
1. Edit `.env` file
2. Backend auto-reloads on restart
3. No manual migration needed

---

## ✅ VERIFICATION CHECKLIST

After database initialization, verify:

- [ ] Backend running: http://127.0.0.1:8001/health returns OK
- [ ] Swagger docs accessible: http://127.0.0.1:8001/docs
- [ ] User created successfully via API
- [ ] Login works with created credentials
- [ ] Dashboard loads without errors
- [ ] Can create master data (departments, products)
- [ ] Data persists after refresh
- [ ] Audit logs record actions

---

## 🎯 NEXT STEPS

1. ✅ Create admin user (triggers DB init)
2. ✅ Login to dashboard
3. ✅ Create master data
4. ✅ Test all workflows
5. ✅ Verify data persistence

---

## 📞 DATABASE SUPPORT

**Railway Dashboard:** https://railway.app/dashboard  
**Database Name:** railway  
**Host:** shortline.proxy.rlwy.net  
**Port:** 19278  

**To Check Database Status:**
1. Go to Railway dashboard
2. Select your PostgreSQL database
3. Click "Data" tab
4. View table list and data

---

**Status:** ✅ Environment files created, database ready for initialization  
**Next Action:** Create first user via Swagger to initialize all tables  
**Created:** January 18, 2026
