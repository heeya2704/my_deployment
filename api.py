import os
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
import pandas as pd
import joblib

app = FastAPI(
    title="Logistic Regression Prediction API",
    description="FastAPI service for Logistic Regression classification based on StudyHours",
    version="1.0.0"
)

# Load Trained Logistic Regression Model
MODEL_PATH = "mymodel.pkl"
try:
    model = joblib.load(MODEL_PATH)
    print(f"Loaded Logistic Regression model successfully from {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Warning: Could not load model from {MODEL_PATH}: {e}")


# Pydantic Schema for Input Validation
class PredictRequest(BaseModel):
    study_hours: Optional[float] = Field(
        default=None,
        alias="StudyHours",
        description="Number of study hours"
    )
    hours: Optional[float] = Field(
        default=None,
        description="Alias for study_hours"
    )

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "StudyHours": 5.0
            }
        }


@app.get("/", summary="Root status endpoint")
def root():
    """Root endpoint confirming API is online."""
    return {"message": "Logistic Regression ML API is running!"}


@app.get("/testing", summary="Health check endpoint")
def testing():
    """Simple health check endpoint returning JSON status."""
    return {"message": "all ok"}


@app.post(
    "/prediction",
    status_code=status.HTTP_200_OK,
    summary="Make prediction",
    description="Predicts Pass (1) or Fail (0) based on StudyHours using Logistic Regression model"
)
@app.post("/predict", status_code=status.HTTP_200_OK, summary="Make prediction (alias)")
def predict(
    payload: Optional[PredictRequest] = None,
    hours: Optional[float] = Query(None, description="Query parameter for study hours"),
    study_hours: Optional[float] = Query(None, description="Query parameter for study hours")
):
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model (mymodel.pkl) is missing or not loaded."
        )

    # Extract study hours from JSON payload or query parameters
    input_hours = None
    if payload:
        if payload.study_hours is not None:
            input_hours = payload.study_hours
        elif payload.hours is not None:
            input_hours = payload.hours
            
    if input_hours is None and study_hours is not None:
        input_hours = study_hours
    elif input_hours is None and hours is not None:
        input_hours = hours

    if input_hours is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input 'StudyHours' or 'hours' is required in request body or query parameter."
        )

    try:
        # Prepare DataFrame with feature column expected by the model
        newdata = pd.DataFrame({'StudyHours': [float(input_hours)]})
        
        # Predict Class (0 or 1)
        mynewdata = model.predict(newdata)
        prediction_val = int(mynewdata[0])
        
        # Predict Probability if model supports predict_proba
        pass_prob = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(newdata)[0]
            pass_prob = round(float(probabilities[1]), 4)
            
        status_label = "Pass" if prediction_val == 1 else "Fail"

        return {
            "Predication": float(prediction_val),
            "Prediction": prediction_val,
            "status": status_label,
            "pass_probability": pass_prob,
            "study_hours": float(input_hours)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model prediction failure: {str(e)}"
        )