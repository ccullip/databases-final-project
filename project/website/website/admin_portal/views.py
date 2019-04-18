from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient

# Create your views here.

def index(request):
    return HttpResponse('Hello, welcome to the index page.')

def home(request):
    return render(request, 'home.html')

def table(request):
    patients = Patient.objects.filter(gender="Female").values()
    fields = Patient._meta.concrete_fields
    field_list = []
    for field in fields:
        field_list.append(field.name)
    return render(request, 'table.html', {'patients': patients, 'fields': field_list})

def patient_data(request):
    data = Patient.objects.get(patient_id=7128)
    return HttpResponse(data)
