# Bug Fix: "Unknown column 'tax_amount'" Error

## Problem
When approving or rejecting property registrations through the registrar interface, the application threw this error:
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1054, "Unknown column 'tax_amount' in 'field list'")
[SQL: UPDATE properties SET status=%(status)s, ...]
```

## Root Cause
The error was caused by a **database trigger** named `trg_auto_create_tax_assessment` that was trying to insert data into the `tax_assessments` table using an outdated column name.

### The Issue:
1. The trigger referenced a column called `tax_amount` 
2. The actual `tax_assessments` table uses `annual_tax` instead
3. When SQLAlchemy tried to update the `properties` table (changing status to 'approved'), the trigger fired
4. The trigger's INSERT statement failed because `tax_amount` doesn't exist

## Solution Applied

### 1. Fixed the Database Trigger
**Dropped the old trigger:**
```sql
DROP TRIGGER IF EXISTS trg_auto_create_tax_assessment;
```

**Created corrected trigger** with proper column names matching the actual schema:
```sql
CREATE TRIGGER trg_auto_create_tax_assessment
AFTER UPDATE ON properties
FOR EACH ROW
BEGIN
    IF OLD.status != 'approved' AND NEW.status = 'approved' THEN
        INSERT INTO tax_assessments (
            property_id,
            assessment_year,
            assessment_date,
            assessed_value,
            tax_rate,
            annual_tax,        -- Corrected: was 'tax_amount'
            tax_paid,
            tax_due,
            due_date,
            status
        )
        VALUES (
            NEW.id,
            YEAR(CURDATE()),
            CURDATE(),
            COALESCE(NEW.market_value, NEW.govt_guidance_value, 100000),
            0.01,  -- 1% tax rate
            COALESCE(NEW.market_value, NEW.govt_guidance_value, 100000) * 0.01,
            0.0,
            COALESCE(NEW.market_value, NEW.govt_guidance_value, 100000) * 0.01,
            DATE_ADD(CURDATE(), INTERVAL 3 MONTH),
            'pending'
        );
    END IF;
END;
```

### 2. Improved Application Code (registrar.py)
Added `session.no_autoflush` blocks to prevent premature session flushing when querying owners:

**Before:**
```python
owners = property_obj.get_current_owners()
```

**After:**
```python
with db.session.no_autoflush:
    owners = property_obj.get_current_owners()
```

This prevents SQLAlchemy from auto-flushing pending changes (which would trigger the database trigger) during a query operation.

### 3. Cleared Python Cache
Removed all `__pycache__` directories to ensure no stale bytecode is used:
```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

## Files Modified
1. **Database**: `trg_auto_create_tax_assessment` trigger recreated
2. **app/routes/registrar.py**: Added no_autoflush blocks (lines 152-154, 175-177)
3. **fix_trigger.sql**: Created with corrected trigger definition

## Testing
After applying the fix:
1. Restart the Flask application
2. Login as registrar (registrar@lrms.com / password123)
3. Navigate to pending property registrations
4. Try to approve or reject a property
5. The operation should now complete successfully without errors

## Prevention
- Always ensure database triggers reference correct column names
- Use `SHOW TRIGGERS` to inspect trigger definitions
- When seeing SQLAlchemy flush errors, check for database-side operations (triggers, procedures)
- Consider using explicit transaction management when complex database operations are involved
