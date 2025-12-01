# Quick Git Upload Script for Hugging Face

# Step 1: Clone your Space
cd "C:\Users\tansu\Desktop"
git clone https://huggingface.co/spaces/Tansuuuu/Diabetic-Retinopathy-Detection
cd Diabetic-Retinopathy-Detection

# Step 2: Copy your files
# Copy app_hf.py as app.py
Copy-Item "C:\Users\tansu\Desktop\Diabetic-Retinopathy-Detection-main\Diabetic-Retinopathy-Detection-main\app_hf.py" -Destination "app.py"

# Copy requirements.txt
Copy-Item "C:\Users\tansu\Desktop\Diabetic-Retinopathy-Detection-main\Diabetic-Retinopathy-Detection-main\requirements.txt" -Destination "requirements.txt"

# Create folder and copy model
New-Item -ItemType Directory -Path "Retinal_blindness_detection_Pytorch-master" -Force
Copy-Item "C:\Users\tansu\Desktop\Diabetic-Retinopathy-Detection-main\Diabetic-Retinopathy-Detection-main\Retinal_blindness_detection_Pytorch-master\classifier.pt" -Destination "Retinal_blindness_detection_Pytorch-master\classifier.pt"

# Step 3: Install Git LFS for large files
git lfs install
git lfs track "*.pt"

# Step 4: Commit and push
git add .
git commit -m "Add diabetic retinopathy detection app"
git push

# When prompted for password, use your Hugging Face access token
# Generate one at: https://huggingface.co/settings/tokens
