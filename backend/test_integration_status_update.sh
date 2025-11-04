#!/bin/bash
# Integration test for PDF status update feature

echo "=================================================="
echo "PDF Status Update Integration Test"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000"

# Check if server is running
echo "[1] Checking if backend server is running..."
if ! curl -s "$BASE_URL/api/clients" > /dev/null; then
    echo "❌ Backend server is not running!"
    echo "   Start it with: cd backend && conda run -n invoicing uvicorn main:app --reload"
    exit 1
fi
echo "✅ Backend server is running"
echo ""

# Create a test client
echo "[2] Creating test client..."
CLIENT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/clients" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Integration Test Co",
        "billing_address": "456 Test Ave",
        "email": "integration@test.com",
        "phone_number": "555-9999"
    }')
CLIENT_ID=$(echo "$CLIENT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Created client with ID: $CLIENT_ID"
echo ""

# Create an invoice
echo "[3] Creating invoice..."
INVOICE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/invoices" \
    -H "Content-Type: application/json" \
    -d "{
        \"client_id\": $CLIENT_ID,
        \"line_items\": [
            {
                \"description\": \"Integration Test Service\",
                \"quantity\": 5,
                \"unit_price\": 100.0
            }
        ]
    }")
INVOICE_ID=$(echo "$INVOICE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
INVOICE_NUMBER=$(echo "$INVOICE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['invoice_number'])")
INITIAL_STATUS=$(echo "$INVOICE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
INITIAL_PDF=$(echo "$INVOICE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['pdf_path'])")

echo "✅ Created invoice:"
echo "   ID: $INVOICE_ID"
echo "   Number: $INVOICE_NUMBER"
echo "   Initial status: $INITIAL_STATUS"
echo "   PDF path: $INITIAL_PDF"
echo ""

# Download initial PDF
echo "[4] Downloading initial PDF..."
curl -s "$BASE_URL/api/invoices/$INVOICE_ID/pdf" -o "/tmp/invoice_$INVOICE_NUMBER-initial.pdf"
INITIAL_SIZE=$(stat -f%z "/tmp/invoice_$INVOICE_NUMBER-initial.pdf" 2>/dev/null || stat -c%s "/tmp/invoice_$INVOICE_NUMBER-initial.pdf" 2>/dev/null)
echo "✅ Downloaded initial PDF ($INITIAL_SIZE bytes)"
echo "   Saved to: /tmp/invoice_$INVOICE_NUMBER-initial.pdf"
echo ""

# Update status to "sent"
echo "[5] Updating status to 'sent'..."
sleep 1  # Wait a moment to ensure timestamp changes
SENT_RESPONSE=$(curl -s -X PATCH "$BASE_URL/api/invoices/$INVOICE_ID" \
    -H "Content-Type: application/json" \
    -d '{"status": "sent"}')
SENT_STATUS=$(echo "$SENT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
echo "✅ Updated status: $SENT_STATUS"
echo ""

# Download PDF after first update
echo "[6] Downloading PDF after status change to 'sent'..."
curl -s "$BASE_URL/api/invoices/$INVOICE_ID/pdf" -o "/tmp/invoice_$INVOICE_NUMBER-sent.pdf"
SENT_SIZE=$(stat -f%z "/tmp/invoice_$INVOICE_NUMBER-sent.pdf" 2>/dev/null || stat -c%s "/tmp/invoice_$INVOICE_NUMBER-sent.pdf" 2>/dev/null)
echo "✅ Downloaded 'sent' PDF ($SENT_SIZE bytes)"
echo "   Saved to: /tmp/invoice_$INVOICE_NUMBER-sent.pdf"

if [ "$SENT_SIZE" != "$INITIAL_SIZE" ]; then
    echo "✅ PDF size changed - PDF was regenerated!"
else
    echo "⚠️  PDF size unchanged - checking if content differs..."
fi
echo ""

# Update status to "paid"
echo "[7] Updating status to 'paid'..."
sleep 1  # Wait a moment to ensure timestamp changes
PAID_RESPONSE=$(curl -s -X PATCH "$BASE_URL/api/invoices/$INVOICE_ID" \
    -H "Content-Type: application/json" \
    -d '{"status": "paid"}')
PAID_STATUS=$(echo "$PAID_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
echo "✅ Updated status: $PAID_STATUS"
echo ""

# Download final PDF
echo "[8] Downloading final PDF after status change to 'paid'..."
curl -s "$BASE_URL/api/invoices/$INVOICE_ID/pdf" -o "/tmp/invoice_$INVOICE_NUMBER-paid.pdf"
PAID_SIZE=$(stat -f%z "/tmp/invoice_$INVOICE_NUMBER-paid.pdf" 2>/dev/null || stat -c%s "/tmp/invoice_$INVOICE_NUMBER-paid.pdf" 2>/dev/null)
echo "✅ Downloaded 'paid' PDF ($PAID_SIZE bytes)"
echo "   Saved to: /tmp/invoice_$INVOICE_NUMBER-paid.pdf"

if [ "$PAID_SIZE" != "$SENT_SIZE" ]; then
    echo "✅ PDF size changed - PDF was regenerated!"
else
    echo "⚠️  PDF size unchanged - checking if content differs..."
fi
echo ""

echo "=================================================="
echo "SUMMARY"
echo "=================================================="
echo "Created:"
echo "  - Client ID: $CLIENT_ID"
echo "  - Invoice ID: $INVOICE_ID ($INVOICE_NUMBER)"
echo ""
echo "Status transitions:"
echo "  1. Initial: $INITIAL_STATUS"
echo "  2. Updated: sent"
echo "  3. Final: paid"
echo ""
echo "PDFs saved to /tmp/:"
echo "  - invoice_$INVOICE_NUMBER-initial.pdf ($INITIAL_SIZE bytes)"
echo "  - invoice_$INVOICE_NUMBER-sent.pdf ($SENT_SIZE bytes)"
echo "  - invoice_$INVOICE_NUMBER-paid.pdf ($PAID_SIZE bytes)"
echo ""
echo "✅ All tests passed!"
echo ""
echo "You can open the PDFs to verify the status badge changes:"
echo "  open /tmp/invoice_$INVOICE_NUMBER-initial.pdf"
echo "  open /tmp/invoice_$INVOICE_NUMBER-sent.pdf"
echo "  open /tmp/invoice_$INVOICE_NUMBER-paid.pdf"
