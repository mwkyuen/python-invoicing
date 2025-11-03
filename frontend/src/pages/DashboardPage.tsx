import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { clientApi } from '../api/clientApi';
import { invoiceApi } from '../api/invoiceApi';
import { Client } from '../types/Client';
import { Invoice } from '../types/Invoice';
import LoadingSpinner from '../components/LoadingSpinner';
import InvoiceStatusBadge from '../components/InvoiceStatusBadge';
import ErrorMessage from '../components/ErrorMessage';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [clients, setClients] = useState<Client[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'clients' | 'invoices'>('invoices');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [clientsData, invoicesData] = await Promise.all([
        clientApi.getClients(),
        invoiceApi.getInvoices(),
      ]);
      setClients(clientsData);
      setInvoices(invoicesData);
    } catch (err: any) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async (invoiceId: number, invoiceNumber: string) => {
    try {
      const blob = await invoiceApi.downloadInvoicePDF(invoiceId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${invoiceNumber}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      alert('Failed to download PDF: ' + (err.response?.data?.detail || err.message));
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Invoicing Dashboard</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => navigate('/clients/new')}
            style={{
              padding: '10px 20px',
              backgroundColor: '#3498db',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            + New Client
          </button>
          <button
            onClick={() => navigate('/invoices/new')}
            style={{
              padding: '10px 20px',
              backgroundColor: '#2ecc71',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            + New Invoice
          </button>
        </div>
      </div>

      <ErrorMessage message={error} />

      {/* Tabs */}
      <div style={{ borderBottom: '2px solid #ddd', marginBottom: '20px' }}>
        <button
          onClick={() => setActiveTab('invoices')}
          style={{
            padding: '10px 20px',
            border: 'none',
            borderBottom: activeTab === 'invoices' ? '3px solid #3498db' : 'none',
            backgroundColor: 'transparent',
            cursor: 'pointer',
            fontWeight: activeTab === 'invoices' ? 'bold' : 'normal',
          }}
        >
          Invoices ({invoices.length})
        </button>
        <button
          onClick={() => setActiveTab('clients')}
          style={{
            padding: '10px 20px',
            border: 'none',
            borderBottom: activeTab === 'clients' ? '3px solid #3498db' : 'none',
            backgroundColor: 'transparent',
            cursor: 'pointer',
            fontWeight: activeTab === 'clients' ? 'bold' : 'normal',
          }}
        >
          Clients ({clients.length})
        </button>
      </div>

      {/* Invoices Tab */}
      {activeTab === 'invoices' && (
        <div>
          <h2>Invoices</h2>
          {invoices.length === 0 ? (
            <p>No invoices yet. Create one to get started!</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f5f5f5' }}>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Invoice #</th>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Client</th>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Date</th>
                  <th style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>Total</th>
                  <th style={{ padding: '10px', textAlign: 'center', border: '1px solid #ddd' }}>Status</th>
                  <th style={{ padding: '10px', textAlign: 'center', border: '1px solid #ddd' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {invoices.map((invoice) => {
                  const client = clients.find((c) => c.id === invoice.client_id);
                  return (
                    <tr key={invoice.id}>
                      <td style={{ padding: '10px', border: '1px solid #ddd' }}>{invoice.invoice_number}</td>
                      <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client?.name || 'Unknown'}</td>
                      <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                        {new Date(invoice.issue_date).toLocaleDateString()}
                      </td>
                      <td style={{ padding: '10px', textAlign: 'right', border: '1px solid #ddd' }}>
                        ${invoice.total_amount.toFixed(2)}
                      </td>
                      <td style={{ padding: '10px', textAlign: 'center', border: '1px solid #ddd' }}>
                        <InvoiceStatusBadge status={invoice.status} />
                      </td>
                      <td style={{ padding: '10px', textAlign: 'center', border: '1px solid #ddd' }}>
                        <button
                          onClick={() => navigate(`/invoices/${invoice.id}/edit`)}
                          style={{
                            padding: '5px 10px',
                            marginRight: '5px',
                            backgroundColor: '#3498db',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer',
                          }}
                        >
                          Edit Status
                        </button>
                        {invoice.pdf_path && (
                          <button
                            onClick={() => downloadPDF(invoice.id, invoice.invoice_number)}
                            style={{
                              padding: '5px 10px',
                              backgroundColor: '#2ecc71',
                              color: 'white',
                              border: 'none',
                              borderRadius: '4px',
                              cursor: 'pointer',
                            }}
                          >
                            Download PDF
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Clients Tab */}
      {activeTab === 'clients' && (
        <div>
          <h2>Clients</h2>
          {clients.length === 0 ? (
            <p>No clients yet. Create one to get started!</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f5f5f5' }}>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Name</th>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Email</th>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Phone</th>
                  <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Created</th>
                </tr>
              </thead>
              <tbody>
                {clients.map((client) => (
                  <tr key={client.id}>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.name}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.email}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.phone_number}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                      {new Date(client.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
