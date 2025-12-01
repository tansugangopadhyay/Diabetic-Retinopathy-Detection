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
            'risk': 'Low',
            'color': '#10b981'
        },
        1: {
            'level': 'Mild',
            'description': 'Mild non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Schedule a follow-up examination within 6-12 months. Maintain strict blood sugar control.',
            'risk': 'Low-Medium',
            'color': '#3b82f6'
        },
        2: {
            'level': 'Moderate',
            'description': 'Moderate non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Consult with an ophthalmologist within 3-6 months. Close monitoring required.',
            'risk': 'Medium',
            'color': '#f59e0b'
        },
        3: {
            'level': 'Severe',
            'description': 'Severe non-proliferative diabetic retinopathy detected.',
            'recommendation': 'Immediate consultation with a retinal specialist required. Treatment may be necessary.',
            'risk': 'High',
            'color': '#ef4444'
        },
        4: {
            'level': 'Proliferative DR',
            'description': 'Proliferative diabetic retinopathy detected.',
            'recommendation': 'Urgent medical attention required. Immediate treatment necessary to prevent vision loss.',
            'risk': 'Critical',
            'color': '#dc2626'
        }
    }
    return info.get(severity_level, info[0])

def predict_image(image):
    """Make prediction on the uploaded image"""
    if not model_loaded:
        return "❌ Model not loaded. Please check the model file.", None
    
    if image is None:
        return "⚠️ Please upload an image first.", None
    
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
        
        # Create beautiful result HTML
        result_html = f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 1rem; color: white; margin: 1rem 0;">
            <h2 style="margin: 0 0 1rem 0; font-size: 2rem;">🔬 Analysis Complete</h2>
            
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Diagnosis</p>
                        <h3 style="margin: 0.25rem 0 0 0; font-size: 1.75rem; color: {info['color']};">
                            {info['level']}
                        </h3>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Confidence</p>
                        <h3 style="margin: 0.25rem 0 0 0; font-size: 1.75rem;">{confidence:.1f}%</h3>
                    </div>
                </div>
                
                <div style="background: rgba(0,0,0,0.2); height: 8px; border-radius: 100px; overflow: hidden; margin: 1rem 0;">
                    <div style="background: {info['color']}; height: 100%; width: {confidence}%; border-radius: 100px; transition: width 1s ease;"></div>
                </div>
                
                <p style="margin: 0; opacity: 0.9;">Risk Level: <strong>{info['risk']}</strong></p>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0;">
                <h4 style="margin: 0 0 0.5rem 0;">📋 Description</h4>
                <p style="margin: 0; line-height: 1.6;">{info['description']}</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 0.75rem; margin: 1rem 0;">
                <h4 style="margin: 0 0 0.5rem 0;">💡 Recommendation</h4>
                <p style="margin: 0; line-height: 1.6;">{info['recommendation']}</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 3px solid #fbbf24;">
                <p style="margin: 0; font-size: 0.875rem; opacity: 0.9;">
                    ⚠️ <strong>Disclaimer:</strong> This tool is for educational and screening purposes only. 
                    Always consult with a qualified healthcare professional for medical diagnosis and treatment.
                </p>
            </div>
        </div>
        
        <div style="margin-top: 1.5rem;">
            <h4 style="margin-bottom: 1rem;">📊 Probability Distribution</h4>
            <div style="background: white; padding: 1.5rem; border-radius: 0.75rem;">
                {''.join([f'''
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="color: #374151; font-weight: 500;">{CLASSES[i]}</span>
                        <span style="color: #6b7280; font-weight: 600;">{prob*100:.1f}%</span>
                    </div>
                    <div style="background: #e5e7eb; height: 8px; border-radius: 100px; overflow: hidden;">
                        <div style="background: {get_severity_info(i)['color']}; height: 100%; width: {prob*100}%; border-radius: 100px;"></div>
                    </div>
                </div>
                ''' for i, prob in enumerate(probabilities)])}
            </div>
        </div>
        """
        
        return result_html, image
        
    except Exception as e:
        return f"❌ Error during prediction: {str(e)}", None

# Custom CSS for better styling
custom_css = """
#component-0 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.1rem !important;
}
.gr-button-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4) !important;
}
"""

# Create Gradio interface with custom theme
with gr.Blocks(css=custom_css, title="Diabetic Retinopathy Detection", theme=gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="blue",
)) as demo:
    
    gr.HTML("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 1rem 1rem;">
        <h1 style="color: white; font-size: 2.5rem; margin: 0; font-weight: 700;">🔬 Diabetic Retinopathy Detection</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0.5rem 0 0 0;">AI-Powered Early Detection using ResNet-152 Deep Learning</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="📤 Upload Retinal Image", height=400)
            analyze_btn = gr.Button("🔍 Analyze Image", variant="primary", size="lg")
            
            gr.Markdown("""
            ### 📊 Severity Levels
            - **Level 0:** No DR - No signs detected
            - **Level 1:** Mild - Mild non-proliferative DR
            - **Level 2:** Moderate - Moderate non-proliferative DR
            - **Level 3:** Severe - Severe non-proliferative DR
            - **Level 4:** Proliferative DR - Urgent attention required
            """)
        
        with gr.Column(scale=1):
            result_html = gr.HTML(label="Results")
            result_image = gr.Image(label="Analyzed Image", height=300)
    
    # Event handler
    analyze_btn.click(
        fn=predict_image,
        inputs=[input_image],
        outputs=[result_html, result_image]
    )
    
    gr.HTML("""
    <div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid #e5e7eb;">
        <p style="margin: 0 0 0.5rem 0; font-size: 1.1rem; font-weight: 600;">Made by Tansu Gangopadhyay</p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
            <a href="https://github.com/tansugangopadhyay" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">🔗 GitHub</a>
            <a href="https://www.linkedin.com/in/tansugangopadhyay/" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">💼 LinkedIn</a>
            <a href="https://www.ijcseonline.org/pub_paper/7-IJCSE-09595.pdf" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">📄 Research Paper</a>
        </div>
        <p style="margin: 1rem 0 0 0; color: #6b7280; font-size: 0.875rem;">© 2025 Tansu Gangopadhyay. All rights reserved.</p>
    </div>
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
