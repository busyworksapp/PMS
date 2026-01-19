# Backend API Quick Reference

**API Base URL:** `http://127.0.0.1:8000`  
**API Documentation:** `http://127.0.0.1:8000/docs` (Swagger UI)  
**Backend Status:** ✅ OPERATIONAL - All endpoints working

---

## 🔐 Authentication

### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@barron.com",
  "password": "password123"
}

Response:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1,
  "role": "admin",
  "department_id": 1
}
```

### Usage - Add to Header
```
Authorization: Bearer {token}
```

---

## 📋 Core API Endpoints

### **1. ORDERS** (`/api/orders`)

```
# List orders
GET /api/orders?status=pending&skip=0&limit=100

# Get order detail
GET /api/orders/{id}

# Create order
POST /api/orders
{
  "order_number": "ORD-2026-001",
  "customer_name": "Customer A",
  "product_id": 1,
  "quantity": 100,
  "start_date": "2026-01-20T09:00:00Z",
  "end_date": "2026-01-25T17:00:00Z"
}

# Update order
PUT /api/orders/{id}
{
  "quantity": 110,
  "status": "in_progress"
}

# Schedule order to machine/department
POST /api/orders/{id}/schedule
{
  "machine_id": 1,
  "department_id": 1,
  "production_stage_id": 1,
  "scheduled_start": "2026-01-20T08:00:00Z",
  "scheduled_end": "2026-01-23T17:00:00Z"
}

# Place on hold
POST /api/orders/{id}/hold
{
  "reason": "Awaiting material",
  "expected_resume_date": "2026-01-25T08:00:00Z"
}

# Import from Excel
POST /api/orders/import/excel
Content-Type: multipart/form-data
file: orders.xlsx
mapping: {"A": "order_number", "B": "customer_name", ...}

# Import from D365
POST /api/orders/import/d365
{
  "d365_api_key": "key",
  "filters": {"status": "pending"}
}
```

---

### **2. DEFECTS** (`/api/defects`)

```
# List defects
GET /api/defects?status=open&type=internal_reject

# Create internal reject
POST /api/defects
{
  "order_id": 1,
  "defect_type": "internal_reject",
  "quantity": 5,
  "description": "Failed quality check",
  "root_cause": "Operator error",
  "created_by_user_id": 1
}

# Get defect detail
GET /api/defects/{id}

# Approve defect
POST /api/defects/{id}/approve
{
  "approved_by_user_id": 1,
  "notes": "Approved for correction"
}

# Reject defect
POST /api/defects/{id}/reject
{
  "rejected_by_user_id": 1,
  "reason": "Not verified"
}
```

---

### **3. SOP/NCR TICKETS** (`/api/sop-ncr`)

```
# List SOP tickets
GET /api/sop-ncr/sop-tickets?status=open

# Create SOP ticket (charge another department)
POST /api/sop-ncr/sop-tickets
{
  "raising_department_id": 1,
  "charged_department_id": 2,
  "sop_reference": "SOP-2024-001",
  "failure_description": "Procedure not followed",
  "impact_description": "20 units defective",
  "raised_by_user_id": 1
}

# Get ticket detail
GET /api/sop-ncr/sop-tickets/{id}

# Assign ticket
POST /api/sop-ncr/sop-tickets/{id}/assign
{
  "assigned_to_user_id": 5,
  "notes": "Review and complete NCR"
}

# Complete NCR
POST /api/sop-ncr/sop-tickets/{id}/complete-ncr
{
  "root_cause_analysis": "Root cause found",
  "corrective_actions": "Corrective action implemented",
  "preventive_measures": "Preventive measures in place",
  "completed_by_user_id": 3
}

# Reject ticket
POST /api/sop-ncr/sop-tickets/{id}/reject
{
  "rejection_reason": "Not our responsibility",
  "rejected_by_user_id": 3
}

# Escalate to HOD
POST /api/sop-ncr/sop-tickets/{id}/escalate-to-hod
{
  "escalation_reason": "Ticket not addressed",
  "escalated_by_user_id": 2
}

