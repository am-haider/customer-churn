from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Annotated
import os
import uvicorn
import pickle
import numpy as np

# Setup directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")
frontend_path = os.path.join(BASE_DIR, "Frontend")

# Load model
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")
    model = None

app = FastAPI(title="Customer Churn Prediction API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class customer_data(BaseModel):
    Gender_encoded: Annotated[int, Field(ge=0, le=1)]
    Subscription_Type_encoded: Annotated[int, Field(ge=0, le=2)]
    Contract_Length_encoded: Annotated[int, Field(ge=0, le=2)]
    Payment_Delay: Annotated[int, Field(ge=0)]

@app.post("/predict")
def predict_churn(data: customer_data):
    if model is None:
        return {"error": "Model not loaded"}

    features = np.array([[data.Gender_encoded,
                          data.Subscription_Type_encoded,
                          data.Contract_Length_encoded,
                          data.Payment_Delay]])

    prediction = int(model.predict(features)[0])
    return {"churn_prediction": prediction}

# Serve static files from Frontend directory at the root
# MUST be added after all other routes
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

