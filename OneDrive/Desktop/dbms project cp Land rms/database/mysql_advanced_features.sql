-- ============================================================================
-- LAND REGISTRY MANAGEMENT SYSTEM - ADVANCED MySQL FEATURES
-- ============================================================================
-- This file contains stored procedures, triggers, views, and indexes
-- to showcase MySQL's real-world capabilities
-- Password: 1234 | Database: land_registry_db
-- ============================================================================

USE land_registry_db;

-- ============================================================================
-- SECTION 1: STORED PROCEDURES
-- ============================================================================

-- Procedure 1: Calculate Property Tax
DELIMITER $$

DROP PROCEDURE IF EXISTS calculate_property_tax$$

CREATE PROCEDURE calculate_property_tax(
    IN p_property_id INT,
    IN p_tax_year INT,
    OUT p_tax_amount DECIMAL(10,2),
    OUT p_status VARCHAR(50)
)
BEGIN
    DECLARE v_market_value DECIMAL(15,2);
    DECLARE v_property_type VARCHAR(50);
    DECLARE v_area DECIMAL(10,2);
    DECLARE v_tax_rate DECIMAL(5,4);
    
    -- Get property details
    SELECT market_value, property_type, area 
    INTO v_market_value, v_property_type, v_area
    FROM properties 
    WHERE id = p_property_id;
    
    -- Check if property exists
    IF v_market_value IS NULL THEN
        SET p_status = 'ERROR: Property not found';
        SET p_tax_amount = 0;
    ELSE
        -- Calculate tax based on property type
        CASE v_property_type
            WHEN 'residential' THEN SET v_tax_rate = 0.01;  -- 1%
            WHEN 'commercial' THEN SET v_tax_rate = 0.02;   -- 2%
            WHEN 'agricultural' THEN SET v_tax_rate = 0.005; -- 0.5%
            WHEN 'industrial' THEN SET v_tax_rate = 0.025;  -- 2.5%
            ELSE SET v_tax_rate = 0.01;
        END CASE;
        
        -- Calculate final tax
        SET p_tax_amount = v_market_value * v_tax_rate;
        
        -- Insert into tax_assessments table
        INSERT INTO tax_assessments (
            property_id, 
            assessment_year, 
            assessed_value, 
            tax_amount, 
            status, 
            due_date,
            created_at
        ) VALUES (
            p_property_id,
            p_tax_year,
            v_market_value,
            p_tax_amount,
            'pending',
            DATE_ADD(CURDATE(), INTERVAL 30 DAY),
            NOW()
        );
        
        SET p_status = 'SUCCESS: Tax calculated and assessment created';
    END IF;
END$$

DELIMITER ;


-- Procedure 2: Get Complete Property Report
DELIMITER $$

DROP PROCEDURE IF EXISTS get_property_report$$

CREATE PROCEDURE get_property_report(IN p_property_id INT)
BEGIN
    -- Property basic info
    SELECT 
        p.id,
        p.ulpin,
        p.property_type,
        p.state,
        p.district,
        p.village_city,
        p.area,
        p.area_unit,
        p.market_value,
        p.latitude,
        p.longitude,
        p.status,
        p.created_at
    FROM properties p
    WHERE p.id = p_property_id;
    
    -- Ownership details
    SELECT 
        o.id,
        ow.full_name AS owner_name,
        ow.aadhar_number,
        ow.pan_number,
        o.ownership_percentage,
        o.acquisition_date,
        o.acquisition_mode
    FROM ownerships o
    JOIN owners ow ON o.owner_id = ow.id
    WHERE o.property_id = p_property_id AND o.is_active = TRUE;
    
    -- Payment history
    SELECT 
        payment_reference,
        receipt_number,
        payment_type,
        amount,
        payment_method,
        status,
        payment_date
    FROM payments
    WHERE property_id = p_property_id
    ORDER BY payment_date DESC
    LIMIT 10;
    
    -- Tax assessments
    SELECT 
        assessment_year,
        assessed_value,
        tax_amount,
        status,
        due_date,
        paid_date
    FROM tax_assessments
    WHERE property_id = p_property_id
    ORDER BY assessment_year DESC
    LIMIT 5;
END$$

DELIMITER ;


-- Procedure 3: Get Ownership Chain (Property History)
DELIMITER $$

DROP PROCEDURE IF EXISTS get_ownership_chain$$

