const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const ExamResult = require('../models/ExamResult');
const User = require('../models/User');
const nodemailer = require('nodemailer');

const mailer = nodemailer.createTransport({
  host: process.env.SMTP_HOST || 'smtp.gmail.com',
  port: process.env.SMTP_PORT || 587,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
});

// Middleware: Verify JWT
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret-key');
    req.user = decoded;
    next();
  } catch(err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Submit exam result
router.post('/submit', authenticate, async (req, res) => {
  try {
    const { totalQuestions, timeLimit, passScore, correct, wrong, skipped, answers, timeUsed, mode } = req.body;

    const scorePercentage = Math.round((correct / totalQuestions) * 100);
    const passed = scorePercentage >= passScore;

    const user = await User.findById(req.user.userId);

    const result = new ExamResult({
      userId: req.user.userId,
      userEmail: user.email,
      userName: user.name,
      totalQuestions,
      timeLimit,
      passScore,
      correct,
      wrong,
      skipped,
      scorePercentage,
      passed,
      timeUsed,
      answers,
      startTime: new Date(Date.now() - timeUsed * 1000),
      endTime: new Date(),
      mode
    });

    await result.save();

    // Send result email (async, don't wait)
    sendResultEmail(user.email, user.name, result).catch(console.error);

    res.json({
      resultId: result._id,
      passed,
      scorePercentage
    });
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Get user's exam history
router.get('/history', authenticate, async (req, res) => {
  try {
    const results = await ExamResult.find({ userId: req.user.userId })
      .sort({ createdAt: -1 })
      .select('-answers');

    res.json(results);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Get specific exam result
router.get('/:resultId', authenticate, async (req, res) => {
  try {
    const result = await ExamResult.findOne({
      _id: req.params.resultId,
      userId: req.user.userId
    });

    if (!result) return res.status(404).json({ error: 'Result not found' });

    res.json(result);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Helper: Send result email
async function sendResultEmail(email, name, result) {
  const subject = result.passed ? '✓ Exam Passed!' : '✗ Exam Not Passed';
  const html = `
    <h2>${subject}</h2>
    <p>Hello ${name || 'User'},</p>
    <p>Your exam results are ready:</p>
    <ul>
      <li><strong>Score:</strong> ${result.scorePercentage}% (${result.passed ? 'PASSED' : 'NOT PASSED'})</li>
      <li><strong>Correct:</strong> ${result.correct}/${result.totalQuestions}</li>
      <li><strong>Wrong:</strong> ${result.wrong}</li>
      <li><strong>Skipped:</strong> ${result.skipped}</li>
      <li><strong>Time Used:</strong> ${Math.floor(result.timeUsed / 60)}m</li>
      <li><strong>Pass Score:</strong> ${result.passScore}%</li>
    </ul>
    <p><a href="${process.env.FRONTEND_URL || 'http://localhost:5000'}/results/${result._id}">View Full Results →</a></p>
  `;

  return mailer.sendMail({
    from: process.env.SMTP_USER,
    to: email,
    subject,
    html
  });
}

module.exports = router;
