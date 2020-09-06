from django.shortcuts import render, redirect
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from tasks.build_template_context import BuildTemplateContext


@login_required
def kanbanpage(request, tasklist_to_show_id=None):
    user_mail = request.session['user_mail']

    if tasklist_to_show_id:
        tasklist = TaskList.objects.get(id=tasklist_to_show_id)
        tasks = SimpleTask.get_tasks_from_tasklist(tasklist)
    else:
        tasks = SimpleTask.get_all_tasks_by_user(user_mail)

    initial_backlog = SimpleTask.get_kanban_backlog_tasks(tasks)

    data_dict_obj = BuildTemplateContext('all', initial_backlog)

    final_backlog = data_dict_obj.get_data()

    all_tasklists = TaskList.get_tasklists_from_user(user_mail)

    final_backlog['all_tasklists'] = all_tasklists

    in_progress = SimpleTask.objects.filter(tasklist__user__email=user_mail,
                                            in_progress=True)

    finished = SimpleTask.objects.filter(tasklist__user__email=user_mail,
                                         in_progress=False,
                                         is_done=True)

    context = {"backlog": final_backlog,
               "in_progress": in_progress,
               "finished": finished}

    return render(request, "kanban.html", context)


@login_required
def one_category_kanbanpage(request, id):
    user_mail = request.session['user_mail']
    if id == 0:
        return kanbanpage(request, tasklist_to_show_id=None)

    try:
        tasklist = TaskList.objects.get(id=id)

        if tasklist in TaskList.get_tasklists_from_user(user_mail):
            return kanbanpage(request, tasklist_to_show_id=id)
        else:
            return kanbanpage(request, tasklist_to_show_id=None)
    except(ObjectDoesNotExist):
        return kanbanpage(request, tasklist_to_show_id=None)


@login_required
def set_in_progress(request):
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
