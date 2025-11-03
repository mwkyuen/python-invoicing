# Application Specification

> **📚 Related Docs**: [Copilot Instructions](copilot-instructions.md) · [Developer Onboarding](ONBOARDING.md) · [Prompt Templates](prompts/)

Complete API endpoints, workflows, and feature specifications for the Python Invoicing System.

**What's in this document**:
- 📋 **API Endpoints** - All REST endpoints with request/response schemas
- 🎨 **Frontend Pages** - All 4 pages with features and components
- 🗄️ **Database Schema** - Table definitions with SQL
- 🔄 **Workflows** - User flows for each feature
- ✅ **Business Rules** - Validation and business logic requirements

## 📋 Backend API Endpoints

### Client Endpoints
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/clients` | Create new client | `{name, billing_address, email, phone_number}` | `ClientResponse` with id |
| GET | `/api/clients` | List all clients | - | Array of `ClientResponse` |
| GET | `/api/clients/{id}` | Get single client | - | `ClientResponse` |

### Invoice Endpoints
| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/invoices` | Create invoice | `{client_id, line_items: [{description, quantity, unit_price}, ...]}` | `InvoiceResponse` with generated invoice_number |
| GET | `/api/invoices` | List all invoices | - | Array of `InvoiceResponse` with line items |
| GET | `/api/invoices/{id}` | Get single invoice | - | `InvoiceResponse` with line items |
| PATCH | `/api/invoices/{id}` | Update invoice status | `{status: "draft" \| "sent" \| "paid" \| "cancelled"}` | Updated `InvoiceResponse` |
| GET | `/api/invoices/{id}/pdf` | Download invoice PDF | - | PDF file |

## 🎨 Frontend Pages

### 1. Create Client Page
**Route**: `/clients/new`

**Features**:
- Form with fields:
  - Name (text, required)
  - Billing Address (textarea, required)
  - Email (email, required)
  - Phone Number (tel, required)
- Form validation
- Submit to `POST /api/clients`
- Show success message with client details
- Redirect to dashboard after success

**Components Used**:
- `ClientForm`
- `ErrorMessage`
- `LoadingSpinner`

---

### 2. Dashboard / List Page
**Route**: `/` or `/dashboard`

**Features**:
- Two sections or tabs:

**Clients Section**:
- Table displaying:
  - Name
  - Email
  - Phone Number
  - Created Date
  - Actions (View details)
- Fetch from `GET /api/clients`
- Link to "Create New Client" page

**Invoices Section**:
- Table displaying:
  - Invoice Number
  - Client Name (joined from client data)
  - Total Amount
  - Status (with color badge)
  - Issue Date
  - Actions (View, Edit Status, Download PDF)
- Fetch from `GET /api/invoices`
- Link to "Create New Invoice" page
- Filter by status (optional)

**Components Used**:
- `ClientList`
- `InvoiceList`
- `InvoiceStatusBadge`
- `LoadingSpinner`

---

### 3. Create Invoice Page
**Route**: `/invoices/new`

**Features**:
- Form with:

  **Client Selection**:
  - Client ID selector (dropdown or autocomplete)
  - Populated from `GET /api/clients`
  - Show client name and email

  **Line Items Section**:
  - Dynamic list of line items
  - Each row has:
    - Description (text, required)
    - Quantity (number, required, > 0)
    - Unit Price (number, required, ≥ 0)
    - Amount (calculated: quantity × unit_price, read-only)
  - "Add Line Item" button
  - "Remove" button for each row (except first)
  - Must have at least one line item

  **Total Display**:
  - Real-time calculation
  - Sum of all line item amounts
  - Displayed prominently

- Submit to `POST /api/invoices`
- Success state shows:
  - Generated invoice_number
  - Total amount
  - Link to download PDF
  - Link to view invoice details

**Components Used**:
- `InvoiceForm`
- `ClientSelector`
- `LineItemInput` (reusable for each row)
- `ErrorMessage`
- `LoadingSpinner`

---

### 4. Update Invoice Page
**Route**: `/invoices/:id/edit`

