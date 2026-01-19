# Frontend Development Guide

**Status:** 🔴 **CRITICAL PATH** - NOT STARTED  
**Priority:** 🔴 **HIGHEST** - Required to make system usable  
**Estimated Effort:** 1-2 weeks for 1-2 developers  
**Tech Stack:** Pure HTML/CSS/JavaScript (no frameworks)

---

## 🎯 Frontend Development Requirements

The system must have a **production-floor-ready interface** with an industrial design aesthetic.

### Design Principles

1. **No JavaScript Frameworks** - Use vanilla JS (Fetch API for HTTP calls)
2. **No CSS Frameworks** - Use vanilla CSS (responsive, mobile-first)
3. **Industrial Design** - High-contrast colors, serious appearance, production-floor ready
4. **Mobile-First** - Operators need mobile access to job tracking
5. **HTML Semantics** - Pure HTML5 with proper structure
6. **Separation of Concerns** - HTML (structure), CSS (styling), JS (logic)

### Color Scheme (Industrial/Factory Theme)

```css
/* Primary Colors */
--primary: #1a1a1a;      /* Dark gray/black */
--secondary: #ff6b35;    /* Orange (safety/warning) */
--accent: #00a86b;       /* Green (success/operational) */
--danger: #dc143c;       /* Red (alerts/errors) */
--warning: #ffa500;      /* Orange (caution) */
--info: #0066cc;         /* Blue (information) */

/* Background/Text */
--bg-dark: #0d0d0d;
--bg-light: #f5f5f5;
--text-dark: #1a1a1a;
--text-light: #ffffff;
--border: #cccccc;
```

### Layout Structure

All pages should follow this responsive layout:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barron Production Management</title>
    <link rel="stylesheet" href="/css/global.css">
    <link rel="stylesheet" href="/css/theme.css">
</head>
<body>
    <!-- Header/Nav -->
    <header>
        <nav class="navbar"></nav>
    </header>

    <!-- Main Content -->
    <main class="container">
        <!-- Page content here -->
    </main>

    <!-- Footer -->
    <footer>
        <p>&copy; 2026 Barron Manufacturing</p>
    </footer>

    <!-- Global JavaScript -->
    <script src="/js/api.js"></script>
    <script src="/js/auth.js"></script>
    <script src="/js/app.js"></script>
