# SitecoreAI Exam Simulator - Deployment Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│ Frontend: exam-enhanced.html                    │
│ Hosting: Vercel / Netlify (FREE)               │
└────────────────────┬────────────────────────────┘
                     │ API Calls
                     ▼
┌─────────────────────────────────────────────────┐
│ Backend: Node.js/Express                        │
│ Hosting: Railway / Render (FREE TIER)           │
└────────────────────┬────────────────────────────┘
                     │ Database
                     ▼
┌─────────────────────────────────────────────────┐
│ Database: MongoDB Atlas                         │
│ Plan: Free (512 MB) - Upgrade as needed         │
└─────────────────────────────────────────────────┘
```

---

## Step 1: Database Setup (MongoDB Atlas)

### Free Tier Features
- 512 MB storage
- 3 replica set
- 100,000 req/month API access (M0 cluster)

### Setup Instructions

1. **Create MongoDB Atlas Account**
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up free
   - Create organization

2. **Create Free Cluster**
   - Click "Create" → New Project
   - Project Name: `sitecoreai-exam`
   - Click "Build a Database"
   - Select "M0 Free" tier
   - Cloud Provider: AWS (or your preferred)
   - Region: Closest to your users
   - Cluster Name: `exam-cluster`
   - Click "Create Cluster"

3. **Create Database User**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Username: `exam-admin`
   - Generate secure password
   - Built-in Role: `Atlas admin`
   - Add User

4. **Allow Network Access**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Select "Allow access from anywhere" (0.0.0.0/0)
   - Click "Confirm"

5. **Get Connection String**
   - Go to Databases → Collections
   - Click "Connect"
   - Select "Connect your application"
   - Copy connection string (looks like):
     ```
     mongodb+srv://exam-admin:PASSWORD@exam-cluster.xyz.mongodb.net/?retryWrites=true&w=majority
     ```
   - Replace `PASSWORD` with your password

---

## Step 2: Backend Deployment (Railway or Render)

### Option A: Railway (Recommended)

**Features:**
- Free tier: $5/month credit
- Auto-deploys from GitHub
- Environment variables management
- 2GB RAM, 10GB storage per project

**Steps:**

1. **Push code to GitHub**
   ```bash
   cd backend
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Sign up (connect GitHub)
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your backend repo
   - Select `backend` directory

3. **Add Environment Variables**
   - Go to Project Settings
   - Variables → Add variable for each from `.env.example`:
     - `MONGODB_URI`: Your connection string
     - `JWT_SECRET`: Generate random string (use `openssl rand -base64 32`)
     - `SMTP_*`: Your email credentials
     - `FRONTEND_URL`: Your frontend domain
     - `NODE_ENV`: `production`

4. **Deploy**
   - Railway auto-deploys on GitHub push
   - Your API will be at: `https://[project-name].railway.app`

### Option B: Render

**Features:**
- Free tier: Node.js
- Auto-deploys from GitHub
- Limitations: Spins down after 15 min inactivity (not ideal for production)

**Steps:**

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Dashboard → New → Web Service
   - Connect GitHub repo
   - Select `backend` directory
   - Name: `sitecoreai-exam-api`
   - Runtime: `Node`
   - Build: `npm install`
   - Start: `npm start`

3. **Add Environment Variables** (same as Railway)

4. **Deploy**
   - Click "Create Web Service"
   - Your API will be at: `https://sitecoreai-exam-api.onrender.com`

---

## Step 3: Frontend Deployment (Vercel or Netlify)

### Option A: Vercel (Recommended for Next.js, but works for static too)

**Features:**
- Free tier: Unlimited deployments, 50 GB bandwidth
- Super fast CDN
- One-click GitHub deploy

**Steps:**

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Add Frontend to GitHub**
   ```bash
   git add frontend/exam-enhanced.html
   git commit -m "Add exam frontend"
   git push
   ```

3. **Deploy on Vercel**
   - Vercel Dashboard → New Project
   - Select your GitHub repo
   - Framework: `Other` (static HTML)
   - Root Directory: `frontend`
   - Click "Deploy"

4. **Configure API URL**
   - In `exam-enhanced.html`, update API calls:
     ```javascript
     const API_URL = 'https://your-backend.railway.app';
     ```

### Option B: Netlify

**Steps:**

1. **Create Netlify Account**
   - Go to https://netlify.com
   - Sign up

2. **Deploy**
   - Drag and drop `frontend/exam-enhanced.html`
   - Or connect GitHub → New site from Git

3. **Custom Domain**
   - Domain settings → Custom domain
   - Point your domain's DNS

---

## Step 4: Email Setup (SendGrid or Gmail)

### Option A: SendGrid (Free)

**Features:**
- Free tier: 100 emails/day
- 30 days retention

**Setup:**

1. Go to https://sendgrid.com/free
2. Sign up free
3. Go to Settings → API Keys
4. Create new API key
5. Use API key as `SMTP_PASS` in `.env`

