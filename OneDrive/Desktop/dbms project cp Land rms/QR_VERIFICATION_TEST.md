# QR Code Verification System - Testing Guide

## Overview
The QR Code Verification system allows public (no login required) verification of:
1. **Mutation Certificates** - Verify ownership transfer certificates
2. **Properties** - Verify complete property details including history

## Testing the System

### 1. Certificate Verification

**URL Format:**
```
http://127.0.0.1:5000/verify/<certificate_number>
```

**Example URLs:**
```
http://127.0.0.1:5000/verify/MC2025000001
http://127.0.0.1:5000/verify/MC2025000234
```

**What It Shows:**
- Certificate validity badge (Valid/Invalid)
- Certificate number
- Property ULPIN and details
- Previous and new owner information
- Mutation type and status
- Application and approval dates
- Officer who approved
- QR code for mobile verification
- Timeline of the mutation process

**To Test:**
1. Log in as admin: http://127.0.0.1:5000/admin/login
2. Go to Mutations page: http://127.0.0.1:5000/admin/mutations
3. Find an approved mutation with a certificate number
4. Copy the certificate number (format: MC2025XXXXXX)
5. Open: http://127.0.0.1:5000/verify/MC2025XXXXXX
6. Verify all details are displayed correctly

### 2. Property Verification

**URL Format:**
```
http://127.0.0.1:5000/verify/property/<ulpin>
```

**Example URLs:**
```
http://127.0.0.1:5000/verify/property/MH-MUM-2020-00001
http://127.0.0.1:5000/verify/property/DL-NEW-2021-00456
```

**What It Shows:**
- Property validity badge (Valid/Invalid)
- Complete property details (ULPIN, type, address, area, value)
- Current owner information
- Complete ownership history (mutations)
- Payment history (last 10 transactions)
- QR code for mobile verification
- Visual timeline of all ownership changes

**To Test:**
1. Log in as admin: http://127.0.0.1:5000/admin/login
2. Go to Properties page: http://127.0.0.1:5000/admin/properties
3. Copy any property's ULPIN
4. Open: http://127.0.0.1:5000/verify/property/<ULPIN>
5. Verify complete property history is displayed

## Features

### 🎯 Key Features
- ✅ **No Login Required** - Public verification without authentication
- ✅ **QR Code Display** - Embedded QR codes for mobile scanning
- ✅ **Print Friendly** - Clean print layout (print button included)
- ✅ **Professional Design** - Gradient backgrounds, clean layout
- ✅ **Complete Information** - All relevant details in one page
- ✅ **Invalid Detection** - Clear error messages for invalid codes
- ✅ **Timeline View** - Visual timeline for mutations

### 🔒 Security
- Only public information is displayed
- No sensitive user data exposed
- Read-only verification (cannot modify data)
- Works without session/authentication

## QR Code Generation

The system automatically generates QR codes containing:
- For certificates: Verification URL with certificate number
- For properties: Verification URL with ULPIN

QR codes are base64-encoded PNG images displayed inline in the HTML.

## Integration Points

### Where to Add QR Codes in Existing Pages

#### 1. Citizen Dashboard - My Properties
File: `app/templates/citizen/properties.html`
Add QR code button next to each property that links to `/verify/property/<ulpin>`

#### 2. Citizen Dashboard - Mutation Details
File: `app/templates/citizen/mutation_detail.html`
Add QR code section showing the certificate QR when status is 'approved'

#### 3. Officer Dashboard - Approved Mutations
File: `app/templates/officer/my_approvals.html`
Add "Generate QR" button that shows the certificate verification QR code

#### 4. Admin Dashboard - Property Details
File: `app/templates/admin/property_detail.html`
Add QR code section at the top showing property verification QR

## Sample Test Data

To find test data in the database:

```sql
-- Find approved mutations with certificates
SELECT id, mutation_certificate_number, mutation_number, status 
FROM mutations 
WHERE status = 'approved' 
AND mutation_certificate_number IS NOT NULL 
LIMIT 10;

-- Find properties with ULPINs
SELECT id, ulpin, locality, district, property_type 
FROM properties 
LIMIT 10;
```

## Error Handling

### Invalid Certificate Number
- Shows "Invalid Certificate" badge in red
- Displays error message
- Provides link back to homepage

### Invalid ULPIN
- Shows "Invalid Property" badge in red
- Displays error message
- Provides link back to homepage

### Missing Data
- System handles null/missing fields gracefully
- Optional fields (remarks, approval dates) are conditionally displayed

## Next Steps

1. ✅ **QR Verification System** - COMPLETED
2. ⏳ **Integrate QR display in existing pages** - Add QR code buttons/sections
3. ⏳ **Export to PDF with QR codes** - Add QR codes to PDF certificates
4. ⏳ **Email notifications with QR codes** - Include QR in notification emails

## Files Modified

### New Files
- `app/routes/public.py` - Public verification routes (no auth)
- `app/templates/public/verify_certificate.html` - Certificate verification page
- `app/templates/public/verify_property.html` - Property verification page  
- `app/utils/qr_code_generator.py` - QR code generation utilities

### Modified Files
- `app/__init__.py` - Registered public blueprint
- `app/routes/__init__.py` - Added public blueprint import
- `app/models/mutation.py` - Added owner relationships and fields

## Dependencies
- `qrcode[pil]` - QR code generation
- `pillow` - Image processing

Both packages are already installed and working.
