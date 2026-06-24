# Quick Start Guide - SitecoreAI Exam Simulator

## 🚀 Get Running in 5 Minutes (Local)

### Step 1: Backend Setup
```bash
cd backend
npm install
cp .env.example .env

# Edit .env - for local testing, use:
# MONGODB_URI=mongodb://localhost:27017/sitecoreai-exam (or MongoDB Atlas free tier)
# JWT_SECRET=test-secret-key
# SMTP_USER=your-email@gmail.com
# SMTP_PASS=your-app-password

npm start
# ✓ Server running on port 5000
```

### Step 2: Frontend
Open in browser:
```
file:///C:/Projects/SitecoreAI/frontend/exam-enhanced.html
```

Or serve locally:
```bash
# In new terminal
python3 -m http.server 8000
# Visit http://localhost:8000/frontend/exam-enhanced.html
```

### Step 3: Test Flow
1. Select exam config (60 questions, 120 min, 80% pass)
2. Click "Start Exam"
3. Answer a few questions (pick option with ✓ for correct)
4. Mark some for review (press M)
5. Click "Submit Exam"
6. See results page

---

## 🌐 Deploy to Production (20 Minutes)

### Option 1: MongoDB Atlas (Database)

**Create Free Cluster:**
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up → Create Project
3. Build Database → M0 Free Tier
4. Create database user (exam-admin / secure-password)
5. Network Access → Allow 0.0.0.0/0
6. Get connection string (copy it)

### Option 2: Railway (Backend)

**Deploy Backend:**
1. Push code to GitHub (`git push`)
2. Go to https://railway.app
3. New Project → Deploy from GitHub
4. Select your repo
5. Add variables:
   ```
   MONGODB_URI=<from Atlas>
   JWT_SECRET=<run: openssl rand -base64 32>
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASS=<Gmail app password>
   FRONTEND_URL=https://your-domain.com
   ```
6. Wait for deploy → Copy API URL

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Auth (if not already)
3. Create App Password (Mail, Windows Computer)
4. Use this as SMTP_PASS in Railway

### Option 3: Vercel (Frontend)

**Deploy Frontend:**
1. Push to GitHub
2. Go to https://vercel.com
3. New Project → Import from GitHub
4. Select repo → Deploy
5. Get domain URL

**Update API URL in exam-enhanced.html:**
Find this line in the file:
```javascript
const API_BASE = 'https://your-backend-api.railway.app';
```
Replace with your Railway API URL.

---

## ✅ Checklist Before Going Live

**Database**
- [ ] MongoDB Atlas cluster created
- [ ] Connection string copied
- [ ] Network whitelist: 0.0.0.0/0
- [ ] Database user created

**Backend**
- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] All env vars set correctly
- [ ] API URL copied

**Frontend**
- [ ] API_BASE URL updated in exam-enhanced.html
- [ ] Vercel project deployed
- [ ] Custom domain configured (optional)

**Email**
- [ ] Gmail account with app password ready
- [ ] OR SendGrid account with API key

**Testing**
- [ ] Request OTP → email received ✓
- [ ] Login with OTP ✓
- [ ] Complete exam ✓
- [ ] Results saved ✓
- [ ] Email notification sent ✓

---

## 📁 Important Files

### Frontend (What Users See)
- `frontend/exam-enhanced.html` - Main exam interface (183 KB)
- `frontend/login.html` - OTP login
- `frontend/admin-dashboard.html` - Admin stats

### Backend (What Powers It)
- `backend/server.js` - Express server
- `backend/routes/auth.js` - Login/OTP
- `backend/routes/exam.js` - Results saving
- `backend/routes/admin.js` - Admin endpoints
- `backend/models/User.js` - Database schema

### Configuration
- `backend/.env` - Secrets (NEVER commit!)
- `DEPLOYMENT_GUIDE.md` - Detailed hosting instructions
- `README.md` - Complete documentation

### Questions
- `questions_merged.json` - All 283 questions (embedded in HTML)

---

## 🔑 Key Features Working

- ✅ 60 official exam config (or 283 full bank for practice)
- ✅ 120 min timer (configurable)
- ✅ 80% pass score (official)
- ✅ Mark for Review (press M key)
- ✅ Report Question (in practice mode)
- ✅ Dropdowns for all settings
- ✅ Results with email
- ✅ Admin dashboard
- ✅ Question CRUD

---

