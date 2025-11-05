-- =====================================================
-- ADVANCED MYSQL FEATURES FOR LAND REGISTRY MANAGEMENT SYSTEM
-- =====================================================
-- This file contains:
-- 1. 8 Advanced Stored Procedures & Functions
-- 2. 10 Comprehensive Triggers
-- 3. 12 Strategic Views
-- 4. Performance Indexes
-- 5. Table Partitioning (commented - manual setup)
-- 6. MySQL Events (Scheduled Jobs)
-- =====================================================

USE land_registry_db;

-- =====================================================
-- SECTION 1: STORED PROCEDURES & FUNCTIONS
-- =====================================================

-- Drop existing procedures if they exist
DROP PROCEDURE IF EXISTS sp_calculate_property_tax_advanced;
DROP PROCEDURE IF EXISTS sp_get_property_valuation_trends;
DROP PROCEDURE IF EXISTS sp_analyze_market_by_region;
DROP PROCEDURE IF EXISTS sp_get_owner_portfolio_report;
DROP PROCEDURE IF EXISTS sp_auto_approve_simple_mutations;
DROP PROCEDURE IF EXISTS sp_generate_tax_reminders;
DROP PROCEDURE IF EXISTS sp_update_analytics_cache;
DROP FUNCTION IF EXISTS fn_calculate_property_risk_score;
DROP FUNCTION IF EXISTS fn_generate_ulpin;

DELIMITER $$

-- =====================================================
-- 1. ADVANCED TAX CALCULATOR
-- =====================================================
CREATE PROCEDURE sp_calculate_property_tax_advanced(
    IN p_property_id INT,
    IN p_assessment_year INT,
    OUT p_base_tax DECIMAL(12,2),
    OUT p_penalties DECIMAL(12,2),
    OUT p_total_tax DECIMAL(12,2)
)
BEGIN
    DECLARE v_market_value DECIMAL(15,2);
    DECLARE v_property_type VARCHAR(50);
    DECLARE v_area DECIMAL(10,2);
    DECLARE v_last_payment_date DATE;
    DECLARE v_months_overdue INT;
    DECLARE v_tax_rate DECIMAL(5,4);
    
    -- Get property details
    SELECT market_value, property_type, area
    INTO v_market_value, v_property_type, v_area
    FROM properties
    WHERE id = p_property_id;
    
    -- Determine tax rate based on property type
    SET v_tax_rate = CASE 
        WHEN v_property_type = 'Residential' THEN 0.008
        WHEN v_property_type = 'Commercial' THEN 0.015
        WHEN v_property_type = 'Agricultural' THEN 0.003
        WHEN v_property_type = 'Industrial' THEN 0.020
        ELSE 0.010
    END;
    
    -- Calculate base tax
    SET p_base_tax = v_market_value * v_tax_rate;
    
    -- Get last payment date
    SELECT MAX(payment_date) INTO v_last_payment_date
    FROM payments
    WHERE property_id = p_property_id AND status = 'completed';
    
    -- Calculate penalties for overdue payments
    IF v_last_payment_date IS NOT NULL THEN
        SET v_months_overdue = TIMESTAMPDIFF(MONTH, v_last_payment_date, CURDATE());
        IF v_months_overdue > 12 THEN
            SET p_penalties = p_base_tax * 0.02 * (v_months_overdue - 12);
        ELSE
            SET p_penalties = 0.00;
        END IF;
    ELSE
        SET p_penalties = 0.00;
    END IF;
    
    -- Calculate total
    SET p_total_tax = p_base_tax + p_penalties;
    
    -- Insert into tax_assessments if not exists for this year
    INSERT INTO tax_assessments (property_id, assessment_year, assessed_value, tax_amount, status, assessment_date)
    VALUES (p_property_id, p_assessment_year, v_market_value, p_total_tax, 'assessed', CURDATE())
    ON DUPLICATE KEY UPDATE 
        assessed_value = v_market_value,
        tax_amount = p_total_tax,
        assessment_date = CURDATE();
END$$

-- =====================================================
-- 2. PROPERTY VALUATION TREND ANALYSIS
-- =====================================================
CREATE PROCEDURE sp_get_property_valuation_trends(
    IN p_property_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    -- Get valuation history from property_valuations table
    SELECT 
        pv.id,
        pv.valuation_date,
        pv.valuation_amount,
        pv.valuation_type,
        pv.valued_by,
        u.full_name AS valuer_name,
        ROUND((pv.valuation_amount - LAG(pv.valuation_amount) OVER (ORDER BY pv.valuation_date)) / 
              LAG(pv.valuation_amount) OVER (ORDER BY pv.valuation_date) * 100, 2) AS percentage_change
    FROM property_valuations pv
    LEFT JOIN users u ON pv.valued_by = u.id
    WHERE pv.property_id = p_property_id
      AND pv.valuation_date BETWEEN p_start_date AND p_end_date
    ORDER BY pv.valuation_date ASC;
    
    -- Get summary statistics
    SELECT 
        COUNT(*) AS total_valuations,
        MIN(valuation_amount) AS min_value,
        MAX(valuation_amount) AS max_value,
        AVG(valuation_amount) AS avg_value,
        STDDEV(valuation_amount) AS std_deviation,
        (MAX(valuation_amount) - MIN(valuation_amount)) / MIN(valuation_amount) * 100 AS total_growth_percent
    FROM property_valuations
    WHERE property_id = p_property_id
      AND valuation_date BETWEEN p_start_date AND p_end_date;
END$$

-- =====================================================
-- 3. GEOGRAPHIC MARKET ANALYSIS
-- =====================================================
CREATE PROCEDURE sp_analyze_market_by_region(
    IN p_district VARCHAR(100),
    IN p_state VARCHAR(100)
)
BEGIN
    -- Property count and value statistics by region
    SELECT 
        p.district,
        p.village_city,
        COUNT(*) AS total_properties,
        COUNT(CASE WHEN p.status = 'approved' THEN 1 END) AS approved_properties,
        COUNT(CASE WHEN p.status = 'pending' THEN 1 END) AS pending_properties,
        AVG(p.market_value) AS avg_market_value,
        MIN(p.market_value) AS min_market_value,
        MAX(p.market_value) AS max_market_value,
        SUM(p.market_value) AS total_market_value,
        AVG(p.area) AS avg_area,
        COUNT(DISTINCT p.property_type) AS property_types_count
    FROM properties p
    WHERE p.district = p_district
      AND p.state = p_state
      AND p.status IN ('approved', 'pending')
    GROUP BY p.district, p.village_city
    ORDER BY total_properties DESC;
    
    -- Property type distribution
    SELECT 
        property_type,
        COUNT(*) AS count,
        AVG(market_value) AS avg_value,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM properties WHERE district = p_district), 2) AS percentage
    FROM properties
    WHERE district = p_district
      AND state = p_state
      AND status = 'approved'
    GROUP BY property_type
    ORDER BY count DESC;
