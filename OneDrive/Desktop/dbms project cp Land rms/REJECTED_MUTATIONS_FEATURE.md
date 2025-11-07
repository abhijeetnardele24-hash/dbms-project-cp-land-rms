# Rejected Mutations Feature ✅

## Overview
The "Rejected" card on the officer dashboard is now fully clickable and functional, displaying all mutations that have been rejected by the logged-in officer.

---

## ✨ What Was Implemented

### 1. **Clickable Rejected Card**
- The "Rejected" statistics card on the officer dashboard now has a clickable link
- Clicking it navigates to `/officer/rejected` route
- Card displays the total count of rejected mutations by the current officer

### 2. **New Route: `/officer/rejected`**
- **URL Function**: `officer.rejected_mutations`
- **Access**: Officers only (with `@officer_required` decorator)
- **Functionality**: 
  - Shows all mutations rejected by the logged-in officer
  - Filtered by `processed_by=current_user.id` and `status='rejected'`
  - Ordered by rejection date (most recent first)
  - Pagination: 50 items per page

### 3. **Professional Rejected Mutations Page**
Template: `app/templates/officer/rejected_mutations.html`

**Features:**
- ✅ **Comprehensive Table View** with columns:
  - Mutation Number
  - Type (transfer, inheritance, etc.)
  - Property ULPIN (clickable link)
  - Requester name
  - Submitted date
  - **Rejection date** (highlighted in red)
  - **Rejection reason** (truncated to 50 chars with "...")
  - View Details button

- ✅ **Pagination Support**
  - Shows 50 mutations per page
  - Full pagination controls (Previous/Next, page numbers)
  - Shows current page and total pages

- ✅ **Statistics Summary Card** (below the table):
  - Total Rejections count
  - Last Rejection date
  - Total Pages count
  - Visual icons for each metric

- ✅ **Empty State Handling**:
  - When no rejections exist, shows positive message
  - Provides link to review pending mutations
  - "You haven't rejected any mutations yet. This is a good sign!"

### 4. **Quick Actions Integration**
- Added "Rejected Mutations" button to Quick Actions sidebar
- Button style: Red outline (`btn-outline-danger`)
- Icon: `fa-times-circle`
- Position: Between "My Approval History" and "View All Properties"

---

## 🎨 Visual Design

