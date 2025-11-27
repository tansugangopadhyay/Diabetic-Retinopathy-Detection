"""
Configuration file for Diabetic Retinopathy Detection System
Modify these settings as needed
"""

import os

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Model Settings
    MODEL_PATH = 'Retinal_blindness_detection_Pytorch-master/classifier.pt'
    MODEL_DEVICE = 'auto'  # 'auto', 'cuda', or 'cpu'
    
    # Image Processing Settings
    IMAGE_SIZE = (224, 224)
    NORMALIZE_MEAN = (0.485, 0.456, 0.406)
    NORMALIZE_STD = (0.229, 0.224, 0.225)
    
    # Classification Settings
    NUM_CLASSES = 5
    CLASS_NAMES = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']
    
    # CORS Settings
    CORS_ORIGINS = '*'  # Change to specific origins in production
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Add production-specific settings here
    # For example:
    # CORS_ORIGINS = ['https://yourdomain.com']


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
