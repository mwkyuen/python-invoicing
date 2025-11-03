# Python Invoicing System - Setup Instructions

## Quick Start

### Backend Setup (Using Conda)

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create conda environment from environment.yml**:
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the conda environment**:
   ```bash
   conda activate invoicing
   ```

4. **Install Playwright browsers** (first time only):
   ```bash
   playwright install chromium
   ```

5. **Run the backend server**:
   ```bash
   uvicorn main:app --reload
   ```

   The backend will be available at: **http://localhost:8000**
   - API documentation: **http://localhost:8000/docs**

**Alternative: Update existing environment**:
```bash
conda env update -f environment.yml --prune
```

### Frontend Setup

1. **Open a new terminal and navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the frontend development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at: **http://localhost:5173**

## Using the Application

1. Open your browser to **http://localhost:5173**
2. You'll see the Dashboard with Clients and Invoices tabs
3. Click "**+ New Client**" to create your first client
4. Click "**+ New Invoice**" to create an invoice for a client
5. Use "**Edit Status**" to update invoice status (draft → sent → paid)

## Project Structure

```
python-invoicing/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── domain/          # Business entities (Client, Invoice, LineItem)
│   │   ├── models/          # Pydantic API models
│   │   ├── schemas/         # SQLAlchemy database models
│   │   ├── daos/            # Data access layer
│   │   ├── use_cases/       # Business logic layer
│   │   ├── routers/         # API endpoints
│   │   ├── db.py            # Database setup
│   │   └── pdf_generator.py # PDF generation with Playwright
│   ├── main.py              # FastAPI application
│   └── environment.yml      # Conda environment definition
│
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── api/             # API client layer
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx          # Main app component
│   │   └── main.tsx         # Entry point
│   └── package.json         # Node dependencies
│
└── .github/                  # Documentation and AI prompts
    ├── copilot-instructions.md
    ├── ONBOARDING.md
    └── APPLICATION_SPEC.md
```

## Prerequisites

- **Conda** (Miniconda or Anaconda) - [Download here](https://docs.conda.io/en/latest/miniconda.html)
- **Node.js** 18+ and npm - [Download here](https://nodejs.org/)

## Architecture

This application follows **Clean Architecture** principles with clear separation of concerns:

### Backend Layers
1. **Domain Models** (`app/domain/`) - Pure Python business entities
2. **Use-Cases** (`app/use_cases/`) - Business logic orchestration
3. **DAOs** (`app/daos/`) - Database operations with model conversions
4. **Routers** (`app/routers/`) - HTTP API endpoints

### Data Flow
```
HTTP Request → Router (Pydantic) → Use-Case (Domain) → DAO → Database
Database → DAO (converts to Domain) → Use-Case → Router (converts to Pydantic) → HTTP Response
```

## API Endpoints

### Clients
- `POST /api/clients` - Create new client
- `GET /api/clients` - List all clients
- `GET /api/clients/{id}` - Get single client

### Invoices
- `POST /api/invoices` - Create new invoice with line items
- `GET /api/invoices` - List all invoices
- `GET /api/invoices/{id}` - Get single invoice
- `PATCH /api/invoices/{id}` - Update invoice status
- `GET /api/invoices/{id}/pdf` - Download invoice PDF (when implemented)

## Development

### Backend Testing
```bash
cd backend
conda activate invoicing
pytest
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

### Building for Production

**Backend**:
```bash
cd backend
conda activate invoicing
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run build
# Serve the dist/ directory with any static file server
```

### Exporting Dependencies for Deployment

If you need a `requirements.txt` for deployment (Docker, etc.):
```bash
conda activate invoicing
pip list --format=freeze > requirements.txt
```

## Troubleshooting

### Port Already in Use
- Backend: Change port with `uvicorn main:app --port 8001`
- Frontend: Vite will automatically suggest an alternative port

### Database Issues
- Delete `invoices.db` and restart the backend to recreate the database

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`

## Documentation

For more detailed information:
- **Developer Onboarding**: `.github/ONBOARDING.md`
- **API Specification**: `.github/APPLICATION_SPEC.md`
- **AI Agent Instructions**: `.github/copilot-instructions.md`