# HOD decision
POST /api/sop-ncr/sop-tickets/{id}/hod-decision
{
  "decision": "Quality Dept is responsible",
  "final_responsible_department_id": 3,
  "action": "complete_ncr",
  "decided_by_hod_user_id": 10
}

# Get SOP dashboard
GET /api/sop-ncr/sop-dashboard?department_id=1
```

---

### **4. MAINTENANCE** (`/api/maintenance`)

```
# List maintenance tickets
GET /api/maintenance/tickets?status=open

# Create maintenance ticket
POST /api/maintenance/tickets
{
  "machine_id": 1,
  "issue_description": "Motor overheating",
  "priority": "high",
  "reported_by_user_id": 1,
  "maintenance_type": "corrective"
}

# Get ticket detail
GET /api/maintenance/tickets/{id}

# Assign ticket
POST /api/maintenance/tickets/{id}/assign
{
  "assigned_to_user_id": 5,
  "target_completion_date": "2026-01-20T17:00:00Z"
}

# Update status
PUT /api/maintenance/tickets/{id}
{
  "status": "in_progress",
  "work_log": "Started diagnostics"
}

# Complete ticket
POST /api/maintenance/tickets/{id}/complete
{
  "completion_notes": "Replaced motor, tested successfully",
  "work_hours": 4,
  "completed_by_user_id": 5
}

# Get maintenance history
GET /api/maintenance/tickets/{machine_id}/history
```

---

### **5. FINANCE/BOM** (`/api/finance`)

```
# List BOMs
GET /api/finance/boms

# Get BOM detail
GET /api/finance/boms/{id}

# Create BOM
POST /api/finance/boms
{
  "product_id": 1,
  "total_material_cost": 50.00,
  "total_labor_cost": 25.00,
  "overhead_allocation": 15.00
}

# Add component to BOM
POST /api/finance/boms/{id}/components
{
  "raw_material_id": 1,
  "quantity": 10,
  "unit_cost": 5.00,
  "description": "Main component"
}

# Get product cost analysis
GET /api/finance/products/{id}/cost-analysis
```

---

### **6. MASTER DATA** (`/api/master`)

```
# List departments
GET /api/master/departments

# Create department
POST /api/master/departments
{
  "name": "Cutting",
  "description": "Order cutting section",
  "manager_id": 1
}

# List products
GET /api/master/products

# Create product
POST /api/master/products
{
  "name": "T-Shirt",
  "description": "Cotton T-Shirt",
  "code": "TSH-001",
  "category": "apparel"
}

# List machines
GET /api/master/machines

# Create machine
POST /api/master/machines
{
  "name": "Cutting Machine 1",
  "machine_type": "cutter",
  "department_id": 1,
  "capacity": 500
}

# List users
GET /api/master/users

# Create user
POST /api/master/users
{
  "email": "operator@barron.com",
  "password": "password123",
  "full_name": "John Operator",
  "role": "operator",
  "department_id": 1
}
```

---

## 🔄 Common Workflows

### Create Order → Schedule → Track → Complete

```
1. POST /api/orders                    Create order
2. POST /api/orders/{id}/schedule      Schedule to machine
3. PUT /api/orders/{id}                Update status to in_progress
4. GET /api/orders/{id}                Check progress
5. PUT /api/orders/{id}                Mark complete
```

### Raise SOP Ticket → Respond → Complete NCR

```
1. POST /api/sop-ncr/sop-tickets                   Create ticket
2. POST /api/sop-ncr/sop-tickets/{id}/assign      Assign to responder
3. POST /api/sop-ncr/sop-tickets/{id}/complete-ncr Complete NCR (resolves)
OR
2. POST /api/sop-ncr/sop-tickets/{id}/reject      Reject (escalates)
3. POST /api/sop-ncr/sop-tickets/{id}/escalate-to-hod Escalate
4. POST /api/sop-ncr/sop-tickets/{id}/hod-decision HOD decides
```

### Log Defect → Get Approval → Fix

```
1. POST /api/defects                   Log internal reject
2. GET /api/defects/{id}              Check status
3. POST /api/defects/{id}/approve     Get approval
4. Implement corrective action
5. PUT /api/orders/{id}               Update order status
```

---

## 🛠️ JavaScript Example Usage

```javascript
// Initialize API client
const api = new APIClient('http://127.0.0.1:8000');