</body>
</html>
```

---

## 📄 9 Pages to Build (Priority Order)

### **1. LOGIN PAGE** (Priority: CRITICAL)

**File:** `/frontend/login.html`

**Purpose:** Authenticate users, issue JWT tokens

**Components:**
- Login form (email/password)
- Password reset link
- Remember me checkbox
- Error messages
- Loading state

**API Integration:**
```javascript
// POST /api/auth/login
// Request: { email, password }
// Response: { token, user_id, role, department_id }
```

**Wireframe:**
```
┌─────────────────────────────┐
│     BARRON MFG              │
│  Production Management      │
├─────────────────────────────┤
│                             │
│   ┌─────────────────────┐   │
│   │ Email/Username  [_] │   │
│   │ Password        [_] │   │
│   │                     │   │
│   │ [Login Button]      │   │
│   │ Remember Me     [☐] │   │
│   └─────────────────────┘   │
│                             │
│   Forgot Password?          │
└─────────────────────────────┘
```

---

### **2. DASHBOARD (Production Overview)** (Priority: CRITICAL)

**File:** `/frontend/dashboard.html`

**Purpose:** Real-time view of production status, capacity, alerts

**Components:**
- **Summary Cards:**
  - Total Orders (count, on-time %)
  - Capacity Utilization (bar chart)
  - Active Issues (defects, maintenance)
  - SLA Breaches (count)

- **Status Table:**
  - Recent orders with status
  - Machine utilization
  - Department workload

- **Charts:**
  - Order timeline (bar/Gantt-style)
  - Capacity by department (pie chart)
  - Defects by type (bar chart)

- **Alerts Section:**
  - Overdue orders
  - SLA breaches
  - Equipment down
  - Critical defects

**API Integration:**
```javascript
// GET /api/jobs/dashboard/planning
// Returns: summary, orders, capacity, alerts
```

---

### **3. ORDER MANAGEMENT** (Priority: CRITICAL)

**Files:** `/frontend/orders.html`, `/frontend/order-detail.html`, `/frontend/order-create.html`

**Purpose:** Create, schedule, track orders

**Sub-pages:**

#### 3a. Order List
- Search/filter by:
  - Order number
  - Customer name
  - Status (pending, scheduled, in-progress, completed)
  - Date range
  - Department

- Table columns:
  - Order #
  - Customer
  - Product
  - Quantity
  - Status
  - Start Date
  - End Date
  - Progress %
  - Actions (View, Edit, Schedule)

- Bulk Actions:
  - Export to Excel
  - Import from Excel
  - Schedule multiple

**API Integration:**
```javascript
// GET /api/jobs/orders (with filters)
// POST /api/jobs/orders/import/excel
```

#### 3b. Order Detail
- Display:
  - Order info (number, customer, product, qty, value)
  - Schedule (start/end, scheduled/actual)
  - Line items (products with quantities)
  - Assigned machines/departments
  - Production stages
  - Timeline/history
  - Defects/exceptions
  - Status changes

- Actions:
  - Edit order details
  - Reschedule
  - Add items
  - Place on hold
  - Complete order
  - View timeline

**API Integration:**
```javascript
// GET /api/jobs/orders/{id}
// PUT /api/jobs/orders/{id}
// POST /api/jobs/orders/{id}/schedule
// POST /api/jobs/orders/{id}/hold
```

#### 3c. Create Order
- Form fields:
  - Order number (auto-generated or manual)
  - Customer name
  - Product (dropdown from master data)
  - Quantity
  - Order value
  - Start/end dates
  - Notes

- Actions:
  - Save & Schedule Next
  - Save & Add Items
  - Import from Excel/D365

**API Integration:**
```javascript
// POST /api/jobs/orders
// GET /api/master/products (for dropdown)
```

---

### **4. PRODUCTION SCHEDULING** (Priority: HIGH)

**File:** `/frontend/scheduling.html`

**Purpose:** Allocate orders to machines/departments with timeline

**Components:**

- **Machine/Dept Grid:**
  - Rows: Machines/Departments
  - Columns: Time slots (hourly/daily/weekly)
  - Cells: Orders assigned (color-coded by status)
  - Show: Order #, duration, status

- **Capacity View:**
  - Utilization % for each resource
  - Available capacity indicators
  - Color coding (green=optimal, red=overload)

- **Drag & Drop:**
  - Drag orders to different machines
  - Automatic conflict detection
  - Immediate capacity recalculation

- **Timeline:**
  - Gantt chart view
  - Critical path highlighting
  - Bottleneck identification

**API Integration:**
```javascript
// GET /api/jobs/capacity
// POST /api/jobs/orders/{id}/schedule
// POST /api/jobs/orders/{id}/reallocate
```

---

### **5. DEFECTS MANAGEMENT** (Priority: HIGH)

**Files:** `/frontend/defects.html`, `/frontend/defect-detail.html`, `/frontend/defect-create.html`

**Purpose:** Log, track, and resolve internal rejects and customer returns

**Sub-pages:**

#### 5a. Defect List
- Filter by:
  - Type (internal reject, customer return)
  - Status (open, approved, closed)
  - Department
  - Date range

- Table columns:
  - Defect ID
  - Type
  - Order #
  - Description
  - Quantity
  - Status
  - Assigned To
  - Due Date
  - Actions

#### 5b. Defect Detail
- Display:
  - Defect info
  - Affected order
  - Root cause analysis
  - Corrective actions
  - Approval history
  - Replacement status

- Actions:
  - Approve/Reject
  - Assign corrective action
  - Update status
  - Add notes

**API Integration:**
```javascript
// GET /api/defects
// POST /api/defects
// PUT /api/defects/{id}
```

---

### **6. SOP/NCR TICKET TRACKING** (Priority: HIGH)

**Files:** `/frontend/sop-tickets.html`, `/frontend/sop-detail.html`, `/frontend/sop-create.html`

**Purpose:** Inter-departmental SOP compliance tracking and NCR completion

**Sub-pages:**

#### 6a. SOP Ticket List
- Filter by:
  - Status (open, assigned, escalated, closed)
  - Charged department
  - Raising department
  - Priority

- Table columns:
  - Ticket #
  - SOP Reference
  - Raising Dept
  - Charged Dept
  - Status
  - Created Date
  - Actions

#### 6b. SOP Ticket Detail
- Display:
  - Ticket number & status
  - SOP reference
  - Failure description
  - Impact analysis
  - Charged department
  - Escalation history
  - NCR details (if completed)
  - Audit trail

- Actions (vary by status):
  - **Open:** Assign, Reject, Reassign
  - **Assigned:** Complete NCR, Escalate to HOD
  - **Escalated:** HOD decision button
  - **Closed:** View readonly

**API Integration:**
```javascript
// GET /api/sop-ncr/sop-tickets
// POST /api/sop-ncr/sop-tickets
// POST /api/sop-ncr/sop-tickets/{id}/assign
// POST /api/sop-ncr/sop-tickets/{id}/complete-ncr
```

---

### **7. MAINTENANCE MANAGEMENT** (Priority: MEDIUM)

**Files:** `/frontend/maintenance.html`, `/frontend/maintenance-detail.html`, `/frontend/maintenance-create.html`

**Purpose:** Equipment maintenance ticket lifecycle

**Sub-pages:**

#### 7a. Maintenance Ticket List
- Filter by:
  - Status (open, assigned, in-progress, closed)
  - Machine
  - Priority (critical, high, medium, low)
  - SLA status (on-track, at-risk, breached)

- Table columns:
  - Ticket #
  - Machine
  - Issue
  - Priority
  - Status
  - Assigned To
  - SLA Target
  - Days Open
  - Actions

#### 7b. Maintenance Detail
- Display:
  - Ticket details
  - Machine info
  - Issue description
  - Priority & SLA
  - Assignment history
  - Work log
  - Completion status

- Actions:
  - Assign to technician
  - Update status
  - Log work hours
  - Mark complete

**API Integration:**
```javascript
// GET /api/maintenance/tickets
// POST /api/maintenance/tickets
// PUT /api/maintenance/tickets/{id}
```

---

### **8. FINANCE & BOM MANAGEMENT** (Priority: MEDIUM)

**File:** `/frontend/finance.html`

**Purpose:** Bill of Materials creation and cost tracking

**Components:**

- **BOM List:**
  - Product BOMs
  - Total cost per unit
  - Component breakdown
  - Material cost vs labor
  - Profitability analysis

- **BOM Detail:**
  - Components (with quantities, unit costs)
  - Total material cost
  - Labor cost
  - Overhead allocation
  - Product selling price
  - Profit margin

- **Cost Analysis:**
  - Cost by component
  - Cost by department
  - Trend analysis

- **Actions:**
  - Create new BOM
  - Edit BOM
  - View product profitability
  - Export cost report

**API Integration:**
```javascript
// GET /api/finance/boms
// POST /api/finance/boms
// GET /api/finance/boms/{id}
```

---

### **9. OPERATOR MOBILE PORTAL** (Priority: MEDIUM)

**File:** `/frontend/operator-portal.html` (Responsive, mobile-first)

**Purpose:** Operators track assigned jobs and update status

**Components:**

- **My Jobs (Simplified):**
  - List of assigned jobs
  - Current status
  - Remaining quantity
  - Step-by-step instructions
  - One-click status update

- **Job Detail (Mobile):**
  - Job #
  - Product info
  - Instructions
  - Current progress
  - Quantity input
  - Issue reporting button

- **Issue Report:**
  - Log problems
  - Suggest solutions
  - Submit for review

- **My Stats:**
  - Jobs completed today
  - Efficiency %
  - Quality metrics

**Mobile Optimizations:**
- Touch-friendly buttons
- Large input fields
- Minimal scrolling
- Landscape/portrait support
- Offline capability (caching)

**API Integration:**
```javascript
// GET /api/operators/jobs (assigned to user)
// POST /api/operators/jobs/{id}/update-quantity
// POST /api/operators/jobs/{id}/report-issue
```

---

### **BONUS: 10. ADMIN CONFIGURATION PANEL** (Priority: LOW for MVP)

**File:** `/frontend/admin.html`

**Purpose:** System configuration, form builder, workflow management

**Components:**

- **System Settings:**
  - Database connection
  - API endpoints
  - Email configuration
  - Audit settings

- **Dynamic Forms:**
  - Form field configuration
  - Validation rules
  - Display options

- **Workflows:**
  - SOP ticket routing rules
  - Approval workflows
  - Escalation policies

- **User Management:**
  - Create/edit users
  - Assign roles
  - Department assignment

- **Audit Logs:**
  - View all system changes
  - Filter by user/date/action
  - Export audit trail

**API Integration:**
```javascript
// GET /api/admin/settings
// POST /api/admin/forms
// GET /api/admin/audit-logs
```

---

## 🛠️ JavaScript Modules to Build

### 1. **API Communication Module** (`/js/api.js`)

```javascript
// Generic HTTP client for all API calls
class APIClient {
    constructor(baseUrl = 'http://127.0.0.1:8000') {
        this.baseUrl = baseUrl;
        this.token = localStorage.getItem('auth_token');
    }

