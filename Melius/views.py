from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import TaskList, SimpleTask


def homepage(request):
    return render(request, "home.html")
