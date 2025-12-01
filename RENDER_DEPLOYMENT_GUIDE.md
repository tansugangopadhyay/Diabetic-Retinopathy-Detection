# 🚀 Complete Render Deployment Guide

This guide will walk you through deploying your Diabetic Retinopathy Detection application on Render (both frontend and backend together).

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ A GitHub account
- ✅ A Render account (free) - Sign up at [render.com](https://render.com)
- ✅ Your project code ready
- ✅ The trained model file (`classifier.pt`)

---

## 🎯 Deployment Overview

Your app will be deployed as a **single web service** on Render that serves both:
- **Backend API** (Flask + PyTorch model)
- **Frontend** (HTML/CSS/JavaScript)

**Estimated Time:** 15-20 minutes  
**Cost:** FREE (Render Free Tier)

---

## 📝 Step-by-Step Deployment Process

### **STEP 1: Prepare Your GitHub Repository**

#### 1.1 Push Your Code to GitHub

If you haven't already pushed your code to GitHub:

```bash
# Navigate to your project directory
cd "C:\Users\tansu\Desktop\Diabetic-Retinopathy-Detection-main\Diabetic-Retinopathy-Detection-main"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Prepare for Render deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

#### 1.2 Verify Required Files

Make sure these files are in your repository:
- ✅ `app.py` (updated with PORT environment variable)
- ✅ `requirements.txt` (includes gunicorn)
- ✅ `render.yaml` (Render configuration)
- ✅ `frontend/` directory (with index.html, styles.css, script.js)
- ✅ `.gitignore` (excludes unnecessary files)

---

### **STEP 2: Upload Model File to Cloud Storage**

⚠️ **IMPORTANT:** The model file (`classifier.pt`) is too large for GitHub. You need to host it separately.

#### Option A: Use Google Drive (Recommended for Free)

1. **Upload `classifier.pt` to Google Drive**
   - Go to [drive.google.com](https://drive.google.com)
   - Upload your `classifier.pt` file
   
2. **Get Shareable Link**
   - Right-click on the file → "Get link"
   - Set permissions to "Anyone with the link can view"
   - Copy the link (it will look like: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`)

3. **Extract File ID**
   - From the URL above, copy the `FILE_ID` part
   - Example: If URL is `https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing`
   - File ID is: `1ABC123xyz`

4. **Create Download Script**
   - Create a file named `download_model.sh` in your project root:

```bash
#!/bin/bash
# Download model from Google Drive
FILE_ID="YOUR_FILE_ID_HERE"
DESTINATION="Retinal_blindness_detection_Pytorch-master/classifier.pt"

# Create directory if it doesn't exist
mkdir -p Retinal_blindness_detection_Pytorch-master

# Download using gdown
pip install gdown
gdown "https://drive.google.com/uc?id=${FILE_ID}" -O "${DESTINATION}"

echo "Model downloaded successfully!"
```

5. **Make it executable and add to git**
```bash
git add download_model.sh
git commit -m "Add model download script"
git push
```

#### Option B: Use Kaggle Dataset (Alternative)

If your model is already on Kaggle:
1. Use the Kaggle API to download during build
2. Add Kaggle credentials as environment variables in Render

---

### **STEP 3: Update Render Configuration**

Update your `render.yaml` to download the model during build:

```yaml
services:
  - type: web
    name: diabetic-retinopathy-detection
    env: python
    buildCommand: |
      pip install -r requirements.txt
      chmod +x download_model.sh
      ./download_model.sh
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 10000
    healthCheckPath: /api/health
    autoDeploy: true
```

Commit and push this change:
```bash
git add render.yaml
git commit -m "Update render config to download model"
git push
```

---

### **STEP 4: Deploy on Render**

#### 4.1 Create New Web Service

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** button → Select **"Web Service"**

2. **Connect GitHub Repository**
   - Click **"Connect account"** to link your GitHub
   - Authorize Render to access your repositories
   - Select your **Diabetic-Retinopathy-Detection** repository

3. **Configure Web Service**

   Fill in the following details:

   | Field | Value |
   |-------|-------|
   | **Name** | `diabetic-retinopathy-detection` |
   | **Region** | Choose closest to you (e.g., Oregon, Frankfurt) |
   | **Branch** | `main` (or your default branch) |
   | **Root Directory** | Leave blank |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt && chmod +x download_model.sh && ./download_model.sh` |
   | **Start Command** | `gunicorn app:app` |
   | **Plan** | **Free** |

4. **Add Environment Variables** (Optional)

   Click **"Advanced"** → **"Add Environment Variable"**:
   
   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.11.0` |
   | `PORT` | `10000` |

5. **Click "Create Web Service"**

---

### **STEP 5: Monitor Deployment**

#### 5.1 Watch Build Logs

- Render will start building your application
- You'll see logs showing:
  - ✅ Installing Python dependencies
  - ✅ Downloading PyTorch and torchvision
  - ✅ Downloading model file
  - ✅ Starting gunicorn server

**Expected Build Time:** 10-15 minutes (PyTorch is large)

#### 5.2 Check for Errors

Common issues and solutions:

