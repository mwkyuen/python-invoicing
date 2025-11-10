"""
PDF generation using WeasyPrint for invoice rendering.
Simpler and more reliable than Playwright - no browser dependencies.
"""
from pathlib import Path
from datetime import datetime
from weasyprint import HTML
from jinja2 import Template

from app.domain.invoice import Invoice
from app.domain.client import Client


# HTML template for invoice
INVOICE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
            color: #333;
        }
        .header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 40px;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
        }
        .company-info {
            flex: 1;
        }
        .invoice-info {
            text-align: right;
        }
        .invoice-number {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        .client-section {
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 14px;
            color: #7f8c8d;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .client-details {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 40px;
        }
        th {
            background-color: #2c3e50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: normal;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        .text-right {
            text-align: right;
        }
        .total-section {
            margin-left: auto;
            width: 300px;
        }
        .total-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
        }
        .total-row.final {
            border-top: 2px solid #2c3e50;
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding-top: 15px;
            margin-top: 10px;
        }
        .footer {
            margin-top: 60px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .status-draft { background-color: #95a5a6; color: white; }
        .status-sent { background-color: #3498db; color: white; }
        .status-paid { background-color: #2ecc71; color: white; }
        .status-cancelled { background-color: #e74c3c; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <div class="company-info">
            <h1 style="margin: 0; color: #2c3e50;">Python Invoicing System</h1>
            <p style="margin: 5px 0; color: #7f8c8d;">Professional Invoice Management</p>
        </div>
        <div class="invoice-info">
            <div class="invoice-number">{{ invoice.invoice_number }}</div>
            <p style="margin: 5px 0;">Date: {{ invoice.issue_date.strftime('%B %d, %Y') }}</p>
            <span class="status-badge status-{{ invoice.status }}">{{ invoice.status }}</span>
        </div>
    </div>

    <div class="client-section">
        <div class="section-title">Bill To:</div>
        <div class="client-details">
            <strong style="font-size: 16px;">{{ client.name }}</strong><br>
            {{ client.billing_address }}<br>
            {{ client.email }}<br>
            {{ client.phone_number }}
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 50%;">Description</th>
                <th class="text-right">Quantity</th>
                <th class="text-right">Unit Price</th>
                <th class="text-right">Amount</th>
            </tr>
        </thead>
        <tbody>
            {% for item in invoice.line_items %}
            <tr>
                <td>{{ item.description }}</td>
                <td class="text-right">{{ "%.2f"|format(item.quantity) }}</td>
                <td class="text-right">${{ "%.2f"|format(item.unit_price) }}</td>
                <td class="text-right">${{ "%.2f"|format(item.amount) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="total-section">
        <div class="total-row">
            <span>Subtotal:</span>
            <span>${{ "%.2f"|format(invoice.total_amount) }}</span>
        </div>
        <div class="total-row final">
            <span>Total:</span>
            <span>${{ "%.2f"|format(invoice.total_amount) }}</span>
        </div>
    </div>

    <div class="footer">
        <p>Thank you for your business!</p>
        <p>Generated on {{ now.strftime('%B %d, %Y at %I:%M %p') }}</p>
    </div>
</body>
</html>
"""


def generate_invoice_pdf(invoice: Invoice, client: Client) -> str:
    """
    Generate a PDF invoice using WeasyPrint.

    Much simpler than Playwright:
    - No browser required
    - No hanging or blocking
    - Faster (< 1 second)
    - Pure Python

    Args:
        invoice: Invoice domain model with line items
        client: Client domain model

    Returns:
        Path to the generated PDF file
    """
    print(f"[PDF Generator] Starting PDF generation for {invoice.invoice_number}")

    # Create output directory if it doesn't exist
    output_dir = Path("generated_invoices")
    output_dir.mkdir(exist_ok=True)

    # Generate filename
    pdf_filename = f"{invoice.invoice_number}.pdf"
    pdf_path = output_dir / pdf_filename

    print("[PDF Generator] Rendering HTML template...")
    # Render HTML from template
    template = Template(INVOICE_TEMPLATE)
    html_content = template.render(
        invoice=invoice,
        client=client,
        now=datetime.now()
    )

    print("[PDF Generator] Generating PDF with WeasyPrint...")
    try:
        # Generate PDF - simple one-liner!
        HTML(string=html_content).write_pdf(str(pdf_path))
        print(f"[PDF Generator] PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"[PDF Generator] ERROR: Failed to generate PDF: {e}")
        raise

    return str(pdf_path)
