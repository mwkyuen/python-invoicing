# Transaction Management - Clean Architecture

This document explains how database transactions are handled following Clean Architecture principles.

## Architecture Layers

```
┌─────────────────────────────────────────────┐
│ Router Layer (HTTP)                         │
│ - Handles HTTP requests/responses           │
│ - Validates input (Pydantic)                │
│ - Calls use-cases                           │
│ - Handles errors with rollback              │
│ - NO database commits                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ Use-Case Layer (Business Logic)             │
│ - Orchestrates business workflows           │
│ - Validates domain rules                    │
│ - Coordinates multiple DAOs                 │
│ - NO database commits                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ DAO Layer (Data Access)                     │
│ - Executes database operations              │
│ - Converts Domain ↔ Database models         │
│ - COMMITS transactions after operations     │
│ - Single source of truth for persistence    │
└─────────────────────────────────────────────┘
```

## Transaction Responsibility

### ✅ DAO Layer (app/daos/)
**DOES handle commits**
- `client_dao.create()` - Commits after insert
- `invoice_dao.create()` - Commits after insert with line items
- `invoice_dao.update_status()` - Commits after update
- `invoice_dao.update_pdf_path()` - Commits after update

### ❌ Use-Case Layer (app/use_cases/)
**Does NOT handle commits**
- Calls DAO methods which handle their own commits
- Focuses on business logic and orchestration
- Comments indicate "DAO handles commit"

### ❌ Router Layer (app/routers/)
**Does NOT handle commits**
- Uses `db.rollback()` in exception handlers only
- No `db.commit()` calls anywhere
- The `get_db()` dependency closes the session automatically

## Pattern Example

```python
# ❌ OLD WAY (Anti-pattern)
@router.post("/api/clients")
def create_client(request, db):
    try:
        client = use_case.execute(db, request)
        return response
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.commit()  # ❌ WRONG - commits even during errors!

# ✅ NEW WAY (Clean Architecture)
@router.post("/api/clients")
def create_client(request, db):
    try:
        client = use_case.execute(db, request)  # DAO commits inside
        return response
    except Exception as e:
        db.rollback()
        raise
```

## Benefits

1. **Single Responsibility**: Each DAO method is responsible for its own transaction
2. **Consistency**: All database operations commit at the same layer
3. **Safety**: No risk of committing during exception handling
4. **Testability**: Easy to mock DAOs without worrying about transaction state
5. **Clean Architecture**: Data access concerns stay in the data access layer

## Database Configuration

SQLite timeout is set to 30 seconds in `app/db.py`:

```python
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # Wait up to 30 seconds for lock
    }
)
```

This prevents "database is locked" errors by allowing the database to wait for locks to release.

## Error Handling

- **Router Layer**: Catches exceptions and calls `db.rollback()`
- **DAO Layer**: If an error occurs before commit, the session is rolled back by the router
- **Session Cleanup**: `get_db()` dependency always closes the session in a `finally` block

## Files Modified

1. `app/daos/client_dao.py` - Added `db.commit()` in `create()`
2. `app/daos/invoice_dao.py` - Added `db.commit()` in `create()`, `update_status()`, `update_pdf_path()`
3. `app/use_cases/create_client_use_case.py` - Removed `db.commit()`
4. `app/use_cases/create_invoice_use_case.py` - Removed `db.commit()`
5. `app/use_cases/update_invoice_status_use_case.py` - Removed `db.commit()`
6. `app/routers/clients.py` - Removed `finally: db.commit()` block
7. `app/routers/invoices.py` - Removed `finally: db.commit()` blocks (2 endpoints)
8. `app/db.py` - Added `timeout: 30` to SQLite connection

---

**Last Updated**: November 3, 2025
**Architecture**: Clean Architecture with Domain-Driven Design