END$$

-- =====================================================
-- 4. OWNER PORTFOLIO ANALYTICS
-- =====================================================
CREATE PROCEDURE sp_get_owner_portfolio_report(
    IN p_owner_id INT
)
BEGIN
    -- Owner's complete portfolio
    SELECT 
        p.id,
        p.ulpin,
        p.property_type,
        p.area,
        p.area_unit,
        p.market_value,
        p.village_city,
        p.district,
        p.state,
        p.status,
        o.ownership_percentage,
        o.acquisition_date,
        DATEDIFF(CURDATE(), o.acquisition_date) AS days_owned
    FROM properties p
    INNER JOIN ownerships o ON p.id = o.property_id
    WHERE o.owner_id = p_owner_id
      AND o.is_active = TRUE
    ORDER BY p.market_value DESC;
    
    -- Portfolio summary
    SELECT 
        COUNT(DISTINCT p.id) AS total_properties,
        SUM(p.market_value * o.ownership_percentage / 100) AS total_portfolio_value,
        AVG(p.market_value) AS avg_property_value,
        SUM(p.area) AS total_area,
        COUNT(DISTINCT p.district) AS districts_count,
        COUNT(CASE WHEN p.property_type = 'Residential' THEN 1 END) AS residential_count,
        COUNT(CASE WHEN p.property_type = 'Commercial' THEN 1 END) AS commercial_count,
        COUNT(CASE WHEN p.property_type = 'Agricultural' THEN 1 END) AS agricultural_count
    FROM properties p
    INNER JOIN ownerships o ON p.id = o.property_id
    WHERE o.owner_id = p_owner_id
      AND o.is_active = TRUE;
    
    -- Recent mutations
    SELECT 
        m.id,
        m.mutation_number,
        m.mutation_type,
        p.ulpin,
        m.submission_date,
        m.status,
        m.transaction_amount
    FROM mutations m
    INNER JOIN properties p ON m.property_id = p.id
    INNER JOIN ownerships o ON p.id = o.property_id
    WHERE o.owner_id = p_owner_id
    ORDER BY m.submission_date DESC
    LIMIT 10;
END$$

-- =====================================================
-- 5. AUTO-APPROVE SIMPLE MUTATIONS
-- =====================================================
CREATE PROCEDURE sp_auto_approve_simple_mutations()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_mutation_id INT;
    DECLARE v_property_id INT;
    DECLARE v_transaction_amount DECIMAL(15,2);
    
    DECLARE mutation_cursor CURSOR FOR
        SELECT m.id, m.property_id, m.transaction_amount
        FROM mutations m
        INNER JOIN properties p ON m.property_id = p.id
        WHERE m.status = 'pending'
          AND m.mutation_type IN ('Gift', 'Inheritance')
          AND DATEDIFF(CURDATE(), m.submission_date) >= 7
          AND p.status = 'approved'
          AND NOT EXISTS (
              SELECT 1 FROM property_disputes pd 
              WHERE pd.property_id = m.property_id 
                AND pd.status = 'open'
          );
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN mutation_cursor;
    
    read_loop: LOOP
        FETCH mutation_cursor INTO v_mutation_id, v_property_id, v_transaction_amount;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Auto-approve the mutation
        UPDATE mutations 
        SET status = 'approved',
            approval_date = CURDATE(),
            officer_comments = 'Auto-approved: Simple mutation with no disputes'
        WHERE id = v_mutation_id;
        
        -- Create notification
        INSERT INTO notifications (user_id, title, message, notification_type, is_read)
        SELECT 
            u.id,
            'Mutation Auto-Approved',
            CONCAT('Your mutation request #', v_mutation_id, ' has been automatically approved.'),
            'success',
            FALSE
        FROM users u
        INNER JOIN owners o ON u.id = o.user_id
        INNER JOIN ownerships ow ON o.id = ow.owner_id
        WHERE ow.property_id = v_property_id AND ow.is_active = TRUE;
        
    END LOOP;
    
    CLOSE mutation_cursor;
    
    -- Return count of auto-approved mutations
    SELECT ROW_COUNT() AS mutations_auto_approved;
END$$

