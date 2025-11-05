# Test Users Summary

## Database Successfully Populated! ✅

All data has been saved to your MySQL database and is ready to view in MySQL Workbench.

---

## 5 New Test Users Created

**Password for ALL users: `1234`**

### 1. Rajesh Kumar
- **Email:** rajesh.kumar@example.com
- **Phone:** 9876543210
- **Address:** Plot 101, Sector 15, Pune, Maharashtra
- **Property ULPIN:** MH-PUNE-2024-001
- **Property Type:** Residential - Apartment
- **Location:** Koregaon Park, Pune
- **Area:** 1200 sqft
- **Mutation Type:** Sale
- **Mutation Number:** MUT-2024-1001
- **Mutation Status:** Pending (Ready for officer review)

---

### 2. Priya Sharma
- **Email:** priya.sharma@example.com
- **Phone:** 9876543211
- **Address:** House 202, Green Avenue, Mumbai, Maharashtra
- **Property ULPIN:** MH-MUM-2024-002
- **Property Type:** Residential - Independent House
- **Location:** Bandra West, Mumbai
- **Area:** 850 sqft
- **Mutation Type:** Inheritance
- **Mutation Number:** MUT-2024-1002
- **Mutation Status:** Pending (Ready for officer review)

---

### 3. Amit Patel
- **Email:** amit.patel@example.com
- **Phone:** 9876543212
- **Address:** Shop 303, Market Complex, Nagpur, Maharashtra
- **Property ULPIN:** MH-NAG-2024-003
- **Property Type:** Commercial - Shop
- **Location:** Sitabuldi, Nagpur
- **Area:** 500 sqft
- **Mutation Type:** Sale
- **Mutation Number:** MUT-2024-1003
- **Mutation Status:** Pending (Ready for officer review)

---

### 4. Sneha Desai
- **Email:** sneha.desai@example.com
- **Phone:** 9876543213
- **Address:** Villa 404, Palm Grove, Nashik, Maharashtra
- **Property ULPIN:** MH-NASH-2024-004
- **Property Type:** Residential - Villa
- **Location:** Gangapur Road, Nashik
- **Area:** 2500 sqft
- **Mutation Type:** Gift
- **Mutation Number:** MUT-2024-1004
- **Mutation Status:** Pending (Ready for officer review)

---

### 5. Vikram Mehta
- **Email:** vikram.mehta@example.com
- **Phone:** 9876543214
- **Address:** Farmhouse 505, Rural Area, Aurangabad, Maharashtra
- **Property ULPIN:** MH-AUR-2024-005
- **Property Type:** Agricultural - Farmhouse
- **Location:** Paithan Road, Aurangabad Rural
- **Area:** 5000 sqft
- **Mutation Type:** Partition
- **Mutation Number:** MUT-2024-1005
- **Mutation Status:** Pending (Ready for officer review)

---

## What Was Created

For each user, the following records were created in MySQL:

1. **User Account** - In `users` table
   - Role: citizen
   - Active and email verified
   - Password: 1234

2. **Owner Record** - In `owners` table
   - Linked to user account
   - Individual owner type

3. **Property Record** - In `properties` table
   - Status: Approved (so mutations can be requested)
   - Complete address and property details
   - Unique ULPIN for each property

4. **Ownership Record** - In `ownerships` table
   - 100% ownership
   - Sole ownership type
   - Active status

5. **Mutation Request** - In `mutations` table
   - Status: Pending (for officer to review)
   - Payment status: Pending
   - Priority: Normal
   - Different mutation types for variety

---

## How to View in MySQL Workbench

1. Open MySQL Workbench
2. Connect to your database (password: 1234)
3. Run these queries to see the data:

```sql
-- View all test users
SELECT * FROM users WHERE email LIKE '%@example.com';

-- View all properties
SELECT id, ulpin, property_type, locality, village_city FROM properties;

-- View all pending mutations (for officer review)
SELECT 
    m.mutation_number,
    m.mutation_type,
    m.status,
    u.full_name as requester,
    p.ulpin as property_ulpin
FROM mutations m
JOIN users u ON m.requester_id = u.id
JOIN properties p ON m.property_id = p.id
WHERE m.status = 'pending';

-- View complete data for a specific user (e.g., Rajesh Kumar)
SELECT 
    u.full_name,
    u.email,
    p.ulpin,
    p.property_type,
    p.locality,
    m.mutation_number,
    m.mutation_type,
    m.status
FROM users u
LEFT JOIN owners o ON u.id = o.user_id
LEFT JOIN ownerships os ON o.id = os.owner_id
LEFT JOIN properties p ON os.property_id = p.id
LEFT JOIN mutations m ON p.id = m.property_id
WHERE u.email = 'rajesh.kumar@example.com';
```

---

## Testing the Application

### As Citizen:
1. Login with any of the 5 test user emails
2. Password: `1234`
3. You can:
   - View your property
   - View your pending mutation request
   - Track mutation status

### As Officer:
1. Login with officer credentials
2. Navigate to "Pending Mutations" or "Review Mutations"
3. You will see all 5 pending mutation requests
4. You can approve, reject, or request more information

---

## Database Tables Updated

- ✅ `users` - 5 new citizen users added
- ✅ `owners` - 5 new owner records added
- ✅ `properties` - 5 new properties added (all approved)
- ✅ `ownerships` - 5 new ownership records added
- ✅ `mutations` - 5 new mutation requests added (all pending)

All data is now in your MySQL database with proper relationships and ready for testing!
