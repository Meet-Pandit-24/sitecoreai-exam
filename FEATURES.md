# 🎯 SitecoreAI CMS Developer Certification Exam Simulator

## Overview
**SitecoreAI Exam Simulator** is a comprehensive, production-ready web application that replicates the official **Sitecore CMS Developer Certification exam experience**. It provides candidates with 283 verified exam questions, real-time scoring, performance tracking, and instant result notifications.

---

## ✨ Key Features

### 📋 Exam Simulation
- **283 Verified Questions** - Extracted from official Sitecore V3 & V4 certification documents
- **Flexible Configuration** - Choose number of questions (10-283), time limit (30-180 minutes), pass score (50-100%)
- **Multiple Exam Modes**
  - Practice Mode: Review answers immediately
  - Exam Mode: Locked questions, timed, full results only
  - Custom Mode: Configure your own parameters
- **Real-time Timer** - Visual countdown with warning states (yellow at 10 min, red at 5 min)
- **Progress Tracking** - Sidebar shows answered/flagged/skipped questions at a glance

### 🏆 Advanced Exam Features
- **Mark for Review** - Flag questions to revisit later
- **Report Issue** - Submit corrections for questions (with admin review dashboard)
- **Instant Results** - Score calculation, pass/fail status, detailed breakdown
- **Email Notifications** - Exam results emailed immediately after submission (SendGrid integration)

### 📊 Student Dashboard
- **Exam History** - View all previous attempts with dates, scores, and timings
- **Performance Analytics**
  - Total attempts
  - Pass/fail counts
  - Average score
  - Time spent analysis
- **Detailed Results** - Review each attempt with question-by-question breakdown

### 🔐 Authentication & Security
- **OTP-Based Login** - 6-digit One-Time Password sent via email
- **Domain Restriction** - Only @horizontal.com emails allowed
- **JWT Tokens** - 7-day expiring session tokens for secure API access
- **No Password Storage** - Zero password security risk (OTP only)

### 👨‍💼 Admin Dashboard
**4 Comprehensive Tabs:**

1. **Overview** - System-wide statistics
   - Total users registered
   - Total exam attempts
   - Overall pass rate
   - Average score across all users

2. **Users Management**
   - List all registered users
   - Track attempt counts
   - View last login dates
   - Identify user activity

3. **Results Tracking**
   - All exam attempts across users
   - Sortable by date, score, status
   - Filter passed/failed exams
   - Export data for reporting

4. **Issue Reports**
   - User-reported question problems
   - Track report status (pending/resolved)
   - Bulk resolve issues
   - Feedback collection system

### ❓ Questions Management
- **View All Questions** - Browse 283 questions with search & filters
- **Add New Questions** - Modal form for creating questions
- **Edit Questions** - Modify any existing question
- **Delete Questions** - Remove questions safely
- **Duplicate Questions** - Create variations quickly
- **Advanced Export**
  - **JSON** - For data exchange and backup
  - **CSV** - Edit in Excel, share with team
  - **Excel** - Direct .xls format
- **Bulk Import**
  - Upload JSON files
  - Upload CSV files
  - Upload Excel spreadsheets
  - Validate and import with error handling
- **Migration Tool** - `npm run seed` loads all 283 questions from frontend into database

