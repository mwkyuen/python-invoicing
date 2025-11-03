# Write Tests

Write comprehensive tests for this feature:

**Feature to Test**:
[Describe the feature, component, or endpoint]

**Backend Tests** (Test each Clean Architecture layer):

1. **Setup** (`backend/tests/`):
   - Use pytest fixtures for test database
   - Use TestClient for API/Router testing
   - Mock DAOs when testing Use-Cases
   - Mock Use-Cases when testing Routers
   - Use in-memory SQLite for DAO tests

2. **DAO Layer Tests** (`tests/test_daos/`):
   - Test database operations in isolation
   - Use test database with real SQLAlchemy
   - ✅ CRUD operations work correctly
   - ✅ Queries return expected results
   - ✅ Transactions and rollbacks
   - ✅ Foreign key constraints
   - **No mocking** - test against real (test) database

3. **Use-Case Layer Tests** (`tests/test_use_cases/`):
   - Test business logic in isolation
   - Mock DAO dependencies
   - ✅ Business rules are enforced
   - ✅ Proper coordination between DAOs
   - ✅ Error handling and exceptions
   - ✅ Transaction management
   - ✅ Edge cases and validation
   - **Mock DAOs** - focus on logic, not data

4. **Router Layer Tests** (`tests/test_routers/`):
   - Test HTTP endpoints with TestClient
   - Mock Use-Case dependencies
   - ✅ HTTP status codes are correct
   - ✅ Request validation (Pydantic)
   - ✅ Response transformation
   - ✅ Error responses formatted correctly
   - **Mock Use-Cases** - focus on HTTP, not business logic

5. **Integration Tests** (`tests/test_integration/`):
   - Test full flow without mocks
   - ✅ End-to-end scenarios work
   - ✅ All layers integrate correctly
   - ✅ Database state is correct after operations

6. **Example Test Structure**:
```python
# DAO Test (no mocks)
def test_dao_create_client(test_db):
    dao = ClientDAO(test_db)
    client = dao.create(name="Test", email="test@example.com")
    assert client.id is not None

# Use-Case Test (mock DAOs)
def test_use_case_create_invoice(mock_dao):
    use_case = CreateInvoiceUseCase(mock_dao)
    result = use_case.execute(client_id=1, items=[...])
    assert result.invoice_number.startswith("INV-")

# Router Test (mock use-cases)
def test_router_create_invoice(client, mock_use_case):
    response = client.post("/api/invoices", json={...})
    assert response.status_code == 201
```

Ensure tests are isolated, repeatable, and cover both success and failure scenarios.
