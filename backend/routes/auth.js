const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const User = require('../models/User');

async function sendEmail(to, subject, html) {
  const apiKey = process.env.SMTP_PASS;
  const fromEmail = process.env.FROM_EMAIL || 'noreply@sitecoreai-exam.com';

  console.log('[Email] Sending via SendGrid API');
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
  console.log('[Email] Sent successfully via SendGrid API');
}

// Request OTP
router.post('/request-otp', async (req, res) => {
  try {
    const { email } = req.body;
    console.log('[OTP] Request started for:', email);

    // Verify email is from allowed domain
    if (!email.endsWith('@horizontal.com')) {
      console.log('[OTP] Invalid domain:', email);
      return res.status(403).json({ error: 'Only @horizontal.com emails allowed' });
    }

    // Generate 6-digit OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const expiry = new Date(Date.now() + 15 * 60000); // 15 minutes
    console.log('[OTP] Generated OTP:', otp);

    console.log('[OTP] Querying database...');
    let user = await User.findOne({ email });
    if (!user) {
      user = new User({ email, otpCode: otp, otpExpires: expiry });
    } else {
      user.otpCode = otp;
      user.otpExpires = expiry;
    }
    await user.save();
    console.log('[OTP] User saved to database');

    // Send OTP email
    console.log('[OTP] Sending email from:', process.env.FROM_EMAIL, 'to:', email);
    await sendEmail(email, 'SitecoreAI Exam - Login Code', `
      <h2>Your OTP Code</h2>
      <p>Use this code to log in: <strong>${otp}</strong></p>
      <p>Code expires in 15 minutes.</p>
    `);
    console.log('[OTP] Email sent successfully');

    res.json({ message: 'OTP sent to email', email });
  } catch(err) {
    console.error('[OTP] Error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// Verify OTP
router.post('/verify-otp', async (req, res) => {
  try {
    const { email, otp } = req.body;

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    if (user.otpCode !== otp || new Date() > user.otpExpires) {
      return res.status(401).json({ error: 'Invalid or expired OTP' });
    }

    user.isVerified = true;
    user.lastLogin = new Date();
    user.otpCode = null;
    user.otpExpires = null;
    await user.save();

    const token = jwt.sign(
      { userId: user._id, email: user.email, isAdmin: user.isAdmin },
      process.env.JWT_SECRET || 'secret-key',
      { expiresIn: '7d' }
    );

    res.json({
      token,
      user: {
        id: user._id,
        email: user.email,
        name: user.name,
        isAdmin: user.isAdmin
      }
    });
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Verify token
router.get('/verify', (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token' });

    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret-key');
    res.json({ valid: true, user: decoded });
  } catch(err) {
    res.status(401).json({ error: 'Invalid token' });
  }
});

module.exports = router;
