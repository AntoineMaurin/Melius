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

    for task in SimpleTask.objects.filter(tasklist=tasklist):
        task.due_date = str(task.due_date)

    overdue_tasks = get_overdue_tasks_list(tasklist)
    due_today_tasks = get_today_tasks_list(tasklist)
    due_tommorow_tasks = get_tomorrow_tasks_list(tasklist)
    future_tasks = get_future_tasks(tasklist)
    no_date_tasks = get_no_date_tasks(tasklist)
    finished_tasks = get_finished_tasks(tasklist)


    return render(request, "tasks.html",
                 {'overdue_tasks': overdue_tasks,
                  'due_today_tasks': due_today_tasks,
                  'due_tommorow_tasks': due_tommorow_tasks,
                  'future_tasks': future_tasks,
                  'no_date_tasks': no_date_tasks,
                  'finished_tasks': finished_tasks})
