const mongoose = require('mongoose');

const questionReportSchema = new mongoose.Schema({
  questionId: { type: Number, required: true },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  userEmail: String,

  issue: { type: String, required: true },
  status: { type: String, enum: ['pending', 'reviewed', 'resolved', 'rejected'], default: 'pending' },
  adminNotes: String,

  createdAt: { type: Date, default: Date.now },
  resolvedAt: Date
});

questionReportSchema.index({ questionId: 1, status: 1 });
questionReportSchema.index({ createdAt: -1 });

module.exports = mongoose.model('QuestionReport', questionReportSchema);
