-- =====================================================
-- PERFORMANCE OPTIMIZATION & INDEXING STRATEGIES
-- Land Registry Management System
-- =====================================================
-- This file contains comprehensive indexing strategies,
-- query optimization, and performance tuning for the LRMS database
-- =====================================================

USE land_registry_db;

-- =====================================================
-- SECTION 1: DROP EXISTING INDEXES (IF RECREATING)
-- =====================================================

-- Note: Run this section only if you need to recreate indexes

-- Properties table indexes
-- ALTER TABLE properties DROP INDEX IF EXISTS idx_composite_location;
-- ALTER TABLE properties DROP INDEX IF EXISTS idx_composite_status_type;
-- ALTER TABLE properties DROP INDEX IF EXISTS idx_market_value;
-- ALTER TABLE properties DROP INDEX IF EXISTS idx_registered_date;

-- =====================================================
-- SECTION 2: COMPREHENSIVE INDEXING STRATEGY
-- =====================================================

-- Properties Table Indexes
-- Primary access patterns: location-based searches, status filtering, type filtering

-- Composite index for location-based queries (most common search pattern)
CREATE INDEX idx_composite_location 
ON properties(district, state, village_city, status);

-- Composite index for status and property type filtering
CREATE INDEX idx_composite_status_type 
ON properties(status, property_type, created_at DESC);

-- Index for value-based searches and sorting
CREATE INDEX idx_market_value 
ON properties(market_value DESC);

-- Index for date-based queries and reports
CREATE INDEX idx_registered_date 
ON properties(registered_date DESC);

-- Fulltext index for ULPIN and survey numbers
CREATE FULLTEXT INDEX idx_fulltext_property_numbers 
ON properties(ulpin, survey_number, plot_number);

-- Spatial index for geographic queries (if using spatial data types)
-- CREATE SPATIAL INDEX idx_spatial_coords ON properties(location_point);

-- =====================================================
-- Ownerships Table Indexes
-- =====================================================

-- Composite index for active ownership queries
CREATE INDEX idx_composite_ownership 
ON ownerships(property_id, owner_id, is_current);

-- Index for owner-based lookups
CREATE INDEX idx_owner_property_lookup 
ON ownerships(owner_id, is_current, created_at DESC);

-- Index for acquisition date sorting
CREATE INDEX idx_acquisition_date 
ON ownerships(acquisition_date DESC);

-- =====================================================
-- Owners Table Indexes
-- =====================================================

-- Composite index for identity document searches
CREATE INDEX idx_composite_identity 
ON owners(aadhar_number, pan_number);

-- Fulltext search on owner names
CREATE FULLTEXT INDEX idx_fulltext_owner_names 
ON owners(full_name, father_name);

-- Index for active owners
CREATE INDEX idx_active_owners 
ON owners(is_active, created_at DESC);

-- =====================================================
-- Mutations Table Indexes
-- =====================================================

-- Composite index for mutation processing workflow
CREATE INDEX idx_composite_mutation_workflow 
ON mutations(status, application_date DESC);

-- Index for property mutation history
CREATE INDEX idx_mutation_property_history 
ON mutations(property_id, application_date DESC);

-- Index for requester lookup
CREATE INDEX idx_mutation_requester 
ON mutations(requester_id, status, application_date DESC);

-- Index for review tracking
CREATE INDEX idx_mutation_review 
ON mutations(reviewed_by, review_date DESC);

-- Fulltext search on mutation numbers
CREATE FULLTEXT INDEX idx_fulltext_mutation_number 
ON mutations(mutation_number);

-- =====================================================
-- Payments Table Indexes
-- =====================================================

-- Composite index for payment queries
CREATE INDEX idx_composite_payment_lookup 
ON payments(user_id, status, payment_date DESC);

-- Index for property payment history
CREATE INDEX idx_payment_property 
ON payments(property_id, payment_date DESC);

-- Index for transaction lookup
CREATE INDEX idx_transaction_lookup 
ON payments(transaction_id, payment_reference);

-- Index for payment type analysis
CREATE INDEX idx_payment_type_status 
ON payments(payment_type, status, payment_date DESC);

-- Index for date-range queries
CREATE INDEX idx_payment_date_range 
ON payments(payment_date DESC, total_amount);

-- =====================================================
-- Tax Assessments Table Indexes
-- =====================================================

-- Composite index for tax queries
CREATE INDEX idx_composite_tax_assessment 
ON tax_assessments(property_id, assessment_year, status);

-- Index for overdue tax tracking
CREATE INDEX idx_tax_due_date 
ON tax_assessments(due_date, status);

