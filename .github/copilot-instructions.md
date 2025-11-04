# Python Invoicing System - AI Agent Instructions

> **📚 Related Docs**: [Developer Onboarding](ONBOARDING.md) · [API Spec](APPLICATION_SPEC.md) · [Prompt Templates](prompts/)

## Project Overview
Full-stack invoicing application with React/TypeScript frontend and FastAPI/Python backend. Users enter client details and itemized services through a form, then the system generates numbered PDF invoices stored in SQLite.

## Architecture

### Tech Stack
- **Backend**: Python 3.10, FastAPI, Pydantic, SQLite
- **Frontend**: React, TypeScript
- **PDF Generation**: Playwright (headless Chromium) with HTML templates
- **Database**: SQLite with simple schema design
- **Environment**: Conda (environment.yml)

### Project Structure
```
python-invoicing/
├── backend/
│   ├── app/
│   │   ├── domain/          # Domain models: Business entities (Client, Invoice, LineItem)
│   │   ├── models/          # Pydantic models: API request/response validation
│   │   ├── schemas/         # SQLAlchemy ORM models: Database tables
│   │   ├── routers/         # Routes layer: FastAPI route handlers (HTTP concerns)
│   │   ├── use_cases/       # Use-case layer: Business logic and orchestration
│   │   ├── daos/            # Data Access Objects: Database operations
│   │   ├── db.py            # Database connection and session management
│   │   └── pdf_generator.py # PDF generation with Playwright
│   ├── tests/               # Backend tests (pytest)
│   ├── environment.yml      # Conda environment definition
│   └── main.py              # FastAPI application entry point
├── frontend/
│   ├── src/
│   │   ├── components/      # React components (InvoiceForm, etc.)
│   │   ├── types/           # TypeScript interfaces
│   │   └── api/             # API client for backend calls
│   ├── package.json
│   └── tsconfig.json
└── invoices.db              # SQLite database (gitignored)
```

## Database Schema

Three core tables: **clients**, **invoices** (with status field), and **line_items**.

**Key Patterns**:
- Invoice number generation is atomic and sequential (use database transactions)
- Invoice status tracks lifecycle: "draft" → "sent" → "paid" or "cancelled"
- Total amounts are calculated automatically from line items

**See APPLICATION_SPEC.md for complete SQL table definitions.**

## API Endpoints

### Client Endpoints
- `POST /api/clients` - Create new client (name, billing_address, email, phone_number)
- `GET /api/clients` - List all clients (with pagination optional)
- `GET /api/clients/{id}` - Get single client details

### Invoice Endpoints
- `POST /api/invoices` - Create invoice (client_id, line_items array)
  - Line items: `[{description, quantity, unit_price}, ...]`
  - Auto-generates invoice_number
  - Calculates total_amount from line items
- `GET /api/invoices` - List all invoices (with filtering/pagination optional)
- `GET /api/invoices/{id}` - Get single invoice with line items
- `PATCH /api/invoices/{id}` - Update invoice status
- `GET /api/invoices/{id}/pdf` - Download invoice PDF

## Backend Development

### Domain Models (`app/domain/`)
Domain models represent core business entities independent of infrastructure:

- **Pure Python dataclasses or classes** (not SQLAlchemy, not Pydantic)
- Contain business logic and domain rules
- Used internally by use-cases for business operations
- Independent of database structure or API contracts
- Examples: `Client`, `Invoice`, `LineItem`

**Key Concepts**:
- Domain models are the "language" of the business logic
- They can have methods that enforce business rules (e.g., `validate()`)
- Calculated properties for automatic values (e.g., `total_amount`, `amount`)
- DAOs convert between SQLAlchemy models and domain models
- Use-cases work primarily with domain models

**For complete domain model code examples with validation and business logic, see `.github/ONBOARDING.md`.**

### Clean Architecture Layers
The backend follows a Clean Architecture-inspired layered approach with clear separation of concerns:

**1. Routes Layer** (`app/routers/`):
- Handle HTTP requests/responses (FastAPI route handlers)
- Validate input using Pydantic models
- Call use-case functions
- Transform use-case results into HTTP responses (Pydantic)
- Handle HTTP status codes and error responses
- **No business logic or database access**

**2. Use-Case Layer** (`app/use_cases/`):
- Implement business logic and orchestration
- Work with **domain models** for business operations
- Coordinate between multiple DAOs if needed
- Handle transactions and atomic operations
- Execute domain-specific workflows (e.g., invoice number generation, PDF creation)
- Return domain objects or raise domain exceptions
- **No HTTP concerns or direct database queries**

**3. Data Access Objects (DAOs)** (`app/daos/`):
- Encapsulate all database operations
- Use SQLAlchemy ORM for queries
- Convert between SQLAlchemy models and domain models
- Provide CRUD operations for each entity
- Return domain models (not SQLAlchemy models)
- **No business logic or HTTP concerns**

**4. Domain Models** (`app/domain/`):
- Pure Python business entities
- Contain business rules and validation
- Used by use-cases for business logic
- Independent of database and API layers

**Example Flow**:
```
HTTP Request (JSON)
    ↓
Router (Pydantic models) → validates → calls use-case
    ↓
Use-Case (Domain models) → business logic → calls DAO
    ↓
DAO (converts) → SQLAlchemy → Database
                    ↓
                Domain model ← converts ← SQLAlchemy model
                    ↓
Use-Case (Domain model) → processes → returns
    ↓
Router (converts) → Pydantic response → HTTP Response (JSON)
```

