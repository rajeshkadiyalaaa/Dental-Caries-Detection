"""Classification model implementation (ResNet-50)."""
import torch
import torch.nn as nn
from torchvision.models import resnet50


class DentalCariesClassifier(nn.Module):
    """ResNet-50 based classifier for caries severity."""
    
    def __init__(self, num_classes: int = 4):
        """Initialize classifier.
        
        Args:
            num_classes: Number of severity classes
        """
        super().__init__()
        # Load pretrained ResNet-50
        self.model = resnet50(weights='DEFAULT')
        
        # Replace final layer for 4-class classification
        in_features = self.model.fc.in_features
        self.model.fc = nn.Linear(in_features, num_classes)
    
    def forward(self, x):
        """Forward pass.
        
        Args:
            x: Input image tensor
            
        Returns:
            Classification logits
        """
        return self.model(x)
    
    def predict(self, x):
        """Get predictions with confidence scores.
        
        Args:
            x: Input image tensor
            
        Returns:
            Tuple of (predicted class, class probabilities)
        """
        with torch.no_grad():
            logits = self.forward(x)
            probs = torch.softmax(logits, dim=1)
            pred_class = torch.argmax(logits, dim=1)
            return pred_class, probs
    
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
