const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const ExamResult = require('../models/ExamResult');
const QuestionReport = require('../models/QuestionReport');
const User = require('../models/User');

// Middleware: Verify JWT and Admin
const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret-key');
    if (!decoded.isAdmin) return res.status(403).json({ error: 'Admin only' });
    req.user = decoded;
    next();
  } catch(err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Get all users with attempt stats
router.get('/users', authenticate, async (req, res) => {
  try {
    const users = await User.find().select('-passwordHash -otpCode');
    const stats = await Promise.all(users.map(async (user) => {
      const results = await ExamResult.find({ userId: user._id });
      const passCount = results.filter(r => r.passed).length;
      return {
        ...user.toObject(),
        attempts: results.length,
        passed: passCount,
        avgScore: results.length ? Math.round(results.reduce((sum, r) => sum + r.scorePercentage, 0) / results.length) : 0,
        lastAttempt: results.length ? results[0].createdAt : null
      };
    }));
    res.json(stats);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Get all exam results
router.get('/results', authenticate, async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = 20;
    const skip = (page - 1) * limit;

    const results = await ExamResult.find()
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .select('-answers');

    const total = await ExamResult.countDocuments();

    res.json({
      results,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) }
    });
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Get question reports
router.get('/reports', authenticate, async (req, res) => {
  try {
    const status = req.query.status || 'pending';
    const reports = await QuestionReport.find({ status })
      .sort({ createdAt: -1 })
      .limit(100);

    res.json(reports);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Update report status
router.patch('/reports/:reportId', authenticate, async (req, res) => {
  try {
    const { status, adminNotes } = req.body;
    const report = await QuestionReport.findByIdAndUpdate(
      req.params.reportId,
      {
        status,
        adminNotes,
        resolvedAt: status !== 'pending' ? new Date() : null
      },
      { new: true }
    );
    res.json(report);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Get dashboard stats
router.get('/dashboard/stats', authenticate, async (req, res) => {
  try {
    const totalUsers = await User.countDocuments();
    const totalAttempts = await ExamResult.countDocuments();
    const passedAttempts = await ExamResult.countDocuments({ passed: true });
    const pendingReports = await QuestionReport.countDocuments({ status: 'pending' });

    const avgScore = await ExamResult.aggregate([
      { $group: { _id: null, avg: { $avg: '$scorePercentage' } } }
    ]);

    res.json({
      totalUsers,
      totalAttempts,
      passedAttempts,
      passRate: totalAttempts ? Math.round((passedAttempts / totalAttempts) * 100) : 0,
      avgScore: avgScore[0]?.avg || 0,
      pendingReports
    });
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
