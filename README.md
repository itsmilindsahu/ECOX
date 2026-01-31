# 🌱 ECOX

**ECOX** is an AI-powered, farmer-first web application that helps identify crop health issues by analyzing leaf images and, more importantly, estimating **disease severity and urgency** to guide timely action.

Unlike traditional crop disease apps that only focus on naming diseases, ECOX prioritizes **decision support** for real-world farming conditions.

---

## 🚜 Problem Statement

Farmers often rely on visual inspection to assess crop diseases, which can lead to delayed or incorrect treatment.  
Most AI-based tools require high-quality images, stable internet, GPS access, and provide only disease names without indicating **how severe the problem is**.

This gap is especially critical for farmers using **low-end smartphones** in rural areas.

---

## 💡 Our Solution

ECOX provides:
- Image-based crop disease analysis
- **Severity estimation** (Mild / Moderate / Severe)
- **Urgency-based recommendations**
- Region-aware crop hints
- Clear guidance even when the disease is unknown

The system is designed to work with **low-quality images**, minimal user input, and without relying on GPS or constant internet access.

---

## ✨ Key Features

- 📷 **Camera & Image Upload Support**  
- 🌡️ **Disease Severity Estimation**  
- 🚦 **Urgency Classification & Action Advice**  
- 🧠 **Ethical AI Handling of Unknown Diseases**  
- 🌍 **Region-based Crop Suggestions (Manual, Privacy-safe)**  
- 📊 **Common Disease Knowledge by Region**  
- 📱 **Optimized for Low-End Smartphones**  
- 🎨 **Simple Green & White Farmer-Friendly UI**

---

## ⚙️ System Architecture (Overview)

1. **Frontend (Streamlit Web App)**  
   - Mobile-friendly interface  
   - Camera capture & upload  

2. **Image Processing Layer**  
   - Image resizing & normalization  
   - Low-end phone noise handling  
   - Image quality assessment  

3. **AI Inference Layer**  
   - Lightweight pretrained CNN (MobileNetV2)  
   - Demo-level disease classification  

4. **Decision Intelligence Layer**  
   - Infected area estimation  
   - Severity & urgency determination  
   - Action recommendation  

5. **Context Layer**  
   - Region-based crop hints  
   - Common disease knowledge  

---

## 🧠 Design Philosophy

- **Severity over disease name**  
- **Do not blame the user for AI limitations**  
- **No GPS dependency** (privacy & offline-friendly)  
- **Minimal clicks, minimal cognitive load**  
- **Clear and honest feedback**

---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ecox.git
cd ecox
