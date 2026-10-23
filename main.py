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

# --- Offline Disease Knowledge Base (Bilingual) ---
disease_info = {
    "Pepper_bell___Bacterial_spot": {
        "en": {
            "name": "Pepper Bell - Bacterial Spot",
            "organic": "Neem oil spray or copper-based organic fungicides.",
            "chemical": "Copper sprays combined with Mancozeb.",
            "prevention": "Ensure good air circulation, avoid overhead watering."
        },
        "hi": {
            "name": "शिमला मिर्च - जीवाणु धब्बा (Bacterial Spot)",
            "organic": "नीम के तेल का स्प्रे या तांबा (copper) आधारित जैविक फफूंदनाशक का उपयोग करें।",
            "chemical": "मैनकोज़ेब (Mancozeb) के साथ कॉपर स्प्रे का छिड़काव करें।",
            "prevention": "पौधों के बीच हवा का अच्छा प्रवाह रखें, ऊपर से पानी देने से बचें।"
        }
    },
    "Potato___Early_blight": {
        "en": {
            "name": "Potato - Early Blight",
            "organic": "Bacillus subtilis or copper fungicides.",
            "chemical": "Chlorothalonil or Mancozeb based fungicides.",
            "prevention": "Crop rotation and remove infected plant debris."
        },
        "hi": {
            "name": "आलू - अगेती झुलसा (Early Blight)",
            "organic": "बैसिलस सबटिलिस या तांबा (copper) फफूंदनाशक का प्रयोग करें।",
            "chemical": "क्लोरोथालोनिल या मैनकोज़ेब आधारित फफूंदनाशक का छिड़काव करें।",
            "prevention": "फसल चक्र अपनाएं और संक्रमित पौधे के हिस्सों को तुरंत खेत से हटा दें।"
        }
    },
    "Potato___Late_blight": {
        "en": {
            "name": "Potato - Late Blight",
            "organic": "Copper sprays (preventative only).",
            "chemical": "Mefenoxam or Chlorothalonil.",
            "prevention": "Use certified disease-free seeds and avoid damp conditions."
        },
        "hi": {
            "name": "आलू - पछेती झुलसा (Late Blight)",
            "organic": "बचाव के लिए तांबे (copper) का स्प्रे करें।",
            "chemical": "मेफेनोक्साम (Mefenoxam) या क्लोरोथालोनिल का उपयोग करें।",
            "prevention": "प्रमाणित रोग-मुक्त बीजों का उपयोग करें और खेत में नमी/जलभराव से बचें।"
        }
    },
    "Tomato___Bacterial_spot": {
        "en": {
            "name": "Tomato - Bacterial Spot",
            "organic": "Copper-based sprays early in the season.",
            "chemical": "Copper fungicides mixed with Mancozeb.",
            "prevention": "Use drip irrigation instead of sprinklers."
        },
        "hi": {
            "name": "टमाटर - जीवाणु धब्बा (Bacterial Spot)",
            "organic": "सीजन की शुरुआत में तांबा आधारित स्प्रे का इस्तेमाल करें।",
            "chemical": "मैनकोज़ेब के साथ कॉपर फफूंदनाशक का छिड़काव करें।",
            "prevention": "फव्वारे (sprinklers) की जगह ड्रिप सिंचाई (बूंद-बूंद सिंचाई) का प्रयोग करें।"
        }
    },
    "Tomato___Early_blight": {
        "en": {
            "name": "Tomato - Early Blight",
            "organic": "Prune lower leaves, use copper fungicides.",
            "chemical": "Chlorothalonil, Mancozeb, or Copper formulations.",
            "prevention": "Mulching to prevent soil from splashing on leaves."
        },
        "hi": {
            "name": "टमाटर - अगेती झुलसा (Early Blight)",
            "organic": "निचली पत्तियों की छंटाई करें और तांबा फफूंदनाशक का उपयोग करें।",
            "chemical": "क्लोरोथालोनिल, मैनकोज़ेब या कॉपर आधारित दवा का छिड़काव करें।",
            "prevention": "मिट्टी को पत्तियों पर उछलने से रोकने के लिए मल्चिंग (Mulching) करें।"
        }
    },
    "Tomato___Late_blight": {
        "en": {
            "name": "Tomato - Late Blight",
            "organic": "Copper sprays before wet weather.",
            "chemical": "Chlorothalonil or Mancozeb.",
            "prevention": "Destroy infected plants immediately, do not compost."
        },
        "hi": {
            "name": "टमाटर - पछेती झुलसा (Late Blight)",
            "organic": "नम/बारिश के मौसम से पहले तांबे (copper) का स्प्रे करें।",
            "chemical": "क्लोरोथालोनिल या मैनकोज़ेब का छिड़काव करें।",
            "prevention": "संक्रमित पौधों को तुरंत नष्ट कर दें, इनसे खाद (compost) न बनाएं।"
        }
    },
    "Tomato___Leaf_Mold": {
        "en": {
            "name": "Tomato - Leaf Mold",
            "organic": "Increase ventilation, use potassium bicarbonate.",
            "chemical": "Fungicides containing Chlorothalonil.",
            "prevention": "Keep humidity low in greenhouses and space plants out."
        },
        "hi": {
            "name": "टमाटर - लीफ मोल्ड (पत्ती फफूंदी)",
            "organic": "हवा का प्रवाह बढ़ाएं और पोटेशियम बाइकार्बोनेट का उपयोग करें।",
            "chemical": "क्लोरोथालोनिल युक्त फफूंदनाशक का छिड़काव करें।",
            "prevention": "ग्रीनहाउस में नमी कम रखें और पौधों के बीच पर्याप्त दूरी रखें।"
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "en": {
            "name": "Tomato - Septoria Leaf Spot",
            "organic": "Remove infected leaves, apply neem oil.",
            "chemical": "Chlorothalonil or Mancozeb.",
            "prevention": "Weed control and crop rotation for 1-2 years."
        },
        "hi": {
            "name": "टमाटर - सेप्टोरिया लीफ स्पॉट",
            "organic": "संक्रमित पत्तियों को तोड़ दें और नीम के तेल का छिड़काव करें।",
            "chemical": "क्लोरोथालोनिल या मैनकोज़ेब का उपयोग करें।",
            "prevention": "खरपतवार नियंत्रण करें और 1-2 साल के लिए फसल चक्र अपनाएं।"
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "en": {
            "name": "Tomato - Spider Mites",
            "organic": "Insecticidal soap, neem oil, or releasing ladybugs.",
            "chemical": "Miticides or Abamectin.",
            "prevention": "Keep plants watered; mites thrive in dry/hot conditions."
        },
        "hi": {
            "name": "टमाटर - मकड़ी के जाले (Spider Mites)",
            "organic": "कीटनाशक साबुन, नीम का तेल या मित्र कीटों (Ladybugs) का उपयोग करें।",
            "chemical": "माइटिसाइड्स (Miticides) या एबामेक्टिन (Abamectin) का छिड़काव करें।",
            "prevention": "पौधों में नमी बनाए रखें; ये कीट सूखे और गर्म मौसम में पनपते हैं।"
        }
    },
    "Tomato___Target_Spot": {
        "en": {
            "name": "Tomato - Target Spot",
            "organic": "Improve airflow and use copper fungicides.",
            "chemical": "Chlorothalonil or Azoxystrobin.",
            "prevention": "Avoid leaving wet foliage overnight."
        },
        "hi": {
            "name": "टमाटर - टारगेट स्पॉट",
            "organic": "हवा का प्रवाह सुधारें और तांबा फफूंदनाशक का उपयोग करें।",
            "chemical": "क्लोरोथालोनिल या एज़ोक्सीस्ट्रोबिन (Azoxystrobin) का छिड़काव करें।",
            "prevention": "रात भर पत्तियों को गीला छोड़ने से बचें।"
        }
    },
    "Tomato___Tomato_YellowLeaf__Curl_Virus": {
        "en": {
            "name": "Tomato - Yellow Leaf Curl Virus",
            "organic": "Use reflective mulches to repel whiteflies (vectors).",
            "chemical": "Insecticides like Imidacloprid to control whiteflies.",
            "prevention": "Plant resistant varieties and use weed-free fields."
        },
        "hi": {
            "name": "टमाटर - पीला पत्ता मरोड़ वायरस (Yellow Leaf Curl)",
            "organic": "सफेद मक्खी को दूर रखने के लिए रिफ्लेक्टिव मल्च (Reflective mulches) का उपयोग करें।",
            "chemical": "सफेद मक्खी को नियंत्रित करने के लिए इमिडाक्लोप्रिड (Imidacloprid) जैसे कीटनाशक का उपयोग करें।",
            "prevention": "प्रतिरोधी किस्मों को लगाएं और खेत को खरपतवार मुक्त रखें।"
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "en": {
            "name": "Tomato - Mosaic Virus",
            "organic": "No cure. Remove and destroy infected plants.",
            "chemical": "No chemical control available for viruses.",
            "prevention": "Disinfect tools, wash hands often, avoid using tobacco near plants."
        },
        "hi": {
            "name": "टमाटर - मोज़ेक वायरस",
            "organic": "कोई इलाज नहीं है। संक्रमित पौधों को तुरंत उखाड़ कर नष्ट कर दें।",
            "chemical": "वायरस के लिए कोई रासायनिक नियंत्रण उपलब्ध नहीं है।",
            "prevention": "औजारों को कीटाणुरहित करें, हाथ धोएं और पौधों के पास तंबाकू का सेवन न करें।"
        }
    }
}

# Healthy crops default info
healthy_info = {
    "en": {
        "name": "Healthy Crop",
        "organic": "N/A - Plant is healthy!",
        "chemical": "N/A - Avoid unnecessary chemicals.",
        "prevention": "Maintain proper watering, sunlight, and regular fertilizer schedule."
    },
    "hi": {
        "name": "स्वस्थ पौधा (Healthy Crop)",
        "organic": "लागू नहीं - आपका पौधा बिल्कुल स्वस्थ है!",
        "chemical": "लागू नहीं - अनावश्यक रसायनों के उपयोग से बचें।",
        "prevention": "उचित सिंचाई, धूप और नियमित खाद का शेड्यूल बनाए रखें।"
    }
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
                    "en": {
                        "name": predicted_class,
                        "organic": "Consult local agricultural expert.",
                        "chemical": "Consult local agricultural expert.",
                        "prevention": "Maintain field hygiene."
                    },
                    "hi": {
                        "name": predicted_class,
                        "organic": "स्थानीय कृषि विशेषज्ञ से सलाह लें।",
                        "chemical": "स्थानीय कृषि विशेषज्ञ से सलाह लें।",
                        "prevention": "खेत में साफ-सफाई बनाए रखें।"
                    }
                })
            
            return {
                "filename": file.filename, 
                "prediction": predicted_class,
                "confidence": confidence_score,
                "treatment": treatment  # Ab isme 'en' aur 'hi' dono aayenge
            }
    
    except Exception as e:
        return {"error": str(e)}