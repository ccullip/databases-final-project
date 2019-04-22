from .models import Patient

def filter_gender(patients, value):
    return patients.filter(gender=value)
