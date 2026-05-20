"""Model manager for loading and managing AI models."""
import threading
from typing import Optional, Tuple
import torch
from config import Config
from logger_config import setup_logger
from src.utils import load_checkpoint, ensure_model_directory, get_device

logger = setup_logger(__name__)


class ModelManager:
    """Thread-safe model manager for loading and managing models."""
    
    def __init__(self):
        """Initialize model manager."""
        self.detector: Optional[object] = None
        self.classifier: Optional[object] = None
        self.recommender: Optional[object] = None
        self.device: Optional[torch.device] = None
        self._lock = threading.Lock()
        self._loaded = False
    
    def initialize(self) -> bool:
        """Initialize and load all models.
        
        Returns:
            True if all models loaded successfully, False otherwise
        """
        with self._lock:
            if self._loaded:
                logger.debug("Models already loaded")
                return True
            
            logger.info("Initializing model manager...")
            
            try:
                # Get device
                self.device = get_device()
                
                # Ensure model directories exist
                ensure_model_directory()
                
                # Load models
                if not self._load_detection_model():
                    logger.error("Failed to load detection model")
                    return False
                
                if not self._load_classification_model():
                    logger.error("Failed to load classification model")
                    return False
                
                if not self._load_recommendation_model():
                    logger.error("Failed to load recommendation model")
                    return False
                
                self._loaded = True
                logger.info("All models initialized successfully")
                return True
                
            except Exception as e:
                logger.error(f"Error initializing models: {str(e)}", exc_info=True)
                return False
    
    def _load_detection_model(self) -> bool:
        """Load detection model.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from src.detection.model import DentalCariesDetector
            
            logger.info("Loading detection model...")
            self.detector = DentalCariesDetector()
            
            if load_checkpoint(
                self.detector,
                Config.MODEL_PATHS['detection'],
                self.device
            ):
                self.detector = self.detector.to(self.device)
                self.detector.eval()
                logger.info("Detection model loaded successfully")
                return True
            else:
                logger.warning("Detection model loaded without pretrained weights")
                self.detector = self.detector.to(self.device)
                self.detector.eval()
                return True
                
        except Exception as e:
            logger.error(f"Error loading detection model: {str(e)}", exc_info=True)
            return False
    
    def _load_classification_model(self) -> bool:
        """Load classification model.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from src.classification.model import DentalCariesClassifier
            
            logger.info("Loading classification model...")
            self.classifier = DentalCariesClassifier()
            
            if load_checkpoint(
                self.classifier,
                Config.MODEL_PATHS['classification'],
                self.device
            ):
                self.classifier = self.classifier.to(self.device)
                self.classifier.eval()
                logger.info("Classification model loaded successfully")
                return True
            else:
                logger.warning("Classification model loaded without pretrained weights")
                self.classifier = self.classifier.to(self.device)
                self.classifier.eval()
                return True
                
        except Exception as e:
            logger.error(f"Error loading classification model: {str(e)}", exc_info=True)
            return False
    
    def _load_recommendation_model(self) -> bool:
        """Load recommendation model.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            from src.recommendation.model import DentalRecommendationSystem
            
            logger.info("Loading recommendation model...")
            self.recommender = DentalRecommendationSystem()
            
            if load_checkpoint(
                self.recommender,
                Config.MODEL_PATHS['recommendation'],
                self.device
            ):
                self.recommender = self.recommender.to(self.device)
                self.recommender.eval()
                logger.info("Recommendation model loaded successfully")
                return True
            else:
                logger.warning("Recommendation model loaded without pretrained weights")
                self.recommender = self.recommender.to(self.device)
                self.recommender.eval()
                return True
                
        except Exception as e:
            logger.error(f"Error loading recommendation model: {str(e)}", exc_info=True)
            return False
    
    def is_loaded(self) -> bool:
        """Check if all models are loaded.
        
        Returns:
            True if all models are loaded, False otherwise
        """
        return self._loaded and all([
            self.detector is not None,
            self.classifier is not None,
            self.recommender is not None
        ])
