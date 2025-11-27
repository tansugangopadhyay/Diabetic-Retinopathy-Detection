# 🔬 Diabetic Retinopathy Detection System

An advanced AI-powered web application for detecting and classifying diabetic retinopathy from retinal fundus images using deep learning.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-1.13.1-red.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **AI-Powered Detection**: Uses ResNet-152 deep learning architecture for accurate classification
- **5 Severity Levels**: Classifies diabetic retinopathy into 5 stages (No DR, Mild, Moderate, Severe, Proliferative DR)
- **Modern Web Interface**: Beautiful, responsive UI with real-time analysis
- **High Accuracy**: Trained model achieves medical-grade accuracy
- **Detailed Results**: Provides confidence scores, probability distributions, and medical recommendations
- **Easy to Use**: Simple drag-and-drop interface for image upload

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Model Setup](#-model-setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Research Paper](#-research-paper)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended
- CUDA-capable GPU (optional, for faster inference)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Diabetic-Retinopathy-Detection-main
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🧠 Model Setup

The trained model file (`classifier.pt`) needs to be downloaded separately due to its large size.

### Download the Model

1. Download the pre-trained ResNet-152 model from:
   - **Kaggle**: [Blindness Detection Pretrained Weights](https://www.kaggle.com/souravs17031999/blindness-detection-pretrained-weights-pytorch)
   
2. Place the `classifier.pt` file in the following location:
   ```
   Diabetic-Retinopathy-Detection-main/
   └── Retinal_blindness_detection_Pytorch-master/
       └── classifier.pt
   ```

### Verify Model Path

Ensure the model path in `app.py` matches your setup:
```python
MODEL_PATH = 'Retinal_blindness_detection_Pytorch-master/classifier.pt'
```

## 💻 Usage

### Starting the Application

1. **Start the Backend Server**:
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

2. **Access the Web Interface**:
   - Open your browser and navigate to: `http://localhost:5000`
   - Or open `frontend/index.html` directly in your browser

### Using the Application

1. **Upload Image**:
   - Click on the upload area or drag and drop a retinal fundus image
   - Supported formats: PNG, JPG, JPEG (Max 16MB)

2. **Analyze**:
   - Click the "Analyze Image" button
   - Wait for the AI model to process the image

3. **View Results**:
   - See the severity classification
   - Review confidence scores and probability distribution
   - Read medical recommendations

### Sample Images

Test images are available in:
```
Retinal_blindness_detection_Pytorch-master/sampleimages/
```

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda" | "cpu"
}
```

#### 2. Predict
```http
POST /api/predict
```

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "severity_value": 0,
  "severity_class": "No DR",
  "confidence": 98.5,
  "probabilities": {
    "No DR": 98.5,
    "Mild": 1.2,
    "Moderate": 0.2,
    "Severe": 0.05,
    "Proliferative DR": 0.05
  },
  "info": {
    "level": "No DR",
    "description": "No signs of diabetic retinopathy detected.",
    "recommendation": "Continue regular eye examinations...",
    "color": "#10b981",
    "risk": "Low"
  },
  "image_data": "data:image/jpeg;base64,..."
}
```

#### 3. Get Classes
```http
GET /api/classes
```

**Response:**
```json
{
  "classes": ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"],
  "info": [...]
}
```

## 📁 Project Structure

```
Diabetic-Retinopathy-Detection-main/
├── app.py                          # Flask backend server
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # License file
├── Research Paper.pdf              # Published research paper
│
├── frontend/                       # Web frontend
│   ├── index.html                  # Main HTML file
│   ├── styles.css                  # Styling
│   └── script.js                   # JavaScript logic
│
├── Retinal_blindness_detection_Pytorch-master/
│   ├── classifier.pt               # Trained model (download separately)
│   ├── model.py                    # Model architecture
│   ├── blindness.py                # Original GUI application
│   ├── sampleimages/               # Test images
│   ├── training.ipynb              # Training notebook
│   ├── inference.ipynb             # Inference notebook
│   └── requirements.txt            # Original requirements
│
└── uploads/                        # Temporary upload folder (auto-created)
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Deep Learning**: PyTorch 1.13.1
- **Model**: ResNet-152 (pretrained and fine-tuned)
- **Image Processing**: Pillow, torchvision
- **API**: RESTful API with CORS support

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients, animations, glassmorphism
- **JavaScript**: Vanilla JS (no frameworks)
- **Fonts**: Inter, Space Grotesk (Google Fonts)

### Model Architecture
- **Base Model**: ResNet-152
- **Custom Classifier**: 
  - Linear(2048 → 512) + ReLU
  - Linear(512 → 5) + LogSoftmax
- **Loss Function**: Negative Log Likelihood Loss
- **Optimizer**: Adam
- **Input Size**: 224×224 RGB images

## 📊 Severity Levels

| Level | Classification | Description | Risk |
|-------|---------------|-------------|------|
| 0 | No DR | No signs of diabetic retinopathy | Low |
| 1 | Mild | Mild non-proliferative diabetic retinopathy | Low-Medium |
| 2 | Moderate | Moderate non-proliferative diabetic retinopathy | Medium |
| 3 | Severe | Severe non-proliferative diabetic retinopathy | High |
| 4 | Proliferative DR | Proliferative diabetic retinopathy | Critical |

## 📄 Research Paper

This project is based on published research on diabetic retinopathy detection using deep learning. The research paper is included in the repository as `Research Paper.pdf`.

## 🔧 Troubleshooting

### Model Not Loading
- Ensure `classifier.pt` is in the correct location
- Check the `MODEL_PATH` variable in `app.py`
- Verify the model file is not corrupted

### CORS Errors
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that the backend server is running

### Out of Memory
- Use CPU instead of GPU for inference
- Reduce batch size (already set to 1 for single image inference)
- Close other applications

### Port Already in Use
- Change the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational and screening purposes only. It is not a substitute for professional medical diagnosis. Always consult with a qualified healthcare professional for medical advice and treatment.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Original Model & Research: [Research Team]
- Web Application: [Your Name]

## 🙏 Acknowledgments

- ResNet architecture by Microsoft Research
- PyTorch framework
- Kaggle for hosting the dataset and model weights
- Medical professionals for domain expertise

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Made with ❤️ for early detection and prevention of diabetic retinopathy**
