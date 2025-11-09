-- ============================================================
-- LAND REGISTRY MANAGEMENT SYSTEM
-- MySQL Command Prompt Demonstration Script
-- ============================================================
-- Run these commands step-by-step during your presentation
-- Use: mysql -u root -p1234 -D land_registry_db
-- ============================================================

-- ============================================================
-- PART 1: DATABASE OVERVIEW
-- ============================================================

-- 1. Show all databases
SHOW DATABASES;

-- 2. Select our database
USE land_registry_db;

-- 3. Show all tables (15+ tables)
SHOW TABLES;

-- 4. Count total tables
SELECT COUNT(*) as total_tables 
FROM information_schema.tables 
WHERE table_schema = 'land_registry_db';

-- ============================================================
-- PART 2: TABLE STRUCTURE DEMONSTRATION
-- ============================================================

-- 5. Show properties table structure (300+ fields)
DESCRIBE properties;

-- 6. Show column count in properties table
SELECT COUNT(*) as total_columns 
FROM information_schema.columns 
WHERE table_schema = 'land_registry_db' 
  AND table_name = 'properties';

-- 7. Show users table structure
DESCRIBE users;

-- 8. Show tax_assessments table structure
DESCRIBE tax_assessments;

-- 9. Show ownerships table structure (many-to-many relationship)
DESCRIBE ownerships;

-- ============================================================
-- PART 3: DATA OVERVIEW
-- ============================================================

-- 10. Count total properties
SELECT COUNT(*) as total_properties FROM properties;

-- 11. Properties by status (aggregate function)
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM properties), 2) as percentage
FROM properties
GROUP BY status
ORDER BY count DESC;

-- 12. Properties by type
SELECT 
    property_type,
    COUNT(*) as count,
    AVG(area) as avg_area
FROM properties
GROUP BY property_type
ORDER BY count DESC;

-- 13. Total users by role
SELECT 
    role,
    COUNT(*) as user_count
FROM users
GROUP BY role
ORDER BY user_count DESC;

-- 14. Recent property registrations (last 10)
SELECT 
    id,
    ulpin,
    village_city,
    district,
    property_type,
    status,
    DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as registered_on
FROM properties
ORDER BY created_at DESC
LIMIT 10;

-- ============================================================
-- PART 4: CONSTRAINTS & RELATIONSHIPS
-- ============================================================

-- 15. Show primary keys
SELECT 
    table_name,
    column_name,
    constraint_name
FROM information_schema.key_column_usage
WHERE table_schema = 'land_registry_db'
  AND constraint_name = 'PRIMARY'
ORDER BY table_name;

-- 16. Show foreign key relationships
SELECT 
    TABLE_NAME as 'Table',
    COLUMN_NAME as 'Column',
    REFERENCED_TABLE_NAME as 'References Table',
    REFERENCED_COLUMN_NAME as 'References Column'
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'land_registry_db'
  AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;

-- 17. Show unique constraints
SELECT 
    table_name,
    column_name
FROM information_schema.statistics
WHERE table_schema = 'land_registry_db'
  AND non_unique = 0
  AND index_name != 'PRIMARY'
ORDER BY table_name;

-- ============================================================
-- PART 5: INDEXES (PERFORMANCE OPTIMIZATION)
-- ============================================================

-- 18. Show all indexes in database
SELECT 
    table_name,
    index_name,
    GROUP_CONCAT(column_name ORDER BY seq_in_index) as indexed_columns,
    index_type
FROM information_schema.statistics
WHERE table_schema = 'land_registry_db'
GROUP BY table_name, index_name, index_type
ORDER BY table_name, index_name;

-- 19. Count indexes per table
SELECT 
    table_name,
    COUNT(DISTINCT index_name) as index_count
FROM information_schema.statistics
WHERE table_schema = 'land_registry_db'
GROUP BY table_name
ORDER BY index_count DESC;

-- ============================================================
-- PART 6: DATABASE TRIGGERS (ADVANCED FEATURE)
-- ============================================================

-- 20. Show all triggers
SHOW TRIGGERS;

-- 21. Show specific trigger definition
SHOW CREATE TRIGGER trg_auto_create_tax_assessment\G

-- ============================================================
-- PART 7: DATABASE VIEWS
-- ============================================================

-- 22. Show all views
SELECT 
    table_name as view_name,
    view_definition
FROM information_schema.views
WHERE table_schema = 'land_registry_db';

