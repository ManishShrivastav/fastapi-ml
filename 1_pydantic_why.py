from pydantic import BaseModel
from typing import Dict, List

class Patient(BaseModel):
    name: str
    age: int
    weight: float = None
    married: bool = None
    allergies: List[str] = None
    contact_details: Dict[str, str] = None


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserting patient data into the database...")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Updating patient data in the database...")

patient_info = {"name": "nitin", 
                "age": "30", 
                "weight": 75.5, 
                "married": True, 
                "allergies": ["pollen", "dust"], 
                "contact_details": {"email": "nitin@example.com", "phone": "1234567890"}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
update_patient_data(patient1)