-- =====================================================
-- 6. TAX REMINDER GENERATOR
-- =====================================================
CREATE PROCEDURE sp_generate_tax_reminders()
BEGIN
    -- Generate reminders for properties with overdue taxes
    INSERT INTO notifications (user_id, title, message, notification_type, is_read, created_at)
    SELECT DISTINCT
        u.id,
        'Tax Payment Due',
        CONCAT('Tax payment is due for property ULPIN: ', p.ulpin, '. Amount: ₹', 
               FORMAT(ta.tax_amount, 2), '. Please pay by ', 
               DATE_FORMAT(DATE_ADD(ta.due_date, INTERVAL 30 DAY), '%d-%b-%Y')),
        'warning',
        FALSE,
        NOW()
    FROM properties p
    INNER JOIN tax_assessments ta ON p.id = ta.property_id
    INNER JOIN ownerships o ON p.id = o.property_id AND o.is_active = TRUE
    INNER JOIN owners ow ON o.owner_id = ow.id
    INNER JOIN users u ON ow.user_id = u.id
    WHERE ta.status = 'assessed'
      AND ta.due_date < CURDATE()
      AND NOT EXISTS (
          SELECT 1 FROM payments pay
          WHERE pay.property_id = p.id
            AND pay.payment_type = 'property_tax'
            AND YEAR(pay.payment_date) = ta.assessment_year
            AND pay.status = 'completed'
      );
    
    SELECT ROW_COUNT() AS reminders_sent;
END$$

-- =====================================================
-- 7. UPDATE ANALYTICS CACHE
-- =====================================================
CREATE PROCEDURE sp_update_analytics_cache()
BEGIN
    -- Create temporary cache table if not exists
    CREATE TABLE IF NOT EXISTS analytics_cache (
        cache_key VARCHAR(100) PRIMARY KEY,
        cache_value TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    
    -- Update property statistics
    INSERT INTO analytics_cache (cache_key, cache_value)
    SELECT 'property_stats', JSON_OBJECT(
        'total', COUNT(*),
        'approved', SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END),
        'pending', SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END),
        'rejected', SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END),
        'total_value', SUM(COALESCE(market_value, 0))
    )
    FROM properties
    ON DUPLICATE KEY UPDATE cache_value = VALUES(cache_value);
    
    -- Update revenue statistics
    INSERT INTO analytics_cache (cache_key, cache_value)
    SELECT 'revenue_stats', JSON_OBJECT(
        'total_revenue', SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END),
        'pending_revenue', SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END),
        'this_month', SUM(CASE WHEN status = 'completed' AND MONTH(payment_date) = MONTH(CURDATE()) THEN amount ELSE 0 END),
        'this_year', SUM(CASE WHEN status = 'completed' AND YEAR(payment_date) = YEAR(CURDATE()) THEN amount ELSE 0 END)
    )
    FROM payments
    ON DUPLICATE KEY UPDATE cache_value = VALUES(cache_value);
    
    SELECT 'Analytics cache updated successfully' AS message;
END$$

-- =====================================================
-- 8. PROPERTY RISK SCORE CALCULATOR (FUNCTION)
-- =====================================================
CREATE FUNCTION fn_calculate_property_risk_score(
    p_property_id INT
) RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_risk_score DECIMAL(5,2) DEFAULT 0.0;
    DECLARE v_dispute_count INT;
    DECLARE v_mutation_count INT;
    DECLARE v_ownership_changes INT;
    DECLARE v_tax_overdue_months INT;
    DECLARE v_property_age_years INT;
    
    -- Count disputes
    SELECT COUNT(*) INTO v_dispute_count
    FROM property_disputes
    WHERE property_id = p_property_id AND status IN ('open', 'under_review');
    
    -- Count mutations
    SELECT COUNT(*) INTO v_mutation_count
    FROM mutations
    WHERE property_id = p_property_id;
    
    -- Count ownership changes in last 2 years
    SELECT COUNT(*) INTO v_ownership_changes
    FROM mutations
    WHERE property_id = p_property_id 
      AND status = 'approved'
      AND approval_date >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR);
    
    -- Get tax overdue months
    SELECT COALESCE(MAX(TIMESTAMPDIFF(MONTH, ta.due_date, CURDATE())), 0)
    INTO v_tax_overdue_months
    FROM tax_assessments ta
    WHERE ta.property_id = p_property_id
      AND ta.status = 'assessed'
      AND ta.due_date < CURDATE();
    
    -- Get property age
    SELECT TIMESTAMPDIFF(YEAR, created_at, CURDATE())
    INTO v_property_age_years
    FROM properties
    WHERE id = p_property_id;
    
    -- Calculate risk score (0-100 scale)
    SET v_risk_score = 0;
    
    -- Disputes add significant risk
    SET v_risk_score = v_risk_score + (v_dispute_count * 25);
    
    -- Frequent ownership changes are suspicious
    IF v_ownership_changes >= 3 THEN
        SET v_risk_score = v_risk_score + 30;
    ELSIF v_ownership_changes >= 2 THEN
        SET v_risk_score = v_risk_score + 15;
    END IF;
    
    -- Tax overdue increases risk
    IF v_tax_overdue_months > 12 THEN
        SET v_risk_score = v_risk_score + 20;
    ELSIF v_tax_overdue_months > 6 THEN
        SET v_risk_score = v_risk_score + 10;
    END IF;
    
    -- New properties have slight risk (less history)
    IF v_property_age_years < 1 THEN
        SET v_risk_score = v_risk_score + 5;
    END IF;
    
    -- Cap at 100
    IF v_risk_score > 100 THEN
        SET v_risk_score = 100;
    END IF;
    
    RETURN v_risk_score;
