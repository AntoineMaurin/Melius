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
def set_tasks_dict(request, tasks, display='all'):

    user_mail = request.session['user_mail']

    data_dict_obj = BuildTemplateContext(display, tasks)

    data_dict = data_dict_obj.get_data()

    all_tasklists = TaskList.get_tasklists_from_user(user_mail)

    data_dict['all_tasklists'] = all_tasklists

    return data_dict

@login_required
def tasks_dashboard(request, tasklist_to_show_id=None, display='all'):

    user_mail = request.session['user_mail']
    if tasklist_to_show_id:
        tasklist = TaskList.get_tasklist_by_id(id=tasklist_to_show_id)
        tasks = SimpleTask.get_tasks_from_tasklist(tasklist)
    else:
        tasks = SimpleTask.get_all_tasks_by_user(user_mail)

    dict = set_tasks_dict(request, tasks, display)

    if tasklist_to_show_id:
        dict['tasklist_to_show'] = tasklist

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
def change_task_state(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.is_done = not task.is_done
    task.save()
    if 'tasklist_to_show_id' in request.session:
        id = request.session['tasklist_to_show_id']
    else:
        id = None
    return tasks_dashboard(request, tasklist_to_show_id=id)

@login_required
def change_matrix_task_state(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.is_done = not task.is_done
    task.save()
    return coveys_matrix_page(request)

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
    request.session['tasklist_to_show_id'] = 0
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
def sort_by_urgent(request, id):
    if id > 0:
        return tasks_dashboard(request, tasklist_to_show_id=id,
                               display='urgent')
    else:
        return tasks_dashboard(request, tasklist_to_show_id=None,
                                        display='urgent')

@login_required
def sort_by_important(request, id):
    if id > 0:
        return tasks_dashboard(request, tasklist_to_show_id=id,
                               display='important')
    else:
        return tasks_dashboard(request, tasklist_to_show_id=None,
                               display='important')

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

@login_required
def coveys_matrix_page(request):

    user_mail = request.session['user_mail']
    tasks = SimpleTask.get_all_tasks_by_user(user_mail)

    matrix_data = set_tasks_dict(request, tasks, display='matrix')

    full_backlog = SimpleTask.get_finished_tasks_not_in_matrix(tasks)

    final_backlog = set_tasks_dict(request, full_backlog, display='all')

    return render(request, "stephen_covey_matrix.html",
                 {'backlog': final_backlog,
                  'matrix_data': matrix_data})

def covey_one_category_backlog(request, id):
    user_mail = request.session['user_mail']
    tasklist = TaskList.objects.get(id=id)
    tasks_in_tasklist = SimpleTask.get_tasks_from_tasklist(tasklist)

    backlog = SimpleTask.get_finished_tasks_not_in_matrix(tasks_in_tasklist)

    one_category_backlog = set_tasks_dict(request, backlog, display='all')

    all_tasks = SimpleTask.get_all_tasks_by_user(user_mail)

    matrix_data = set_tasks_dict(request, all_tasks, display='matrix')

    return render(request, "stephen_covey_matrix.html",
                 {'backlog': one_category_backlog,
                  'matrix_data': matrix_data})

@login_required
def update_matrix_task(request):
    id = request.POST['task_id']
    dest = request.POST['destination']
    task = SimpleTask.get_task_with_id(id)

    if dest == 'top-left':
        task.is_important = True
        task.is_urgent = True

    elif dest == 'top-right':
        task.is_important = True
        task.is_urgent = False

    elif dest == 'bottom-left':
        task.is_important = False
        task.is_urgent = True

    elif dest == 'bottom-right':
        task.is_important = False
        task.is_urgent = False

    task.save()
    return coveys_matrix_page(request)

@login_required
def retire_task_from_matrix(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.is_important = None
    task.is_urgent = None
    task.save()
    return coveys_matrix_page(request)

@login_required
def kanbanpage(request):
    user = User.objects.get(email=request.session['user_mail'])

    full_backlog = SimpleTask.get_all_undone_tasks_by_user(user)

    in_progress = SimpleTask.objects.filter(tasklist__user=user,
                                            in_progress=True)

    finished = SimpleTask.objects.filter(tasklist__user=user,
                                         in_progress=False,
                                         is_done=True)

    context = {"backlog" : full_backlog,
               "in_progress": in_progress,
               "finished": finished}

    return render(request, "kanban.html", context)

def one_category_kanbanpage(request, id):
    pass

@login_required
def set_in_pogress(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.in_progress = True
    task.save()
    return kanbanpage(request)

@login_required
def set_back_in_progress(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.in_progress = True
    task.is_done = False
    task.save()
    return kanbanpage(request)

@login_required
def cancel_in_progress(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.in_progress = False
    task.save()
    return kanbanpage(request)

@login_required
def set_finished(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.in_progress = False
    task.is_done = True
    task.save()
    return kanbanpage(request)
