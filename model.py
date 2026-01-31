import tensorflow as tf
import numpy as np

model = tf.keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=True
)

def predict_disease(img):
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img * 255)

    preds = model.predict(img)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)

    label = decoded[0][0][1]
    confidence = decoded[0][0][2]

    return label, confidence


# Demo-friendly disease mapping
def map_to_crop_disease(raw_label):
    mapping = {
        "Windsor_tie": "Leaf Blight (Demo)",
        "bow_tie": "Leaf Spot Disease (Demo)",
        "green_snake": "Fungal Infection (Demo)",
        "necklace": "Nutrient Deficiency (Demo)"
    }

    return mapping.get(raw_label, "Unknown Crop Disease")
