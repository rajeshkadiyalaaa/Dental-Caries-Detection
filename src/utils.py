"""Utility functions for the Dental Caries Detection System."""
import io
import os
from typing import Tuple, Optional
from PIL import Image
import torch
from config import Config
from logger_config import setup_logger

logger = setup_logger(__name__)


def validate_image(image_bytes: bytes) -> Image.Image:
    """Validate and load image from bytes.
    
    Args:
        image_bytes: Raw image data in bytes
        
    Returns:
        PIL Image object in RGB format
        
    Raises:
        ValueError: If image is invalid, too large, or corrupted
    """
    if not image_bytes:
        raise ValueError("Empty image data provided")
    
    # Check file size
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > Config.MAX_IMAGE_SIZE_MB:
        raise ValueError(
            f"Image size {size_mb:.2f}MB exceeds maximum of {Config.MAX_IMAGE_SIZE_MB}MB"
        )
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        raise ValueError(f"Failed to load image: {str(e)}")
    
    # Check image dimensions
    if image.size[0] > Config.MAX_IMAGE_DIMENSIONS[0] or \
       image.size[1] > Config.MAX_IMAGE_DIMENSIONS[1]:
        raise ValueError(
            f"Image dimensions {image.size} exceed maximum {Config.MAX_IMAGE_DIMENSIONS}"
        )
    
    # Convert to RGB
    try:
        return image.convert('RGB')
    except Exception as e:
        raise ValueError(f"Failed to convert image to RGB: {str(e)}")


def get_device() -> torch.device:
    """Get the appropriate device (GPU or CPU).
    
    Returns:
        torch.device object
    """
    if Config.USE_GPU and torch.cuda.is_available():
        device = torch.device('cuda')
        logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device('cpu')
        logger.info("Using CPU")
    
    return device


def ensure_model_directory() -> None:
    """Ensure all model directories exist."""
    for model_type, path in Config.MODEL_PATHS.items():
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def load_checkpoint(
    model: torch.nn.Module,
    checkpoint_path: str,
    device: torch.device
) -> bool:
    """Load a model checkpoint with error handling.
    
    Args:
        model: The model to load checkpoint into
        checkpoint_path: Path to the checkpoint file
        device: Device to load the checkpoint on
        
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(checkpoint_path):
        logger.warning(f"Checkpoint not found: {checkpoint_path}")
        return False
    
    try:
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
        
        # Handle both full model and state_dict checkpoints
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            else:
                model.load_state_dict(checkpoint)
        else:
            model.load_state_dict(checkpoint)
        
        logger.info(f"Successfully loaded checkpoint: {checkpoint_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to load checkpoint {checkpoint_path}: {str(e)}", exc_info=True)
        return False
