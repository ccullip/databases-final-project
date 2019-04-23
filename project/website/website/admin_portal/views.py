from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient, Has
from .forms import FilterForm
from django.template import RequestContext
from django.forms import modelformset_factory
from .helper import *
from django.db import connection, transaction


# Create your views here.

def index(request):
    return HttpResponse('Hello, welcome to the index page.')

def home(request):
    data = request.POST or None

    request.session['data'] = data

    return render(request, 'home.html')

def table(request):
    request_data = request.session.pop('data')
    data = Patient.objects.filter(gender="Female").values()
    field_list = ['patient_id', 'race', 'gender', 'payer_id']
    if request_data is not None:
        field_list = ['patient_id', 'race', 'gender']
        keys = request_data.keys()
        cursor = connection.cursor()
        select_ps = "SELECT Patient.patient_id, Patient.race, Patient.gender"
        from_ps = "FROM Patient"
        where_ps = "WHERE "
        joins = {"Encounter": False}
        for key in keys:
            if key == "Gender":
                value = request_data.get(key)
                where_ps += "Patient.gender = '" + value + "'"
            elif key == "Race":
                value = request_data.get(key)
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Patient.race = '" + value + "'"
            elif key == "Age":
                value = request_data.get(key)
                field_list.append('age')
                joins["Encounter"] = True
                # add to select statement
                select_ps += ", Encounter.age"
                # add to where statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Encounter.age = '" + value + "'"
            elif key == "Medication":
                value = request_data.get(key)
                field_list.append('medication')
                joins["Encounter"] = True
                joins["Medication"] = True
                # add to select statement
                select_ps += ", Medication.med_name"
                # add to from statement
                if where_ps != "WHERE ":
                    where_ps += " AND "
                where_ps += "Medication.med_name = '" + value + "'"

        if joins["Encounter"]:
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Encounter.encounter_id = Has.encounter_id AND Has.patient_id = Patient.patient_id "
            from_ps += ", Has, Encounter"
        if joins["Medication"]:
            where_ps += "AND Medication.med_name = Prescribes.med_name AND Prescribes.encounter_id = Encounter.encounter_id "
            from_ps += ", Prescribes, Medication"

        ps = select_ps + " " + from_ps + " " + where_ps + ";"
        print(ps)
        cursor.execute(ps)
        data = cursor.fetchall()
        print(data)
    return render(request, 'table.html', {'data': data, 'fields': field_list})

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
