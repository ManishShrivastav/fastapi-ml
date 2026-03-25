from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city where the patient resides", example="New York")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="The gender of the patient", example="male")]
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
        

class PatientUpdate(BaseModel):
    name: Annotated[str | None, Field(default=None, description="The name of the patient", example="John Doe")] # str | None explicitly tells Pydantic the field is nullable.
                                                                                                                # default=None makes it not required.
    city: Annotated[str | None, Field(default=None, description="The city where the patient resides", example="New York")]
    age: Annotated[int | None, Field(default=None, gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal["male", "female", "other"] | None, Field(default=None, description="The gender of the patient", example="male")]
    height: Annotated[float | None, Field(default=None, gt=0, description="The height of the patient in meters", example=1.75)]
    weight: Annotated[float | None, Field(default=None, gt=0, description="The weight of the patient in kilograms", example=70.0)]

def load_patients():
    with open("patients.json", "r") as f:
        data = json.load(f)
    
    return data

def save_patients(patients):
    with open("patients.json", "w") as f:
        json.dump(patients, f)


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


@app.post("/add-patient")
def add_patient(patient: Patient):
    # Load existing patients from the JSON file
    patients = load_patients()

    # Check if the patient ID already exists
    if patient.id in patients:
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists")
    
    # Add the new patient
    patients[patient.id] = patient.model_dump(exclude=['id'])
    
    # Save the updated patients back to the JSON file
    save_patients(patients)

    return JSONResponse(content={"message": f"Patient with ID {patient.id} added successfully"}, status_code=201)


@app.put("/update-patient/{patient_id}")
def update_patient(patient_id: str , patient_update: PatientUpdate):
    patients = load_patients()

    if patient_id not in patients:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    
    existing_patient_info = patients[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key, value in updated_patient_info.items():
        if value is not None:
            existing_patient_info[key] = value

    # existing_patient_info -> pydantic object -> updated bmi and verdict -> dict -> update the patient info in the patients dict
    existing_patient_info['id'] = patient_id # we need to add the id back to the existing_patient_info before creating the Patient object, otherwise it will raise a validation error since id is a required field in the Patient model.
    updated_patient = Patient(**existing_patient_info) # this will automatically update the bmi and verdict based on the updated height and weight
    existing_patient_info = updated_patient.model_dump(exclude=['id']) # we need to exclude the id when updating the existing_patient_info since the id is not stored in the patients dict, it's only used as the key in the patients dict.

    # Update the patient info in the patients dict
    patients[patient_id] = existing_patient_info
    
    save_patients(patients)

    return JSONResponse(content={"message": f"Patient with ID {patient_id} updated successfully"}, status_code=200)