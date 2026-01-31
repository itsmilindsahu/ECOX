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

# ---------------- THEME ----------------
st.markdown(
    """
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #1b5e20; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- AUTO REGION FROM LANGUAGE ----------------
LANGUAGE_REGION = {
    "English": "Other / Not sure",
    "Hindi": "Uttar Pradesh",
    "Telugu": "Andhra Pradesh / Telangana"
}

# ---------------- REGION → CROPS ----------------
REGION_CROPS = {
    "Andhra Pradesh / Telangana": ["Rice", "Cotton", "Chilli", "Maize"],
    "Tamil Nadu": ["Rice", "Sugarcane", "Banana"],
    "Karnataka": ["Maize", "Ragi", "Coffee"],
    "Maharashtra": ["Cotton", "Soybean", "Sugarcane"],
    "Punjab / Haryana": ["Wheat", "Rice", "Mustard"],
    "Uttar Pradesh": ["Wheat", "Sugarcane", "Rice"],
    "Other / Not sure": ["Rice", "Wheat", "Maize", "Tomato", "Potato"]
}

# ---------------- REGION → COMMON DISEASES ----------------
REGION_DISEASES = {
    "Andhra Pradesh / Telangana": ["Leaf Blight", "Bacterial Spot", "Wilt"],
    "Tamil Nadu": ["Leaf Spot", "Powdery Mildew"],
    "Karnataka": ["Rust Disease", "Leaf Curl"],
    "Maharashtra": ["Boll Rot", "Wilt"],
    "Punjab / Haryana": ["Rust", "Blight"],
    "Uttar Pradesh": ["Smut", "Red Rot"],
    "Other / Not sure": ["Leaf Spot", "Blight", "Wilt"]
}

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🌱 ecox</h1>
    <p style='text-align:center;color:gray;'>
    Simple AI guidance for farmers
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- LANGUAGE ----------------
language = st.selectbox("🌐 Language", ["English", "Hindi", "Telugu"])
auto_region = LANGUAGE_REGION[language]

# ---------------- REGION ----------------
st.markdown("### 📍 Select Region")
region = st.selectbox("", list(REGION_CROPS.keys()), index=list(REGION_CROPS.keys()).index(auto_region))

# ---------------- DISTRICT ----------------
st.markdown("### 📍 Select District (Optional)")
district = st.text_input("Enter your district name (optional)")

# ---------------- COMMON DISEASE INFO ----------------
st.info(
    f"📊 **Common diseases in this region:** "
    f"{', '.join(REGION_DISEASES[region])}"
)

# ---------------- CROP SELECTION ----------------
st.markdown("### 🌾 Select Crop")
crop = st.selectbox("", REGION_CROPS[region])

# ---------------- VOICE INPUT (DEMO) ----------------
with st.expander("🗣️ Voice Crop Selection (Experimental)"):
    st.info("🎤 Speak the crop name (demo feature)")
    spoken_crop = st.text_input("Voice input result (simulated)")
    if spoken_crop:
        st.success(f"Detected crop: {spoken_crop} (demo)")

# ---------------- IMAGE INPUT ----------------
st.markdown("### 📸 Take or Upload Leaf Photo")
camera_img = st.camera_input("Take Photo")
upload_img = st.file_uploader("Upload Photo", type=["jpg", "png", "jpeg"])
image_file = camera_img if camera_img else upload_img

# ---------------- PROCESS ----------------
if image_file:
    image = Image.open(image_file)
    st.image(image, use_container_width=True)

    processed_img = preprocess_image(image_file)
    quality_status, quality_message = check_image_quality(processed_img)

    st.divider()

    if quality_status == "poor":
        st.warning("⚠️ Image quality issue")
        st.info(quality_message)

    else:
        raw_label, confidence = predict_disease(processed_img)
        disease_label = map_to_crop_disease(raw_label)

        infected_pct = infected_area_percentage(processed_img)
        severity = severity_level(infected_pct)
        urgency = urgency_message(severity)
        actions = action_recommendation(severity)

        st.markdown("## 🌱 Result")

        st.write(f"**Region:** {region}")
        if district:
            st.write(f"**District:** {district}")
        st.write(f"**Crop:** {crop}")
        st.write(f"**Disease:** {disease_label}")

        st.subheader("🌡️ Severity")
        st.progress(min(max(int(infected_pct), 0), 100))
        st.write(f"{severity} ({infected_pct:.1f}%)")

        st.subheader("🚦 Urgency")
        st.info(urgency)

        st.subheader("🌿 What to do")
        st.write(f"Organic: {actions['Organic']}")
        st.write(f"Chemical: {actions['Chemical']}")
        st.write(f"Advice: {actions['Advice']}")

        st.success("✅ Analysis complete")

st.divider()

st.markdown(
    """
    <p style='text-align:center;color:gray;font-size:12px;'>
    ecox • Designed for low-end smartphones • Demo version
    </p>
    """,
    unsafe_allow_html=True
)
