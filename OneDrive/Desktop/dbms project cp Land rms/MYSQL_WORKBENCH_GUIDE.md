# MySQL Workbench Verification Guide
## Land Registry Management System

---

## Connection Details
- **Host:** localhost
- **Port:** 3306 (default)
- **Username:** root
- **Password:** 1234
- **Database:** land_registry_db

---

## Step 1: Connect to MySQL

1. Open **MySQL Workbench**
2. Click on **"MySQL Connections"** (or the + icon)
3. Enter the following details:
   - Connection Name: `Land Registry DB`
   - Hostname: `localhost`
   - Port: `3306`
   - Username: `root`
4. Click **"Test Connection"**
5. Enter password: `1234`
6. Click **"OK"** and then **"OK"** again to save the connection

---

## Step 2: Open the Database

1. Double-click on your new connection
2. Enter password: `1234`
3. In the left sidebar, expand **Schemas**
4. Find and click on **`land_registry_db`**
5. You should now see all the tables, views, stored procedures, and triggers

---

## Step 3: Explore Data

### View All Tables
Run this query to see all tables:
```sql
SHOW TABLES;
```

**Expected output:** 27 tables including:
- users
- properties
- mutations
- payments
- owners
- ownerships
- audit_logs
- notifications
- tax_assessments
- and more...

---

## Step 4: Verify User Data

```sql
SELECT id, email, role, created_at 
FROM users
ORDER BY created_at;
```

**Expected users:**
1. admin@lrms.com (admin)
2. registrar@lrms.com (registrar)
3. officer@lrms.com (officer)
4. user@lrms.com (citizen)
5. user2@lrms.com (citizen)

---

## Step 5: Verify Property Data

```sql
SELECT 
    p.id,
    p.survey_number,
    p.area,
    p.area_unit,
    p.latitude,
    p.longitude,
    p.status,
    p.district,
    p.village_city,
    p.created_at
FROM properties p
ORDER BY p.created_at DESC;
```

**What to check:**
- Survey numbers (e.g., SRV/2023/001, SRV/2023/002)
- Area values in square meters
- Status (approved, pending, rejected, etc.)
- Location coordinates (latitude/longitude)
- District and village information

---

## Step 6: Verify Ownership Data

```sql
SELECT 
    o.id,
    p.survey_number,
    ow.full_name as owner_name,
    ow.aadhar_number,
    ow.pan_number,
    o.ownership_percentage,
    o.ownership_type,
    o.acquisition_mode,
    o.acquisition_date
FROM ownerships o
LEFT JOIN properties p ON o.property_id = p.id
LEFT JOIN owners ow ON o.owner_id = ow.id
ORDER BY p.survey_number;
```

**What to check:**
- Owner names linked to properties
- Ownership percentages (should total 100% per property)
- Aadhar and PAN numbers
- Acquisition details

---

## Step 7: Verify Mutation Data

```sql
SELECT 
    m.id,
    m.mutation_type,
    m.status,
    p.survey_number,
    m.applicant_name,
    m.application_date,
    m.completion_date,
    m.fee_amount,
    m.remarks
FROM mutations m
LEFT JOIN properties p ON m.property_id = p.id
ORDER BY m.application_date DESC;
```

**What to check:**
- Mutation types (sale, inheritance, gift, etc.)
- Status (pending, approved, rejected)
- Linked property survey numbers
- Fee amounts
- Application and completion dates

---

## Step 8: Verify Payment Data

```sql
SELECT 
    p.id,
    p.payment_reference,
    p.amount,
    p.payment_type,
    p.payment_method,
    p.status,
    p.payment_date,
    p.completed_date,
    p.receipt_number,
    u.email as payer_email,
    pr.survey_number
FROM payments p
LEFT JOIN users u ON p.user_id = u.id
LEFT JOIN properties pr ON p.property_id = pr.id
ORDER BY p.payment_date DESC;
```

**What to check:**
- Payment references (e.g., PAY202500000001)
- Amounts in INR
- Payment types (property_tax, mutation_fee, registration_fee)
- Payment methods (online, card, UPI, etc.)
- Status (completed, pending, failed)
- Receipt numbers

---

## Step 9: Check Database Features

### View Stored Procedures
```sql
SHOW PROCEDURE STATUS WHERE Db = 'land_registry_db';
```

**Expected procedures:**
1. calculate_property_tax
2. get_dashboard_stats
3. get_ownership_chain
4. get_property_report

### View Triggers
```sql
SHOW TRIGGERS FROM land_registry_db;
```

**Expected triggers:**
1. after_payment_insert (on payments)
2. after_property_insert (on properties)
3. before_property_update (on properties)
4. after_property_status_update (on properties)

### View Views
```sql
SELECT TABLE_NAME 
FROM information_schema.VIEWS 
WHERE TABLE_SCHEMA = 'land_registry_db';
```

