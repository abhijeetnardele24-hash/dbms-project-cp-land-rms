# Database - Land Registry Management System

## Overview
This directory contains all SQL-related files for the Land Registry Management System. The project uses **MySQL 8.0+** as the primary database management system.

## Database Architecture

### Database: `land_registry_db`
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Tables**: 15+ normalized tables with proper relationships

## SQL Files

### 1. **schema.sql** (Main Database Schema)
Complete database schema with all tables, relationships, indexes, and constraints.

**Key Tables:**
- `users` - User authentication and role management
- `properties` - Land parcel/property records with ULPIN
- `owners` - Property owner information
- `ownerships` - Property-Owner relationships (supports joint ownership)
- `mutations` - Ownership change/mutation requests
- `documents` - Document management system
- `tax_assessments` - Property tax assessments
- `payments` - Payment transactions
- `notifications` - User notifications
- `audit_logs` - Complete audit trail
- `property_valuations` - Property valuation history
- `land_categories` - Master data for land classification
- `usage_types` - Property usage types
- `document_types` - Document type master data

**Database Features:**
- ✅ 15+ normalized tables (3NF)
- ✅ Foreign key constraints for referential integrity
- ✅ Strategic indexes for query optimization
- ✅ ENUM types for data validation
- ✅ Cascading deletes/updates where appropriate
- ✅ Timestamp tracking (created_at, updated_at)
- ✅ Soft deletes using is_active flags
- ✅ JSON fields for flexible data storage
- ✅ Decimal precision for financial data
- ✅ Unique constraints for data integrity

### 2. **advanced_mysql_features.sql**
Advanced database programming features:

**Stored Procedures (8+):**
- `sp_calculate_property_tax_advanced` - Tax calculation with penalties
- `sp_get_property_valuation_trends` - Valuation trend analysis
- `sp_analyze_market_by_region` - Geographic market analysis
- `sp_get_owner_portfolio_report` - Owner portfolio analytics
- `sp_auto_approve_simple_mutations` - Automated mutation approval
- `sp_generate_tax_reminders` - Tax reminder generation
- `sp_update_analytics_cache` - Analytics caching

**Functions:**
- `fn_calculate_property_risk_score` - Risk score calculation
- `fn_generate_ulpin` - ULPIN generation logic

**Triggers (10+):**
- Property status change triggers
- Audit logging triggers
- Automatic notification triggers
- Tax calculation triggers
- Validation triggers

**Views (12+):**
- `v_property_details` - Complete property information
- `v_active_ownerships` - Current ownership relationships
- `v_pending_mutations` - Pending mutation requests
- `v_tax_summary` - Tax assessment summaries
- `v_user_dashboard` - User dashboard data
- `v_property_documents` - Property document summary
- And more...

**MySQL Events:**
- Scheduled tax reminders
- Overdue payment notifications
- Data cleanup jobs

### 3. **queries.sql** (Common SQL Queries)
Collection of commonly used queries organized by category:

**User Management Queries:**
- Active users by role
- User registration statistics
- Role-based user counts

**Property Queries:**
- Approved properties with owners
- Property statistics by district
- High-value properties
- Properties without owners
- Joint ownership properties

**Ownership Queries:**
- Complete ownership details
- Properties by owner
- Owner portfolio value
- Joint ownership analysis

**Mutation Queries:**
- Pending mutation requests
- Mutation statistics by type
- Processing time analysis

**Tax & Payment Queries:**
- Pending tax assessments
- Tax collection summary
- Payment history
- Revenue reports
- Overdue payments

**Document Queries:**
- Documents pending verification
- Document statistics by type

**Audit & Activity Queries:**
- Recent system activity
- Activity by user role
- Most active users

**Notification Queries:**
- Unread notifications
- Notification statistics

**Analytical Queries:**
- Property market trends
- Comprehensive reports
- Dashboard statistics

### 4. **mysql_advanced_features.sql**
Additional MySQL optimization features:
- Table partitioning strategies
- Performance indexes
- Query optimization hints
- Stored procedure optimization

### 5. **implement_partitioning.sql**
Table partitioning implementation for:
- Large tables (properties, payments, audit_logs)
- Range partitioning by date
- Performance optimization for historical data

## Database Statistics

### Table Count: 15+
### Stored Procedures: 8+
### Functions: 2+
### Triggers: 10+
### Views: 12+
### Indexes: 50+

## Entity Relationships

