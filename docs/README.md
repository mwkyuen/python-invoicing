# Documentation Index

Welcome to the Python Invoicing System documentation! This guide helps you find the right documentation for your needs.

## 🚀 Getting Started

### New Users
1. **[QUICKSTART.md](../QUICKSTART.md)** - Get up and running in 5 minutes
2. **[SETUP.md](../SETUP.md)** - Detailed setup instructions with troubleshooting

### New Developers
1. **[ONBOARDING.md](../.github/ONBOARDING.md)** - Understanding the codebase architecture
2. **[APPLICATION_SPEC.md](../.github/APPLICATION_SPEC.md)** - API endpoints and data models
3. **[FEATURES.md](FEATURES.md)** - All implemented features with examples

---

## 📖 Core Documentation

### Architecture & Design
- **[ONBOARDING.md](../.github/ONBOARDING.md)** - Clean Architecture explained with code examples
  - Domain models (Client, Invoice, LineItem)
  - Data flow through layers (Router → Use-Case → DAO)
  - Model types (Domain, Pydantic, SQLAlchemy)

- **[copilot-instructions.md](../.github/copilot-instructions.md)** - AI agent guidance
  - Tech stack overview
  - Backend conventions
  - Frontend patterns
  - Development workflow

### API Reference
- **[APPLICATION_SPEC.md](../.github/APPLICATION_SPEC.md)** - Complete API specification
  - All REST endpoints with request/response schemas
  - Database schema with SQL definitions
  - Frontend page specifications
  - Business rules and workflows

### Features
- **[FEATURES.md](FEATURES.md)** - Feature documentation
  - Client management (CRUD, email validation)
  - Invoice management (CRUD, status tracking)
  - Delete functionality with validation
  - PDF generation and cache management
  - Dashboard UI patterns

---

## 🛠️ Development Guides

### Prompt Templates
Location: `../.github/prompts/`

Reusable prompts for common development tasks:
- **[setup-backend.md](../.github/prompts/setup-backend.md)** - Setting up Python/FastAPI backend
- **[setup-frontend.md](../.github/prompts/setup-frontend.md)** - Setting up React/TypeScript frontend
- **[add-api-endpoint.md](../.github/prompts/add-api-endpoint.md)** - Adding new API endpoints
- **[add-react-component.md](../.github/prompts/add-react-component.md)** - Creating React components
- **[write-tests.md](../.github/prompts/write-tests.md)** - Writing backend tests
- **[clean-architecture-guide.md](../.github/prompts/clean-architecture-guide.md)** - Clean Architecture patterns
- **[review-clean-architecture.md](../.github/prompts/review-clean-architecture.md)** - Architecture review checklist

### Common Tasks

**Adding a New Feature**:
1. Define API contract in Pydantic models
2. Implement DAO (data access)
3. Implement Use-Case (business logic)
4. Implement Router (HTTP handling)
5. Create frontend API client
6. Build React component
7. Write tests

**Understanding Existing Code**:
1. Start with [ONBOARDING.md](../.github/ONBOARDING.md) for architecture overview
2. Check [APPLICATION_SPEC.md](../.github/APPLICATION_SPEC.md) for API contracts
3. Review domain models in `backend/app/domain/`
4. Trace data flow: Router → Use-Case → DAO

---

## 📚 Quick Reference

### Project Structure
```
python-invoicing/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── domain/      # Business entities (pure Python)
│   │   ├── models/      # Pydantic API models
│   │   ├── schemas/     # SQLAlchemy database models
│   │   ├── daos/        # Data access layer
│   │   ├── use_cases/   # Business logic layer
│   │   └── routers/     # HTTP API endpoints
│   └── main.py          # FastAPI application
│
├── frontend/             # React + TypeScript
│   └── src/
│       ├── api/         # API client layer
│       ├── components/  # Reusable components
│       ├── pages/       # Page components
│       └── types/       # TypeScript interfaces
│
├── docs/                # Documentation
│   ├── FEATURES.md      # Feature documentation
│   └── archive/         # Archived implementation docs
│
└── .github/             # Core docs & AI prompts
    ├── ONBOARDING.md
    ├── APPLICATION_SPEC.md
    ├── copilot-instructions.md
    └── prompts/
```

### Key Concepts

**Domain Models** (Pure Python):
- `Client` - Customer with name, email, billing address
- `Invoice` - Invoice with auto-calculated total
- `LineItem` - Line item with auto-calculated amount

**Data Flow**:
```
HTTP → Router (Pydantic) → Use-Case (Domain) → DAO (SQLAlchemy) → Database
```

**Clean Architecture Layers**:
1. **Router** - HTTP concerns (request/response)
2. **Use-Case** - Business logic orchestration
3. **DAO** - Database operations and conversions
4. **Domain** - Business entities and rules

---

## 🗄️ Archive

Historical implementation documentation (for reference):
- `archive/DELETE_FEATURE_SUMMARY.md` - Delete feature implementation
- `archive/CLIENT_DELETION_VALIDATION.md` - Client deletion validation
- `archive/DANGER_COLUMN_UI.md` - Dashboard UI improvements
- `archive/DUPLICATE_EMAIL_VALIDATION.md` - Email uniqueness validation
- `archive/INVOICE_VIEWING_FEATURE.md` - Invoice viewing implementation
- `archive/DASHBOARD_CENTRIC_UPDATE.md` - Dashboard action pattern
- `archive/TRANSACTION_MANAGEMENT.md` - Database transaction handling

**Note**: These docs contain detailed implementation notes but are superseded by [FEATURES.md](FEATURES.md) for feature documentation.

---

## 🎯 Finding What You Need

| I want to... | Read this... |
|-------------|--------------|
| Get the app running | [QUICKSTART.md](../QUICKSTART.md) |
| Understand the architecture | [ONBOARDING.md](../.github/ONBOARDING.md) |
| See all API endpoints | [APPLICATION_SPEC.md](../.github/APPLICATION_SPEC.md) |
| Learn about features | [FEATURES.md](FEATURES.md) |
| Add a new endpoint | [add-api-endpoint.md](../.github/prompts/add-api-endpoint.md) |
| Create a component | [add-react-component.md](../.github/prompts/add-react-component.md) |
| Write tests | [write-tests.md](../.github/prompts/write-tests.md) |
| Configure AI agent | [copilot-instructions.md](../.github/copilot-instructions.md) |
| Troubleshoot setup | [SETUP.md](../SETUP.md) |

---

## 📝 Contributing to Documentation

When adding new documentation:
- **Features**: Update [FEATURES.md](FEATURES.md)
- **API Changes**: Update [APPLICATION_SPEC.md](../.github/APPLICATION_SPEC.md)
- **Architecture Changes**: Update [ONBOARDING.md](../.github/ONBOARDING.md)
- **Setup Changes**: Update [SETUP.md](../SETUP.md) or [QUICKSTART.md](../QUICKSTART.md)

Keep implementation details in `archive/` for reference but maintain current state in main docs.

---

*Last Updated: November 4, 2025*
