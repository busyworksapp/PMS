# 🎯 BARRON PRODUCTION MANAGEMENT SYSTEM - REFERENCE CARD

## ⚡ QUICK REFERENCE

### 🌐 URLs
```
Backend:        http://127.0.0.1:8001
Swagger Docs:   http://127.0.0.1:8001/docs
Frontend:       http://localhost:3000
Login:          http://localhost:3000/templates/login.html
```

### 🔐 Credentials
```
Username:  admin
Password:  admin123
Employee#: ADM001
```

### 📁 Key Files
```
.env                    → Configuration file
app/backend/app/        → API code
app/frontend/templates/ → HTML pages
```

---

## 📋 WHAT'S BEEN DONE

### ✅ Completed
1. Full application built (46+ endpoints)
2. Backend running on port 8001
3. Frontend running on port 3000
4. Swagger documentation live
5. **.env files created with Railway credentials**
6. Database driver configured (PyMySQL)
7. Code ready for production

### ⏳ Next Steps
1. Create admin user (triggers DB init)
2. Login to dashboard
3. Create master data
4. Test workflows

---

## 🚀 CREATE FIRST USER (INITIALIZES DATABASE)

**Go to:** http://127.0.0.1:8001/docs

**Find:** POST /api/auth/register

**Click:** Try it out

**Paste:**
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

**Click:** Execute

**Result:** Status 200 = Database initialized! ✅

---

## 📚 DOCUMENTATION

| File | Purpose | Read Time |
|------|---------|-----------|
| QUICK_START.md | Get started fast | 5 min |
| DATABASE_SETUP.md | Database info | 10 min |
| TESTING_GUIDE.md | Test everything | 15 min |
| BUILD_SUMMARY.md | Complete details | 30 min |
| DEPLOYMENT_COMPLETE.md | Full overview | 10 min |

---

## 🔧 ENVIRONMENT (.env)

**Location:** `app/backend/.env`

```
DATABASE_URL=mysql+pymysql://root:PASSWORD@shortline.proxy.rlwy.net:19278/railway
REDIS_URL=redis://default:PASSWORD@caboose.proxy.rlwy.net:39766
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
APP_NAME=Barron Production Management System
DEBUG=False
```

---

## 🗄️ DATABASE

**Type:** MySQL on Railway  
**Host:** shortline.proxy.rlwy.net:19278  
**Database:** railway  
**Tables:** Auto-created on first API call  

---

## ✨ MODULES

- ✅ Authentication
- ✅ Job Planning
- ✅ Defects
- ✅ Maintenance
- ✅ SOP/NCR
- ✅ Master Data
- ✅ Finance/BOM
- ✅ Operator Portal

---

## ⏱️ TIME ESTIMATE

| Task | Time |
|------|------|
| Create user | 2 min |
| Login | 1 min |
| Create master data | 5 min |
| Test workflows | 10 min |
| **Total** | **18 min** |

---

**Ready? Go to http://127.0.0.1:8001/docs and create your first user!**
