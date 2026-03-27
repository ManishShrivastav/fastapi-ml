from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Health Insurance Premium Prediction API."}

@app.get("/health")
def health_check():
    return{
        "status": "OK",
        "model_loaded": model is not None,
        "model_version": MODEL_VERSION
    }   

@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: UserInput):

    user_input = {
        "bmi": input_data.bmi,
        "age_group": input_data.age_group,
        "lifestyle_risk": input_data.lifestyle_risk,
        "city_tier": input_data.city_tier,
        "income_lpa": input_data.income_lpa,
        "occupation": input_data.occupation
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content=prediction)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})