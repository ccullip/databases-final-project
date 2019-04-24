from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient, Has
from .forms import FilterForm
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

    request.session['data'] = data

    return render(request, 'home.html')

# def graphics(request);
#     return render(request, 'graphics.html')


def table(request):
    request_data = request.session.pop('data')
    data = request_data #Patient.objects.filter(gender="Female").values()
    field_list = ['patient_id', 'race', 'gender', 'payer_id']
    values = []
    size = 0
    if request_data is not None:
        field_list = ['Patient Id', 'Race', 'Gender']
        keys = request_data.keys()
        cursor = connection.cursor()
        select_ps = "SELECT Patient.patient_id, Patient.race, Patient.gender"
        from_ps = "FROM Patient"
        where_ps = "WHERE "
        joins = {"Encounter": False,
                 "Medication": False,
                 "Vitals": False,
                 "Source": False,
                 "Discharge": False}
        for key in keys:
            print("[" + key + "]")
            if key == "Gender":
                value = request_data.get(key)
                values.append(value + " ")
                where_ps += "Patient.gender = '" + value + "'"
            elif key == "Race":
                value = request_data.get(key)
                values.append(value + " ")
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Patient.race = '" + value + "'"
            elif key == "Age":
                value = request_data.get(key)
                values.append(value + " ")
                field_list.append('Age')
                joins["Encounter"] = True
                # add to select statement
                select_ps += ", Encounter.age"
                # add to where statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Encounter.age = '" + value + "'"
            elif key == "Medication":
                value = request_data.get(key)
                values.append(value + " ")
                field_list.append('Medication')
                joins["Encounter"] = True
                joins["Medication"] = True
                # add to select statement
                select_ps += ", Medication.med_name"
                # add to from statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Medication.med_name = '" + value + "'"
            elif key == "a1c_result":
                value = request_data.get(key)
                values.append(value + " ")
                field_list.append("A1c Result")
                joins["Encounter"] = True
                joins["Vitals"] = True
                # add to select statement
                select_ps += ", Vitals.a1c_result"
                # add to from statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Vitals.a1c_result = '" + value + "'"
            elif key == "glucose_result":
                value = request_data.get(key)
                values.append(value + " ")
                field_list.append("Glucose Result")
                joins["Encounter"] = True
                joins["Vitals"] = True
                # add to select statement
                select_ps += ", Vitals.glucose_result"
                # add to from statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Vitals.glucose_result = '" + value + "'"
            elif key == "source_id":
                value = request_data.get(key)
                values.append(value + " ")
                field_list.append("Admission Source")
                joins["Encounter"] = True
                joins["Source"] = True
                # add to select statement
                select_ps += ", Source.source_name"
                # add to from statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Source.source_id = '" + value + "'"
            elif key == "discharge_id":
                value = request_data.get(key)
                values.append(value + " ")
                field_list.append("Discharge Destination")
                joins["Encounter"] = True
                joins["Discharge"] = True
                # add to select statement
                select_ps += ", Discharge.discharge_name"
                # add to from statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Discharge.discharge_id = '" + value + "'"

        if joins["Encounter"]:
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Encounter.encounter_id = Has.encounter_id AND Has.patient_id = Patient.patient_id "
            from_ps += ", Has, Encounter"
        if joins["Medication"]:
            where_ps += "AND Medication.med_name = Prescribes.med_name AND Prescribes.encounter_id = Encounter.encounter_id "
            from_ps += ", Prescribes, Medication"
        if joins["Vitals"]:
            where_ps += "AND Vitals.encounter_id = Encounter.encounter_id "
            from_ps += ", Vitals"
        if joins["Source"]:
            where_ps += "AND Source.source_id = GetsPatientFrom.source_id AND GetsPatientFrom.encounter_id = Encounter.encounter_id "
            from_ps += ", Source, GetsPatientFrom "
        if joins["Discharge"]:
            where_ps += "AND Discharge.discharge_id = SendsPatientTo.discharge_id AND SendsPatientTo.discharge_id = Encounter.encounter_id "
            from_ps += ", Discharge, SendsPatientTo "

        ps = select_ps + " " + from_ps + " " + where_ps + ";"
        # print(ps)
        cursor.execute(ps)
        data = cursor.fetchall()
        size = len(data)
    print(data)
    print(field_list)

    return render(request, 'table.html', {'data': data, 'fields': field_list,'filters': values, "size": size})

def patient_data(request):
    data = Patient.objects.get(patient_id=7128)
    return HttpResponse(data)

def filter(request):
    print(request.POST)
    FilterFormSet = modelformset_factory(FilterForm)
    data = request.POST or None
    formset = FilterFormSet(data=data, queryset=FilterForm.objects.filter(user=request.user))
    for form in formset:
        form.fields['category'].queryset
    if request.method == "POST" and form.is_valid():
        return HttpResponse("hello")

    return render('home.html', {'form': form}, RequestContext(request))
