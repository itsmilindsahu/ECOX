import cv2
import numpy as np
from PIL import Image

# ---------------- IMAGE PREPROCESSING ----------------
def preprocess_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")

    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # IMPORTANT: 224x224 for MobileNetV2
    img = cv2.resize(img, (224, 224))

    # Simulate low-end smartphone image
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.convertScaleAbs(img, alpha=0.85, beta=10)

    img = img / 255.0
    return img


# ---------------- SEVERITY ESTIMATION ----------------
def infected_area_percentage(img):
    img_uint8 = (img * 255).astype("uint8")
    gray = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

    infected_pixels = np.sum(thresh > 0)
    total_pixels = thresh.size

    return (infected_pixels / total_pixels) * 100


def severity_level(percentage):
    if percentage < 30:
        return "Mild"
    elif percentage < 60:
        return "Moderate"
    else:
        return "Severe"


def urgency_message(severity):
    if severity == "Severe":
        return "🚨 High urgency: Immediate action required"
    elif severity == "Moderate":
        return "⚠️ Medium urgency: Treat soon"
    else:
        return "✅ Low urgency: Monitor crop"


# ---------------- ACTION RECOMMENDATIONS ----------------
def action_recommendation(severity):
    if severity == "Mild":
        return {
            "Organic": "Neem oil spray or baking soda solution",
            "Chemical": "Not required",
            "Advice": "Monitor the crop for a few days"
        }
    elif severity == "Moderate":
        return {
            "Organic": "Neem oil + garlic extract spray",
            "Chemical": "Low-dose fungicide if needed",
            "Advice": "Treat within 2–3 days"
        }
    else:
        return {
            "Organic": "Organic methods not sufficient",
            "Chemical": "Recommended fungicide / pesticide",
            "Advice": "Immediate treatment and expert consultation"
        }
