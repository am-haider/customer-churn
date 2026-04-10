from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated
import os
import uvicorn
import pickle
import numpy as np

# Setup directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")

# Load model
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")
    model = None

app = FastAPI(title="Customer Churn Prediction API")

# Add CORS Middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class customer_data(BaseModel):
    Gender_encoded: Annotated[int, Field(ge=0, le=1)]
    Subscription_Type_encoded: Annotated[int, Field(ge=0, le=2)]
    Contract_Length_encoded: Annotated[int, Field(ge=0, le=2)]
    Payment_Delay: Annotated[int, Field(ge=0)]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Customer Churn Prediction API!"}

@app.post("/predict")
def predict_churn(data: customer_data):
    if model is None:
        return {"error": "Model not loaded"}

    # Convert input to numpy array matching training features
    features = np.array([[data.Gender_encoded,
                          data.Subscription_Type_encoded,
                          data.Contract_Length_encoded,
                          data.Payment_Delay]])

    # Make prediction
    prediction = int(model.predict(features)[0])
    
    # Return result
    return {"churn_prediction": prediction}