# 🚀 Deploying to Replit

## Step 1: Create Replit Project

1. Go to: https://replit.com
2. Click **"+ Create"**
3. Choose **"Import from GitHub"**
4. Paste: `https://github.com/Meet-Pandit-24/sitecoreai-exam.git`
5. Click **Import**
6. When asked for folder, choose **`backend`** folder
7. Click **Create Replit** ✅

---

## Step 2: Set Environment Variables

1. Click **Secrets** icon (lock icon) in left sidebar
2. Add these variables:

```
MONGODB_URI = mongodb+srv://[your-mongodb-connection-string]
JWT_SECRET = your-secret-key-min-32-chars
SMTP_PASS = SG.your-sendgrid-api-key
FROM_EMAIL = noreply@sitecoreai-exam.com
NODE_ENV = production
```

**Where to get these:**

| Variable | Where to Find |
|----------|---------------|
| **MONGODB_URI** | MongoDB Atlas → Connect → Connection String |
| **JWT_SECRET** | Any random 32+ char string (e.g., use `openssl rand -base64 32`) |
| **SMTP_PASS** | SendGrid → API Keys → Create Key |
| **FROM_EMAIL** | Your SendGrid verified sender email |

---

## Step 3: Deploy

1. Click **Run** button (or press Ctrl+Enter)
2. Wait for: `✓ Server running on port 5000`
3. Copy the **Replit URL** from top (looks like: `https://your-replit-name.replit.dev`)

---

## Step 4: Update Frontend API URL

Go to: **`frontend/login.html`** and change:

**Find (line 112):**
```javascript
const API_BASE = 'https://sitecoreai-exam-production.up.railway.app';
```

**Replace with:**
```javascript
const API_BASE = 'https://your-replit-name.replit.dev';
```

---

## Step 5: Redeploy Frontend

1. Commit the change:
   ```bash
   git add frontend/login.html
   git commit -m "Update API URL to Replit backend"
   git push origin master
   ```

2. Vercel auto-deploys
3. Wait 2-3 minutes
4. Visit: https://sitecoreai-exam.vercel.app/login.html
5. Try login! ✅

---

## 🎯 Quick Reference

| Component | Location |
|-----------|----------|
| **Backend** | https://your-replit-name.replit.dev |
| **Frontend** | https://sitecoreai-exam.vercel.app |
| **Database** | MongoDB Atlas |
| **Email** | SendGrid API |

---

## ⚠️ Important Notes

- Replit free tier is **100% free** but has limitations:
  - App goes to sleep after inactivity (will restart when accessed)
  - No uptime guarantee
  - For production, consider upgrading or using paid tier

- To keep Replit always running (paid):
  - Upgrade to Replit Pro ($7/month)
  - Or use their "Always On" feature

---

## 🆘 Troubleshooting

**Backend not responding?**
- Check Replit console for errors
- Verify all env vars are set correctly
- Try clicking Run again

**MongoDB connection failed?**
- Check MONGODB_URI is correct
- Ensure MongoDB Atlas allows Replit IPs
- Add `0.0.0.0/0` to MongoDB Atlas IP whitelist

**Login still fails?**
- Check browser console for errors
- Verify API_BASE URL in login.html is correct
- Clear browser cache and refresh

---

## ✨ Done!

Your backend is now hosted on Replit! 🎉
