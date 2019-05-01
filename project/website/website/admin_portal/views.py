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
    request.session.flush()
    return HttpResponse('Hello, welcome to the index page.')

def home(request):
    data = request.POST or None
    if data and 'select-patient' not in data:
        request.session['data'] = data
        print(data)

    if 'data' in request.session.keys():
        request_data = request.session.get('data')
        print(request_data)
    else:
        request_data = None
    size = 0
    cursor = connection.cursor()
    patient_data = []
    patient_fields = []
    filters = []


    if data and 'select-patient' in data:
        print('entered')
        patient_id = data.get('select-patient')
        ps = "SELECT * FROM Patient natural join Has natural join Encounter WHERE Patient.patient_id = " + patient_id + ";"
        print(ps)
        cursor.execute(ps)
        patient_data = cursor.fetchall()
        print(patient_data)
        patient_fields = ['Encounter ID', 'Patient ID', 'Race', 'Gender', 'Payer Code', '# of lab procedures',
                          '# of medications', 'Admission type', 'Duration (days)', 'Age', 'Readmitted?']
        print(patient_fields)
    if request_data is not None:
        print(request_data)
        print(request_data.keys)
        data, table_field_list, filters = createPreparedStatement(cursor, request_data)
        size = len(data)
    else:
        ps = "SELECT * FROM Patient WHERE Patient.payer_code != '?' LIMIT 100;"
        cursor.execute(ps)
        data = cursor.fetchall()
        size = len(data)
        table_field_list = ['patient_id', 'race', 'gender', 'payer_id']
    print(patient_fields)
    return render(request, 'home.html',
                  {'data': data, 'table_fields': table_field_list, "size": size, 'patient_data': patient_data,
                   'patient_fields': patient_fields, "filters": filters})

# def graphics(request);
#     return render(request, 'graphics.html')

def patient_data(request):
    data = Patient.objects.get(patient_id=7128)
    return HttpResponse(data)
