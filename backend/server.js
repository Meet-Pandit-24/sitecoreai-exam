const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const path = require('path');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Database Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb+srv://user:pass@cluster.mongodb.net/sitecoreai-exam', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).catch(err => console.error('DB Connection Error:', err));

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/exam', require('./routes/exam'));
app.use('/api/admin', require('./routes/admin'));
app.use('/api/questions', require('./routes/questions'));

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected'
  });
});

// Database health check
app.get('/api/health/db', async (req, res) => {
  try {
    const state = mongoose.connection.readyState;
    const states = { 0: 'disconnected', 1: 'connected', 2: 'connecting', 3: 'disconnecting' };
    res.json({
      status: 'ok',
      mongodb: {
        state: states[state],
        connected: state === 1
      },
      timestamp: new Date().toISOString()
    });
  } catch(err) {
    res.status(500).json({
      status: 'error',
      mongodb: { connected: false, error: err.message },
      timestamp: new Date().toISOString()
    });
  }
});

// Serve static frontend (in production)
app.use(express.static(path.join(__dirname, '../frontend')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/exam-enhanced.html'));
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: err.message });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✓ Server running on port ${PORT}`);
  console.log(`  Health check: http://localhost:${PORT}/api/health`);
});
