from django.shortcuts import render, HttpResponse

# create views here
def home(request):
	return render(request, 'home.html')