// Login
async function login() {
    const response = await api.post('/api/auth/login', {
        email: 'admin@barron.com',
        password: 'password123'
    });
    api.setToken(response.token);
    localStorage.setItem('auth_token', response.token);
}

// Get orders
async function getOrders() {
    const orders = await api.get('/api/orders?status=pending');
    return orders;
}

// Create order
async function createOrder() {
    const order = await api.post('/api/orders', {
        order_number: 'ORD-2026-001',
        customer_name: 'Customer A',
        product_id: 1,
        quantity: 100,
        start_date: new Date().toISOString(),
        end_date: new Date(Date.now() + 5*24*60*60*1000).toISOString()
    });
    return order;
}

// Schedule order
async function scheduleOrder(orderId) {
    const scheduled = await api.post(
        `/api/orders/${orderId}/schedule`,
        {
            machine_id: 1,
            department_id: 1,
            production_stage_id: 1,
            scheduled_start: new Date().toISOString(),
            scheduled_end: new Date(Date.now() + 3*24*60*60*1000).toISOString()
        }
    );
    return scheduled;
}

// Create SOP ticket
async function createSOPTicket() {
    const ticket = await api.post('/api/sop-ncr/sop-tickets', {
        raising_department_id: 1,
        charged_department_id: 2,
        sop_reference: 'SOP-2024-001',
        failure_description: 'Failed quality check',
        impact_description: '20 units defective',
        raised_by_user_id: 1
    });
    return ticket;
}

// Get maintenance dashboard
async function getMaintenance() {
    const tickets = await api.get('/api/maintenance/tickets?status=open');
    return tickets;
}
```

---

## 📊 Response Format

All endpoints return:

```json
{
  "success": true,
  "data": {},           // Actual response data
  "message": "Success", // Human-readable message
  "timestamp": "2026-01-18T10:30:00Z"
}
```

Error response:

```json
{
  "success": false,
  "data": null,
  "message": "Order not found",
  "timestamp": "2026-01-18T10:30:00Z"
}
```

---

## 🐛 Debugging Tips

### Check Console Errors
```javascript
// In browser DevTools
console.log('Response:', data);
console.error('Error:', error);
```

### Test API Directly
```bash
# Linux/Mac
curl -H "Authorization: Bearer {token}" \
  http://127.0.0.1:8000/api/orders

# PowerShell
$headers = @{Authorization = "Bearer {token}"}
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/orders" `
  -Headers $headers
```

### View Server Logs
```bash
# Terminal where server is running
# Shows all requests, errors, performance
```

### Check API Docs
Open `http://127.0.0.1:8000/docs` to see:
- All endpoints
- Request/response schemas
- Try-it-out interface
- Error codes

---

## 🚀 Common Tasks

### Display orders in table
```javascript
const orders = await api.get('/api/orders');
const table = document.getElementById('orders-table');
orders.forEach(order => {
    const row = table.insertRow();
    row.insertCell(0).textContent = order.order_number;
    row.insertCell(1).textContent = order.customer_name;
    row.insertCell(2).textContent = order.status;
});
```

### Handle errors
```javascript
try {
    const order = await api.post('/api/orders', data);
} catch (error) {
    console.error('Failed to create order:', error.message);
    // Show error to user
}
```

### Auto-refresh data
```javascript
setInterval(async () => {
    const orders = await api.get('/api/orders');
    updateUI(orders);
}, 5000); // Refresh every 5 seconds
```

### Filter in UI
```javascript
const orders = await api.get(`/api/orders?status=${selectedStatus}`);
displayOrders(orders);
```

---

## 📞 Support

- **API Docs:** `http://127.0.0.1:8000/docs`
- **System Status:** See `SYSTEM_STATUS.md`
- **Development Guide:** See `FRONTEND_DEVELOPMENT_GUIDE.md`
- **Architecture Details:** See `ARCHITECTURE.md`

All endpoints are fully documented and ready to use!