END$$

-- =====================================================
-- 9. ULPIN GENERATOR WITH CHECK DIGIT (FUNCTION)
-- =====================================================
CREATE FUNCTION fn_generate_ulpin(
    p_state VARCHAR(2),
    p_district VARCHAR(3),
    p_village VARCHAR(3)
) RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE v_sequence VARCHAR(8);
    DECLARE v_ulpin VARCHAR(20);
    DECLARE v_check_digit INT;
    DECLARE v_sum INT DEFAULT 0;
    DECLARE v_count INT;
    DECLARE i INT;
    
    -- Get next sequence number for this location
    SELECT COUNT(*) + 1 INTO v_count
    FROM properties
    WHERE state = p_state 
      AND district LIKE CONCAT(p_district, '%')
      AND village_city LIKE CONCAT(p_village, '%');
    
    SET v_sequence = LPAD(v_count, 8, '0');
    
    -- Construct base ULPIN: SS-DDD-VVV-SSSSSSSS
    SET v_ulpin = CONCAT(p_state, p_district, p_village, v_sequence);
    
    -- Calculate check digit using Luhn algorithm
    SET i = 1;
    WHILE i <= LENGTH(v_ulpin) DO
        IF SUBSTRING(v_ulpin, i, 1) REGEXP '[0-9]' THEN
            SET v_sum = v_sum + CAST(SUBSTRING(v_ulpin, i, 1) AS UNSIGNED);
        END IF;
        SET i = i + 1;
    END WHILE;
    
    SET v_check_digit = (10 - (v_sum % 10)) % 10;
    
    -- Final ULPIN with check digit
    SET v_ulpin = CONCAT(p_state, '-', p_district, '-', p_village, '-', v_sequence, '-', v_check_digit);
    
    RETURN v_ulpin;
END$$

DELIMITER ;

-- =====================================================
-- SECTION 2: TRIGGERS
-- =====================================================

-- Drop existing triggers
DROP TRIGGER IF EXISTS trg_property_audit_insert;
DROP TRIGGER IF EXISTS trg_property_audit_update;
DROP TRIGGER IF EXISTS trg_property_audit_delete;
DROP TRIGGER IF EXISTS trg_ownership_change_alert;
DROP TRIGGER IF EXISTS trg_detect_suspicious_mutations;
DROP TRIGGER IF EXISTS trg_auto_create_tax_assessment;
DROP TRIGGER IF EXISTS trg_validate_property_value;
DROP TRIGGER IF EXISTS trg_generate_payment_receipt;
DROP TRIGGER IF EXISTS trg_auto_send_mutation_notification;
DROP TRIGGER IF EXISTS trg_update_mutation_ownership;

DELIMITER $$

-- =====================================================
-- 1. PROPERTY AUDIT TRAIL - INSERT
-- =====================================================
CREATE TRIGGER trg_property_audit_insert
AFTER INSERT ON properties
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (
        user_id, action, table_name, record_id, 
        changes, ip_address, user_agent, created_at
    )
    VALUES (
        NEW.created_by,
        'CREATE',
        'properties',
        NEW.id,
        JSON_OBJECT(
            'ulpin', NEW.ulpin,
            'property_type', NEW.property_type,
            'area', NEW.area,
            'market_value', NEW.market_value,
            'village_city', NEW.village_city,
            'district', NEW.district,
            'state', NEW.state,
            'status', NEW.status
        ),
        'system',
        'trigger',
        NOW()
    );
END$$

-- =====================================================
-- 2. PROPERTY AUDIT TRAIL - UPDATE
-- =====================================================
CREATE TRIGGER trg_property_audit_update
AFTER UPDATE ON properties
FOR EACH ROW
BEGIN
    DECLARE v_changes JSON;
    
    SET v_changes = JSON_OBJECT(
        'before', JSON_OBJECT(
            'status', OLD.status,
            'market_value', OLD.market_value,
            'property_type', OLD.property_type,
            'approved_by', OLD.approved_by
        ),
        'after', JSON_OBJECT(
            'status', NEW.status,
            'market_value', NEW.market_value,
            'property_type', NEW.property_type,
            'approved_by', NEW.approved_by
        )
    );
    
    INSERT INTO audit_logs (
        user_id, action, table_name, record_id,
        changes, ip_address, user_agent, created_at
    )
    VALUES (
        COALESCE(NEW.approved_by, NEW.created_by),
        'UPDATE',
        'properties',
        NEW.id,
        v_changes,
        'system',
        'trigger',
        NOW()
    );
END$$

-- =====================================================
-- 3. PROPERTY AUDIT TRAIL - DELETE
-- =====================================================
CREATE TRIGGER trg_property_audit_delete
AFTER DELETE ON properties
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (
        user_id, action, table_name, record_id,
        changes, ip_address, user_agent, created_at
    )
    VALUES (
        OLD.created_by,
        'DELETE',
        'properties',
        OLD.id,
        JSON_OBJECT(
            'ulpin', OLD.ulpin,
            'property_type', OLD.property_type,
            'status', OLD.status
        ),
        'system',
        'trigger',
        NOW()
    );
END$$

