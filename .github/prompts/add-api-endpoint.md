# Add New API Endpoint

Add a new API endpoint following the project's FastAPI conventions:

**Endpoint Details**:
- Method: [GET/POST/PUT/DELETE]
- Path: `/api/[resource]/[action]`
- Description: [What this endpoint does]

**Implementation Steps** (Follow Clean Architecture layers):

1. **Define Domain Model** (if needed):
   - Create domain entity in `backend/app/domain/`
   - Use pure Python (dataclass or regular class)
   - Add business rules as methods (validation, calculations)
   - Example: `Client`, `Invoice`, `LineItem`

2. **Define Pydantic Models** (if needed):
   - Request model in `backend/app/models/` (e.g., `ClientCreateRequest`)
   - Response model in `backend/app/models/` (e.g., `ClientResponse`)
   - Add proper validation and type hints

3. **Update Database Schema** (if needed):
   - Add/modify SQLAlchemy model in `backend/app/schemas/`
   - Create Alembic migration or update init script

4. **Create DAO (Data Access Object)** in `backend/app/daos/`:
   - Implement database operations (CRUD)
   - Use SQLAlchemy for queries
   - Convert SQLAlchemy models ↔ Domain models
   - Return domain models (not SQLAlchemy models)
   - **NO business logic** - only data access and conversion

5. **Create Use-Case Function** in `backend/app/use_cases/`:
   - Implement business logic using domain models
   - Call DAO functions for data access
   - Work exclusively with domain models internally
   - Handle transactions (use database session)
   - Coordinate multiple DAOs if needed
   - Apply domain rules and validation
   - Return domain models
   - **NO HTTP concerns or Pydantic models**

6. **Add Route Handler** in `backend/app/routers/`:
   - Create FastAPI endpoint with proper HTTP method
   - Validate request with Pydantic models
   - Convert Pydantic request → domain model (if needed)
   - Call use-case function with domain models
   - Convert domain model → Pydantic response
   - Handle HTTP status codes and error responses
   - Include docstring with OpenAPI details
   - **NO business logic or database access**

7. **Write Tests** in `backend/tests/`:
   - Domain model tests: Test business rules and calculations
   - DAO tests: Test queries and conversions (use test database)
   - Use-Case tests: Mock DAOs, test business logic with domain models
   - Router tests: Use TestClient, test HTTP layer and conversions
   - Integration tests: Test full flow

8. **Update Frontend** (if needed):
   - Add TypeScript interface in `frontend/src/types/`
   - Add API function in `frontend/src/api/`
   - Update relevant components

**Layer Responsibilities**:
- **Domain**: Business entities and rules (pure Python)
- **Router**: HTTP + conversion Pydantic ↔ Domain
- **Use-Case**: Business logic with domain models
- **DAO**: Database + conversion SQLAlchemy ↔ Domain

**Conversion Flow**:
```
Pydantic (API) → Domain (Business) → SQLAlchemy (DB)
      ↑              ↑                    ↑
   Router      Use-Case                 DAO
```

Ensure each layer stays focused on its single responsibility.
