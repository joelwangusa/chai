// components/ChatBox.js

import { useState, useEffect } from 'react';
import axios from 'axios';
import Message from './Message';

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [summary, setSummary] = useState('');
  const [page, setPage] = useState(0);

  useEffect(() => {
    fetchChatHistory();
  }, [page]);

  const fetchChatHistory = async () => {
    try {
      const response = await axios.get(`/api/chat_history?page=${page}&size=10`);
      setMessages(response.data.chat_history);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!input) return;
    try {
      const response = await axios.post('/api/chat', { input_text: input });
      setMessages([...messages, { sender: 'User', message: input }, { sender: 'Bot', message: response.data.response }]);
      setInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleGetSummary = async () => {
    try {
      const response = await axios.post('/api/summary', { chat_history: messages });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error getting summary:', error);
    }
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} message={msg.message} />
        ))}
      </div>
      <div className="summary-content">
        {summary && <div className="summary"><strong>Summary:</strong> {summary}</div>}
      </div>
      <div className="summary">
        <button onClick={handleGetSummary}>Get Summary</button>
      </div>
      <div className="input-container">
        <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
      <style jsx>{`
        .chatbox {
          display: flex;
          flex-direction: column;
          height: 80vh;
          width:100%;
          padding: 20px;
          box-sizing: border-box;
        }
        .messages {
          flex: 1;
          overflow-y: scroll;
          margin-bottom: 20px;
        }
        input {
          padding: 10px;
          margin-bottom: 10px;
          width: calc(100% - 100px);
          box-sizing: border-box;
        }
        button {
          padding: 10px;
          width: 80px;
        }
      `}</style>
    </div>
  );
}