-- Index for assessment year reports
CREATE INDEX idx_assessment_year_status 
ON tax_assessments(assessment_year DESC, status);

-- =====================================================
-- Documents Table Indexes
-- =====================================================

-- Composite index for entity document lookup
CREATE INDEX idx_composite_entity_documents 
ON documents(entity_type, entity_id, is_verified);

-- Index for document verification workflow
CREATE INDEX idx_document_verification 
ON documents(is_verified, uploaded_at DESC);

-- Index for document type filtering
CREATE INDEX idx_document_type_lookup 
ON documents(document_type_id, entity_type);

-- =====================================================
-- Notifications Table Indexes
-- =====================================================

-- Composite index for unread notifications
CREATE INDEX idx_composite_notifications 
ON notifications(user_id, is_read, created_at DESC);

-- Index for notification type filtering
CREATE INDEX idx_notification_type 
ON notifications(notification_type, created_at DESC);

-- =====================================================
-- Audit Logs Table Indexes
-- =====================================================

-- Composite index for audit queries
CREATE INDEX idx_composite_audit 
ON audit_logs(user_id, action, created_at DESC);

-- Index for entity audit trail
CREATE INDEX idx_audit_entity 
ON audit_logs(entity_type, entity_id, created_at DESC);

-- Index for action-based searches
CREATE INDEX idx_audit_action_date 
ON audit_logs(action, created_at DESC);

-- Index for date-range audit queries
CREATE INDEX idx_audit_date_range 
ON audit_logs(created_at DESC);

-- =====================================================
-- Users Table Additional Indexes
-- =====================================================

-- Index for active users by role
CREATE INDEX idx_users_role_active 
ON users(role, is_active, created_at DESC);

-- Index for login tracking
CREATE INDEX idx_users_last_login 
ON users(last_login DESC);

-- Fulltext search on user details
CREATE FULLTEXT INDEX idx_fulltext_user_details 
ON users(full_name, email);

-- =====================================================
-- SECTION 3: QUERY OPTIMIZATION EXAMPLES
-- =====================================================

-- Example 1: Optimized property search with covering index
-- Before optimization:
-- SELECT * FROM properties WHERE district = 'Mumbai' AND status = 'approved';

-- After optimization (use specific columns):
-- SELECT id, ulpin, property_type, area, market_value 
-- FROM properties 
-- WHERE district = 'Mumbai' AND status = 'approved'
-- ORDER BY created_at DESC;

-- Example 2: Optimized ownership lookup
-- Using composite index:
-- SELECT p.*, o.full_name 
-- FROM properties p
-- INNER JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
-- INNER JOIN owners o ON ow.owner_id = o.id
-- WHERE p.district = 'Mumbai' AND p.status = 'approved';

-- Example 3: Optimized payment history
-- SELECT payment_reference, transaction_id, amount, payment_date
-- FROM payments
-- WHERE user_id = 123 AND status = 'completed'
-- ORDER BY payment_date DESC
-- LIMIT 10;

-- =====================================================
-- SECTION 4: QUERY EXECUTION ANALYSIS
-- =====================================================

-- Analyze a complex query
EXPLAIN ANALYZE
SELECT 
    p.ulpin,
    p.property_type,
    p.market_value,
    o.full_name as owner_name,
    COUNT(d.id) as document_count
FROM properties p
INNER JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
INNER JOIN owners o ON ow.owner_id = o.id
LEFT JOIN documents d ON p.id = d.entity_id AND d.entity_type = 'property'
WHERE p.district = 'Mumbai' 
  AND p.status = 'approved'
GROUP BY p.id, o.id
ORDER BY p.market_value DESC
LIMIT 20;

-- =====================================================
-- SECTION 5: COVERING INDEXES FOR COMMON QUERIES
-- =====================================================

-- Covering index for property list view
CREATE INDEX idx_covering_property_list 
ON properties(district, status, id, ulpin, property_type, area, market_value, village_city);

-- Covering index for payment reports
CREATE INDEX idx_covering_payment_report 
ON payments(payment_date, status, payment_type, total_amount, user_id);

-- Covering index for mutation dashboard
CREATE INDEX idx_covering_mutation_dashboard 
ON mutations(status, application_date, property_id, requester_id, mutation_type);

-- =====================================================
-- SECTION 6: PARTITIONING STRATEGY
-- =====================================================

