# 🔧 Render Deployment Troubleshooting Guide

This guide helps you solve common issues when deploying to Render.

---

## 🚨 Common Issues & Solutions

### 1. Model Download Fails

**Error Message:**
```
❌ Model download failed!
gdown: error: file ID not found
```

**Causes:**
- Google Drive file ID is incorrect
- File permissions are not set to "Anyone with the link"
- File was deleted or moved

**Solutions:**

✅ **Verify Google Drive Link:**
1. Go to Google Drive
2. Right-click on `classifier.pt` → "Get link"
3. Ensure it's set to "Anyone with the link can view"
4. Copy the link: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
5. Extract the `FILE_ID` portion

✅ **Update download_model.sh:**
```bash
FILE_ID="1ABC123xyz"  # Replace with your actual File ID
```

✅ **Test Download Locally:**
```bash
pip install gdown
gdown "https://drive.google.com/uc?id=YOUR_FILE_ID" -O test_model.pt
```

✅ **Alternative: Use Direct Download Link:**
If gdown fails, try using `wget` or `curl`:
```bash
# In download_model.sh, replace gdown with:
wget --no-check-certificate "https://drive.google.com/uc?export=download&id=${FILE_ID}" -O "${DESTINATION}"
```

---

### 2. Out of Memory Error

**Error Message:**
```
Error: Process out of memory
Killed
```

**Causes:**
- PyTorch model is too large for 512MB RAM
- Multiple processes consuming memory
- Memory leak during model loading

**Solutions:**

✅ **Optimize Model Loading:**

Update `app.py`:
```python
# Use weights_only=True to reduce memory usage
checkpoint = torch.load(path, map_location='cpu', weights_only=True)
```

✅ **Reduce Dependencies:**

Remove unnecessary packages from `requirements.txt`:
```text
# Only keep essential packages
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
torch>=2.2.0
torchvision>=0.17.0
Pillow>=10.0.0
numpy>=1.24.0
gunicorn>=21.2.0
```

✅ **Use CPU-Only PyTorch:**

Install CPU-only version (smaller):
```bash
# In requirements.txt
torch==2.2.0+cpu
torchvision==0.17.0+cpu
--find-links https://download.pytorch.org/whl/torch_stable.html
```

✅ **Upgrade to Paid Plan:**
- Render Starter plan: $7/month, 512MB → 2GB RAM
- Render Standard plan: $25/month, 4GB RAM

---

### 3. Build Timeout

**Error Message:**
```
Build exceeded maximum time limit of 15 minutes
```

**Causes:**
- PyTorch installation takes too long
- Model download is slow
- Too many dependencies

**Solutions:**

✅ **Use Pre-built Wheels:**

Add to `requirements.txt`:
```text
--find-links https://download.pytorch.org/whl/torch_stable.html
torch==2.2.0+cpu
torchvision==0.17.0+cpu
```

✅ **Cache Dependencies:**

Render automatically caches pip packages between builds. Ensure you're not clearing cache.

✅ **Optimize Model Download:**

Use a faster CDN or smaller model file if possible.

---

### 4. Port Binding Error

**Error Message:**
```
Error: Address already in use
Error: Failed to bind to port
```

**Causes:**
- App not using Render's PORT environment variable
- Multiple processes trying to use same port

**Solutions:**

✅ **Verify app.py Uses PORT:**

```python
# At the end of app.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

✅ **Check Start Command:**

In `render.yaml`:
```yaml
startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
```

Or simply:
```yaml
startCommand: gunicorn app:app
```
(Gunicorn automatically uses PORT env var)

---

### 5. Module Not Found Error

**Error Message:**
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'torch'
```

**Causes:**
- Dependencies not installed
- Wrong Python version
- requirements.txt not found

**Solutions:**

✅ **Verify requirements.txt:**

Ensure all dependencies are listed:
```text
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
torch>=2.2.0
torchvision>=0.17.0
Pillow>=10.0.0
numpy>=1.24.0
gunicorn>=21.2.0
```

✅ **Check Build Command:**

In Render dashboard or `render.yaml`:
```yaml
buildCommand: pip install -r requirements.txt
```

✅ **Verify Python Version:**

```yaml
envVars:
  - key: PYTHON_VERSION
    value: 3.11.0
```

---

### 6. Model Not Loading

**Error Message:**
```json
{
  "status": "healthy",
  "model_loaded": false,
  "device": "cpu"
}
```

