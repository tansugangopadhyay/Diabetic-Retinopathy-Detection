"""
Flask Backend API for Diabetic Retinopathy Detection
Serves the PyTorch ResNet-152 model for retinal image classification
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import torch
from torch import nn
import torchvision
from torchvision import models
from PIL import Image
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_PATH = 'Retinal_blindness_detection_Pytorch-master/classifier.pt'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Model setup
model = models.resnet152(pretrained=False)
num_ftrs = model.fc.in_features
out_ftrs = 5
model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 512),
    nn.ReLU(),
    nn.Linear(512, out_ftrs),
    nn.LogSoftmax(dim=1)
)

# Load model weights
def load_model(path):
    """Load the trained model from checkpoint"""
    try:
        checkpoint = torch.load(path, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        model.eval()
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

# Classes for diabetic retinopathy severity
CLASSES = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']

# Image transformations
test_transforms = torchvision.transforms.Compose([
    torchvision.transforms.Resize((224, 224)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

# Load model on startup
model_loaded = load_model(MODEL_PATH)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_severity_info(severity_level):
    """Get detailed information about each severity level"""
    info = {
        0: {
            'level': 'No DR',
            'description': 'No signs of diabetic retinopathy detected.',
            'recommendation': 'Continue regular eye examinations and maintain good blood sugar control.',
            'color': '#10b981',
            'risk': 'Low'
        },
        1: {
            'level': 'Mild',
            'description': 'Mild non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Schedule a follow-up examination within 6-12 months. Maintain strict blood sugar control.',
            'color': '#3b82f6',
            'risk': 'Low-Medium'
        },
        2: {
            'level': 'Moderate',
            'description': 'Moderate non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Consult with an ophthalmologist within 3-6 months. Close monitoring required.',
            'color': '#f59e0b',
            'risk': 'Medium'
        },
        3: {
            'level': 'Severe',
            'description': 'Severe non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Immediate consultation with a retinal specialist required. Treatment may be necessary.',
            'color': '#ef4444',
            'risk': 'High'
        },
        4: {
            'level': 'Proliferative DR',
            'description': 'Proliferative diabetic retinopathy detected.',
            'recommendation': 'Urgent medical attention required. Immediate treatment necessary to prevent vision loss.',
            'color': '#dc2626',
            'risk': 'Critical'
        }
    }
    return info.get(severity_level, info[0])

def predict_image(image_path):
    """Make prediction on the uploaded image"""
    try:
        # Load and transform image
        image = Image.open(image_path).convert('RGB')
        img_tensor = test_transforms(image).unsqueeze(0)
        
        # Make prediction
        with torch.no_grad():
            output = model(img_tensor.to(device))
            ps = torch.exp(output)
            top_p, top_class = ps.topk(1, dim=1)
            
            severity_value = top_class.item()
            confidence = top_p.item() * 100
            
            # Get all class probabilities
            probabilities = ps[0].cpu().numpy()
            
        return {
            'severity_value': severity_value,
            'severity_class': CLASSES[severity_value],
            'confidence': round(confidence, 2),
            'probabilities': {CLASSES[i]: round(float(prob) * 100, 2) for i, prob in enumerate(probabilities)},
            'info': get_severity_info(severity_value)
        }
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('frontend', path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'device': str(device)
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded. Please check model path.'}), 500
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG.'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        result = predict_image(filepath)
        
        # Convert image to base64 for display
        with open(filepath, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        result['image_data'] = f"data:image/jpeg;base64,{img_data}"
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get all severity classes"""
    return jsonify({
        'classes': CLASSES,
        'info': [get_severity_info(i) for i in range(len(CLASSES))]
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Diabetic Retinopathy Detection System")
    print("=" * 60)
    print(f"Model Path: {MODEL_PATH}")
    print(f"Model Loaded: {model_loaded}")
    print(f"Device: {device}")
    print("=" * 60)
    
    if not model_loaded:
        print("\n⚠️  WARNING: Model not loaded!")
        print(f"Please ensure the model file exists at: {MODEL_PATH}")
        print("Download from: https://www.kaggle.com/souravs17031999/blindness-detection-pretrained-weights-pytorch")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