CREATE PROCEDURE get_ownership_chain(IN p_property_id INT)
BEGIN
    SELECT 
        o.id,
        ow.full_name AS owner_name,
        o.ownership_percentage,
        o.acquisition_date,
        o.acquisition_mode,
        o.is_active,
        o.start_date,
        o.end_date,
        o.created_at
    FROM ownerships o
    JOIN owners ow ON o.owner_id = ow.id
    WHERE o.property_id = p_property_id
    ORDER BY o.acquisition_date DESC;
END$$

DELIMITER ;


-- Procedure 4: Generate Dashboard Statistics
DELIMITER $$

DROP PROCEDURE IF EXISTS get_dashboard_stats$$

CREATE PROCEDURE get_dashboard_stats()
BEGIN
    -- Overall statistics
    SELECT 
        COUNT(*) as total_properties,
        COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_properties,
        COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_properties,
        COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_properties,
        COUNT(CASE WHEN latitude IS NOT NULL THEN 1 END) as properties_with_location,
        SUM(CASE WHEN market_value IS NOT NULL THEN market_value ELSE 0 END) as total_market_value,
        AVG(area) as average_area
    FROM properties;
    
    -- Property type distribution
    SELECT 
        property_type,
        COUNT(*) as count,
        SUM(market_value) as total_value
    FROM properties
    WHERE property_type IS NOT NULL
    GROUP BY property_type;
    
    -- Revenue statistics
    SELECT 
        COUNT(*) as total_payments,
        SUM(amount) as total_revenue,
        SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) as completed_revenue,
        SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) as pending_revenue
    FROM payments;
    
    -- Recent registrations
    SELECT 
        DATE(created_at) as registration_date,
        COUNT(*) as count
    FROM properties
    WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY DATE(created_at)
    ORDER BY registration_date DESC;
END$$

DELIMITER ;


-- ============================================================================
-- SECTION 2: TRIGGERS
-- ============================================================================

-- Trigger 1: Auto-generate ULPIN after property insert
DELIMITER $$

DROP TRIGGER IF EXISTS after_property_insert$$

CREATE TRIGGER after_property_insert
AFTER INSERT ON properties
FOR EACH ROW
BEGIN
    DECLARE v_ulpin VARCHAR(50);
    
    -- Generate ULPIN if not provided
    IF NEW.ulpin IS NULL THEN
        SET v_ulpin = CONCAT(
            UPPER(LEFT(NEW.state, 2)),
            UPPER(LEFT(NEW.district, 3)),
            UPPER(LEFT(NEW.village_city, 3)),
            YEAR(CURDATE()),
            LPAD(NEW.id, 6, '0')
        );
        
        UPDATE properties 
        SET ulpin = v_ulpin 
        WHERE id = NEW.id;
    END IF;
END$$

DELIMITER ;


-- Trigger 2: Log property updates to audit table
DELIMITER $$

DROP TRIGGER IF EXISTS before_property_update$$

CREATE TRIGGER before_property_update
BEFORE UPDATE ON properties
FOR EACH ROW
BEGIN
    -- Insert audit log entry
    INSERT INTO audit_logs (
        user_id,
        entity_type,
        entity_id,
        action,
        old_data,
        new_data,
        ip_address,
        created_at
    ) VALUES (
        @current_user_id,  -- Set via application
        'property',
        OLD.id,
        'UPDATE',
        JSON_OBJECT(
            'status', OLD.status,
            'market_value', OLD.market_value,
            'latitude', OLD.latitude,
            'longitude', OLD.longitude
        ),
        JSON_OBJECT(
            'status', NEW.status,
            'market_value', NEW.market_value,
            'latitude', NEW.latitude,
            'longitude', NEW.longitude
        ),
        @current_user_ip,
        NOW()
    );
END$$

DELIMITER ;


-- Trigger 3: Update tax assessment status after payment
DELIMITER $$

DROP TRIGGER IF EXISTS after_payment_insert$$

CREATE TRIGGER after_payment_insert
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    -- If payment is for property tax, update tax assessment
    IF NEW.payment_type = 'property_tax' AND NEW.status = 'completed' THEN
        UPDATE tax_assessments
        SET status = 'paid',
            paid_date = NEW.payment_date,
            paid_amount = NEW.amount
        WHERE property_id = NEW.property_id
        AND assessment_year = NEW.tax_year
        AND status = 'pending';
    END IF;
END$$

DELIMITER ;


