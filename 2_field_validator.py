from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import Dict, List, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    linkedin_url: Optional[AnyUrl] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):

        valid_domains = ["hdfc.com", "icici.com"]
        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        
        return value
    
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

