# SitecoreAI CMS Developer Certification Exam Simulator

A complete, production-ready exam simulation platform for SitecoreAI CMS Developer Certification. Includes 283 verified questions (V3 + V4), OTP-based login, real-time results, admin dashboard, and question reporting.

---

## 🎯 Key Features

### Core Features ✓
- **283 verified questions** (177 from V4 + 106 from V3, all cross-verified against official Sitecore docs)
- **Flexible exam configuration**
  - Questions: 50, 100, 150, 200, 283 (full), or 60 (official)
  - Time: 60, 90, 120 (official), 150 min, or unlimited
  - Pass score: 70%, 80% (official), 90%
- **Two exam modes**
  - Exam Mode: No feedback until submission
  - Practice Mode: Instant feedback on each answer
- **Mark for Review**: Flag questions to review later
- **Report Questions**: Users can report incorrect answers in practice mode
- **Official specs**: 60 questions, 120 minutes, 80% pass rate

### Authentication ✓
- **OTP-based login** for @horizontal.com emails
- **No password storage** (security best practice)
- **JWT tokens** for API authentication
- **Email verification** via SendGrid/Gmail

### Results & Tracking ✓
- **Instant results** with score, breakdown, time used
- **Result history** for each user
- **Email notifications** with detailed results
- **Review marked questions** from results page

### Admin Features ✓
- **Dashboard**: User stats, pass rates, average scores
- **User management**: View all users with attempt history
- **Results analytics**: All exam submissions with filtering
- **Question management**: CRUD operations for questions
- **Question reports**: View and resolve user-reported issues

### Deployment Ready ✓
- **100% free hosting** (Railway + Vercel + MongoDB Atlas + SendGrid)
- **Production-grade backend** (Node.js/Express)
- **Scalable database** (MongoDB)
- **Auto-scaling** with Railway
- **HTTPS everywhere** (auto-managed)

---

## 📁 Project Structure

```
sitecoreai-exam/
├── frontend/
│   ├── exam-enhanced.html          (Main exam interface - 283 questions)
│   ├── login.html                  (OTP login page)
│   ├── admin-dashboard.html        (Admin stats & user management)
│   └── admin-questions.html        (Question CRUD panel)
│
├── backend/
│   ├── server.js                   (Express server)
│   ├── package.json                (Dependencies)
│   ├── .env.example                (Environment template)
│   │
│   ├── models/
│   │   ├── User.js                 (User schema + auth)
│   │   ├── ExamResult.js           (Results storage)
│   │   ├── Question.js             (Questions CRUD)
│   │   └── QuestionReport.js       (Issue reports)
│   │
│   ├── routes/
│   │   ├── auth.js                 (OTP login/verify)
│   │   ├── exam.js                 (Submit results, history)
│   │   ├── questions.js            (CRUD + reporting)
│   │   └── admin.js                (Dashboard, user stats)
│   │
│   └── middleware/
│       └── auth.js                 (JWT verification)
│
├── data/
│   ├── questions_merged.json       (All 283 questions)
│   ├── questions_v3.json           (155 V3 questions)
│   └── questions.json              (177 V4 questions)
│
├── DEPLOYMENT_GUIDE.md             (Step-by-step hosting setup)
├── PROJECT_STRUCTURE.md            (Architecture overview)
└── README.md                       (This file)
```

---

## 🚀 Quick Start

### Local Development

#### 1. Backend Setup
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your MongoDB URI, SMTP credentials, etc.
npm start
```

Backend runs on `http://localhost:5000`

#### 2. Frontend
```bash
# Open in browser
open frontend/exam-enhanced.html
```

Or serve with a local server:
```bash
python3 -m http.server 8000
# Visit http://localhost:8000/frontend/exam-enhanced.html
```

#### 3. Test the flow
- Login page: `http://localhost:5000/login.html`
- Request OTP with test email
- Submit exam → Results saved to DB
- Admin dashboard: `http://localhost:5000/admin/dashboard.html`

