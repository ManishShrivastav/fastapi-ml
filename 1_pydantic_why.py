from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import Dict, List, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Patient Name", description="The name of the patient in less than 50 characters", example="John Doe")]
    email: EmailStr
    linkedin_url: Optional[AnyUrl] = None
    age: int = Field(..., gt=0, lt=120, description="Age must be a positive integer between 1 and 119")
    weight: Annotated[float, Field(gt=0, strict=True, description="Weight must be a positive number")]
    married: Annotated[bool, Field(default=None, description="Indicates if the patient is married")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5, description="List of allergies (max 5 items)")]
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

