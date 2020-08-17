from django.shortcuts import render, redirect
from tasks.models import TaskList, SimpleTask
from tasks.forms import SimpleTaskForm


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
                              description=description)
    return redirect('/tasks')

def deltask(request, id):
    SimpleTask.objects.get(id=id).delete()
    return redirect('/tasks')

def update_task(request, id):
    task = SimpleTask.objects.get(id=id)
    tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    tasks = reversed(SimpleTask.objects.filter(tasklist=tasklist))
    return render(request, "tasks.html", {'task': task, 'tasks': tasks})

def edit_task(request, id):
    task = SimpleTask.objects.get(id=id)
    task.name = request.POST['name']
    task.due_date = request.POST['due_date']
    task.description = request.POST['description']
    task.save()
    return redirect('/tasks')
