from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def homepage(request):
    return render(request, "home.html")

def taskspage(request):
    return render(request, "tasks.html")

def zerodivision(request):
    division_by_zero = 1 / 0
