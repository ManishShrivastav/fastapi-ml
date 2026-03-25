from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city where the patient resides", example="New York")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="The gender of the patient", example="Male")]
    height: Annotated[float, Field(..., gt=0, description="The height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(..., gt=0, description="The weight of the patient in kilograms", example=70.0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_patients():
    with open("patients.json", "r") as f:
        data = json.load(f)
    
    return data


@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patient records."}

@app.get("/view-patients")
def view_patients():
    return load_patients()


@app.get("/view-patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example="P001")):
    # load all patients from the JSON file
    patients = load_patients()
    patient = patients.get(patient_id)
    
    if patient:
        return patient
    else:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    
@app.get("/sort-patients")
def sort_patients(sort_by: str = Query("name", description="Sort on the basis of height, weight, or bmi"), 
                  order: str = Query("asc", description="Sort order: asc for ascending, desc for descending")):
    
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Please use one of {valid_fields}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order. Please use 'asc' or 'desc'")
    
    patients = load_patients()

    sorted_patients = sorted(patients.values(), key=lambda x: x[sort_by], reverse=(order == "desc"))
    
    return sorted_patients


