# 🦷 Dental Caries Detection & Recommendation System

A comprehensive AI-powered system for detecting dental caries, classifying severity levels, and providing personalized treatment recommendations using deep learning models.

## 📋 Overview

Dental caries (tooth decay) is one of the most prevalent oral health issues affecting millions worldwide. Early detection and intervention are crucial to prevent severe complications and costly treatments. This project leverages cutting-edge deep learning techniques to automate cavity detection from dental X-rays and provide evidence-based treatment recommendations.

### Key Capabilities
- **🔍 Precise Detection**: Identify and localize cavities using Mask R-CNN
- **📊 Severity Classification**: Classify caries into 4 severity levels using ResNet-50
- **💡 Smart Recommendations**: Generate personalized treatment advice using BERT

---

## 🏗️ System Architecture

### Multi-Stage Pipeline

```
Input X-ray Image
    ↓
Detection (Mask R-CNN) → Identify cavity regions
    ↓
Classification (ResNet-50) → Determine severity level
    ↓
Recommendation (BERT) → Generate treatment advice
    ↓
Output: Report with visualizations & recommendations
```

### Components

#### 1. **Detection Module** (Mask R-CNN)
- Backbone: ResNet-50-FPN
- Instance segmentation of cavity regions
- Bounding box and mask predictions
- Precision spatial localization with ROI Align

#### 2. **Classification Module** (ResNet-50)
- Transfer learning from ImageNet
- 4-level severity classification:
  - **Normal**: No visible caries
  - **Superficial**: Surface-level decay
  - **Medium**: Deeper penetration
  - **Deep**: Severe decay extending to pulp
- Class-weighted loss for imbalanced data handling
- Confidence scoring for predictions

#### 3. **Recommendation Module** (BERT)
- Context-aware recommendation generation
- Five recommendation categories:
  - Routine Care
  - Preventive Measures
  - Immediate Treatment
  - Dietary Modifications
  - Oral Hygiene Education
- Severity-based prioritization

---

## 📁 Project Structure

```
dental_caries_project/
├── src/
│   ├── detection/              # Mask R-CNN implementation
│   │   ├── model.py           # Model architecture
│   │   ├── train.py           # Training pipeline
│   │   ├── predict.py         # Inference script
│   │   └── utils.py           # Utility functions
│   ├── classification/         # ResNet-50 implementation
│   │   ├── model.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── utils.py
│   ├── recommendation/         # BERT implementation
│   │   ├── model.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── utils.py
│   └── web/                    # Flask web interface
│       ├── templates/          # HTML templates
│       └── static/             # CSS, JavaScript assets
├── models/                     # Trained model checkpoints
│   ├── detection/
│   ├── classification/
│   └── recommendation/
├── tests/                      # Unit test suite
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
└── README.md                  # Documentation
```

---

## 📊 Dataset

**Dental AI Dataset V4 (Augmented)**

### Distribution
| Class | Count | Percentage |
|-------|-------|------------|
| Normal | 15 | 2.2% |
| Superficial | 204 | 30.0% |
| Medium | 204 | 30.0% |
| Deep | 258 | 37.9% |
| **Total** | **681** | **100%** |

### Augmentation Techniques
- Random rotations (±15°)
- Horizontal/vertical flips
- Brightness/contrast adjustments
- Gaussian noise injection

### Training Configuration
| Parameter | Value |
|-----------|-------|
| Batch Size | 16 |
| Learning Rate | 0.0001 |
| Validation Split | 20% |
| Early Stopping | 10 epochs patience |
| Weight Decay | 1e-4 |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- CUDA 11.0+ (for GPU support, optional but recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/rajeshkadiyalaaa/Dental-Caries-Detection.git
cd Dental-Caries-Detection
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download and extract dataset**
```bash
unzip dental_ai_dataset_v4_augmented.zip
```

5. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## 💻 Usage

### Web Interface
1. Navigate to the web application in your browser
2. Upload a dental X-ray image (PNG or JPEG)
3. View real-time analysis with:
   - Detected cavity regions (visualization with bounding boxes)
   - Severity classification and confidence score
   - Personalized treatment recommendations

### Features
- ✅ Drag-and-drop image upload
- ✅ Real-time image preview
- ✅ Interactive result visualization
- ✅ Mobile-responsive design
- ✅ Exportable analysis reports

---

## 📈 Performance Metrics

| Metric | Status | Value |
|--------|--------|-------|
| **Detection AP@0.5** | To be evaluated | - |
| **Classification Accuracy** | To be evaluated | - |
| **Classification F1-Score** | To be evaluated | - |
| **Recommendation Relevance** | To be evaluated | - |

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| Detection | PyTorch + Mask R-CNN |
| Classification | PyTorch + ResNet-50 |
| NLP/Recommendations | Hugging Face + BERT |
| Web Framework | Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Data Processing | Pandas, NumPy, OpenCV |

---

## 🔮 Future Enhancements

### Model Improvements
- [ ] Implement k-fold cross-validation
- [ ] Experiment with EfficientNet and Vision Transformers
- [ ] Add ensemble techniques for increased robustness
- [ ] Develop real-time inference optimization

### Dataset Expansion
- [ ] Collect more diverse normal cases
- [ ] Include varied X-ray types and angles
- [ ] Add multi-modal imaging data

### Feature Additions
- [ ] Treatment progress tracking
- [ ] Multi-image batch analysis
- [ ] PDF report generation
- [ ] Dentist feedback integration
- [ ] Mobile application
- [ ] Patient history management

---

## 📝 License

[License information to be added]

---

## 📚 Citation

If you use this project in your research or work, please cite:

```bibtex
[Citation information to be added]
```

---

## 📧 Contact & Support

For questions, suggestions, or collaboration opportunities:

- **GitHub Issues**: [Open an issue](https://github.com/rajeshkadiyalaaa/Dental-Caries-Detection/issues)
- **Contact**: [Your contact information to be added]

---

## ⭐ Acknowledgments

- Dental AI Dataset V4 providers
- PyTorch and Hugging Face communities
- Contributors and collaborators

---

**Built with ❤️ for better oral health outcomes**
