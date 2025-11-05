-- =====================================================
-- LAND REGISTRY MANAGEMENT SYSTEM - COMMON SQL QUERIES
-- =====================================================
-- Description: Collection of commonly used SQL queries for the system
-- =====================================================

USE land_registry_db;

-- =====================================================
-- USER MANAGEMENT QUERIES
-- =====================================================

-- Get all active users by role
SELECT 
    id, email, full_name, phone_number, role, created_at, last_login
FROM users
WHERE is_active = TRUE
ORDER BY role, full_name;

-- Count users by role
SELECT 
    role,
    COUNT(*) as user_count,
    COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active_count,
    COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_count
FROM users
GROUP BY role
ORDER BY user_count DESC;

-- Recent user registrations (last 30 days)
SELECT 
    email, full_name, role, created_at
FROM users
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY created_at DESC;

-- =====================================================
-- PROPERTY QUERIES
-- =====================================================

-- Get all approved properties with owner information
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
    GROUP_CONCAT(DISTINCT o.full_name SEPARATOR ', ') as owners,
    COUNT(DISTINCT ow.owner_id) as owner_count
FROM properties p
LEFT JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
LEFT JOIN owners o ON ow.owner_id = o.id
WHERE p.status = 'approved'
GROUP BY p.id
ORDER BY p.created_at DESC;

-- Property statistics by district
SELECT 
    district,
    state,
    COUNT(*) as total_properties,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_count,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_count,
    AVG(market_value) as avg_market_value,
    SUM(market_value) as total_market_value,
    AVG(area) as avg_area
FROM properties
GROUP BY district, state
ORDER BY total_properties DESC;

-- Properties by type and status
SELECT 
    property_type,
    status,
    COUNT(*) as count,
    AVG(market_value) as avg_value,
    SUM(market_value) as total_value
FROM properties
GROUP BY property_type, status
ORDER BY property_type, status;

-- High-value properties (top 10)
SELECT 
    p.ulpin,
    p.property_type,
    p.area,
    p.market_value,
    p.village_city,
    p.district,
    p.state,
    GROUP_CONCAT(o.full_name SEPARATOR ', ') as owners
FROM properties p
LEFT JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
LEFT JOIN owners o ON ow.owner_id = o.id
WHERE p.status = 'approved'
GROUP BY p.id
ORDER BY p.market_value DESC
LIMIT 10;

-- Properties without owners
SELECT 
    p.id,
    p.ulpin,
    p.property_type,
    p.area,
    p.market_value,
    p.village_city,
    p.district,
    p.status
FROM properties p
LEFT JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
WHERE ow.id IS NULL
ORDER BY p.created_at DESC;

-- =====================================================
-- OWNERSHIP QUERIES
-- =====================================================

-- Get complete ownership details for a property
SELECT 
    p.ulpin,
    p.property_type,
    p.market_value,
    o.full_name as owner_name,
    o.aadhar_number,
    o.pan_number,
    o.phone_number,
    ow.ownership_percentage,
    ow.ownership_type,
    ow.acquisition_date,
    ow.acquisition_mode
FROM properties p
INNER JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
INNER JOIN owners o ON ow.owner_id = o.id
WHERE p.ulpin = 'ULPIN123456'  -- Replace with actual ULPIN
ORDER BY ow.ownership_percentage DESC;

-- Properties owned by a specific person (by Aadhar)
SELECT 
    p.ulpin,
    p.property_type,
    p.area,
    p.market_value,
    p.village_city,
    p.district,
    p.state,
    ow.ownership_percentage,
    ow.acquisition_date
FROM properties p
INNER JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
INNER JOIN owners o ON ow.owner_id = o.id
WHERE o.aadhar_number = '123456789012'  -- Replace with actual Aadhar
ORDER BY ow.acquisition_date DESC;

-- Joint ownership properties
SELECT 
    p.id,
    p.ulpin,
    p.property_type,
    p.market_value,
    COUNT(ow.owner_id) as owner_count,
    GROUP_CONCAT(CONCAT(o.full_name, ' (', ow.ownership_percentage, '%)') SEPARATOR ', ') as owners_with_share
FROM properties p
INNER JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
INNER JOIN owners o ON ow.owner_id = o.id
GROUP BY p.id
HAVING owner_count > 1
ORDER BY owner_count DESC;

-- Owner portfolio value
SELECT 
    o.id,
    o.full_name,
    o.aadhar_number,
    COUNT(DISTINCT p.id) as properties_owned,
    SUM(p.market_value * ow.ownership_percentage / 100) as total_property_value,
    AVG(p.market_value) as avg_property_value
FROM owners o
INNER JOIN ownerships ow ON o.id = ow.owner_id AND ow.is_current = TRUE
INNER JOIN properties p ON ow.property_id = p.id AND p.status = 'approved'
GROUP BY o.id
ORDER BY total_property_value DESC;

-- =====================================================
-- MUTATION QUERIES
-- =====================================================

