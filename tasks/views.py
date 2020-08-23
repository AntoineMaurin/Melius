from django.shortcuts import render, redirect
from tasks.models import TaskList, SimpleTask
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tasks.utils import *
import datetime

def set_tasks_dict(request, display, tasklist_to_show):

    user_mail = request.session['user_mail']
    all_tasklists = TaskList.get_tasklists_from_user(user_mail)

    overdue_tasks = SimpleTask.get_overdue_tasks_list(tasklist_to_show)
    due_today_tasks = SimpleTask.get_today_tasks_list(tasklist_to_show)
    due_tommorow_tasks = SimpleTask.get_tomorrow_tasks_list(tasklist_to_show)
    future_tasks = SimpleTask.get_future_tasks(tasklist_to_show)
    no_date_tasks = SimpleTask.get_no_date_tasks(tasklist_to_show)
    finished_tasks = SimpleTask.get_finished_tasks(tasklist_to_show)

    all_data = {'overdue_tasks': overdue_tasks,
                'due_today_tasks': due_today_tasks,
                'due_tommorow_tasks': due_tommorow_tasks,
                'future_tasks': future_tasks,
                'no_date_tasks': no_date_tasks,
                'finished_tasks': finished_tasks,
                'all_tasklists': all_tasklists,
                'tasklist_to_show': tasklist_to_show}

    if display == 'all':
        return all_data

    elif display == 'current':
        current = {}
        current_keys = ['overdue_tasks', 'due_today_tasks',
                        'due_tommorow_tasks', 'future_tasks', 'no_date_tasks',
                        'all_tasklists', 'tasklist_to_show']

        for k, v in all_data.items():
            if k in current_keys:
                current[k] = v

        return current

    elif display == 'finished':
        finished = {}
        finished_keys = ['finished_tasks', 'all_tasklists', 'tasklist_to_show']

        for k, v in all_data.items():
            if k in finished_keys:
                finished[k] = v

        return finished

@login_required
def tasks_dashboard(request, tasklist_to_show_id=None,
                    updating_task=None, display='all'):

    if tasklist_to_show_id:
        tasklist_to_show = TaskList.get_tasklist_by_id(id=tasklist_to_show_id)
    else:
        user_mail = request.session['user_mail']
        lists = TaskList.get_tasklists_from_user(user_mail)[:1]
        try:
            tasklist_to_show = lists[0]
        except(IndexError):
            tasklist_to_show = None

    for task in SimpleTask.get_tasks_with_due_date_from_tasklist(tasklist=tasklist_to_show):
        task.due_date = str(task.due_date)

    dict = set_tasks_dict(request, display, tasklist_to_show)

    if updating_task:
        dict['current_updating_task'] = updating_task

    return render(request, "tasks.html", dict)

@login_required
def addtask(request):
    task_name = request.POST['name']
    due_date = request.POST['due_date']
    description = request.POST['description']
    tasklist_id = request.POST['tasklists']

    user_tasklist = TaskList.get_tasklist_by_id(id=tasklist_id)

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

def change_task_state(request, id):
    task = SimpleTask.get_task_with_id(id)
    task.is_done = not task.is_done
    task.save()
    return redirect('/tasks')

@login_required
def deltask(request, id):
    SimpleTask.get_task_with_id(id).delete()
    return JsonResponse({'task_id': id})

@login_required
def update_task(request, id):
    task = SimpleTask.get_task_with_id(id)
    task.name = request.POST['name']
    task.due_date = request.POST['due_date']

    if len(str(task.due_date)) > 5:
        task.due_date_clean_display = convert_to_clean_date(task.due_date)
        task.due_date = convert_into_date_type(str(task.due_date))
    else:
        task.due_date = None
        task.due_date_clean_display = None

    task.description = request.POST['description']
    new_category_id = request.POST['tasklists']
    new_tasklist = TaskList.get_tasklist_by_id(new_category_id)
    task.tasklist = new_tasklist
    task.save()
    return redirect('/tasks')

def show_tasklist(request, id):
    return tasks_dashboard(request, tasklist_to_show_id=id)

def sort_tasklist(request):
    type_sort = request.POST.get('type_sort')
    if not type_sort:
        type_sort = 'all'

    return tasks_dashboard(request, tasklist_to_show_id=tasklist_id,
                     display=type_sort)

def sort_by_all(request, id):
    return tasks_dashboard(request, tasklist_to_show_id=id,
                     display='all')

def sort_by_current(request, id):
    return tasks_dashboard(request, tasklist_to_show_id=id,
                    display='current')

def sort_by_finished(request, id):
    return tasks_dashboard(request, tasklist_to_show_id=id,
                    display='finished')


def addcategory(request):
    list_name = request.POST['list_name']
    list_color = request.POST['list_color']
    user = User.objects.get(email=request.session['user_mail'])

    TaskList.objects.create(name=list_name, user=user, color=list_color)
    return redirect('/tasks')

def editcategory(request):
    list_id = request.POST['list_id']
    tasklist_to_edit = TaskList.get_tasklist_by_id(id=list_id)

    new_list_name = request.POST['list_name']
    new_list_color = request.POST['list_color']

    tasklist_to_edit.name = new_list_name
    tasklist_to_edit.color = new_list_color
    tasklist_to_edit.save()
    return redirect('/tasks')

def deletecategory(request):
    list_id = request.POST['list_id']
    tasklist_to_edit = TaskList.get_tasklist_by_id(id=list_id)
    tasklist_to_edit.delete()
    return redirect('/tasks')

def edit_task(request, id):
    task = SimpleTask.get_task_with_id(id=id)
    data = {"task_name": task.name,
            "task_id": task.id,
            "category_name": task.tasklist.name,
            "category_color": task.tasklist.color,
            "due_date": task.due_date,
            "description": task.description}
    return JsonResponse(data)