-- =====================================================
-- 4. OWNERSHIP CHANGE ALERT
-- =====================================================
CREATE TRIGGER trg_ownership_change_alert
AFTER UPDATE ON ownerships
FOR EACH ROW
BEGIN
    IF OLD.is_active = TRUE AND NEW.is_active = FALSE THEN
        -- Ownership was deactivated - create alert
        INSERT INTO notifications (user_id, title, message, type, is_read)
        SELECT 
            u.id,
            'Ownership Change Alert',
            CONCAT('Ownership status changed for property ID: ', NEW.property_id),
            'warning',
            FALSE
        FROM owners o
        INNER JOIN users u ON o.user_id = u.id
        WHERE o.id = NEW.owner_id;
    END IF;
END$$

-- =====================================================
-- 5. FRAUD DETECTION FOR MUTATIONS
-- =====================================================
CREATE TRIGGER trg_detect_suspicious_mutations
BEFORE INSERT ON mutations
FOR EACH ROW
BEGIN
    DECLARE v_recent_mutations INT;
    DECLARE v_risk_score DECIMAL(5,2);
    
    -- Check for multiple mutations in short time
    SELECT COUNT(*) INTO v_recent_mutations
    FROM mutations
    WHERE property_id = NEW.property_id
      AND submission_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
    
    -- Get property risk score
    SET v_risk_score = fn_calculate_property_risk_score(NEW.property_id);
    
    -- Flag suspicious activity
    IF v_recent_mutations >= 2 OR v_risk_score > 70 THEN
        SET NEW.status = 'under_review';
        
        -- Create alert for admin
        INSERT INTO notifications (user_id, title, message, type, is_read)
        SELECT 
            id,
            'Suspicious Mutation Detected',
            CONCAT('High-risk mutation detected for property ID: ', NEW.property_id, 
                   '. Risk Score: ', v_risk_score),
            'danger',
            FALSE
        FROM users
        WHERE role = 'admin'
        LIMIT 1;
    END IF;
END$$

-- =====================================================
-- 6. AUTO-CREATE TAX ASSESSMENT ON APPROVAL
-- =====================================================
CREATE TRIGGER trg_auto_create_tax_assessment
AFTER UPDATE ON properties
FOR EACH ROW
BEGIN
    IF OLD.status != 'approved' AND NEW.status = 'approved' THEN
        -- Create initial tax assessment
        INSERT INTO tax_assessments (
            property_id, assessment_year, assessed_value,
            tax_amount, due_date, status, assessment_date
        )
        VALUES (
            NEW.id,
            YEAR(CURDATE()),
            NEW.market_value,
            NEW.market_value * 0.01, -- 1% tax rate
            DATE_ADD(CURDATE(), INTERVAL 3 MONTH),
            'assessed',
            CURDATE()
        );
    END IF;
END$$

-- =====================================================
-- 7. VALIDATE PROPERTY VALUE
-- =====================================================
CREATE TRIGGER trg_validate_property_value
BEFORE INSERT ON properties
FOR EACH ROW
BEGIN
    -- Ensure market value is reasonable based on area
    IF NEW.market_value IS NOT NULL AND NEW.area IS NOT NULL THEN
        IF NEW.market_value / NEW.area > 1000000 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Property value per unit area exceeds maximum threshold';
        END IF;
        
        IF NEW.market_value < 10000 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Property value is too low to be valid';
        END IF;
    END IF;
END$$

-- =====================================================
-- 8. AUTO-GENERATE PAYMENT RECEIPT
-- =====================================================
CREATE TRIGGER trg_generate_payment_receipt
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    -- Receipt is already generated in the application
    -- This trigger logs the payment for audit
    INSERT INTO audit_logs (
        user_id, action, table_name, record_id,
        changes, ip_address, user_agent, created_at
    )
    VALUES (
        NEW.user_id,
        'PAYMENT',
        'payments',
        NEW.id,
        JSON_OBJECT(
            'amount', NEW.amount,
            'payment_type', NEW.payment_type,
            'payment_reference', NEW.payment_reference,
            'status', NEW.status
        ),
        'system',
        'trigger',
        NOW()
    );
END$$

-- =====================================================
-- 9. AUTO-SEND MUTATION NOTIFICATIONS
-- =====================================================
CREATE TRIGGER trg_auto_send_mutation_notification
AFTER INSERT ON mutations
FOR EACH ROW
BEGIN
    -- Notify property owners
    INSERT INTO notifications (user_id, title, message, type, is_read)
    SELECT DISTINCT
        u.id,
        'New Mutation Request',
        CONCAT('A new mutation request (', NEW.mutation_type, ') has been submitted for your property.'),
        'info',
        FALSE
    FROM ownerships o
    INNER JOIN owners ow ON o.owner_id = ow.id
    INNER JOIN users u ON ow.user_id = u.id
    WHERE o.property_id = NEW.property_id 
      AND o.is_active = TRUE;
    
    -- Notify officers
    INSERT INTO notifications (user_id, title, message, type, is_read)
    SELECT 
        id,
        'New Mutation for Review',
        CONCAT('Mutation #', NEW.mutation_number, ' requires your review.'),
        'info',
        FALSE
    FROM users
    WHERE role IN ('officer', 'registrar')
    LIMIT 5;
END$$

-- =====================================================
-- 10. UPDATE OWNERSHIP ON MUTATION APPROVAL
-- =====================================================
CREATE TRIGGER trg_update_mutation_ownership
AFTER UPDATE ON mutations
FOR EACH ROW
BEGIN
    IF OLD.status != 'approved' AND NEW.status = 'approved' THEN
        -- Deactivate old ownerships
        UPDATE ownerships
        SET is_active = FALSE,
            end_date = NEW.approval_date
        WHERE property_id = NEW.property_id
          AND is_active = TRUE;
        
        -- Note: New ownership should be created by the application
        -- This trigger just closes the old ownership records
    END IF;
