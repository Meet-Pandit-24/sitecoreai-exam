# SendGrid Email Setup Guide

## Why SendGrid Instead of Gmail?

✅ **SendGrid Benefits:**
- Free tier: 100 emails/day (more than enough for exams)
- Professional email service (not personal account)
- Better deliverability (emails go to inbox, not spam)
- Easy API integration
- No 2FA/app passwords needed
- Scalable when you grow
- Industry standard

---

## Step-by-Step Setup

### Step 1: Create SendGrid Account (2 minutes)

1. Go to https://sendgrid.com/free
2. Sign up with your email:
   - Full Name: Your Name
   - Email: Your email (any email works)
   - Password: Create password
3. Click "Create Account"
4. Verify your email (check inbox)
5. Done! You're logged in

---

### Step 2: Create API Key (3 minutes)

1. In SendGrid dashboard, go to:
   **Settings** → **API Keys**

2. Click **"Create API Key"** button

3. Fill in:
   - **API Key Name:** `SitecoreAI Exam`
   - **Permissions:** Select `Mail Send`
   - Click **"Create & Copy"**

4. **IMPORTANT: Copy the API key immediately**
   - It only shows once!
   - Format: `SG.xxxxx...`
   - Save it somewhere safe

5. In your `backend/.env` file, add:
   ```
   SMTP_PASS=SG.your-api-key-here
   ```

---

### Step 3: Verify Sender Email (5 minutes)

For SendGrid to send emails, you need to verify a sender email.

#### Option A: Verify Your Domain (Recommended for production)
1. In SendGrid: **Settings** → **Sender Authentication**
2. Click **"Authenticate Your Domain"**
3. Enter your domain (e.g., `yourdomain.com`)
4. Follow DNS setup instructions
5. Add the records to your domain registrar
6. Verify (takes 10-30 min)

#### Option B: Use Single Sender (Quick for testing)
1. In SendGrid: **Settings** → **Senders**
2. Click **"Create New Sender"**
3. Fill in:
   - **From Email:** `noreply@yourdomain.com` (or any email)
   - **From Name:** `SitecoreAI Exam`
   - **Reply To Email:** Your actual email
4. Click **"Create"**
5. Verify via email link (check inbox)
6. Use this email in `FROM_EMAIL`:
   ```
   FROM_EMAIL=noreply@yourdomain.com
   ```

---

### Step 4: Configure Backend (.env file)

Create or edit `backend/.env`:

```env
# Database
MONGODB_URI=mongodb+srv://exam-admin:PASSWORD@exam-cluster.abc.mongodb.net/sitecoreai-exam

# JWT
JWT_SECRET=your-random-secret-key

# SendGrid Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=SG.your-sendgrid-api-key-here
FROM_EMAIL=noreply@yourdomain.com

# Frontend
FRONTEND_URL=https://exam.yourdomain.com

# Server
PORT=5000
NODE_ENV=production
```

---

## Testing Locally

1. Install dependencies:
   ```bash
   cd backend
   npm install
   ```

2. Create `.env` file with all variables (above)

3. Start server:
   ```bash
   npm start
   ```

4. Test login:
   - Open frontend/exam-enhanced.html
   - Request OTP
   - Check your email for code
   - Login with code

---

## Deploying to Railway

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Add SendGrid email support"
git push origin master
```

### Step 2: Add Variables to Railway

1. Go to Railway dashboard
2. Select your project
3. Go to **Variables** tab
4. Add these variables:
   ```
   SMTP_HOST=smtp.sendgrid.net
   SMTP_PORT=587
   SMTP_USER=apikey
   SMTP_PASS=SG.your-sendgrid-api-key-here
   FROM_EMAIL=noreply@yourdomain.com
   ```

5. Click **Redeploy**

### Step 3: Test on Railway

1. Get your Railway URL
2. Update frontend `exam-enhanced.html`:
   ```javascript
   const API_BASE = 'https://your-railway-domain.railway.app';
   ```
3. Deploy frontend to Vercel
4. Test: Request OTP → should arrive in email

---

## Troubleshooting

### Email not arriving

**Problem:** OTP email not showing up  
**Solution:**
- Check spam folder
- Verify sender email is authenticated in SendGrid
- Check SMTP credentials in Railway variables
- Check Railway logs for errors

### 550 Error (Invalid sender)

**Problem:** "550 Unauthorized sender"  
**Solution:**
- Go to SendGrid: **Settings** → **Senders**
- Verify the email address is authenticated
- Use that email in `FROM_EMAIL` env var

### API Key invalid

**Problem:** "Invalid credentials"  
**Solution:**
- Make sure API key starts with `SG.`
- Make sure you copied it completely
- Create a new API key and try again

### Rate limit (100 emails/day)

**Problem:** Getting rate limit errors  
**Solution:**
- You've sent 100+ emails in a day
- Wait until tomorrow (free tier resets daily)
- Upgrade to paid plan if needed (very cheap)

---

## SendGrid Limits & Pricing

| Feature | Free Tier | Cost |
|---------|-----------|------|
| Emails/day | 100 | Free |
| Email limit | 100/day | Resets daily |
| Support | Community | Paid |
| Upgrade to 1,000/day | — | $10/month |
| Upgrade to 10,000/day | — | $20/month |

---

## What Changes Were Made

Updated backend to use SendGrid instead of Gmail:

**Files Changed:**
- `backend/routes/auth.js` - Updated OTP email sender
- `backend/routes/exam.js` - Updated result email sender
- `backend/.env.example` - Added SendGrid config

**Key Changes:**
- Uses `smtp.sendgrid.net` instead of `smtp.gmail.com`
- Uses API key for authentication (not password)
- Uses `FROM_EMAIL` environment variable
- Default fallback email if FROM_EMAIL not set

---

## Next Steps

1. ✅ Code updated (done)
2. Create SendGrid account
3. Create API key
4. Verify sender email
5. Create `backend/.env` with SendGrid credentials
6. Test locally (`npm start`)
7. Push to GitHub
8. Update Railway variables
9. Redeploy

---

## Reference Links

- SendGrid Free: https://sendgrid.com/free
- API Keys: https://app.sendgrid.com/settings/api_keys
- Senders: https://app.sendgrid.com/settings/senders
- Docs: https://docs.sendgrid.com/

---

**Total setup time: 10-15 minutes**  
**No personal email account needed!** ✅
