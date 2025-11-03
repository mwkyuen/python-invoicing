# Setup Backend

Create the complete backend structure for this FastAPI invoicing application:

1. **Project Structure** (Clean Architecture Layers): Create `backend/` directory with:
   - `main.py` - FastAPI app with CORS middleware
   - `app/db.py` - SQLAlchemy setup with SQLite connection
   - `app/domain/` - Domain models: Pure Python business entities
   - `app/models/` - Pydantic models for API request/response validation
   - `app/schemas/` - SQLAlchemy ORM models for database tables
   - `app/routers/` - Routes layer: HTTP request/response handling
   - `app/use_cases/` - Use-case layer: Business logic and orchestration
   - `app/daos/` - Data Access Objects: Database operations
   - `requirements.txt` - Dependencies list

2. **Domain Models** (in `app/domain/`) - Pure Python entities:
   - `Client` - Business entity with validation methods
   - `Invoice` - Business entity with total calculation and validation
   - `LineItem` - Business entity with amount calculation
   - Use dataclasses or regular classes (NOT SQLAlchemy or Pydantic)
   - Include business rules and domain logic as methods

3. **SQLAlchemy Schemas** (in `app/schemas/`) - Database tables:
   - `ClientTable` - name, billing_address, email, phone_number, created_at
   - `InvoiceTable` - invoice_number, client_id, issue_date, total_amount, status, pdf_path, created_at
   - `LineItemTable` - invoice_id, description, quantity, unit_price, amount
   - Include relationships: Invoice → Client (many-to-one), LineItem → Invoice (many-to-one)

4. **Pydantic Models** (in `app/models/`) - API contracts:
   - Request models: `ClientCreateRequest`, `InvoiceCreateRequest`, `LineItemCreateRequest`
   - Response models: `ClientResponse`, `InvoiceResponse`, `LineItemResponse`

5. **Data Access Objects** (in `app/daos/`):
   - `ClientDAO` - create, get_by_id, get_all, convert SQLAlchemy ↔ Domain
   - `InvoiceDAO` - create, get_by_id, get_all, update_status, generate_next_invoice_number, convert SQLAlchemy ↔ Domain
   - `LineItemDAO` - create, get_by_invoice_id, convert SQLAlchemy ↔ Domain
   - Each DAO returns domain models (not SQLAlchemy models)
   - Include conversion methods: `_to_domain()` and `_from_domain()`

6. **Use-Cases** (in `app/use_cases/`):
   - `create_client_use_case.py` - Validate and create client
   - `list_clients_use_case.py` - Retrieve all clients
   - `create_invoice_use_case.py` - Generate invoice number, create invoice + line items, trigger PDF
   - `list_invoices_use_case.py` - Retrieve all invoices with line items
   - `get_invoice_use_case.py` - Retrieve single invoice with details
   - `update_invoice_status_use_case.py` - Update invoice status with validation
   - Business logic uses domain models exclusively
   - No SQLAlchemy or Pydantic models in use-case logic

7. **API Routes** (in `app/routers/`):

   **Client Routes** (`app/routers/clients.py`):
   - `POST /api/clients` - Create client (name, billing_address, email, phone_number)
   - `GET /api/clients` - List all clients
   - `GET /api/clients/{id}` - Get single client

   **Invoice Routes** (`app/routers/invoices.py`):
   - `POST /api/invoices` - Create invoice (client_id, line_items array)
     - Line items: `[{description, quantity, unit_price}, ...]`
     - Auto-generates invoice_number and calculates total_amount
   - `GET /api/invoices` - List all invoices (with line items)
   - `GET /api/invoices/{id}` - Get single invoice with line items
   - `PATCH /api/invoices/{id}` - Update invoice status
   - `GET /api/invoices/{id}/pdf` - Download invoice PDF

   All routes convert between Pydantic (API) and domain models

8. **Key Features**:
   - Domain models contain business rules (validation, calculations)
   - Use-cases work exclusively with domain models
   - DAOs handle conversion between SQLAlchemy and domain models
   - Routers handle conversion between Pydantic and domain models
   - Database initialization script

**Architecture Flow**:
```
HTTP Request (JSON)
    ↓
Router (Pydantic) → validates input
    ↓
Use-Case (Domain) → business logic
    ↓
DAO → converts Domain ↔ SQLAlchemy
    ↓
Database

Return path:
SQLAlchemy → DAO converts → Domain → Use-Case → Router converts → Pydantic (JSON)
```

Include all necessary imports and follow the project conventions from copilot-instructions.md.
