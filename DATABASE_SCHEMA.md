# Database Schema Reference

**Database:** Railway MySQL  
**Host:** shortline.proxy.rlwy.net:19278  
**Database Name:** th_db  
**Tables:** 18  
**Status:** ✅ Fully Initialized with Sample Data

---

## Core Tables

### `users`
User accounts with role-based access

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role ENUM('admin', 'manager', 'supervisor', 'operator', 'technician'),
    department_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

Sample Data:
```
ID | Email | Role | Department | Active
1  | admin@barron.com | admin | - | YES
2  | manager1@barron.com | manager | 1 (Cutting) | YES
```

---

### `departments`
Manufacturing departments/sections

```sql
CREATE TABLE departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    manager_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(id)
);
```

Sample Data:
```
ID | Name | Description | Manager
1  | Cutting | Order cutting section | 2
2  | Stitching | Order stitching section | NULL
3  | Packing | Order packing section | NULL
```

---

### `products`
Manufactured products/SKUs

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    code VARCHAR(100) UNIQUE,
    category VARCHAR(50),
    standard_cost DECIMAL(10, 2),
    standard_hours DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

Sample Data:
```
ID | Name | Code | Category | Cost
1  | T-Shirt | TSH-001 | Apparel | 5.00
2  | Polo Shirt | POL-001 | Apparel | 7.50
3  | Jacket | JAC-001 | Apparel | 15.00
```

---

### `machines`
Manufacturing machines/equipment

```sql
CREATE TABLE machines (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    machine_type VARCHAR(50),
    department_id INT NOT NULL,
    capacity INT,
    is_operational BOOLEAN DEFAULT TRUE,
    last_maintenance DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

Sample Data:
```
ID | Name | Type | Department | Capacity
1  | Cutter-1 | cutter | 1 | 500
2  | Stitcher-1 | stitcher | 2 | 300
3  | Packer-1 | packer | 3 | 400
```

---

## Order Management Tables

### `orders`
Main order/job records

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(100) UNIQUE NOT NULL,
    sales_order_number VARCHAR(100),
    customer_name VARCHAR(255) NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    order_value DECIMAL(12, 2),
    status VARCHAR(50) DEFAULT 'pending',
    source VARCHAR(50),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    scheduled_start DATETIME,
    scheduled_end DATETIME,
    actual_start DATETIME,
    actual_end DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

Statuses: `pending`, `scheduled`, `in_progress`, `on_hold`, `completed`, `cancelled`

---

### `order_items`
Line items within orders

```sql
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT,
    quantity INT NOT NULL,
    assigned_machine_id INT,
    assigned_department_id INT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (assigned_machine_id) REFERENCES machines(id),
    FOREIGN KEY (assigned_department_id) REFERENCES departments(id)
);
```

---

### `order_schedules`
Machine/department allocation for orders

```sql
CREATE TABLE order_schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    machine_id INT NOT NULL,
    department_id INT NOT NULL,
    production_stage_id INT,
    sequence_number INT,
    scheduled_start DATETIME,
    scheduled_end DATETIME,
    actual_start DATETIME,
    actual_end DATETIME,
    duration_hours DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (machine_id) REFERENCES machines(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (production_stage_id) REFERENCES production_stages(id)
);
```

---

### `production_stages`
Department-specific production stages

```sql
CREATE TABLE production_stages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    department_id INT NOT NULL,
    stage_number INT,
    is_required BOOLEAN DEFAULT TRUE,
    standard_hours DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

Sample Data:
```
ID | Name | Department | Number
1  | Cutting | 1 | 1
2  | Stitching | 2 | 2
3  | Packing | 3 | 3
```

---

### `capacity_targets`
Daily/weekly/monthly capacity targets

```sql
CREATE TABLE capacity_targets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    department_id INT NOT NULL,
    machine_id INT,
    target_quantity INT,
    period VARCHAR(50), -- 'daily', 'weekly', 'monthly'
    period_date DATE,
    achieved_quantity INT DEFAULT 0,
    utilization_percent DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (machine_id) REFERENCES machines(id)
);
```

---

### `order_exceptions`
Orders on hold or with issues

```sql
CREATE TABLE order_exceptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    exception_type VARCHAR(50), -- 'on_hold', 'delayed', 'quality_issue'
    reason TEXT NOT NULL,
    raised_by_user_id INT,
    expected_resume_date DATETIME,
    resolved_date DATETIME,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (raised_by_user_id) REFERENCES users(id)
);
```

---

## Quality Management Tables

### `internal_rejects`
Internal defect/reject tracking