### 🎨 Professional UI/UX
- **Dark Theme** - Gradient backgrounds, accent colors (#e53935 red)
- **Responsive Design** - Works on desktop, tablet, mobile
- **Real-time Feedback** - Success/error messages, loading states
- **Accessibility** - Proper contrast, keyboard navigation, ARIA labels
- **Modern Components** - Modals, dropdowns, progress bars, badges

---

## 🎯 Benefits

### For Exam Candidates
✅ **Practice with Real Questions** - 283 verified questions matching official exam
✅ **Time Management** - Build speed with configurable time limits
✅ **Performance Tracking** - Monitor improvement across multiple attempts
✅ **Instant Feedback** - Know results immediately with email notification
✅ **Flexible Learning** - Practice full exams or custom question sets
✅ **Mistake Identification** - Review answers to identify weak areas

### For Organizations
✅ **Certification Tracking** - Monitor employee certification progress
✅ **Performance Metrics** - Dashboard analytics for training effectiveness
✅ **Question Management** - Add custom questions, maintain question bank
✅ **Secure System** - OTP-based auth, no password storage, JWT tokens
✅ **Scalable Infrastructure** - Cloud-deployed, handles unlimited users
✅ **Free Hosting** - Railway (backend), Vercel (frontend), MongoDB Atlas

### For Administrators
✅ **Full Control** - Manage users, questions, and reports
✅ **Easy Analytics** - View stats at a glance on Overview tab
✅ **Issue Tracking** - Resolve question problems systematically
✅ **Data Export** - Export questions in multiple formats
✅ **User Management** - Track who's taking exams and their progress

---

## 🔧 Technical Architecture

### Frontend
- **HTML/CSS/JavaScript** - No framework dependencies, lightweight
- **Pages:**
  - `index.html` - Redirect/auth check
  - `login.html` - OTP login interface
  - `exam-enhanced.html` - Main exam simulator (283 questions embedded)
  - `dashboard.html` - Student results dashboard
  - `admin.html` - Admin management interface
- **Features:**
  - localStorage for token persistence
  - Responsive CSS Grid
  - Real-time timer with visual feedback
  - Modal dialogs for actions

### Backend (Node.js/Express)
- **Endpoints:** 13 REST API routes
  - Authentication (OTP request/verify)
  - Exam submission & history
  - Questions CRUD & import
  - Admin analytics & reporting
- **Database:** MongoDB with 4 collections
  - Users (profile, OTP, verification status)
  - ExamResults (scores, answers, timing)
  - Questions (283 questions with metadata)
  - QuestionReports (issue tracking)
- **Email:** SendGrid integration for OTP & result emails
- **Security:** JWT tokens, authentication middleware, domain validation

### Deployment
- **Frontend:** Vercel (automatic deployments from GitHub)
- **Backend:** Railway (Node.js app, auto-restart)
- **Database:** MongoDB Atlas (free tier, cloud-hosted)
- **Email:** SendGrid API (100 free emails/day)
- **Version Control:** Git with proper .gitignore

---

## 📊 Question Bank

**283 Total Questions** covering:
- **Content Modeling** (Templates, Fields, Standard Values)
- **Content Structure** (Inheritance, Insert Options, Sections)
- **Page Building** (Layouts, Placeholders, Renderings)
- **Headless Architecture** (JSS, GraphQL, Experience Edge)
- **Content Serialization** (CLI, Deployment, Version Control)
- **Personalization** (Page Variants, Rendering Parameters)
- **Security** (Access Control, Permissions, Roles)
- **GraphQL APIs** (Experience Edge, Authoring API)
- **DevOps** (Cloud CLI, Provisioning, CI/CD)

**Question Formats:**
- Single-choice (most questions)
- Multiple-choice (marked as "hard" difficulty)
- Difficulty levels: Easy, Medium, Hard
- Categories for organization

---

## 🚀 Getting Started

### For Candidates
1. Visit: `https://sitecoreai-exam.vercel.app`
2. Enter email (must be @horizontal.com)
3. Click "Request OTP"
4. Check email for 6-digit code
5. Enter OTP to login
6. Configure exam (questions, time, pass score)
7. Take exam
8. View results instantly + get email notification

### For Admins
1. Login as candidate first (must be @horizontal.com)
2. Access admin dashboard: `/admin.html`
3. View stats, manage users, review reports, manage questions
4. Edit questions, export data, track performance

### For Developers
1. Clone repository
2. Backend setup:
   ```bash
   cd backend
   npm install
   npm run seed        # Load 283 questions
   npm start          # Start server on port 5000
   ```
3. Frontend: Deploy to Vercel (automatic from git push)
4. Configure `.env` with MongoDB URI and SendGrid API key

---

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Total Questions | 283 |
| Question Categories | 10+ |
| Difficulty Levels | 3 (Easy, Medium, Hard) |
| Max Exam Time | 180 minutes |
| Max Questions per Exam | 283 |
| OTP Validity | 15 minutes |
| JWT Token Validity | 7 days |
| Email Delivery | SendGrid API |
| Database | MongoDB Atlas |
| Frontend Hosting | Vercel |
| Backend Hosting | Railway |
| Supported Browsers | Chrome, Firefox, Safari, Edge |

---

## 🔒 Security Features

✅ **Email-Based OTP** - No password storage
✅ **JWT Authentication** - Secure token-based sessions
✅ **Domain Validation** - Only @horizontal.com emails allowed
✅ **HTTPS** - All traffic encrypted
✅ **API Rate Limiting** - Protection against abuse
✅ **Input Validation** - Prevent injection attacks
✅ **CORS Configured** - Secure cross-origin requests
✅ **Admin Verification** - Confirm admin status before dashboard access

---

## 📱 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | Latest | ✅ Fully Supported |
| Firefox | Latest | ✅ Fully Supported |
| Safari | Latest | ✅ Fully Supported |
| Edge | Latest | ✅ Fully Supported |
| Mobile Chrome | Latest | ✅ Fully Supported |
| Mobile Safari | Latest | ✅ Fully Supported |

---

## 🎓 Perfect For

- **Certification Candidates** - Practice before official exam
- **Training Programs** - Track learner progress
- **Organizations** - Monitor team certifications
- **Self-Paced Learning** - Flexible study schedule
- **Performance Assessment** - Identify knowledge gaps
- **Competitive Exams** - Build exam-taking skills

---

## 💡 Future Enhancements

Potential features for v2.0:
- Timed randomization (different question order per attempt)
- Topic-specific practice modes
- Difficulty-based adaptive testing
- Detailed performance reports with PDF export
- Mobile app (React Native)
- Dark/Light theme toggle
- Offline mode support
- Leaderboards
- Integration with learning platforms (LMS)
- Video explanations for answers

---

## 📞 Support

For issues, questions, or feedback:
- **Report Issues** - Use the "Report Issue" button in exam
- **Admin Review** - Check Reports tab in admin dashboard
- **Contact:** mpandit@horizontal.com

---

**Version:** 1.0.0
**Last Updated:** June 30, 2026
**Status:** Production Ready ✅
