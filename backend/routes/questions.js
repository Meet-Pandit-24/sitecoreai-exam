const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const Question = require('../models/Question');
const QuestionReport = require('../models/QuestionReport');

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

// Get all questions (public - for exam)
router.get('/', async (req, res) => {
  try {
    const questions = await Question.find().sort({ id: 1 });
    res.json(questions);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Get single question
router.get('/:id', async (req, res) => {
  try {
    const question = await Question.findOne({ id: parseInt(req.params.id) });
    if (!question) return res.status(404).json({ error: 'Question not found' });
    res.json(question);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Create question (admin only)
router.post('/', authenticate, async (req, res) => {
  try {
    const { id, question, options, answer, multi, source, difficulty, topic, notes } = req.body;

    if (!question || !options || !answer) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Get next ID if not provided
    const nextId = id || (await Question.findOne().sort({ id: -1 }).then(q => (q?.id || 0) + 1));

    const newQuestion = new Question({
      id: nextId,
      question,
      options,
      answer,
      multi: multi || false,
      source: source || 'admin',
      difficulty: difficulty || 'medium',
      topic,
      notes,
      verified: false
    });

    await newQuestion.save();
    res.status(201).json(newQuestion);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Update question (admin only)
router.patch('/:id', authenticate, async (req, res) => {
  try {
    const { question, options, answer, difficulty, topic, notes, verified } = req.body;

    const updated = await Question.findOneAndUpdate(
      { id: parseInt(req.params.id) },
      {
        ...(question && { question }),
        ...(options && { options }),
        ...(answer && { answer }),
        ...(difficulty && { difficulty }),
        ...(topic && { topic }),
        ...(notes && { notes }),
        ...(verified !== undefined && { verified }),
        updatedAt: new Date()
      },
      { new: true }
    );

    if (!updated) return res.status(404).json({ error: 'Question not found' });

    res.json(updated);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Delete question (admin only)
router.delete('/:id', authenticate, async (req, res) => {
  try {
    const deleted = await Question.findOneAndDelete({ id: parseInt(req.params.id) });
    if (!deleted) return res.status(404).json({ error: 'Question not found' });
    res.json({ message: 'Deleted', id: deleted.id });
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Report question issue (user)
router.post('/:id/report', async (req, res) => {
  try {
    const { issue, userId, userEmail } = req.body;

    if (!issue) return res.status(400).json({ error: 'Issue description required' });

    const report = new QuestionReport({
      questionId: parseInt(req.params.id),
      userId: userId || null,
      userEmail: userEmail || 'anonymous',
      issue
    });

    await report.save();

    // Increment report count
    await Question.findOneAndUpdate(
      { id: parseInt(req.params.id) },
      { $inc: { reportCount: 1 } }
    );

    res.status(201).json({ message: 'Report submitted', id: report._id });
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// Bulk import questions (admin only)
router.post('/bulk/import', authenticate, async (req, res) => {
  try {
    const { questions } = req.body;

    if (!Array.isArray(questions)) {
      return res.status(400).json({ error: 'Questions must be an array' });
    }

    const inserted = await Question.insertMany(questions, { ordered: false });

    res.status(201).json({
      message: `Imported ${inserted.length} questions`,
      count: inserted.length
    });
  } catch(err) {
    // Partial success ok
    if (err.writeErrors) {
      res.status(201).json({
        message: `Imported ${err.insertedDocs.length} of ${questions.length} questions`,
        count: err.insertedDocs.length,
        errors: err.writeErrors.length
      });
    } else {
      res.status(500).json({ error: err.message });
    }
  }
});

module.exports = router;