-- Partition audit_logs by date (improves query performance on large tables)
-- Note: This requires table recreation, so it's commented out
/*
ALTER TABLE audit_logs
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p_2023 VALUES LESS THAN (2024),
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- Partition payments by year
/*
ALTER TABLE payments
PARTITION BY RANGE (YEAR(payment_date)) (
    PARTITION p_2023 VALUES LESS THAN (2024),
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- =====================================================
-- SECTION 7: STATISTICS AND MAINTENANCE
-- =====================================================

-- Update table statistics for better query planning
ANALYZE TABLE properties;
ANALYZE TABLE ownerships;
ANALYZE TABLE owners;
ANALYZE TABLE mutations;
ANALYZE TABLE payments;
ANALYZE TABLE tax_assessments;
ANALYZE TABLE documents;
ANALYZE TABLE notifications;
ANALYZE TABLE audit_logs;
ANALYZE TABLE users;

-- Optimize tables (reclaim space and rebuild indexes)
OPTIMIZE TABLE properties;
OPTIMIZE TABLE ownerships;
OPTIMIZE TABLE owners;
OPTIMIZE TABLE mutations;
OPTIMIZE TABLE payments;

-- =====================================================
-- SECTION 8: INDEX USAGE MONITORING
-- =====================================================

-- Check index usage statistics
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    INDEX_NAME,
    SEQ_IN_INDEX,
    COLUMN_NAME,
    CARDINALITY,
    INDEX_TYPE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'land_registry_db'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- Check unused indexes (run after application has been in use)
SELECT 
    s.TABLE_SCHEMA,
    s.TABLE_NAME,
    s.INDEX_NAME,
    s.CARDINALITY
FROM information_schema.STATISTICS s
LEFT JOIN performance_schema.table_io_waits_summary_by_index_usage i
    ON s.TABLE_SCHEMA = i.OBJECT_SCHEMA
    AND s.TABLE_NAME = i.OBJECT_NAME
    AND s.INDEX_NAME = i.INDEX_NAME
WHERE s.TABLE_SCHEMA = 'land_registry_db'
    AND s.INDEX_NAME != 'PRIMARY'
    AND i.INDEX_NAME IS NULL;

-- =====================================================
-- SECTION 9: QUERY PERFORMANCE OPTIMIZATION TIPS
-- =====================================================

-- 1. Use LIMIT for large result sets
-- Good: SELECT * FROM properties WHERE status = 'approved' LIMIT 100;
-- Bad:  SELECT * FROM properties WHERE status = 'approved';

-- 2. Avoid SELECT * - specify only needed columns
-- Good: SELECT id, ulpin, property_type FROM properties;
-- Bad:  SELECT * FROM properties;

-- 3. Use EXPLAIN to analyze query execution
-- EXPLAIN SELECT * FROM properties WHERE district = 'Mumbai';

-- 4. Use EXISTS instead of IN for subqueries
-- Good: SELECT * FROM properties p WHERE EXISTS (SELECT 1 FROM ownerships o WHERE o.property_id = p.id);
-- Bad:  SELECT * FROM properties WHERE id IN (SELECT property_id FROM ownerships);

-- 5. Use JOINs instead of subqueries when possible
-- Good: SELECT p.* FROM properties p INNER JOIN ownerships o ON p.id = o.property_id;
-- Bad:  SELECT * FROM properties WHERE id IN (SELECT property_id FROM ownerships);

-- 6. Use UNION ALL instead of UNION when duplicates are acceptable
-- UNION ALL is faster as it doesn't remove duplicates

-- 7. Avoid functions on indexed columns in WHERE clause
-- Bad:  SELECT * FROM properties WHERE YEAR(created_at) = 2024;
-- Good: SELECT * FROM properties WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- =====================================================
-- SECTION 10: CACHE AND BUFFER OPTIMIZATION
-- =====================================================

-- Check current cache settings
SHOW VARIABLES LIKE 'query_cache%';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Recommended settings (set in my.cnf or my.ini):
-- innodb_buffer_pool_size = 1G (or 70-80% of RAM for dedicated DB server)
-- query_cache_size = 64M
-- query_cache_type = 1

-- =====================================================
-- SECTION 11: SLOW QUERY LOG ANALYSIS
-- =====================================================

-- Enable slow query log
-- SET GLOBAL slow_query_log = 'ON';
-- SET GLOBAL long_query_time = 2; -- queries taking more than 2 seconds

-- Check slow queries
-- SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- =====================================================
-- END OF OPTIMIZATION FILE
-- =====================================================

-- Summary of indexes created:
-- - 40+ strategic indexes
-- - Covering indexes for common queries
-- - Fulltext indexes for text search
-- - Composite indexes for complex queries
-- - Performance monitoring queries
-- - Optimization best practices

-- This comprehensive indexing strategy should significantly improve
-- query performance across all modules of the Land Registry Management System
