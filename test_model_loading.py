"""
Debug script to test model loading
"""
import torch
from torch import nn
from torchvision import models

print("=" * 60)
print("MODEL LOADING DEBUG")
print("=" * 60)

# Model path
MODEL_PATH = 'Retinal_blindness_detection_Pytorch-master/classifier.pt'

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

# Create model architecture
print("\n1. Creating model architecture...")
model = models.resnet152(pretrained=False)
num_ftrs = model.fc.in_features
out_ftrs = 5
model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 512),
    nn.ReLU(),
    nn.Linear(512, out_ftrs),
    nn.LogSoftmax(dim=1)
)
print("✓ Model architecture created")

# Load checkpoint
print(f"\n2. Loading checkpoint from: {MODEL_PATH}")
try:
    checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
    print("✓ Checkpoint loaded")
    print(f"   Checkpoint keys: {list(checkpoint.keys())}")
except Exception as e:
    print(f"✗ Error loading checkpoint: {e}")
    exit(1)

# Load model state
print("\n3. Loading model state...")
try:
    model.load_state_dict(checkpoint['model_state_dict'])
    print("✓ Model state loaded")
except Exception as e:
    print(f"✗ Error loading model state: {e}")
    print("\nTrying to inspect checkpoint structure...")
    if 'model_state_dict' in checkpoint:
        print(f"   model_state_dict keys (first 5): {list(checkpoint['model_state_dict'].keys())[:5]}")
    exit(1)

# Move to device and set to eval mode
print("\n4. Setting up model...")
model.to(device)
model.eval()
print("✓ Model ready for inference")

print("\n" + "=" * 60)
print("SUCCESS! Model loaded correctly!")
print("=" * 60)
print("\nThe model is working. Your Flask app should work too.")
print("Make sure to restart the Flask server after placing the model file.")