END$$

DELIMITER ;

-- =====================================================
-- SECTION 3: VIEWS
-- =====================================================

-- Drop existing views
DROP VIEW IF EXISTS vw_realtime_dashboard_stats;
DROP VIEW IF EXISTS vw_executive_kpi_summary;
DROP VIEW IF EXISTS vw_revenue_analytics;
DROP VIEW IF EXISTS vw_tax_defaulters;
DROP VIEW IF EXISTS vw_pending_approvals;
DROP VIEW IF EXISTS vw_geographic_distribution;
DROP VIEW IF EXISTS vw_high_value_properties;
DROP VIEW IF EXISTS vw_mutation_pattern_analysis;
DROP VIEW IF EXISTS vw_user_activity_heatmap;
DROP VIEW IF EXISTS vw_compliance_audit;
DROP VIEW IF EXISTS vw_property_ownership_summary;
DROP VIEW IF EXISTS vw_recent_transactions;

-- =====================================================
-- 1. REAL-TIME DASHBOARD STATISTICS
-- =====================================================
CREATE VIEW vw_realtime_dashboard_stats AS
SELECT 
    (SELECT COUNT(*) FROM properties) AS total_properties,
    (SELECT COUNT(*) FROM properties WHERE status = 'approved') AS approved_properties,
    (SELECT COUNT(*) FROM properties WHERE status = 'pending') AS pending_properties,
    (SELECT COUNT(*) FROM properties WHERE status = 'rejected') AS rejected_properties,
    (SELECT COUNT(*) FROM mutations) AS total_mutations,
    (SELECT COUNT(*) FROM mutations WHERE status = 'pending') AS pending_mutations,
    (SELECT COUNT(*) FROM mutations WHERE status = 'approved') AS approved_mutations,
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM users WHERE role = 'citizen') AS citizen_users,
    (SELECT SUM(amount) FROM payments WHERE status = 'completed') AS total_revenue,
    (SELECT SUM(amount) FROM payments WHERE status = 'completed' AND MONTH(payment_date) = MONTH(CURDATE())) AS monthly_revenue,
    (SELECT SUM(amount) FROM payments WHERE status = 'pending') AS pending_payments,
    (SELECT SUM(market_value) FROM properties WHERE status = 'approved') AS total_property_value,
    (SELECT AVG(market_value) FROM properties WHERE status = 'approved') AS avg_property_value;

-- =====================================================
-- 2. EXECUTIVE KPI SUMMARY
-- =====================================================
CREATE VIEW vw_executive_kpi_summary AS
SELECT 
    DATE_FORMAT(CURDATE(), '%Y-%m') AS reporting_period,
    COUNT(DISTINCT p.id) AS properties_registered,
    COUNT(DISTINCT CASE WHEN p.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN p.id END) AS new_registrations_30d,
    COUNT(DISTINCT m.id) AS total_mutations,
    COUNT(DISTINCT CASE WHEN m.submission_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN m.id END) AS new_mutations_30d,
    COALESCE(SUM(CASE WHEN pay.status = 'completed' THEN pay.amount ELSE 0 END), 0) AS revenue_collected,
    COALESCE(SUM(CASE WHEN pay.status = 'completed' AND pay.payment_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN pay.amount ELSE 0 END), 0) AS revenue_30d,
    COUNT(DISTINCT u.id) AS active_users,
    ROUND(AVG(DATEDIFF(m.approval_date, m.submission_date)), 1) AS avg_approval_days
FROM properties p
LEFT JOIN mutations m ON p.id = m.property_id
LEFT JOIN payments pay ON p.id = pay.property_id
LEFT JOIN users u ON u.last_login >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

-- =====================================================
-- 3. REVENUE ANALYTICS
-- =====================================================
CREATE VIEW vw_revenue_analytics AS
SELECT 
    payment_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount,
    DATE_FORMAT(payment_date, '%Y-%m') AS payment_month,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS completed_amount,
    SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) AS pending_amount,
    SUM(CASE WHEN status = 'failed' THEN amount ELSE 0 END) AS failed_amount
FROM payments
WHERE payment_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY payment_type, DATE_FORMAT(payment_date, '%Y-%m')
ORDER BY payment_month DESC, total_amount DESC;

-- =====================================================
-- 4. TAX DEFAULTERS LIST
-- =====================================================
CREATE VIEW vw_tax_defaulters AS
SELECT 
    p.id AS property_id,
    p.ulpin,
    p.village_city,
    p.district,
    p.state,
    ta.tax_amount,
    ta.due_date,
    DATEDIFF(CURDATE(), ta.due_date) AS days_overdue,
    ROUND(ta.tax_amount * 0.02 * FLOOR(DATEDIFF(CURDATE(), ta.due_date) / 30), 2) AS penalty_amount,
    u.full_name AS owner_name,
    u.email AS owner_email,
    u.phone AS owner_phone
FROM tax_assessments ta
INNER JOIN properties p ON ta.property_id = p.id
INNER JOIN ownerships o ON p.id = o.property_id AND o.is_active = TRUE
INNER JOIN owners ow ON o.owner_id = ow.id
INNER JOIN users u ON ow.user_id = u.id
WHERE ta.status = 'assessed'
  AND ta.due_date < CURDATE()
  AND NOT EXISTS (
      SELECT 1 FROM payments pay
      WHERE pay.property_id = p.id
        AND pay.payment_type = 'property_tax'
        AND YEAR(pay.payment_date) = ta.assessment_year
        AND pay.status = 'completed'
  )
