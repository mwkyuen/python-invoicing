import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import CreateClientPage from './pages/CreateClientPage';
import CreateInvoicePage from './pages/CreateInvoicePage';
import UpdateInvoicePage from './pages/UpdateInvoicePage';

function App() {
  return (
    <BrowserRouter>
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#f5f5f5'
      }}>
        <nav style={{
          backgroundColor: '#2c3e50',
          padding: '15px 20px',
          color: 'white',
          marginBottom: '20px'
        }}>
          <h1 style={{ margin: 0 }}>Python Invoicing System</h1>
        </nav>

        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/clients/new" element={<CreateClientPage />} />
          <Route path="/invoices/new" element={<CreateInvoicePage />} />
          <Route path="/invoices/:id/edit" element={<UpdateInvoicePage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
