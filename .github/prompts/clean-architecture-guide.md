# Clean Architecture Implementation Guide

This project follows Clean Architecture principles with domain models at the core and three distinct layers. **ALWAYS** implement features following this pattern.

## Domain Models (`app/domain/`)

**Purpose**: Pure business entities independent of infrastructure

**Characteristics**:
- ✅ Pure Python (dataclasses or regular classes)
- ✅ Business rules and validation as methods
- ✅ Domain calculations (e.g., total amount)
- ✅ No dependencies on frameworks (no SQLAlchemy, no Pydantic, no FastAPI)
- ✅ Used internally by use-cases for all business logic

**Example**:
```python
# app/domain/client.py
from dataclasses import dataclass
import re

@dataclass
class Client:
    name: str
    billing_address: str
    email: str
    phone_number: str
    id: int | None = None

    def validate(self):
        """Domain validation rules"""
        if not self.name or len(self.name) < 2:
            raise ValueError("Client name must be at least 2 characters")

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

    @property
    def display_name(self) -> str:
        """Domain logic"""
        return self.name.upper()
```

## Layer Responsibilities

### 1. Routes Layer (`app/routers/`)
**Purpose**: Handle HTTP concerns only

**Responsibilities**:
- ✅ Receive HTTP requests
- ✅ Validate input with Pydantic models
- ✅ Convert Pydantic → Domain models (for use-case input)
- ✅ Call use-case functions with domain models
- ✅ Convert Domain → Pydantic models (for HTTP response)
- ✅ Set HTTP status codes
- ✅ Handle HTTP-specific errors (404, 400, etc.)

**NOT Allowed**:
- ❌ Business logic
- ❌ Direct database access
- ❌ Calling DAOs directly
- ❌ Domain rules or calculations

**Example**:
```python
# app/routers/invoices.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import InvoiceCreateRequest, InvoiceResponse
from app.use_cases import create_invoice_use_case
from app.domain import Invoice

router = APIRouter()

@router.post("/api/invoices", response_model=InvoiceResponse, status_code=201)
def create_invoice(request: InvoiceCreateRequest, db: Session = Depends(get_db)):
    """Route handler - HTTP concerns + Pydantic ↔ Domain conversion"""
    try:
        # Convert Pydantic → Domain (if needed, or pass directly to use-case)
        # Use-case returns domain model
        domain_invoice = create_invoice_use_case.execute(db, request)

        # Convert Domain → Pydantic response
        return InvoiceResponse(
            id=domain_invoice.id,
            invoice_number=domain_invoice.invoice_number,
            total_amount=domain_invoice.total_amount,
            # ... other fields
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 2. Use-Case Layer (`app/use_cases/`)
**Purpose**: Implement business logic and orchestration

**Responsibilities**:
- ✅ Work exclusively with domain models
- ✅ Business rules and domain logic
- ✅ Orchestrate multiple DAO calls
- ✅ Manage transactions
- ✅ Coordinate workflows (e.g., create invoice → generate number → create PDF)
- ✅ Call domain model validation methods
- ✅ Return domain models
- ✅ Raise domain exceptions

**NOT Allowed**:
- ❌ HTTP status codes or responses
- ❌ Direct SQL queries (use DAOs)
- ❌ Pydantic request/response models
- ❌ SQLAlchemy models (use domain models)
- ❌ FastAPI dependencies

**Example**:
```python
# app/use_cases/create_invoice_use_case.py
from app.daos import InvoiceDAO, ClientDAO, LineItemDAO
from app.domain import Invoice, LineItem, Client
from datetime import datetime

def execute(db: Session, client_id: int, items: list) -> Invoice:
    """Use-case - business logic with domain models"""
    client_dao = ClientDAO(db)
    invoice_dao = InvoiceDAO(db)
    line_item_dao = LineItemDAO(db)

    # Get domain model from DAO
    client: Client = client_dao.get_by_id(client_id)
    if not client:
        raise ValueError("Client not found")

    # Create domain models
    line_items = [
        LineItem(description=item['desc'], quantity=item['qty'], unit_price=item['price'])
        for item in items
    ]

    # Create invoice domain model
    invoice = Invoice(
        invoice_number="",  # Will be generated
        client_id=client_id,
        issue_date=datetime.now(),
        line_items=line_items
    )

    # Domain validation
    invoice.validate()  # Business rules in domain model

    # Generate invoice number (business logic)
    invoice.invoice_number = invoice_dao.generate_next_invoice_number()

    # Orchestrate multiple operations in transaction
    try:
        # DAO persists and returns domain model
        saved_invoice = invoice_dao.create(invoice)

        for line_item in line_items:
            line_item_dao.create(saved_invoice.id, line_item)

        db.commit()

        # Trigger PDF generation (domain logic)
        generate_invoice_pdf(saved_invoice)

        return saved_invoice
    except Exception as e:
        db.rollback()
        raise
```

### 3. Data Access Objects Layer (`app/daos/`)
**Purpose**: Encapsulate database operations and convert between SQLAlchemy ↔ Domain models

**Responsibilities**:
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ SQL queries via SQLAlchemy ORM
- ✅ Convert SQLAlchemy models → Domain models
- ✅ Convert Domain models → SQLAlchemy models
- ✅ Return domain models (not SQLAlchemy models)
- ✅ Simple data filtering and ordering

**NOT Allowed**:
- ❌ Business logic or rules
- ❌ Calling other DAOs
- ❌ Transaction management (handled by use-cases)
- ❌ Domain calculations or validation

**Example**:
```python
# app/daos/invoice_dao.py
from sqlalchemy.orm import Session
from app.schemas import InvoiceTable, LineItemTable
from app.domain import Invoice, LineItem
from datetime import datetime

class InvoiceDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, invoice: Invoice) -> Invoice:
        """DAO - database operations + conversion"""
        # Convert Domain → SQLAlchemy
        db_invoice = InvoiceTable(
            invoice_number=invoice.invoice_number,
            client_id=invoice.client_id,
            issue_date=invoice.issue_date,
            total_amount=invoice.total_amount,
            pdf_path=invoice.pdf_path
        )
        self.db.add(db_invoice)
        self.db.flush()  # Don't commit - let use-case handle transaction

        # Convert SQLAlchemy → Domain
        return self._to_domain(db_invoice)

    def get_by_id(self, invoice_id: int) -> Invoice | None:
        """Query and convert to domain model"""
        db_invoice = self.db.query(InvoiceTable).filter(InvoiceTable.id == invoice_id).first()
        return self._to_domain(db_invoice) if db_invoice else None

    def _to_domain(self, db_invoice: InvoiceTable) -> Invoice:
        """Convert SQLAlchemy → Domain"""
        # Get line items if needed
        db_line_items = self.db.query(LineItemTable).filter(
            LineItemTable.invoice_id == db_invoice.id
        ).all()

        line_items = [
            LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            for item in db_line_items
        ]

        return Invoice(
            invoice_number=db_invoice.invoice_number,
            client_id=db_invoice.client_id,
            issue_date=db_invoice.issue_date,
            line_items=line_items,
            pdf_path=db_invoice.pdf_path
        )

    def generate_next_invoice_number(self) -> str:
        """Simple query - format generation"""
        last_invoice = self.db.query(InvoiceTable).order_by(InvoiceTable.id.desc()).first()
        next_num = 1 if not last_invoice else int(last_invoice.invoice_number.split("-")[-1]) + 1
        return f"INV-{datetime.now().year}-{next_num:04d}"
```

## Data Flow Pattern

```
HTTP Request (JSON)
    ↓
┌─────────────────────┐
│   Router Layer      │  - Validate HTTP input (Pydantic)
│  (HTTP Concerns)    │  - Convert Pydantic → Domain
│                     │  - Call use-case with domain models
│                     │  - Convert Domain → Pydantic response
└─────────────────────┘
    ↓ Domain Models
┌─────────────────────┐
│  Use-Case Layer     │  - Work with domain models
│ (Business Logic)    │  - Apply business rules
│                     │  - Coordinate DAOs
│                     │  - Manage transactions
└─────────────────────┘
    ↓ Domain Models
┌─────────────────────┐
│    DAO Layer        │  - Convert Domain → SQLAlchemy
│ (Data Access)       │  - Execute SQL queries
│                     │  - Convert SQLAlchemy → Domain
└─────────────────────┘
    ↓ SQLAlchemy
  Database

Model Types at Each Layer:
Router:      Pydantic ↔ Domain
Use-Case:    Domain only
DAO:         Domain ↔ SQLAlchemy
Database:    SQLAlchemy (ORM) → SQL
```

## Testing Strategy

Each layer is tested independently:

1. **DAO Tests**: Real database (test DB), no mocks
2. **Use-Case Tests**: Mock DAOs, test business logic
3. **Router Tests**: Mock use-cases, test HTTP layer
4. **Integration Tests**: No mocks, test full flow

## Common Mistakes to Avoid

❌ **Router calling DAO directly**
```python
# WRONG - Router bypassing use-case
@router.post("/api/invoices")
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    dao = InvoiceDAO(db)
    return dao.create(...)  # Missing business logic!
```

✅ **Correct - Router calls use-case**
```python
# CORRECT - Proper layer separation
@router.post("/api/invoices")
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    result = create_invoice_use_case.execute(db, data)
    return InvoiceResponse.from_orm(result)
```

❌ **DAO containing business logic**
```python
# WRONG - DAO should not have business rules
class InvoiceDAO:
    def create(self, data):
        if data.total_amount < 0:  # Business rule in DAO!
            raise ValueError("Invalid amount")
        ...
```

✅ **Correct - Business logic in use-case**
```python
# CORRECT - Use-case handles business rules
def create_invoice_use_case(db, data):
    if data.total_amount < 0:  # Business rule in use-case
        raise ValueError("Invalid amount")

    dao = InvoiceDAO(db)
    return dao.create(...)
```

## Model Conversions

| Location | Input Model | Output Model | Purpose |
|----------|------------|--------------|---------|
| Router | Pydantic (Request) | Domain | Prepare for use-case |
| Router | Domain | Pydantic (Response) | HTTP response |
| Use-Case | Domain | Domain | Business logic |
| DAO | Domain | SQLAlchemy | Save to database |
| DAO | SQLAlchemy | Domain | Return from database |

## Quick Reference

| Concern | Layer | Model Type |
|---------|-------|------------|
| HTTP status codes | Router | - |
| Pydantic validation | Router | Pydantic |
| Pydantic ↔ Domain conversion | Router | Both |
| Business rules | Use-Case | Domain |
| Domain validation | Use-Case | Domain |
| Transaction management | Use-Case | - |
| Multi-DAO coordination | Use-Case | Domain |
| Domain ↔ SQLAlchemy conversion | DAO | Both |
| SQL queries | DAO | SQLAlchemy |
| CRUD operations | DAO | SQLAlchemy |
| Error formatting | Router | - |
| Domain exceptions | Use-Case | - |
| Database commits | Use-Case | - |

**Remember**:
- Domain models are the core - pure Python with business logic
- Use-cases work exclusively with domain models
- Conversions happen at boundaries (Router and DAO)
