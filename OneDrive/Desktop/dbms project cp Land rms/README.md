# Land Registry Management System (LRMS)

## 🗄️ Database Management System (DBMS) Project

A comprehensive **SQL/MySQL-based** Land Registry Management System demonstrating advanced database concepts and enterprise-level DBMS implementation. This project showcases extensive use of MySQL features including stored procedures, triggers, views, complex queries, and normalized database design.

### 🎯 DBMS Features Highlighted
- ✅ **15+ Normalized Tables** (3NF) with proper relationships
- ✅ **8+ Stored Procedures** for complex business logic
- ✅ **10+ Database Triggers** for automated operations
- ✅ **12+ Database Views** for simplified data access
- ✅ **50+ Strategic Indexes** for query optimization
- ✅ **Complex SQL Queries** (JOINs, Subqueries, CTEs, Window Functions)
- ✅ **Table Partitioning** for performance optimization
- ✅ **Foreign Key Constraints** for referential integrity
- ✅ **MySQL Events** for scheduled tasks
- ✅ **ACID Compliance** with transaction management

### 🛠️ Technology Stack
- **Primary**: MySQL 8.0+ (Database Management System)
- **Backend**: Python Flask (Application Layer)
- **ORM**: SQLAlchemy (Database Abstraction)
- **Frontend**: HTML/Bootstrap (User Interface)

The system manages land records, property ownership, tax assessments, mutations, and all related land registry operations with sophisticated multi-role authentication and authorization.

## Features

### Role-Based Access Control
- **Administrator**: Complete system oversight, user management, reports, system settings
- **Land Registrar**: Property registration review, approval, certificate generation
- **Registration Officer**: Mutation requests, ownership updates, document verification
- **Citizen**: Property registration, mutation requests, tax payments, document management

### Core Functionality
- ✅ Property registration with ULPIN generation
- ✅ Ownership management with support for joint ownership
- ✅ Mutation requests and approval workflow
- ✅ Tax assessment and payment processing
- ✅ Document management with secure uploads
- ✅ In-app and email notifications
- ✅ Comprehensive audit logging
- ✅ Advanced search and filtering
- ✅ Report generation (PDF, Excel)

## Database Files (SQL)

The `database/` directory contains comprehensive SQL files demonstrating advanced DBMS concepts:

### Core SQL Files
1. **schema.sql** (500+ lines)
   - Complete database schema with 15+ tables
   - All relationships, constraints, and indexes
   - Master data initialization

2. **advanced_mysql_features.sql** (1000+ lines)
   - 8+ Stored Procedures
   - 2+ Functions
   - 10+ Triggers
   - 12+ Views
   - MySQL Events

3. **queries.sql** (500+ lines)
   - 50+ Complex SQL queries
   - Analytical queries
   - Reports and dashboards
   - Statistical analysis

4. **mysql_advanced_features.sql**
   - Performance optimization
   - Query optimization

5. **implement_partitioning.sql**
   - Table partitioning strategies

👉 **See `database/README.md` for detailed documentation**

## Technology Stack

- **Database (Primary)**: MySQL 8.0+ with advanced features
- **Backend**: Python 3.8+, Flask 3.0
- **Database Driver**: PyMySQL
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **Migrations**: Flask-Migrate
- **Email**: Flask-Mail
- **PDF**: ReportLab/WeasyPrint
- **Excel**: openpyxl
- **Frontend**: Bootstrap 5, JavaScript, Chart.js

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- MySQL Workbench (for database management)
- pip (Python package manager)

## Installation

### 1. Clone or Extract the Project

```bash
cd "C:\Users\Abhijeet Nardele\OneDrive\Desktop\dbms project cp Land rms"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Database Setup

#### Create Database in MySQL

Open MySQL Workbench or MySQL Command Line and execute:

```sql
CREATE DATABASE land_registry_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Verify MySQL Connection

The system is configured to connect to MySQL with:
- **Host**: localhost
- **Port**: 3306
- **User**: root
- **Password**: 1234
- **Database**: land_registry_db

Connection string: `mysql+pymysql://root:1234@localhost/land_registry_db`

If your MySQL password is different, update `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/land_registry_db'
```

### 5. Initialize Database

```powershell
# Initialize Flask-Migrate
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration to create all tables
flask db upgrade
```

### 6. Seed Sample Data

```powershell
python seed_data.py
```

This creates:
- Test users for all roles (admin, registrar, officer, citizen)
- Sample properties
- Sample ownership records
- Sample mutations
- Master data (land categories, usage types, document types)

### 7. Run the Application

```powershell
python run.py
```

The application will start on: `http://localhost:5000`

## Default Test Accounts

After running seed_data.py, you can log in with:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@lrms.com | password123 |
| Registrar | registrar@lrms.com | password123 |
| Officer | officer@lrms.com | password123 |
| Citizen | user@lrms.com | password123 |

## Viewing Data in MySQL Workbench