-- 23. Query from a view (dashboard statistics)
SELECT * FROM vw_property_dashboard_stats;

-- ============================================================
-- PART 8: COMPLEX QUERIES (JOINS)
-- ============================================================

-- 24. Properties with owner information (INNER JOIN)
SELECT 
    p.ulpin,
    p.village_city,
    p.status,
    o.name as owner_name,
    o.email,
    os.ownership_percentage
FROM properties p
INNER JOIN ownerships os ON p.id = os.property_id
INNER JOIN owners o ON os.owner_id = o.id
WHERE p.status = 'approved'
  AND os.is_active = TRUE
LIMIT 10;

-- 25. Properties with tax assessment information (LEFT JOIN)
SELECT 
    p.ulpin,
    p.village_city,
    p.market_value,
    ta.annual_tax,
    ta.tax_paid,
    ta.tax_due,
    ta.status as tax_status
FROM properties p
LEFT JOIN tax_assessments ta ON p.id = ta.property_id
WHERE p.status = 'approved'
LIMIT 10;

-- 26. Properties with approver information
SELECT 
    p.ulpin,
    p.village_city,
    p.status,
    u.name as approved_by,
    u.role,
    DATE_FORMAT(p.approval_date, '%Y-%m-%d') as approval_date
FROM properties p
LEFT JOIN users u ON p.approved_by = u.id
WHERE p.status = 'approved'
ORDER BY p.approval_date DESC
LIMIT 10;

-- ============================================================
-- PART 9: AGGREGATE FUNCTIONS & STATISTICS
-- ============================================================

-- 27. Total market value by district
SELECT 
    district,
    COUNT(*) as total_properties,
    SUM(market_value) as total_market_value,
    AVG(market_value) as avg_market_value,
    MIN(market_value) as min_value,
    MAX(market_value) as max_value
FROM properties
WHERE status = 'approved' 
  AND market_value IS NOT NULL
GROUP BY district
HAVING COUNT(*) > 5
ORDER BY total_market_value DESC
LIMIT 10;

-- 28. Property area statistics
SELECT 
    property_type,
    COUNT(*) as count,
    ROUND(MIN(area), 2) as min_area,
    ROUND(AVG(area), 2) as avg_area,
    ROUND(MAX(area), 2) as max_area,
    ROUND(SUM(area), 2) as total_area
FROM properties
WHERE area IS NOT NULL
GROUP BY property_type
ORDER BY avg_area DESC;

-- 29. Monthly registration trends (date functions)
SELECT 
    YEAR(created_at) as year,
    MONTH(created_at) as month,
    COUNT(*) as registrations,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending
FROM properties
GROUP BY YEAR(created_at), MONTH(created_at)
ORDER BY year DESC, month DESC
LIMIT 12;

-- ============================================================
-- PART 10: SUBQUERIES
-- ============================================================

-- 30. Properties with above-average area
SELECT 
    ulpin,
    village_city,
    area,
    property_type
FROM properties
WHERE area > (SELECT AVG(area) FROM properties)
  AND status = 'approved'
ORDER BY area DESC
LIMIT 10;

-- 31. Districts with most properties
SELECT 
    district,
    property_count,
    avg_value
FROM (
    SELECT 
        district,
        COUNT(*) as property_count,
        AVG(market_value) as avg_value
    FROM properties
    WHERE status = 'approved'
    GROUP BY district
) as district_stats
WHERE property_count > 10
ORDER BY property_count DESC;

-- ============================================================
-- PART 11: AUDIT LOGGING DEMONSTRATION
-- ============================================================

-- 32. Recent audit activities
SELECT 
    al.id,
    u.name as user_name,
    u.role,
    al.action,
    al.entity_type,
    al.entity_id,
    al.description,
    DATE_FORMAT(al.created_at, '%Y-%m-%d %H:%i:%s') as timestamp
FROM audit_logs al
INNER JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC
LIMIT 20;

-- 33. Actions by user role
SELECT 
    u.role,
    al.action,
    COUNT(*) as action_count
FROM audit_logs al
INNER JOIN users u ON al.user_id = u.id
GROUP BY u.role, al.action
ORDER BY u.role, action_count DESC;

-- ============================================================
-- PART 12: TAX ASSESSMENT DEMONSTRATION
-- ============================================================

-- 34. Tax assessments with property details
SELECT 
    p.ulpin,
    p.village_city,
    p.market_value,
    ta.assessment_year,
    ta.assessed_value,
    ta.tax_rate,
    ta.annual_tax,
    ta.tax_paid,
    ta.tax_due,
    ta.status,
    DATE_FORMAT(ta.due_date, '%Y-%m-%d') as due_date
