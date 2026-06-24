# SitecoreAI Exam Simulator - Full Stack Architecture

## Structure
```
sitecoreai-exam/
├── frontend/
│   ├── index.html (main exam page)
│   ├── login.html (OTP login)
│   ├── admin/
│   │   ├── dashboard.html (results & user stats)
│   │   ├── questions.html (CRUD panel)
│   └── css/, js/ (assets)
├── backend/
│   ├── server.js (main Express server)
│   ├── routes/
│   │   ├── auth.js (OTP login)
│   │   ├── exam.js (exam endpoints)
│   │   ├── admin.js (admin panel)
│   │   └── questions.js (CRUD)
│   ├── models/
│   │   ├── User.js
│   │   ├── ExamResult.js
│   │   ├── Question.js
│   │   └── QuestionReport.js
│   ├── middleware/
│   │   └── auth.js
│   ├── config/
│   │   └── db.js
│   └── package.json
└── README.md
```

## Stack Choice
- **Frontend**: Vanilla JS + HTML5 (lightweight, no build step needed)
- **Backend**: Node.js + Express (simple, free tier hosting available)
- **Database**: MongoDB Atlas (free 512MB tier)
- **Auth**: OTP via email (SendGrid free tier or Mailgun)
- **Hosting**: 
  - Frontend: Vercel/Netlify (free)
  - Backend: Railway/Render (free tier)
  - Database: MongoDB Atlas (free)

## Timeline
1. Update HTML with new features (dropdowns, mark for review, report)
2. Create backend API structure
3. Database schema
4. Deployment setup