```sql
CREATE TABLE internal_rejects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    order_item_id INT,
    defect_type VARCHAR(50), -- 'internal_reject', 'customer_return'
    quantity INT NOT NULL,
    description TEXT,
    root_cause TEXT,
    impact_description TEXT,
    correction_action TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'replacement_processed', 'closed'
    approved_by_user_id INT,
    approved_date DATETIME,
    created_by_user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (order_item_id) REFERENCES order_items(id),
    FOREIGN KEY (approved_by_user_id) REFERENCES users(id),
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);
```

---

### `customer_returns`
Customer return documentation

```sql
CREATE TABLE customer_returns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    return_quantity INT NOT NULL,
    return_reason TEXT,
    received_date DATETIME,
    inspection_date DATETIME,
    defect_analysis TEXT,
    replacement_order_id INT,
    status VARCHAR(50) DEFAULT 'received',
    created_by_user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (replacement_order_id) REFERENCES orders(id),
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);
```

---

## SOP/NCR Tables

### `sop_tickets`
Inter-departmental SOP failure tickets

```sql
CREATE TABLE sop_tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    sop_reference VARCHAR(100),
    raising_department_id INT NOT NULL,
    charged_department_id INT NOT NULL,
    failure_description TEXT NOT NULL,
    impact_description TEXT,
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'assigned', 'rejected', 'reassigned', 'escalated_to_hod', 'closed'
    raised_by_user_id INT,
    assigned_to_user_id INT,
    reassigned_to_department_id INT,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (raising_department_id) REFERENCES departments(id),
    FOREIGN KEY (charged_department_id) REFERENCES departments(id),
    FOREIGN KEY (reassigned_to_department_id) REFERENCES departments(id),
    FOREIGN KEY (raised_by_user_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id)
);
```

Status Workflow:
```
OPEN → ASSIGNED → (COMPLETED or REJECTED)
                     ↓
                   ESCALATED_TO_HOD → HOD_DECISION_PENDING → REASSIGNED or CLOSED
```

---

### `ncr_reports`
Non-Conformance Report completion

```sql
CREATE TABLE ncr_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sop_ticket_id INT NOT NULL,
    root_cause_analysis TEXT NOT NULL,
    corrective_actions TEXT NOT NULL,
    preventive_measures TEXT NOT NULL,
    completed_by_user_id INT,
    completion_date DATETIME,
    effectiveness_review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sop_ticket_id) REFERENCES sop_tickets(id),
    FOREIGN KEY (completed_by_user_id) REFERENCES users(id)
);
```

---

## Maintenance Tables

### `maintenance_tickets`
Equipment maintenance request tracking

```sql
CREATE TABLE maintenance_tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    machine_id INT NOT NULL,
    issue_description TEXT NOT NULL,
    priority VARCHAR(50), -- 'critical', 'high', 'medium', 'low'
    maintenance_type VARCHAR(50), -- 'preventive', 'corrective', 'emergency'
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'assigned', 'in_progress', 'closed'
    reported_by_user_id INT,
    assigned_to_user_id INT,
    target_completion_date DATETIME,
    actual_completion_date DATETIME,
    work_log TEXT,
    estimated_hours DECIMAL(10, 2),
    actual_hours DECIMAL(10, 2),
    sla_status VARCHAR(50), -- 'on_track', 'at_risk', 'breached'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machines(id),
    FOREIGN KEY (reported_by_user_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to_user_id) REFERENCES users(id)
);
```

---

### `maintenance_history`
Historical maintenance records

```sql
CREATE TABLE maintenance_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    machine_id INT NOT NULL,
    maintenance_date DATETIME,
    maintenance_type VARCHAR(50),
    description TEXT,
    hours_spent DECIMAL(10, 2),
    technician_id INT,
    cost DECIMAL(10, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (machine_id) REFERENCES machines(id),
    FOREIGN KEY (technician_id) REFERENCES users(id)
);
```

---

## Finance Tables

### `bills_of_materials`
Product Bill of Materials (cost structure)

```sql
CREATE TABLE bills_of_materials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    version INT DEFAULT 1,
    effective_date DATE,
    total_material_cost DECIMAL(12, 2),
    total_labor_cost DECIMAL(12, 2),
    total_overhead DECIMAL(12, 2),
    total_cost DECIMAL(12, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_by_user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);
```

---

### `bom_components`
Components within a BOM

```sql
CREATE TABLE bom_components (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bom_id INT NOT NULL,
    raw_material_id INT,
    quantity DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50),
    unit_cost DECIMAL(12, 2),
    total_cost DECIMAL(12, 2),
    supplier_id INT,
    lead_time_days INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bom_id) REFERENCES bills_of_materials(id),
    FOREIGN KEY (supplier_id) REFERENCES users(id)
);
```

---

## System Tables

### `audit_logs`
Complete audit trail of all changes

