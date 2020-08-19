from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import TaskList, SimpleTask
from tasks.forms import SimpleTaskForm
from Melius.utils import *


def homepage(request):
    return render(request, "home.html")

@login_required
def taskspage(request):
    form = SimpleTaskForm()
    name = request.session['user_name']
    tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    tasks = SimpleTask.objects.filter(tasklist=tasklist).order_by('creation')

    for task in tasks:
        task.due_date = str(task.due_date)
        
    # overdue_tasks
    # due_today_tasks
    # due_tommorow_tasks
    # future_tasks
    # finished_tasks

    return render(request, "tasks.html",
                 {'tasks': tasks,
                  'form': form})
