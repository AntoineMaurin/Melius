from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User
import datetime
from datetime import date


def homepage(request):
    return render(request, "home.html")

@login_required
def dashboardpage(request):
    user = User.objects.get(email=request.session['user_mail'])
    all_tasks = SimpleTask.get_all_tasks_by_user(user).count()
    done_tasks = SimpleTask.get_all_done_tasks_by_user(user).count()

    today = date.today()
    next_week = today + datetime.timedelta(days=7)

    today_done_tasks = SimpleTask.objects.filter(tasklist__user=user,
                                                 due_date=today,
                                                 is_done=True).count()

    today_total_tasks = SimpleTask.objects.filter(tasklist__user=user,
                                                  due_date=today).count()

    total_until_next_week = SimpleTask.objects.filter(tasklist__user=user,
                                                      due_date__range=(today, next_week)).count()

    done_for_next_week = SimpleTask.objects.filter(tasklist__user=user,
                                                   is_done=True,
                                                   due_date__range=(today, next_week)).count()

    context = {'all_tasks': all_tasks,
               'done_tasks': done_tasks,
               'today_done_tasks': today_done_tasks,
               'today_total_tasks': today_total_tasks,
               'total_until_next_week': total_until_next_week,
               'done_for_next_week': done_for_next_week}

    return render(request, "dashboard.html", context)
