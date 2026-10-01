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

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    try:
        # Read the uploaded image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Preprocess the image
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # Predict
        with torch.no_grad():
            outputs = model(input_tensor)
            _, predicted = torch.max(outputs, 1)
            predicted_class = classes[predicted.item()]
            
        return {"filename": file.filename, "prediction": predicted_class}
    
    except Exception as e:
        return {"error": str(e)}