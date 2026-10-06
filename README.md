# 🍃 AgriVision AI - Smart Crop Disease Detector

AgriVision AI is a highly optimized, AI-powered Progressive Web App (PWA) built to help farmers and agriculturists instantly diagnose crop diseases. By utilizing a fine-tuned Deep Learning model (ResNet18) and a lightning-fast FastAPI backend, it provides real-time disease detection along with instant organic and chemical treatment recommendations.

Designed with rural accessibility in mind, the platform features an **Offline Knowledge Base**, meaning it can provide treatment solutions without relying on external APIs or internet connectivity once the disease is classified.

---

## ✨ Key Features

- **🧠 Deep Learning Engine:** Powered by PyTorch and a fine-tuned ResNet18 architecture trained on the PlantVillage dataset for high-accuracy disease classification (15 classes).
- **⚡ High-Performance Backend:** Built with FastAPI for asynchronous, robust, and fast image processing and model serving.
- **📱 Progressive Web App (PWA):** Fully installable on mobile devices and desktops, acting like a native app.
- **🩺 Offline Treatment Recommender:** An integrated rule-based knowledge base that instantly provides *Organic Solutions*, *Chemical Controls*, and *Prevention Tips* without requiring third-party APIs.
- **🎯 AI Confidence Metrics:** Displays the exact confidence percentage of the model's prediction using softmax probability.
- **🎨 Modern Premium UI:** Features a sleek, responsive Glassmorphism dashboard built with Tailwind CSS, including drag-and-drop uploads and cyberpunk-style scanning animations.
- **📤 Native Web Sharing:** Built-in Web Share API to easily share diagnosis results directly to WhatsApp or other messaging platforms.

---

## 🛠️ Tech Stack

**Backend & AI:**
- Python 3
- PyTorch & Torchvision (CNN / ResNet18)
- FastAPI (REST API Framework)
- Uvicorn (ASGI Server)

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Tailwind CSS (Styling & Layout)
- PWA (Service Workers, Manifest)

---

## 🚀 Getting Started

Follow these steps to run the project on your local machine.

### 1. Prerequisites
Ensure you have Python 3.8+ installed. A GPU (NVIDIA) is recommended for faster training, but the app runs perfectly on the CPU for predictions.

### 2. Clone the Repository
```bash
git clone [https://github.com/the-miz-4u/Crop-Disease-Detector.git](https://github.com/the-miz-4u/Crop-Disease-Detector.git)
cd Crop-Disease-Detector
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
# For Windows
venv\Scripts\activate
# For Mac/Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install fastapi uvicorn python-multipart jinja2 torch torchvision pillow
```

### 5. Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Open your browser and navigate to `http://127.0.0.1:8000` to use the application.

---

## 📁 Project Structure

```text
Crop-Disease-Detector/
│
├── main.py                 # FastAPI backend & offline knowledge base
├── train.py                # PyTorch model training script
├── model/
│   ├── disease_model.pth   # Trained ResNet18 weights
│   └── classes.pth         # Serialized class labels
│
├── static/
│   ├── style.css           # Additional custom styles
│   ├── script.js           # Frontend logic, PWA install, and API fetching
│   ├── manifest.json       # PWA Manifest configuration
│   └── sw.js               # Service Worker for offline capabilities
│
└── templates/
    └── index.html          # Main application interface (Glassmorphism UI)
```

---

## 👨‍💻 Author

**Manish Sharma**  
B.Tech CSE Undergraduate  
GitHub: [@the-miz-4u](https://github.com/the-miz-4u)