**Features**:
- Invoice ID from URL parameter
- Fetch invoice details from `GET /api/invoices/{id}`
- Display (read-only):
  - Invoice Number
  - Client Name
  - Total Amount
  - Issue Date
  - Current Status
  - Line Items (table)
- Form to update:
  - Status dropdown (draft, sent, paid, cancelled)
  - Submit button
- Submit to `PATCH /api/invoices/{id}`
- Show success message
- Redirect to dashboard or stay on page with updated data

**Components Used**:
- `InvoiceStatusForm`
- `InvoiceStatusBadge`
- `ErrorMessage`
- `LoadingSpinner`

---

## 🗄️ Database Schema

### clients table
```sql
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    billing_address TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### invoices table
```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,
    client_id INTEGER NOT NULL,
    issue_date TIMESTAMP NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    pdf_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

### line_items table
```sql
CREATE TABLE line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    quantity REAL NOT NULL,
    unit_price REAL NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);
```

## 🔄 Key Workflows

### Create Client Workflow
```
User fills form → Submit → POST /api/clients → Client created
                                              ↓
                                    Redirect to dashboard
```

### Create Invoice Workflow
```
User selects client → Adds line items → Reviews total → Submit
                                                         ↓
                                        POST /api/invoices (client_id + line_items)
                                                         ↓
                        Backend: Validate → Generate invoice_number → Save → Generate PDF
                                                         ↓
                                    Return invoice with invoice_number
                                                         ↓
                                    Display success with PDF download link
```

### Update Invoice Status Workflow
```
User navigates to /invoices/{id}/edit → Fetch invoice details
                                                ↓
                                    User selects new status → Submit
                                                ↓
                                    PATCH /api/invoices/{id}
                                                ↓
                                    Backend: Validate → Update status
                                                ↓
                                    Return updated invoice
                                                ↓
                                    Show success message
```

### List & View Workflow
```
User visits dashboard → Fetch clients (GET /api/clients)
                       → Fetch invoices (GET /api/invoices)
                                                ↓
                                    Display both lists in tabs/sections
                                                ↓
                        User can: Create new, View details, Edit status, Download PDF
```

## 📦 Domain Models

This application uses **domain models** - pure Python business entities with automatic calculations and validation.

**Key Domain Models**:
- **Client** - Customer with name, billing_address, email, phone_number
- **Invoice** - Invoice with auto-calculated total_amount from line_items
- **LineItem** - Line item with auto-calculated amount (quantity × unit_price)

**Important**: `total_amount` and `amount` are **calculated properties** - never set manually!

For complete domain model code examples with validation methods, see [ONBOARDING.md](ONBOARDING.md#-domain-models-the-heart-of-the-system).

## ✅ Business Rules

1. **Invoice Number**: Auto-generated, sequential, unique (e.g., INV-2025-0001)
2. **Invoice Status**: Must be one of: draft, sent, paid, cancelled
3. **Line Items**: Invoice must have at least one line item
4. **Total Calculation**: Automatically calculated from line items (cannot be manually set)
5. **Client Validation**: Email must be valid format, phone must be valid format
6. **Amount Validation**: Quantity must be positive, unit_price must be non-negative
7. **PDF Generation**: Triggered on invoice creation, stored in backend

## 🚀 Development Order

1. **Backend First**:
   - Setup project structure (domain, models, schemas, DAOs, use-cases, routers)
   - Implement client endpoints (POST, GET list, GET single)
   - Implement invoice endpoints (POST, GET list, GET single, PATCH)
   - Add invoice number generation logic
   - Add PDF generation (basic template)
   - Write tests for each layer

2. **Frontend Second**:
   - Setup React + TypeScript + Router
   - Create API client with typed functions
   - Build Create Client page
   - Build Dashboard with lists
   - Build Create Invoice page with dynamic line items
   - Build Update Invoice page
   - Add error handling and loading states

3. **Integration**:
   - Test full workflows end-to-end
   - Fix CORS issues if any
   - Test PDF download
   - Add polish (styling, validation messages)

This specification provides everything needed to build the complete application!