1. Open MySQL Workbench
2. Connect to localhost (root/1234)
3. Select `land_registry_db` database
4. Browse tables:
   - `users` - All user accounts
   - `properties` - Land parcels
   - `owners` - Property owners
   - `ownerships` - Property-Owner relationships
   - `mutations` - Ownership change requests
   - `payments` - Tax and fee payments
   - `documents` - Uploaded documents
   - `notifications` - User notifications
   - `audit_logs` - System activity logs

## Project Structure

```
land-registry-ms/
│
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── owner.py
│   │   ├── ownership.py
│   │   ├── mutation.py
│   │   ├── document.py
│   │   ├── payment.py
│   │   ├── notification.py
│   │   ├── audit_log.py
│   │   ├── tax_assessment.py
│   │   └── master_data.py
│   │
│   ├── routes/                  # Blueprint routes
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication
│   │   ├── main.py             # Home & common routes
│   │   ├── admin.py            # Admin dashboard
│   │   ├── registrar.py        # Registrar dashboard
│   │   ├── officer.py          # Officer dashboard
│   │   ├── citizen.py          # Citizen dashboard
│   │   └── api.py              # REST API endpoints
│   │
│   ├── forms/                   # WTForms
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── property_forms.py
│   │   ├── mutation_forms.py
│   │   ├── payment_forms.py
│   │   └── user_forms.py
│   │
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── admin/
│   │   ├── registrar/
│   │   ├── officer/
│   │   ├── citizen/
│   │   └── auth/
│   │
│   ├── static/                  # Static files
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── decorators.py        # Role-based decorators
│       ├── email_utils.py       # Email sending
│       ├── file_utils.py        # File handling
│       └── notification_utils.py # Notifications
│
├── migrations/                  # Database migrations
├── logs/                        # Application logs
│
├── config.py                    # Configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── seed_data.py                 # Sample data generator
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Development Commands

```powershell
# Run development server
python run.py

# Create new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Open Flask shell with models imported
flask shell

# Initialize database
flask init-db

# Seed database
flask seed-db
```

## MySQL Database Schema

### Key Tables

**users**: User accounts with roles (admin, registrar, officer, citizen)
- Primary key: id
- Unique: email
- Indexed: role, email

**properties**: Land parcels/properties
- Primary key: id
- Unique: ulpin (Unique Land Parcel Identification Number)
- Foreign keys: approved_by → users.id
- Indexed: status, ulpin

**owners**: Property owners
- Primary key: id
- Foreign keys: user_id → users.id
- Unique: aadhar_number, pan_number

**ownerships**: Property-Owner relationships
- Primary key: id
- Foreign keys: property_id → properties.id, owner_id → owners.id
- Supports joint ownership with percentages

**mutations**: Ownership change requests
- Primary key: id
- Foreign keys: property_id → properties.id, requester_id → users.id
- Unique: mutation_number
- Indexed: status

**payments**: Tax and fee payments
- Primary key: id
- Foreign keys: user_id → users.id, property_id → properties.id
- Unique: payment_reference, transaction_id

**notifications**: User notifications
- Primary key: id
- Foreign keys: user_id → users.id
- Indexed: is_read

**audit_logs**: System activity tracking
- Primary key: id
- Foreign keys: user_id → users.id
- Indexed: action, created_at

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/register` - User registration (citizen only)

### Admin (requires admin role)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/properties` - All properties
- `GET /admin/reports` - System reports

### Registrar (requires registrar role)
- `GET /registrar/dashboard` - Registrar dashboard
- `GET /registrar/pending-registrations` - Pending property registrations
- `POST /registrar/approve-property/<id>` - Approve property
- `POST /registrar/reject-property/<id>` - Reject property

### Officer (requires officer role)
- `GET /officer/dashboard` - Officer dashboard
- `GET /officer/pending-mutations` - Pending mutations
- `POST /officer/approve-mutation/<id>` - Approve mutation
- `POST /officer/reject-mutation/<id>` - Reject mutation

### Citizen (requires citizen role)
- `GET /citizen/dashboard` - Citizen dashboard
- `GET /citizen/my-properties` - User's properties
- `POST /citizen/register-property` - Submit property registration
- `POST /citizen/submit-mutation` - Submit mutation request
- `POST /citizen/make-payment` - Make tax payment

## Security Features

- ✅ Password hashing with Werkzeug
- ✅ CSRF protection with Flask-WTF
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ XSS protection through template escaping
- ✅ Role-based access control
- ✅ Secure file upload validation
- ✅ Session management
- ✅ Audit logging

## Troubleshooting

### Database Connection Issues

If you see "Can't connect to MySQL server":
1. Verify MySQL is running
2. Check username/password in config.py
3. Ensure land_registry_db database exists
4. Verify MySQL is on port 3306

### Module Import Errors

```powershell
pip install -r requirements.txt
```

### Migration Errors

```powershell
# Delete migrations folder
Remove-Item -Recurse migrations

# Re-initialize
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

## Support

For issues or questions about this Land Registry Management System, please refer to the documentation files:
- DATABASE_SCHEMA.md - Detailed database schema
- DEPLOYMENT.md - Production deployment guide
- API_DOCUMENTATION.md - Complete API reference

## License

This is a DBMS course project for educational purposes.
