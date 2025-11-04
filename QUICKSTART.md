# Quick Start with Conda

## One-Command Setup

```bash
chmod +x setup.sh && ./setup.sh
```

## Manual Setup

### Backend
```bash
cd backend
conda env create -f environment.yml
conda activate invoicing
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Using the App

Open **http://localhost:5173** in your browser.

## PDF Generation

This application uses **WeasyPrint** (pure Python PDF library) to generate professional invoice PDFs from HTML/CSS templates. PDFs are automatically generated when you create an invoice and stored in `backend/generated_invoices/`.

## Managing the Conda Environment

**Update environment**:
```bash
conda env update -f environment.yml --prune
```

**Remove environment**:
```bash
conda env remove -n invoicing
```

**List environments**:
```bash
conda env list
```

## Documentation

- Full setup instructions: `SETUP.md`
- Developer onboarding: `.github/ONBOARDING.md`
- API specification: `.github/APPLICATION_SPEC.md`
