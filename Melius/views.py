from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def taskspage(request):
    return render(request, "tasks.html")
