---
title: Diabetic Retinopathy Detection
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.16.0
app_file: app.py
pinned: false
license: mit
---

# 🔬 Diabetic Retinopathy Detection System

AI-powered early detection of diabetic retinopathy using **ResNet-152 deep learning**. Upload retinal fundus images for instant 5-level severity classification.

## 🌟 Features

- **🎯 5-Level Classification**: No DR, Mild, Moderate, Severe, Proliferative DR
- **🧠 ResNet-152 Model**: State-of-the-art deep learning architecture
- **📊 Confidence Scores**: Get probability distribution for all severity levels
- **⚡ Instant Results**: Real-time analysis in seconds
- **🎨 Professional UI**: Clean, intuitive Gradio interface
- **📱 Responsive**: Works on desktop and mobile devices

## 🚀 How to Use

1. **Upload** a retinal fundus image (JPEG, PNG)
2. **Click** "Analyze Image" button
3. **View** results with:
   - Diagnosis and severity level
   - Confidence percentage
   - Risk assessment
   - Medical recommendations
   - Probability distribution chart

## 📋 Severity Levels

| Level | Classification | Description |
|-------|---------------|-------------|
| **0** | No DR | No signs of diabetic retinopathy |
| **1** | Mild | Mild non-proliferative DR |
| **2** | Moderate | Moderate non-proliferative DR |
| **3** | Severe | Severe non-proliferative DR |
| **4** | Proliferative DR | Advanced stage, urgent care needed |

## 🛠️ Technology Stack

- **Framework**: Gradio 4.0+
- **Deep Learning**: PyTorch 2.2+
- **Model**: ResNet-152 (pre-trained, fine-tuned)
- **Image Processing**: torchvision, Pillow
- **Deployment**: Hugging Face Spaces

## 📊 Model Architecture

```
Input (224x224 RGB)
    ↓
ResNet-152 Backbone
    ↓
Custom Classifier Head
    ├── Linear (2048 → 512)
    ├── ReLU
    ├── Linear (512 → 5)
    └── LogSoftmax
    ↓
Output (5 classes)
```

## ⚠️ Medical Disclaimer

**This tool is for educational and screening purposes only.**

- Not a substitute for professional medical diagnosis
- Always consult qualified healthcare professionals
- Results should be verified by ophthalmologists
- Do not make treatment decisions based solely on this tool

## 📄 Research

This project is based on published research in diabetic retinopathy detection using deep learning.

**Read the full paper**: [IJCSE Publication](https://www.ijcseonline.org/pub_paper/7-IJCSE-09595.pdf)

## 👨‍💻 Author

**Tansu Gangopadhyay**

- 🔗 [GitHub](https://github.com/tansugangopadhyay)
- 💼 [LinkedIn](https://www.linkedin.com/in/tansugangopadhyay/)
- 📧 [Contact](https://github.com/tansugangopadhyay)

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Dataset: Diabetic Retinopathy Detection Challenge
- Framework: PyTorch, Gradio
- Platform: Hugging Face Spaces

---

**© 2025 Tansu Gangopadhyay. All rights reserved.**

*Built with ❤️ using PyTorch and Gradio*
