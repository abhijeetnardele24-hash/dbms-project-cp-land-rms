# Quick Start Guide
## Land Registry Management System

---

## 🚀 How to Run the Application

### 1. Start the Flask Application
```powershell
python run.py
```

The application will start on: **http://127.0.0.1:5000**

---

## 👤 Login Credentials

### Citizen Account
- **Email:** user@lrms.com
- **Password:** password
- **Can do:** Register properties, submit mutations, make payments, view dashboard

### Officer Account
- **Email:** officer@lrms.com
- **Password:** password
- **Can do:** Review and approve/reject mutations, view all properties

### Registrar Account
- **Email:** registrar@lrms.com
- **Password:** password
- **Can do:** Approve property registrations, manage users, full system access

### Admin Account
- **Email:** admin@lrms.com
- **Password:** password
- **Can do:** Full system administration

---

## 📊 View Data in MySQL Workbench

### Connection Details
- **Host:** localhost
- **Username:** root
- **Password:** 1234
- **Database:** land_registry_db

### Quick Query to See Everything
```sql
-- Count all data
SELECT 
    'Users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Properties', COUNT(*) FROM properties
UNION ALL
SELECT 'Mutations', COUNT(*) FROM mutations
UNION ALL
SELECT 'Payments', COUNT(*) FROM payments
UNION ALL
SELECT 'Owners', COUNT(*) FROM owners
UNION ALL
SELECT 'Ownerships', COUNT(*) FROM ownerships
UNION ALL
SELECT 'Audit Logs', COUNT(*) FROM audit_logs;
```

---

## ✅ Testing Data Persistence

### Run Automated Tests
```powershell
python test_data_persistence.py
```

This script will:
- ✓ Connect to MySQL database
- ✓ Verify table structure
- ✓ Check existing data
- ✓ Verify stored procedures and triggers
- ✓ Test data relationships
- ✓ Check audit trail
- ✓ Generate detailed report

---

## 🎯 Demo Workflow

### 1. Register a New Property (as Citizen)
1. Login as **user@lrms.com**
2. Go to **"Register Property"**
3. Click on map to select location (GPS coordinates will be captured)
4. Fill in property details:
   - Survey Number (e.g., SRV/2024/100)
   - Area and Unit
   - District, Village, State
   - Owner Information
5. Submit and make payment
6. **Check MySQL Workbench** - New entry in `properties`, `owners`, `ownerships`, and `payments` tables

### 2. Submit a Mutation (as Citizen)
1. Go to **"My Properties"**
2. Click **"Submit Mutation"** on a property
3. Select mutation type (Sale, Inheritance, Gift, etc.)
4. Fill in new owner details
5. Upload documents (optional)
6. Make payment
7. **Check MySQL Workbench** - New entry in `mutations` and `payments` tables

### 3. Approve Mutation (as Officer)
1. Logout and login as **officer@lrms.com**
2. Go to **"Pending Mutations"**
3. Review mutation details
4. Add comments if needed
5. Approve or reject
6. **Check MySQL Workbench** - Mutation status updated, audit log created

### 4. View Dashboard Analytics
1. Login as any user
2. Go to **Dashboard**
3. See beautiful charts showing:
   - Property statistics
   - Payment analytics
   - Status breakdown
   - Recent activities

---

## 📋 Key Features to Demonstrate

### 1. Interactive Maps
- Property registration with clickable map
- GPS coordinate capture
- Location display on property details page

### 2. Payment System
- Simulated Razorpay gateway
- Multiple payment methods (UPI, Card, Net Banking, Wallet)
- Payment receipt generation
- All payments saved in MySQL

### 3. MySQL Advanced Features
- **4 Stored Procedures:**
  - `calculate_property_tax`
  - `get_dashboard_stats`
  - `get_ownership_chain`
  - `get_property_report`

- **4 Triggers:**
  - `after_payment_insert`
  - `after_property_insert`
  - `before_property_update`
  - `after_property_status_update`