-- Trigger 4: Create notification after property approval
DELIMITER $$

DROP TRIGGER IF EXISTS after_property_status_update$$

CREATE TRIGGER after_property_status_update
AFTER UPDATE ON properties
FOR EACH ROW
BEGIN
    DECLARE v_owner_user_id INT;
    
    -- Check if status changed to approved or rejected
    IF OLD.status != NEW.status AND (NEW.status = 'approved' OR NEW.status = 'rejected') THEN
        -- Get owner's user_id
        SELECT u.id INTO v_owner_user_id
        FROM ownerships o
        JOIN owners ow ON o.owner_id = ow.id
        JOIN users u ON ow.user_id = u.id
        WHERE o.property_id = NEW.id AND o.is_active = TRUE
        LIMIT 1;
        
        -- Create notification
        IF v_owner_user_id IS NOT NULL THEN
            INSERT INTO notifications (
                user_id,
                notification_type,
                title,
                message,
                related_entity_type,
                related_entity_id,
                is_read,
                created_at
            ) VALUES (
                v_owner_user_id,
                CONCAT('property_', NEW.status),
                CONCAT('Property ', NEW.status),
                CONCAT('Your property registration (ULPIN: ', NEW.ulpin, ') has been ', NEW.status),
                'property',
                NEW.id,
                FALSE,
                NOW()
            );
        END IF;
    END IF;
END$$

DELIMITER ;


-- ============================================================================
-- SECTION 3: VIEWS
-- ============================================================================

-- View 1: Property Dashboard Statistics
CREATE OR REPLACE VIEW v_property_dashboard_stats AS
SELECT 
    COUNT(*) as total_properties,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_properties,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_properties,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_properties,
    COUNT(CASE WHEN status = 'under_review' THEN 1 END) as under_review_properties,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as properties_with_location,
    SUM(CASE WHEN market_value IS NOT NULL THEN market_value ELSE 0 END) as total_market_value,
    AVG(area) as average_area,
    AVG(market_value) as average_market_value
FROM properties;


-- View 2: Revenue Analytics
CREATE OR REPLACE VIEW v_revenue_analytics AS
SELECT 
    YEAR(payment_date) as payment_year,
    MONTH(payment_date) as payment_month,
    payment_type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) as completed_amount,
    SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) as pending_amount,
    AVG(amount) as average_amount
FROM payments
GROUP BY YEAR(payment_date), MONTH(payment_date), payment_type
ORDER BY payment_year DESC, payment_month DESC;


-- View 3: Property Details with Owner Info
CREATE OR REPLACE VIEW v_property_with_owners AS
SELECT 
    p.id as property_id,
    p.ulpin,
    p.property_type,
    p.state,
    p.district,
    p.village_city,
    p.locality,
    p.area,
    p.area_unit,
    p.market_value,
    p.latitude,
    p.longitude,
    p.status as property_status,
    p.created_at as registration_date,
    o.id as ownership_id,
    ow.full_name as owner_name,
    ow.aadhar_number,
    ow.pan_number,
    ow.mobile_number,
    ow.email as owner_email,
    o.ownership_percentage,
    o.acquisition_date,
    u.full_name as registered_by_user,
    u.email as user_email
FROM properties p
LEFT JOIN ownerships o ON p.id = o.property_id AND o.is_active = TRUE
LEFT JOIN owners ow ON o.owner_id = ow.id
LEFT JOIN users u ON ow.user_id = u.id
WHERE p.status IN ('approved', 'pending', 'under_review');


-- View 4: Pending Approvals Summary
CREATE OR REPLACE VIEW v_pending_approvals AS
SELECT 
    p.id,
    p.ulpin,
    p.property_type,
    p.village_city,
    p.district,
    p.state,
    p.area,
    p.area_unit,
    p.status,
    p.created_at,
    DATEDIFF(CURDATE(), p.created_at) as days_pending,
    ow.full_name as owner_name,
    ow.mobile_number as owner_mobile,
    COUNT(d.id) as document_count
FROM properties p
LEFT JOIN ownerships o ON p.id = o.property_id AND o.is_active = TRUE
LEFT JOIN owners ow ON o.owner_id = ow.id
LEFT JOIN documents d ON p.id = d.property_id
WHERE p.status IN ('pending', 'under_review')
GROUP BY p.id, p.ulpin, p.property_type, p.village_city, p.district, p.state, 
         p.area, p.area_unit, p.status, p.created_at, ow.full_name, ow.mobile_number