FROM tax_assessments ta
INNER JOIN properties p ON ta.property_id = p.id
ORDER BY ta.created_at DESC
LIMIT 10;

-- 35. Total tax revenue
SELECT 
    COUNT(*) as total_assessments,
    SUM(annual_tax) as total_annual_tax,
    SUM(tax_paid) as total_collected,
    SUM(tax_due) as total_pending,
    ROUND(SUM(tax_paid) * 100.0 / SUM(annual_tax), 2) as collection_rate_percentage
FROM tax_assessments;

-- ============================================================
-- PART 13: PAYMENT TRACKING
-- ============================================================

-- 36. Recent payments
SELECT 
    pay.payment_reference,
    u.name as paid_by,
    pay.payment_type,
    pay.amount,
    pay.payment_method,
    pay.status,
    DATE_FORMAT(pay.payment_date, '%Y-%m-%d %H:%i') as payment_date
FROM payments pay
INNER JOIN users u ON pay.user_id = u.id
ORDER BY pay.payment_date DESC
LIMIT 15;

-- 37. Revenue by payment type
SELECT 
    payment_type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MAX(amount) as max_amount
FROM payments
WHERE status = 'completed'
GROUP BY payment_type
ORDER BY total_amount DESC;

-- ============================================================
-- PART 14: LIVE WORKFLOW DEMONSTRATION
-- ============================================================

-- 38. Show a pending property (before approval)
SELECT 
    id,
    ulpin,
    village_city,
    district,
    area,
    property_type,
    status,
    market_value,
    DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as created_at
FROM properties
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 1;

-- 39. Check tax assessment for this property (should be empty before approval)
SELECT 
    ta.*
FROM tax_assessments ta
INNER JOIN properties p ON ta.property_id = p.id
WHERE p.status = 'pending'
ORDER BY p.created_at DESC
LIMIT 1;

-- ============================================================
-- AFTER APPROVAL DEMONSTRATION (Run after approving property)
-- ============================================================

-- 40. Check property status change
SELECT 
    id,
    ulpin,
    village_city,
    status,
    approved_by,
    DATE_FORMAT(approval_date, '%Y-%m-%d %H:%i') as approval_date,
    DATE_FORMAT(registration_date, '%Y-%m-%d %H:%i') as registration_date
FROM properties
WHERE ulpin = 'MH-THA-2021-01418'  -- Replace with actual ULPIN
LIMIT 1;

-- 41. Check auto-created tax assessment (trigger result)
SELECT 
    ta.id,
    ta.property_id,
    ta.assessment_year,
    ta.assessed_value,
    ta.tax_rate,
    ta.annual_tax,
    ta.tax_due,
    DATE_FORMAT(ta.due_date, '%Y-%m-%d') as due_date,
    ta.status,
    DATE_FORMAT(ta.created_at, '%Y-%m-%d %H:%i') as created_at
FROM tax_assessments ta
INNER JOIN properties p ON ta.property_id = p.id
WHERE p.ulpin = 'MH-THA-2021-01418'  -- Replace with actual ULPIN
LIMIT 1;

-- 42. Check audit log entry
SELECT 
    al.id,
    u.name as performed_by,
    al.action,
    al.description,
    DATE_FORMAT(al.created_at, '%Y-%m-%d %H:%i:%s') as timestamp
FROM audit_logs al
INNER JOIN users u ON al.user_id = u.id
WHERE al.action = 'approve_property'
ORDER BY al.created_at DESC
LIMIT 1;

-- ============================================================
-- PART 15: DATABASE SIZE & PERFORMANCE INFO
-- ============================================================

-- 43. Database size
SELECT 
    table_name,
    ROUND((data_length + index_length) / 1024 / 1024, 2) as size_mb,
    table_rows
FROM information_schema.tables
WHERE table_schema = 'land_registry_db'
  AND table_type = 'BASE TABLE'
ORDER BY (data_length + index_length) DESC;

-- 44. Total database size
SELECT 
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as total_size_mb
FROM information_schema.tables
WHERE table_schema = 'land_registry_db';

-- ============================================================
-- PART 16: ADVANCED QUERIES FOR IMPRESSIVE DEMO
-- ============================================================

