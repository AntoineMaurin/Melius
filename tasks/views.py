from django.shortcuts import render, redirect
from django.utils import timezone
from tasks.models import TaskList, SimpleTask
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tasks.utils import *
import datetime
from tasks.build_template_context import BuildTemplateContext


@login_required
def set_tasks_dict(request, display, tasklist_to_show):

    user_mail = request.session['user_mail']
    data_dict_obj = BuildTemplateContext(display, tasklist_to_show, user_mail)
    data_dict = data_dict_obj.get_data()

    return data_dict

@login_required
def tasks_dashboard(request, tasklist_to_show_id=None, display='all'):

    if tasklist_to_show_id:
        tasklist_to_show = TaskList.get_tasklist_by_id(id=tasklist_to_show_id)

        for task in SimpleTask.get_tasks_with_due_date_from_tasklist(tasklist=tasklist_to_show):
            task.due_date = str(task.due_date)

        dict = set_tasks_dict(request, display, tasklist_to_show)

    else:
        dict = set_tasks_dict(request, display, tasklist_to_show_id)

    return render(request, "tasks.html", dict)

@login_required
def addtask(request):
    task_name = request.POST['name']
    due_date = request.POST['due_date']
    description = request.POST['description']
    tasklist_id = request.POST['tasklists']
    importance = request.POST['importance']
    emergency = request.POST['emergency']

    user_tasklist = TaskList.get_tasklist_by_id(id=tasklist_id)

    if not due_date:
        due_date = None
    task = SimpleTask(tasklist=user_tasklist,
                      name=task_name,
                      due_date=due_date,
                      description=description,
                      creation=timezone.now(),
                      is_important=importance,
                      is_urgent=emergency)
    if task.due_date:
        task.due_date_clean_display = convert_to_clean_date(task.due_date)

    task.save()
    return tasks_dashboard(request, tasklist_to_show_id=user_tasklist.id)

@login_required
def change_task_state(request, id):
    task = SimpleTask.get_task_with_id(id)
    task.is_done = not task.is_done
    task.save()
    return tasks_dashboard(request, tasklist_to_show_id=task.tasklist.id)
    # return redirect("/tasks")

@login_required
def deltask(request, id):
    SimpleTask.get_task_with_id(id).delete()
    return JsonResponse({'task_id': id})

@login_required
def update_task(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.name = request.POST['name']
    task.due_date = request.POST['due_date']
    task.is_important = request.POST['importance']
    task.is_urgent = request.POST['emergency']

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
    return tasks_dashboard(request, tasklist_to_show_id=new_tasklist.id)

@login_required
def show_tasklist(request, id):
    return tasks_dashboard(request, tasklist_to_show_id=id)

@login_required
def show_all_tasklists(request):
    return tasks_dashboard(request, tasklist_to_show_id=None)


@login_required
def sort_by_all(request, id):
    if id > 0:
        return tasks_dashboard(request, tasklist_to_show_id=id,
                        display='all')
    else:
        return tasks_dashboard(request, tasklist_to_show_id=None,
                        display='all')

@login_required
def sort_by_current(request, id):
    if id > 0:
        return tasks_dashboard(request, tasklist_to_show_id=id,
                        display='current')
    else:
        return tasks_dashboard(request, tasklist_to_show_id=None,
                        display='current')

@login_required
def sort_by_finished(request, id):
    if id > 0:
        return tasks_dashboard(request, tasklist_to_show_id=id,
                        display='finished')
    else:
        return tasks_dashboard(request, tasklist_to_show_id=None,
                        display='finished')

@login_required
def addcategory(request):
    list_name = request.POST['list_name']
    list_color = request.POST['list_color']
    user = User.objects.get(email=request.session['user_mail'])

    tl = TaskList.objects.create(name=list_name, user=user, color=list_color)

    return tasks_dashboard(request, tasklist_to_show_id=tl.id)

@login_required
def editcategory(request):
    list_id = request.POST['list_id']
    tasklist_to_edit = TaskList.get_tasklist_by_id(id=list_id)

    new_list_name = request.POST['list_name']
    new_list_color = request.POST['list_color']

    tasklist_to_edit.name = new_list_name
    tasklist_to_edit.color = new_list_color
    tasklist_to_edit.save()
    return redirect('/tasks')

@login_required
def deletecategory(request):
    list_id = request.POST['list_id']
    tasklist_to_edit = TaskList.get_tasklist_by_id(id=list_id)
    tasklist_to_edit.delete()
    return redirect('/tasks')

@login_required
def edit_task(request, id):
    task = SimpleTask.get_task_with_id(id=id)
    data = {"task_name": task.name,
            "task_id": task.id,
            "category_name": task.tasklist.name,
            "category_color": task.tasklist.color,
            "due_date": task.due_date,
            "description": task.description}
    return JsonResponse(data)

def coveys_matrix_page(request):
    user = User.objects.get(email=request.session['user_mail'])

    important_urgent = SimpleTask.get_important_urgent_tasks(user)

    important_non_urgent = SimpleTask.get_important_non_urgent_tasks(user)

    non_important_urgent = SimpleTask.get_non_important_urgent_tasks(user)

    non_important_non_urgent = SimpleTask.get_non_important_non_urgent_tasks(user)

    context = {'important_urgent': important_urgent,
               'important_non_urgent': important_non_urgent,
               'non_important_urgent': non_important_urgent,
               'non_important_non_urgent': non_important_non_urgent}

    return render(request, "stephen_covey_matrix.html", context)
