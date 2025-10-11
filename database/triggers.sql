ru-- MySQL Triggers for Automatic Audit Logging
-- Government Property Management Portal

USE property_portal;

-- Drop existing triggers if they exist
DROP TRIGGER IF EXISTS owner_audit_insert;
DROP TRIGGER IF EXISTS owner_audit_update;
DROP TRIGGER IF EXISTS owner_audit_delete;
DROP TRIGGER IF EXISTS parcel_audit_insert;
DROP TRIGGER IF EXISTS parcel_audit_update;
DROP TRIGGER IF EXISTS parcel_audit_delete;
DROP TRIGGER IF EXISTS ownership_audit_insert;
DROP TRIGGER IF EXISTS ownership_audit_update;
DROP TRIGGER IF EXISTS ownership_audit_delete;
DROP TRIGGER IF EXISTS mutation_audit_insert;
DROP TRIGGER IF EXISTS mutation_audit_update;
DROP TRIGGER IF EXISTS mutation_audit_delete;
DROP TRIGGER IF EXISTS tax_assessment_audit_insert;
DROP TRIGGER IF EXISTS tax_assessment_audit_update;
DROP TRIGGER IF EXISTS tax_assessment_audit_delete;

-- OWNER TABLE TRIGGERS
DELIMITER $$

CREATE TRIGGER owner_audit_insert
AFTER INSERT ON owner
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, new_values)
    VALUES (
        'owner',
        NEW.owner_id,
        'INSERT',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'owner_id', NEW.owner_id,
            'name', NEW.name,
            'owner_type', NEW.owner_type,
            'aadhaar_encrypted', NEW.aadhaar_encrypted,
            'pan', NEW.pan,
            'address', NEW.address,
            'contact_no', NEW.contact_no,
            'created_at', NEW.created_at
        )
    );
END$$

CREATE TRIGGER owner_audit_update
AFTER UPDATE ON owner
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values, new_values)
    VALUES (
        'owner',
        NEW.owner_id,
        'UPDATE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'owner_id', OLD.owner_id,
            'name', OLD.name,
            'owner_type', OLD.owner_type,
            'aadhaar_encrypted', OLD.aadhaar_encrypted,
            'pan', OLD.pan,
            'address', OLD.address,
            'contact_no', OLD.contact_no,
            'created_at', OLD.created_at
        ),
        JSON_OBJECT(
            'owner_id', NEW.owner_id,
            'name', NEW.name,
            'owner_type', NEW.owner_type,
            'aadhaar_encrypted', NEW.aadhaar_encrypted,
            'pan', NEW.pan,
            'address', NEW.address,
            'contact_no', NEW.contact_no,
            'created_at', NEW.created_at
        )
    );
END$$

CREATE TRIGGER owner_audit_delete
AFTER DELETE ON owner
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values)
    VALUES (
        'owner',
        OLD.owner_id,
        'DELETE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'owner_id', OLD.owner_id,
            'name', OLD.name,
            'owner_type', OLD.owner_type,
            'aadhaar_encrypted', OLD.aadhaar_encrypted,
            'pan', OLD.pan,
            'address', OLD.address,
            'contact_no', OLD.contact_no,
            'created_at', OLD.created_at
        )
    );
END$$

-- PARCEL TABLE TRIGGERS
CREATE TRIGGER parcel_audit_insert
AFTER INSERT ON parcel
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, new_values)
    VALUES (
        'parcel',
        NEW.parcel_id,
        'INSERT',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'parcel_id', NEW.parcel_id,
            'ulpin', NEW.ulpin,
            'survey_no', NEW.survey_no,
            'total_area', NEW.total_area,
            'land_category', NEW.land_category,
            'current_use_type', NEW.current_use_type,
            'location_id', NEW.location_id,
            'centroid_lat', NEW.centroid_lat,
            'centroid_lon', NEW.centroid_lon,
            'created_at', NEW.created_at
        )
    );
END$$

CREATE TRIGGER parcel_audit_update
AFTER UPDATE ON parcel
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values, new_values)
    VALUES (
        'parcel',
        NEW.parcel_id,
        'UPDATE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'parcel_id', OLD.parcel_id,
            'ulpin', OLD.ulpin,
            'survey_no', OLD.survey_no,
            'total_area', OLD.total_area,
            'land_category', OLD.land_category,
            'current_use_type', OLD.current_use_type,
            'location_id', OLD.location_id,
            'centroid_lat', OLD.centroid_lat,
            'centroid_lon', OLD.centroid_lon
        ),
        JSON_OBJECT(
            'parcel_id', NEW.parcel_id,
            'ulpin', NEW.ulpin,
            'survey_no', NEW.survey_no,
            'total_area', NEW.total_area,
            'land_category', NEW.land_category,
            'current_use_type', NEW.current_use_type,
            'location_id', NEW.location_id,
            'centroid_lat', NEW.centroid_lat,
            'centroid_lon', NEW.centroid_lon
        )
    );