-- 45. Property ownership chain (recursive concept)
SELECT 
    p.ulpin,
    p.village_city,
    GROUP_CONCAT(
        CONCAT(o.name, ' (', os.ownership_percentage, '%)')
        ORDER BY os.ownership_percentage DESC
        SEPARATOR ', '
    ) as owners
FROM properties p
INNER JOIN ownerships os ON p.id = os.property_id AND os.is_active = TRUE
INNER JOIN owners o ON os.owner_id = o.id
WHERE p.status = 'approved'
GROUP BY p.id
HAVING COUNT(os.id) > 1  -- Only joint ownership
LIMIT 10;

-- 46. Properties near expiring tax due dates
SELECT 
    p.ulpin,
    p.village_city,
    ta.annual_tax,
    ta.tax_due,
    DATE_FORMAT(ta.due_date, '%Y-%m-%d') as due_date,
    DATEDIFF(ta.due_date, CURDATE()) as days_remaining
FROM properties p
INNER JOIN tax_assessments ta ON p.id = ta.property_id
WHERE ta.status = 'pending'
  AND ta.due_date IS NOT NULL
  AND ta.due_date > CURDATE()
ORDER BY ta.due_date ASC
LIMIT 10;

-- 47. Most active users (by audit logs)
SELECT 
    u.name,
    u.role,
    COUNT(al.id) as total_actions,
    COUNT(DISTINCT DATE(al.created_at)) as active_days,
    DATE_FORMAT(MAX(al.created_at), '%Y-%m-%d %H:%i') as last_activity
FROM users u
INNER JOIN audit_logs al ON u.id = al.user_id
GROUP BY u.id
ORDER BY total_actions DESC
LIMIT 10;

-- 48. Complex analytical query (demonstrate skills)
SELECT 
    p.district,
    p.property_type,
    COUNT(*) as property_count,
    ROUND(AVG(p.area), 2) as avg_area,
    ROUND(AVG(p.market_value), 2) as avg_value,
    ROUND(SUM(ta.annual_tax), 2) as total_tax,
    COUNT(DISTINCT os.owner_id) as unique_owners,
    ROUND(AVG(ta.tax_paid * 100.0 / ta.annual_tax), 2) as avg_collection_rate
FROM properties p
LEFT JOIN tax_assessments ta ON p.id = ta.property_id
LEFT JOIN ownerships os ON p.id = os.property_id AND os.is_active = TRUE
WHERE p.status = 'approved'
GROUP BY p.district, p.property_type
HAVING property_count >= 5
ORDER BY total_tax DESC
LIMIT 15;

-- ============================================================
-- PART 17: DATA INTEGRITY VERIFICATION
-- ============================================================

-- 49. Verify referential integrity (orphaned records check)
-- Check for ownerships without valid property
SELECT COUNT(*) as orphaned_ownerships
FROM ownerships os
LEFT JOIN properties p ON os.property_id = p.id
WHERE p.id IS NULL;

-- Check for tax assessments without valid property
SELECT COUNT(*) as orphaned_tax_assessments
FROM tax_assessments ta
LEFT JOIN properties p ON ta.property_id = p.id
WHERE p.id IS NULL;

-- 50. Verify data consistency
-- Check ownership percentage totals (should be <= 100)
SELECT 
    property_id,
    SUM(ownership_percentage) as total_percentage
FROM ownerships
WHERE is_active = TRUE
GROUP BY property_id
HAVING SUM(ownership_percentage) > 100;

-- ============================================================
-- BONUS: PERFORMANCE DEMONSTRATION
-- ============================================================

-- 51. Query with index (fast)
EXPLAIN SELECT * FROM properties WHERE status = 'approved';

-- 52. Query with composite index
EXPLAIN SELECT * FROM properties 
WHERE status = 'approved' 
ORDER BY created_at DESC 
LIMIT 10;

-- 53. Join query optimization
EXPLAIN SELECT 
    p.ulpin,
    o.name
FROM properties p
INNER JOIN ownerships os ON p.id = os.property_id
INNER JOIN owners o ON os.owner_id = o.id
WHERE p.status = 'approved'
LIMIT 10;

-- ============================================================
-- END OF DEMONSTRATION SCRIPT
-- ============================================================
-- Total Queries: 53
-- Categories Covered:
-- - Database structure
-- - Table relationships
-- - Constraints & indexes
-- - Triggers & views
-- - Complex joins
-- - Aggregate functions
-- - Subqueries
-- - Date functions
-- - Audit logging
-- - Tax assessments
-- - Performance analysis
-- - Data integrity
-- ============================================================
