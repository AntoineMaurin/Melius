from django.shortcuts import render, redirect
from tasks.models import TaskList, SimpleTask
from tasks.forms import SimpleTaskForm
from datetime import datetime


def addtask(request):
    task_name = request.POST['name']
    due_date = request.POST['due_date']
    description = request.POST['description']
    user_tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    if not due_date:
        due_date = None
    SimpleTask.objects.create(tasklist=user_tasklist,
                              name=task_name,
                              due_date=due_date,
                              description=description,
                              creation=datetime.now())
    return redirect('/tasks')

def deltask(request, id):
    SimpleTask.objects.get(id=id).delete()
    return redirect('/tasks')

def open_update_form(request, id):
    current_updating_task = SimpleTask.objects.get(id=id)
    tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    tasks = SimpleTask.objects.filter(tasklist=tasklist).order_by('creation')
    return render(request, "tasks.html",
                  {'tasks': tasks,
                   'current_updating_task': current_updating_task})

def edit_task(request, id):
    task = SimpleTask.objects.get(id=id)
    task.name = request.POST['name']
    task.due_date = request.POST['due_date']
    if not task.due_date:
        task.due_date = None
    task.description = request.POST['description']
    task.save()
    return redirect('/tasks')