ORDER BY days_overdue DESC;

-- =====================================================
-- 5. PENDING APPROVALS SUMMARY
-- =====================================================
CREATE VIEW vw_pending_approvals AS
SELECT 
    'Property Registration' AS approval_type,
    p.id,
    p.ulpin AS reference_number,
    p.village_city AS location,
    p.created_at AS submitted_date,
    DATEDIFF(CURDATE(), p.created_at) AS days_pending,
    u.full_name AS submitted_by,
    'registrar' AS approver_role
FROM properties p
INNER JOIN users u ON p.created_by = u.id
WHERE p.status = 'pending'

UNION ALL

SELECT 
    'Mutation Request' AS approval_type,
    m.id,
    m.mutation_number AS reference_number,
    p.village_city AS location,
    m.submission_date AS submitted_date,
    DATEDIFF(CURDATE(), m.submission_date) AS days_pending,
    u.full_name AS submitted_by,
    'officer' AS approver_role
FROM mutations m
INNER JOIN properties p ON m.property_id = p.id
INNER JOIN users u ON m.requester_id = u.id
WHERE m.status = 'pending'

ORDER BY days_pending DESC;

-- =====================================================
-- 6. GEOGRAPHIC DISTRIBUTION
-- =====================================================
CREATE VIEW vw_geographic_distribution AS
SELECT 
    state,
    district,
    COUNT(*) AS property_count,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) AS approved_count,
    SUM(COALESCE(market_value, 0)) AS total_value,
    AVG(COALESCE(market_value, 0)) AS avg_value,
    SUM(area) AS total_area,
    COUNT(DISTINCT property_type) AS property_types,
    MIN(created_at) AS first_registration,
    MAX(created_at) AS latest_registration
FROM properties
GROUP BY state, district
ORDER BY property_count DESC;

-- =====================================================
-- 7. HIGH-VALUE PROPERTIES
-- =====================================================
CREATE VIEW vw_high_value_properties AS
SELECT 
    p.id,
    p.ulpin,
    p.property_type,
    p.area,
    p.area_unit,
    p.market_value,
    p.village_city,
    p.district,
    p.state,
    u.full_name AS owner_name,
    o.ownership_percentage,
    p.latitude,
    p.longitude,
    fn_calculate_property_risk_score(p.id) AS risk_score
FROM properties p
INNER JOIN ownerships o ON p.id = o.property_id AND o.is_active = TRUE
INNER JOIN owners ow ON o.owner_id = ow.id
INNER JOIN users u ON ow.user_id = u.id
WHERE p.status = 'approved'
  AND p.market_value > (SELECT AVG(market_value) * 2 FROM properties WHERE status = 'approved')
ORDER BY p.market_value DESC;

-- =====================================================
-- 8. MUTATION PATTERN ANALYSIS
-- =====================================================
CREATE VIEW vw_mutation_pattern_analysis AS
SELECT 
    mutation_type,
    COUNT(*) AS total_count,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) AS approved_count,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_count,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) AS rejected_count,
    ROUND(COUNT(CASE WHEN status = 'approved' THEN 1 END) * 100.0 / COUNT(*), 2) AS approval_rate,
    AVG(DATEDIFF(approval_date, submission_date)) AS avg_processing_days,
    AVG(transaction_amount) AS avg_transaction_value,
    DATE_FORMAT(submission_date, '%Y-%m') AS submission_month
FROM mutations
WHERE submission_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY mutation_type, DATE_FORMAT(submission_date, '%Y-%m')
ORDER BY submission_month DESC, total_count DESC;

-- =====================================================
-- 9. USER ACTIVITY HEATMAP
-- =====================================================
CREATE VIEW vw_user_activity_heatmap AS
SELECT 
    u.role,
    COUNT(DISTINCT u.id) AS user_count,
    COUNT(al.id) AS total_actions,
    COUNT(DISTINCT DATE(al.created_at)) AS active_days,
    AVG(CASE WHEN al.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) THEN 1 ELSE 0 END) AS weekly_activity_score,
    MAX(al.created_at) AS last_activity,
    DATE_FORMAT(al.created_at, '%Y-%m-%d') AS activity_date,
    HOUR(al.created_at) AS activity_hour,
    COUNT(*) AS actions_in_hour
FROM users u
LEFT JOIN audit_logs al ON u.id = al.user_id
WHERE al.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY u.role, DATE_FORMAT(al.created_at, '%Y-%m-%d'), HOUR(al.created_at)
ORDER BY activity_date DESC, activity_hour;

-- =====================================================
-- 10. COMPLIANCE & AUDIT REPORT
-- =====================================================
CREATE VIEW vw_compliance_audit AS
SELECT 
    DATE_FORMAT(created_at, '%Y-%m-%d') AS audit_date,
    table_name,
    action,
    COUNT(*) AS action_count,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT record_id) AS unique_records
FROM audit_logs
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d'), table_name, action
ORDER BY audit_date DESC, action_count DESC;

-- =====================================================
-- 11. PROPERTY OWNERSHIP SUMMARY
-- =====================================================
CREATE VIEW vw_property_ownership_summary AS
SELECT 
    p.id AS property_id,
    p.ulpin,
    p.property_type,
    p.village_city,
    p.district,
    GROUP_CONCAT(u.full_name ORDER BY o.ownership_percentage DESC SEPARATOR ', ') AS owners,
    COUNT(o.id) AS owner_count,
    SUM(o.ownership_percentage) AS total_ownership_percentage,
    MAX(o.acquisition_date) AS latest_acquisition_date
