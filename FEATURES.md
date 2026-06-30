# 🎯 SitecoreAI CMS Developer Certification Exam Simulator

## What It Does
Production-ready web app for practicing **Sitecore CMS Developer Certification** with **283 verified exam questions**, real-time scoring, performance tracking, and instant email results.

---

## ✨ Key Features

### For Candidates
- **283 Questions** - Real certification questions
- **Flexible Exam Mode** - Choose questions (10-283), time limit (30-180 min), pass score (50-100%)
- **Practice Features** - Mark for review, flag issues, get instant results
- **Results Dashboard** - Track attempts, scores, average performance
- **Email Notifications** - Results sent automatically after exam
- **OTP Login** - Secure 6-digit code authentication (@horizontal.com only)

### For Admins
- **Overview Dashboard** - Total users, attempts, pass rate, average score
- **User Management** - View all users and their activity
- **Results Tracking** - All exam attempts with sortable data
- **Issue Reports** - Track and resolve user-reported problems
- **Question Management** - Add, edit, delete, import/export questions
- **Data Export** - Download questions as JSON, CSV, or Excel

### Exam Features
- ⏱️ Real-time countdown timer with warnings
- 📊 Progress sidebar (answered/flagged/skipped tracking)
- 🎯 Instant score calculation
- 📧 Email results (SendGrid integration)
- 🔍 Search & filter questions by category/difficulty
- 📋 Bulk import questions (JSON/CSV/Excel)

---

## 🏗️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML/CSS/JavaScript (no framework) |
| **Backend** | Node.js + Express |
| **Database** | MongoDB Atlas |
| **Email** | SendGrid API |
| **Hosting** | Vercel (frontend), Railway (backend) |
| **Auth** | JWT tokens + OTP |

---

## 📊 Stats

| Metric | Value |
|--------|-------|
| Questions | 283 |
| Categories | Sitecore CMS topics |
| Exam Time | 30-180 minutes |
| OTP Validity | 15 minutes |
| JWT Validity | 7 days |
| Email Limit | 100/day (SendGrid free) |

---

## 🚀 Quick Links

| User Type | URL |
|-----------|-----|
| **Candidate** | https://sitecoreai-exam.vercel.app |
| **Admin Dashboard** | `/admin.html` (after login) |
| **API Backend** | https://sitecoreai-exam-production.up.railway.app |

---

## 🔒 Security

✅ OTP-based login (no passwords)
✅ JWT token authentication (7-day expiry)
✅ Domain validation (@horizontal.com only)
✅ HTTPS encrypted
✅ Input validation & sanitization

---

## ✅ Features Checklist

- [x] 283 verified exam questions
- [x] Flexible exam configuration
- [x] Real-time timer & progress tracking
- [x] Instant results with scoring
- [x] Email notifications
- [x] Student dashboard with analytics
- [x] Admin management panel
- [x] Question CRUD operations
- [x] Bulk import/export (JSON/CSV/Excel)
- [x] OTP-based authentication
- [x] Issue reporting system
- [x] Cloud deployment (free tier)

---

## 📱 Browser Support

Chrome, Firefox, Safari, Edge (latest versions) ✅
Mobile responsive ✅

---

**Status:** ✨ Production Ready
**Version:** 1.0.0