### Option B: Gmail (Your personal email)

**Steps:**

1. Enable 2-Factor Authentication on Gmail
2. Create App Password (not your regular password):
   - Go to myaccount.google.com
   - Security → App passwords
   - Generate password for "Mail" / "Windows Computer"
3. Use app password as `SMTP_PASS`

**Limits:** 500 emails/day for Gmail accounts

---

## Step 5: Domain & SSL

### Get Free Domain
- Freenom.com (free .tk, .ml, .ga)
- Or use subdomain: `exam.yourdomain.com`

### SSL Certificate
- Railway/Render: **Automatic** (included free)
- Vercel/Netlify: **Automatic** (included free)
- MongoDB Atlas: **Automatic** (included free)

---

## Environment Setup Checklist

```
Backend (.env):
☐ MONGODB_URI = mongodb+srv://exam-admin:PASSWORD@exam-cluster...
☐ JWT_SECRET = (generate: openssl rand -base64 32)
☐ SMTP_HOST = smtp.gmail.com or api.sendgrid.com
☐ SMTP_PORT = 587 or 465
☐ SMTP_USER = your-email@gmail.com
☐ SMTP_PASS = your-app-password or api-key
☐ FRONTEND_URL = https://exam.yourdomain.com
☐ PORT = 5000
☐ NODE_ENV = production

Frontend (exam-enhanced.html):
☐ API_URL = https://your-backend-api.railway.app
☐ Domain SSL: https:// (required for OTP emails)

Database:
☐ Network Access: 0.0.0.0/0 (allow anywhere)
☐ Database User created with secure password
☐ Collections auto-created (will generate on first request)
```

---

## Cost Breakdown (Monthly)

| Service | Free Tier | Cost |
|---------|-----------|------|
| MongoDB Atlas | 512 MB | Free |
| Railway | $5 credit | Free (with credit) |
| Vercel | 50 GB bandwidth | Free |
| SendGrid | 100 emails/day | Free |
| **Total** | | **FREE** ✓ |

**Upgrade paths** (if needed):
- Railway: $0.29/hour compute + $0.005/GB storage
- MongoDB: $57/month (M2) to $519+/month (M10)
- Vercel: $20/month (Pro) for advanced features

---

## First-Time Deployment Steps (Quick Start)

### 1. Create `.env` file in `backend/`:
```bash
MONGODB_URI=mongodb+srv://exam-admin:PASSWORD@exam-cluster.xyz.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET=your-random-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FRONTEND_URL=https://exam.yourdomain.com
PORT=5000
NODE_ENV=production
```

### 2. Test locally:
```bash
cd backend
npm install
npm start
# Should see: ✓ Server running on port 5000
```

### 3. Push to GitHub:
```bash
git add .
git commit -m "Full stack ready to deploy"
git push origin main
```

### 4. Deploy Backend (Railway):
- Go to railway.app
- New Project → GitHub
- Select repo
- Add env vars from `.env`
- Done! Get your API URL

### 5. Deploy Frontend (Vercel):
- Go to vercel.com
- New Project → GitHub
- Select repo
- Deploy
- Add custom domain

### 6. Update Frontend API URL:
In `exam-enhanced.html`, find and update:
```javascript
const API_BASE = 'https://your-railway-api.railway.app';
```

### 7. Test the full flow:
- Visit your frontend domain
- Request OTP → check email
- Login → should work
- Complete exam → should save result
- Check admin dashboard

---

## Scaling (If Needed)

**When to upgrade:**

| Metric | Action |
|--------|--------|
| MongoDB >512MB | Upgrade to M2 ($57/mo) |
| Backend CPU high | Upgrade Railway instance |
| 10k+ monthly users | Consider managed solution |
| Custom domain needed | Use your own DNS |

---

## Troubleshooting

### OTP not sending
- Check SMTP credentials
- Verify email account allows app access
- Check Railway/Render logs

### API 502 errors
- Check Railway/Render logs
- Verify MongoDB connection string
- Ensure all env vars are set

### Frontend can't reach API
- Check CORS is enabled in Express
- Verify API URL in frontend code
- Check network tab in browser devtools

### MongoDB connection timeout
- Verify IP whitelist includes your server
- Check connection string syntax
- Test connection from Railway logs

---

## Security Best Practices

1. **Never commit `.env` file** (add to `.gitignore`)
2. **Use environment variables** for all secrets
3. **Change default passwords** after setup
4. **Enable 2FA** on MongoDB Atlas
5. **Monitor API usage** for abuse
6. **Rate limit** sensitive endpoints (OTP)
7. **HTTPS everywhere** (auto-managed by Vercel/Railway)

---

## Support & Docs

- Railway: https://railway.app/docs
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
- MongoDB: https://docs.mongodb.com
- Express: https://expressjs.com