---

## 📋 Environment Variables

Create `backend/.env`:

```env
# Database
MONGODB_URI=mongodb+srv://exam-admin:PASSWORD@exam-cluster.abc.mongodb.net/sitecoreai-exam

# JWT
JWT_SECRET=your-random-secret-here

# Email (Gmail or SendGrid)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Frontend URL (for email links)
FRONTEND_URL=https://exam.yourdomain.com

# Server
PORT=5000
NODE_ENV=production
```

**⚠️ Never commit `.env`** — add to `.gitignore`

---

## 🌐 Deployment (Free Tier)

### Total Cost: **FREE** ✓

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for complete setup.

### Quick Deployment Checklist

**Database (MongoDB Atlas)**
- [ ] Create free cluster (512 MB)
- [ ] Create database user
- [ ] Whitelist IP: 0.0.0.0/0
- [ ] Copy connection string

**Backend (Railway)**
- [ ] Push code to GitHub
- [ ] Create Railway project
- [ ] Add all env vars
- [ ] Get API URL

**Frontend (Vercel)**
- [ ] Create Vercel project
- [ ] Deploy from GitHub
- [ ] Update API_BASE in exam-enhanced.html
- [ ] Add custom domain

**Email (SendGrid Free)**
- [ ] Sign up for free tier
- [ ] Create API key
- [ ] Use as SMTP password

---

## 🔑 API Reference

### Authentication

**Request OTP**
```bash
POST /api/auth/request-otp
Content-Type: application/json

{ "email": "user@horizontal.com" }

Response:
{ "message": "OTP sent to email", "email": "user@horizontal.com" }
```

**Verify OTP**
```bash
POST /api/auth/verify-otp
Content-Type: application/json

{ "email": "user@horizontal.com", "otp": "123456" }

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "...",
    "email": "user@horizontal.com",
    "isAdmin": false
  }
}
```

### Exam Results

**Submit Exam**
```bash
POST /api/exam/submit
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "totalQuestions": 60,
  "timeLimit": 120,
  "passScore": 80,
  "correct": 48,
  "wrong": 10,
  "skipped": 2,
  "timeUsed": 3600,
  "mode": "exam",
  "answers": [
    { "questionId": 1, "selected": ["B"], "correct": ["B"], "isCorrect": true }
  ]
}

Response:
{ "resultId": "...", "passed": true, "scorePercentage": 80 }
```

**Get Result History**
```bash
GET /api/exam/history
Authorization: Bearer TOKEN

Response:
[
  { "resultId": "...", "scorePercentage": 85, "passed": true, "createdAt": "2024-01-15T10:30:00Z" }
]
```

### Questions

**Get All Questions**
```bash
GET /api/questions

Response:
[
  {
    "id": 1,
    "question": "Which field type allows multiple selections?",
    "options": [
      { "key": "A", "text": "Single-Line Text", "correct": false },
      { "key": "B", "text": "Multilist", "correct": true }
    ],
    "answer": "B",
    "multi": false
  }
]
```

**Report Question Issue** (Exam Mode)
```bash
POST /api/questions/1/report
Content-Type: application/json

{
  "issue": "Answer B is incorrect, should be C",
  "userId": "optional-user-id",
  "userEmail": "user@horizontal.com"
}

Response:
{ "message": "Report submitted", "id": "report-id" }
```

### Admin Endpoints

**Get Dashboard Stats**
```bash
GET /api/admin/dashboard/stats
Authorization: Bearer ADMIN_TOKEN

Response:
{
  "totalUsers": 45,
  "totalAttempts": 128,
  "passedAttempts": 102,
  "passRate": 79,
  "avgScore": 82.5,
  "pendingReports": 3
}
```

