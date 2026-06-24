const mongoose = require('mongoose');

const examResultSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  userEmail: String,
  userName: String,

  // Exam config
  totalQuestions: Number,
  timeLimit: Number,
  passScore: Number,

  // Results
  correct: Number,
  wrong: Number,
  skipped: Number,
  scorePercentage: Number,
  passed: Boolean,

  // Details
  timeUsed: Number, // in seconds
  answers: [{
    questionId: Number,
    selected: [String],
    correct: [String],
    isCorrect: Boolean,
    markedForReview: Boolean
  }],

  // Meta
  startTime: Date,
  endTime: Date,
  mode: { type: String, enum: ['exam', 'practice'] },
  createdAt: { type: Date, default: Date.now }
});

// Index for queries
examResultSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model('ExamResult', examResultSchema);