    async get(endpoint) {
        // GET request with auth
    }

    async post(endpoint, data) {
        // POST request with auth
    }

    async put(endpoint, data) {
        // PUT request with auth
    }

    async delete(endpoint) {
        // DELETE request with auth
    }

    setToken(token) {
        // Update token after login
    }
}

const api = new APIClient();
```

### 2. **Authentication Module** (`/js/auth.js`)

```javascript
class Auth {
    async login(email, password) {
        // Login and store token
    }

    async logout() {
        // Clear token and redirect
    }

    isAuthenticated() {
        // Check if user logged in
    }

    getToken() {
        // Retrieve stored token
    }

    redirectIfNotAuth() {
        // Redirect to login if needed
    }
}
```

### 3. **Dynamic Form Renderer** (`/js/forms.js`)

```javascript
// Render forms from JSON configuration
class FormRenderer {
    renderForm(jsonConfig) {
        // Create form HTML from JSON
        // Support: text, email, number, select, checkbox, textarea
    }

    getFormData() {
        // Extract form values
    }

    validate() {
        // Client-side validation
    }
}
```

### 4. **State Management** (`/js/state.js`)

```javascript
// Simple state store for app data
class StateManager {
    constructor() {
        this.state = {
            user: null,
            currentOrder: null,
            orders: [],
            defects: [],
            filters: {}
        };
    }

