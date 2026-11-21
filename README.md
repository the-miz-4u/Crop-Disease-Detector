# AgriVision AI — Intelligent Crop Disease Diagnosis PWA

**AgriVision AI** is a lightweight, bilingual, offline-capable Progressive Web App (PWA) for real-time crop leaf disease detection. Powered by a CPU-optimized **ResNet18** deep learning model and **FastAPI**, it goes beyond standard classification by providing **Explainable AI (Grad-CAM heatmaps)**, **automatic infection severity estimation**, a **Smart Quality & Out-of-Distribution (OOD) Guard**, **voice assistance**, and **instant A4 PDF reports**.

**Live Demo:** [https://crop-disease-detector-ovri.onrender.com](https://crop-disease-detector-ovri.onrender.com)

---

## Screenshots

### 1. Home Page & Upload Interface
![Home Page](https://github.com/user-attachments/assets/5619e428-8037-462b-84f2-920219792b17)

### 2. Diagnosis Result with Grad-CAM Heatmap & Severity %
![Diagnosis Result](https://github.com/user-attachments/assets/07a68068-2a1d-411e-9144-edfa39e05609
)

### 3. Auto-Generated A4 PDF Report
![PDF Report](https://github.com/user-attachments/assets/23fc2860-e49c-469e-921f-8d2a31cfbdfb
)

---

## Key Features

- **Explainable AI (Grad-CAM + Severity %):** Generates a real-time visual focus heatmap over the leaf to highlight diseased regions and calculates the estimated infected area percentage (*Mild / Moderate / Severe*) using pure NumPy, PyTorch, and Pillow (zero OpenCV/Matplotlib overhead).
- **Smart Image Quality & OOD Guard:** Automatically rejects blurry, dark, overexposed, document/screenshot, or non-leaf images before/after inference using Laplacian blur variance, HSV foliage checks, confidence thresholding, and normalized Shannon entropy.
- **Bilingual UI (English & Hindi):** One-click toggle translates the entire interface, diagnosis results, treatment advice, and PDF reports between English and Hindi (`Noto Sans Devanagari`).
- **Voice Assistant (Text-to-Speech):** Reads out the diagnosis aloud in English or Hindi using the Web Speech API for field accessibility.
- **Client-Side A4 PDF Reports:** Generates clean, downloadable A4 diagnosis reports directly on the user's device using `jsPDF` and HTML5 Canvas.
- **Offline-First PWA & Scan History:** Installable on mobile/desktop with Service Workers, live Online/Offline network awareness, and browser-based scan history (`localStorage`) for viewing past reports without internet.
- **512MB RAM Cloud Optimization:** Configured with CPU-only PyTorch wheels to run smoothly on free-tier cloud servers (Render 512MB RAM limit) without Out-of-Memory (OOM) crashes.

---

## How AgriVision AI Bridges Existing Research Gaps

| Aspect | Existing Literature (Conventional Models) | AgriVision AI |
| :--- | :--- | :--- |
| **Transparency** | Black-box classification (disease label only) | **Explainable AI (Grad-CAM)** heatmap + **Infection Severity %** |
| **Real-World Robustness** | Fails on blurry or non-leaf inputs; forces wrong labels | **Smart Quality & OOD Guard** (Blur, Brightness, HSV & Entropy checks) |
| **Compute Efficiency** | Heavy GPU-dependent models (ResNet197, Ensembles) | **Lightweight ResNet18** running on CPU under **512MB RAM** |
| **Farmer Usability** | Lab-only evaluation with no actionable delivery | **Bilingual PWA** with Voice TTS, Offline History & PDF Reports |

---

## Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Tailwind CSS, FontAwesome, Google Fonts (`Poppins`, `Noto Sans Devanagari`)
- **Backend:** Python 3.8+, FastAPI, Uvicorn, Jinja2, `python-multipart`
- **AI / Computer Vision:** PyTorch (CPU-only), Torchvision, ResNet18 (PlantVillage 15-class dataset), NumPy, Pillow (PIL)
- **Web APIs & PWA:** Service Workers, `manifest.json`, `jsPDF`, HTML5 Canvas, Web Speech API, LocalStorage API, Web Share API, Vibration API
- **Deployment:** Render (PaaS), Git & GitHub

---

## Project Structure

```text
Crop-Disease-Detector/
├── main.py                # FastAPI server, ResNet18 inference & /predict endpoint
├── gradcam.py             # Lightweight Grad-CAM heatmap & severity % calculator
├── quality_guard.py       # Pre-inference quality & post-inference OOD guard
├── requirements.txt       # CPU-only PyTorch & backend dependencies
├── model/
│   ├── disease_model.pth  # Trained ResNet18 model weights
│   └── classes.pth        # Saved class labels
├── templates/
│   └── index.html         # Main responsive SaaS dashboard UI
├── static/
│   ├── script.js          # Frontend logic, bilingual toggle, PDF & history
│   ├── manifest.json      # PWA manifest
│   └── sw.js              # Service Worker for offline caching
└── screenshots/
    ├── home.png
    ├── result.png
    └── report.png
```

---

## Local Setup & Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/the-miz-4u/Crop-Disease-Detector.git](https://github.com/the-miz-4u/Crop-Disease-Detector.git)
   cd Crop-Disease-Detector
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies (CPU-only PyTorch)**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. Open `http://127.0.0.1:8000` in your browser.

---

## Deployment Note (Render Free Tier)

To stay within Render's **512MB RAM** limit, `requirements.txt` uses PyTorch's lightweight CPU-only index:

```text
--extra-index-url [https://download.pytorch.org/whl/cpu](https://download.pytorch.org/whl/cpu)
torch
torchvision
```

**Start Command on Render:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