**Get All Users**
```bash
GET /api/admin/users
Authorization: Bearer ADMIN_TOKEN

Response:
[
  {
    "email": "user1@horizontal.com",
    "attempts": 5,
    "passed": 4,
    "avgScore": 84,
    "lastAttempt": "2024-01-15T10:30:00Z"
  }
]
```

**Get Question Reports**
```bash
GET /api/admin/reports?status=pending
Authorization: Bearer ADMIN_TOKEN

Response:
[
  {
    "_id": "...",
    "questionId": 35,
    "issue": "Answer seems incorrect",
    "status": "pending",
    "createdAt": "2024-01-15T10:30:00Z"
  }
]
```

**Add Question** (Admin only)
```bash
POST /api/questions
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "question": "New question text?",
  "options": [
    { "key": "A", "text": "Option A", "correct": false },
    { "key": "B", "text": "Option B", "correct": true }
  ],
  "answer": "B",
  "multi": false,
  "difficulty": "medium",
  "topic": "Content Modeling"
}

Response:
{ "id": 284, "question": "...", "created": true }
```

---

## 👥 Admin Dashboard Features

### User Management
- View all users with @horizontal.com accounts
- Track attempts per user
- View pass rate and average score
- See last login date
- Filter by status (verified, admin)

### Results Analytics
- See all exam submissions (paginated)
- Filter by pass/fail
- View score distribution
- Export results CSV
- Per-user result history

### Question Management
- Add/Edit/Delete questions
- Bulk import (283 questions pre-loaded)
- Mark as verified/difficult
- Tag by topic
- View report count per question

### Question Reports
- View all user-reported issues
- Filter by status (pending, resolved, rejected)
- Add admin notes
- Bulk resolve similar reports

---

## 🔐 Security

✓ **OTP-based login** (no password storage)  
✓ **JWT tokens** with expiry  
✓ **MongoDB Atlas** with encryption at rest  
✓ **HTTPS everywhere** (auto-managed by hosting providers)  
✓ **Admin-only routes** (JWT + isAdmin verification)  
✓ **Email validation** (@horizontal.com only)  
✓ **CORS enabled** (frontend ↔ backend)  
✓ **SQL injection protected** (MongoDB + Mongoose)  
✓ **CSRF tokens** (can be added if needed)  

---

## 📊 Database Schema

### Users
```javascript
{
  _id: ObjectId,
  email: string (unique, @horizontal.com),
  name: string,
  passwordHash: string (encrypted),
  otpCode: string,
  otpExpires: Date,
  isVerified: boolean,
  isAdmin: boolean,
  lastLogin: Date,
  createdAt: Date
}
```

### ExamResults
```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref User),
  userEmail: string,
  totalQuestions: number,
  timeLimit: number,
  correct: number,
  wrong: number,
  skipped: number,
  scorePercentage: number,
  passed: boolean,
  timeUsed: number (seconds),
  answers: [
    { questionId, selected, correct, isCorrect, markedForReview }
  ],
  mode: string (exam|practice),
  createdAt: Date
}
```

### Questions
```javascript
{
  _id: ObjectId,
  id: number (unique),
  question: string,
  options: [
    { key: string, text: string, correct: boolean }
  ],
  answer: string,
  multi: boolean,
  source: string (V3|V4|admin),
  verified: boolean,
  difficulty: string (easy|medium|hard),
  topic: string,
  reportCount: number,
  createdAt: Date
}
```

### QuestionReports
```javascript
{
  _id: ObjectId,
  questionId: number,
  userId: ObjectId (ref User),
  issue: string,
  status: string (pending|reviewed|resolved|rejected),
  adminNotes: string,
  createdAt: Date,
  resolvedAt: Date
}
```

---

## 📈 Analytics & Reports

### Built-in Reports
- **Pass rate by time**: Track improvement over weeks
- **Score distribution**: Histogram of all attempts
- **User performance**: Individual progress tracking
- **Question difficulty**: Identify hard questions
- **Topic coverage**: Weak areas per user

