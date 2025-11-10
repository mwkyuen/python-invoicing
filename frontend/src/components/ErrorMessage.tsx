interface ErrorMessageProps {
  message: string;
}

export default function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) return null;

  return (
    <div style={{
      padding: '10px',
      marginBottom: '15px',
      backgroundColor: '#fee',
      border: '1px solid #fcc',
      borderRadius: '4px',
      color: '#c00'
    }}>
      {message}
    </div>
  );
}
