import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { clientApi } from '../api/clientApi';
import { invoiceApi } from '../api/invoiceApi';
import { Client } from '../types/Client';
import { LineItemCreateRequest } from '../types/Invoice';
import ErrorMessage from './ErrorMessage';
import LoadingSpinner from './LoadingSpinner';

export default function InvoiceForm() {
  const navigate = useNavigate();
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClientId, setSelectedClientId] = useState<number | ''>('');
  const [lineItems, setLineItems] = useState<LineItemCreateRequest[]>([
    { description: '', quantity: 1, unit_price: 0 },
  ]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingClients, setLoadingClients] = useState(true);

  useEffect(() => {
    loadClients();
  }, []);

  const loadClients = async () => {
    try {
      const data = await clientApi.getClients();
      setClients(data);
    } catch (err: any) {
      setError('Failed to load clients');
    } finally {
      setLoadingClients(false);
    }
  };

  const addLineItem = () => {
    setLineItems([...lineItems, { description: '', quantity: 1, unit_price: 0 }]);
  };

  const removeLineItem = (index: number) => {
    setLineItems(lineItems.filter((_, i) => i !== index));
  };

  const updateLineItem = (index: number, field: keyof LineItemCreateRequest, value: string | number) => {
    const updated = [...lineItems];
    updated[index] = { ...updated[index], [field]: value };
    setLineItems(updated);
  };

  const calculateTotal = () => {
    return lineItems.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0).toFixed(2);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedClientId === '') {
      setError('Please select a client');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const invoice = await invoiceApi.createInvoice({
        client_id: selectedClientId as number,
        line_items: lineItems,
      });
      alert(`Invoice ${invoice.invoice_number} created successfully!`);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create invoice');
    } finally {
      setLoading(false);
    }
  };

  if (loadingClients) return <LoadingSpinner />;

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2>Create New Invoice</h2>

      <ErrorMessage message={error} />

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Client *</label>
        <select
          required
          value={selectedClientId}
          onChange={(e) => setSelectedClientId(Number(e.target.value))}
          style={{ width: '100%', padding: '8px', fontSize: '14px' }}
        >
          <option value="">Select a client...</option>
          {clients.map((client) => (
            <option key={client.id} value={client.id}>
              {client.name} - {client.email}
            </option>
          ))}
        </select>
      </div>

      <h3>Line Items</h3>
      {lineItems.map((item, index) => (
        <div key={index} style={{
          border: '1px solid #ddd',
          padding: '15px',
          marginBottom: '10px',
          borderRadius: '4px'
        }}>
          <div style={{ marginBottom: '10px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>Description *</label>
            <input
              type="text"
              required
              value={item.description}
              onChange={(e) => updateLineItem(index, 'description', e.target.value)}
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '5px' }}>Quantity *</label>
              <input
                type="number"
                required
                min="0.01"
                step="0.01"
                value={item.quantity}
                onChange={(e) => updateLineItem(index, 'quantity', parseFloat(e.target.value))}
                style={{ width: '100%', padding: '8px', fontSize: '14px' }}
              />
            </div>

            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '5px' }}>Unit Price ($) *</label>
              <input
                type="number"
                required
                min="0"
                step="0.01"
                value={item.unit_price}
                onChange={(e) => updateLineItem(index, 'unit_price', parseFloat(e.target.value))}
                style={{ width: '100%', padding: '8px', fontSize: '14px' }}
              />
            </div>

            <div style={{ flex: 1, display: 'flex', alignItems: 'flex-end' }}>
              <div style={{ width: '100%' }}>
                <label style={{ display: 'block', marginBottom: '5px' }}>Amount</label>
                <div style={{ padding: '8px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
                  ${(item.quantity * item.unit_price).toFixed(2)}
                </div>
              </div>
            </div>
          </div>

          {lineItems.length > 1 && (
            <button
              type="button"
              onClick={() => removeLineItem(index)}
              style={{
                padding: '5px 10px',
                backgroundColor: '#e74c3c',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Remove
            </button>
          )}
        </div>
      ))}

      <button
        type="button"
        onClick={addLineItem}
        style={{
          padding: '10px 20px',
          backgroundColor: '#95a5a6',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          marginBottom: '20px',
        }}
      >
        Add Line Item
      </button>

      <div style={{
        padding: '15px',
        backgroundColor: '#f9f9f9',
        borderRadius: '4px',
        marginBottom: '20px',
        textAlign: 'right'
      }}>
        <h3>Total: ${calculateTotal()}</h3>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          {loading ? 'Creating...' : 'Create Invoice'}
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
  );
}
