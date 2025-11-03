interface InvoiceStatusBadgeProps {
  status: string;
}

export default function InvoiceStatusBadge({ status }: InvoiceStatusBadgeProps) {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'draft':
        return '#gray';
      case 'sent':
        return '#3498db';
      case 'paid':
        return '#2ecc71';
      case 'cancelled':
        return '#e74c3c';
      default:
        return '#95a5a6';
    }
  };

  return (
    <span style={{
      padding: '4px 8px',
      borderRadius: '4px',
      backgroundColor: getStatusColor(status),
      color: 'white',
      fontSize: '12px',
      fontWeight: 'bold',
      textTransform: 'uppercase'
    }}>
      {status}
    </span>
  );
}
