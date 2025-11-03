# Review Code for Clean Architecture

Review the following code to ensure it follows Clean Architecture principles:

**File to Review**: [file path]
**Layer**: [Router / Use-Case / DAO]

## Review Checklist

### If Reviewing a ROUTER (`app/routers/`):
- [ ] Only handles HTTP concerns (request/response)
- [ ] Uses Pydantic models for validation
- [ ] Calls use-case functions (not DAOs directly)
- [ ] Returns appropriate HTTP status codes
- [ ] Transforms domain objects to response models
- [ ] No business logic in router
- [ ] No database queries in router
- [ ] Proper error handling with HTTPException

**Red Flags**:
- Direct DAO instantiation or calls
- Business calculations or rules
- Transaction management (db.commit/rollback)
- Complex logic beyond HTTP concerns

### If Reviewing a USE-CASE (`app/use_cases/`):
- [ ] Contains business logic and orchestration
- [ ] Coordinates between multiple DAOs if needed
- [ ] Manages database transactions (commit/rollback)
- [ ] Validates business rules
- [ ] Returns domain objects (ORM models or domain entities)
- [ ] Raises domain exceptions (ValueError, BusinessRuleError)
- [ ] No HTTP concepts (no HTTPException, status codes)
- [ ] No Pydantic request/response models
- [ ] No direct SQL queries (uses DAOs)

**Red Flags**:
- HTTP status codes or HTTPException
- FastAPI dependencies (Depends, Request, Response)
- Direct SQLAlchemy queries (db.query)
- Knowledge of API layer concerns

### If Reviewing a DAO (`app/daos/`):
- [ ] Only performs database operations
- [ ] Uses SQLAlchemy ORM for queries
- [ ] Simple CRUD operations
- [ ] Returns ORM models or None
- [ ] No business logic or validation
- [ ] No transaction commits (uses flush, not commit)
- [ ] Doesn't call other DAOs
- [ ] Methods are simple and focused

**Red Flags**:
- Business rule validation
- Complex calculations
- Calling other DAOs
- Transaction management (db.commit)
- Domain logic

## Common Violations

### ❌ Violation Example 1: Router with Business Logic
```python
@router.post("/api/invoices")
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    # WRONG - Business logic in router
    if sum(item.amount for item in data.items) < 0:
        raise HTTPException(400, "Invalid total")

    invoice_number = f"INV-{datetime.now().year}-{get_next_id()}"
    # More business logic...
```

**Fix**: Move business logic to use-case:
```python
@router.post("/api/invoices")
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    result = create_invoice_use_case.execute(db, data)
    return InvoiceResponse.from_orm(result)
```

### ❌ Violation Example 2: Use-Case with HTTP Concerns
```python
def create_invoice_use_case(db, data):
    try:
        # Business logic...
        return invoice
    except Exception:
        # WRONG - HTTP status code in use-case
        raise HTTPException(status_code=500, detail="Error")
```

**Fix**: Raise domain exception, let router handle HTTP:
```python
def create_invoice_use_case(db, data):
    try:
        # Business logic...
        return invoice
    except Exception as e:
        raise ValueError(f"Failed to create invoice: {e}")
```

### ❌ Violation Example 3: DAO with Business Logic
```python
class InvoiceDAO:
    def create(self, data):
        # WRONG - Business rule in DAO
        if data.total_amount < 0:
            raise ValueError("Amount must be positive")

        # WRONG - Transaction management in DAO
        invoice = Invoice(**data)
        self.db.add(invoice)
        self.db.commit()  # Should be in use-case
        return invoice
```

**Fix**: Move validation to use-case, remove commit:
```python
class InvoiceDAO:
    def create(self, invoice_number, client_id, total_amount):
        invoice = Invoice(
            invoice_number=invoice_number,
            client_id=client_id,
            total_amount=total_amount
        )
        self.db.add(invoice)
        self.db.flush()  # Flush, don't commit
        return invoice
```

## Review Output

For each violation found:
1. Identify the layer violation
2. Explain why it breaks Clean Architecture
3. Show which layer should handle this concern
4. Provide corrected code example

If code is clean:
- Confirm it follows Clean Architecture
- Note any best practices demonstrated
- Suggest minor improvements if any
