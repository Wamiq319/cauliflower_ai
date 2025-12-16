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

    with torch.no_grad():
        outputs = _model(tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        pred_idx = torch.argmax(probs, dim=1).item()
        pred_class = CLASSES[pred_idx]
        confidence = probs[0][pred_idx].item()

    return pred_class, confidence, probs

def test_all_images_in_directory():
    """Tests all images in the Image_Testing directory and writes their predictions to a file."""
    image_testing_dir = os.path.join(BASE_DIR, "Test_Images")
    results_file_path = os.path.join(BASE_DIR, "AI_TEST_RESULTS.TXT")

    if not os.path.exists(image_testing_dir):
        print(f"Error: Image testing directory not found at {image_testing_dir}")
        return

    print(f"Testing images in: {image_testing_dir}")
    with open(results_file_path, "w") as results_file:
        results_file.write("AI Model Test Results\n")
        results_file.write("=======================\n\n")

        for filename in os.listdir(image_testing_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                image_path = os.path.join(image_testing_dir, filename)
                try:
                    pred_class, confidence, probs = predict_one_image(image_path)
                    results_file.write(f"Image: {filename}\n")
                    results_file.write(f"  Predicted Class: {pred_class}\n")
                    results_file.write(f"  Confidence: {confidence:.4f}\n")
                    results_file.write("  Disease Probabilities:\n")
                    for i, class_name in enumerate(CLASSES):
                        results_file.write(f"    - {class_name}: {probs[0][i].item():.4f}\n")
                    results_file.write("\n")
                except Exception as e:
                    results_file.write(f"Error processing {filename}: {e}\n\n")
    print(f"Test results written to {results_file_path}")

if __name__ == "__main__":
    test_all_images_in_directory()