    setState(path, value) {
        // Update state
    }

    getState(path) {
        // Get state value
    }

    subscribe(path, callback) {
        // Subscribe to state changes
    }
}
```

### 5. **Table Component** (`/js/table.js`)

```javascript
// Reusable table with sorting, pagination, search
class DataTable {
    constructor(element, columns, data) {
        this.render(columns, data);
    }

    render(columns, data) {
        // Render table HTML
    }

    sort(column) {
        // Sort by column
    }

    filter(query) {
        // Filter rows
    }

    paginate(page, pageSize) {
        // Pagination
    }
}
```

---

## 🎨 CSS Structure

### File Organization

```
/css/
├── global.css          # Reset, typography, utility classes
├── theme.css           # Color scheme, variables
├── layout.css          # Grid, flexbox, containers
├── components.css      # Buttons, forms, cards, tables
├── pages/
│   ├── login.css
│   ├── dashboard.css
│   ├── orders.css
│   ├── defects.css
│   └── ...
└── responsive.css      # Mobile breakpoints
```

### Global Styles Example

```css
:root {
    --primary: #1a1a1a;
    --secondary: #ff6b35;
    --accent: #00a86b;
    --danger: #dc143c;
    --padding-sm: 0.5rem;
    --padding-md: 1rem;
    --padding-lg: 2rem;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background-color: var(--bg-light);
    color: var(--text-dark);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--padding-md);
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: var(--padding-sm);
    }
}
```

---

## 📱 Responsive Breakpoints

```css
/* Desktop First Approach */
@media (max-width: 1024px) {
    /* Tablets */
}

