from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import TaskList, SimpleTask
from tasks.forms import SimpleTaskForm


def homepage(request):
    return render(request, "home.html")

@login_required
def taskspage(request):
    form = SimpleTaskForm()
    name = request.session['user_name']
    tasklist = TaskList.objects.get(user__email=request.session['user_mail'])
    tasks = reversed(SimpleTask.objects.filter(tasklist=tasklist))

    return render(request, "tasks.html", {'tasks': tasks, 'form': form})
