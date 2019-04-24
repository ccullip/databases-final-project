from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient, Has
from django.template import RequestContext
from django.forms import modelformset_factory
from .helper import *
from django.db import connection, transaction
# from . import FusionCharts


# Create your views here.

def index(request):
    return HttpResponse('Hello, welcome to the index page.')

def home(request):
    data = request.POST or None

    if data:
        request.session['data'] = data

    return render(request, 'home.html')

# def graphics(request);
#     return render(request, 'graphics.html')


def table(request):
    size = 0
    cursor = connection.cursor()
    patient_data = []
    patient_fields = []
    filters = []
    if 'data' in request.session.keys():
        request_data = request.session.get('data')
        print(request_data)
    else:
        request_data = None
    keys = request.POST.keys()
    print(keys)
    if 'select-patient' in keys:
        patient_id = request.POST.get('select-patient')
        ps = "SELECT * FROM Patient, Has, Encounter " \
                     "WHERE Patient.patient_id = Has.patient_id AND Has.encounter_id = Encounter.encounter_id AND Patient.patient_id = " + patient_id + ";"
        print(ps)
        cursor.execute(ps)
        patient_data = cursor.fetchall()
        print(patient_data)
        patient_fields = ['patient_id', 'race', 'gender', 'payer_id', 'encounter_id', 'num_lab_procedures', 'num_medications', 'admiss_type', 'duration', 'age', 'readmitted']

    if request_data is not None and len(request_data.keys()) > 1:
        data, table_field_list, filters = createPreparedStatement(cursor, request_data)
        size = len(data)
    else:
        ps = "SELECT Patient.patient_id, Patient.race, Patient.gender, Patient.payer_code FROM Patient WHERE Patient.payer_code != '?' LIMIT 100;"
        cursor.execute(ps)
        data = cursor.fetchall()
        size = len(data)
        table_field_list = ['patient_id', 'race', 'gender', 'payer_id']
    return render(request, 'table.html', {'data': data, 'table_fields': table_field_list, "size": size, 'patient_data': patient_data, 'patient_fields': patient_fields, "filters": filters})

def patient_data(request):
    data = Patient.objects.get(patient_id=7128)
    return HttpResponse(data)