ORDER BY p.created_at ASC;


-- View 5: Tax Collection Summary
CREATE OR REPLACE VIEW v_tax_collection_summary AS
SELECT 
    t.assessment_year,
    COUNT(*) as total_assessments,
    SUM(t.tax_amount) as total_tax_assessed,
    SUM(CASE WHEN t.status = 'paid' THEN t.paid_amount ELSE 0 END) as total_collected,
    SUM(CASE WHEN t.status = 'pending' THEN t.tax_amount ELSE 0 END) as total_pending,
    SUM(CASE WHEN t.status = 'overdue' THEN t.tax_amount ELSE 0 END) as total_overdue,
    COUNT(CASE WHEN t.status = 'paid' THEN 1 END) as paid_count,
    COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN t.status = 'overdue' THEN 1 END) as overdue_count
FROM tax_assessments t
GROUP BY t.assessment_year
ORDER BY t.assessment_year DESC;


-- View 6: Recent Activity Log
CREATE OR REPLACE VIEW v_recent_activity AS
SELECT 
    a.id,
    a.action,
    a.entity_type,
    a.entity_id,
    u.full_name as performed_by,
    u.role as user_role,
    a.created_at,
    a.ip_address
FROM audit_logs a
JOIN users u ON a.user_id = u.id
ORDER BY a.created_at DESC
LIMIT 100;


-- View 7: Geographic Property Distribution
CREATE OR REPLACE VIEW v_geographic_distribution AS
SELECT 
    state,
    district,
    COUNT(*) as property_count,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved_count,
    SUM(area) as total_area,
    AVG(market_value) as avg_market_value,
    COUNT(CASE WHEN latitude IS NOT NULL THEN 1 END) as mapped_properties
FROM properties
GROUP BY state, district
ORDER BY property_count DESC;


-- ============================================================================
-- SECTION 4: INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Index on ULPIN (frequently searched)
CREATE INDEX idx_properties_ulpin ON properties(ulpin);

-- Composite index for location searches
CREATE INDEX idx_properties_location ON properties(state, district, village_city);

-- Index for status filtering
CREATE INDEX idx_properties_status ON properties(status);

-- Index for date-based queries
CREATE INDEX idx_properties_created ON properties(created_at);

-- Index for GPS coordinates (map searches)
CREATE INDEX idx_properties_coordinates ON properties(latitude, longitude);

-- Full-text index for property search
ALTER TABLE properties ADD FULLTEXT INDEX ft_property_search (
    village_city, locality, street_address, description
);

-- Index on payments for faster queries
CREATE INDEX idx_payments_property ON payments(property_id, payment_date);
CREATE INDEX idx_payments_user ON payments(user_id, status);
CREATE INDEX idx_payments_reference ON payments(payment_reference);

-- Index on ownerships
CREATE INDEX idx_ownerships_property ON ownerships(property_id, is_active);
CREATE INDEX idx_ownerships_owner ON ownerships(owner_id, is_active);


-- ============================================================================
-- SECTION 5: SAMPLE USAGE QUERIES
-- ============================================================================

-- Example 1: Calculate tax for a property
/*
CALL calculate_property_tax(1, 2025, @tax_amount, @status);
SELECT @tax_amount as calculated_tax, @status as result_status;
*/

-- Example 2: Get complete property report
/*
CALL get_property_report(1);
*/

-- Example 3: Get ownership chain
/*
CALL get_ownership_chain(1);
*/

-- Example 4: Get dashboard statistics
/*
CALL get_dashboard_stats();
*/

-- Example 5: Query views
/*
SELECT * FROM v_property_dashboard_stats;
SELECT * FROM v_revenue_analytics WHERE payment_year = 2025;
SELECT * FROM v_pending_approvals;
SELECT * FROM v_tax_collection_summary;
SELECT * FROM v_geographic_distribution;
*/

-- Example 6: Full-text search
/*
SELECT id, ulpin, village_city, description
FROM properties
WHERE MATCH(village_city, locality, street_address, description) 
AGAINST ('mumbai residential' IN NATURAL LANGUAGE MODE);
*/


-- ============================================================================
-- END OF ADVANCED MySQL FEATURES
-- ============================================================================
-- Run this entire file in MySQL Workbench to create all procedures, triggers, views
-- Password: 1234 | Database: land_registry_db
-- ============================================================================
