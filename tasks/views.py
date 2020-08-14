from django.shortcuts import render, redirect
from tasks.models import TaskList, SimpleTask


def addtask(request):
    task_name = request.POST['taskname']
    user_tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    SimpleTask.objects.create(tasklist=user_tasklist, name=task_name)
    return redirect('/tasks')

def deltask(request, id):
    SimpleTask.objects.get(id=id).delete()
    return redirect('/tasks')