**Causes:**
- Model file not downloaded
- Wrong model path
- Corrupted model file
- Model file format incompatible

**Solutions:**

✅ **Check Build Logs:**

Look for:
```
✅ Model downloaded successfully!
File size: 500M
```

✅ **Verify Model Path:**

In `app.py`:
```python
MODEL_PATH = 'Retinal_blindness_detection_Pytorch-master/classifier.pt'
```

Should match the path in `download_model.sh`:
```bash
DESTINATION="Retinal_blindness_detection_Pytorch-master/classifier.pt"
```

✅ **Test Model Loading:**

Add debug logging in `app.py`:
```python
def load_model(path):
    try:
        print(f"Attempting to load model from: {path}")
        print(f"File exists: {os.path.exists(path)}")
        if os.path.exists(path):
            print(f"File size: {os.path.getsize(path)} bytes")
        
        checkpoint = torch.load(path, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        model.eval()
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False
```

---

### 7. CORS Errors

**Error Message (in browser console):**
```
Access to fetch at 'https://your-app.onrender.com/api/predict' 
from origin 'https://your-app.onrender.com' has been blocked by CORS policy
```

**Causes:**
- CORS not properly configured
- Missing flask-cors package

**Solutions:**

✅ **Verify CORS Setup:**

In `app.py`:
```python
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend')
CORS(app)  # Enable CORS for all routes
```

✅ **Install flask-cors:**

In `requirements.txt`:
```text
flask-cors==4.0.0
```

✅ **Specific CORS Configuration:**

If you need more control:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

### 8. Slow Cold Starts

**Issue:**
First request after inactivity takes 30-60 seconds

**Causes:**
- Free tier services sleep after 15 minutes of inactivity
- Model needs to be loaded into memory

**Solutions:**

✅ **Use UptimeRobot (Free):**

1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Create new monitor:
   - Type: HTTP(s)
   - URL: `https://your-app.onrender.com/api/health`
   - Interval: 5 minutes
3. This keeps your app awake

✅ **Upgrade to Paid Plan:**
- $7/month Starter plan = no sleep
- Always-on service
- Faster response times

✅ **Optimize Model Loading:**

Cache model in memory:
```python
# Load model once at startup, not per request
model_loaded = load_model(MODEL_PATH)
```

---

### 9. File Upload Errors

**Error Message:**
```json
{
  "error": "No file provided"
}
```

**Causes:**
- Frontend not sending file correctly
- File size exceeds limit
- Wrong content-type

**Solutions:**

✅ **Check File Size Limit:**

In `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

✅ **Verify Frontend Upload:**

In `script.js`:
```javascript
const formData = new FormData();
formData.append('file', file);

fetch('/api/predict', {
    method: 'POST',
    body: formData  // Don't set Content-Type header
})
```

✅ **Check Allowed Extensions:**

In `app.py`:
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

---

### 10. Static Files Not Loading

**Issue:**
CSS/JS files return 404 errors

**Causes:**
- Wrong static folder configuration
- Files not in correct directory

**Solutions:**

✅ **Verify Static Folder:**

In `app.py`:
```python
app = Flask(__name__, static_folder='frontend')
```

✅ **Check Route Configuration:**

```python
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)
```

✅ **Verify File Structure:**

```
project/
├── app.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
```

---

## 🔍 Debugging Tips

### View Live Logs

1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. Watch real-time logs

### Test Locally First

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Test in browser
http://localhost:5000
```

### Check Environment Variables

In Render dashboard:
1. Go to "Environment" tab
2. Verify all variables are set correctly
3. Add debug variables if needed:
   ```
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

### Manual Deploy

Force a new deployment:
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"

---

## 📞 Getting More Help

### Render Support
- [Render Docs](https://render.com/docs)
- [Community Forum](https://community.render.com)
- [Status Page](https://status.render.com)

### Project Issues
- Check GitHub Issues
- Review deployment logs
- Test locally first

---

## ✅ Pre-Deployment Checklist

Before deploying, verify:

- [ ] All files committed to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] Model uploaded to Google Drive
- [ ] File ID updated in `download_model.sh`
- [ ] `app.py` uses PORT environment variable
- [ ] CORS is enabled
- [ ] Static folder configured correctly
- [ ] `.gitignore` excludes large files
- [ ] Tested locally and works

---

**Still having issues?** Check the full deployment guide: `RENDER_DEPLOYMENT_GUIDE.md`