END$$

CREATE TRIGGER parcel_audit_delete
AFTER DELETE ON parcel
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values)
    VALUES (
        'parcel',
        OLD.parcel_id,
        'DELETE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'parcel_id', OLD.parcel_id,
            'ulpin', OLD.ulpin,
            'survey_no', OLD.survey_no,
            'total_area', OLD.total_area,
            'land_category', OLD.land_category,
            'current_use_type', OLD.current_use_type,
            'location_id', OLD.location_id,
            'centroid_lat', OLD.centroid_lat,
            'centroid_lon', OLD.centroid_lon
        )
    );
END$$

-- OWNERSHIP TABLE TRIGGERS
CREATE TRIGGER ownership_audit_insert
AFTER INSERT ON ownership
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, new_values)
    VALUES (
        'ownership',
        NEW.ownership_id,
        'INSERT',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'ownership_id', NEW.ownership_id,
            'parcel_id', NEW.parcel_id,
            'owner_id', NEW.owner_id,
            'share_fraction', NEW.share_fraction,
            'ownership_type', NEW.ownership_type,
            'date_from', NEW.date_from,
            'date_to', NEW.date_to,
            'created_at', NEW.created_at
        )
    );
END$$

CREATE TRIGGER ownership_audit_update
AFTER UPDATE ON ownership
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values, new_values)
    VALUES (
        'ownership',
        NEW.ownership_id,
        'UPDATE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'ownership_id', OLD.ownership_id,
            'parcel_id', OLD.parcel_id,
            'owner_id', OLD.owner_id,
            'share_fraction', OLD.share_fraction,
            'ownership_type', OLD.ownership_type,
            'date_from', OLD.date_from,
            'date_to', OLD.date_to
        ),
        JSON_OBJECT(
            'ownership_id', NEW.ownership_id,
            'parcel_id', NEW.parcel_id,
            'owner_id', NEW.owner_id,
            'share_fraction', NEW.share_fraction,
            'ownership_type', NEW.ownership_type,
            'date_from', NEW.date_from,
            'date_to', NEW.date_to
        )
    );
END$$

CREATE TRIGGER ownership_audit_delete
AFTER DELETE ON ownership
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values)
    VALUES (
        'ownership',
        OLD.ownership_id,
        'DELETE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'ownership_id', OLD.ownership_id,
            'parcel_id', OLD.parcel_id,
            'owner_id', OLD.owner_id,
            'share_fraction', OLD.share_fraction,
            'ownership_type', OLD.ownership_type,
            'date_from', OLD.date_from,
            'date_to', OLD.date_to
        )
    );
END$$

-- MUTATION TABLE TRIGGERS
CREATE TRIGGER mutation_audit_insert
AFTER INSERT ON mutation
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, new_values)
    VALUES (
        'mutation',
        NEW.mutation_id,
        'INSERT',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'mutation_id', NEW.mutation_id,
            'parcel_id', NEW.parcel_id,
            'from_owner_id', NEW.from_owner_id,
            'to_owner_id', NEW.to_owner_id,
            'mutation_type', NEW.mutation_type,
            'date_of_mutation', NEW.date_of_mutation,
            'consideration_value', NEW.consideration_value,
            'status', NEW.status,
            'created_at', NEW.created_at
        )
    );
END$$

CREATE TRIGGER mutation_audit_update
AFTER UPDATE ON mutation
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values, new_values)
    VALUES (
        'mutation',
        NEW.mutation_id,
        'UPDATE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'mutation_id', OLD.mutation_id,
            'parcel_id', OLD.parcel_id,
            'from_owner_id', OLD.from_owner_id,
            'to_owner_id', OLD.to_owner_id,
            'mutation_type', OLD.mutation_type,
            'date_of_mutation', OLD.date_of_mutation,
            'consideration_value', OLD.consideration_value,
            'approved_by', OLD.approved_by,
            'approved_on', OLD.approved_on,
            'status', OLD.status
        ),
        JSON_OBJECT(
            'mutation_id', NEW.mutation_id,
            'parcel_id', NEW.parcel_id,
            'from_owner_id', NEW.from_owner_id,
            'to_owner_id', NEW.to_owner_id,
            'mutation_type', NEW.mutation_type,
            'date_of_mutation', NEW.date_of_mutation,
            'consideration_value', NEW.consideration_value,
            'approved_by', NEW.approved_by,
            'approved_on', NEW.approved_on,
            'status', NEW.status
        )
    );
