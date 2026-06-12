# 🚀 FoodRescue AI - Complete Deployment Guide

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Backend Deployment (Railway.app)](#backend-deployment)
3. [Frontend Deployment (GitHub Pages)](#frontend-deployment)
4. [Testing Production](#testing-production)

---

## Local Development

### Prerequisites
- Python 3.8+
- Git & GitHub account
- Modern web browser

### Setup
```bash
# 1. Install dependencies
cd food_rescue
pip install -r requirements.txt

# 2. Run backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Open browser
http://localhost:8000
```

---

## Backend Deployment (Railway.app)

Railway.app is recommended because:
- ✅ Free tier available ($5-10/month)
- ✅ Simple CLI deployment
- ✅ Auto-scaling
- ✅ Environment variables support
- ✅ PostgreSQL included

### Step 1: Install Railway CLI
```bash
npm install -g railway
```

### Step 2: Login to Railway
```bash
railway login
```
(Browser will open for authentication)

### Step 3: Initialize Project
```bash
cd food_rescue
railway init

# Choose project name: zerohunger
# Select "Create a new project"
```

### Step 4: Add PostgreSQL Plugin
```bash
railway add

# Select "PostgreSQL"
```

### Step 5: Deploy Backend
```bash
railway up
```

### Step 6: Configure Environment
After deployment, set these variables in Railway dashboard:

**Via Railway CLI:**
```bash
railway variables set API_PORT=8000
railway variables set ENVIRONMENT=production
```

**Or manually in Railway dashboard:**
- Go to https://railway.app → Project → Variables
- Add all variables from `.env.example`

### Step 7: Get Your Backend URL
```bash
railway domains
```

**Output:** `https://your-app-xxxxx.railway.app`

### Step 8: Update Frontend
Edit the `docs/` folder files and update:
```javascript
// Change from:
const API_URL = "https://YOUR-BACKEND-URL.railway.app";

// To your actual Railway URL:
const API_URL = "https://your-app-xxxxx.railway.app";
```

Files to update:
- `docs/login.html` (line ~50)
- `docs/restaurant.html` (line ~42)
- `docs/volunteer.html` (line ~40)
- `docs/script.js` (line ~2)

---

## Frontend Deployment (GitHub Pages)

GitHub Pages automatically serves static files from `/docs` folder.

### Step 1: Verify `/docs` Folder
Your repo should have:
```
food_rescue/
├── docs/
│   ├── index.html
│   ├── login.html
│   ├── restaurant.html
│   ├── volunteer.html
│   ├── script.js
│   └── style.css
```

### Step 2: Enable GitHub Pages

1. Go to: **Settings → Pages**
   - URL: https://github.com/giridhar16-03/zerohunger/settings/pages

2. **Source**: Select `Deploy from a branch`

3. **Branch**: Select `main` → `/docs` folder

4. Click **Save**

### Step 3: GitHub Pages Will Build
- Wait 1-2 minutes
- You'll see a green checkmark when ready
- Visit: https://giridhar16-03.github.io/zerohunger/

---

## Testing Production

### Test Login Flow
1. Visit: https://giridhar16-03.github.io/zerohunger/
2. Click "Create Account"
3. Register as Restaurant
4. You should see the dashboard (if backend is running)

### Common Issues

**❌ Backend connection failed**
- Check Railway URL is correct
- Verify environment variables are set
- Check browser console for CORS errors

**❌ 404 Page Not Found**
- Verify files are in `/docs` folder
- Check GitHub Pages settings
- Wait 2-3 minutes after enabling Pages

**❌ Map won't load**
- Check Leaflet CDN link is correct
- Verify OpenStreetMap is accessible
- Check browser console for errors

---

## Production Checklist

- [ ] Backend deployed to Railway.app
- [ ] PostgreSQL configured in Railway
- [ ] Frontend API URLs updated to production backend
- [ ] Files committed to GitHub
- [ ] GitHub Pages enabled
- [ ] Frontend accessible at GitHub Pages URL
- [ ] Login works
- [ ] AI analysis working
- [ ] Orders displayed correctly
- [ ] Maps loading properly

---

## 🆘 Troubleshooting

### Railway Deployment Issues
```bash
# View logs
railway logs

# Check status
railway status

# Redeploy
railway up

# Remove and start fresh
railway remove
railway init
```

### GitHub Pages Issues
```bash
# Verify files are pushed
git status
git log

# Force push if needed
git push -f origin main

# Check GitHub Actions (Settings → Actions)
```

### Frontend-Backend Communication
- Check API_URL matches backend deployment URL
- Verify CORS is enabled on backend
- Check browser console for network errors

---

## 📊 Monitoring

### Railway Monitoring
- Visit: https://railway.app → Project → Deployments
- Monitor CPU, Memory, Requests

### GitHub Pages
- Visit: https://giridhar16-03.github.io/zerohunger/
- Check browser Console (F12) for errors

---

## 🔒 Security Notes

**For Production:**
1. Set `ENVIRONMENT=production` in Railway
2. Enable HTTPS (automatic with Railway)
3. Set strong passwords for test accounts
4. Move database to PostgreSQL (do not use SQLite)
5. Add rate limiting to API
6. Use environment variables for secrets

---

## 💡 Next Steps

1. **Deploy Backend** → Get Railway URL
2. **Update Frontend** → Add Railway URL to JS files
3. **Enable GitHub Pages** → Frontend live
4. **Test End-to-End** → Full flow working
5. **Monitor** → Check logs regularly

---

## 📞 Support

- **Railway Docs:** https://docs.railway.app
- **GitHub Pages:** https://pages.github.com
- **FastAPI:** https://fastapi.tiangolo.com
- **GitHub Issues:** Report bugs in repository

---

**Good luck with deployment! 🚀**
