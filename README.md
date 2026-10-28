# 🍃 AgriVision AI - Smart Crop Disease Detector

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-success?style=for-the-badge&logo=render)](https://crop-disease-detector-ovri.onrender.com)

AgriVision AI is a highly optimized, AI-powered Progressive Web App (PWA) built to help farmers and agriculturists instantly diagnose crop diseases. By utilizing a fine-tuned Deep Learning model (ResNet18) and a lightning-fast FastAPI backend, it provides real-time disease detection along with instant organic and chemical treatment recommendations.

Designed specifically for rural accessibility and real-world agricultural conditions, the platform features an **Offline Knowledge Base** and operates seamlessly even in low or no internet connectivity areas.

---

## 🚀 Live Application
Access the fully deployed application here: **[AgriVision AI Live on Render](https://crop-disease-detector-ovri.onrender.com)**

---

## 📸 Project Screenshots

### 1. Dashboard & Upload Interface
![Main Interface](https://github.com/user-attachments/assets/1ce97f4b-6ab2-4665-8efe-072bad5efb5d)
*Modern Glassmorphism UI with drag-and-drop and direct mobile camera access.*

### 2. Diagnosis & Treatment Results
![Results Screen](https://github.com/user-attachments/assets/5bee0f5e-2f74-4f4f-9d6f-c6ed12a0a663)
*AI Confidence metrics with instant offline organic, chemical, and prevention recommendations.*

### 3. Network Awareness & Mobile View
![Offline Mode](https://github.com/user-attachments/assets/4152b0f7-6e71-40ea-ab4b-090605b4bae7)
*Live network status badge and PWA mobile-first design.*

---

## ✨ Key Features & UX Upgrades

- **🧠 Deep Learning Engine:** Powered by PyTorch and a fine-tuned ResNet18 architecture trained on the PlantVillage dataset for high-accuracy disease classification (15 classes).
- **⚡ High-Performance Backend:** Built with FastAPI for asynchronous, robust, and fast image processing.
- **📱 Progressive Web App (PWA):** Fully installable on mobile devices, acting like a native app with Service Workers for offline caching.
- **🩺 Offline Treatment Recommender:** Instantly provides *Organic Solutions*, *Chemical Controls*, and *Prevention Tips* directly from a local knowledge base (Zero API dependency).
- **🗣️ Voice Assistant (TTS):** Built-in Text-to-Speech reads out the diagnosis aloud, making it accessible for farmers under harsh sunlight in the fields.
- **📶 Live Network Awareness:** A dynamic real-time badge that detects and displays the user's connection status (Online / Offline Mode).
- **📸 Direct Camera Access:** Automatically triggers the mobile's environment (back) camera for quick field scans.
- **📳 Native Hardware Integration:** Features Haptic Feedback (vibration) on successful diagnosis and uses the Native Web Share API to easily forward results via WhatsApp.
- **🎨 Premium Glassmorphism UI:** A sleek, responsive dashboard built with Tailwind CSS, featuring AI laser scanning animations, dynamic status colors, smooth auto-scrolling, and a 1-click "Scan Another Plant" reset flow.

---

## 🛠️ Tech Stack

**Backend & AI:**
- Python 3.8+
- PyTorch & Torchvision (CNN / ResNet18)
- FastAPI (REST API Framework)
- Uvicorn (ASGI Server)

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Tailwind CSS (Styling & Layout)
- PWA (Service Workers, Web Manifest)

---

## 🚀 Getting Started (Local Development)

Follow these steps to run the project on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/the-miz-4u/Crop-Disease-Detector.git](https://github.com/the-miz-4u/Crop-Disease-Detector.git)
cd Crop-Disease-Detector
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn python-multipart jinja2 torch torchvision pillow
```

### 4. Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 📁 Project Structure

```text
Crop-Disease-Detector/
│
├── main.py                 # FastAPI backend & offline knowledge base
├── train.py                # PyTorch model training script (optional)
├── model/
│   ├── disease_model.pth   # Trained ResNet18 weights
│   └── classes.pth         # Serialized class labels
│
├── static/
│   ├── style.css           # Custom CSS animations
│   ├── script.js           # Frontend logic, Voice API, Network tracking
│   ├── manifest.json       # PWA Manifest configuration
│   └── sw.js               # Service Worker for offline capabilities
│
└── templates/
    └── index.html          # Main application interface (Glassmorphism UI)
```

---

## 👨‍💻 Author

**Manish Sharma**  
GitHub: [@the-miz-4u](https://github.com/the-miz-4u)
