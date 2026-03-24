from fastapi import FastAPI, Path
import json

app = FastAPI()

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
        return {"error": "Patient not found"}