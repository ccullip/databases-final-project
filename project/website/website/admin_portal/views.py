from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient

# Create your views here.

def index(request):
    return HttpResponse('Hello, welcome to the index page.')


def patient_data(request):
    data = Patient.objects.get(patient_id=7128)
    return HttpResponse(data)
