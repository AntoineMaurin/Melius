from django.shortcuts import render, redirect
from tasks.models import TaskList, SimpleTask
from tasks.forms import SimpleTaskForm
import datetime
from Melius.utils import *


def addtask(request):
    task_name = request.POST['name']
    due_date = request.POST['due_date']
    # due_date = convert_into_date_type(due_date)
    description = request.POST['description']
    user_tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    if not due_date:
        due_date = None
    task = SimpleTask(tasklist=user_tasklist,
                      name=task_name,
                      due_date=due_date,
                      description=description,
                      creation=datetime.datetime.now())
    if task.due_date:
        task.due_date_clean_display = convert_to_clean_date(task.due_date)

    task.save()
    return redirect('/tasks')

def donetask(request, id):
    done_task = SimpleTask.objects.get(id=id)
    done_task.is_done = True
    done_task.save()
    return redirect('/tasks')

def undonetask(request, id):
    undone_task = SimpleTask.objects.get(id=id)
    undone_task.is_done = False
    undone_task.save()
    return redirect('/tasks')

def deltask(request, id):
    SimpleTask.objects.get(id=id).delete()
    return redirect('/tasks')

def open_update_form(request, id):
    current_updating_task = SimpleTask.objects.get(id=id)
    current_updating_task.due_date = str(current_updating_task.due_date)
    tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    tasks = SimpleTask.objects.filter(tasklist=tasklist).order_by('creation')
    return render(request, "tasks.html",
                  {'tasks': tasks,
                   'current_updating_task': current_updating_task})

def edit_task(request, id):
    task = SimpleTask.objects.get(id=id)
    task.name = request.POST['name']

    if task.due_date:
        task.due_date_clean_display = convert_to_clean_date(task.due_date)

    task.description = request.POST['description']
    task.save()
    return redirect('/tasks')