```
users (1) ----< (M) properties [approved_by]
users (1) ----< (M) owners [user_id]
users (1) ----< (M) mutations [requester_id, reviewed_by]
users (1) ----< (M) payments [user_id]
users (1) ----< (M) notifications [user_id]
users (1) ----< (M) audit_logs [user_id]

properties (1) ----< (M) ownerships
properties (1) ----< (M) mutations
properties (1) ----< (M) documents
properties (1) ----< (M) tax_assessments
properties (1) ----< (M) payments
properties (1) ----< (M) property_valuations

owners (1) ----< (M) ownerships
owners (1) ----< (M) mutations [previous_owner_id, new_owner_id]

land_categories (1) ----< (M) properties
usage_types (1) ----< (M) properties
document_types (1) ----< (M) documents
```

## Key Features

### 1. **ACID Compliance**
- Transactions for data integrity
- Atomic operations for mutations
- Consistent state management
- Isolated concurrent operations
- Durable data storage

### 2. **Data Integrity**
- Foreign key constraints
- Check constraints via ENUM
- Unique constraints (ULPIN, emails, etc.)
- NOT NULL constraints where applicable
- Cascading operations

### 3. **Performance Optimization**
- Strategic indexes on frequently queried columns
- Composite indexes for complex queries
- Table partitioning for large tables
- Query optimization via EXPLAIN
- Connection pooling support

### 4. **Security**
- Role-based access control (RBAC)
- Password hashing (handled by application)
- Audit logging for all critical operations
- Soft deletes for data recovery
- No sensitive data in plain text

### 5. **Scalability**
- Normalized schema (3NF)
- Efficient indexing strategy
- Partitioning for large datasets
- View-based data access
- Stored procedures for complex operations

## Usage

### Setup Database
```bash
# Using MySQL CLI
mysql -u root -p < database/schema.sql

# Or using MySQL Workbench
# File > Open SQL Script > schema.sql > Execute
```

### Run Advanced Features
```bash
mysql -u root -p land_registry_db < database/advanced_mysql_features.sql
```

### Test Queries
```bash
mysql -u root -p land_registry_db < database/queries.sql
```

## Database Configuration

**Connection String:**
```
mysql+pymysql://root:1234@localhost/land_registry_db
```

**Connection Parameters:**
- Host: localhost
- Port: 3306
- Database: land_registry_db
- User: root
- Password: 1234
- Charset: utf8mb4

## Backup & Restore

### Backup Database
```bash
mysqldump -u root -p land_registry_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p land_registry_db < backup.sql
```

### Backup with Stored Procedures/Triggers
```bash
mysqldump -u root -p --routines --triggers land_registry_db > full_backup.sql
```

## Performance Monitoring

### Check Table Sizes
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = "land_registry_db"
ORDER BY (data_length + index_length) DESC;
```

### Check Index Usage
```sql
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    SEQ_IN_INDEX,
    COLUMN_NAME,
    CARDINALITY
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'land_registry_db'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

## SQL Best Practices Used

1. ✅ **Normalization**: Tables are normalized to 3NF
2. ✅ **Proper Data Types**: Appropriate data types for each column
3. ✅ **Indexes**: Strategic indexes on frequently queried columns
4. ✅ **Foreign Keys**: All relationships enforced with FK constraints
5. ✅ **Naming Conventions**: Consistent table and column naming
6. ✅ **Comments**: Inline comments for complex logic
7. ✅ **Default Values**: Sensible defaults for columns
8. ✅ **Timestamps**: Created/Updated timestamps on all tables
9. ✅ **Soft Deletes**: is_active flags instead of hard deletes
10. ✅ **Transaction Safety**: Atomic operations for critical updates

## DBMS Concepts Demonstrated

### Core Concepts
- ✅ Relational database design
- ✅ Entity-Relationship modeling
- ✅ Normalization (1NF, 2NF, 3NF)
- ✅ Primary and Foreign keys
- ✅ Referential integrity
- ✅ ACID properties

### Advanced Concepts
- ✅ Stored Procedures & Functions
- ✅ Triggers (BEFORE/AFTER, INSERT/UPDATE/DELETE)
- ✅ Views (Simple & Complex)
- ✅ Indexes (Single & Composite)
- ✅ Table Partitioning
- ✅ Transactions
- ✅ Joins (INNER, LEFT, RIGHT, CROSS)
- ✅ Subqueries & CTEs
- ✅ Aggregate Functions
- ✅ Window Functions
- ✅ Date/Time Functions
- ✅ String Functions
- ✅ JSON Functions
- ✅ Scheduled Events

## Contact

For database-related questions or issues, refer to the main project README.md

---
**Note:** This is a comprehensive DBMS project demonstrating advanced SQL concepts and best practices for enterprise-level database design.
