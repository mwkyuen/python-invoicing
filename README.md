# Python Invoicing System

A full-stack invoicing application with React/TypeScript frontend and FastAPI/Python backend. Create clients, generate invoices with line items, and track invoice status.

## 🚀 Quick Start

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload  # http://localhost:8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

## 📚 Documentation

- **[Copilot Instructions](.github/copilot-instructions.md)** - AI agent guidance and architecture overview
- **[Developer Onboarding](.github/ONBOARDING.md)** - New developer guide with domain models explained
- **[API Specification](.github/APPLICATION_SPEC.md)** - Complete API endpoints and workflows
- **[Prompt Templates](.github/prompts/)** - Reusable prompts for common development tasks

## 🏗️ Architecture

Clean Architecture with:
- **Domain Models** - Pure Python business entities
- **Use-Cases** - Business logic orchestration
- **DAOs** - Database operations
- **Routers** - FastAPI HTTP endpoints

**Tech Stack**: FastAPI, Pydantic, SQLAlchemy, SQLite, React, TypeScript

See [ONBOARDING.md](.github/ONBOARDING.md) for detailed architecture explanation.

## 📦 Features

- ✅ Create and manage clients
- ✅ Generate invoices with line items
- ✅ Auto-calculated totals
- ✅ Invoice status tracking (draft/sent/paid/cancelled)
- ✅ Sequential invoice numbering
- ✅ PDF generation
- ✅ RESTful API with OpenAPI docs

## 🎯 API Endpoints

**Clients**: `POST /api/clients`, `GET /api/clients`, `GET /api/clients/{id}`

**Invoices**: `POST /api/invoices`, `GET /api/invoices`, `GET /api/invoices/{id}`, `PATCH /api/invoices/{id}`, `GET /api/invoices/{id}/pdf`

See [APPLICATION_SPEC.md](.github/APPLICATION_SPEC.md) for complete API documentation.

## 📖 Contributing

Read [ONBOARDING.md](.github/ONBOARDING.md) to understand the codebase architecture and domain models.
