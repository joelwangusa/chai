export default function Message({ sender, message }) {
  return (
    <div className={`message ${sender === 'Bot' ? 'bot' : 'user'}`}>
      <div className="message-content">
        <strong>{sender}:</strong> {message}
      </div>
      <style jsx>{`
        .message {
          display: flex;
          justify-content: ${sender === 'Bot' ? 'flex-start' : 'flex-end'};
          margin-bottom: 30px;
        }
        .message-content {
          max-width: 100%; // Adjust this value as needed
        }
      `}</style>
    </div>
  );
}