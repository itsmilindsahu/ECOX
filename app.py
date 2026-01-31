import streamlit as st
from PIL import Image
from utils import (
    preprocess_image,
    check_image_quality,
    infected_area_percentage,
    severity_level,
    urgency_message,
    action_recommendation
)
from model import predict_disease, map_to_crop_disease

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ecox", layout="centered")

# ---------------- GREEN + WHITE THEME ----------------
st.markdown(
    """
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #1b5e20; }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 18px;
    }
    .stSelectbox label, .stFileUploader label {
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🌱 ecox</h1>
    <p style='text-align:center; color:#4f4f4f;'>
    Take a photo of your crop leaf and get instant guidance
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- STEP 1: CROP SELECTION ----------------
st.markdown("### 🌾 Step 1: Select Crop")

crop = st.selectbox(
    "",
    ["Rice", "Wheat", "Maize", "Tomato", "Potato", "Cotton", "Other / Not sure"]
)

# ---------------- STEP 2: IMAGE INPUT ----------------
st.markdown("### 📸 Step 2: Take or Upload Photo")

camera_image = st.camera_input("📷 Take Photo")
uploaded_image = st.file_uploader("📁 Or Upload Photo", type=["jpg", "png", "jpeg"])

image_file = camera_image if camera_image else uploaded_image

# ---------------- PROCESS IMAGE ----------------
if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Leaf Image", use_container_width=True)

    processed_img = preprocess_image(image_file)
    quality_status, quality_message = check_image_quality(processed_img)

    st.divider()
    st.markdown("## 🌱 Result")

    # ---------- IMAGE QUALITY ----------
    if quality_status == "poor":
        st.warning("⚠️ Photo quality is not clear")
        st.info(quality_message)

        st.markdown(
            """
            **Tips to get better result:**
            - Take photo in sunlight ☀️  
            - Hold phone steady 📱  
            - Capture only one leaf 🍃
            """
        )

    else:
        # ---------- AI PREDICTION ----------
        raw_label, confidence = predict_disease(processed_img)
        disease_label = map_to_crop_disease(raw_label)

        infected_pct = infected_area_percentage(processed_img)
        severity = severity_level(infected_pct)
        urgency = urgency_message(severity)
        actions = action_recommendation(severity)

        st.success("✅ Photo is clear")

        st.markdown(f"**🌾 Crop:** {crop}")
        st.markdown(f"**🦠 Disease:** {disease_label}")

        # ---------- SEVERITY ----------
        st.markdown("### 🌡️ Disease Severity")
        st.progress(min(max(int(infected_pct), 0), 100))
        st.markdown(f"**Severity:** {severity}")
        st.markdown(f"**Affected Area:** {infected_pct:.1f}%")

        # ---------- URGENCY ----------
        st.markdown("### 🚦 Urgency")
        st.info(urgency)

        # ---------- ACTION ----------
        st.markdown("### 🌿 What should you do?")
        st.markdown(f"**Organic:** {actions['Organic']}")
        st.markdown(f"**Chemical:** {actions['Chemical']}")
        st.markdown(f"**Advice:** {actions['Advice']}")

st.divider()

# ---------------- FOOTER ----------------
st.markdown(
    """
    <p style='text-align:center; color:gray; font-size:13px;'>
    ecox • Simple AI for farmers  
    <br>
    Works on low-end smartphones
    </p>
    """,
    unsafe_allow_html=True
)