### Model Types and Their Purposes

**Pydantic Models** (`app/models/`):
- **Purpose**: API contract - request/response validation
- **Used by**: Routers for HTTP input/output
- **Examples**: `ClientCreate`, `InvoiceCreateRequest`, `InvoiceResponse`
- **Characteristics**: Validation rules, JSON serialization

**Domain Models** (`app/domain/`):
- **Purpose**: Business entities and rules
- **Used by**: Use-cases for business logic
- **Examples**: `Client`, `Invoice`, `LineItem`
- **Characteristics**: Business methods, domain validation, calculations

**SQLAlchemy Schemas** (`app/schemas/`):
- **Purpose**: Database mapping
- **Used by**: DAOs for persistence
- **Examples**: `ClientTable`, `InvoiceTable`, `LineItemTable`
- **Characteristics**: Column definitions, relationships, constraints

### FastAPI Conventions
- Use Pydantic models for request/response validation (e.g., `ClientCreate`, `InvoiceResponse`)
- Use domain models internally in use-cases (e.g., `Client`, `Invoice`)
- Use SQLAlchemy ORM models for database entities (in `schemas/`)
- Implement CORS middleware for frontend communication
- Organize routes by resource: `/api/clients`, `/api/invoices`

### Key Workflows

**Create Client Flow**:
1. Router: Validates client data (Pydantic)
2. Use-Case: Creates Client domain model, validates business rules
3. DAO: Converts to SQLAlchemy, saves to database
4. Router: Returns ClientResponse

**Create Invoice Flow**:
1. Router: Validates invoice request with line items array (Pydantic)
2. Use-Case:
   - Validates client exists
   - Creates Invoice domain model with LineItem list
   - Generates unique invoice_number
   - Calculates total_amount from line items
   - Sets initial status (e.g., "draft")
   - Triggers PDF generation
3. DAO: Saves invoice and line items atomically
4. Router: Returns InvoiceResponse with invoice_number

**Update Invoice Status Flow**:
1. Router: Validates status update request
2. Use-Case: Fetches invoice, updates status, validates state transition
3. DAO: Updates invoice record
4. Router: Returns updated InvoiceResponse

**List Operations**:
- Use-Case: Fetches all records via DAO
- DAO: Queries database, converts to domain models
- Router: Converts domain models to response list

### Testing
- Use `pytest`
- Use TestClient from `fastapi.testclient` for endpoint testing
- Mock database with in-memory SQLite for isolated tests

## Frontend Development

### Application Pages
The frontend consists of four main pages:

1. **Create Client Page** (`/clients/new`)
   - Form with fields: name, billing_address, email, phone_number
   - Submit creates client via `POST /api/clients`
   - Redirect to clients list after success

2. **Clients & Invoices List Page** (`/` or `/dashboard`)
   - Two sections/tabs:
     - **Clients List**: Display all clients (name, email, actions)
     - **Invoices List**: Display all invoices (invoice_number, client, total, status, actions)
   - Fetch from `GET /api/clients` and `GET /api/invoices`
   - Links to create new client/invoice
   - Actions: View details, Edit status, Download PDF

3. **Create Invoice Page** (`/invoices/new`)
   - Form with:
     - Client ID selector (dropdown or autocomplete from clients list)
     - Dynamic line items section (add/remove rows)
     - Each line item: description, quantity, unit_price
     - Real-time total calculation display
   - Submit creates invoice via `POST /api/invoices`
   - Display generated invoice_number after success

4. **Update Invoice Page** (`/invoices/:id/edit`)
   - Form with:
     - Invoice ID (from URL, read-only display)
     - Status dropdown (draft, sent, paid, cancelled)
   - Submit updates via `PATCH /api/invoices/{id}`
   - Show current invoice details for context

### React/TypeScript Patterns
- Use functional components with TypeScript interfaces for props
- Form validation before API submission (consider React Hook Form or similar)
- Type definitions should mirror backend Pydantic models
- Use React Router for page navigation
- Shared components: ClientSelector, LineItemInput, InvoiceStatusBadge

### API Integration
- Create typed API client in `frontend/src/api/` (e.g., `clientApi.ts`, `invoiceApi.ts`)
- Handle loading states and error messages from backend
- Implement proper error handling for 404, 400, 500 responses

## Development Workflow

### Running Locally
**Backend**:
```bash
cd backend
conda env create -f environment.yml  # First time only
conda activate invoicing
playwright install chromium          # First time only
uvicorn main:app --reload            # Runs on http://localhost:8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:5173
```

### Adding Features
1. Define API contract: Update Pydantic models and FastAPI routes
2. Implement backend layers: DAO (data access) → Use-Case (business logic) → Router (HTTP handling)
3. Create/update frontend components with TypeScript types
4. Test each layer: DAO tests → Use-Case tests → Router integration tests
5. Test end-to-end: Form submission → API → PDF generation → response handling

## Code Quality
- Backend: Use Ruff for linting/formatting Python code
- Frontend: Use ESLint + Prettier (standard React/TypeScript setup)
- Type safety: Leverage Pydantic (backend) and TypeScript (frontend) for compile-time checks

## Excluded from Version Control
- `invoices.db` - SQLite database file
- `*.pdf` - Generated invoice PDFs (store in `backend/generated_invoices/` or similar)
- `backend/.venv/` - Python virtual environment
- `frontend/node_modules/` - Node dependencies
- `frontend/dist/` or `frontend/build/` - Built frontend assets