| Error | Solution |
|-------|----------|
| **Model download failed** | Check your Google Drive link permissions |
| **Out of memory** | Render free tier has 512MB RAM - model might be too large |
| **Port binding error** | Ensure `app.py` uses `PORT` environment variable |
| **Module not found** | Verify all dependencies are in `requirements.txt` |

---

### **STEP 6: Test Your Deployment**

#### 6.1 Get Your App URL

Once deployment succeeds, Render will provide a URL like:
```
https://diabetic-retinopathy-detection.onrender.com
```

#### 6.2 Test the Application

1. **Open the URL in your browser**
   - You should see your frontend interface

2. **Test Health Check**
   - Visit: `https://your-app.onrender.com/api/health`
   - Should return:
   ```json
   {
     "status": "healthy",
     "model_loaded": true,
     "device": "cpu"
   }
   ```

3. **Test Image Upload**
   - Upload a retinal image
   - Click "Analyze Image"
   - Verify you get predictions

---

### **STEP 7: Configure Custom Domain (Optional)**

If you want a custom domain:

1. Go to **Settings** → **Custom Domain**
2. Add your domain (e.g., `retinopathy-detector.com`)
3. Update DNS records as instructed by Render
4. Wait for SSL certificate to be issued

---

## ⚙️ Important Render Free Tier Limitations

Be aware of these limitations:

| Limitation | Details |
|------------|---------|
| **RAM** | 512 MB (might be tight for PyTorch) |
| **CPU** | Shared CPU (slower inference) |
| **Sleep** | Service sleeps after 15 min of inactivity |
| **Cold Start** | First request after sleep takes 30-60 seconds |
| **Build Time** | 15 minutes max |
| **Bandwidth** | 100 GB/month |

### Handling Cold Starts

When your app sleeps, the first user will experience a delay. Solutions:

1. **Keep-Alive Service** (Free)
   - Use a service like [UptimeRobot](https://uptimerobot.com) to ping your app every 10 minutes
   
2. **Upgrade to Paid Plan** ($7/month)
   - No sleep
   - More RAM (1GB+)
   - Faster CPU

---

## 🔧 Troubleshooting

### Issue: Model Not Loading

**Symptoms:** API returns "Model not loaded" error

**Solutions:**
1. Check build logs - did model download succeed?
2. Verify model path in `app.py` matches download location
3. Check Google Drive link is public
4. Try downloading model manually and checking file size

### Issue: Out of Memory

**Symptoms:** App crashes or restarts frequently

**Solutions:**
1. **Optimize model loading:**
   ```python
   # In app.py, use map_location='cpu' and weights_only=True
   checkpoint = torch.load(path, map_location='cpu', weights_only=True)
   ```

2. **Use a smaller model** (if available)

3. **Upgrade to paid plan** for more RAM

### Issue: Slow Inference

**Symptoms:** Predictions take 10+ seconds

**Solutions:**
- This is normal on free tier (CPU-only, shared resources)
- Consider upgrading to a paid plan with more CPU
- Optimize image preprocessing

### Issue: Service Keeps Sleeping

**Symptoms:** First request is always slow

**Solutions:**
1. Set up UptimeRobot to ping every 10 minutes
2. Upgrade to paid plan ($7/month) for always-on service

---

## 📊 Monitoring Your App

### View Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs for errors

### Check Metrics

1. Click **"Metrics"** tab
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🔄 Updating Your App

### Automatic Deployment

Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature X"
git push

# Render will automatically detect and redeploy
```

### Manual Deployment

1. Go to Render dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 💰 Cost Optimization Tips

1. **Use Free Tier Wisely**
   - Perfect for demos and portfolios
   - Not recommended for production with high traffic

2. **Monitor Usage**
   - Check bandwidth usage monthly
   - Watch for unexpected traffic spikes

3. **Upgrade When Needed**
   - If you get consistent traffic, upgrade to $7/month plan
   - Better performance and no sleep

---

## 🎉 Success Checklist

After deployment, verify:

- ✅ App URL is accessible
- ✅ Frontend loads correctly
- ✅ `/api/health` returns healthy status
- ✅ Model is loaded (`model_loaded: true`)
- ✅ Image upload works
- ✅ Predictions are accurate
- ✅ No errors in logs

---

## 📞 Getting Help

### Render Support
- [Render Documentation](https://render.com/docs)
- [Render Community Forum](https://community.render.com)
- [Render Status Page](https://status.render.com)

### Common Resources
- [Flask Deployment Guide](https://render.com/docs/deploy-flask)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Build & Deploy](https://render.com/docs/deploys)

---

## 🚀 Next Steps

After successful deployment:

1. **Share Your App**
   - Add the URL to your GitHub README
   - Share on LinkedIn/Twitter
   - Add to your portfolio

2. **Monitor Performance**
   - Set up UptimeRobot for monitoring
   - Check logs regularly
   - Monitor error rates

3. **Gather Feedback**
   - Test with real users
   - Collect feedback
   - Iterate and improve

4. **Consider Upgrades**
   - If traffic increases, upgrade to paid plan
   - Add custom domain
   - Enable auto-scaling

---

## 📝 Quick Reference Commands

```bash
# Check git status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# View git log
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

**Congratulations! 🎉** Your Diabetic Retinopathy Detection app is now live on Render!

**Your App URL:** `https://diabetic-retinopathy-detection.onrender.com`

---

*Last Updated: December 1, 2025*
