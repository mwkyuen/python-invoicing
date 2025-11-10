# Setup Frontend

Create the complete React/TypeScript frontend for the invoicing application:

1. **Project Setup**: Initialize Vite + React + TypeScript in `frontend/` directory:
   - `package.json` with dependencies (react, typescript, axios, react-hook-form)
   - `tsconfig.json` with strict type checking
   - `vite.config.ts` with proxy to backend (http://localhost:8000)

2. **Type Definitions** (in `src/types/`):
   - `Client.ts` - Client interface matching backend Pydantic model
   - `Invoice.ts` - Invoice and LineItem interfaces
   - `ApiResponse.ts` - Generic API response types

3. **API Client** (in `src/api/`):
   - `client.ts` - Axios instance with base configuration
   - `invoiceApi.ts` - Typed functions for all invoice endpoints
   - `clientApi.ts` - Typed functions for client endpoints

4. **Pages** (in `src/pages/` or `src/components/`):
   - `CreateClientPage.tsx` - Form to create new client (name, billing_address, email, phone_number)
   - `DashboardPage.tsx` - Display clients and invoices lists with tabs/sections
   - `CreateInvoicePage.tsx` - Form with client selector and dynamic line items
   - `UpdateInvoicePage.tsx` - Form to update invoice status

5. **Components** (in `src/components/`):
   - `ClientForm.tsx` - Client creation form component
   - `ClientList.tsx` - Display list of clients
   - `InvoiceForm.tsx` - Invoice creation form with client selector
   - `InvoiceList.tsx` - Display list of invoices
   - `InvoiceStatusForm.tsx` - Update invoice status component
   - `LineItemInput.tsx` - Reusable component for adding/editing line items
   - `ClientSelector.tsx` - Dropdown/autocomplete for selecting client
   - `InvoiceStatusBadge.tsx` - Display invoice status with color coding
   - `ErrorMessage.tsx` - Error display component
   - `LoadingSpinner.tsx` - Loading state component

6. **Form Features**:

   **Create Client Form**:
   - Fields: name, billing_address, email, phone_number
   - Validation: email format, required fields, phone format
   - Submit to `POST /api/clients`
   - Redirect to dashboard after success

   **Create Invoice Form**:
   - Client ID selector (dropdown populated from `GET /api/clients`)
   - Dynamic line items with add/remove buttons
   - Each line item: description, quantity, unit_price
   - Real-time total calculation display
   - Submit to `POST /api/invoices` with client_id and line_items array
   - Show generated invoice_number after success

   **Update Invoice Form**:
   - Invoice ID from URL params
   - Status dropdown (draft, sent, paid, cancelled)
   - Display current invoice details (read-only)
   - Submit to `PATCH /api/invoices/{id}`

   **Dashboard/List Views**:
   - Clients table: name, email, created date, actions
   - Invoices table: invoice_number, client name, total, status, date, actions
   - Actions: View (opens detail page), Edit status, Download PDF
   - Error handling for API failures

   **View Invoice Page** (`/invoices/:id`):
   - Display complete invoice details in browser (read-only view)
   - Show invoice header (number, date, status, total)
   - Show client information (name, email, phone, address)
   - Show line items table with quantities, prices, amounts
   - Back to Dashboard button only
   - No action buttons (all actions available from dashboard list)
   - Fetch from `GET /api/invoices/{id}` and `GET /api/clients/{id}`

7. **Post-Creation Success**:
   - After creating an invoice, show success message with invoice details
   - Provide buttons to: View Invoice, Back to Dashboard
   - No automatic redirect - let user choose next action
   - All actions (Edit Status, Download PDF) available from dashboard list

8. **Styling**: Use simple CSS or Tailwind CSS for clean, professional form layout.

Follow React/TypeScript best practices and ensure type safety throughout.
