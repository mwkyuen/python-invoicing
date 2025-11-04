# Features Documentation

This document describes all features implemented in the Python Invoicing System.

## Table of Contents
- [Core Features](#core-features)
- [Delete Functionality](#delete-functionality)
- [Client Deletion Validation](#client-deletion-validation)
- [Duplicate Email Prevention](#duplicate-email-prevention)
- [Invoice Viewing](#invoice-viewing)
- [PDF Cache Management](#pdf-cache-management)

---

## Core Features

### Client Management
- **Create Clients**: Add new clients with name, billing address, email, and phone number
- **List Clients**: View all clients in a searchable table
- **View Client Details**: See complete client information
- **Delete Clients**: Remove clients (with validation - see below)
- **Duplicate Prevention**: Email addresses must be unique across clients

### Invoice Management
- **Create Invoices**: Generate invoices with multiple line items
- **Auto-numbering**: Sequential invoice numbers (INV-2025-0001, INV-2025-0002, etc.)
- **Status Tracking**: Draft → Sent → Paid or Cancelled
- **Auto-calculation**: Total amounts calculated automatically from line items
- **PDF Generation**: Automatic PDF creation using Playwright + HTML templates
- **Delete Invoices**: Remove invoices with cascade deletion of line items

### Dashboard
- **Tabbed Interface**: Separate tabs for Clients and Invoices
- **Action Buttons**: View, Edit Status, Download PDF for each invoice
- **Delete Column**: Separate column with icon-only delete buttons
- **Status Badges**: Color-coded invoice status indicators
- **Client Details**: Mailing address display in clients table

---

## Delete Functionality

### Overview
Full CRUD operations with delete capability for both clients and invoices, following Clean Architecture patterns.

### Implementation

#### Backend (Clean Architecture Layers)

**1. DAO Layer** (`app/daos/`)
- `ClientDAO.delete(client_id)` - Deletes client from database
- `InvoiceDAO.delete(invoice_id)` - Cascade deletes line items, then invoice
- Returns `True` if deleted, `False` if not found

**2. Use-Case Layer** (`app/use_cases/`)
- `delete_client_use_case.execute(db, client_id)` - Business logic for client deletion
- `delete_invoice_use_case.execute(db, invoice_id)` - Business logic for invoice deletion
- Validates IDs are positive integers
- Calls DAO to perform deletion

**3. Router Layer** (`app/routers/`)
- `DELETE /api/clients/{client_id}` - HTTP endpoint for client deletion
- `DELETE /api/invoices/{invoice_id}` - HTTP endpoint for invoice deletion
- Returns 204 No Content on success
- Returns 404 if not found
- Returns 400 for validation errors

#### Frontend

**API Clients** (`src/api/`)
- `clientApi.deleteClient(id)` - Calls DELETE endpoint
- `invoiceApi.deleteInvoice(id)` - Calls DELETE endpoint

**UI Components** (`src/pages/DashboardPage.tsx`)
- Delete column with trashcan icon (🗑️)
- Confirmation dialog before deletion
- Automatic refresh after successful deletion
- Error message display for failed deletions

### User Experience

**Delete Flow**:
1. User clicks delete button (🗑️) in Delete column
2. Browser confirmation dialog appears:
   - "Are you sure you want to delete invoice INV-2025-0001?"
   - "Are you sure you want to delete client John Doe?"
3. User confirms → Item deleted, dashboard refreshes
4. User cancels → No action taken

**UI Design**:
- Separate "Delete" column for visual distinction
- Red button color (#e74c3c) signals danger
- Icon-only button for space efficiency
- Tooltip on hover: "Delete Invoice" / "Delete Client"

---

## Client Deletion Validation

### Business Rule
**"A client cannot be deleted if they have any associated invoices."**

This prevents orphaned invoices and maintains referential integrity.

### Implementation

**Invoice Check** (`app/daos/invoice_dao.py`):
```python
def has_invoices_for_client(self, client_id: int) -> bool:
    """Check if any invoices exist for a given client"""
    count = (
        self.db.query(InvoiceTable)
        .filter(InvoiceTable.client_id == client_id)
        .count()
    )
    return count > 0
```

**Validation Logic** (`app/use_cases/delete_client_use_case.py`):
```python
# Check if client has any invoices
invoice_dao = InvoiceDAO(db)
if invoice_dao.has_invoices_for_client(client_id):
    raise ValueError(
        "Cannot delete client with existing invoices. "
        "Please delete all invoices for this client first."
    )
```

### User Experience

**Scenario 1: Client Without Invoices**
```
User clicks delete → Confirmation → Client deleted ✅
```

**Scenario 2: Client With Invoices**
```
User clicks delete → Error message displayed:
"Cannot delete client with existing invoices. Please delete all invoices for this client first."
Client remains in system ✅
```

**Scenario 3: Delete Invoices First**
```
User deletes all invoices for client → Then deletes client → Success ✅
```

### Testing
Comprehensive test script validates:
- ✅ Clients without invoices can be deleted
- ✅ Clients with invoices cannot be deleted (error message shown)
- ✅ Client still exists after failed deletion attempt
- ✅ After deleting all invoices, client can be deleted

---

## Duplicate Email Prevention

### Business Rule
**"Email addresses must be unique across all clients."**

Email serves as the unique identifier for clients.

### Implementation

**Email Check** (`app/daos/client_dao.py`):
```python
def email_exists(self, email: str) -> bool:
    """Check if a client with the given email already exists"""
    count = (
        self.db.query(ClientTable)
        .filter(ClientTable.email == email)
        .count()
    )
    return count > 0
```

**Validation Logic** (`app/use_cases/create_client_use_case.py`):
```python
# Check for duplicate email
if client_dao.email_exists(email):
    raise ValueError(
        f"A client with email '{email}' already exists. "
        "Please use a different email address."
    )
```

**Error Handling** (already exists in router):
```python
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

### User Experience

**Scenario 1: Unique Email**
```
POST /api/clients {"email": "john@example.com", ...}
→ 201 Created ✅
```

**Scenario 2: Duplicate Email**
```
POST /api/clients {"email": "john@example.com", ...}
→ 400 Bad Request ❌
→ Error: "A client with email 'john@example.com' already exists. 
   Please use a different email address."
```

**Frontend Integration**:
- Error message displays below email field
- Form data preserved (no data loss)
- User can edit email and retry

### Technical Details

**Performance**: 
- Uses COUNT query (fast, efficient)
- No need to fetch full client records
- Indexed email column recommended for production

**Case Sensitivity**: 
- Currently case-sensitive
- "john@example.com" ≠ "John@Example.com"
- Both can exist (future enhancement: case-insensitive)

---

## Invoice Viewing

### Overview
Three action patterns for viewing and managing invoices from the dashboard.

### Dashboard Actions

**Action Buttons** (in Invoices table):

| Button | Icon | Color | Purpose |
|--------|------|-------|---------|
| **View** | 👁️ | Purple (#9b59b6) | Open read-only detail page |
| **Edit** | ✏️ | Blue (#3498db) | Update invoice status |
| **PDF** | 📥 | Green (#2ecc71) | Download invoice PDF |

### View Invoice Page

**Route**: `/invoices/:id`

**Features**:
- Read-only display of complete invoice details
- Invoice header: number, date, status badge, total
- Client information: name, email, phone, billing address
- Line items table: description, quantity, unit price, amount
- Total row at bottom
- "Back to Dashboard" button only

**Purpose**: Information display only - no actions on this page

### Dashboard-Centric Pattern

**Design Philosophy**: 
All actions (Edit Status, Download PDF) are performed from the dashboard list, not from individual invoice pages.

**User Flows**:
```
View Details:  Dashboard → Click 👁️ View → See details → Back to Dashboard
Edit Status:   Dashboard → Click ✏️ Edit → Change status → Back to Dashboard  
Download PDF:  Dashboard → Click 📥 PDF → File downloads → Stay on Dashboard
```

**Benefits**:
- Consistent action location (dashboard)
- Faster workflow (no page navigation for simple actions)
- Clear separation: View page = read-only, Dashboard = actions

---

## PDF Cache Management

### Problem
When invoice status is updated, the PDF is regenerated with the new status. However, browsers cache the PDF by URL, causing users to see the old version when downloading.

### Solution
Added HTTP cache-busting headers to force browsers to fetch fresh PDFs.

### Implementation

**Backend** (`app/routers/invoices.py`):
```python
@router.get("/{invoice_id}/pdf")
async def download_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    # ... fetch invoice and generate PDF ...
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
```

### How It Works

**HTTP Cache Headers**:
- `Cache-Control: no-cache, no-store, must-revalidate` - Tells browser not to cache
- `Pragma: no-cache` - HTTP/1.0 backward compatibility
- `Expires: 0` - Ensures cached version is always expired

**User Experience**:
1. User updates invoice status: Draft → Sent
2. PDF is regenerated with "SENT" status
3. User clicks "Download PDF"
4. Browser ignores cache, fetches fresh PDF
5. Downloaded PDF shows current "SENT" status ✅

**Before Fix**:
- Downloaded PDF showed old status (e.g., "DRAFT" instead of "SENT")
- User had to hard refresh or clear cache

**After Fix**:
- Downloaded PDF always shows current status
- No manual cache clearing needed

---

## Summary Table

| Feature | Status | Backend | Frontend | Validation |
|---------|--------|---------|----------|------------|
| **Client CRUD** | ✅ Complete | DAO + Use-Case + Router | API + UI | Email uniqueness |
| **Invoice CRUD** | ✅ Complete | DAO + Use-Case + Router | API + UI | Line items required |
| **Delete Operations** | ✅ Complete | Cascade deletion | Confirmation dialog | Client invoice check |
| **Email Uniqueness** | ✅ Complete | Database COUNT query | Error display | None |
| **PDF Generation** | ✅ Complete | Playwright + HTML | Download button | None |
| **PDF Cache Fix** | ✅ Complete | HTTP headers | None | None |
| **Dashboard UI** | ✅ Complete | N/A | Tabbed interface | None |
| **Invoice Viewing** | ✅ Complete | Get endpoints | Read-only page | None |

---

## Future Enhancements

### Potential Features
- **Soft Delete**: Archive instead of permanent deletion
- **Bulk Operations**: Delete multiple items at once
- **Search & Filter**: Find clients/invoices quickly
- **Email Notifications**: Send invoice PDFs via email
- **Payment Tracking**: Record payment dates and amounts
- **Recurring Invoices**: Automatically generate monthly invoices
- **Multi-currency Support**: Handle different currencies
- **Client Portal**: Let clients view their own invoices
- **Reports & Analytics**: Revenue tracking, client summaries
- **Audit Trail**: Log all deletions and modifications

### Technical Improvements
- **Case-insensitive Email**: Normalize emails to lowercase
- **Database Indexes**: Add indexes on frequently queried columns
- **API Rate Limiting**: Prevent abuse
- **Pagination**: Handle large datasets efficiently
- **Caching Strategy**: Redis for frequently accessed data
- **Background Jobs**: Async PDF generation for large invoices
- **File Storage**: S3/CloudStorage instead of local filesystem
- **Backup System**: Automated database backups

---

*Last Updated: November 4, 2025*