-- Pending mutation requests
SELECT 
    m.id,
    m.mutation_number,
    m.mutation_type,
    p.ulpin,
    p.property_type,
    p.village_city,
    p.district,
    prev_o.full_name as previous_owner,
    new_o.full_name as new_owner,
    m.transfer_percentage,
    m.application_date,
    u.full_name as requester,
    DATEDIFF(CURDATE(), m.application_date) as days_pending
FROM mutations m
INNER JOIN properties p ON m.property_id = p.id
LEFT JOIN owners prev_o ON m.previous_owner_id = prev_o.id
INNER JOIN owners new_o ON m.new_owner_id = new_o.id
INNER JOIN users u ON m.requester_id = u.id
WHERE m.status = 'pending'
ORDER BY m.application_date ASC;

-- Mutation statistics by type
SELECT 
    mutation_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_count,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_count,
    AVG(CASE WHEN status = 'approved' 
        THEN DATEDIFF(review_date, application_date) END) as avg_processing_days
FROM mutations
GROUP BY mutation_type
ORDER BY total_count DESC;

-- Recent mutations (last 90 days)
SELECT 
    m.mutation_number,
    m.mutation_type,
    p.ulpin,
    new_o.full_name as new_owner,
    m.status,
    m.application_date,
    m.review_date
FROM mutations m
INNER JOIN properties p ON m.property_id = p.id
INNER JOIN owners new_o ON m.new_owner_id = new_o.id
WHERE m.application_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
ORDER BY m.application_date DESC;

-- =====================================================
-- TAX AND PAYMENT QUERIES
-- =====================================================

-- Properties with pending tax assessments
SELECT 
    p.ulpin,
    p.property_type,
    p.market_value,
    p.village_city,
    p.district,
    ta.assessment_year,
    ta.tax_amount,
    ta.due_date,
    DATEDIFF(CURDATE(), ta.due_date) as days_overdue,
    GROUP_CONCAT(o.full_name SEPARATOR ', ') as owners
FROM properties p
INNER JOIN tax_assessments ta ON p.id = ta.property_id
LEFT JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
LEFT JOIN owners o ON ow.owner_id = o.id
WHERE ta.status = 'assessed' 
  AND ta.due_date < CURDATE()
GROUP BY p.id, ta.id
ORDER BY days_overdue DESC;

-- Tax collection summary by year
SELECT 
    assessment_year,
    COUNT(DISTINCT property_id) as properties_assessed,
    SUM(tax_amount) as total_tax_assessed,
    SUM(CASE WHEN status = 'paid' THEN tax_amount ELSE 0 END) as total_tax_collected,
    COUNT(CASE WHEN status = 'paid' THEN 1 END) as paid_count,
    COUNT(CASE WHEN status = 'overdue' THEN 1 END) as overdue_count,
    ROUND(SUM(CASE WHEN status = 'paid' THEN tax_amount ELSE 0 END) / SUM(tax_amount) * 100, 2) as collection_percentage
FROM tax_assessments
GROUP BY assessment_year
ORDER BY assessment_year DESC;

-- Payment history for a property
SELECT 
    pay.payment_reference,
    pay.transaction_id,
    pay.payment_type,
    pay.amount,
    pay.penalty_amount,
    pay.total_amount,
    pay.payment_method,
    pay.status,
    pay.payment_date,
    u.full_name as paid_by
FROM payments pay
INNER JOIN users u ON pay.user_id = u.id
WHERE pay.property_id = 1  -- Replace with actual property ID
ORDER BY pay.payment_date DESC;

-- Daily payment collection report
SELECT 
    DATE(payment_date) as payment_day,
    payment_type,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_collected,
    AVG(total_amount) as avg_transaction
FROM payments
WHERE status = 'completed'
  AND payment_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(payment_date), payment_type
ORDER BY payment_day DESC, payment_type;

-- Top payers
SELECT 
    u.full_name,
    u.email,
    COUNT(pay.id) as payment_count,
    SUM(pay.total_amount) as total_paid,
    MAX(pay.payment_date) as last_payment_date
FROM users u
INNER JOIN payments pay ON u.id = pay.user_id
WHERE pay.status = 'completed'
GROUP BY u.id
ORDER BY total_paid DESC
LIMIT 20;

-- =====================================================
-- DOCUMENT QUERIES
-- =====================================================

-- Documents pending verification
SELECT 
    d.id,
    d.document_name,
    dt.document_type as type,
    d.entity_type,
    d.entity_id,
    d.uploaded_at,
    u.full_name as uploaded_by,
    DATEDIFF(CURDATE(), d.uploaded_at) as days_pending
FROM documents d
LEFT JOIN document_types dt ON d.document_type_id = dt.id
INNER JOIN users u ON d.uploaded_by = u.id
WHERE d.is_verified = FALSE
ORDER BY d.uploaded_at ASC;

-- Documents by entity type
SELECT 
    entity_type,
    COUNT(*) as total_documents,
    COUNT(CASE WHEN is_verified = TRUE THEN 1 END) as verified_count,
    SUM(file_size) / 1024 / 1024 as total_size_mb
