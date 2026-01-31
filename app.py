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

st.set_page_config(page_title="ecox", layout="centered")

st.markdown(
    """
    <h1 style='text-align:center;'>🌱 ecox</h1>
    <p style='text-align:center;color:gray;'>
    AI-powered crop disease severity & treatment assistant
    </p>
    """,
    unsafe_allow_html=True
)

# -------- Crop Selection --------
st.markdown("### 🌾 Select Crop")
crop = st.selectbox(
    "Choose crop type",
    ["Unknown", "Rice", "Wheat", "Maize", "Tomato", "Potato", "Cotton"]
)

# -------- Image Input --------
st.markdown("### 📸 Capture or Upload Leaf Image")

method = st.radio(
    "Image input method",
    ["📷 Take Photo", "📁 Upload Image"],
    horizontal=True
)

image_file = None
if method == "📷 Take Photo":
    image_file = st.camera_input("Take a clear photo of the leaf")
else:
    image_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "png", "jpeg"]
    )

# -------- Processing --------
if image_file:
    image = Image.open(image_file)
    st.image(image, use_container_width=True)

    processed_img = preprocess_image(image_file)

    quality_status, quality_message = check_image_quality(processed_img)

    if quality_status == "poor":
        st.warning("⚠️ Image Quality Issue")
        st.info(quality_message)

        st.markdown(
            "- Take photo in sunlight ☀️\n"
            "- Hold phone steady 📱\n"
            "- Capture only the leaf 🍃"
        )

    else:
        raw_label, confidence = predict_disease(processed_img)
        disease_label = map_to_crop_disease(raw_label)

        infected_pct = infected_area_percentage(processed_img)
        severity = severity_level(infected_pct)
        urgency = urgency_message(severity)
        actions = action_recommendation(severity)

        st.divider()
        st.markdown("## 📊 Analysis Results")

        st.subheader("🧠 AI Prediction")
        st.write(f"**Detected Disease:** {disease_label}")
        st.write(f"**Crop:** {crop}")
        st.write(f"**Confidence:** {confidence:.2f}")

        if "Unknown" in disease_label:
            st.warning("⚠️ Disease not supported in demo model")
            st.info(
                "Image quality is good. The disease is not covered "
                "by the current demo model.\n\n"
                "Severity estimation is still reliable."
            )

            st.subheader("🌡️ Disease Severity")
            st.progress(min(max(int(infected_pct), 0), 100))
            st.write(f"**Severity Level:** {severity}")
            st.write(f"**Affected Area:** {infected_pct:.1f}%")

        else:
            st.subheader("🌡️ Disease Severity")
            st.progress(min(max(int(infected_pct), 0), 100))
            st.write(f"**Severity Level:** {severity}")
            st.write(f"**Affected Area:** {infected_pct:.1f}%")

            st.subheader("🚦 Urgency")
            st.info(urgency)

            st.subheader("🌿 Recommended Action")
            st.write(f"**Organic:** {actions['Organic']}")
            st.write(f"**Chemical:** {actions['Chemical']}")
            st.write(f"**Advice:** {actions['Advice']}")

        st.success("✅ Analysis complete. Designed for real field conditions.")
