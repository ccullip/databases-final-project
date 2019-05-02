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
    encounter_fields = []
    encounter_data = []
    filters = []

    if data and 'select-patient' in data:
        print('entered')
        patient_id = data.get('select-patient')
        encounter_fields = ['Encounter ID', 'Age', 'A1c Result', 'Glucose Result', '# of lab procedures',
                            '# of medications', 'Admission type', 'Duration (days)', 'Readmitted?',
                            'Diagnosis 1', 'Diagnosis 2', 'Diagnosis 3', 'Medication']
        ps = "select encounter_id, age, a1c_result, glucose_result, num_lab_procedures, num_medications, admiss_type, duration, readmitted, " \
             "diag_1, diag_2, diag_3, " \
             "group_concat(Medicine SEPARATOR ', ') as Medicines " \
             "FROM (" \
             "SELECT encounter_id, age, a1c_result, glucose_result, num_lab_procedures, num_medications, admiss_type, duration, readmitted, " \
             "max(CASE WHEN priority = '1' THEN diag_name ELSE NULL END) as diag_1, " \
             "max(CASE WHEN priority = '2' THEN diag_name ELSE NULL END) as diag_2, " \
             "max(CASE WHEN priority = '3' THEN diag_name ELSE NULL END) as diag_3, " \
             "concat(med_name, ': ', dosage_change) as Medicine " \
             "FROM (SELECT encounter.encounter_id, icd_code, priority, diag_name, med_name, dosage_change, " \
             "age, a1c_result, glucose_result, num_lab_procedures, num_medications, admiss_type, duration, readmitted " \
             "FROM patient natural join has natural join encounter natural join diagnoses natural join diagnosis natural join vitals " \
             "LEFT JOIN prescribes on encounter.encounter_id = prescribes.encounter_id " \
             "WHERE patient_id = " + patient_id + ") as subsub " \
             "GROUP BY encounter_id) as sub " \
             "GROUP BY encounter_id;"
        cursor.execute(ps)
        encounter_data = cursor.fetchall()
        patient_cols = "patient_id, race, gender, payer_code"
        ps = "SELECT " + patient_cols + " FROM Patient WHERE Patient.patient_id = " + patient_id + ";"
        cursor.execute(ps)
        patient_data = cursor.fetchall()
    if request_data is not None and len(request_data) > 1:
        data, table_field_list, filters = createPreparedStatement(cursor, request_data)
        size = len(data)
    else:
        ps = "SELECT * FROM Patient WHERE Patient.payer_code != '?' LIMIT 50;"
        cursor.execute(ps)
        data = cursor.fetchall()
        size = len(data)
        table_field_list = ['patient_id', 'race', 'gender', 'payer_id']
    return render(request, 'home.html',
                  {'data': data, 'table_fields': table_field_list, "size": size, 'patient_data': patient_data, 'encounter_data': encounter_data,
                   'encounter_fields': encounter_fields, "filters": filters})

# def graphics(request);
#     return render(request, 'graphics.html')

def add(request):
    data = request.POST or None
    print(data)
    return render(request, 'add.html')
