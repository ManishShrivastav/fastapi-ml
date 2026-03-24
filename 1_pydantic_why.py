from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import Dict, List, Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: Optional[AnyUrl] = None
    age: int
    weight: float = None
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    contact_details: Optional[Dict[str, str]] = None


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("Inserting patient data into the database...")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Updating patient data in the database...")

patient_info = {"name": "nitin", 
                'email': "abc@gmail.com",
                "age": "30", 
                "weight": 75.5, 
                "married": True, 
                "allergies": ["pollen", "dust"], 
                "contact_details": {"email": "nitin@example.com", "phone": "1234567890"},
                "linkedin_url": "https://www.linkedin.com/in/nitin"}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
update_patient_data(patient1)

