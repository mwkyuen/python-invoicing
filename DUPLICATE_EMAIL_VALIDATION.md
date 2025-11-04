# Duplicate Email Validation

## Overview
Prevents creating multiple clients with the same email address. Email is used as a unique identifier for clients.

---

## Implementation

### 1. DAO Layer - Email Check Method

**File**: `backend/app/daos/client_dao.py`

Added `email_exists()` method to check if an email is already in use:

```python
def email_exists(self, email: str) -> bool:
    """
    Check if a client with the given email already exists.
    Returns True if email exists, False otherwise.
    """
    count = (
        self.db.query(ClientTable)
        .filter(ClientTable.email == email)
        .count()
    )
    return count > 0
```

**How it works**:
- Queries the database for clients with matching email
- Uses COUNT query for efficiency (doesn't fetch full records)
- Returns boolean: True if email exists, False if available

---

### 2. Use-Case Layer - Validation Logic

**File**: `backend/app/use_cases/create_client_use_case.py`

Added duplicate check before creating client:

```python
def execute(db: Session, name: str, billing_address: str, email: str, phone_number: str) -> Client:
    """
    Create a new client with validation.
    Business logic layer - works with domain models.
    """
    # Initialize DAO
    client_dao = ClientDAO(db)

    # Check for duplicate email
    if client_dao.email_exists(email):
        raise ValueError(
            f"A client with email '{email}' already exists. "
            "Please use a different email address."
        )

    # Create domain model
    client = Client(
        name=name,
        billing_address=billing_address,
        email=email,
        phone_number=phone_number
    )

    # Domain validation
    client.validate()

    # Persist via DAO (DAO handles commit)
    saved_client = client_dao.create(client)

    return saved_client
```

**Validation flow**:
1. Check if email already exists in database
2. If exists → raise ValueError with clear message
3. If available → proceed with client creation
4. Validate domain model
5. Save to database

---

### 3. Router Layer - Error Handling

**File**: `backend/app/routers/clients.py`

The existing error handling already catches ValueError:

```python
@router.post("", response_model=ClientResponse, status_code=201)
def create_client(
    request: ClientCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new client"""
    try:
        # Call use-case
        client = create_client_use_case.execute(
            db=db,
            name=request.name,
            billing_address=request.billing_address,
            email=request.email,
            phone_number=request.phone_number
        )
        # Convert domain to Pydantic response
        return ClientResponse.from_domain(client)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # ← Catches duplicate email error
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
```

**Error handling**:
- ValueError from use-case → 400 Bad Request
- Error message passed directly to client
- User sees: "A client with email 'john@example.com' already exists. Please use a different email address."

---

## User Experience

### Scenario 1: Creating First Client
```
POST /api/clients
{
  "name": "John Doe",
  "billing_address": "123 Main St",
  "email": "john@example.com",
  "phone_number": "+1-555-0001"
}

✅ Response: 201 Created
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  ...
}
```

### Scenario 2: Attempting Duplicate Email
```
POST /api/clients
{
  "name": "Jane Smith",
  "billing_address": "456 Oak Ave",
  "email": "john@example.com",  // ← Same email as above
  "phone_number": "+1-555-0002"
}

❌ Response: 400 Bad Request
{
  "detail": "A client with email 'john@example.com' already exists. Please use a different email address."
}
```

### Scenario 3: Using Different Email
```
POST /api/clients
{
  "name": "Jane Smith",
  "billing_address": "456 Oak Ave",
  "email": "jane@example.com",  // ← Different email
  "phone_number": "+1-555-0002"
}

✅ Response: 201 Created
{
  "id": 2,
  "name": "Jane Smith",
  "email": "jane@example.com",
  ...
}
```

---

## Frontend Integration

When the frontend receives a 400 error with duplicate email message:

```typescript
// In CreateClientPage.tsx or similar

const handleSubmit = async (formData: ClientFormData) => {
  try {
    const client = await clientApi.createClient(formData);
    // Success: redirect to dashboard or show success message
    navigate('/dashboard');
  } catch (error) {
    if (error.response?.status === 400) {
      // Show validation error to user
      setError(error.response.data.detail);
      // Example: "A client with email 'john@example.com' already exists. Please use a different email address."
    } else {
      // Other errors
      setError('Failed to create client. Please try again.');
    }
  }
};
```

**User sees**:
- Clear error message below email field
- Suggestion to use different email
- Form remains filled (no data loss)
- Can edit email and retry

---

## Technical Details

### Database Query
```sql
-- What happens when checking for duplicate
SELECT COUNT(*) FROM clients WHERE email = 'john@example.com';
-- If result > 0, email exists
-- If result = 0, email available
```

**Performance**:
- COUNT query is fast (indexed column)
- No need to fetch full client records
- Minimal database load

### Case Sensitivity
**Current behavior**: Case-sensitive comparison
- "john@example.com" ≠ "John@Example.com"
- Both can exist in database

**Future enhancement** (if needed):
```python
def email_exists(self, email: str) -> bool:
    count = (
        self.db.query(ClientTable)
        .filter(func.lower(ClientTable.email) == email.lower())
        .count()
    )
    return count > 0
```

---

## Validation Rules

### What's Validated
✅ **Email uniqueness** - No two clients with same email
✅ **Email format** - Validated by domain model (regex pattern)
✅ **Required fields** - Name, billing_address, email, phone_number
✅ **Phone format** - Validated by domain model

### What's NOT Validated
❌ Name uniqueness - Same name allowed (different people)
❌ Phone uniqueness - Same phone allowed (shared numbers)
❌ Address uniqueness - Same address allowed (same office)

**Rationale**: Email is the most reliable unique identifier for clients

---

## Testing

### Manual Test Steps

1. **Create first client**:
   ```bash
   curl -X POST http://localhost:8000/api/clients \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "billing_address": "123 Main St",
       "email": "test@example.com",
       "phone_number": "+1-555-0001"
     }'
   ```
   Expected: 201 Created

2. **Attempt duplicate**:
   ```bash
   curl -X POST http://localhost:8000/api/clients \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith",
       "billing_address": "456 Oak Ave",
       "email": "test@example.com",
       "phone_number": "+1-555-0002"
     }'
   ```
   Expected: 400 Bad Request with error message

3. **Verify only one exists**:
   ```bash
   curl http://localhost:8000/api/clients | jq '.[] | select(.email == "test@example.com")'
   ```
   Expected: Only one client returned

---

## Benefits

### 1. **Data Integrity**
- Prevents duplicate client records
- Ensures email can be used as unique identifier
- Maintains database consistency

### 2. **User Experience**
- Clear error messages
- Immediate feedback
- Suggests corrective action

### 3. **System Reliability**
- Prevents confusion from duplicate contacts
- Simplifies client lookup by email
- Reduces data cleanup needs

### 4. **Business Logic**
- Email is natural unique identifier
- Aligns with common business practices
- Supports future features (email notifications, etc.)

---

## Future Enhancements

### Optional Improvements

1. **Case-insensitive validation**
   - Treat "john@example.com" same as "John@Example.com"
   - Add `func.lower()` to database query

2. **Email normalization**
   - Trim whitespace
   - Convert to lowercase before saving
   - Validate email deliverability

3. **Merge duplicate suggestion**
   - If duplicate found, suggest viewing existing client
   - Provide link to existing client's details
   - Option to update existing instead of creating new

4. **Soft uniqueness**
   - Allow duplicates but warn user
   - Show existing client with same email
   - Require confirmation to proceed

5. **Email verification**
   - Send verification email on creation
   - Mark email as verified/unverified
   - Only enforce uniqueness for verified emails

---

## Summary

✅ **Duplicate email validation implemented** at use-case layer
✅ **Database check** via efficient COUNT query
✅ **Clear error messages** for users
✅ **400 Bad Request** response with detailed message
✅ **No breaking changes** to existing functionality
✅ **Follows clean architecture** pattern

The system now prevents duplicate clients by email address, ensuring data integrity and better user experience! 📧
