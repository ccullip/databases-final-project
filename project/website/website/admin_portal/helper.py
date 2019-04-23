from .models import Patient

def filter_gender(patients, value):
    return patients.filter(gender=value)

def filter_race(patients, value):
    return patients.filter(race=value)