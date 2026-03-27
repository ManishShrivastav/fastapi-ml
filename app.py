from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# import the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# Pydantic model to validate incoming request data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, le=120, description="Age of the user in years")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user in kg")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the user in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual income in lpa")]
    smoker: Annotated[bool, Field(..., description="Whether the user is a smoker")]
    city: Annotated[str, Field(..., description="City of residence")]
    occupation: Annotated[Literal['retired','freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], 
                          Field(..., description="Occupation of the user")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> int:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low" 
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 65:
            return "middle_aged"
        else:
            return "senior"
        
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        

@app.post("/predict")
def predict(input_data: UserInput):

    input_df = pd.DataFrame([{
        "bmi": input_data.bmi,
        "age_group": input_data.age_group,
        "lifestyle_risk": input_data.lifestyle_risk,
        "city_tier": input_data.city_tier,
        "income_lpa": input_data.income_lpa,
        "occupation": input_data.occupation
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={"predicted_category": prediction})