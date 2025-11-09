# MySQL Command Prompt Demo Guide
## Quick Reference for Presentation

---

## 🚀 How to Start

### **Step 1: Open Command Prompt**
```powershell
# Press Win + R, type: cmd
# Or use PowerShell
```

### **Step 2: Login to MySQL**
```bash
mysql -u root -p1234
```

### **Step 3: Select Database**
```sql
USE land_registry_db;
```

---

## 📋 Essential Queries for 5-Minute Demo

### **1. Show Database Overview** (30 seconds)
```sql
-- Show all tables
SHOW TABLES;

-- Count tables
SELECT COUNT(*) as total_tables 
FROM information_schema.tables 
WHERE table_schema = 'land_registry_db';
```
**Say:** "This system has 15+ normalized tables managing the complete property lifecycle."

---

### **2. Show Table Structure** (30 seconds)
```sql
-- Show properties table (300+ fields)
DESCRIBE properties;

-- Count columns
SELECT COUNT(*) as total_columns 
FROM information_schema.columns 
WHERE table_schema = 'land_registry_db' 
  AND table_name = 'properties';
```
**Say:** "The properties table has 300+ comprehensive fields capturing extensive land information."

---

### **3. Show Data Statistics** (1 minute)
```sql
-- Properties by status
SELECT 
    status,
    COUNT(*) as count
FROM properties
GROUP BY status;

-- Properties by type
SELECT 
    property_type,
    COUNT(*) as count,
    AVG(area) as avg_area
FROM properties
GROUP BY property_type;
```
**Say:** "Here's the distribution of properties by status and type, demonstrating aggregate functions."

---

### **4. Show Foreign Keys** (30 seconds)
```sql
-- Show relationships between tables
SELECT 
    TABLE_NAME as 'Table',
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table'
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'land_registry_db'
  AND REFERENCED_TABLE_NAME IS NOT NULL
LIMIT 10;
```
**Say:** "All tables are connected through foreign key constraints ensuring referential integrity."

---

### **5. Show Indexes** (30 seconds)
```sql
-- Count indexes per table
SELECT 
    table_name,
    COUNT(DISTINCT index_name) as index_count
FROM information_schema.statistics
WHERE table_schema = 'land_registry_db'
GROUP BY table_name
ORDER BY index_count DESC
LIMIT 10;
```
**Say:** "We've implemented 50+ strategic indexes for query optimization."

---

### **6. Show Database Trigger** (1 minute)
```sql
-- Show all triggers
SHOW TRIGGERS;

-- Show trigger definition
SHOW CREATE TRIGGER trg_auto_create_tax_assessment\G
```
**Say:** "This trigger automatically creates a tax assessment when a property is approved, demonstrating automation at the database level."

---

### **7. Complex Join Query** (1 minute)
```sql
-- Properties with owners (JOIN demonstration)
SELECT 
    p.ulpin,
    p.village_city,
    p.status,
    o.name as owner_name,
    os.ownership_percentage
FROM properties p
INNER JOIN ownerships os ON p.id = os.property_id
INNER JOIN owners o ON os.owner_id = o.id
WHERE p.status = 'approved'
LIMIT 10;
```
**Say:** "This demonstrates INNER JOIN across three tables to show property ownership information."

---

### **8. Live Workflow Demo** (2 minutes)

#### **Before Approval:**
```sql
-- Show pending property
SELECT 
    id,
    ulpin,
    village_city,
    status,
    market_value
FROM properties
WHERE status = 'pending'
LIMIT 1;

-- Check tax assessment (should be empty)
SELECT COUNT(*) as tax_records
FROM tax_assessments ta
INNER JOIN properties p ON ta.property_id = p.id
WHERE p.status = 'pending';
```
**Say:** "Notice there's no tax assessment for pending properties."

#### **After Approval (Do in browser):**
1. Go to Registrar dashboard
2. Approve a property
3. Return to command prompt

#### **Verify Changes:**
```sql
-- Check property status changed
SELECT 
    id,
    ulpin,
    status,
    approved_by,
    approval_date
FROM properties
WHERE ulpin = 'MH-THA-2021-01418'  -- Use actual ULPIN
LIMIT 1;

-- Check auto-created tax assessment
SELECT 
    property_id,
    assessment_year,
    assessed_value,
    annual_tax,
    tax_due,
    status
FROM tax_assessments
WHERE property_id = 1753;  -- Use actual property_id

-- Check audit log
SELECT 
    u.name,
    al.action,
    al.description,
    al.created_at
FROM audit_logs al
INNER JOIN users u ON al.user_id = u.id
WHERE al.action = 'approve_property'
ORDER BY al.created_at DESC
LIMIT 1;
```
**Say:** "The trigger fired automatically: status updated, tax assessment created, audit log recorded—all in one transaction!"

---

## 🎯 Impressive Advanced Queries

