from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('home/table.html', views.table, name='table'),
    path('patient_data/', views.patient_data, name='patient_data'),
]