from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import TaskList, SimpleTask
from Melius.utils import *


def homepage(request):
    return render(request, "home.html")
