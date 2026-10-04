from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
from fastapi.responses import HTMLResponse, FileResponse # FileResponse add karna na bhoolein

app = FastAPI(title="Crop Disease Detector")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 1. Device and Model Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load saved classes
classes = torch.load('model/classes.pth')
num_classes = len(classes)

# Load ResNet18 Architecture and our saved weights
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load('model/disease_model.pth', map_location=device, weights_only=True))
model = model.to(device)
model.eval() # Set model to evaluation mode

# Image Preprocessing (same as training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- Offline Disease Knowledge Base ---
disease_info = {
    "Pepper_bell___Bacterial_spot": {
        "organic": "Neem oil spray or copper-based organic fungicides.",
        "chemical": "Copper sprays combined with Mancozeb.",
        "prevention": "Ensure good air circulation, avoid overhead watering."
    },
    "Potato___Early_blight": {
        "organic": "Bacillus subtilis or copper fungicides.",
        "chemical": "Chlorothalonil or Mancozeb based fungicides.",
        "prevention": "Crop rotation and remove infected plant debris."
    },
    "Potato___Late_blight": {
        "organic": "Copper sprays (preventative only).",
        "chemical": "Mefenoxam or Chlorothalonil.",
        "prevention": "Use certified disease-free seeds and avoid damp conditions."
    },
    "Tomato___Bacterial_spot": {
        "organic": "Copper-based sprays early in the season.",
        "chemical": "Copper fungicides mixed with Mancozeb.",
        "prevention": "Use drip irrigation instead of sprinklers."
    },
    "Tomato___Early_blight": {
        "organic": "Prune lower leaves, use copper fungicides.",
        "chemical": "Chlorothalonil, Mancozeb, or Copper formulations.",
        "prevention": "Mulching to prevent soil from splashing on leaves."
    },
    "Tomato___Late_blight": {
        "organic": "Copper sprays before wet weather.",
        "chemical": "Chlorothalonil or Mancozeb.",
        "prevention": "Destroy infected plants immediately, do not compost."
    },
    "Tomato___Leaf_Mold": {
        "organic": "Increase ventilation, use potassium bicarbonate.",
        "chemical": "Fungicides containing Chlorothalonil.",
        "prevention": "Keep humidity low in greenhouses and space plants out."
    },
    "Tomato___Septoria_leaf_spot": {
        "organic": "Remove infected leaves, apply neem oil.",
        "chemical": "Chlorothalonil or Mancozeb.",
        "prevention": "Weed control and crop rotation for 1-2 years."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "organic": "Insecticidal soap, neem oil, or releasing ladybugs.",
        "chemical": "Miticides or Abamectin.",
        "prevention": "Keep plants watered; mites thrive in dry/hot conditions."
    },
    "Tomato___Target_Spot": {
        "organic": "Improve airflow and use copper fungicides.",
        "chemical": "Chlorothalonil or Azoxystrobin.",
        "prevention": "Avoid leaving wet foliage overnight."
    },
    "Tomato___Tomato_YellowLeaf__Curl_Virus": {
        "organic": "Use reflective mulches to repel whiteflies (vectors).",
        "chemical": "Insecticides like Imidacloprid to control whiteflies.",
        "prevention": "Plant resistant varieties and use weed-free fields."
    },
    "Tomato___Tomato_mosaic_virus": {
        "organic": "No cure. Remove and destroy infected plants.",
        "chemical": "No chemical control available for viruses.",
        "prevention": "Disinfect tools, wash hands often, avoid using tobacco near plants."
    }
}

# Healthy crops default info
healthy_info = {
    "organic": "N/A - Plant is healthy!",
    "chemical": "N/A - Avoid unnecessary chemicals.",
    "prevention": "Maintain proper watering, sunlight, and regular fertilizer schedule."
}

# --- PWA Routes ---
@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("static/manifest.json", media_type="application/manifest+json")

@app.get("/sw.js")
async def get_sw():
    return FileResponse("static/sw.js", media_type="application/javascript")
# ------------------

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

import torch.nn.functional as F

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            predicted_class = classes[predicted.item()]
            confidence_score = round(confidence.item() * 100, 2)
            
            # --- GET TREATMENT INFO ---
            if "healthy" in predicted_class.lower():
                treatment = healthy_info
            else:
                treatment = disease_info.get(predicted_class, {
                    "organic": "Consult local agricultural expert.",
                    "chemical": "Consult local agricultural expert.",
                    "prevention": "Maintain field hygiene."
                })
            
        return {
            "filename": file.filename, 
            "prediction": predicted_class,
            "confidence": confidence_score,
            "treatment": treatment  # Naya data bheja
        }
    
    except Exception as e:
        return {"error": str(e)}