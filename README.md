# Python Invoicing System

**THIS CODE WAS WRITTEN BY COPILOT - see copilot_chat_01.m1 for details** A full-stack invoicing application with React/TypeScript frontend and FastAPI/Python backend. Create clients, generate invoices with line items, and track invoice status.

## 🚀 Quick Start

**Prerequisites**: [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Node.js](https://nodejs.org/)

**Backend**:
```bash
cd backend
conda env create -f environment.yml
conda activate invoicing
uvicorn main:app --reload  # http://localhost:8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

See [QUICKSTART.md](QUICKSTART.md) for one-command setup or [SETUP.md](SETUP.md) for detailed instructions.

## 📚 Documentation

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - One-command setup with Conda
- **[SETUP.md](SETUP.md)** - Detailed installation and configuration

### Developer Documentation
- **[Developer Onboarding](.github/ONBOARDING.md)** - New developer guide with domain models explained
- **[API Specification](.github/APPLICATION_SPEC.md)** - Complete API endpoints and workflows
- **[Features Guide](docs/FEATURES.md)** - All implemented features with examples
- **[Copilot Instructions](.github/copilot-instructions.md)** - AI agent guidance and architecture overview
- **[Prompt Templates](.github/prompts/)** - Reusable prompts for common development tasks

## 🏗️ Architecture

Clean Architecture with:
- **Domain Models** - Pure Python business entities
- **Use-Cases** - Business logic orchestration
- **DAOs** - Database operations
- **Routers** - FastAPI HTTP endpoints

**Tech Stack**: Python 3.10, FastAPI, Pydantic, SQLAlchemy, SQLite, WeasyPrint, React, TypeScript, Conda

See [ONBOARDING.md](.github/ONBOARDING.md) for detailed architecture explanation.

## 📦 Features

### Core Functionality
- ✅ **Client Management** - Create, view, delete clients with email uniqueness validation
- ✅ **Invoice Management** - Generate invoices with line items and status tracking
- ✅ **Auto-Calculations** - Totals calculated automatically from line items
- ✅ **Sequential Numbering** - Auto-generated invoice numbers (INV-2025-0001, etc.)
- ✅ **PDF Generation** - Professional PDFs using WeasyPrint + HTML/CSS templates
- ✅ **Status Tracking** - Draft → Sent → Paid or Cancelled workflows
- ✅ **Data Protection** - Validation prevents deleting clients with invoices
- ✅ **Dashboard UI** - Tabbed interface with action buttons and delete column

See [docs/FEATURES.md](docs/FEATURES.md) for detailed feature documentation.

## 🎯 API Endpoints

**Clients**: `POST /api/clients`, `GET /api/clients`, `GET /api/clients/{id}`

**Invoices**: `POST /api/invoices`, `GET /api/invoices`, `GET /api/invoices/{id}`, `PATCH /api/invoices/{id}`, `GET /api/invoices/{id}/pdf`

See [APPLICATION_SPEC.md](.github/APPLICATION_SPEC.md) for complete API documentation.

## 📖 Contributing

Read [ONBOARDING.md](.github/ONBOARDING.md) to understand the codebase architecture and domain models.
