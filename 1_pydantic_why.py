def insert_patient_data(name: str, age: int):

    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("Inserting patient data into the database...")
    else:
        print("Invalid input types. Please provide a string for name and an integer for age.")

def update_patient_data(name: str, age: int):

    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("Updating patient data in the database...")
    else:
        print("Invalid input types. Please provide a string for name and an integer for age.")

insert_patient_data("Ananya Verma", 30)
update_patient_data("Ananya Verma", 30)