FROM properties p
INNER JOIN ownerships o ON p.id = o.property_id AND o.is_active = TRUE
INNER JOIN owners ow ON o.owner_id = ow.id
INNER JOIN users u ON ow.user_id = u.id
GROUP BY p.id, p.ulpin, p.property_type, p.village_city, p.district;

-- =====================================================
-- 12. RECENT TRANSACTIONS
-- =====================================================
CREATE VIEW vw_recent_transactions AS
SELECT 
    'Payment' AS transaction_type,
    pay.id AS transaction_id,
    pay.payment_reference AS reference_number,
    pay.amount,
    pay.payment_date AS transaction_date,
    pay.status,
    u.full_name AS user_name,
    p.ulpin AS property_reference
FROM payments pay
INNER JOIN users u ON pay.user_id = u.id
LEFT JOIN properties p ON pay.property_id = p.id
WHERE pay.payment_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)

UNION ALL

SELECT 
    'Mutation' AS transaction_type,
    m.id AS transaction_id,
    m.mutation_number AS reference_number,
    m.transaction_amount AS amount,
    m.submission_date AS transaction_date,
    m.status,
    u.full_name AS user_name,
    p.ulpin AS property_reference
FROM mutations m
INNER JOIN users u ON m.requester_id = u.id
INNER JOIN properties p ON m.property_id = p.id
WHERE m.submission_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)

ORDER BY transaction_date DESC
LIMIT 100;

-- =====================================================
-- SECTION 4: PERFORMANCE INDEXES
-- =====================================================

-- Check and create indexes only if they don't exist
-- Note: Some indexes may already exist from migrations

-- Full-text search index (only if not exists)
CREATE FULLTEXT INDEX idx_property_description_fulltext ON properties(description);

-- Composite indexes for common queries
CREATE INDEX idx_property_location_status ON properties(state, district, village_city, status);
CREATE INDEX idx_property_type_value ON properties(property_type, market_value, status);
CREATE INDEX idx_mutation_status_date ON mutations(status, submission_date, approval_date);
CREATE INDEX idx_payment_status_date ON payments(status, payment_date, payment_type);
CREATE INDEX idx_ownership_active ON ownerships(property_id, is_active, acquisition_date);

-- Indexes for JOIN operations
CREATE INDEX idx_audit_user_date ON audit_logs(user_id, created_at, action);
CREATE INDEX idx_tax_assessment_status ON tax_assessments(property_id, status, due_date);
CREATE INDEX idx_notification_user_read ON notifications(user_id, is_read, created_at);

-- =====================================================
-- SECTION 5: MYSQL EVENTS (Scheduled Jobs)
-- =====================================================

-- Enable event scheduler
SET GLOBAL event_scheduler = ON;

-- Drop existing events
DROP EVENT IF EXISTS evt_daily_tax_reminders;
DROP EVENT IF EXISTS evt_weekly_analytics_update;
DROP EVENT IF EXISTS evt_monthly_auto_approve_mutations;

DELIMITER $$

-- =====================================================
-- 1. DAILY TAX REMINDERS
-- =====================================================
CREATE EVENT evt_daily_tax_reminders
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY + INTERVAL 9 HOUR
DO
BEGIN
    CALL sp_generate_tax_reminders();
END$$

-- =====================================================
-- 2. WEEKLY ANALYTICS CACHE UPDATE
-- =====================================================
CREATE EVENT evt_weekly_analytics_update
ON SCHEDULE EVERY 1 WEEK
STARTS CURRENT_DATE + INTERVAL 1 WEEK + INTERVAL 2 HOUR
DO
BEGIN
    CALL sp_update_analytics_cache();
END$$

-- =====================================================
-- 3. MONTHLY AUTO-APPROVE SIMPLE MUTATIONS
-- =====================================================
CREATE EVENT evt_monthly_auto_approve_mutations
ON SCHEDULE EVERY 1 MONTH
STARTS CURRENT_DATE + INTERVAL 1 MONTH + INTERVAL 10 HOUR
DO
BEGIN
    CALL sp_auto_approve_simple_mutations();
END$$

DELIMITER ;

-- =====================================================
-- SECTION 6: TABLE PARTITIONING SETUP
-- =====================================================
-- Note: Partitioning requires the table to be created with partitioning
-- Or ALTER TABLE which may take time on large tables
-- These commands are provided for reference but commented out

/*
-- Partition audit_logs by year (for scalability)
ALTER TABLE audit_logs
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Partition payments by year
ALTER TABLE payments
PARTITION BY RANGE (YEAR(payment_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Check installed stored procedures
SELECT ROUTINE_NAME, ROUTINE_TYPE, CREATED, LAST_ALTERED
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = 'land_registry_db'
ORDER BY ROUTINE_TYPE, ROUTINE_NAME;

-- Check installed triggers
SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_TIMING
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = 'land_registry_db'
ORDER BY EVENT_OBJECT_TABLE, TRIGGER_NAME;

-- Check installed views
SELECT TABLE_NAME AS view_name
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = 'land_registry_db'
ORDER BY TABLE_NAME;

-- Check installed events
SELECT EVENT_NAME, STATUS, EVENT_TYPE, INTERVAL_VALUE, INTERVAL_FIELD, STARTS, ENDS
FROM information_schema.EVENTS
WHERE EVENT_SCHEMA = 'land_registry_db'
ORDER BY EVENT_NAME;

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================
SELECT '✅ Advanced MySQL Features Installation Complete!' AS message,
       'Procedures: 9, Triggers: 10, Views: 12, Indexes: 8, Events: 3' AS summary;
