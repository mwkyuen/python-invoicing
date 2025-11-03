# Python Invoicing System - Developer Onboarding

> **📚 Related Docs**: [Copilot Instructions](copilot-instructions.md) · [API Spec](APPLICATION_SPEC.md) · [Prompt Templates](prompts/)

Quick start guide for developers joining this project. Use `/explain` with sections of this document to understand the system.

**What's in this document**:
- 🎯 **Domain Models** - Core business entities with code examples
- 🔄 **Data Flow** - How models flow through the system
- 📂 **Project Structure** - Where everything lives
- 💡 **Common Tasks** - How to add features
- ❓ **FAQ** - Answers to common questions

## 🎯 Project Overview

**What is this?** A full-stack invoicing application where users create clients, generate invoices with line items, and track invoice status.

**Tech Stack**:
- **Backend**: FastAPI + SQLAlchemy + SQLite (Clean Architecture)
- **Frontend**: React + TypeScript
- **Architecture**: Domain-Driven Design with Clean Architecture layers

---

## 🏗️ Architecture at a Glance

```
Frontend (React)
      ↓ HTTP/JSON
Backend Layers:
┌─────────────────┐
│   Router        │  FastAPI endpoints (HTTP concerns)
│   (Pydantic)    │  Validates input, returns JSON
└────────┬────────┘
         │
┌────────▼────────┐
│   Use-Case      │  Business logic orchestration
│   (Domain)      │  Works with domain models
└────────┬────────┘
         │
┌────────▼────────┐
│   DAO           │  Database operations
│   (SQLAlchemy)  │  Converts Domain ↔ Database
└────────┬────────┘
         │
     Database
```

**Key Principle**: Domain models are the core. Everything else converts to/from domain models.

---

## 📦 Domain Models (The Heart of the System)

These are **pure Python classes** that represent your business entities. They contain business logic and are independent of frameworks.

### 1. Client Domain Model

**Location**: `backend/app/domain/client.py`

**Purpose**: Represents a customer/client in the system

```python
from dataclasses import dataclass
import re

@dataclass
class Client:
    """
    A client/customer who receives invoices.
    Pure Python - no database or API dependencies.
    """
    name: str
    billing_address: str
    email: str
    phone_number: str
    id: int | None = None

    def validate(self):
        """Business rule validation"""
        if not self.name or len(self.name) < 2:
            raise ValueError("Client name must be at least 2 characters")

        if not self.billing_address:
            raise ValueError("Billing address is required")

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

        # Phone validation
        phone_pattern = r'^\+?[\d\s\-()]+$'
        if not re.match(phone_pattern, self.phone_number):
            raise ValueError("Invalid phone number format")

    @property
    def display_name(self) -> str:
        """Business logic for display"""
        return self.name.upper()
```

**When to use**: Anytime you're working with client data in business logic (use-cases).

---

### 2. LineItem Domain Model

**Location**: `backend/app/domain/line_item.py`

**Purpose**: Represents a single service/product line on an invoice

```python
from dataclasses import dataclass

@dataclass
class LineItem:
    """
    A line item on an invoice with automatic amount calculation.
    Example: "10 hours of web development @ $150/hour = $1,500"
    """
    description: str      # "Web Development Services"
    quantity: float       # 10.0 (can be decimal for hours)
    unit_price: float     # 150.00
    id: int | None = None
    invoice_id: int | None = None

    @property
    def amount(self) -> float:
        """
        Automatically calculates the line item total.
        This is a computed property - never set manually!
        """
        return self.quantity * self.unit_price

    def validate(self):
        """Business rule validation"""
        if not self.description or len(self.description) < 3:
            raise ValueError("Description must be at least 3 characters")

        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
```

**Key Feature**: The `amount` property is **calculated automatically**. You never set it directly - it's always `quantity × unit_price`.

---

### 3. Invoice Domain Model

**Location**: `backend/app/domain/invoice.py`

