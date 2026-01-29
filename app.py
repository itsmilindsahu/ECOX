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

# ---------------- LANGUAGE DICTIONARY ----------------
LANG = {
    "English": {
        "title": "🌱 ecox",
        "subtitle": "AI-powered crop disease severity & treatment assistant",
        "choose_lang": "Select Language",
        "input_title": "📸 Capture or Upload Crop Leaf Image",
        "take_photo": "📷 Take Photo",
        "upload_image": "📁 Upload Image",
        "camera_text": "Take a clear photo of the crop leaf",
        "upload_text": "Upload crop leaf image",
        "results": "📊 Analysis Results",
        "ai_pred": "🧠 AI Prediction",
        "detected": "Detected Disease",
        "confidence": "Model Confidence",
        "severity": "🌡️ Disease Severity",
        "severity_level": "Severity Level",
        "affected": "Affected Area",
        "urgency": "🚦 Urgency Status",
        "action": "🌿 Recommended Action",
        "organic": "Organic Method",
        "chemical": "Chemical Method",
        "advice": "Advice",
        "done": "✅ Analysis complete. Designed for real field conditions."
    },
    "Hindi": {
        "title": "🌱 ecox",
        "subtitle": "फसल रोग की गंभीरता और उपचार के लिए एआई आधारित प्रणाली",
        "choose_lang": "भाषा चुनें",
        "input_title": "📸 फसल पत्ती की तस्वीर लें या अपलोड करें",
        "take_photo": "📷 फोटो लें",
        "upload_image": "📁 फोटो अपलोड करें",
        "camera_text": "फसल पत्ती की स्पष्ट फोटो लें",
        "upload_text": "फसल पत्ती की फोटो अपलोड करें",
        "results": "📊 विश्लेषण परिणाम",
        "ai_pred": "🧠 एआई भविष्यवाणी",
        "detected": "पहचाना गया रोग",
        "confidence": "विश्वास स्तर",
        "severity": "🌡️ रोग की गंभीरता",
        "severity_level": "गंभीरता स्तर",
        "affected": "प्रभावित क्षेत्र",
        "urgency": "🚦 तात्कालिक स्थिति",
        "action": "🌿 अनुशंसित उपचार",
        "organic": "जैविक तरीका",
        "chemical": "रासायनिक तरीका",
        "advice": "सलाह",
        "done": "✅ विश्लेषण पूर्ण हुआ। वास्तविक खेत परिस्थितियों के लिए डिज़ाइन किया गया।"
    },
    "Telugu": {
        "title": "🌱 ecox",
        "subtitle": "పంట వ్యాధి తీవ్రత మరియు చికిత్స కోసం AI ఆధారిత వ్యవస్థ",
        "choose_lang": "భాషను ఎంచుకోండి",
        "input_title": "📸 పంట ఆకు ఫోటో తీయండి లేదా అప్లోడ్ చేయండి",
        "take_photo": "📷 ఫోటో తీయండి",
        "upload_image": "📁 ఫోటో అప్లోడ్ చేయండి",
        "camera_text": "పంట ఆకు యొక్క స్పష్టమైన ఫోటో తీయండి",
        "upload_text": "పంట ఆకు ఫోటోను అప్లోడ్ చేయండి",
        "results": "📊 విశ్లేషణ ఫలితాలు",
        "ai_pred": "🧠 AI అంచనా",
        "detected": "గుర్తించిన వ్యాధి",
        "confidence": "నమ్మక స్థాయి",
        "severity": "🌡️ వ్యాధి తీవ్రత",
        "severity_level": "తీవ్రత స్థాయి",
        "affected": "ప్రభావిత ప్రాంతం",
        "urgency": "🚦 అత్యవసర స్థితి",
        "action": "🌿 సూచించిన చికిత్స",
        "organic": "జైవ పద్ధతి",
        "chemical": "రసాయన పద్ధతి",
        "advice": "సలహా",
        "done": "✅ విశ్లేషణ పూర్తైంది. నిజమైన పొలాల పరిస్థితుల కోసం రూపొందించబడింది."
    }
}

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ecox", layout="centered")

# ---------------- LANGUAGE SELECT ----------------
language = st.selectbox("🌐 Select Language / भाषा / భాష", ["English", "Hindi", "Telugu"])
T = LANG[language]

# ---------------- HEADER ----------------
st.markdown(
    f"""
    <h1 style='text-align: center;'>{T['title']}</h1>
    <p style='text-align: center; color: gray;'>{T['subtitle']}</p>
    """,
    unsafe_allow_html=True
)

# ---------------- IMAGE INPUT ----------------
st.markdown(f"### {T['input_title']}")

input_method = st.radio(
    T["choose_lang"],
    [T["take_photo"], T["upload_image"]],
    horizontal=True
)

image_file = None

if input_method == T["take_photo"]:
    image_file = st.camera_input(T["camera_text"])
else:
    image_file = st.file_uploader(T["upload_text"], type=["jpg", "png", "jpeg"])

# ---------------- PROCESS IMAGE ----------------
if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Leaf Image", use_container_width=True)

    processed_img = preprocess_image(image_file)

    raw_label, confidence = predict_disease(processed_img)
    disease_label = map_to_crop_disease(raw_label)

    infected_pct = infected_area_percentage(processed_img)
    severity = severity_level(infected_pct)
    urgency = urgency_message(severity)
    actions = action_recommendation(severity)

    st.divider()
    st.markdown(f"## {T['results']}")

    st.subheader(T["ai_pred"])
    st.write(f"**{T['detected']}:** {disease_label}")
    st.write(f"**{T['confidence']}:** {confidence:.2f}")

    st.subheader(T["severity"])
    st.progress(min(max(int(infected_pct), 0), 100))
    st.write(f"**{T['severity_level']}:** {severity}")
    st.write(f"**{T['affected']}:** {infected_pct:.1f}%")

    st.subheader(T["urgency"])
    st.info(urgency)

    st.subheader(T["action"])
    st.write(f"**{T['organic']}:** {actions['Organic']}")
    st.write(f"**{T['chemical']}:** {actions['Chemical']}")
    st.write(f"**{T['advice']}:** {actions['Advice']}")

    st.success(T["done"])
