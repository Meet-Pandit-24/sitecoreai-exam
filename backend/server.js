const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const mongoose = require('mongoose');
const path = require('path');

dotenv.config();

console.log('🚀 Starting SitecoreAI Backend Server...');
console.log('Environment:', process.env.NODE_ENV || 'development');
console.log('MongoDB URI:', process.env.MONGODB_URI ? '✅ Configured' : '❌ Missing');

const app = express();

// Middleware
// CORS Configuration
const corsOptions = {
  origin: function(origin, callback) {
    const allowedOrigins = [
      'https://sitecoreai-exam.onrender.com',
      'https://sitecoreai-exam.vercel.app',
      'http://localhost:3000',
      'http://localhost:3001',
      'http://localhost'
    ];

    if (!origin || allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'Accept'],
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
app.options('*', cors(corsOptions));
app.use(express.json());

// Database Connection
const mongoURI = process.env.MONGODB_URI || 'mongodb+srv://user:pass@cluster.mongodb.net/sitecoreai-exam';
console.log('📚 Connecting to MongoDB...');

mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('✅ MongoDB Connected'))
.catch(err => {
  console.error('❌ MongoDB Connection Error:', err.message);
  console.error('URI Preview:', mongoURI.substring(0, 50) + '...');
});

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
