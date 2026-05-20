"""Detection model implementation (Mask R-CNN)."""
import torch
import torch.nn as nn
from torchvision.models.detection import maskrcnn_resnet50_fpn


class DentalCariesDetector(nn.Module):
    """Mask R-CNN based detector for dental caries."""
    
    def __init__(self, num_classes: int = 2):
        """Initialize detector.
        
        Args:
            num_classes: Number of classes (background + caries)
        """
        super().__init__()
        # Load pretrained Mask R-CNN
        self.model = maskrcnn_resnet50_fpn(
            weights='DEFAULT',
            num_classes=num_classes
        )
    
    def forward(self, images):
        """Forward pass.
        
        Args:
            images: List of input images
            
        Returns:
            Detection results
        """
        return self.model(images)
    
    def load_state_dict(self, state_dict, strict=True):
        """Load state dict."""
        return self.model.load_state_dict(state_dict, strict=strict)
    
    def to(self, device):
        """Move model to device."""
        self.model = self.model.to(device)
        return self
    
    def eval(self):
        """Set to evaluation mode."""
        return self.model.eval()
    
    def train(self, mode=True):
        """Set to training mode."""
        return self.model.train(mode)
