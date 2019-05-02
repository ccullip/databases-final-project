from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('home/graphics.html', views.home, name='graphics'),
    path('add/', views.add, name='add')
]