## 🐛 Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| Can't login | Check email is @horizontal.com |
| OTP not arriving | Check SMTP credentials in Railway |
| API 502 error | Check MongoDB connection string |
| Exam won't load | Verify API_BASE URL in exam-enhanced.html |
| Timer not working | Clear browser cache |

---

## 📊 How It Works

```
User opens exam → Browser loads exam-enhanced.html
    ↓
User configures (60 Q, 120 min, 80% pass)
    ↓
User answers questions (stored in browser memory)
    ↓
User clicks Submit → POST to backend /api/exam/submit
    ↓
Backend calculates score → Saves to MongoDB → Sends email
    ↓
Results page shows score + breakdown
    ↓
User can review marked questions or retake
```

---

## 💡 Tips

1. **Local testing**: Use file:// or python3 -m http.server
2. **Database**: Free 512MB tier handles 5,000+ users
3. **Email**: 100/day free (SendGrid) or 500/day (Gmail)
4. **Cost**: $0/month initially (scales later if needed)
5. **Questions**: All 283 embedded in HTML (instant load)

---

## 📚 Full Documentation

- **DEPLOYMENT_GUIDE.md** - Step-by-step hosting setup (20 pages)
- **README.md** - Complete reference (500 lines)
- **DELIVERABLES.md** - What's included (600 lines)
- **PROJECT_STRUCTURE.md** - Architecture overview

---

## 🎯 Common Tasks

### Add a Question (Admin)
```bash
# Via admin dashboard
1. Login (as admin)
2. Go to Admin → Questions
3. Click "Add Question"
4. Fill form → Submit
```

### View User Results (Admin)
```bash
# Via admin dashboard
1. Go to Admin → Results
2. Filter by date or user
3. Click result to see details
```

### Check User Attempts (Admin)
```bash
# Via admin dashboard
1. Go to Admin → Users
2. See attempts, pass rate, avg score
3. View last login date
```

### Report a Question (User)
```bash
# In Practice Mode
1. Answer a question
2. See green/red feedback
3. Click "Report Question"
4. Describe issue
5. Admin reviews it
```

---

## 🔐 Security Notes

- ✅ No passwords stored (OTP only)
- ✅ Email domain restricted (@horizontal.com)
- ✅ JWT tokens expire in 7 days
- ✅ Admin routes require JWT + isAdmin flag
- ✅ HTTPS everywhere (Railway/Vercel auto)
- ✅ Database encrypted at rest (MongoDB Atlas)
- ✅ Never commit .env file (add to .gitignore)

---

## 📞 Getting Help

**For Deployment Issues:**
→ See DEPLOYMENT_GUIDE.md

**For API Questions:**
→ See README.md (API Reference section)

**For Feature Implementation:**
→ See DELIVERABLES.md

**For Architecture Questions:**
→ See PROJECT_STRUCTURE.md

---

## 🚀 Next Steps

**If deploying:**
1. Create MongoDB Atlas cluster (5 min)
2. Set up Railway backend (5 min)
3. Deploy Vercel frontend (3 min)
4. Add Gmail app password (2 min)
5. Test full flow (5 min)
→ **Total: 20 minutes live!**

**If developing locally:**
1. `npm install` in backend (2 min)
2. Set up .env file (2 min)
3. `npm start` backend (1 min)
4. Open exam-enhanced.html (1 min)
5. Test exam → Results (5 min)
→ **Total: 11 minutes**

---

## 🎓 What's in the Box

| Component | Status | Location |
|-----------|--------|----------|
| Frontend | ✅ Ready | frontend/exam-enhanced.html |
| Backend API | ✅ Ready | backend/server.js |
| Database Models | ✅ Ready | backend/models/ |
| Auth System | ✅ Ready | backend/routes/auth.js |
| Admin Dashboard | ✅ Ready | frontend/admin-* |
| Question Bank | ✅ 283 qs | questions_merged.json |
| Docs | ✅ Complete | README.md + guides |
| Email Setup | ✅ Ready | SMTP config in .env |

---

**Everything is ready to go!** 🎉

Pick one:
- **Want to test locally?** → Run backend + open HTML
- **Want to go live?** → Follow DEPLOYMENT_GUIDE.md
- **Want to customize?** → See README.md
- **Have questions?** → See DELIVERABLES.md

---

**Built and tested: June 24, 2024**  
**283 questions verified | All features working | Production ready**
