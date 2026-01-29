import streamlit as st
from PIL import Image
from utils import (
    preprocess_image,
    infected_area_percentage,
    severity_level,
    urgency_message,
    action_recommendation
)
from model import predict_disease, map_to_crop_disease

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ecox",
    layout="centered"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align: center;'>🌱 ecox</h1>
    <p style='text-align: center; color: gray;'>
    AI-powered crop disease severity & treatment assistant
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------- IMAGE INPUT ----------------
st.markdown("### 📸 Capture or Upload Crop Leaf Image")

input_method = st.radio(
    "Choose image input method",
    ["📷 Take Photo", "📁 Upload Image"],
    horizontal=True
)

image_file = None

if input_method == "📷 Take Photo":
    image_file = st.camera_input("Take a clear photo of the crop leaf")

else:
    image_file = st.file_uploader(
        "Upload crop leaf image",
        type=["jpg", "png", "jpeg"]
    )

# ---------------- PROCESS IMAGE ----------------
if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Leaf Image", use_container_width=True)

    # Preprocess
    processed_img = preprocess_image(image_file)

    # AI prediction
    raw_label, confidence = predict_disease(processed_img)
    disease_label = map_to_crop_disease(raw_label)

    # Severity analysis
    infected_pct = infected_area_percentage(processed_img)
    severity = severity_level(infected_pct)
    urgency = urgency_message(severity)
    actions = action_recommendation(severity)

    st.divider()
    st.markdown("## 📊 Analysis Results")

    # ---------------- AI PREDICTION ----------------
    st.subheader("🧠 AI Prediction")
    st.write(f"**Detected Disease:** {disease_label}")
    st.write(f"**Model Confidence:** {confidence:.2f}")

    # ---------------- SEVERITY ----------------
    st.subheader("🌡️ Disease Severity")
    st.progress(min(max(int(infected_pct), 0), 100))
    st.write(f"**Severity Level:** {severity}")
    st.write(f"**Affected Area:** {infected_pct:.1f}%")

    # ---------------- URGENCY ----------------
    st.subheader("🚦 Urgency Status")
    st.info(urgency)

    # ---------------- ACTION ----------------
    st.subheader("🌿 Recommended Action")
    st.write(f"**Organic Method:** {actions['Organic']}")
    st.write(f"**Chemical Method:** {actions['Chemical']}")
    st.write(f"**Advice:** {actions['Advice']}")

    st.success("✅ Analysis complete. Designed for real field conditions.")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align: center; font-size: 12px; color: gray;'>
    ecox • AI4Life Hackathon • IISER Tirupati  
    <br>
    Demo system – model can be fine-tuned with crop-specific datasets
    </p>
    """,
    unsafe_allow_html=True
)
