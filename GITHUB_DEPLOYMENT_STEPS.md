# Step-by-Step: Push to GitHub & Deploy to Railway

## Part 1: Create GitHub Repository (5 minutes)

### Step 1.1: Go to GitHub
1. Visit https://github.com/new
2. Sign in with your GitHub account

### Step 1.2: Create New Repository
Fill in the form:
```
Repository name:    sitecoreai-exam
Description:        SitecoreAI CMS Exam Simulator - Production Ready
Visibility:         Public (for Railway to access) or Private
Initialize:         DON'T check any boxes (we already have files)
```

Click **Create repository**

### Step 1.3: Copy Your Repository URL
After creation, you'll see:
```
https://github.com/yourusername/sitecoreai-exam.git
```
Copy this URL (you'll need it in the next step)

---

## Part 2: Push Code to GitHub (2 minutes)

Open PowerShell/Git Bash in `C:\Projects\SitecoreAI\`

### Step 2.1: Add GitHub Remote
```bash
git remote add origin https://github.com/yourusername/sitecoreai-exam.git
```

### Step 2.2: Verify Remote Added
```bash
git remote -v
```
Should show:
```
origin  https://github.com/yourusername/sitecoreai-exam.git (fetch)
origin  https://github.com/yourusername/sitecoreai-exam.git (push)
```

### Step 2.3: Push to GitHub
```bash
git push -u origin master
```

This will:
- Upload all files
- Create master branch on GitHub
- Set up tracking

### Step 2.4: Verify on GitHub
1. Go to your GitHub repo URL
2. Should see all 41 files
3. See your commit message with features

---

## Part 3: Deploy to Railway (15 minutes)

### Step 3.1: Go to Railway
1. Visit https://railway.app
2. Sign up with GitHub (recommended)
3. Click "New Project"

### Step 3.2: Import from GitHub
1. Select "Deploy from GitHub repo"
2. Authorize Railway to access your GitHub
3. Select your `sitecoreai-exam` repo
4. Click "Deploy Now"

Railway will:
- Detect Node.js project
- Install dependencies
- Start deployment

### Step 3.3: Add Environment Variables

While deploying, go to **Variables** tab:

Add each variable from `backend/.env.example`:

```
MONGODB_URI
  Value: mongodb+srv://exam-admin:PASSWORD@exam-cluster.abc.mongodb.net/sitecoreai-exam

JWT_SECRET
  Value: (generate random: openssl rand -base64 32)

SMTP_HOST
  Value: smtp.gmail.com

SMTP_PORT
  Value: 587

SMTP_USER
  Value: your-email@gmail.com

SMTP_PASS
  Value: your-app-password (from Gmail)

FRONTEND_URL
  Value: https://exam.yourdomain.com (or https://sitecoreai-exam.railway.app)

NODE_ENV
  Value: production
```

### Step 3.4: Get Your Backend API URL

Once deployed:
1. Go to "Settings"
2. Find "Domain"
3. Copy the Railway-generated URL (looks like `https://sitecoreai-exam.railway.app`)
4. This is your `API_BASE` URL

---

## Part 4: Deploy Frontend to Vercel (3 minutes)

### Step 4.1: Go to Vercel
1. Visit https://vercel.com
2. Sign up with GitHub
3. Click "New Project"

### Step 4.2: Import GitHub Repo
1. Click "Import Project"
2. Paste your repo URL: `https://github.com/yourusername/sitecoreai-exam.git`
3. Vercel will import it
4. Framework: Select "Other" (HTML/Static)
5. Root Directory: Select `frontend/`
6. Click "Deploy"

### Step 4.3: Wait for Deployment
- Vercel will build and deploy
- You'll get a URL like: `https://sitecoreai-exam.vercel.app`

### Step 4.4: Update Frontend API URL

You need to update the API URL in `exam-enhanced.html`

**Option A: Update in Frontend File**
1. In local repo, open `frontend/exam-enhanced.html`
2. Find this line (around line 1000):
   ```javascript
   const API_BASE = 'https://your-backend-api.railway.app';
   ```
3. Replace with your Railway URL:
   ```javascript
   const API_BASE = 'https://sitecoreai-exam.railway.app';
   ```
4. Save file
5. Git commit and push:
   ```bash
   git add frontend/exam-enhanced.html
   git commit -m "Update API URL for Railway backend"
   git push origin master
   ```
6. Vercel will auto-redeploy

---

## Part 5: Configure Custom Domain (Optional)

### For Frontend (Vercel)
1. Go to Vercel dashboard
2. Project Settings → Domains
3. Add your domain: `exam.yourdomain.com`
4. Follow DNS instructions

### For Backend (Railway)
1. Go to Railway dashboard
2. Project Settings → Domains
3. Add custom domain
4. Update MongoDB URI if using custom domain

---

## Part 6: Test Everything Works

### Step 6.1: Test Login
1. Open your Vercel frontend URL
2. Request OTP with email
3. Check email for code
4. Login with code
5. See exam load

### Step 6.2: Test Exam
1. Configure exam settings
2. Answer a few questions
3. Click "Submit Exam"
4. See results page
5. Check email for results

### Step 6.3: Test Admin Dashboard
1. Login as admin
2. Go to `/admin-dashboard.html`
3. Should see user stats
4. Should see your exam result

---

## Troubleshooting

### Can't login - OTP not arriving
- Check SMTP variables in Railway
- Check Gmail app password is correct
- Check spam folder

### Exam won't load - API errors
- Check API_BASE URL in exam-enhanced.html
- Check Railway deployment status
- Check Railway logs for errors

### MongoDB connection error
- Verify MONGODB_URI is correct
- Check network whitelist (0.0.0.0/0)
- Verify database user exists

### Vercel says "Not Found"
- Check root directory is set to `frontend/`
- Check `exam-enhanced.html` exists in frontend/

---

## Summary of URLs

After everything is deployed, you'll have:

```
Frontend:   https://exam.yourdomain.com (Vercel)
Backend:    https://sitecoreai-exam.railway.app (Railway)
Database:   MongoDB Atlas (connected via MONGODB_URI)
```

---

## Files to Reference

- `DEPLOYMENT_GUIDE.md` - Detailed hosting guide
- `backend/.env.example` - All required variables
- `QUICK_START.md` - Quick reference
- `GIT_SETUP_COMPLETE.md` - Git status verification

---

## Quick Checklist

- [ ] GitHub repo created
- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] MongoDB URI added to Railway
- [ ] Other env vars added to Railway
- [ ] Backend deployed to Railway
- [ ] Vercel frontend deployed
- [ ] API_BASE URL updated in frontend
- [ ] Frontend redeployed after URL update
- [ ] Test login works
- [ ] Test exam works
- [ ] Check email received results

---

**Everything is ready to go! Follow the steps above and you'll be live in 20 minutes.** 🚀
