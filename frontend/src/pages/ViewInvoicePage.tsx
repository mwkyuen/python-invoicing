import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { invoiceApi } from '../api/invoiceApi';
import { clientApi } from '../api/clientApi';
import { Invoice } from '../types/Invoice';
import { Client } from '../types/Client';
import LoadingSpinner from '../components/LoadingSpinner';
import InvoiceStatusBadge from '../components/InvoiceStatusBadge';
import ErrorMessage from '../components/ErrorMessage';

export default function ViewInvoicePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [client, setClient] = useState<Client | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadInvoice();
  }, [id]);

  const loadInvoice = async () => {
    try {
      if (!id) return;
      const invoiceData = await invoiceApi.getInvoice(Number(id));
      setInvoice(invoiceData);

      // Load client details
      const clientData = await clientApi.getClient(invoiceData.client_id);
      setClient(clientData);
    } catch (err: any) {
      setError('Failed to load invoice: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!invoice) return <ErrorMessage message="Invoice not found" />;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Invoice Details</h1>
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '10px 20px',
            backgroundColor: '#95a5a6',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          ← Back to Dashboard
        </button>
      </div>

      <ErrorMessage message={error} />

      {/* Invoice Header */}
      <div style={{
        backgroundColor: '#f8f9fa',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '20px',
        border: '1px solid #dee2e6'
      }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
          <div>
            <h2 style={{ marginTop: 0, color: '#2c3e50' }}>{invoice.invoice_number}</h2>
            <p style={{ margin: '5px 0' }}>
              <strong>Issue Date:</strong> {new Date(invoice.issue_date).toLocaleDateString()}
            </p>
            <p style={{ margin: '5px 0' }}>
              <strong>Status:</strong> <InvoiceStatusBadge status={invoice.status} />
            </p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <h3 style={{ marginTop: 0, color: '#27ae60', fontSize: '32px' }}>
              ${invoice.total_amount.toFixed(2)}
            </h3>
            <p style={{ color: '#7f8c8d', margin: '5px 0' }}>Total Amount</p>
          </div>
        </div>
      </div>

      {/* Client Information */}
      {client && (
        <div style={{
          backgroundColor: '#ffffff',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '20px',
          border: '1px solid #dee2e6'
        }}>
          <h3 style={{ marginTop: 0, borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>
            Client Information
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
            <div>
              <p style={{ margin: '5px 0' }}>
                <strong>Name:</strong> {client.name}
              </p>
              <p style={{ margin: '5px 0' }}>
                <strong>Email:</strong> {client.email}
              </p>
            </div>
            <div>
              <p style={{ margin: '5px 0' }}>
                <strong>Phone:</strong> {client.phone_number}
              </p>
              <p style={{ margin: '5px 0' }}>
                <strong>Address:</strong> {client.billing_address}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Line Items */}
      <div style={{
        backgroundColor: '#ffffff',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '20px',
        border: '1px solid #dee2e6'
      }}>
        <h3 style={{ marginTop: 0, borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>
          Line Items
        </h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5' }}>
              <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Description</th>
              <th style={{ padding: '10px', textAlign: 'center', border: '1px solid #ddd' }}>Quantity</th>
              <th style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>Unit Price</th>
              <th style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {invoice.line_items.map((item, index) => (
              <tr key={index}>
                <td style={{ padding: '10px', border: '1px solid #ddd' }}>{item.description}</td>
                <td style={{ padding: '10px', textAlign: 'center', border: '1px solid #ddd' }}>
                  {item.quantity}
                </td>
                <td style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>
                  ${item.unit_price.toFixed(2)}
                </td>
                <td style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>
                  ${item.amount.toFixed(2)}
                </td>
              </tr>
            ))}
            <tr style={{ backgroundColor: '#f8f9fa', fontWeight: 'bold' }}>
              <td colSpan={3} style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>
                Total:
              </td>
              <td style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>
                ${invoice.total_amount.toFixed(2)}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
