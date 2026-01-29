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
        "lang": "Select Language",
        "crop": "🌾 Select Crop (Optional but Recommended)",
        "crop_hint": "Choose the crop type",
        "input": "📸 Capture or Upload Crop Leaf Image",
        "take": "📷 Take Photo",
        "upload": "📁 Upload Image",
        "camera": "Take a clear photo of the crop leaf",
        "upload_txt": "Upload crop leaf image",
        "results": "📊 Analysis Results",
        "pred": "🧠 AI Prediction",
        "detected": "Detected Disease",
        "confidence": "Model Confidence",
        "severity": "🌡️ Disease Severity",
        "severity_lvl": "Severity Level",
        "affected": "Affected Area",
        "urgency": "🚦 Urgency Status",
        "action": "🌿 Recommended Action",
        "organic": "Organic Method",
        "chemical": "Chemical Method",
        "advice": "Advice",
        "unknown_warn": "⚠️ The system could not confidently identify the disease.",
        "unknown_help": (
            "🔍 Suggested Actions:\n"
            "- Capture a clearer image in good lighting\n"
            "- Upload images of multiple leaves\n"
            "- Monitor the crop for 2–3 days\n"
            "- Consult a local agriculture officer if symptoms persist"
        ),
        "done": "✅ Analysis complete. Designed for real field conditions."
    },
    "Hindi": {
        "title": "🌱 ecox",
        "subtitle": "फसल रोग की गंभीरता और उपचार के लिए एआई आधारित प्रणाली",
        "lang": "भाषा चुनें",
        "crop": "🌾 फसल चुनें (अनुशंसित)",
        "crop_hint": "फसल का चयन करें",
        "input": "📸 फसल पत्ती की फोटो लें या अपलोड करें",
        "take": "📷 फोटो लें",
        "upload": "📁 फोटो अपलोड करें",
        "camera": "फसल पत्ती की स्पष्ट फोटो लें",
        "upload_txt": "फसल पत्ती की फोटो अपलोड करें",
        "results": "📊 विश्लेषण परिणाम",
        "pred": "🧠 एआई भविष्यवाणी",
        "detected": "पहचाना गया रोग",
        "confidence": "विश्वास स्तर",
        "severity": "🌡️ रोग की गंभीरता",
        "severity_lvl": "गंभीरता स्तर",
        "affected": "प्रभावित क्षेत्र",
        "urgency": "🚦 तात्कालिक स्थिति",
        "action": "🌿 अनुशंसित उपचार",
        "organic": "जैविक तरीका",
        "chemical": "रासायनिक तरीका",
        "advice": "सलाह",
        "unknown_warn": "⚠️ रोग को सही तरीके से पहचाना नहीं जा सका।",
        "unknown_help": (
            "🔍 सुझाव:\n"
            "- बेहतर रोशनी में स्पष्ट फोटो लें\n"
            "- कई पत्तियों की फोटो अपलोड करें\n"
            "- 2–3 दिन तक फसल पर नजर रखें\n"
            "- समस्या बनी रहे तो कृषि अधिकारी से संपर्क करें"
        ),
        "done": "✅ विश्लेषण पूर्ण हुआ। वास्तविक खेत परिस्थितियों के लिए डिज़ाइन किया गया।"
    },
    "Telugu": {
        "title": "🌱 ecox",
        "subtitle": "పంట వ్యాధి తీవ్రత మరియు చికిత్స కోసం AI ఆధారిత వ్యవస్థ",
        "lang": "భాషను ఎంచుకోండి",
        "crop": "🌾 పంటను ఎంచుకోండి (సిఫార్సు చేయబడింది)",
        "crop_hint": "పంట రకం ఎంచుకోండి",
        "input": "📸 పంట ఆకు ఫోటో తీయండి లేదా అప్లోడ్ చేయండి",
        "take": "📷 ఫోటో తీయండి",
        "upload": "📁 ఫోటో అప్లోడ్ చేయండి",
        "camera": "పంట ఆకు యొక్క స్పష్టమైన ఫోటో తీయండి",
        "upload_txt": "పంట ఆకు ఫోటోను అప్లోడ్ చేయండి",
        "results": "📊 విశ్లేషణ ఫలితాలు",
        "pred": "🧠 AI అంచనా",
        "detected": "గుర్తించిన వ్యాధి",
        "confidence": "నమ్మక స్థాయి",
        "severity": "🌡️ వ్యాధి తీవ్రత",
        "severity_lvl": "తీవ్రత స్థాయి",
        "affected": "ప్రభావిత ప్రాంతం",
        "urgency": "🚦 అత్యవసర స్థితి",
        "action": "🌿 సూచించిన చికిత్స",
        "organic": "జైవ పద్ధతి",
        "chemical": "రసాయన పద్ధతి",
        "advice": "సలహా",
        "unknown_warn": "⚠️ వ్యాధిని ఖచ్చితంగా గుర్తించలేకపోయాం.",
        "unknown_help": (
            "🔍 సూచనలు:\n"
            "- మంచి వెలుతురులో స్పష్టమైన ఫోటో తీయండి\n"
            "- అనేక ఆకుల ఫోటోలు అప్లోడ్ చేయండి\n"
            "- 2–3 రోజులు పంటను గమనించండి\n"
            "- సమస్య కొనసాగితే వ్యవసాయ అధికారిని సంప్రదించండి"
        ),
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

# ---------------- CROP SELECTION ----------------
st.markdown(f"### {T['crop']}")
crop = st.selectbox(
    T["crop_hint"],
    ["Unknown", "Rice", "Wheat", "Maize", "Tomato", "Potato", "Cotton"]
)

# ---------------- IMAGE INPUT ----------------
st.markdown(f"### {T['input']}")

method = st.radio(
    T["lang"],
    [T["take"], T["upload"]],
    horizontal=True
)

image_file = None

if method == T["take"]:
    image_file = st.camera_input(T["camera"])
else:
    image_file = st.file_uploader(T["upload_txt"], type=["jpg", "png", "jpeg"])

# ---------------- PROCESS IMAGE ----------------
if image_file:
    image = Image.open(image_file)
    st.image(image, use_container_width=True)

    processed_img = preprocess_image(image_file)

    raw_label, confidence = predict_disease(processed_img)
    disease_label = map_to_crop_disease(raw_label)

    infected_pct = infected_area_percentage(processed_img)
    severity = severity_level(infected_pct)
    urgency = urgency_message(severity)
    actions = action_recommendation(severity)

    st.divider()
    st.markdown(f"## {T['results']}")

    st.subheader(T["pred"])
    st.write(f"**{T['detected']}:** {disease_label}")
    st.write(f"**Crop:** {crop}")
    st.write(f"**{T['confidence']}:** {confidence:.2f}")

    if "Unknown" in disease_label:
        st.warning(T["unknown_warn"])
        st.info(T["unknown_help"])
    else:
        st.subheader(T["severity"])
        st.progress(min(max(int(infected_pct), 0), 100))
        st.write(f"**{T['severity_lvl']}:** {severity}")
        st.write(f"**{T['affected']}:** {infected_pct:.1f}%")

        st.subheader(T["urgency"])
        st.info(urgency)

        st.subheader(T["action"])
        st.write(f"**{T['organic']}:** {actions['Organic']}")
        st.write(f"**{T['chemical']}:** {actions['Chemical']}")
        st.write(f"**{T['advice']}:** {actions['Advice']}")

    st.success(T["done"])
