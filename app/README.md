# Barron Production Management System

A comprehensive, enterprise-grade production management platform for managing branding operations, job scheduling, defect tracking, maintenance, and more.

## Features

### 1. **Job Planning & Scheduling**
- Order scheduling and capacity planning
- Department-based production workflows
- Smart order allocation and tracking
- Visual status indicators

### 2. **Defects & Quality Management**
- Internal reject ticket management with approval workflows
- Customer return logging and tracking
- Automated alerts and notifications
- QC-based reporting scheduler

### 3. **SOP Failure & NCR Management**
- Department-to-department SOP failure tickets
- Non-Conformance Report (NCR) workflow
- HOD escalation and decision tracking
- Complete audit trail

### 4. **Equipment Maintenance**
- Machinery maintenance request management
- Assignment and status tracking
- SLA-based prioritization
- Preventive maintenance scheduling

### 5. **Master Data Administration**
- Dynamic department, product, and machine management
- User and role-based access control
- Configurable forms and workflows
- Complete audit logging

### 6. **Operator Mobile Interface**
- Mobile-optimized job board
- Quick job start/stop workflows
- Quantity validation and discrepancy tracking
- Support for allocated and unallocated jobs

## Tech Stack

- **Backend**: Python FastAPI
- **Database**: MySQL (primary relational data) + JSON (dynamic configs)
- **Cache**: Redis
- **Frontend**: HTML5 + Vanilla JavaScript + CSS (industrial design)
- **Authentication**: JWT-based
- **Architecture**: RESTful API with role-based access control

## Project Structure

```
app/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── core/              # Config, security, auth
│   │   ├── db/                # Database setup
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── routes/            # API endpoints (auth, master, orders)
│   │   └── services/          # Business logic layer
│   ├── main.py                # FastAPI app initialization
│   └── requirements.txt        # Python dependencies
│
└── frontend/                   # Static HTML/CSS/JS
    ├── templates/             # HTML pages
    │   ├── login.html         # Main login
    │   ├── operator-login.html # Operator quick auth
    │   ├── dashboard.html     # Main dashboard
    │   ├── job-planning.html  # Order scheduling
    │   ├── operator-jobs.html # Operator job board (mobile)
    │   ├── defects.html       # Defects & returns
    │   ├── maintenance.html   # Maintenance management
    │   └── master-data.html   # Admin configuration
    └── static/
        ├── css/style.css      # Industrial-grade styling
        └── js/main.js         # API client & utility functions
```

## Quick Start

### Prerequisites
- Python 3.9+
- MySQL Server (or use the provided connection string for Railway MySQL)
- Redis (or use the provided connection string for Railway Redis)
- PowerShell 5.1+

### Installation & Running

1. **Clone/Extract the project**
   ```powershell
   cd app\backend
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the backend server**
   ```powershell
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Start a local web server for frontend**
   
   In a new PowerShell terminal:
   ```powershell
   cd app\frontend
   # Using Python's built-in server
   python -m http.server 3000
   ```

   Or if you have Node.js installed:
   ```powershell
   npx http-server --port 3000 --gzip
   ```

5. **Access the application**
   - Open browser: `http://localhost:3000`
   - Main Login: `http://localhost:3000/templates/login.html`
   - Operator Login: `http://localhost:3000/templates/operator-login.html`

### Default Test Credentials

Demo users will be created on first run. For now, use the registration endpoint to create test users.

**Test Operator:**
- Employee Number: `1001` (password is same as employee number)

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Key API Endpoints

### Authentication
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - Login with credentials
- `POST /api/auth/operator-login` - Operator login by employee number

### Master Data
- `GET /api/master/departments` - List departments
- `POST /api/master/departments` - Create department
- `GET /api/master/products` - List products
- `POST /api/master/products` - Create product
- `GET /api/master/machines` - List machines
- `POST /api/master/machines` - Create machine

### Orders
- `GET /api/orders` - List orders
- `POST /api/orders` - Create order
- `GET /api/orders/{order_id}` - Get order details
- `POST /api/orders/{order_id}/schedules` - Schedule order

## Configuration

### Database Connection
The app uses Railway MySQL and Redis by default. Connection strings are configured in `app/core/config.py`:

```python
DATABASE_URL = "mysql+mysqldb://root:fYJdZhXYpLzfiLFhgjvjkUWUzDKKCaYa@shortline.proxy.rlwy.net:19278/railway"
REDIS_URL = "redis://default:maXFCPazHpxaASnHpDcszQQpTsfONXFE@caboose.proxy.rlwy.net:39766"
```

To use a local MySQL instance, update the `DATABASE_URL` in `app/core/config.py`:
```python
DATABASE_URL = "mysql+mysqldb://root:password@localhost:3306/barron_prod"
```

## Architecture Highlights

### Dynamic & Flexible
- Forms, workflows, and SLAs are JSON-based and configurable without code changes
- Role-based permissions at system, module, and field levels
- Multi-tenant capability through department isolation

### Industrial-Grade
- Dark, high-contrast UI optimized for factory floors and older smartphones
- Complete audit trails for all actions
- SLA-based escalation and notifications
- Optimized for low-bandwidth environments

### Scalable
- RESTful API design
- Stateless authentication
- Database normalization with JSON flexibility
- Redis caching for performance

## Development Roadmap

### Next Phase Implementations
1. **Batch 1**: SOP/NCR module, Maintenance module, complete CRUD for all entities
2. **Batch 2**: Finance/BOM module, Cost impact calculations, Reporting dashboards
3. **Batch 3**: D365 integration, Advanced notifications, Mobile app
4. **Batch 4**: Analytics, ML-based predictive maintenance, Supply chain optimization

### Upcoming Features
- Excel file import/export for orders and master data
- D365 Business Central integration
- Advanced reporting and KPI dashboards
- Predictive maintenance using ML
- Real-time notification system (WebSockets)
- Mobile app (React Native / Flutter)

## Database Schema

Key tables include:
- `users`, `departments`, `machines` - Core organizational structure
- `orders`, `order_items`, `order_schedules` - Job planning
- `internal_rejects`, `customer_returns` - Defect management
- `sop_failure_tickets`, `non_conformance_reports` - SOP/NCR
- `maintenance_tickets` - Equipment maintenance
- `bills_of_materials`, `bom_components` - Finance
- `dynamic_forms`, `form_fields` - Flexible configurations
- `audit_logs` - Complete action history

## Security

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Full audit logging of all sensitive operations
- SQL injection prevention via SQLAlchemy ORM
- CORS configured for cross-origin requests

## Support & Contributing

For issues, improvements, or feature requests, document the requirement and submit for review.

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Developed for**: Barron (Pty) Ltd
