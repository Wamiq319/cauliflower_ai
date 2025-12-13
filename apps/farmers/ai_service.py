# farmers/ai_service.py
import torch
import timm
from PIL import Image
from torchvision import transforms as T
import os

# Config
MODEL_NAME = "rexnet_150"
BASE_DIR = os.path.dirname(__file__)
CHECKPOINT_PATH = os.path.join(BASE_DIR, "cabbage_best_model.pth")

# Classes (same as training order)
CLASSES = [
    "Alternaria_Leaf_Spot",
    "club root",
    "Downy Mildew",
    "Cabbage aphid colony",
    "Ring spot",
    "Black Rot",
    "Bacterial spot rot",
    "No disease",
]

# Transform
mean, std, im_size = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225], 224
tfs = T.Compose([
    T.Resize((im_size, im_size)),
    T.ToTensor(),
    T.Normalize(mean=mean, std=std)
])

# Load model once (singleton)
device = "cuda" if torch.cuda.is_available() else "cpu"
_model = timm.create_model(MODEL_NAME, pretrained=False, num_classes=len(CLASSES)).to(device)
_model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=device))
_model.eval()

def predict_one_image(image_file):
    """Predict disease from Django UploadedFile"""
    image = Image.open(image_file).convert("RGB")
    tensor = tfs(image).unsqueeze(0).to(device)

    print(f"\n[AI Service] Starting prediction for image...")
    with torch.no_grad():
        outputs = _model(tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        
        # Log all class probabilities
        print("[AI Service] Class Probabilities:")
        for idx, class_name in enumerate(CLASSES):
            prob = probs[0][idx].item()
            print(f"  - {class_name}: {prob:.4f}")

        pred_idx = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred_idx].item()
        
        raw_pred_class = CLASSES[pred_idx]
        print(f"[AI Service] Top Prediction: '{raw_pred_class}' with confidence {confidence:.4f}")

        if confidence < 0.9:
            print(f"[AI Service] Confidence {confidence:.4f} is below threshold 0.9. Result: Unknown")
            pred_class = "Unknown"
        else:
            print(f"[AI Service] Confidence {confidence:.4f} is sufficient. Result: {raw_pred_class}")
            pred_class = raw_pred_class

    return pred_class, confidence
