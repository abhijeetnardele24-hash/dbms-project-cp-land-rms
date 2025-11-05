-- ============================================================================
-- FIX: Remove problematic trigger that prevents property registration
-- ============================================================================
-- The after_property_insert trigger tries to UPDATE properties table
-- during INSERT, which MySQL doesn't allow
-- ULPIN is already generated in Python code during registrar approval
-- ============================================================================

USE land_registry_db;

-- Drop the problematic trigger
DROP TRIGGER IF EXISTS after_property_insert;

-- Confirm trigger is dropped
SELECT 'Trigger after_property_insert has been removed successfully!' as status;

-- Show remaining triggers (should not include after_property_insert)
SHOW TRIGGERS WHERE `Table` = 'properties';
