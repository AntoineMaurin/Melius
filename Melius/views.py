from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User


def homepage(request):
    return render(request, "home.html")

@login_required
def dashboardpage(request):
    user_mail = request.session['user_mail']
    user = User.objects.get(email=user_mail)
    all_tasks = SimpleTask.get_all_tasks_by_user(user).count()
    done_tasks = SimpleTask.get_all_done_tasks_by_user(user).count()
    not_done_tasks = SimpleTask.get_all_undone_tasks_by_user(user).count()
    context = {'all_tasks': all_tasks,
               'done_tasks': done_tasks,
               'not_done_tasks': not_done_tasks,}
    return render(request, "dashboard.html", context)
