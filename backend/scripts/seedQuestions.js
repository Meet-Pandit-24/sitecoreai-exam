#!/usr/bin/env node

const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const Question = require('../models/Question');
require('dotenv').config();

async function seedQuestions() {
  try {
    console.log('🔌 Connecting to MongoDB...');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB');

    // Drop old index if it exists
    try {
      console.log('🔧 Removing old indexes...');
      await Question.collection.dropIndex('id_1');
      console.log('✅ Old index removed');
    } catch(err) {
      // Index doesn't exist, that's fine
    }

    // Read exam-enhanced.html file
    const htmlPath = path.join(__dirname, '../../frontend/exam-enhanced.html');
    const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

    // Extract ALL_QUESTIONS array from HTML
    const match = htmlContent.match(/const ALL_QUESTIONS = \[([\s\S]*?)\];/);
    if (!match) {
      throw new Error('Could not find ALL_QUESTIONS in exam-enhanced.html');
    }

    const questionsJson = '[' + match[1] + ']';
    const allQuestions = JSON.parse(questionsJson);
    console.log(`📖 Found ${allQuestions.length} questions in exam-enhanced.html`);

    // Convert to new schema format
    const convertedQuestions = allQuestions.map(q => ({
      question: q.question,
      options: q.options.map(opt => opt.text),
      correctAnswer: q.answer,
      category: 'Sitecore CMS',
      difficulty: q.multi ? 'hard' : 'medium',
      verified: true
    }));

    // Clear existing questions
    const deleteResult = await Question.deleteMany({});
    console.log(`🗑️  Deleted ${deleteResult.deletedCount} existing questions`);

    // Insert all questions
    const insertResult = await Question.insertMany(convertedQuestions);
    console.log(`✅ Imported ${insertResult.length} questions into database`);

    // Display sample
    console.log('\n📊 Sample questions imported:');
    insertResult.slice(0, 3).forEach((q, i) => {
      console.log(`\n${i+1}. ${q.question.substring(0, 80)}...`);
      console.log(`   Options: ${q.options.join(' | ')}`);
      console.log(`   Answer: ${q.correctAnswer}`);
    });

    console.log(`\n✨ Migration complete! ${insertResult.length} questions are ready in the database.`);
    await mongoose.connection.close();
  } catch(err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

seedQuestions();
