# 📊 Data Scripts & Database Initialization Guide

## Overview

Three Python scripts manage your Railway MySQL database:

| Script | Purpose | When to Use |
|--------|---------|-----------|
| **init_database.py** | Create all tables | First time setup, new deployment |
| **seed_data.py** | Add sample data | After tables created, for testing |
| **reset_database.py** | Delete & recreate | Development reset, clean start |

---

## 🚀 Quick Start (First Time Setup)

### Step 1: Initialize Database Tables
```powershell
cd "c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend"
python init_database.py
```

**Expected Output:**
```
============================================================
  BARRON PRODUCTION MANAGEMENT SYSTEM
  Database Initialization Script
============================================================

📊 Database: railway
🔑 Connection: Checking...
✅ Connection successful!

📋 Creating tables...
✅ All tables created successfully!

📊 Created 11 tables:

    1. users
    2. departments
    3. products
    4. machines
    5. orders
    6. order_items
    ...
```

**What happens:**
- ✅ Connects to Railway MySQL database
- ✅ Creates all 11+ database tables
- ✅ Sets up foreign key relationships
- ✅ Creates indexes for performance

### Step 2: Seed Sample Data
```powershell
python seed_data.py
```

**Expected Output:**
```
============================================================
  BARRON PRODUCTION MANAGEMENT SYSTEM
  Database Seed Script - Sample Data
============================================================

✅ Tables verified

👤 Creating admin user...
   ✅ Admin user created (admin/admin123)

🏢 Creating departments...
   ✅ Production
   ✅ Quality Assurance
   ✅ Maintenance

📦 Creating products...
   ✅ PROD001 - Industrial Widget A
   ✅ PROD002 - Industrial Widget B
   ✅ PROD003 - Assembly Kit C

🔧 Creating machines...
   ✅ MACH001 - CNC Lathe #1
   ✅ MACH002 - Press Machine #2
   ✅ MACH003 - Assembly Station #1

============================================================
✅ DATABASE SEEDING COMPLETE!
============================================================

📊 Data Summary:
   Departments: 3
   Products: 3
   Machines: 3
   Users: 1
```

**What gets created:**
- ✅ 1 Admin user (admin/admin123)
- ✅ 3 Departments (Production, QA, Maintenance)
- ✅ 3 Products (Widget A, Widget B, Assembly Kit C)
- ✅ 3 Machines (CNC Lathe, Press, Assembly Station)
- ✅ All relationships established

### Step 3: Start the Application
```powershell
cd ..
python -m uvicorn app.main:app --port 8001
```

### Step 4: Login and Test
- Go to: http://localhost:3000/templates/login.html
- Username: **admin**
- Password: **admin123**

---

## 📋 Database Tables Created

### Core Tables

**users** - Authentication & user management
- id, username, email, fullname, employee_number, role
- hashed_password, is_active, created_at, updated_at

**departments** - Organization structure
- id, name, description, manager, created_at, updated_at

**products** - Product catalog
- id, code, name, description, unit, unit_cost, created_at

**machines** - Equipment inventory
- id, code, name, model, serial_number, status, department_id

**orders** - Customer/production orders
- id, order_number, customer, product_id, quantity, due_date, status

**order_items** - Line items for orders
- id, order_id, description, quantity, status, assigned_machine_id

### Quality Control Tables

**internal_rejects** - Quality defects
- id, order_id, machine_id, reject_reason, quantity, action_taken

**customer_returns** - Product returns
- id, order_id, return_reason, quantity, receive_date, action

### Maintenance Tables

**maintenance_tickets** - Equipment maintenance
- id, machine_id, issue_description, priority, status, assigned_to

**sop_failure_tickets** - SOP violations
- id, description, severity, action_required, status

**non_conformance_reports** - NCR records
- id, description, affected_product, root_cause, corrective_action

---

## 🔄 Database Management Commands

### Check Database Status
```powershell
python init_database.py
```
This will test the connection and show all tables.

### Add More Sample Data
Edit `seed_data.py` and add more entries:
```python
departments_data = [
    {
        "name": "New Department",
        "description": "Description",
        "manager": "Manager Name",
    },
    # Add more...
]
```

Then run: `python seed_data.py`

### Reset Everything (Development Only)
```powershell
python reset_database.py
```

**Warning: This deletes ALL data!**
- Type `CONFIRM` when prompted
- Drops all tables
- Recreates empty tables

### Reset and Reseed
```powershell
python reset_database.py
python seed_data.py
```

Quick clean slate for testing.

---

## 🔐 Connection Details

**Location:** `app/backend/.env`

```
DATABASE_URL=mysql+pymysql://root:PASSWORD@shortline.proxy.rlwy.net:19278/railway
```

**Components:**
- **Host:** shortline.proxy.rlwy.net
- **Port:** 19278
- **Database:** railway
- **Driver:** PyMySQL (mysql+pymysql)
- **User:** root

---

## ✅ Verification Checklist

After running the scripts:

- [ ] `init_database.py` runs without errors
- [ ] All tables appear in output
- [ ] `seed_data.py` completes successfully
- [ ] Admin user created
- [ ] Sample data visible in output
- [ ] Can login with admin/admin123
- [ ] Dashboard loads with data

---

## 🆘 Troubleshooting

### "Connection refused"
**Problem:** Cannot connect to Railway MySQL
**Solution:**
1. Check `.env` file exists in `app/backend/`
2. Verify DATABASE_URL is correct
3. Check internet connection
4. Restart Railway service

### "Table already exists"
**Problem:** Table creation fails because table exists
**Solution:**
- This is normal if running twice
- Use `reset_database.py` if you need fresh start

### "Import error: No module named 'app'"
**Problem:** Python path not correct
**Solution:**
```powershell
cd "c:\Users\4667.KevroAD\OneDrive - Barron (Pty) Ltd\Desktop\th\app\backend"
python init_database.py  # Run from this directory
```

### "No such table"
**Problem:** Database not initialized
**Solution:**
1. Run `init_database.py` first
2. Wait for confirmation
3. Then run `seed_data.py`

---

## 🎯 Next Steps

1. **Run the scripts in order:**
   ```powershell
   python init_database.py
   python seed_data.py
   ```

2. **Start the application:**
   ```powershell
   python -m uvicorn app.main:app --port 8001
   ```

3. **Test the system:**
   - Login at: http://localhost:3000/templates/login.html
   - Create orders, log defects, schedule maintenance
   - Verify data persists

4. **Extend sample data:**
   - Edit `seed_data.py` to add more test data
   - Create additional departments, products, machines
   - Run again to add to database

---

## 📖 File Locations

```
th/
├── app/backend/
│   ├── init_database.py    ← Create tables
│   ├── seed_data.py         ← Add sample data
│   ├── reset_database.py    ← Reset (caution!)
│   ├── .env                 ← Database credentials
│   └── app/
│       ├── models/          ← Table definitions
│       ├── db/database.py   ← Connection config
│       └── main.py          ← Application entry
└── app/frontend/
    └── templates/           ← Web pages
```

---

## ✨ Success!

Once complete:
- ✅ 11+ database tables created
- ✅ Sample admin user ready
- ✅ Test data available
- ✅ System ready for production use

**You're ready to start testing the Barron Production Management System!**

---

**Created:** January 18, 2026  
**Version:** 1.0.0  
**Status:** ✅ Ready for use
