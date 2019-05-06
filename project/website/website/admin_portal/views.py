from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient, Has
from django.template import RequestContext
from django.forms import modelformset_factory
from .helper import *
from django.db import connection, transaction
from . import constants
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
    encounter_fields = []
    encounter_data = []
    filters = []
    chart = None
    charts = []

    if data and 'select-patient' in data:
        print('entered')
        patient_id = data.get('select-patient')
        encounter_fields = constants.encounter_fields
        ps = constants.createGiantPreparedStatement(patient_id)
        cursor.execute(ps)
        encounter_data = cursor.fetchall()
        patient_cols = "patient_id, race, gender, payer_code"
        ps = "SELECT " + patient_cols + " FROM Patient WHERE Patient.patient_id = " + patient_id + ";"
        cursor.execute(ps)
        patient_data = cursor.fetchall()
    if request_data is not None and len(request_data) > 1:
        print("hello!")
        print("--------------------")
        print(request_data)
        keys = list(request_data.keys())
        keys.remove(constants.token_name)
        print(keys)
        print()
        # print(list(request_data.keys()).remove(constants.token_name))
        print("--------------------")
        data, table_field_list, filters = createPreparedStatement(cursor, request_data)
        size = len(data)
        print(size)
        print(data)
        idk = list(zip(*data))
        idk = idk[1:]

        print(idk)
        print("-----")

        print(len(idk))
        print()
        print(table_field_list)
        print(filters)
        chart = createPieChart()
        # print(data)
    else:
        ps = "SELECT * FROM Patient WHERE Patient.payer_code != '?' LIMIT 50;"
        cursor.execute(ps)
        data = cursor.fetchall()
        size = len(data)
        table_field_list = ['patient_id', 'race', 'gender', 'payer_id']
    return render(request, 'home.html',
                  {'data': data, 'table_fields': table_field_list, "size": size, 'patient_data': patient_data, 'encounter_data': encounter_data,
                   'encounter_fields': encounter_fields, "filters": filters, "chart": chart})


def add(request):
    data = request.POST or None
    print(data)
    cursor = connection.cursor()
    return render(request, 'add.html')
