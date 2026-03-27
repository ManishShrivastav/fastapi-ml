from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# import the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

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