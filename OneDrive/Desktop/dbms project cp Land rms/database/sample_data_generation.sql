-- =====================================================
-- SAMPLE DATA GENERATION
-- Land Registry Management System
-- =====================================================
-- This file contains SQL scripts to generate comprehensive
-- sample/test data for all tables in the LRMS database
-- =====================================================

USE land_registry_db;

-- =====================================================
-- SECTION 1: CLEAR EXISTING DATA (OPTIONAL - USE WITH CAUTION)
-- =====================================================

-- Uncomment the following lines to clear existing data
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE audit_logs;
-- TRUNCATE TABLE notifications;
-- TRUNCATE TABLE documents;
-- TRUNCATE TABLE payments;
-- TRUNCATE TABLE tax_assessments;
-- TRUNCATE TABLE mutations;
-- TRUNCATE TABLE ownerships;
-- TRUNCATE TABLE owners;
-- TRUNCATE TABLE properties;
-- TRUNCATE TABLE users;
-- SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- SECTION 2: INSERT SAMPLE USERS
-- =====================================================

INSERT INTO users (email, password_hash, full_name, phone_number, role, is_active, email_verified) VALUES
-- Admin users
('admin@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'System Administrator', '9876543210', 'admin', TRUE, TRUE),
('super.admin@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Super Administrator', '9876543211', 'admin', TRUE, TRUE),

-- Registrar users
('registrar@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'John Registrar', '9876543212', 'registrar', TRUE, TRUE),
('registrar2@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Sarah Registrar', '9876543213', 'registrar', TRUE, TRUE),

-- Officer users
('officer@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Mike Officer', '9876543214', 'officer', TRUE, TRUE),
('officer2@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Emma Officer', '9876543215', 'officer', TRUE, TRUE),

-- Citizen users
('user@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Rajesh Kumar', '9876543220', 'citizen', TRUE, TRUE),
('user2@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Priya Sharma', '9876543221', 'citizen', TRUE, TRUE),
('user3@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Amit Patel', '9876543222', 'citizen', TRUE, TRUE),
('user4@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Sneha Verma', '9876543223', 'citizen', TRUE, TRUE),
('user5@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Vikram Singh', '9876543224', 'citizen', TRUE, TRUE),
('user6@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Anjali Reddy', '9876543225', 'citizen', TRUE, TRUE),
('user7@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Rahul Gupta', '9876543226', 'citizen', TRUE, TRUE),
('user8@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Kavita Iyer', '9876543227', 'citizen', TRUE, TRUE),
('user9@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Arjun Nair', '9876543228', 'citizen', TRUE, TRUE),
('user10@lrms.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5i7wvxP7pJfWu', 'Deepika Joshi', '9876543229', 'citizen', TRUE, TRUE);

-- =====================================================
-- SECTION 3: INSERT SAMPLE OWNERS
-- =====================================================

INSERT INTO owners (user_id, full_name, father_name, date_of_birth, gender, aadhar_number, pan_number, phone_number, email, address_line1, city, state, pincode) VALUES
(7, 'Rajesh Kumar', 'Ramesh Kumar', '1975-05-15', 'Male', '123456789012', 'ABCDE1234F', '9876543220', 'user@lrms.com', '123 MG Road', 'Mumbai', 'Maharashtra', '400001'),
(8, 'Priya Sharma', 'Suresh Sharma', '1982-08-20', 'Female', '223456789012', 'BCDEF2345G', '9876543221', 'user2@lrms.com', '456 Brigade Road', 'Bangalore', 'Karnataka', '560001'),
(9, 'Amit Patel', 'Jayesh Patel', '1978-03-10', 'Male', '323456789012', 'CDEFG3456H', '9876543222', 'user3@lrms.com', '789 CG Road', 'Ahmedabad', 'Gujarat', '380001'),
(10, 'Sneha Verma', 'Anil Verma', '1985-12-25', 'Female', '423456789012', 'DEFGH4567I', '9876543223', 'user4@lrms.com', '321 Park Street', 'Kolkata', 'West Bengal', '700001'),
(11, 'Vikram Singh', 'Balwant Singh', '1970-07-05', 'Male', '523456789012', 'EFGHI5678J', '9876543224', 'user5@lrms.com', '654 Connaught Place', 'Delhi', 'Delhi', '110001'),
(12, 'Anjali Reddy', 'Venkat Reddy', '1988-11-18', 'Female', '623456789012', 'FGHIJ6789K', '9876543225', 'user6@lrms.com', '987 Jubilee Hills', 'Hyderabad', 'Telangana', '500001'),
(13, 'Rahul Gupta', 'Mohan Gupta', '1983-04-30', 'Male', '723456789012', 'GHIJK7890L', '9876543226', 'user7@lrms.com', '246 Civil Lines', 'Jaipur', 'Rajasthan', '302001'),
(14, 'Kavita Iyer', 'Krishnan Iyer', '1990-09-14', 'Female', '823456789012', 'HIJKL8901M', '9876543227', 'user8@lrms.com', '135 Anna Nagar', 'Chennai', 'Tamil Nadu', '600001'),
(15, 'Arjun Nair', 'Madhavan Nair', '1976-06-22', 'Male', '923456789012', 'IJKLM9012N', '9876543228', 'user9@lrms.com', '468 MG Road', 'Kochi', 'Kerala', '682001'),
(16, 'Deepika Joshi', 'Prakash Joshi', '1992-02-08', 'Female', '103456789012', 'JKLMN0123O', '9876543229', 'user10@lrms.com', '791 FC Road', 'Pune', 'Maharashtra', '411001');

-- =====================================================
-- SECTION 4: INSERT SAMPLE PROPERTIES
-- =====================================================

INSERT INTO properties (ulpin, property_type, area, area_unit, market_value, survey_number, plot_number, village_city, district, state, pincode, latitude, longitude, land_category_id, usage_type_id, status, approved_by, approval_date, registered_date) VALUES
-- Mumbai properties
('MH01-MUM-001-2024', 'Residential', 1500.00, 'sq_ft', 12500000.00, 'SN-001', 'P-101', 'Andheri', 'Mumbai', 'Maharashtra', '400053', 19.1197, 72.8464, 1, 1, 'approved', 3, '2024-01-15 10:30:00', '2024-01-20 14:00:00'),
('MH01-MUM-002-2024', 'Commercial', 2500.00, 'sq_ft', 25000000.00, 'SN-002', 'P-102', 'Bandra', 'Mumbai', 'Maharashtra', '400050', 19.0596, 72.8295, 2, 2, 'approved', 3, '2024-01-18 11:00:00', '2024-01-22 15:30:00'),
('MH01-MUM-003-2024', 'Residential', 1800.00, 'sq_ft', 15000000.00, 'SN-003', 'P-103', 'Juhu', 'Mumbai', 'Maharashtra', '400049', 19.1075, 72.8263, 1, 1, 'approved', 3, '2024-02-05 09:45:00', '2024-02-10 16:00:00'),

-- Bangalore properties
('KA02-BLR-001-2024', 'Residential', 2000.00, 'sq_ft', 18000000.00, 'SN-004', 'P-201', 'Koramangala', 'Bangalore', 'Karnataka', '560034', 12.9352, 77.6245, 1, 1, 'approved', 3, '2024-01-25 10:15:00', '2024-02-01 14:30:00'),
('KA02-BLR-002-2024', 'Commercial', 3000.00, 'sq_ft', 30000000.00, 'SN-005', 'P-202', 'Whitefield', 'Bangalore', 'Karnataka', '560066', 12.9698, 77.7500, 2, 2, 'approved', 3, '2024-02-10 11:30:00', '2024-02-15 15:00:00'),
('KA02-BLR-003-2024', 'Industrial', 5000.00, 'sq_ft', 35000000.00, 'SN-006', 'P-203', 'Peenya', 'Bangalore', 'Karnataka', '560058', 13.0291, 77.5197, 4, 4, 'approved', 3, '2024-03-01 09:00:00', '2024-03-05 13:00:00'),

-- Ahmedabad properties
('GJ03-AMD-001-2024', 'Residential', 1600.00, 'sq_ft', 10000000.00, 'SN-007', 'P-301', 'Satellite', 'Ahmedabad', 'Gujarat', '380015', 23.0225, 72.5714, 1, 1, 'approved', 4, '2024-02-15 10:45:00', '2024-02-20 14:00:00'),
('GJ03-AMD-002-2024', 'Commercial', 2800.00, 'sq_ft', 22000000.00, 'SN-008', 'P-302', 'Vastrapur', 'Ahmedabad', 'Gujarat', '380015', 23.0395, 72.5246, 2, 2, 'approved', 4, '2024-03-05 11:15:00', '2024-03-10 15:30:00'),
('GJ03-AMD-003-2024', 'Agricultural', 10000.00, 'sq_meters', 5000000.00, 'SN-009', 'P-303', 'Sanand', 'Ahmedabad', 'Gujarat', '382110', 22.9944, 72.3662, 3, 3, 'approved', 4, '2024-03-15 09:30:00', '2024-03-20 13:00:00'),

-- Kolkata properties
('WB04-KOL-001-2024', 'Residential', 1400.00, 'sq_ft', 11000000.00, 'SN-010', 'P-401', 'Salt Lake', 'Kolkata', 'West Bengal', '700064', 22.5726, 88.3639, 1, 1, 'approved', 4, '2024-02-20 10:00:00', '2024-02-25 14:30:00'),
('WB04-KOL-002-2024', 'Commercial', 2400.00, 'sq_ft', 20000000.00, 'SN-011', 'P-402', 'Park Street', 'Kolkata', 'West Bengal', '700016', 22.5555, 88.3624, 2, 2, 'approved', 4, '2024-03-10 11:00:00', '2024-03-15 15:00:00'),

-- Delhi properties
('DL05-DEL-001-2024', 'Residential', 2200.00, 'sq_ft', 20000000.00, 'SN-012', 'P-501', 'Vasant Vihar', 'Delhi', 'Delhi', '110057', 28.5500, 77.1600, 1, 1, 'approved', 3, '2024-03-20 10:30:00', '2024-03-25 14:00:00'),
('DL05-DEL-002-2024', 'Commercial', 3500.00, 'sq_ft', 35000000.00, 'SN-013', 'P-502', 'Connaught Place', 'Delhi', 'Delhi', '110001', 28.6289, 77.2065, 2, 2, 'approved', 3, '2024-04-01 11:30:00', '2024-04-05 15:30:00'),

-- Hyderabad properties
('TG06-HYD-001-2024', 'Residential', 1900.00, 'sq_ft', 14000000.00, 'SN-014', 'P-601', 'Gachibowli', 'Hyderabad', 'Telangana', '500032', 17.4399, 78.3487, 1, 1, 'approved', 4, '2024-03-25 09:45:00', '2024-03-30 13:30:00'),
('TG06-HYD-002-2024', 'Commercial', 2700.00, 'sq_ft', 24000000.00, 'SN-015', 'P-602', 'HITEC City', 'Hyderabad', 'Telangana', '500081', 17.4435, 78.3772, 2, 2, 'approved', 4, '2024-04-05 10:15:00', '2024-04-10 14:00:00'),

-- Jaipur properties
('RJ07-JAI-001-2024', 'Residential', 1700.00, 'sq_ft', 12000000.00, 'SN-016', 'P-701', 'Malviya Nagar', 'Jaipur', 'Rajasthan', '302017', 26.8521, 75.8132, 1, 1, 'pending', NULL, NULL, NULL),
('RJ07-JAI-002-2024', 'Commercial', 2600.00, 'sq_ft', 21000000.00, 'SN-017', 'P-702', 'MI Road', 'Jaipur', 'Rajasthan', '302001', 26.9124, 75.7873, 2, 2, 'pending', NULL, NULL, NULL);

-- =====================================================
-- SECTION 5: INSERT SAMPLE OWNERSHIPS
-- =====================================================

INSERT INTO ownerships (property_id, owner_id, ownership_percentage, ownership_type, acquisition_date, acquisition_mode, is_current) VALUES
-- Single ownership
(1, 1, 100.00, 'sole', '2024-01-20', 'purchase', TRUE),
(2, 2, 100.00, 'sole', '2024-01-22', 'purchase', TRUE),
(3, 3, 100.00, 'sole', '2024-02-10', 'purchase', TRUE),
(4, 4, 100.00, 'sole', '2024-02-01', 'purchase', TRUE),
(5, 5, 100.00, 'sole', '2024-02-15', 'purchase', TRUE),
(6, 6, 100.00, 'sole', '2024-03-05', 'purchase', TRUE),
(7, 7, 100.00, 'sole', '2024-02-20', 'purchase', TRUE),
(8, 8, 100.00, 'sole', '2024-03-10', 'purchase', TRUE),
(9, 9, 100.00, 'sole', '2024-03-20', 'purchase', TRUE),

-- Joint ownership
(10, 1, 50.00, 'joint', '2024-02-25', 'purchase', TRUE),
(10, 2, 50.00, 'joint', '2024-02-25', 'purchase', TRUE),

(11, 3, 60.00, 'joint', '2024-03-15', 'purchase', TRUE),
(11, 4, 40.00, 'joint', '2024-03-15', 'purchase', TRUE),

(12, 5, 100.00, 'sole', '2024-03-25', 'purchase', TRUE),
(13, 6, 100.00, 'sole', '2024-04-05', 'purchase', TRUE),
(14, 7, 100.00, 'sole', '2024-03-30', 'purchase', TRUE),
(15, 8, 100.00, 'sole', '2024-04-10', 'purchase', TRUE);

-- =====================================================
-- SECTION 6: INSERT SAMPLE MUTATIONS
-- =====================================================

INSERT INTO mutations (mutation_number, property_id, mutation_type, mutation_reason, previous_owner_id, new_owner_id, transfer_percentage, requester_id, application_date, status, reviewed_by, review_date, application_fee, stamp_duty, registration_fee, total_fees) VALUES
-- Approved mutations
('MUT-2024-001', 1, 'sale', 'Property sold to new owner', 1, 10, 100.00, 7, '2024-05-01 10:00:00', 'approved', 5, '2024-05-05 14:00:00', 5000.00, 125000.00, 10000.00, 140000.00),
('MUT-2024-002', 3, 'gift', 'Gift deed to family member', 3, 9, 100.00, 9, '2024-05-10 11:00:00', 'approved', 5, '2024-05-12 15:00:00', 5000.00, 0.00, 10000.00, 15000.00),

-- Pending mutations
('MUT-2024-003', 5, 'sale', 'Property sale transaction', 5, 7, 100.00, 7, '2024-06-01 09:00:00', 'pending', NULL, NULL, 5000.00, 300000.00, 10000.00, 315000.00),
('MUT-2024-004', 7, 'inheritance', 'Inheritance from father', 7, 8, 100.00, 8, '2024-06-05 10:00:00', 'under_review', 6, NULL, 5000.00, 0.00, 10000.00, 15000.00);

-- =====================================================
-- SECTION 7: INSERT SAMPLE TAX ASSESSMENTS
-- =====================================================

INSERT INTO tax_assessments (property_id, assessment_year, assessed_value, tax_amount, status, due_date, assessed_by, assessment_date) VALUES
-- 2024 assessments
(1, 2024, 12500000.00, 100000.00, 'paid', '2024-03-31', 3, '2024-01-25'),
(2, 2024, 25000000.00, 375000.00, 'paid', '2024-03-31', 3, '2024-01-28'),
(3, 2024, 15000000.00, 120000.00, 'paid', '2024-03-31', 3, '2024-02-15'),
(4, 2024, 18000000.00, 144000.00, 'paid', '2024-03-31', 3, '2024-02-08'),
(5, 2024, 30000000.00, 450000.00, 'assessed', '2024-03-31', 3, '2024-02-20'),
(6, 2024, 35000000.00, 700000.00, 'assessed', '2024-03-31', 3, '2024-03-10'),
(7, 2024, 10000000.00, 80000.00, 'paid', '2024-03-31', 4, '2024-02-25'),
(8, 2024, 22000000.00, 330000.00, 'overdue', '2024-03-31', 4, '2024-03-15'),
(9, 2024, 5000000.00, 15000.00, 'paid', '2024-03-31', 4, '2024-03-25'),
(10, 2024, 11000000.00, 88000.00, 'assessed', '2024-03-31', 4, '2024-03-05');

-- =====================================================
-- SECTION 8: INSERT SAMPLE PAYMENTS
-- =====================================================

INSERT INTO payments (payment_reference, transaction_id, user_id, property_id, payment_type, amount, penalty_amount, total_amount, payment_method, payment_gateway, status, payment_date, receipt_number) VALUES
('PAY-2024-0001', 'TXN-123456789', 7, 1, 'property_tax', 100000.00, 0.00, 100000.00, 'online', 'Razorpay', 'completed', '2024-03-15 10:30:00', 'RCP-001'),
('PAY-2024-0002', 'TXN-123456790', 8, 2, 'property_tax', 375000.00, 0.00, 375000.00, 'online', 'Razorpay', 'completed', '2024-03-18 11:00:00', 'RCP-002'),
('PAY-2024-0003', 'TXN-123456791', 9, 3, 'property_tax', 120000.00, 0.00, 120000.00, 'card', 'PayU', 'completed', '2024-03-20 14:30:00', 'RCP-003'),
('PAY-2024-0004', 'TXN-123456792', 10, 4, 'property_tax', 144000.00, 0.00, 144000.00, 'online', 'Razorpay', 'completed', '2024-03-22 09:45:00', 'RCP-004'),
('PAY-2024-0005', 'TXN-123456793', 13, 7, 'property_tax', 80000.00, 0.00, 80000.00, 'online', 'PhonePe', 'completed', '2024-03-25 10:15:00', 'RCP-005'),
('PAY-2024-0006', 'TXN-123456794', 15, 9, 'property_tax', 15000.00, 0.00, 15000.00, 'card', 'Razorpay', 'completed', '2024-03-28 11:30:00', 'RCP-006'),
('PAY-2024-0007', NULL, 7, 1, 'mutation_fee', 140000.00, 0.00, 140000.00, 'online', 'Razorpay', 'completed', '2024-05-06 12:00:00', 'RCP-007'),
('PAY-2024-0008', NULL, 9, 3, 'mutation_fee', 15000.00, 0.00, 15000.00, 'card', 'PayU', 'completed', '2024-05-13 13:30:00', 'RCP-008');

-- =====================================================
-- SECTION 9: INSERT SAMPLE NOTIFICATIONS
-- =====================================================

INSERT INTO notifications (user_id, notification_type, title, message, related_entity_type, related_entity_id, is_read) VALUES
(7, 'success', 'Property Approved', 'Your property registration has been approved.', 'property', 1, TRUE),
(8, 'success', 'Property Approved', 'Your property registration has been approved.', 'property', 2, TRUE),
(7, 'info', 'Tax Payment Due', 'Your property tax payment is due by 31st March 2024.', 'tax_assessment', 1, FALSE),
(8, 'warning', 'Tax Payment Overdue', 'Your property tax payment is overdue. Please pay immediately.', 'tax_assessment', 8, FALSE),
(7, 'success', 'Mutation Approved', 'Your mutation request has been approved.', 'mutation', 1, FALSE),
(9, 'success', 'Mutation Approved', 'Your mutation request has been approved.', 'mutation', 2, FALSE),
(7, 'info', 'Mutation Under Review', 'Your mutation request is under review.', 'mutation', 3, FALSE);

-- =====================================================
-- SECTION 10: INSERT SAMPLE AUDIT LOGS
-- =====================================================

INSERT INTO audit_logs (user_id, action, entity_type, entity_id, description, ip_address) VALUES
(1, 'LOGIN', 'user', 1, 'Admin logged in', '192.168.1.100'),
(3, 'APPROVE_PROPERTY', 'property', 1, 'Property approved by registrar', '192.168.1.101'),
(7, 'REGISTER_PROPERTY', 'property', 1, 'New property registered', '192.168.1.102'),
(7, 'PAYMENT_SUCCESS', 'payment', 1, 'Tax payment completed', '192.168.1.102'),
(5, 'APPROVE_MUTATION', 'mutation', 1, 'Mutation request approved by officer', '192.168.1.103'),
(7, 'SUBMIT_MUTATION', 'mutation', 1, 'New mutation request submitted', '192.168.1.102'),
(3, 'APPROVE_PROPERTY', 'property', 2, 'Property approved by registrar', '192.168.1.101'),
(8, 'REGISTER_PROPERTY', 'property', 2, 'New property registered', '192.168.1.104');

-- =====================================================
-- SECTION 11: VERIFICATION QUERIES
-- =====================================================

-- Count records in each table
SELECT 'Users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'Owners', COUNT(*) FROM owners
UNION ALL
SELECT 'Properties', COUNT(*) FROM properties
UNION ALL
SELECT 'Ownerships', COUNT(*) FROM ownerships
UNION ALL
SELECT 'Mutations', COUNT(*) FROM mutations
UNION ALL
SELECT 'Tax Assessments', COUNT(*) FROM tax_assessments
UNION ALL
SELECT 'Payments', COUNT(*) FROM payments
UNION ALL
SELECT 'Notifications', COUNT(*) FROM notifications
UNION ALL
SELECT 'Audit Logs', COUNT(*) FROM audit_logs;

-- Verify data integrity
SELECT 
    'Properties without owners' as check_name,
    COUNT(*) as count
FROM properties p
LEFT JOIN ownerships o ON p.id = o.property_id AND o.is_current = TRUE
WHERE o.id IS NULL

UNION ALL

SELECT 
    'Orphaned ownerships',
    COUNT(*)
FROM ownerships o
LEFT JOIN properties p ON o.property_id = p.id
WHERE p.id IS NULL

UNION ALL

SELECT 
    'Payments without properties',
    COUNT(*)
FROM payments pay
LEFT JOIN properties p ON pay.property_id = p.id
WHERE pay.property_id IS NOT NULL AND p.id IS NULL;

-- =====================================================
-- END OF SAMPLE DATA GENERATION
-- =====================================================

-- Summary:
-- - 17 Users (2 admin, 2 registrar, 2 officer, 11 citizen)
-- - 10 Owners
-- - 17 Properties (15 approved, 2 pending)
-- - 20 Ownerships (including joint ownerships)
-- - 4 Mutations (2 approved, 2 pending)
-- - 10 Tax Assessments
-- - 8 Payments
-- - 7 Notifications
-- - 8 Audit Log entries

-- This provides a comprehensive dataset for testing all features of the LRMS
