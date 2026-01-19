# SETUP GUIDE - Barron Production Management System

## ⚡ Quick Start (5 minutes)

### Step 1: Install Python Dependencies
```powershell
cd app\backend
pip install -r requirements.txt
```

### Step 2: Start the Backend Server
```powershell
# Run from: app\backend directory
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Output should show:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

### Step 3: Start the Frontend Server (New Terminal)
```powershell
# Run from: app\frontend directory
python -m http.server 3000
```

Output should show:
```
Serving HTTP on 0.0.0.0 port 3000 ...
```

### Step 4: Open the Application
- **Main App**: http://localhost:3000/templates/login.html
- **Operator Portal**: http://localhost:3000/templates/operator-login.html
- **API Docs**: http://localhost:8000/docs

---

## 🔑 Test Credentials

Use the registration endpoint to create users. All users can use their username to login.

**Default Admin (create via registration):**
- Username: `admin`
- Password: `admin123`
- Role: `admin`

**Sample Operator:**
- Employee Number: `1001`
- Password: `1001` (same as employee number)

---

## 📁 Project Structure

```
app/
├── backend/                    # FastAPI Application
│   ├── app/
│   │   ├── core/              # Configuration & Security
│   │   │   ├── config.py      # App settings (DB, Redis URLs)
│   │   │   ├── security.py    # JWT & password hashing
│   │   │   └── __init__.py
│   │   │
│   │   ├── db/                # Database Setup
│   │   │   ├── database.py    # SQLAlchemy engine & session
│   │   │   └── __init__.py
│   │   │
│   │   ├── models/            # SQLAlchemy ORM Models
│   │   │   ├── user.py        # Users & roles
│   │   │   ├── department.py  # Departments
│   │   │   ├── product.py     # Products & stages
│   │   │   ├── machine.py     # Machinery
│   │   │   ├── order.py       # Orders & scheduling
│   │   │   ├── defect.py      # Rejects & returns
│   │   │   ├── maintenance.py # Maintenance tickets
│   │   │   ├── sop_ncr.py     # SOP tickets & NCR
│   │   │   ├── bom.py         # Bill of Materials
│   │   │   ├── form_config.py # Dynamic forms
│   │   │   ├── audit.py       # Audit logs
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/           # Pydantic Request/Response Models
│   │   │   ├── user.py        # User schemas
│   │   │   ├── master.py      # Master data schemas
│   │   │   ├── order.py       # Order schemas
│   │   │   └── __init__.py
│   │   │
│   │   ├── routes/            # API Endpoints
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── master.py      # Master data endpoints
│   │   │   ├── orders.py      # Order management endpoints
│   │   │   ├── defects.py     # Defect tracking endpoints
│   │   │   ├── maintenance.py # Maintenance endpoints
│   │   │   ├── sop_ncr.py     # SOP/NCR endpoints
│   │   │   ├── finance.py     # Finance & BOM endpoints
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/          # Business Logic Layer (for future expansion)
│   │   │   └── __init__.py
│   │   │
│   │   ├── main.py            # FastAPI App Initialization
│   │   └── __init__.py
│   │
│   ├── requirements.txt        # Python Dependencies
│   ├── run.ps1               # PowerShell startup script
│   └── main.py               # Alternative entry point
│
└── frontend/                  # Web Interface
    ├── templates/            # HTML Pages
    │   ├── login.html        # Main login page
    │   ├── operator-login.html
    │   ├── dashboard.html    # Admin dashboard
    │   ├── job-planning.html # Order scheduling
    │   ├── operator-jobs.html # Operator job board (mobile-friendly)
    │   ├── defects.html      # Defects & returns
    │   ├── maintenance.html  # Maintenance management
    │   └── master-data.html  # Admin configuration
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css     # Industrial-grade styles (dark theme)
    │   │
    │   ├── js/
    │   │   └── main.js       # API client & UI utilities
    │
    └── run.ps1               # Frontend server startup script
```

---

## 🔌 API Endpoints Overview

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/operator-login` | Operator quick login |

### Master Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/master/departments` | List departments |
| POST | `/api/master/departments` | Create department |
| GET | `/api/master/products` | List products |
| POST | `/api/master/products` | Create product |
| GET | `/api/master/machines` | List machines |
| POST | `/api/master/machines` | Create machine |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders` | List orders |
| POST | `/api/orders` | Create order |
| GET | `/api/orders/{id}` | Get order details |
| POST | `/api/orders/{id}/schedules` | Schedule order |

### Defects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/defects/rejects` | List internal rejects |
| POST | `/api/defects/rejects` | Create reject ticket |
| GET | `/api/defects/returns` | List customer returns |
| POST | `/api/defects/returns` | Log return |
| PATCH | `/api/defects/rejects/{id}/approve` | Approve reject |
| PATCH | `/api/defects/rejects/{id}/status` | Update status |

