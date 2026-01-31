# 🌱 ECOX  
*A Prototype for Crop Disease Severity Estimation and Decision Support*

---

## 1. Background and Motivation

Crop diseases are a major cause of yield loss in agriculture.  
In many rural areas, farmers rely on visual inspection and personal experience to judge whether a disease is serious or not. This often leads to delayed or incorrect treatment.

Most existing AI-based crop disease systems focus only on identifying the disease name. However, for practical decision-making, farmers need to know **how severe the disease is** and **whether immediate action is required**.

This project was developed to study how image-based AI systems can support **severity estimation and decision guidance**, especially under real-world constraints such as low-end smartphones and limited connectivity.

---

## 2. Problem Statement

- Farmers often use low-quality mobile phone cameras.
- Disease identification alone does not indicate urgency.
- Many AI systems assume high-quality images and constant internet access.
- GPS-based solutions raise privacy and reliability concerns.

There is a need for a simple and reliable system that can assist farmers in **estimating disease severity** and **choosing appropriate actions**, without relying on complex infrastructure.

---

## 3. Objective of the Project

The main objectives of this project are:

- To analyze crop leaf images using a lightweight AI model.
- To estimate the **severity of visible infection** rather than only classifying diseases.
- To provide **action-oriented guidance** based on severity levels.
- To design a system that works with low-end devices and minimal user input.

---

## 4. Overview of the Proposed System

ECOX is a web-based prototype that allows a user to:

1. Select their region and crop type.
2. Capture or upload an image of a crop leaf.
3. Receive an estimate of disease severity.
4. Obtain simple guidance on urgency and treatment.

The system is designed as a **decision-support tool**, not a diagnostic replacement.

---

## 5. System Architecture (Conceptual)

The system follows a layered structure:

- **User Interface:**  
  A simple web interface optimized for mobile devices.

- **Image Processing Layer:**  
  Image resizing, normalization, and basic quality checks to handle low-quality inputs.

- **AI Inference Layer:**  
  A pretrained convolutional neural network (MobileNetV2) is used to demonstrate disease-related feature extraction.

- **Severity Estimation Layer:**  
  The proportion of visually affected leaf area is estimated to classify severity as Mild, Moderate, or Severe.

- **Decision Logic Layer:**  
  Severity levels are mapped to urgency and suggested actions.

- **Context Layer:**  
  Region-based crop and disease information is used to provide contextual guidance without GPS dependency.

---

## 6. Design Considerations

- **Severity-first approach:**  
  Severity estimation is prioritized over disease naming.

- **Ethical handling of uncertainty:**  
  When the disease cannot be identified confidently, the system avoids giving misleading advice.

- **Low-end device support:**  
  The system is designed to tolerate noisy and low-resolution images.

- **Privacy-aware design:**  
  Region selection is manual to avoid GPS and location tracking.

---

## 7. Implementation Details

- **Frontend:** Streamlit (Python-based web framework)
- **AI Model:** MobileNetV2 (pretrained on ImageNet, used as a demonstration model)
- **Image Processing:** OpenCV and NumPy
- **Deployment:** Streamlit Cloud

This implementation focuses on validating the **end-to-end pipeline** rather than achieving high classification accuracy.

---

## 8. Limitations

- The current AI model is not trained on crop-specific disease datasets.
- Disease labels are limited and used for demonstration purposes.
- The system does not replace expert agricultural diagnosis.

These limitations are acknowledged and addressed in the future scope.

---

## 9. Future Scope

- Training with crop-specific datasets (e.g., PlantVillage).
- District-level disease trend analysis.
- Multilingual and voice-based guidance.
- Integration with agricultural advisory services.

---

## 10. Conclusion

ECOX demonstrates how AI can be used as a **support tool** for agricultural decision-making rather than a black-box predictor. The project emphasizes simplicity, transparency, and real-world constraints, making it suitable for further academic and applied research.

---

## 11. Acknowledgement

This project was developed as part of the **AI4Life Hackathon** at **Indian Institute of Science Education and Research (IISER) Tirupati**.

---

## Disclaimer

This is a student research prototype intended for academic discussion and demonstration purposes.