### Color Scheme
- **Card Gradient**: Pink to yellow (#fa709a → #fee140)
- **Header Background**: Danger red (`bg-danger`)
- **Rejection Date**: Bold red text
- **Button Style**: Red outline (`btn-outline-danger`)

### User Experience
- Hover effect on dashboard card (lifts up with shadow)
- Responsive table layout
- Color-coded badges for mutation types
- Truncated rejection reasons with ellipsis (...)
- Empty state with encouraging message

---

## 📊 Data Display

### Table Columns:
1. **Mutation Number**: Bold, unique identifier
2. **Type**: Badge with mutation type (transfer, inheritance, etc.)
3. **Property ULPIN**: Clickable link to property details
4. **Requester**: Full name of the person who submitted
5. **Submitted Date**: When mutation was originally created
6. **Rejection Date**: When you rejected it (highlighted in red)
7. **Rejection Reason**: Shows `rejection_reason` or `officer_comments` (first 50 chars)
8. **Actions**: "View Details" button to see full mutation info

### Summary Statistics:
- **Total Rejections**: Count of all rejected mutations by officer
- **Last Rejection**: Month/Year of most recent rejection
- **Total Pages**: Number of pagination pages

---

## 🔧 Technical Implementation

### Files Modified:

1. **`app/templates/officer/dashboard.html`**
   - Line 98: Wrapped rejected card in clickable link
   - Line 183-185: Added "Rejected Mutations" to Quick Actions

2. **`app/routes/officer.py`**
   - Lines 184-199: Added `rejected_mutations()` route function
   - Query filters: `processed_by=current_user.id, status='rejected'`
   - Order by: `rejection_date.desc()`
   - Pagination: 50 per page

3. **`app/templates/officer/rejected_mutations.html`** (NEW FILE)
   - 197 lines of professional HTML/Jinja2 template
   - Responsive table layout
   - Pagination controls
   - Statistics summary card
   - Empty state handling

---

## 🚀 How to Use

### For Officers:

1. **Login** to your officer account
2. **Dashboard**: See the "Rejected" card (4th card, orange gradient)
3. **Click the card** OR **Click "Rejected Mutations" in Quick Actions**
4. **View all rejected mutations** in a detailed table
5. **Click "View Details"** to see full mutation information
6. **Navigate pages** if you have more than 50 rejections

### Data Shown:
- Only mutations **YOU** rejected (filtered by your user ID)
- Sorted by most recent rejection first
- Full details including rejection reason/comments
- Links to property details for context

---

## 📋 Navigation Flow

```
Officer Dashboard
    │
    ├─► Rejected Card (Click) → Rejected Mutations Page
    │                              │
    │                              ├─► View Details → Mutation Detail Page
    │                              └─► Property Link → Property Detail Page
    │
    └─► Quick Actions
        └─► Rejected Mutations (Click) → Rejected Mutations Page
```

---

## ✅ Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| Clickable Card | ✅ | Rejected card on dashboard is now clickable |
| Route Created | ✅ | `/officer/rejected` route implemented |
| Template Created | ✅ | Professional HTML page with table |
| Data Filtering | ✅ | Shows only current officer's rejections |
| Pagination | ✅ | 50 items per page with controls |
| Statistics | ✅ | Summary card with 3 key metrics |
| Empty State | ✅ | Friendly message when no rejections |
| Quick Actions | ✅ | Added to sidebar for easy access |
| Responsive Design | ✅ | Works on all screen sizes |
| Professional UI | ✅ | Color-coded, modern design |

---

## 🎯 Benefits

### For Officers:
1. **Track Performance**: See all mutations you've rejected
2. **Review History**: Access rejection reasons and dates
3. **Quality Control**: Review your rejection patterns
4. **Transparency**: Full audit trail of your decisions

### For Placement/Interviews:
1. **Complete CRUD**: Demonstrates read operations with filtering
2. **User-Specific Data**: Shows role-based access control
3. **Professional UI**: Modern, industry-standard design
4. **Pagination**: Handles large datasets efficiently
5. **Empty State Handling**: Good UX practices
6. **Data Relationships**: Shows joins between mutations, properties, users

---

## 🔄 All Officer Dashboard Cards Now Clickable

| Card | Status | Destination |
|------|--------|-------------|
| Pending Mutations | ✅ Clickable | `/officer/pending-mutations` |
| Under Review | ✅ Clickable | `/officer/under-review` |
| My Approvals | ✅ Clickable | `/officer/my-approvals` |
| Rejected | ✅ **NOW CLICKABLE** | `/officer/rejected` |

---

## 📝 Sample Data Display

If you have rejected mutations, you'll see:
```
┌──────────────────────────────────────────────────────────────┐
│ Mutation Number | Type     | Property ULPIN | Rejected On   │
├──────────────────────────────────────────────────────────────┤
│ MUT-2024-001   | Transfer | ULPIN-12345    | 2024-01-15    │
│ MUT-2024-002   | Sale     | ULPIN-67890    | 2024-01-14    │
└──────────────────────────────────────────────────────────────┘
```

If no rejections:
```
┌──────────────────────────────────────────────────────┐
│            ✓ No Rejected Mutations                   │
│   You haven't rejected any mutations yet.           │
│         This is a good sign!                         │
│                                                       │
│        [Review Pending Mutations]                    │
└──────────────────────────────────────────────────────┘
```

---

**Status**: ✅ Fully Implemented and Ready to Use!  
**Last Updated**: 2024  
**Route**: `/officer/rejected`  
**Access**: Officers Only 🔒