**Purpose**: Represents an invoice with automatic total calculation

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Invoice:
    """
    An invoice with line items and automatic total calculation.
    The core business entity of the system.
    """
    invoice_number: str           # "INV-2025-0042" (auto-generated)
    client_id: int                # Reference to client
    issue_date: datetime          # When invoice was created
    status: str                   # "draft", "sent", "paid", "cancelled"
    line_items: List[LineItem]    # List of services/products
    pdf_path: str | None = None   # Path to generated PDF
    id: int | None = None

    @property
    def total_amount(self) -> float:
        """
        Automatically calculates invoice total from line items.
        This is ALWAYS the sum of all line item amounts.
        Never set this manually!
        """
        return sum(item.amount for item in self.line_items)

    def validate(self):
        """Business rule validation"""
        if not self.invoice_number:
            raise ValueError("Invoice number is required")

        if not self.line_items:
            raise ValueError("Invoice must have at least one line item")

        if self.total_amount <= 0:
            raise ValueError("Invoice total must be positive")

        # Validate status
        valid_statuses = ["draft", "sent", "paid", "cancelled"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")

        # Validate each line item
        for item in self.line_items:
            item.validate()

    def add_line_item(self, item: LineItem):
        """Business method to add a line item"""
        item.validate()
        self.line_items.append(item)

    @property
    def is_finalized(self) -> bool:
        """Check if invoice has been finalized (PDF generated)"""
        return self.pdf_path is not None

    def can_update_status(self, new_status: str) -> bool:
        """Business rule: Check if status transition is valid"""
        # Example: Can't change from "paid" back to "draft"
        if self.status == "paid" and new_status == "draft":
            return False
        return True
```

**Key Features**:
- `total_amount` is **automatically calculated** from line items
- Contains business rules (validation, status transitions)
- Has domain methods (`add_line_item()`, `is_finalized()`)

---

## 🔄 How Domain Models Flow Through the System

### Example: Creating an Invoice

**1. Frontend sends JSON**:
```json
POST /api/invoices
{
  "client_id": 123,
  "line_items": [
    {"description": "Web Development", "quantity": 10, "unit_price": 150.00},
    {"description": "Design Services", "quantity": 5, "unit_price": 100.00}
  ]
}
```

**2. Router (Pydantic validation)**:
```python
# app/routers/invoices.py
@router.post("/api/invoices", response_model=InvoiceResponse)
def create_invoice(request: InvoiceCreateRequest, db: Session = Depends(get_db)):
    # Pydantic validates the JSON structure
    # Then calls use-case
    domain_invoice = create_invoice_use_case.execute(db, request)
    # Converts domain → Pydantic for JSON response
    return InvoiceResponse.from_domain(domain_invoice)
```

**3. Use-Case (Business logic with domain models)**:
```python
# app/use_cases/create_invoice_use_case.py
def execute(db: Session, request: InvoiceCreateRequest) -> Invoice:
    # Create domain model line items
    line_items = [
        LineItem(
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        for item in request.line_items
    ]

    # Create domain model invoice
    invoice = Invoice(
        invoice_number="",  # Will be generated
        client_id=request.client_id,
        issue_date=datetime.now(),
        status="draft",
        line_items=line_items
    )

    # Domain validation (business rules)
    invoice.validate()  # ← Domain model method!

    # total_amount is calculated automatically
    print(f"Total: ${invoice.total_amount}")  # ← Domain property!

    # Generate invoice number (business logic)
    invoice.invoice_number = invoice_dao.generate_next_invoice_number()

    # Save via DAO
    saved_invoice = invoice_dao.create(invoice)

    # Generate PDF (business workflow)
    generate_invoice_pdf(saved_invoice)

    return saved_invoice  # Returns domain model
```

**4. DAO (Converts domain ↔ database)**:
```python
# app/daos/invoice_dao.py
def create(self, invoice: Invoice) -> Invoice:
    # Convert domain model → SQLAlchemy
    db_invoice = InvoiceTable(
        invoice_number=invoice.invoice_number,
        client_id=invoice.client_id,
        issue_date=invoice.issue_date,
        total_amount=invoice.total_amount,  # ← Calculated property!
        status=invoice.status,
        pdf_path=invoice.pdf_path
    )

    self.db.add(db_invoice)
    self.db.flush()

    # Save line items
    for line_item in invoice.line_items:
        db_line_item = LineItemTable(
            invoice_id=db_invoice.id,
            description=line_item.description,
            quantity=line_item.quantity,
            unit_price=line_item.unit_price,
            amount=line_item.amount  # ← Calculated property!
        )
        self.db.add(db_line_item)

    self.db.flush()

    # Convert SQLAlchemy → domain model
    return self._to_domain(db_invoice)
```

**5. Response (JSON back to frontend)**:
```json
{
  "id": 42,
  "invoice_number": "INV-2025-0042",
  "client_id": 123,
  "issue_date": "2025-11-03T10:30:00",
  "total_amount": 2000.00,
  "status": "draft",
  "line_items": [
    {
      "description": "Web Development",
      "quantity": 10,
      "unit_price": 150.00,
      "amount": 1500.00
    },
    {
      "description": "Design Services",
      "quantity": 5,
      "unit_price": 100.00,
      "amount": 500.00
    }
  ]
}
```

---

## 📂 Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
└── app/
    ├── domain/            # ← DOMAIN MODELS (pure Python)
    │   ├── client.py      #    Business entities with logic
    │   ├── invoice.py     #    Independent of frameworks
    │   └── line_item.py
    │
    ├── models/            # Pydantic models (API contracts)
    │   ├── client.py      # Request/response validation
    │   ├── invoice.py     # JSON serialization
    │   └── line_item.py
    │
    ├── schemas/           # SQLAlchemy ORM (database tables)
    │   ├── client.py      # Maps to database structure
    │   ├── invoice.py
    │   └── line_item.py
    │
    ├── daos/              # Data Access Objects
    │   ├── client_dao.py  # Database operations
    │   ├── invoice_dao.py # Domain ↔ SQLAlchemy conversion
    │   └── line_item_dao.py
    │
    ├── use_cases/         # Business logic layer
    │   ├── create_client_use_case.py
    │   ├── create_invoice_use_case.py
    │   ├── list_invoices_use_case.py
    │   └── update_invoice_status_use_case.py
    │
    ├── routers/           # FastAPI endpoints
    │   ├── clients.py     # HTTP layer
    │   └── invoices.py    # Pydantic ↔ Domain conversion
    │
    └── db.py              # Database connection
```

---

## 🎯 Quick Reference: Model Types

| Model Type | Location | Purpose | Example |
|------------|----------|---------|---------|
| **Domain** | `app/domain/` | Business entities & logic | `Client`, `Invoice`, `LineItem` |
| **Pydantic** | `app/models/` | API validation | `InvoiceCreateRequest`, `InvoiceResponse` |
| **SQLAlchemy** | `app/schemas/` | Database tables | `ClientTable`, `InvoiceTable` |

**Remember**: Use-cases work exclusively with **domain models**. Conversions happen at boundaries (Router and DAO).

---

## 🚀 Common Developer Tasks

### Task: Add a new field to Client

1. **Add to domain model** (`app/domain/client.py`):
   ```python
   @dataclass
   class Client:
       # ... existing fields ...
       company_name: str | None = None  # New field
   ```

2. **Add to database schema** (`app/schemas/client.py`):
   ```python
   class ClientTable(Base):
       # ... existing columns ...
       company_name = Column(String, nullable=True)
   ```

3. **Update DAO conversion** (`app/daos/client_dao.py`):
   ```python
   def _to_domain(self, db_client: ClientTable) -> Client:
       return Client(
           # ... existing fields ...
           company_name=db_client.company_name  # New field
       )
   ```

4. **Update Pydantic models** (`app/models/client.py`):
   ```python
   class ClientResponse(BaseModel):
       # ... existing fields ...
       company_name: str | None = None
   ```

### Task: Add business validation to Invoice

**Add to domain model** (`app/domain/invoice.py`):
```python
def validate(self):
    # ... existing validation ...

    # New business rule
    if self.status == "paid" and not self.pdf_path:
        raise ValueError("Paid invoices must have a PDF generated")
```

This validation automatically applies everywhere the domain model is used!

---

## 💡 Key Principles

1. **Domain models are pure Python** - No SQLAlchemy, no Pydantic, no FastAPI
2. **Business logic lives in domain models and use-cases** - Not in routers or DAOs
3. **Use-cases orchestrate workflows** - They coordinate DAOs and apply business rules
4. **Conversions happen at boundaries** - Router (Pydantic ↔ Domain), DAO (Domain ↔ SQLAlchemy)
5. **Calculated properties are automatic** - `amount`, `total_amount` are never set manually

---

## 📚 Additional Resources

- **API Spec**: `.github/APPLICATION_SPEC.md` - Complete endpoint listing
- **Architecture Guide**: `.github/prompts/clean-architecture-guide.md` - Detailed layer explanations
- **Setup Prompts**: `.github/prompts/setup-backend.md` - How to build the backend
- **Copilot Instructions**: `.github/copilot-instructions.md` - AI agent guidance

---

## ❓ FAQ

**Q: Why separate domain models from SQLAlchemy models?**
A: So business logic is independent of database structure. You can change the database without touching business rules.

**Q: Why are total_amount and amount calculated properties?**
A: To ensure they're always consistent. You can't accidentally set a wrong total - it's always calculated from line items.

**Q: Where do I put new business logic?**
A: In domain models (for entity logic) or use-cases (for workflows). Never in routers or DAOs.

**Q: Can domain models talk to the database?**
A: No! Domain models are pure Python. Only DAOs touch the database.

**Q: What's the difference between Pydantic and domain models?**
A: Pydantic models are for API (JSON validation). Domain models are for business logic. They serve different purposes.

---

Welcome to the team! 🎉 Use `/explain [section]` to dive deeper into any part of this document.
