# ⚡ Render Deployment - Quick Start

**Time Required:** 15-20 minutes  
**Cost:** FREE

---

## 🎯 Quick Steps

### 1️⃣ Upload Model to Google Drive

1. Upload `classifier.pt` to Google Drive
2. Right-click → "Get link" → Set to "Anyone with the link"
3. Copy the File ID from the URL
4. Update `download_model.sh` with your File ID:
   ```bash
   FILE_ID="YOUR_FILE_ID_HERE"  # Replace this
   ```

### 2️⃣ Push to GitHub

```bash
cd "C:\Users\tansu\Desktop\Diabetic-Retinopathy-Detection-main\Diabetic-Retinopathy-Detection-main"

git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 3️⃣ Deploy on Render

1. Go to [render.com](https://render.com) → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `diabetic-retinopathy-detection`
   - **Build Command:** `pip install -r requirements.txt && chmod +x download_model.sh && ./download_model.sh`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
5. Click **"Create Web Service"**

### 4️⃣ Wait for Deployment

- Build takes ~10-15 minutes
- Watch logs for progress
- Once complete, your app will be live!

### 5️⃣ Test Your App

Visit: `https://your-app-name.onrender.com`

Test API: `https://your-app-name.onrender.com/api/health`

---

## ⚠️ Important Notes

- **First Load:** Takes 30-60 seconds (cold start)
- **Free Tier:** App sleeps after 15 min of inactivity
- **RAM Limit:** 512 MB (might be tight for PyTorch)
- **Solution:** Use [UptimeRobot](https://uptimerobot.com) to keep app awake

---

## 🆘 Need Help?

See the full guide: `RENDER_DEPLOYMENT_GUIDE.md`

---

## ✅ Success Checklist

- [ ] Model uploaded to Google Drive
- [ ] File ID updated in `download_model.sh`
- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Build completed successfully
- [ ] App URL accessible
- [ ] Health check returns `model_loaded: true`
- [ ] Image upload and prediction working

---

**That's it! Your app is live! 🚀**
