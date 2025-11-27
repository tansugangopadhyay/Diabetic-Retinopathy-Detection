# ⚡ QUICK REFERENCE CARD

## 🚀 Start the Application

```bash
# Method 1: Double-click
start.bat

# Method 2: Command line
python app.py
```

**Access at**: http://localhost:5000

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend server |
| `frontend/index.html` | Main web page |
| `frontend/styles.css` | Styling |
| `frontend/script.js` | Interactions |
| `config.py` | Settings |
| `requirements.txt` | Dependencies |

---

## ⚠️ BEFORE FIRST RUN

**Download Model File:**
1. Go to: https://www.kaggle.com/souravs17031999/blindness-detection-pretrained-weights-pytorch
2. Download: `classifier.pt`
3. Place in: `Retinal_blindness_detection_Pytorch-master/classifier.pt`

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

---

## 🎯 Usage Flow

1. **Start Server** → `python app.py`
2. **Open Browser** → http://localhost:5000
3. **Upload Image** → Drag & drop or click
4. **Click Analyze** → Wait 2-5 seconds
5. **View Results** → See diagnosis & recommendations

---

## 🎨 Severity Levels

| Level | Name | Color | Action |
|-------|------|-------|--------|
| 0 | No DR | 🟢 | Monitor regularly |
| 1 | Mild | 🔵 | Check in 6-12 months |
| 2 | Moderate | 🟠 | Consult in 3-6 months |
| 3 | Severe | 🔴 | See specialist soon |
| 4 | Proliferative | 🔴 | Urgent treatment |

---

## 🔌 API Endpoints

```http
GET  /api/health          # Check server status
POST /api/predict         # Analyze image
GET  /api/classes         # Get severity info
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Model not loaded | Download classifier.pt |
| Can't connect | Start Flask server |
| Module not found | `pip install -r requirements.txt` |
| Port in use | Change port in app.py |

---

## 📊 Test Images

Sample images available in:
```
Retinal_blindness_detection_Pytorch-master/sampleimages/
```

Try: `eye1.png`, `eye2.png`, etc.

---

## 🎨 Design Colors

- **Primary**: #3b82f6 (Blue)
- **Secondary**: #8b5cf6 (Purple)
- **Background**: #0f172a (Navy)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Orange)
- **Danger**: #ef4444 (Red)

---

## 📝 Key Features

✅ Drag & drop upload
✅ Real-time analysis
✅ Circular progress indicator
✅ Probability charts
✅ Medical recommendations
✅ Responsive design
✅ Dark theme
✅ Smooth animations

---

## 🔧 Configuration

Edit `config.py` to change:
- Port number
- Upload folder
- Max file size
- Model path
- Image size

---

## 📚 Documentation

- **Setup**: `SETUP_GUIDE.md`
- **Complete Docs**: `README.md`
- **Summary**: `PROJECT_SUMMARY.md`
- **This Card**: `QUICK_REFERENCE.md`

---

## 💡 Pro Tips

1. Use high-quality retinal images
2. JPEG format recommended
3. Test with sample images first
4. Check terminal for errors
5. GPU speeds up inference

---

## 🎉 That's It!

**You're ready to detect diabetic retinopathy with AI!**

Need help? Check the documentation files above.

---

**Made with ❤️ | RetinaAI**
