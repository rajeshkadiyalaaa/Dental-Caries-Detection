"""Flask application for Dental Caries Detection System."""
from flask import Flask, request, jsonify, render_template
import torch
import torchvision.transforms as transforms
import warnings
from typing import Dict, Tuple, Any

from config import Config
from logger_config import setup_logger
from src.models_manager import ModelManager
from src.utils import validate_image

# Filter out deprecation warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Setup logging
logger = setup_logger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_IMAGE_SIZE_MB * 1024 * 1024

# Initialize model manager
model_manager = ModelManager()


def analyze_image(image_file) -> Dict[str, Any]:
    """Analyze a dental X-ray image.
    
    Args:
        image_file: File object from request
        
    Returns:
        dict: Analysis results containing detections, severity, confidence, and recommendations
        
    Raises:
        ValueError: If image validation fails
        RuntimeError: If model inference fails
    """
    try:
        logger.info("Starting image analysis...")
        
        # Read and validate image
        image_bytes = image_file.read()
        image = validate_image(image_bytes)
        logger.debug(f"Image loaded successfully. Size: {image.size}")
        
        # Create transforms for detection
        detection_transform = transforms.Compose([
            transforms.Resize(Config.DETECTION_INPUT_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=Config.NORMALIZATION_MEAN,
                std=Config.NORMALIZATION_STD
            )
        ])
        
        # Create transforms for classification
        classification_transform = transforms.Compose([
            transforms.Resize(Config.CLASSIFICATION_INPUT_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=Config.NORMALIZATION_MEAN,
                std=Config.NORMALIZATION_STD
            )
        ])
        
        # Apply transforms
        detection_tensor = detection_transform(image)
        classification_tensor = classification_transform(image)
        logger.debug(f"Detection tensor shape: {detection_tensor.shape}")
        logger.debug(f"Classification tensor shape: {classification_tensor.shape}")
        
        # Move to device
        detection_tensor = detection_tensor.to(model_manager.device)
        classification_tensor = classification_tensor.to(model_manager.device)
        
        # Get detection results
        with torch.no_grad():
            detections = model_manager.detector([detection_tensor])
            boxes = detections[0]['boxes'].cpu().numpy()
            scores = detections[0]['scores'].cpu().numpy()
            
            # Filter by confidence
            high_conf_indices = scores > Config.DETECTION_CONFIDENCE_THRESHOLD
            filtered_boxes = boxes[high_conf_indices].tolist()
            filtered_scores = scores[high_conf_indices].tolist()
            
            logger.info(
                f"Detection complete: Found {len(filtered_boxes)} regions "
                f"with confidence > {Config.DETECTION_CONFIDENCE_THRESHOLD}"
            )
            
            # Get classification
            class_pred, class_prob = model_manager.classifier.predict(
                classification_tensor.unsqueeze(0)
            )
            
            severity_index = class_pred.item()
            severity = Config.get_severity_label(severity_index)
            confidence = float(class_prob[0][severity_index].item())
            
            logger.info(f"Classification complete: severity={severity}, confidence={confidence:.4f}")
            
            # Get recommendations
            recommendations = model_manager.recommender.get_recommendations(
                'caries',
                severity,
                confidence
            )
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            
            return {
                'detections': {
                    'boxes': filtered_boxes,
                    'scores': filtered_scores,
                    'num_caries': len(filtered_boxes)
                },
                'severity': severity,
                'confidence': confidence,
                'recommendations': recommendations
            }
            
    except ValueError as e:
        logger.error(f"Image validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}", exc_info=True)
        raise RuntimeError(f"Image analysis failed: {str(e)}")


@app.route('/')
def home():
    """Render the home page.
    
    Returns:
        Rendered HTML template
    """
    logger.debug("Home page requested")
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze() -> Tuple[Dict[str, Any], int]:
    """Analyze uploaded image.
    
    Returns:
        JSON response with analysis results or error message
    """
    logger.info("Analyze endpoint called")
    
    try:
        # Check if file exists
        if 'file' not in request.files:
            logger.warning("No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            logger.warning("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not Config.validate_extension(file.filename):
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({
                'error': f'Invalid file type. Please upload one of: {Config.ALLOWED_EXTENSIONS}'
            }), 400
        
        # Analyze image
        results = analyze_image(file)
        logger.info("Image analysis completed successfully")
        return jsonify(results), 200
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except RuntimeError as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint.
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        'status': 'healthy',
        'models_loaded': model_manager.is_loaded(),
        'device': str(model_manager.device)
    }), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error.
    
    Args:
        error: The error object
        
    Returns:
        JSON error response
    """
    logger.warning("Request entity too large")
    return jsonify({
        'error': f'File too large. Maximum size is {Config.MAX_IMAGE_SIZE_MB}MB'
    }), 413


if __name__ == '__main__':
    logger.info("Starting Dental Caries Detection application...")
    
    if model_manager.initialize():
        logger.info("Models initialized successfully")
        logger.info(
            f"Starting Flask app on {Config.HOST}:{Config.PORT} "
            f"(debug={Config.DEBUG})"
        )
        app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    else:
        logger.error("Failed to initialize models. Exiting...")
        exit(1)
