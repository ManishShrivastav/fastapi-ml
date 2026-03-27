from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities

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
    
    @field_validator("city")
    @classmethod
    def normalize_city(cls, value:str) -> str:
        return value.strip().title()
    
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
