const mongoose = require('mongoose');

const questionSchema = new mongoose.Schema({
  id: { type: Number, unique: true, required: true },
  question: { type: String, required: true },
  options: [{
    key: String,
    text: String,
    correct: Boolean
  }],
  answer: String,
  multi: Boolean,
  source: String, // 'V3', 'V4', etc

  // Admin notes
  verified: { type: Boolean, default: false },
  difficulty: { type: String, enum: ['easy', 'medium', 'hard'], default: 'medium' },
  topic: String,
  notes: String,
  reportCount: { type: Number, default: 0 },

  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

questionSchema.index({ topic: 1, verified: 1 });

module.exports = mongoose.model('Question', questionSchema);
