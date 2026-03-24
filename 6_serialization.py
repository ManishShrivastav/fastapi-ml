from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    gender: str = 'Male'
    age: int
    address: Address


address_dict = {"city": "New York", "state": "NY", "zip_code": "10001"}

address1 = Address(**address_dict)

patient_dict = {"name": "John Doe", "age": 30, "address": address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude={"name": True, "age": True, "address": {"zip_code": True}}, exclude_unset=True)

print(temp)
print(type(temp))