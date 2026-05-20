"""Configuration management for Dental Caries Detection System."""
import os
from typing import Dict, Tuple


class Config:
    """Application configuration."""
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Model Configuration
    MODEL_PATHS = {
        'detection': 'models/detection/model.pth',
        'classification': 'models/classification/model.pth',
        'recommendation': 'models/recommendation/model.pth'
    }
    
    # Inference Configuration
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    SEVERITY_MAP = ['normal', 'superficial', 'medium', 'deep']
    
    # Image Processing Configuration
    MAX_IMAGE_SIZE_MB = 10  # Maximum image size in MB
    MAX_IMAGE_DIMENSIONS = (4096, 4096)  # Maximum image dimensions
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
    
    # Image Preprocessing
    DETECTION_INPUT_SIZE = (800, 800)
    CLASSIFICATION_INPUT_SIZE = (224, 224)
    NORMALIZATION_MEAN = [0.485, 0.456, 0.406]
    NORMALIZATION_STD = [0.229, 0.224, 0.225]
    
    # Inference Parameters
    DETECTION_CONFIDENCE_THRESHOLD = float(os.getenv('DETECTION_CONFIDENCE_THRESHOLD', 0.5))
    CLASSIFICATION_BATCH_SIZE = 1
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # Device Configuration
    USE_GPU = os.getenv('USE_GPU', 'True').lower() == 'true'
    
    @classmethod
    def get_image_size(cls) -> Tuple[int, int]:
        """Get detection image size."""
        return cls.DETECTION_INPUT_SIZE
    
    @classmethod
    def get_severity_label(cls, index: int) -> str:
        """Get severity label from index."""
        if 0 <= index < len(cls.SEVERITY_MAP):
            return cls.SEVERITY_MAP[index]
        raise ValueError(f"Invalid severity index: {index}")
    
    @classmethod
    def validate_extension(cls, filename: str) -> bool:
        """Validate file extension."""
        _, ext = os.path.splitext(filename.lower())
        return ext in cls.ALLOWED_EXTENSIONS
