from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient
from .forms import FilterForm
from django.template import RequestContext
from django.forms import modelformset_factory
from .helper import *

# Create your views here.

def index(request):
    return HttpResponse('Hello, welcome to the index page.')

def home(request):
    data = request.POST or None
    request.session['data'] = data

    return render(request, 'home.html')

def table(request):
    data = request.session.pop('data')
    print(data)
    patient_list = Patient.objects.filter(gender="Female").values()
    fields = Patient._meta.concrete_fields
    field_list = []
    for field in fields:
        field_list.append(field.name)
    if data is not None:
        keys = data.keys()
        key_list = []
        patients = Patient.objects
        for key in keys:
            if key == "Gender":
                value = data.get(key)
                patients = filter_gender(patients, value)
        patient_list = patients.values()
    return render(request, 'table.html', {'patients': patient_list, 'fields': field_list})

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
