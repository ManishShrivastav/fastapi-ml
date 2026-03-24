from fastapi import FastAPI
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