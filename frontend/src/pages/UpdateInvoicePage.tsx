import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { invoiceApi } from '../api/invoiceApi';
import { Invoice } from '../types/Invoice';
import ErrorMessage from '../components/ErrorMessage';
import LoadingSpinner from '../components/LoadingSpinner';

export default function UpdateInvoicePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadInvoice(parseInt(id));
    }
  }, [id]);

  const loadInvoice = async (invoiceId: number) => {
    try {
      const data = await invoiceApi.getInvoice(invoiceId);
      setInvoice(data);
      setStatus(data.status);
    } catch (err: any) {
      setError('Failed to load invoice');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !invoice) return;

    setError('');
    setSubmitting(true);

    try {
      await invoiceApi.updateInvoiceStatus(parseInt(id), { status });
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update invoice status');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!invoice) return <div>Invoice not found</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Update Invoice Status</h2>

      <div style={{
        padding: '15px',
        backgroundColor: '#f9f9f9',
        borderRadius: '4px',
        marginBottom: '20px'
      }}>
        <p><strong>Invoice Number:</strong> {invoice.invoice_number}</p>
        <p><strong>Issue Date:</strong> {new Date(invoice.issue_date).toLocaleDateString()}</p>
        <p><strong>Total Amount:</strong> ${invoice.total_amount.toFixed(2)}</p>
        <p><strong>Current Status:</strong> {invoice.status}</p>
      </div>

      <ErrorMessage message={error} />

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>New Status *</label>
          <select
            required
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            style={{ width: '100%', padding: '8px', fontSize: '14px' }}
          >
            <option value="draft">Draft</option>
            <option value="sent">Sent</option>
            <option value="paid">Paid</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            type="submit"
            disabled={submitting}
            style={{
              padding: '10px 20px',
              backgroundColor: '#3498db',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            {submitting ? 'Updating...' : 'Update Status'}
          </button>
          <button
            type="button"
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
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
