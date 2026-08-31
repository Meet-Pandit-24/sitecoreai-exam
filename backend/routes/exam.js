const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const ExamResult = require('../models/ExamResult');
const User = require('../models/User');

async function sendEmail(to, subject, html) {
  console.log('[Email-DEBUG] ===== START SENDGRID EMAIL SEND =====');
  const apiKey = process.env.SMTP_PASS;
  const fromEmail = process.env.FROM_EMAIL || 'noreply@sitecoreai-exam.com';

  console.log('[Email-DEBUG] API Key:', apiKey ? 'EXISTS-' + apiKey.substring(0, 10) : 'MISSING!!');
  console.log('[Email-DEBUG] FROM_EMAIL:', fromEmail);
  console.log('[Email-DEBUG] TO_EMAIL:', to);
  console.log('[Email-DEBUG] SUBJECT:', subject);

  const payload = {
    personalizations: [{ to: [{ email: to }] }],
    from: { email: fromEmail },
    subject: subject,
    content: [{ type: 'text/html', value: html }]
  };

  try {
    console.log('[Email-DEBUG] Making SendGrid API call...');
    const response = await fetch('https://api.sendgrid.com/v3/mail/send', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    console.log('[Email-DEBUG] Response Status Code:', response.status);
    const responseText = await response.text();
    console.log('[Email-DEBUG] Response Body:', responseText);

    if (!response.ok) {
      console.log('[Email-DEBUG] ERROR: NOT OK RESPONSE');
      throw new Error(`SendGrid API error: ${response.status} - ${responseText}`);
    }
    console.log('[Email-DEBUG] ===== SUCCESS: EMAIL SENT =====');
  } catch(err) {
    console.error('[Email-DEBUG] CATCH ERROR:', err.message);
    console.error('[Email-DEBUG] Stack:', err.stack);
    throw err;
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
    const emailEnabled = process.env.EMAIL_ENABLED !== 'false';
    console.log('[EXAM-DEBUG] EMAIL_ENABLED env:', process.env.EMAIL_ENABLED);
    console.log('[EXAM-DEBUG] emailEnabled boolean:', emailEnabled);
    if (emailEnabled) {
      console.log('[EXAM] Sending result email to:', user.email);
      sendResultEmail(user.email, user.name, result)
        .then(() => console.log('[EXAM] Result email sent successfully'))
        .catch(err => console.error('[EXAM] Result email error:', err.message));
    } else {
      console.log('[EXAM] ⚠️ EMAIL DISABLED - Result email not sent');
    }

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

  const html = '<h2>' + (result.passed ? 'Exam Passed!' : 'Exam Not Passed') + '</h2>' +
    '<p>Hello ' + (name || 'User') + ',</p>' +
    '<p>Your exam results are ready:</p>' +
    '<ul>' +
    '<li><strong>Score:</strong> ' + result.scorePercentage + '% (' + statusText + ')</li>' +
    '<li><strong>Correct:</strong> ' + result.correct + '/' + result.totalQuestions + '</li>' +
    '<li><strong>Wrong:</strong> ' + result.wrong + '</li>' +
    '<li><strong>Skipped:</strong> ' + result.skipped + '</li>' +
    '<li><strong>Time Used:</strong> ' + Math.floor(result.timeUsed / 60) + 'm</li>' +
    '<li><strong>Pass Score:</strong> ' + result.passScore + '%</li>' +
    '</ul>' +
    '<p><a href="https://sitecoreai-exam.vercel.app/dashboard.html">View Full Results Dashboard</a></p>';

  console.log('[EMAIL] Calling sendEmail with subject:', subject);
  return sendEmail(email, subject, html);
}

module.exports = router;