### Maintenance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/maintenance/tickets` | List maintenance tickets |
| POST | `/api/maintenance/tickets` | Create ticket |
| PATCH | `/api/maintenance/tickets/{id}/assign` | Assign ticket |
| PATCH | `/api/maintenance/tickets/{id}/status` | Update status |

### SOP/NCR
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sop-ncr/tickets` | List SOP tickets |
| POST | `/api/sop-ncr/tickets` | Create SOP ticket |
| POST | `/api/sop-ncr/tickets/{id}/ncr` | Submit NCR |
| PATCH | `/api/sop-ncr/tickets/{id}/reject` | Reject ticket |
| PATCH | `/api/sop-ncr/tickets/{id}/reassign` | Reassign ticket |
| PATCH | `/api/sop-ncr/tickets/{id}/hod-decision` | HOD decision |

### Finance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/finance/boms` | List BOMs |
| POST | `/api/finance/boms` | Create BOM |
| GET | `/api/finance/boms/{id}/components` | Get BOM components |
| POST | `/api/finance/boms/{id}/cost-impact` | Calculate impact |
| GET | `/api/finance/boms/{id}/history` | Get version history |

---

## 🗄️ Database

### Connection Details
- **Host**: shortline.proxy.rlwy.net
- **Port**: 19278
- **Database**: railway
- **User**: root
- **Password**: fYJdZhXYpLzfiLFhgjvjkUWUzDKKCaYa

### Local Alternative
For local MySQL, update `app/core/config.py`:
```python
DATABASE_URL = "mysql+mysqldb://root:password@localhost:3306/barron_prod"
```

### Key Tables
- `users` - System users
- `departments` - Departments
- `machines` - Equipment
- `products` - Products & items
- `orders` - Customer orders
- `order_schedules` - Job scheduling
- `internal_rejects` - Defect tickets
- `customer_returns` - Return tracking
- `maintenance_tickets` - Service requests
- `sop_failure_tickets` - SOP violations
- `non_conformance_reports` - NCR records
- `bills_of_materials` - Cost structure
- `audit_logs` - Complete history

---

## 🚀 Deployment

### Using PowerShell Scripts
```powershell
# Backend
cd app\backend
.\run.ps1

# Frontend (new terminal)
cd app\frontend
.\run.ps1
```

### Docker (Optional)
```bash
# Build
docker build -t barron-prod backend/

# Run
docker run -p 8000:8000 -e DATABASE_URL=<url> barron-prod
```

---

## 📝 Features Summary

✅ **Job Planning** - Order scheduling & capacity management
✅ **Defect Tracking** - Internal rejects & customer returns
✅ **SOP/NCR** - Non-conformance workflows with escalation
✅ **Maintenance** - Equipment service request management
✅ **Master Data** - Dynamic product, department, machine management
✅ **Operator Portal** - Mobile-friendly job board
✅ **Audit Trails** - Complete action history
✅ **Role-Based Access** - Fine-grained permissions
✅ **Finance Integration** - BOM & cost impact tracking

---

## 🔧 Troubleshooting

### Backend won't start
```powershell
# Check Python version
python --version  # Must be 3.9+

# Check dependencies
pip list | grep fastapi

# Try reinstalling
pip install --upgrade -r requirements.txt
```

### Database connection error
- Verify MySQL/Railway credentials in `app/core/config.py`
- Check network connectivity to shortline.proxy.rlwy.net
- Ensure port 19278 is not blocked

### CORS errors
- Frontend and backend must run on different ports (3000 and 8000)
- CORS is enabled for all origins in development

### Redis not needed yet
- Redis connection is configured but not actively used in MVP
- Future releases will use it for caching and real-time features

---

## 📞 Next Steps

1. **Create test data** - Use the Master Data admin panel
2. **Test workflows** - Create orders, rejects, maintenance tickets
3. **Review audit logs** - Check the database audit_logs table
4. **Customize** - Forms and workflows are JSON-based and configurable

---

**Last Updated**: January 2026  
**Version**: 1.0.0 MVP
