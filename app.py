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

st.set_page_config(
    page_title="Crop Disease Detection",
    layout="centered"
)

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style='text-align: center;'>🌱 Crop Disease Detection System</h1>
    <p style='text-align: center; color: gray;'>
    AI-based severity analysis and treatment recommendation for farmers
    </p>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "📸 Upload crop leaf image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Leaf Image", use_container_width=True)

    processed_img = preprocess_image(uploaded_file)

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

    # ---------- AI PREDICTION CARD ----------
    with st.container():
        st.subheader("🧠 AI Prediction")
        st.write(f"**Detected Disease:** {disease_label}")
        st.write(f"**Model Confidence:** {confidence:.2f}")

    # ---------- SEVERITY CARD ----------
    with st.container():
        st.subheader("🌡️ Disease Severity")
        st.progress(min(max(int(infected_pct), 0), 100))
        st.write(f"**Severity Level:** {severity}")
        st.write(f"**Affected Area:** {infected_pct:.1f}%")

    # ---------- URGENCY CARD ----------
    with st.container():
        st.subheader("🚦 Urgency Status")
        st.info(urgency)

    # ---------- ACTION CARD ----------
    with st.container():
        st.subheader("🌿 Recommended Action")
        st.write(f"**Organic Method:** {actions['Organic']}")
        st.write(f"**Chemical Method:** {actions['Chemical']}")
        st.write(f"**Advice:** {actions['Advice']}")

    st.success("✅ Analysis complete. This system is optimized for real field conditions.")