### **Aggregate with Multiple Functions:**
```sql
SELECT 
    district,
    COUNT(*) as total_properties,
    SUM(market_value) as total_value,
    AVG(market_value) as avg_value,
    MIN(market_value) as min_value,
    MAX(market_value) as max_value
FROM properties
WHERE status = 'approved' 
  AND market_value IS NOT NULL
GROUP BY district
HAVING COUNT(*) > 5
ORDER BY total_value DESC
LIMIT 5;
```
**Say:** "This demonstrates COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING, and ORDER BY in one query."

---

### **Subquery:**
```sql
-- Properties above average area
SELECT 
    ulpin,
    village_city,
    area,
    property_type
FROM properties
WHERE area > (SELECT AVG(area) FROM properties)
  AND status = 'approved'
ORDER BY area DESC
LIMIT 5;
```
**Say:** "This uses a subquery to find properties with above-average area."

---

### **Date Functions:**
```sql
-- Monthly registration trends
SELECT 
    YEAR(created_at) as year,
    MONTH(created_at) as month,
    COUNT(*) as registrations
FROM properties
GROUP BY YEAR(created_at), MONTH(created_at)
ORDER BY year DESC, month DESC
LIMIT 6;
```
**Say:** "Date functions used for trend analysis."

---

## 💡 If Teacher Asks Specific Questions

### **"Show me normalization"**
```sql
-- Bad design (not normalized):
-- properties table with owner_names VARCHAR(500) -- Multiple owners in one field

-- Good design (3NF - what we did):
SELECT 
    p.ulpin,
    GROUP_CONCAT(o.name SEPARATOR ', ') as all_owners
FROM properties p
INNER JOIN ownerships os ON p.id = os.property_id
INNER JOIN owners o ON os.owner_id = o.id
GROUP BY p.id
LIMIT 5;
```
**Say:** "We separated owners into their own table with a junction table for many-to-many relationships."

---

### **"How do you ensure data integrity?"**
```sql
-- Show constraints
SELECT 
    table_name,
    column_name,
    constraint_name,
    referenced_table_name
FROM information_schema.key_column_usage
WHERE table_schema = 'land_registry_db'
  AND referenced_table_name = 'properties'
LIMIT 10;
```
**Say:** "Foreign keys prevent orphaned records. If I try to delete a property with ownerships, it will fail or cascade delete."

---

### **"Show me transaction example"**
```sql
-- Explain with words (can't demo easily in cmd)
-- "When approving a property:
-- START TRANSACTION;
-- UPDATE properties SET status='approved' WHERE id=1;
-- INSERT INTO tax_assessments (...) VALUES (...);
-- INSERT INTO audit_logs (...) VALUES (...);
-- COMMIT;
-- If any step fails, ROLLBACK ensures atomicity."
```

---

### **"How does indexing help?"**
```sql
-- Show query plan WITH index
EXPLAIN SELECT * FROM properties WHERE status = 'approved';

-- Result shows "Using index" or "Using where"
```
**Say:** "The index on status column allows MySQL to jump directly to matching rows instead of scanning all records."

---

## 🔧 Troubleshooting

### **If query is too long:**
```sql
-- Use \G instead of ; for vertical output
SELECT * FROM properties WHERE id = 1\G
```

### **If you get an error:**
```sql
-- Check you're in the right database
SELECT DATABASE();

-- Should show: land_registry_db
```

### **To clear screen:**
```sql
\! cls   -- Windows
\! clear -- Linux/Mac
```

### **To exit MySQL:**
```sql
EXIT;
-- or
\q
```

---

## 📝 Backup One-Liners (If Time Runs Short)

```sql
-- Show everything quickly
SHOW TABLES;
SELECT COUNT(*) FROM properties;
SELECT status, COUNT(*) FROM properties GROUP BY status;
SHOW TRIGGERS;
```

---

## 🎬 Recommended Flow (5 minutes)

1. **Login** (10 sec): `mysql -u root -p1234`
2. **Overview** (30 sec): Tables count, structure
3. **Data Stats** (30 sec): Status distribution
4. **Relationships** (30 sec): Foreign keys
5. **Advanced Features** (30 sec): Triggers, indexes
6. **Complex Query** (30 sec): JOIN example
7. **Live Demo** (2 min): Approval workflow with verification
8. **Wrap Up** (10 sec): Summary

**Total: ~5 minutes**

---

## 💡 Pro Tips

✅ **Keep queries ready in Notepad** - Copy/paste quickly
✅ **Test all queries before presentation** - Ensure they work
✅ **Know the results** - Don't be surprised by output
✅ **Have backup screenshots** - In case MySQL fails
✅ **Explain while query runs** - Don't just show results
✅ **Use LIMIT** - Keep output manageable
✅ **Stay calm** - If something fails, move to next query

---

## 📁 File Location
Full script: `DEMO_MYSQL_QUERIES.sql`
This guide: `DEMO_GUIDE.md`

**Good luck with your presentation!** 🚀