FROM documents
GROUP BY entity_type
ORDER BY total_documents DESC;

-- =====================================================
-- AUDIT AND ACTIVITY QUERIES
-- =====================================================

-- Recent system activity
SELECT 
    al.id,
    u.full_name as user_name,
    u.role,
    al.action,
    al.entity_type,
    al.entity_id,
    al.description,
    al.created_at
FROM audit_logs al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC
LIMIT 100;

-- Activity by user role
SELECT 
    u.role,
    al.action,
    COUNT(*) as action_count,
    MAX(al.created_at) as last_activity
FROM audit_logs al
INNER JOIN users u ON al.user_id = u.id
WHERE al.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY u.role, al.action
ORDER BY u.role, action_count DESC;

-- Most active users
SELECT 
    u.full_name,
    u.email,
    u.role,
    COUNT(al.id) as activity_count,
    MAX(al.created_at) as last_activity
FROM users u
INNER JOIN audit_logs al ON u.id = al.user_id
WHERE al.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY u.id
ORDER BY activity_count DESC
LIMIT 20;

-- =====================================================
-- NOTIFICATION QUERIES
-- =====================================================

-- Unread notifications by user
SELECT 
    u.full_name,
    u.email,
    COUNT(n.id) as unread_count,
    MIN(n.created_at) as oldest_notification
FROM users u
INNER JOIN notifications n ON u.id = n.user_id
WHERE n.is_read = FALSE
GROUP BY u.id
HAVING unread_count > 0
ORDER BY unread_count DESC;

-- Notification statistics by type
SELECT 
    notification_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN is_read = TRUE THEN 1 END) as read_count,
    COUNT(CASE WHEN is_read = FALSE THEN 1 END) as unread_count,
    AVG(CASE WHEN is_read = TRUE 
        THEN TIMESTAMPDIFF(MINUTE, created_at, read_at) END) as avg_read_time_minutes
FROM notifications
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY notification_type
ORDER BY total_count DESC;

-- =====================================================
-- COMPLEX ANALYTICAL QUERIES
-- =====================================================

-- Property market trends by district (last 12 months)
SELECT 
    district,
    YEAR(registered_date) as year,
    MONTH(registered_date) as month,
    COUNT(*) as properties_registered,
    AVG(market_value) as avg_market_value,
    MIN(market_value) as min_market_value,
    MAX(market_value) as max_market_value
FROM properties
WHERE status = 'approved'
  AND registered_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY district, YEAR(registered_date), MONTH(registered_date)
ORDER BY district, year DESC, month DESC;

-- Comprehensive property report with all details
SELECT 
    p.id,
    p.ulpin,
    p.property_type,
    p.area,
    p.area_unit,
    p.market_value,
    p.survey_number,
    p.village_city,
    p.district,
    p.state,
    p.status,
    lc.category_name as land_category,
    ut.usage_type,
    GROUP_CONCAT(DISTINCT CONCAT(o.full_name, ' (', ow.ownership_percentage, '%)') 
        ORDER BY ow.ownership_percentage DESC SEPARATOR ', ') as owners,
    COUNT(DISTINCT d.id) as document_count,
    COUNT(DISTINCT m.id) as mutation_count,
    COALESCE(SUM(CASE WHEN ta.status = 'assessed' THEN ta.tax_amount ELSE 0 END), 0) as pending_tax,
    COALESCE(MAX(ta.assessment_year), 0) as last_tax_year
FROM properties p
LEFT JOIN land_categories lc ON p.land_category_id = lc.id
LEFT JOIN usage_types ut ON p.usage_type_id = ut.id
LEFT JOIN ownerships ow ON p.id = ow.property_id AND ow.is_current = TRUE
LEFT JOIN owners o ON ow.owner_id = o.id
LEFT JOIN documents d ON p.id = d.entity_id AND d.entity_type = 'property'
LEFT JOIN mutations m ON p.id = m.property_id
LEFT JOIN tax_assessments ta ON p.id = ta.property_id
WHERE p.status = 'approved'
GROUP BY p.id
ORDER BY p.created_at DESC;

-- System dashboard statistics
SELECT 
    (SELECT COUNT(*) FROM users WHERE is_active = TRUE) as total_active_users,
    (SELECT COUNT(*) FROM properties WHERE status = 'approved') as total_properties,
    (SELECT COUNT(*) FROM properties WHERE status = 'pending') as pending_properties,
    (SELECT COUNT(*) FROM mutations WHERE status = 'pending') as pending_mutations,
    (SELECT COUNT(*) FROM documents WHERE is_verified = FALSE) as unverified_documents,
    (SELECT SUM(market_value) FROM properties WHERE status = 'approved') as total_property_value,
    (SELECT SUM(tax_amount) FROM tax_assessments WHERE status = 'assessed') as pending_tax_amount,
    (SELECT SUM(total_amount) FROM payments WHERE status = 'completed' 
        AND YEAR(payment_date) = YEAR(CURDATE())) as yearly_revenue;

-- =====================================================
-- END OF QUERIES
-- =====================================================
