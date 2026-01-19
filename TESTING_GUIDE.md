# 🎯 BARRON PRODUCTION MANAGEMENT SYSTEM - TESTING GUIDE

## ✅ System Status

| Component | Status | URL |
|-----------|--------|-----|
| **Backend API** | ✅ Running on port 8001 | http://127.0.0.1:8001 |
| **Swagger Docs** | ✅ Live | http://127.0.0.1:8001/docs |
| **Frontend UI** | ✅ Running on port 3000 | http://localhost:3000 |
| **Login Page** | ✅ Ready | http://localhost:3000/templates/login.html |

---

## 📋 STEP-BY-STEP TESTING GUIDE

### **Step 1️⃣ Create Test User (Using Swagger UI)**

**You should have the Swagger docs open now:** http://127.0.0.1:8001/docs

#### Instructions:
1. **Locate the Auth section** - Scroll down to find `/api/auth/register`
2. **Click on POST /api/auth/register** - The blue button
3. **Click "Try it out"** button
4. **Copy and paste this JSON** into the request body field:

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

5. **Click Execute** button
6. **Expected Response (200 Success):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@barron.com",
  "fullname": "System Administrator",
  "employee_number": "ADM001",
  "role": "admin",
  "is_active": true
}
```

✅ **User Created Successfully!**

---

### **Step 2️⃣ Login to Dashboard**

**Go to:** http://localhost:3000/templates/login.html

#### Login Credentials:
- **Username:** `admin`
- **Password:** `admin123`

#### What to expect:
- Enter credentials and click "Login"
- Redirect to dashboard.html
- See welcome message and statistics

✅ **Dashboard Loaded!**

---

### **Step 3️⃣ Create Master Data**

Once on the dashboard, click **"Master Data Admin"** link in the navigation.

#### 3a. Create Departments (3 total)

In the **Departments** tab:

**Department 1:**
- Name: `Branding Department`
- Description: `Branding and design operations`

**Department 2:**
- Name: `Printing Department`
- Description: `Printing operations`

**Department 3:**
- Name: `Finishing Department`
- Description: `Finishing and packaging`

#### 3b. Create Products (2-3 total)

In the **Products** tab:

**Product 1:**
- Code: `PROD001`
- Name: `Standard Box`
- Description: `Standard packaging box`

**Product 2:**
- Code: `PROD002`
- Name: `Premium Box`
- Description: `Premium packaging with special branding`

**Product 3:**
- Code: `PROD003`
- Name: `Custom Label`
- Description: `Custom printed labels`

#### 3c. Create Machines (3 total)

In the **Machines** tab:

**Machine 1:**
- Name: `Branding Press 1`
- Machine Number: `BP-001`
- Department: `Branding Department`
- Status: `Active`

**Machine 2:**
- Name: `Printing Press 1`
- Machine Number: `PP-001`
- Department: `Printing Department`
- Status: `Active`

**Machine 3:**
- Name: `Finishing Line 1`
- Machine Number: `FL-001`
- Department: `Finishing Department`
- Status: `Active`

✅ **Master Data Complete!**

---

### **Step 4️⃣ Test Job Planning Workflow**

**Go to:** Job Planning page (from dashboard navigation)

#### Create Your First Order:

1. Click **"New Order"** button
2. Fill in the form:
   - Order Number: `ORD-2026-001`
   - Customer Name: `Test Customer Inc.`
   - Order Value: `5000`
   - Department: `Branding Department`
   - Start Date: `2026-01-18`
   - End Date: `2026-01-25`
   - Notes: `Test order for system validation`

3. Click **"Save Order"**
4. Verify order appears in the list above the form
5. Test filters:
   - Search by order number
   - Filter by status
   - Filter by department

✅ **Job Planning Works!**

---

### **Step 5️⃣ Test Defects Workflow**

**Go to:** Defects page (from dashboard navigation)

#### Log Internal Reject:

1. Click **"New Internal Reject Ticket"** button
2. Fill in:
   - Order: `ORD-2026-001` (the one we created)
   - Quantity Rejected: `5`
   - Production Stage: `Branding`
   - Reason: `Color mismatch on first batch`

3. Click **"Save Reject"**
4. Verify reject appears in the list with status "Pending Approval"

#### Log Customer Return:

1. Click **"Log Customer Return"** button
2. Fill in:
   - Order: `ORD-2026-001`
   - Quantity Returned: `2`
   - Reason: `Customer requested different design`

3. Click **"Save Return"**
4. Verify return appears in the returns list

✅ **Defects Tracking Works!**

---

### **Step 6️⃣ Test Maintenance Workflow**

**Go to:** Maintenance page (from dashboard navigation)

#### Create Maintenance Request:

1. Click **"New Maintenance Request"** button
2. Fill in:
   - Machine: `Branding Press 1` (from dropdown)
   - Issue Description: `Press temperature sensor needs calibration`
   - Severity: `High`
   - Fault Date/Time: `2026-01-18 14:30`
   - Notes: `Last calibrated 6 months ago`

3. Click **"Create Ticket"**
4. Verify ticket appears in the list with status "Open"
5. View maintenance statistics at top

✅ **Maintenance Requests Work!**

---

### **Step 7️⃣ Test Operator Portal**

**Go to:** http://localhost:3000/templates/operator-login.html

#### Operator Login:

1. Enter Employee Number: `ADM001` (from the user we created)
2. Click **"Login"**
3. You should be redirected to operator-jobs.html
4. See:
   - List of allocated jobs
   - Quick action buttons (Start Job, End Job, Run Unallocated Job)
   - Jobs in progress table

✅ **Operator Portal Works!**

---

## 🔍 Advanced Testing

### Test API Directly (Using Swagger)

In the Swagger docs, you can test any endpoint:

#### Example: Get All Orders
1. Find **GET /api/orders**
2. Click "Try it out"
3. Add filters:
   - `status=in_progress`
   - `department_id=1`
4. Click "Execute"
5. See the JSON response

#### Example: Login User
1. Find **POST /api/auth/login**
2. Click "Try it out"
3. Paste:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
4. Click "Execute"
5. You'll get a JWT token in the response

---

## ✨ Key Workflows to Verify

### Workflow 1: Order Creation → Defect Logging → Approval
1. Create order in Job Planning
2. Log reject in Defects
3. View reject in Defects list
4. Test approval flow

### Workflow 2: Equipment Maintenance
1. Create maintenance ticket
2. Assign to technician (if available)
3. Update status through lifecycle
4. Verify history tracking

### Workflow 3: SOP/NCR (Advanced)
1. Create SOP ticket
2. Log department charged and department being charged
3. Test escalation to HOD
4. Verify audit trail

---

## 📊 Database Information

The system uses MySQL hosted on Railway:
- **Host:** shortline.proxy.rlwy.net:19278
- **Database:** railway
- **Tables created on first API call:**
  - users
  - departments
  - products
  - machines
  - orders
  - order_items
  - order_schedules
  - internal_rejects
  - customer_returns
  - maintenance_tickets
  - sop_failure_tickets
  - non_conformance_reports
  - bills_of_materials
  - audit_logs

---

## 🐛 Troubleshooting

### Issue: Login page doesn't load
- **Solution:** Make sure frontend is running on port 3000
- **Check:** http://localhost:3000/templates/login.html

### Issue: API returns 404
- **Solution:** Make sure backend is running on port 8001
- **Check:** http://127.0.0.1:8001/docs

### Issue: Cannot create user
- **Solution:** Database may need initialization
- **Try:** Make an API call to /health first to trigger initialization

### Issue: Data not persisting
- **Solution:** Check database connection string in `app/core/config.py`
- **Current setting:** Uses Railway MySQL

---

## 🚀 Next Steps

After completing all tests above:

1. ✅ Test all 6 main modules (Planning, Defects, Maintenance, SOP/NCR, Finance, Master Data)
2. ✅ Create 5-10 sample records in each module
3. ✅ Verify audit logs are recording actions
4. ✅ Test user roles and permissions
5. ✅ Review API documentation for advanced features

---

## 📞 Support

**API Documentation:** http://127.0.0.1:8001/docs  
**Frontend URL:** http://localhost:3000  
**Health Check:** http://127.0.0.1:8001/health  

---

**Status: ✅ System Ready for Testing**  
**Created:** January 18, 2026  
**Version:** 1.0.0 MVP