**Expected view:**
- v_property_dashboard_stats

---

## Step 10: Test Stored Procedures

### Get Dashboard Statistics
```sql
CALL get_dashboard_stats();
```

This will return various statistics like:
- Total properties
- Total users
- Total payments
- Pending mutations
- etc.

### Calculate Property Tax
```sql
-- Replace 1 with an actual property ID from your properties table
CALL calculate_property_tax(1, 2024);
```

### Get Property Report
```sql
-- Replace 1 with an actual property ID
CALL get_property_report(1);
```

### Get Ownership Chain
```sql
-- Replace 1 with an actual property ID
CALL get_ownership_chain(1);
```

---

## Step 11: Query the Dashboard View

```sql
SELECT * FROM v_property_dashboard_stats;
```

This view provides a comprehensive overview of properties with their ownership and status information.

---

## Step 12: Check Audit Trail

```sql
SELECT 
    al.id,
    al.action,
    al.action_type,
    al.entity_type,
    al.entity_id,
    u.email as user_email,
    al.description,
    al.created_at
FROM audit_logs al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC
LIMIT 50;
```

**What to check:**
- User actions (create, update, delete, login, logout)
- Entity types (properties, mutations, payments, users)
- Timestamps of actions
- User emails who performed actions

---

## Step 13: Complex Queries for Analysis

### Properties by Status
```sql
SELECT 
    status,
    COUNT(*) as count,
    SUM(area) as total_area
FROM properties
GROUP BY status;
```

### Payments by Type
```sql
SELECT 
    payment_type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount
FROM payments
WHERE status = 'completed'
GROUP BY payment_type;
```

### Mutations by Status
```sql
SELECT 
    status,
    COUNT(*) as count,
    AVG(DATEDIFF(completion_date, application_date)) as avg_processing_days
FROM mutations
WHERE completion_date IS NOT NULL
GROUP BY status;
```

### Properties with Multiple Owners
```sql
SELECT 
    p.survey_number,
    COUNT(o.id) as owner_count,
    GROUP_CONCAT(ow.full_name SEPARATOR ', ') as owners
FROM properties p
JOIN ownerships o ON p.id = o.property_id
JOIN owners ow ON o.owner_id = ow.id
GROUP BY p.id, p.survey_number
HAVING owner_count > 1;
```

---

## Step 14: Real-time Monitoring

Keep this query open to see new data as it's added:

```sql
SELECT 
    'Properties' as entity,
    COUNT(*) as count,
    MAX(created_at) as last_updated
FROM properties
UNION ALL
SELECT 
    'Mutations' as entity,
    COUNT(*) as count,
    MAX(created_at) as last_updated
FROM mutations
UNION ALL
SELECT 
    'Payments' as entity,
    COUNT(*) as count,
    MAX(created_at) as last_updated
FROM payments
UNION ALL
SELECT 
    'Audit Logs' as entity,
    COUNT(*) as count,
    MAX(created_at) as last_updated
FROM audit_logs;
```

---

## Step 15: Export Data

To export any table or query result:
1. Run your query
2. Click on **"Export"** icon in the result grid
3. Choose format (CSV, JSON, SQL, etc.)
4. Save the file

---

## Troubleshooting

### Cannot Connect
- Ensure MySQL service is running
- Check if port 3306 is open
- Verify username and password

### Cannot See Database
- Make sure you selected `land_registry_db` schema in the left panel
- Refresh the schema list (right-click on Schemas > Refresh All)

### Empty Tables
- Run the Flask application first to generate sample data
- Login and perform operations (register property, submit mutation, make payment)
- Then refresh the tables in MySQL Workbench

---

## Key Features to Demonstrate

1. **Data Persistence:** Show how form data from the web application appears in MySQL tables
2. **Relationships:** Demonstrate foreign key relationships between tables
3. **Triggers:** Show audit logs automatically created when data changes
4. **Stored Procedures:** Execute procedures to get complex reports
5. **Views:** Query the dashboard view for aggregated statistics
6. **Data Integrity:** Show UNIQUE constraints on payment references and survey numbers
7. **Transactions:** Demonstrate how payment and mutation data is linked

---

## Current Database Statistics

As of last verification:
- **Users:** 5
- **Properties:** 3
- **Mutations:** 2
- **Payments:** 4
- **Ownerships:** 3
- **Audit Logs:** 22
- **Stored Procedures:** 4
- **Triggers:** 4
- **Views:** 1

---

## Notes

- All timestamps are stored in datetime format
- Money amounts are stored as FLOAT
- Status fields use ENUM for data integrity
- Foreign keys maintain referential integrity
- Triggers automatically log important changes
- Stored procedures provide complex business logic

---

**For support, contact the development team or refer to the main README.md file.**