END$$

CREATE TRIGGER mutation_audit_delete
AFTER DELETE ON mutation
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values)
    VALUES (
        'mutation',
        OLD.mutation_id,
        'DELETE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'mutation_id', OLD.mutation_id,
            'parcel_id', OLD.parcel_id,
            'from_owner_id', OLD.from_owner_id,
            'to_owner_id', OLD.to_owner_id,
            'mutation_type', OLD.mutation_type,
            'date_of_mutation', OLD.date_of_mutation,
            'consideration_value', OLD.consideration_value,
            'approved_by', OLD.approved_by,
            'approved_on', OLD.approved_on,
            'status', OLD.status
        )
    );
END$$

-- TAX ASSESSMENT TABLE TRIGGERS
CREATE TRIGGER tax_assessment_audit_insert
AFTER INSERT ON tax_assessment
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, new_values)
    VALUES (
        'tax_assessment',
        NEW.tax_id,
        'INSERT',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'tax_id', NEW.tax_id,
            'parcel_id', NEW.parcel_id,
            'assessment_year', NEW.assessment_year,
            'land_value', NEW.land_value,
            'building_value', NEW.building_value,
            'total_assessed_value', NEW.total_assessed_value,
            'tax_due', NEW.tax_due,
            'amount_paid', NEW.amount_paid,
            'paid_on', NEW.paid_on,
            'status', NEW.status,
            'created_at', NEW.created_at
        )
    );
END$$

CREATE TRIGGER tax_assessment_audit_update
AFTER UPDATE ON tax_assessment
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values, new_values)
    VALUES (
        'tax_assessment',
        NEW.tax_id,
        'UPDATE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'tax_id', OLD.tax_id,
            'parcel_id', OLD.parcel_id,
            'assessment_year', OLD.assessment_year,
            'land_value', OLD.land_value,
            'building_value', OLD.building_value,
            'total_assessed_value', OLD.total_assessed_value,
            'tax_due', OLD.tax_due,
            'amount_paid', OLD.amount_paid,
            'paid_on', OLD.paid_on,
            'status', OLD.status
        ),
        JSON_OBJECT(
            'tax_id', NEW.tax_id,
            'parcel_id', NEW.parcel_id,
            'assessment_year', NEW.assessment_year,
            'land_value', NEW.land_value,
            'building_value', NEW.building_value,
            'total_assessed_value', NEW.total_assessed_value,
            'tax_due', NEW.tax_due,
            'amount_paid', NEW.amount_paid,
            'paid_on', NEW.paid_on,
            'status', NEW.status
        )
    );
END$$

CREATE TRIGGER tax_assessment_audit_delete
AFTER DELETE ON tax_assessment
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_pk_value, action, user_id, timestamp, old_values)
    VALUES (
        'tax_assessment',
        OLD.tax_id,
        'DELETE',
        @current_user_id,
        NOW(),
        JSON_OBJECT(
            'tax_id', OLD.tax_id,
            'parcel_id', OLD.parcel_id,
            'assessment_year', OLD.assessment_year,
            'land_value', OLD.land_value,
            'building_value', OLD.building_value,
            'total_assessed_value', OLD.total_assessed_value,
            'tax_due', OLD.tax_due,
            'amount_paid', OLD.amount_paid,
            'paid_on', OLD.paid_on,
            'status', OLD.status
        )
    );
END$$

DELIMITER ;

-- Procedure to set current user for audit logging
DELIMITER $$
CREATE PROCEDURE SetCurrentUser(IN user_id INT)
BEGIN
    SET @current_user_id = user_id;
END$$
DELIMITER ;

-- Function to get audit trail for a specific record
DELIMITER $$
CREATE FUNCTION GetAuditTrail(table_name VARCHAR(100), record_pk VARCHAR(100))
RETURNS JSON
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE audit_data JSON;
    
    SELECT JSON_ARRAYAGG(
        JSON_OBJECT(
            'audit_id', audit_id,
            'action', action,
            'timestamp', timestamp,
            'user_id', user_id,
            'old_values', old_values,
            'new_values', new_values
        )
    ) INTO audit_data
    FROM audit_log
    WHERE audit_log.table_name = table_name 
    AND audit_log.record_pk_value = record_pk
    ORDER BY timestamp DESC;
    
    RETURN COALESCE(audit_data, JSON_ARRAY());
END$$
DELIMITER ;


