from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import TaskList, SimpleTask
from tasks.build_template_context import BuildTemplateContext
from django.core.exceptions import ObjectDoesNotExist


@login_required
def coveys_matrix_page(request, tasklist_to_show_id=None):
    user_mail = request.session['user_mail']

    if tasklist_to_show_id:
        tasklist = TaskList.objects.get(id=tasklist_to_show_id)
        tasks = SimpleTask.get_tasks_from_tasklist(tasklist)
    else:
        tasks = SimpleTask.get_all_tasks_by_user(user_mail)

    backlog_tasks = SimpleTask.get_matrix_backlog_tasks(tasks)

    backlog_obj = BuildTemplateContext('all', backlog_tasks)
    final_backlog = backlog_obj.get_data()

    all_user_tasks = SimpleTask.get_all_tasks_by_user(user_mail)

    matrix_obj = BuildTemplateContext('matrix', all_user_tasks)
    matrix_data = matrix_obj.get_data()

    all_tasklists = TaskList.get_tasklists_from_user(user_mail)

    final_backlog['all_tasklists'] = all_tasklists

    return render(request, "stephen_covey_matrix.html",
                           {'backlog': final_backlog,
                            'matrix_data': matrix_data})


def covey_sort_backlog(request, id):

    user_mail = request.session['user_mail']

    if id == 0:
        return coveys_matrix_page(request, tasklist_to_show_id=None)

    try:
        tasklist = TaskList.objects.get(id=id)

        if tasklist in TaskList.get_tasklists_from_user(user_mail):
            return coveys_matrix_page(request, tasklist_to_show_id=id)
        else:
            return coveys_matrix_page(request, tasklist_to_show_id=None)
    except(ObjectDoesNotExist):
        return coveys_matrix_page(request, tasklist_to_show_id=None)


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
def change_matrix_task_state(request):
    id = request.POST['task_id']
    task = SimpleTask.get_task_with_id(id)
    task.is_done = not task.is_done
    task.save()
    return coveys_matrix_page(request)
