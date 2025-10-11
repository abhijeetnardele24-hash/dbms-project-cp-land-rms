-- Government Property Management Portal Database Schema
-- MySQL Database Schema for Land Records Management System

-- Create database
CREATE DATABASE IF NOT EXISTS property_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE property_portal;

-- 1. User Account Table
CREATE TABLE user_account (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Registrar', 'Approver', 'Admin') NOT NULL,
    last_login DATETIME NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- 2. Location Table
CREATE TABLE location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    village VARCHAR(100) NOT NULL,
    taluka VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_district (district),
    INDEX idx_state (state),
    INDEX idx_pincode (pincode)
);

-- 3. Owner Table
CREATE TABLE owner (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_type ENUM('Individual', 'Company', 'Government') NOT NULL,
    aadhaar_encrypted VARCHAR(500) NULL,
    pan VARCHAR(10) NULL,
    address TEXT NULL,
    contact_no VARCHAR(15) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_owner_type (owner_type),
    INDEX idx_pan (pan)
);

-- 4. Document Table
CREATE TABLE document (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    doc_type ENUM('Sale Deed', 'Lease Deed', 'Mutation Record', 'Encumbrance', 'Tax Receipt') NOT NULL,
    file_name VARCHAR(255) NULL,
    file_path VARCHAR(500) NULL,
    registered_at DATETIME NULL,
    registration_office VARCHAR(255) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_doc_type (doc_type),
    INDEX idx_registered_at (registered_at)
);

-- 5. Parcel Table
CREATE TABLE parcel (
    parcel_id INT AUTO_INCREMENT PRIMARY KEY,
    ulpin VARCHAR(50) UNIQUE NOT NULL,
    survey_no VARCHAR(50) NOT NULL,
    total_area DECIMAL(10, 4) NOT NULL,
    land_category ENUM('Agricultural', 'Residential', 'Commercial', 'Industrial', 'State Owned') NOT NULL,
    current_use_type VARCHAR(100) NULL,
    location_id INT NOT NULL,
    centroid_lat DECIMAL(10, 8) NULL,
    centroid_lon DECIMAL(11, 8) NULL,
    current_version_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE RESTRICT,
    INDEX idx_ulpin (ulpin),
    INDEX idx_survey_no (survey_no),
    INDEX idx_land_category (land_category),
    INDEX idx_location (location_id)
);

-- 6. Parcel Version Table
CREATE TABLE parcel_version (
    version_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    valid_from DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_to DATETIME NULL,
    boundary_geometry TEXT NULL,
    area_at_version DECIMAL(10, 4) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id) ON DELETE CASCADE,
    INDEX idx_parcel_id (parcel_id),
    INDEX idx_valid_from (valid_from)
);

-- 7. Ownership Table
CREATE TABLE ownership (
    ownership_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    owner_id INT NOT NULL,
    share_fraction DECIMAL(5, 4) NOT NULL,
    ownership_type ENUM('Freehold', 'Leasehold', 'Joint', 'Inherited') NOT NULL,
    date_from DATE NOT NULL,
    date_to DATE NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id) ON DELETE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES owner(owner_id) ON DELETE RESTRICT,
    INDEX idx_parcel_owner (parcel_id, owner_id),
    INDEX idx_date_from (date_from),
    INDEX idx_ownership_type (ownership_type)
);

-- 8. Mutation Table
CREATE TABLE mutation (
    mutation_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    from_owner_id INT NOT NULL,
    to_owner_id INT NOT NULL,
    mutation_type ENUM('Sale', 'Gift', 'Inheritance', 'Lease Transfer', 'Government Acquisition') NOT NULL,
    date_of_mutation DATE NOT NULL,
    consideration_value DECIMAL(15, 2) NULL,
    approved_by INT NULL,
    approved_on DATE NULL,
    status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
    document_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id) ON DELETE RESTRICT,
    FOREIGN KEY (from_owner_id) REFERENCES owner(owner_id) ON DELETE RESTRICT,
    FOREIGN KEY (to_owner_id) REFERENCES owner(owner_id) ON DELETE RESTRICT,
    FOREIGN KEY (approved_by) REFERENCES user_account(user_id) ON DELETE SET NULL,
    FOREIGN KEY (document_id) REFERENCES document(document_id) ON DELETE SET NULL,
    INDEX idx_parcel_id (parcel_id),
    INDEX idx_status (status),
    INDEX idx_mutation_type (mutation_type),
    INDEX idx_date_of_mutation (date_of_mutation)
);