@media (max-width: 768px) {
    /* Mobile landscape */
}

@media (max-width: 480px) {
    /* Mobile portrait */
}
```

---

## 🔄 Development Workflow

### Step 1: Setup Frontend Directory
```bash
mkdir -p frontend/{html,css,js}
```

### Step 2: Create Base Files
- `frontend/index.html` (login/redirect)
- `frontend/css/global.css`
- `frontend/js/api.js`

### Step 3: Build Each Page
For each page:
1. Create HTML structure
2. Add page-specific CSS
3. Add page-specific JavaScript
4. Test with live API

### Step 4: Integration
- Connect pages together
- Test full workflows
- Optimize performance

### Step 5: Deploy
- Move frontend to `app/frontend`
- Configure web server
- Test in production

---

## 🚀 Quick Start Commands

```bash
# 1. Create HTML file
# File: frontend/index.html
# Content: Basic login template

# 2. Create CSS file
# File: frontend/css/global.css
# Content: Industrial design system

# 3. Create JS file
# File: frontend/js/api.js
# Content: API communication layer

# 4. Test in browser
# Open: http://127.0.0.1:8000/frontend/

# 5. Check API responses
# Open: http://127.0.0.1:8000/docs
```

---

## 📊 Estimated Timeline

| Page | Hours | Priority | Blocker |
|------|-------|----------|---------|
| Login | 2 | CRITICAL | API ready ✓ |
| Dashboard | 4 | CRITICAL | API ready ✓ |
| Order Mgmt | 6 | CRITICAL | API ready ✓ |
| Scheduling | 5 | HIGH | Gantt library needed |
| Defects | 4 | HIGH | API ready ✓ |
| SOP/NCR | 5 | HIGH | API ready ✓ |
| Maintenance | 4 | MEDIUM | API ready ✓ |
| Finance | 3 | MEDIUM | API ready ✓ |
| Operator Portal | 4 | MEDIUM | API ready ✓ |
| Admin Panel | 5 | LOW | Can skip for MVP |
| **CSS System** | 8 | CRITICAL | Needed for all pages |
| **JS Modules** | 6 | CRITICAL | Needed for all pages |
| **Total** | **56 hours** | | **~1.5-2 weeks** |

---

## ✅ Success Criteria

### Frontend is "done" when:
- ✅ Login page works and authenticates
- ✅ Dashboard shows real data from API
- ✅ Users can create orders
- ✅ Users can schedule orders
- ✅ Users can track defects
- ✅ SOP/NCR workflow functional
- ✅ Mobile responsive (operators can use tablets)
- ✅ No console errors
- ✅ API calls complete in <1 second
- ✅ Works in Chrome, Firefox, Safari

---

## 🎯 Start Here

**Recommended first build: Login page**

1. Create `/frontend/login.html`
2. Create `/frontend/css/global.css` with industrial design
3. Create `/frontend/js/api.js` with authentication
4. Test login flow
5. Build dashboard next

---

## 📚 References

- **API Docs:** http://127.0.0.1:8000/docs
- **System Status:** See `SYSTEM_STATUS.md`
- **Architecture:** See `ARCHITECTURE.md`

The entire backend is ready. **Focus on building the UI!**

