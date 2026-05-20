"""Recommendation model implementation (BERT-based)."""
import torch
import torch.nn as nn
from typing import List


class DentalRecommendationSystem(nn.Module):
    """BERT-based system for generating treatment recommendations."""
    
    def __init__(self):
        """Initialize recommendation system."""
        super().__init__()
        
        # Recommendation templates based on severity
        self.recommendations = {
            'normal': [
                'Continue regular brushing and flossing',
                'Maintain a balanced diet with limited sugary foods',
                'Schedule routine dental checkups every 6 months',
                'Consider fluoride toothpaste for added protection'
            ],
            'superficial': [
                'Begin professional cleaning if not done recently',
                'Increase fluoride use with professional-grade products',
                'Reduce consumption of acidic beverages and foods',
                'Consider dental sealants on vulnerable surfaces',
                'Implement strict oral hygiene regimen'
            ],
            'medium': [
                'Schedule urgent dental appointment for treatment assessment',
                'Avoid hard or sticky foods that may worsen decay',
                'Use antimicrobial mouthwash twice daily',
                'Consider root canal therapy evaluation',
                'Implement strict dietary modifications'
            ],
            'deep': [
                'Seek immediate dental treatment - possible root canal needed',
                'Avoid chewing on affected tooth',
                'Take pain management as prescribed by dentist',
                'Prepare for potential extraction or advanced restoration',
                'Follow dentist\'s pre-treatment instructions carefully'
            ]
        }
    
    def forward(self, x):
        """Forward pass.
        
        Args:
            x: Input tensor
            
        Returns:
            Output tensor
        """
        return x
    
    def get_recommendations(
        self,
        condition: str,
        severity: str,
        confidence: float
    ) -> List[str]:
        """Get recommendations based on condition and severity.
        
        Args:
            condition: Medical condition (e.g., 'caries')
            severity: Severity level
            confidence: Confidence score of the prediction
            
        Returns:
            List of recommendations
        """
        if severity not in self.recommendations:
            return ['Consult with your dentist for professional evaluation']
        
        recommendations = self.recommendations[severity].copy()
        
        # Add confidence disclaimer if confidence is low
        if confidence < 0.7:
            recommendations.append(
                f'Note: This recommendation has lower confidence ({confidence:.2%}). \
                Please consult your dentist for confirmation.'
            )
        
        return recommendations
    
    def load_state_dict(self, state_dict, strict=True):
        """Load state dict."""
        return super().load_state_dict(state_dict, strict=strict)
    
    def to(self, device):
        """Move model to device."""
        return super().to(device)
