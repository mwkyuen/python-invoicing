import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { clientApi } from '../api/clientApi';
import { ClientCreateRequest } from '../types/Client';
import ErrorMessage from './ErrorMessage';

export default function ClientForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<ClientCreateRequest>({
    name: '',
    billing_address: '',
    email: '',
    phone_number: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await clientApi.createClient(formData);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create client');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h2>Create New Client</h2>

      <ErrorMessage message={error} />

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Name *</label>
        <input
          type="text"
          required
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          style={{ width: '100%', padding: '8px', fontSize: '14px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Billing Address *</label>
        <textarea
          required
          value={formData.billing_address}
          onChange={(e) => setFormData({ ...formData, billing_address: e.target.value })}
          style={{ width: '100%', padding: '8px', fontSize: '14px', minHeight: '80px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Email *</label>
        <input
          type="email"
          required
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          style={{ width: '100%', padding: '8px', fontSize: '14px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Phone Number *</label>
        <input
          type="tel"
          required
          value={formData.phone_number}
          onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
          style={{ width: '100%', padding: '8px', fontSize: '14px' }}
        />
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
          {loading ? 'Creating...' : 'Create Client'}
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
