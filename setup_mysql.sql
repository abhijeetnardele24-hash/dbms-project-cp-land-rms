-- MySQL Database Setup Script for LRMS
-- Run this script as MySQL root user

-- Create database
CREATE DATABASE IF NOT EXISTS lrms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional - you can use root or existing user)
CREATE USER IF NOT EXISTS 'lrms_user'@'localhost' IDENTIFIED BY 'lrms_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON lrms.* TO 'lrms_user'@'localhost';
GRANT ALL PRIVILEGES ON lrms.* TO 'root'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Use the database
USE lrms;

-- Show that database is ready
SELECT 'LRMS Database setup completed successfully!' as Status;