```sql
CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entity_type VARCHAR(50), -- 'order', 'defect', 'sop_ticket', 'maintenance'
    entity_id INT,
    action VARCHAR(50), -- 'create', 'update', 'delete', 'approve'
    old_values JSON,
    new_values JSON,
    changed_by_user_id INT,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    remarks TEXT,
    FOREIGN KEY (changed_by_user_id) REFERENCES users(id),
    INDEX (entity_type, entity_id, change_timestamp)
);
```

---

### `form_configs`
Dynamic form configuration (JSON)

```sql
CREATE TABLE form_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    form_name VARCHAR(100) UNIQUE NOT NULL,
    form_type VARCHAR(50), -- 'order_entry', 'defect_report', 'sop_ticket'
    description TEXT,
    fields JSON, -- Array of field definitions
    validation_rules JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_by_user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);
```

Example JSON:
```json
{
  "fields": [
    {
      "name": "order_number",
      "type": "text",
      "label": "Order Number",
      "required": true,
      "validation": "alphanumeric"
    },
    {
      "name": "customer_name",
      "type": "text",
      "label": "Customer Name",
      "required": true
    }
  ]
}
```

---

### `workflow_configs`
Workflow and escalation rules (JSON)

```sql
CREATE TABLE workflow_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    workflow_name VARCHAR(100) UNIQUE NOT NULL,
    workflow_type VARCHAR(50), -- 'sop_ticket', 'defect_approval'
    description TEXT,
    stages JSON, -- Array of workflow stages
    escalation_rules JSON, -- SLA and escalation conditions
    is_active BOOLEAN DEFAULT TRUE,
    created_by_user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id)
);
```

---

## Index Strategy

```sql
-- Performance indexes
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_customer ON orders(customer_name);
CREATE INDEX idx_order_schedules_machine ON order_schedules(machine_id);
CREATE INDEX idx_order_schedules_dates ON order_schedules(scheduled_start, scheduled_end);
CREATE INDEX idx_defects_order ON internal_rejects(order_id);
CREATE INDEX idx_defects_status ON internal_rejects(status);
CREATE INDEX idx_sop_tickets_status ON sop_tickets(status);
CREATE INDEX idx_sop_tickets_department ON sop_tickets(charged_department_id);
CREATE INDEX idx_maintenance_machine ON maintenance_tickets(machine_id);
CREATE INDEX idx_maintenance_status ON maintenance_tickets(status);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(change_timestamp);
```

---

## Data Sample Queries

### All orders for a customer
```sql
SELECT * FROM orders
WHERE customer_name = 'Customer A'
ORDER BY created_at DESC;
```

### Orders on hold
```sql
SELECT o.order_number, o.customer_name, o.status, oe.reason
FROM orders o
JOIN order_exceptions oe ON o.id = oe.order_id
WHERE oe.status = 'open'
AND oe.exception_type = 'on_hold';
```

### Machine utilization
```sql
SELECT m.name, COUNT(os.id) as scheduled_jobs,
       SUM(os.duration_hours) as total_hours
FROM machines m
LEFT JOIN order_schedules os ON m.id = os.machine_id
WHERE os.scheduled_start >= DATE(NOW())
GROUP BY m.id
ORDER BY total_hours DESC;
```

### Open SOP tickets
```sql
SELECT st.ticket_number, st.sop_reference,
       d1.name as raising_dept,
       d2.name as charged_dept,
       st.status
FROM sop_tickets st
JOIN departments d1 ON st.raising_department_id = d1.id
JOIN departments d2 ON st.charged_department_id = d2.id
WHERE st.status IN ('open', 'assigned', 'escalated_to_hod')
ORDER BY st.created_at DESC;
```

### Overdue maintenance
```sql
SELECT mt.ticket_number, m.name,
       DATEDIFF(NOW(), mt.target_completion_date) as days_overdue,
       mt.status
FROM maintenance_tickets mt
JOIN machines m ON mt.machine_id = m.id
WHERE mt.target_completion_date < NOW()
AND mt.status != 'closed'
ORDER BY mt.target_completion_date ASC;
```

### BOM costs by product
```sql
SELECT p.name,
       bm.total_material_cost,
       bm.total_labor_cost,
       bm.total_overhead,
       bm.total_cost
FROM products p
JOIN bills_of_materials bm ON p.id = bm.product_id
WHERE bm.is_active = TRUE
ORDER BY bm.total_cost DESC;
```

---

## Connection Details

```
Host: shortline.proxy.rlwy.net
Port: 19278
Database: th_db
User: {user}
Password: {password}

Connection String (Python):
mysql+pymysql://{user}:{password}@shortline.proxy.rlwy.net:19278/th_db
```

---

## Database Health

```sql
-- Check table counts
SELECT TABLE_NAME, TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'th_db'
ORDER BY TABLE_ROWS DESC;

-- Check database size
SELECT SUM(data_length + index_length) / 1024 / 1024 as size_mb
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'th_db';
```

---

All tables are properly indexed, normalized, and ready for production use!

