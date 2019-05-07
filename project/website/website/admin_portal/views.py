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
    print(data)
    if data and 'select-patient' not in data and 'select-specific-patient' not in data:
        request.session['data'] = data
        print("select-specific-patient is not in the data")
        print("select-patient is not in the data")
    else:
        if data and 'select-specific-patient' in data and data['select-specific-patient'] == ['Default']:
            data = None

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
    table_field_list = None
    patient_charts = []
    pie = True

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

    if data and len(data) == 1:
        data = None

    if data and 'select-specific-patient' in data:
        print("line 60 ??????????")
        print(data)
        patient_id = data.get('select-specific-patient')
        data, table_field_list, filters = createPreparedStatementForSpecificPatient(cursor, patient_id)
        print(patient_id)
    elif request_data is not None and len(request_data) > 2:
        if(request_data['graphtype'] != 'pie'):
            pie = False
        print("line 66")
        print("hello?")
        print(request_data)
        keys = list(request_data.keys())
        keys.remove(constants.token_name)
        keys.remove(constants.graph_key)

        titles = list(set(constants.titles_options) - set(keys))

        data, table_field_list, filters = createPreparedStatement(cursor, request_data)
        size = len(data)
        zipped_data = list(zip(*data))
        if zipped_data:
            for title in titles:
                value = constants.titles_dict[title]
                print(value)
                if value:
                    datum = list(zipped_data[value])
                    if len(datum) > 1:
                        charts.append(createGraphic(datum, title, pie))
        # ps = "SELECT * FROM Patient WHERE Patient.payer_code != '?' LIMIT 50;"
        # cursor.execute(ps)
        # data = cursor.fetchall()
        # size = len(data)
        # table_field_list = ['patient_id', 'race', 'gender', 'payer_id']

    return render(request, 'home.html',
                  {'data': data, 'table_fields': table_field_list, "size": size,
                  'patient_data': patient_data, 'encounter_data': encounter_data,
                  'encounter_fields': encounter_fields, "filters": filters,
                  "chart": chart, "charts": charts, "patient_charts": patient_charts})


def add(request):
    data = request.POST or None
    print(data)
    successful = False
    patient_id = None
    if data:
        if all(patient_attr in data for patient_attr in ['patientID', 'Gender', 'Race', 'PayerCode']) and 'patientID' != '':
            cursor = connection.cursor()
            patient_id = data['patientID']
            successful = insertNewPatient(cursor, data)
    return render(request, 'add.html',
                  {'data':data, 'successful':successful,'patient_id': patient_id})