-- 9. Tenant Agreement Table
CREATE TABLE tenant_agreement (
    agreement_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    owner_id INT NOT NULL,
    tenant_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    rent_amount DECIMAL(12, 2) NULL,
    phone_number VARCHAR(15) NULL,
    tenant_name VARCHAR(255) NULL,
    deposit_amount DECIMAL(12, 2) NULL,
    document_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id) ON DELETE RESTRICT,
    FOREIGN KEY (owner_id) REFERENCES owner(owner_id) ON DELETE RESTRICT,
    FOREIGN KEY (tenant_id) REFERENCES owner(owner_id) ON DELETE RESTRICT,
    FOREIGN KEY (document_id) REFERENCES document(document_id) ON DELETE SET NULL,
    INDEX idx_parcel_id (parcel_id),
    INDEX idx_owner_tenant (owner_id, tenant_id),
    INDEX idx_start_date (start_date)
);

-- 10. Encumbrance Table
CREATE TABLE encumbrance (
    encumbrance_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    type ENUM('Mortgage', 'Lien', 'Court Case', 'Dispute', 'Tax Dues') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    related_party_id INT NULL,
    case_number VARCHAR(100) NULL,
    status ENUM('Active', 'Resolved') NOT NULL DEFAULT 'Active',
    document_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id) ON DELETE RESTRICT,
    FOREIGN KEY (related_party_id) REFERENCES owner(owner_id) ON DELETE SET NULL,
    FOREIGN KEY (document_id) REFERENCES document(document_id) ON DELETE SET NULL,
    INDEX idx_parcel_id (parcel_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_case_number (case_number)
);

-- 11. Tax Assessment Table
CREATE TABLE tax_assessment (
    tax_id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT NOT NULL,
    assessment_year INT NOT NULL,
    land_value DECIMAL(15, 2) NULL,
    building_value DECIMAL(15, 2) NULL,
    total_assessed_value DECIMAL(15, 2) NOT NULL,
    tax_due DECIMAL(12, 2) NOT NULL,
    amount_paid DECIMAL(12, 2) DEFAULT 0,
    paid_on DATE NULL,
    status ENUM('Paid', 'Unpaid', 'Partial') NOT NULL DEFAULT 'Unpaid',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id) ON DELETE RESTRICT,
    INDEX idx_parcel_id (parcel_id),
    INDEX idx_assessment_year (assessment_year),
    INDEX idx_status (status),
    UNIQUE KEY unique_parcel_year (parcel_id, assessment_year)
);

-- 12. Audit Log Table
CREATE TABLE audit_log (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_pk_value VARCHAR(100) NOT NULL,
    action ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    user_id INT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    old_values JSON NULL,
    new_values JSON NULL,
    FOREIGN KEY (user_id) REFERENCES user_account(user_id) ON DELETE SET NULL,
    INDEX idx_table_name (table_name),
    INDEX idx_action (action),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id)
);

-- Add foreign key constraint for current_version_id after parcel_version table is created
ALTER TABLE parcel ADD CONSTRAINT fk_parcel_current_version 
    FOREIGN KEY (current_version_id) REFERENCES parcel_version(version_id) ON DELETE SET NULL;

-- Insert default admin user
INSERT INTO user_account (username, password_hash, role, is_active) VALUES 
('admin', 'scrypt:32768:8:1$YourHashHere$hash', 'Admin', TRUE);

-- Create indexes for better performance
CREATE INDEX idx_audit_log_composite ON audit_log(table_name, record_pk_value, timestamp);
CREATE INDEX idx_ownership_active ON ownership(parcel_id, date_to);
CREATE INDEX idx_mutation_pending ON mutation(status, created_at);
CREATE INDEX idx_tax_unpaid ON tax_assessment(status, assessment_year);

-- Views for common queries
CREATE VIEW active_ownerships AS
SELECT o.*, p.ulpin, p.survey_no, own.name as owner_name
FROM ownership o
JOIN parcel p ON o.parcel_id = p.parcel_id
JOIN owner own ON o.owner_id = own.owner_id
WHERE o.date_to IS NULL;

CREATE VIEW pending_mutations AS
SELECT m.*, p.ulpin, p.survey_no, 
       from_own.name as from_owner_name,
       to_own.name as to_owner_name
FROM mutation m
JOIN parcel p ON m.parcel_id = p.parcel_id
JOIN owner from_own ON m.from_owner_id = from_own.owner_id
JOIN owner to_own ON m.to_owner_id = to_own.owner_id
WHERE m.status = 'Pending';

CREATE VIEW tax_summary AS
SELECT 
    assessment_year,
    COUNT(*) as total_assessments,
    SUM(tax_due) as total_tax_due,
    SUM(amount_paid) as total_collected,
    SUM(CASE WHEN status = 'Paid' THEN 1 ELSE 0 END) as paid_count,
    SUM(CASE WHEN status = 'Unpaid' THEN 1 ELSE 0 END) as unpaid_count,
    SUM(CASE WHEN status = 'Partial' THEN 1 ELSE 0 END) as partial_count
FROM tax_assessment
GROUP BY assessment_year
ORDER BY assessment_year DESC;
