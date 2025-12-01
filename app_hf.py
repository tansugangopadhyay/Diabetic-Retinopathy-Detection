import gradio as gr
import torch
from torch import nn
import torchvision
from torchvision import models
from PIL import Image
import numpy as np

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
MODEL_PATH = 'Retinal_blindness_detection_Pytorch-master/classifier.pt'

def load_model(path):
    """Load the trained model from checkpoint"""
    try:
        checkpoint = torch.load(path, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        model.eval()
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

# Load model on startup
model_loaded = load_model(MODEL_PATH)

# Classes for diabetic retinopathy severity
CLASSES = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']

# Image transformations
test_transforms = torchvision.transforms.Compose([
    torchvision.transforms.Resize((224, 224)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

def get_severity_info(severity_level):
    """Get detailed information about each severity level"""
    info = {
        0: {
            'level': 'No DR',
            'description': 'No signs of diabetic retinopathy detected.',
            'recommendation': 'Continue regular eye examinations and maintain good blood sugar control.',
            'risk': 'Low'
        },
        1: {
            'level': 'Mild',
            'description': 'Mild non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Schedule a follow-up examination within 6-12 months. Maintain strict blood sugar control.',
            'risk': 'Low-Medium'
        },
        2: {
            'level': 'Moderate',
            'description': 'Moderate non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Consult with an ophthalmologist within 3-6 months. Close monitoring required.',
            'risk': 'Medium'
        },
        3: {
            'level': 'Severe',
            'description': 'Severe non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Immediate consultation with a retinal specialist required. Treatment may be necessary.',
            'risk': 'High'
        },
        4: {
            'level': 'Proliferative DR',
            'description': 'Proliferative diabetic retinopathy detected.',
            'recommendation': 'Urgent medical attention required. Immediate treatment necessary to prevent vision loss.',
            'risk': 'Critical'
        }
    }
    return info.get(severity_level, info[0])

def predict_image(image):
    """Make prediction on the uploaded image"""
    if not model_loaded:
        return "❌ Model not loaded. Please check the model file.", None, None
    
    try:
        # Transform image
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
        
        # Get severity info
        info = get_severity_info(severity_value)
        
        # Create result text
        result_text = f"""
## 🔬 Analysis Results

**Diagnosis:** {info['level']}  
**Confidence:** {confidence:.2f}%  
**Risk Level:** {info['risk']}

### 📋 Description
{info['description']}

### 💡 Recommendation
{info['recommendation']}

### ⚠️ Disclaimer
This tool is for educational and screening purposes only. Always consult with a qualified healthcare professional for medical diagnosis and treatment.
"""
        
        # Create probability distribution
        prob_dict = {CLASSES[i]: float(prob) * 100 for i, prob in enumerate(probabilities)}
        
        return result_text, prob_dict, image
        
    except Exception as e:
        return f"❌ Error during prediction: {str(e)}", None, None

# Create Gradio interface
with gr.Blocks(title="Diabetic Retinopathy Detection", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔬 Diabetic Retinopathy Detection System
    ### AI-Powered Early Detection using ResNet-152 Deep Learning
    
    Upload a retinal fundus image to detect and classify diabetic retinopathy severity.
    
    **Made by Tansu Gangopadhyay** | [GitHub](https://github.com/tansugangopadhyay) | [LinkedIn](https://www.linkedin.com/in/tansugangopadhyay/) | [Research Paper](https://www.ijcseonline.org/pub_paper/7-IJCSE-09595.pdf)
    """)
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Upload Retinal Image")
            analyze_btn = gr.Button("🔍 Analyze Image", variant="primary", size="lg")
            
            gr.Markdown("""
            ### 📊 Severity Levels
            - **Level 0:** No DR - No signs detected
            - **Level 1:** Mild - Mild non-proliferative DR
            - **Level 2:** Moderate - Moderate non-proliferative DR
            - **Level 3:** Severe - Severe non-proliferative DR
            - **Level 4:** Proliferative DR - Urgent attention required
            """)
        
        with gr.Column():
            result_text = gr.Markdown(label="Results")
            probability_plot = gr.BarPlot(
                x="Class",
                y="Probability (%)",
                title="Probability Distribution",
                y_lim=[0, 100],
                height=300
            )
            result_image = gr.Image(label="Analyzed Image")
    
    # Event handler
    analyze_btn.click(
        fn=predict_image,
        inputs=[input_image],
        outputs=[result_text, probability_plot, result_image]
    )
    
    gr.Markdown("""
    ---
    ### 🌟 About This Project
    This system uses a ResNet-152 deep learning model trained on retinal fundus images to detect and classify diabetic retinopathy into 5 severity levels. 
    The model achieves medical-grade accuracy for early detection and prevention of vision loss.
    
    **Technology Stack:** PyTorch, ResNet-152, Gradio, Python
    
    © 2025 Tansu Gangopadhyay. All rights reserved.
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