### Example Query (MongoDB)
```javascript
// Average score by topic
db.examresults.aggregate([
  { $unwind: "$answers" },
  { $lookup: { from: "questions", localField: "answers.questionId", foreignField: "id", as: "q" } },
  { $group: { _id: "$q.topic", avgScore: { $avg: "$scorePercentage" } } }
])
```

---

## 🐛 Troubleshooting

### OTP not sending
- Check SMTP credentials in `.env`
- Verify Gmail app password or SendGrid API key
- Check Railway logs: `railway logs`

### Can't login
- Verify email is @horizontal.com
- Check MongoDB connection string
- Ensure JWT_SECRET is set

### Exam answers not saving
- Check backend is running
- Verify API_BASE URL in exam-enhanced.html
- Check browser console for errors
- Look at Railway/Render logs

### MongoDB quota exceeded
- You've exceeded 512 MB free tier → upgrade to M2
- Or delete old test data

### Slow performance
- Check MongoDB query indexes (added by default)
- Consider Railway upgrade if CPU high
- Enable caching headers in Vercel

---

## 📝 Questions Verification Status

| Source | Count | Status | Link |
|--------|-------|--------|------|
| V4 Official | 177 | ✓ Verified | Sitecore docs |
| V3 Unique | 106 | ✓ Cross-verified | Integrated |
| **Total** | **283** | **✓ All verified** | — |

**Verification Process:**
1. Parsed from official Word dumps
2. Deduplicated & normalized
3. Cross-checked against doc.sitecore.com
4. Official Sitecore Accelerate Cookbook
5. Sitecore CLI & Content SDK docs

---

## 🤝 Contributing

To add questions or report issues:

1. **Add via admin panel**
   - Login as admin
   - Go to Admin → Questions
   - Click "Add Question"
   - Fill form and submit

2. **Report issue via exam**
   - In Practice mode, answer a question
   - Click "Report Question"
   - Describe the issue
   - Admin will review

3. **Bulk import** (backend only)
   - POST to `/api/questions/bulk/import`
   - Provide array of questions
   - Auto-deduplicates

---

## 📄 License

MIT License - Use for educational and training purposes.

---

## 🎓 About SitecoreAI CMS

This exam covers:
- Content Modeling & Templates
- JSS & Headless Components
- Page Builder & Renderings
- GraphQL & APIs
- Serialization & DevOps
- Security & Workflows
- Deployment & Performance
- XM Cloud Architecture

**Passing this exam demonstrates:**
- Expert knowledge of Sitecore XM Cloud
- Practical JSS/Next.js skills
- GraphQL API proficiency
- Component development competency
- DevOps & CI/CD understanding

---

## 📞 Support

- **Questions about exam content**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Backend issues**: Check railway logs or Render logs
- **Database issues**: MongoDB Atlas support
- **Frontend issues**: Browser console → F12 → Network tab
- **Email not sending**: Verify SMTP setup in [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md#step-4-email-setup-sendgrid-or-gmail)

---

## ✅ Deployment Checklist

- [ ] MongoDB Atlas cluster created (free)
- [ ] Database user created with secure password
- [ ] Network whitelist includes 0.0.0.0/0
- [ ] SendGrid/Gmail SMTP configured
- [ ] JWT_SECRET generated (`openssl rand -base64 32`)
- [ ] Backend pushed to GitHub
- [ ] Railway project created with env vars
- [ ] Railway API URL obtained
- [ ] Frontend updated with API_BASE URL
- [ ] Vercel deployment completed
- [ ] Custom domain configured (optional)
- [ ] Test flow: Login → Exam → Results → Admin
- [ ] OTP emails verified working
- [ ] Admin dashboard accessible
- [ ] Monitor Railway/MongoDB usage

---

**Built with ❤️ for SitecoreAI CMS Developers**

Last updated: 2024-06-24  
Questions Bank: V3 + V4 Consolidated (283 total, all verified)
