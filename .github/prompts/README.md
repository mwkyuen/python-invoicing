# Prompt Files Index

Quick reference for all available prompt templates in `.github/prompts/`.

## 🏗️ Project Setup

### `setup-backend.md`
Set up complete backend with Clean Architecture layers (routers, use-cases, DAOs), database models, and API endpoints.

**Usage**: `@setup-backend.md - Initialize the backend structure`

### `setup-frontend.md`
Set up React + TypeScript frontend with form components, API client, and type definitions.

**Usage**: `@setup-frontend.md - Create the frontend application`

## 🔧 Development

### `create-domain-model.md`
Create a pure Python domain model with business logic and validation rules.

**Usage**: `@create-domain-model.md - Create Payment domain model`

### `add-api-endpoint.md`
Add a new REST API endpoint following Clean Architecture pattern (Domain → DAO → Use-Case → Router).

**Usage**: `@add-api-endpoint.md - Add GET /api/clients endpoint`

### `add-react-component.md`
Create a new React component with TypeScript, proper state management, and API integration.

**Usage**: `@add-react-component.md - Create InvoiceList component`

## 🧪 Testing

### `write-tests.md`
Write comprehensive tests for each layer (DAO, Use-Case, Router) with proper mocking strategy.

**Usage**: `@write-tests.md - Test the invoice creation feature`

## 📚 Architecture Reference

### `clean-architecture-guide.md`
Complete reference for Clean Architecture implementation with examples, common mistakes, and quick reference table.

**Usage**: `@clean-architecture-guide.md - Explain the layer responsibilities`

### `review-clean-architecture.md`
Review code to ensure it follows Clean Architecture principles with violation detection and fixes.

**Usage**: `@review-clean-architecture.md - Review app/routers/invoices.py`

## 🎯 Quick Tips

**Combine Prompts**:
```
@setup-backend.md and @setup-frontend.md - Build the complete application
```

**Extend Prompts**:
```
@add-api-endpoint.md - Add POST /api/invoices endpoint with PDF generation support
```

**Reference During Development**:
```
Following @clean-architecture-guide.md, implement the invoice creation flow
```

## 📋 Checklist for New Features

1. ✅ Review `.github/copilot-instructions.md` for project context
2. ✅ Use `@clean-architecture-guide.md` to understand layer separation
3. ✅ Use `@create-domain-model.md` to define business entities
4. ✅ Use `@add-api-endpoint.md` to implement backend (DAO → Use-Case → Router)
5. ✅ Use `@add-react-component.md` to implement frontend
6. ✅ Use `@write-tests.md` to add test coverage
7. ✅ Use `@review-clean-architecture.md` to verify compliance

## 💡 Best Practices

- Always reference the Clean Architecture guide when adding backend features
- Start with domain models (pure Python with business logic)
- Keep layer responsibilities clear:
  - Router: HTTP + Pydantic ↔ Domain conversion
  - Use-Case: Business logic with domain models
  - DAO: Database + SQLAlchemy ↔ Domain conversion
- Use-cases work exclusively with domain models
- Test each layer independently with appropriate mocking
- Domain models should have no framework dependencies
- Follow existing patterns in the codebase