- **1 View:**
  - `v_property_dashboard_stats`

### 4. Data Relationships
- Properties → Owners (Many-to-Many via Ownerships)
- Properties → Mutations (One-to-Many)
- Users → Payments (One-to-Many)
- Properties → Payments (One-to-Many)

### 5. Audit Trail
- All important actions logged automatically
- View in `audit_logs` table
- Includes user, action, timestamp, and details

---

## 🔍 Important Tables in MySQL

### Core Tables
1. **users** - All system users with roles
2. **properties** - Property registrations with GPS coordinates
3. **owners** - Property owner information
4. **ownerships** - Links properties to owners
5. **mutations** - Property transfer requests
6. **payments** - All payment transactions
7. **audit_logs** - System activity tracking

### Reference Tables
8. **land_categories** - Types of land (Residential, Commercial, etc.)
9. **usage_types** - Property usage (Residential, Agricultural, etc.)
10. **property_statuses** - Status lookup
11. **document_types** - Document categories

---

## 🎨 UI Features

### Modern Design
- Purple gradient navbar
- Responsive layout
- Chart.js visualizations
- Leaflet.js interactive maps
- Bootstrap 5 components
- Custom animations

### Key Pages
- **Dashboard** - Statistics and charts
- **Property Registration** - Form with interactive map
- **My Properties** - Property list with actions
- **Mutations** - Submit and track mutations
- **Payments** - Payment history and receipts
- **Property Details** - Full details with location map

---

## 📁 Project Structure

```
dbms project cp Land rms/
├── app/
│   ├── routes/          # All route handlers
│   ├── models/          # Database models
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS, images
├── config.py            # Configuration
├── run.py               # Application entry point
├── test_data_persistence.py  # Test script
├── MYSQL_WORKBENCH_GUIDE.md  # Detailed MySQL guide
├── QUICK_START.md       # This file
└── requirements.txt     # Python dependencies
```

---

## 💾 Backup Location

Complete project backup saved at:
**`C:\Users\Abhijeet Nardele\Desktop\land_rms_backup.zip`**

---

## 🐛 Troubleshooting

### Application won't start
```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if needed
taskkill /PID <process_id> /F
```

### Cannot connect to MySQL
```powershell
# Check MySQL service status
Get-Service MySQL*

# Start MySQL service if stopped
net start MySQL80
```

### Database connection error
- Verify MySQL password is **1234**
- Check `config.py` has correct connection string
- Ensure database **land_registry_db** exists

---

## 📞 Next Steps

1. ✅ **Run the test script** - `python test_data_persistence.py`
2. ✅ **Start the application** - `python run.py`
3. ✅ **Login and test workflows** - Register property, submit mutation, make payment
4. ✅ **Open MySQL Workbench** - Connect and view data
5. ✅ **Run queries** - Use MYSQL_WORKBENCH_GUIDE.md for sample queries
6. ✅ **Demo the features** - Show maps, payments, approvals, analytics

---

## 🎓 For Presentation

### What to Highlight
1. **Real-world application** - Complete land registry system
2. **MySQL integration** - All data persists in MySQL with password 1234
3. **Advanced MySQL features** - Stored procedures, triggers, views
4. **Modern web technologies** - Flask, Bootstrap, Chart.js, Leaflet
5. **Data relationships** - Complex foreign key relationships
6. **Audit trail** - Automatic logging of all actions
7. **Payment integration** - Simulated payment gateway
8. **Interactive features** - Maps, charts, real-time updates

### Demo Flow
1. Show MySQL Workbench with existing data
2. Run application and login
3. Perform an operation (register property/submit mutation)
4. Immediately refresh MySQL Workbench to show new data
5. Run stored procedure to generate reports
6. Show audit logs to demonstrate triggers
7. Display dashboard with analytics
8. Show property location on map

---

**Good luck with your presentation! 🚀**
