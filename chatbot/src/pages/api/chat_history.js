import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { page, size } = req.query;
    try {
      const response = await axios.get(`http://localhost:8000/chat_history?page=${page}&size=${size}`);
      res.status(200).json(response.data);
    } catch (error) {
      res.status(500).json({ error: 'Error fetching chat history' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
