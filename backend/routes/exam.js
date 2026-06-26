const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const ExamResult = require('../models/ExamResult');
const User = require('../models/User');

async function sendEmail(to, subject, html) {
  const apiKey = process.env.SMTP_PASS;
  const fromEmail = process.env.FROM_EMAIL || 'noreply@sitecoreai-exam.com';

  const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: fromEmail },
      subject: subject,
      content: [{ type: 'text/html', value: html }]
    })
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`SendGrid API error: ${response.status} - ${error}`);
  }
}

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
    console.log('[EXAM] Result saved:', result._id);

    // Send result email (async, don't wait)
    console.log('[EXAM] Sending result email to:', user.email);
    sendResultEmail(user.email, user.name, result)
      .then(() => console.log('[EXAM] Result email sent successfully'))
      .catch(err => console.error('[EXAM] Result email error:', err.message));

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
  console.log('[EMAIL] Starting result email process for:', email);
  const subject = result.passed ? 'Exam Passed - ' + result.scorePercentage + '%!' : 'Exam Not Passed - ' + result.scorePercentage + '%';
  const statusColor = result.passed ? '#00c853' : '#f44336';
  const statusText = result.passed ? 'PASSED' : 'NOT PASSED';

  const html = '<html><body style="font-family: Arial, sans-serif; background: #f5f5f5; color: #333;">' +
    '<div style="max-width: 600px; margin: 20px auto; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">' +
    '<div style="background: #1a1d27; color: #fff; padding: 30px; text-align: center;">' +
    '<h1 style="margin: 0; font-size: 28px; font-weight: 700;">SitecoreAI Exam Results</h1>' +
    '</div>' +
    '<div style="padding: 30px;">' +
    '<p style="font-size: 16px; margin: 0 0 20px 0;">Hello ' + (name || 'User') + ',</p>' +
    '<p style="font-size: 14px; color: #666; margin: 0 0 20px 0;">Your SitecoreAI CMS Developer Certification exam has been completed. Here are your results:</p>' +
    '<div style="background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); border-left: 4px solid ' + statusColor + '; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">' +
    '<div style="font-size: 48px; font-weight: 700; color: ' + statusColor + '; margin: 10px 0;">' + result.scorePercentage + '%</div>' +
    '<div style="font-size: 18px; font-weight: 700; color: ' + statusColor + '; margin: 10px 0;">' + statusText + '</div>' +
    '<div style="font-size: 12px; color: #666;">Pass Score Required: ' + result.passScore + '%</div>' +
    '</div>' +
    '<table style="width: 100%; margin: 25px 0; border-collapse: collapse;">' +
    '<tr><td style="background: #f9f9f9; border: 1px solid #e0e0e0; padding: 15px; text-align: center;"><div style="font-size: 24px; font-weight: 700; color: #00c853;">' + result.correct + '</div><div style="font-size: 12px; color: #999; margin-top: 5px;">CORRECT</div></td>' +
    '<td style="background: #f9f9f9; border: 1px solid #e0e0e0; padding: 15px; text-align: center;"><div style="font-size: 24px; font-weight: 700; color: #f44336;">' + result.wrong + '</div><div style="font-size: 12px; color: #999; margin-top: 5px;">WRONG</div></td></tr>' +
    '<tr><td style="background: #f9f9f9; border: 1px solid #e0e0e0; padding: 15px; text-align: center;"><div style="font-size: 24px; font-weight: 700; color: #1a1d27;">' + result.totalQuestions + '</div><div style="font-size: 12px; color: #999; margin-top: 5px;">TOTAL</div></td>' +
    '<td style="background: #f9f9f9; border: 1px solid #e0e0e0; padding: 15px; text-align: center;"><div style="font-size: 24px; font-weight: 700; color: #1a1d27;">' + result.skipped + '</div><div style="font-size: 12px; color: #999; margin-top: 5px;">SKIPPED</div></td></tr>' +
    '</table>' +
    '<div style="text-align: center;">' +
    '<a href="https://sitecoreai-exam.vercel.app/dashboard.html" style="display: inline-block; background: #e53935; color: #fff; padding: 14px 32px; text-decoration: none; border-radius: 8px; font-weight: 700; margin-top: 20px;">View Full Results Dashboard</a>' +
    '</div>' +
    '</div>' +
    '<div style="background: #f5f5f5; padding: 20px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #e0e0e0;">' +
    '<p style="margin: 5px 0;">SitecoreAI CMS Developer Certification Exam Simulator</p>' +
    '<p style="margin: 5px 0;">© 2026 - All Rights Reserved</p>' +
    '</div>' +
    '</div>' +
    '</body></html>';

  console.log('[EMAIL] Calling sendEmail with subject:', subject);
  return sendEmail(email, subject, html);
}

module.exports = router;
