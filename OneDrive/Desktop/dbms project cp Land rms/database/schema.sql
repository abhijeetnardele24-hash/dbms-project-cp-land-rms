-- =====================================================
-- LAND REGISTRY MANAGEMENT SYSTEM - DATABASE SCHEMA
-- =====================================================
-- DBMS: MySQL 8.0+
-- Description: Complete database schema for Land Registry Management System
-- Features: Property registration, ownership tracking, mutation requests,
--          tax management, audit logging, and comprehensive reporting
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS land_registry_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE land_registry_db;

-- =====================================================
-- TABLE: users
-- Description: User accounts with role-based access control
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    role ENUM('admin', 'registrar', 'officer', 'citizen') NOT NULL DEFAULT 'citizen',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: land_categories
-- Description: Master data for land classification
-- =====================================================
CREATE TABLE IF NOT EXISTS land_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: usage_types
-- Description: Property usage classifications
-- =====================================================
CREATE TABLE IF NOT EXISTS usage_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usage_type VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: document_types
-- Description: Types of documents in the system
-- =====================================================
CREATE TABLE IF NOT EXISTS document_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_type VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_mandatory BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: properties
-- Description: Land parcel/property records
-- =====================================================
CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ulpin VARCHAR(50) UNIQUE COMMENT 'Unique Land Parcel Identification Number',
    property_type ENUM('Residential', 'Commercial', 'Agricultural', 'Industrial', 'Mixed') NOT NULL,
    area DECIMAL(10, 2) NOT NULL,
    area_unit VARCHAR(20) DEFAULT 'sq_meters',
    market_value DECIMAL(15, 2),
    survey_number VARCHAR(100),
    plot_number VARCHAR(100),
    khata_number VARCHAR(100),
    
    -- Location details
    village_city VARCHAR(255),
    taluk_block VARCHAR(255),
    district VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    pincode VARCHAR(10),
    
    -- Geographic coordinates
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Property details
    land_category_id INT,
    usage_type_id INT,
    boundaries TEXT COMMENT 'JSON: {north, south, east, west}',
    
    -- Status and approval
    status ENUM('draft', 'pending', 'approved', 'rejected', 'under_review') DEFAULT 'pending',
    approved_by INT,
    approval_date TIMESTAMP NULL,
    rejection_reason TEXT,
    
    -- Timestamps
    registered_date TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (land_category_id) REFERENCES land_categories(id) ON DELETE SET NULL,
    FOREIGN KEY (usage_type_id) REFERENCES usage_types(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_ulpin (ulpin),
    INDEX idx_status (status),
    INDEX idx_district (district),
    INDEX idx_property_type (property_type),
    INDEX idx_location (district, village_city),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: owners
-- Description: Property owner information
-- =====================================================
CREATE TABLE IF NOT EXISTS owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    full_name VARCHAR(255) NOT NULL,
    father_name VARCHAR(255),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
    
    -- Identity documents
    aadhar_number VARCHAR(12) UNIQUE,
    pan_number VARCHAR(10) UNIQUE,
    
    -- Contact information
    phone_number VARCHAR(20),
    email VARCHAR(255),
    
    -- Address
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_aadhar (aadhar_number),
    INDEX idx_pan (pan_number),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: ownerships
-- Description: Property-Owner relationship (supports joint ownership)
-- =====================================================
CREATE TABLE IF NOT EXISTS ownerships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    owner_id INT NOT NULL,
    ownership_percentage DECIMAL(5, 2) DEFAULT 100.00,
    ownership_type ENUM('sole', 'joint', 'partial') DEFAULT 'sole',
    acquisition_date DATE,
    acquisition_mode ENUM('purchase', 'inheritance', 'gift', 'transfer', 'other') DEFAULT 'purchase',
    
    -- Status
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES owners(id) ON DELETE CASCADE,
    
    INDEX idx_property_id (property_id),
    INDEX idx_owner_id (owner_id),
    INDEX idx_is_current (is_current)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: mutations
-- Description: Ownership change/mutation requests
-- =====================================================
CREATE TABLE IF NOT EXISTS mutations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_number VARCHAR(50) UNIQUE,
    property_id INT NOT NULL,
    
    -- Mutation details
    mutation_type ENUM('sale', 'inheritance', 'gift', 'partition', 'court_order', 'other') NOT NULL,
    mutation_reason TEXT,
    
    -- Previous and new owners
    previous_owner_id INT,
    new_owner_id INT NOT NULL,
    transfer_percentage DECIMAL(5, 2) DEFAULT 100.00,
    
    -- Application details
    requester_id INT NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Status and workflow
    status ENUM('pending', 'under_review', 'approved', 'rejected', 'completed') DEFAULT 'pending',
    reviewed_by INT,
    review_date TIMESTAMP NULL,
    review_notes TEXT,
    
    -- Fees
    application_fee DECIMAL(10, 2),
    stamp_duty DECIMAL(12, 2),
    registration_fee DECIMAL(10, 2),
    total_fees DECIMAL(12, 2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (previous_owner_id) REFERENCES owners(id) ON DELETE SET NULL,
    FOREIGN KEY (new_owner_id) REFERENCES owners(id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_mutation_number (mutation_number),
    INDEX idx_status (status),
    INDEX idx_property_id (property_id),
    INDEX idx_requester_id (requester_id),
    INDEX idx_application_date (application_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: documents
-- Description: Document management for properties and mutations
-- =====================================================
CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_type_id INT,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT,
    mime_type VARCHAR(100),
    
    -- Associated entity
    entity_type ENUM('property', 'mutation', 'payment', 'owner', 'other') NOT NULL,
    entity_id INT NOT NULL,
    
    -- Document details
    document_number VARCHAR(100),
    issue_date DATE,
    expiry_date DATE,
    issuing_authority VARCHAR(255),
    
    -- Verification
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by INT,
    verification_date TIMESTAMP NULL,
    
    -- Metadata
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_type_id) REFERENCES document_types(id) ON DELETE SET NULL,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_document_type_id (document_type_id),
    INDEX idx_uploaded_by (uploaded_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: tax_assessments
-- Description: Property tax assessments
-- =====================================================
CREATE TABLE IF NOT EXISTS tax_assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    assessment_year INT NOT NULL,
    assessed_value DECIMAL(15, 2) NOT NULL,
    tax_amount DECIMAL(12, 2) NOT NULL,
    
    -- Status
    status ENUM('assessed', 'paid', 'overdue', 'waived') DEFAULT 'assessed',
    due_date DATE,
    
    -- Assessment details
    assessed_by INT,
    assessment_date DATE,
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (assessed_by) REFERENCES users(id) ON DELETE SET NULL,
    
    UNIQUE KEY uk_property_year (property_id, assessment_year),
    INDEX idx_assessment_year (assessment_year),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: payments
-- Description: Payment transactions
-- =====================================================
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_reference VARCHAR(100) UNIQUE NOT NULL,
    transaction_id VARCHAR(255) UNIQUE,
    
    -- Payment details
    user_id INT NOT NULL,
    property_id INT,
    mutation_id INT,
    
    -- Amount details
    payment_type ENUM('property_tax', 'mutation_fee', 'registration_fee', 'penalty', 'other') NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    penalty_amount DECIMAL(10, 2) DEFAULT 0.00,
    total_amount DECIMAL(12, 2) NOT NULL,
    
    -- Payment method
    payment_method ENUM('online', 'cash', 'cheque', 'dd', 'card') NOT NULL,
    payment_gateway VARCHAR(100),
    
    -- Status
    status ENUM('pending', 'processing', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    payment_date TIMESTAMP NULL,
    
    -- Additional details
    remarks TEXT,
    receipt_number VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL,
    FOREIGN KEY (mutation_id) REFERENCES mutations(id) ON DELETE SET NULL,
    
    INDEX idx_payment_reference (payment_reference),
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_payment_date (payment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: notifications
-- Description: User notifications
-- =====================================================
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    notification_type ENUM('info', 'warning', 'success', 'error') DEFAULT 'info',
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Related entity
    related_entity_type VARCHAR(50),
    related_entity_id INT,
    
    -- Status
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: audit_logs
-- Description: System activity audit trail
-- =====================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INT,
    
    -- Details
    description TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Data changes
    old_values JSON,
    new_values JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: property_valuations
-- Description: Property valuation history
-- =====================================================
CREATE TABLE IF NOT EXISTS property_valuations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    valuation_date DATE NOT NULL,
    valuation_amount DECIMAL(15, 2) NOT NULL,
    valuation_type ENUM('market', 'government', 'bank', 'insurance') DEFAULT 'market',
    
    -- Valuer details
    valued_by INT,
    valuation_method VARCHAR(255),
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (valued_by) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_property_id (property_id),
    INDEX idx_valuation_date (valuation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: property_status_history
-- Description: Track status changes of properties
-- =====================================================
CREATE TABLE IF NOT EXISTS property_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by INT NOT NULL,
    change_reason TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_property_id (property_id),
    INDEX idx_changed_at (changed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

-- Insert default master data
INSERT INTO land_categories (category_name, description) VALUES
('Urban Residential', 'Land used for residential purposes in urban areas'),
('Urban Commercial', 'Land used for commercial activities in urban areas'),
('Agricultural', 'Land used for agriculture and farming'),
('Industrial', 'Land designated for industrial use'),
('Forest', 'Forest land'),
('Government', 'Government owned land');

INSERT INTO usage_types (usage_type, description) VALUES
('Residential', 'Residential buildings and housing'),
('Commercial', 'Shops, offices, and commercial establishments'),
('Agricultural', 'Farming and agricultural activities'),
('Industrial', 'Manufacturing and industrial operations'),
('Mixed Use', 'Multiple uses combined'),
('Vacant', 'Vacant or unused land');

INSERT INTO document_types (document_type, description, is_mandatory) VALUES
('Sale Deed', 'Property sale agreement', TRUE),
('Title Deed', 'Property ownership document', TRUE),
('Encumbrance Certificate', 'Certificate of property encumbrance', TRUE),
('Tax Receipt', 'Property tax payment receipt', FALSE),
('Aadhar Card', 'Owner identity proof', TRUE),
('PAN Card', 'Owner PAN card', TRUE),
('Survey Document', 'Land survey report', FALSE),
('Mutation Certificate', 'Previous mutation certificate', FALSE);
