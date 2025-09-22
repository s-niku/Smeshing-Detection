# src/serve_api.py
import joblib
import re
from fastapi import FastAPI
from pydantic import BaseModel

# ---------- Load model + vectorizer ----------
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ---------- Cleaning function (same as train/predict) ----------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " url ", text)
    text = re.sub(r"\d+", " number ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- FastAPI app ----------
app = FastAPI(title="Smishing Detection API", version="1.0")

class MessageRequest(BaseModel):
    text: str
    

class MessageResponse(BaseModel):
    prediction: str
    label: str
    probabilities: dict

@app.post("/predict", response_model=MessageResponse)
def predict(request: MessageRequest):
    msg_clean = clean_text(request.text)
    msg_vec = vectorizer.transform([msg_clean])

    pred = model.predict(msg_vec)[0]
    probs = model.predict_proba(msg_vec)[0]

    # build response
    label = "Smishing/Spam" if pred == "spam" else "Safe (Ham)"
    return {
        "prediction": str(pred),
        "label": label,
        "probabilities": {
            "ham": float(probs[0]),
            "spam": float(probs[1])
        }
    }
