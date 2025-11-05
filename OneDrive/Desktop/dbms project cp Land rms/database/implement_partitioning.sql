-- =====================================================
-- TABLE PARTITIONING IMPLEMENTATION
-- For scalability with large datasets
-- =====================================================

USE land_registry_db;

-- NOTE: Partitioning requires the table to not have existing data
-- or to be done carefully with ALTER TABLE

-- =====================================================
-- 1. PARTITION AUDIT_LOGS BY YEAR
-- =====================================================

-- Check if table has data
SELECT COUNT(*) AS audit_log_count FROM audit_logs;

-- Partitioning strategy: Range partition by year
-- This allows efficient querying and purging of old data

-- If table is empty, use CREATE TABLE with partitioning
-- If table has data, we need to:
-- 1. Backup data
-- 2. Drop table
-- 3. Recreate with partitioning
-- 4. Restore data

-- For demonstration, here's the partition structure:
/*
ALTER TABLE audit_logs
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- =====================================================
-- 2. PARTITION PAYMENTS BY YEAR
-- =====================================================

SELECT COUNT(*) AS payments_count FROM payments;

-- Partitioning strategy: Range partition by year of payment
/*
ALTER TABLE payments
PARTITION BY RANGE (YEAR(payment_date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- =====================================================
-- BENEFITS OF PARTITIONING
-- =====================================================
-- 1. Faster queries on date ranges (partition pruning)
-- 2. Easy archival of old data (drop old partitions)
-- 3. Better performance on large tables (1M+ rows)
-- 4. Parallel query execution per partition
-- 5. Maintenance operations can be per-partition

-- =====================================================
-- MONITORING PARTITIONS
-- =====================================================

-- View partition information
SELECT 
    TABLE_NAME,
    PARTITION_NAME,
    PARTITION_METHOD,
    PARTITION_EXPRESSION,
    TABLE_ROWS
FROM information_schema.PARTITIONS
WHERE TABLE_SCHEMA = 'land_registry_db'
  AND TABLE_NAME IN ('audit_logs', 'payments')
ORDER BY TABLE_NAME, PARTITION_ORDINAL_POSITION;

-- =====================================================
-- MAINTENANCE OPERATIONS
-- =====================================================

-- Add new partition for next year
-- ALTER TABLE audit_logs ADD PARTITION (PARTITION p2027 VALUES LESS THAN (2028));

-- Drop old partition (archival)
-- ALTER TABLE audit_logs DROP PARTITION p2020;

-- Rebuild partition
-- ALTER TABLE audit_logs REBUILD PARTITION p2024;

-- Optimize partition
-- ALTER TABLE audit_logs OPTIMIZE PARTITION p2024;

SELECT '✅ Partitioning strategy documented!' AS status,
       'Apply ALTER TABLE statements when ready for production' AS note;
