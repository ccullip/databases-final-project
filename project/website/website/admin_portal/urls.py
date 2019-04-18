from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('patient_data/', views.patient_data, name='patient_data'),
]