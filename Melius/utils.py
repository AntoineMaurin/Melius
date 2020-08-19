from tasks.models import TaskList, SimpleTask
import datetime

def convert_to_clean_date(due_date):
    if isinstance(due_date, str):
        due_date = convert_into_date_type(due_date)
    return due_date.strftime("%d %b")

def is_due_today(due_date):
    return due_date == datetime.date.today()

def is_due_tomorrow(due_date):
    return due_date == datetime.date.today() + datetime.timedelta(days=1)

def is_overdue(due_date):
    return due_date < datetime.date.today()

def is_for_future(due_date):
    return due_date > datetime.date.today() + datetime.timedelta(days=2)

def convert_into_date_type(str_date):
     return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()

def get_overdue_tasks_list(tasklist):
    overdue_tasks = []
    tasks = SimpleTask.objects.filter(
                                      tasklist=tasklist, is_done=False
                                      ).exclude(
                                                due_date=None
                                      ).order_by('creation')
    for task in tasks:
        if is_overdue(task.due_date):
            overdue_tasks.append(task)
    return overdue_tasks

def get_today_tasks_list(tasklist):
    today_tasks = []
    tasks = SimpleTask.objects.filter(
                                      tasklist=tasklist, is_done=False
                                      ).exclude(
                                                due_date=None
                                      ).order_by('creation')
    for task in tasks:
        if is_due_today(task.due_date):
            today_tasks.append(task)
    return today_tasks

def get_tomorrow_tasks_list(tasklist):
    tomorrow_tasks = []
    tasks = SimpleTask.objects.filter(
                                      tasklist=tasklist, is_done=False
                                      ).exclude(
                                                due_date=None
                                      ).order_by('creation')
    for task in tasks:
        if is_due_tomorrow(task.due_date):
            tomorrow_tasks.append(task)
    return tomorrow_tasks

def get_future_tasks(tasklist):
    future_tasks = []
    tasks = SimpleTask.objects.filter(
                                      tasklist=tasklist, is_done=False
                                      ).exclude(
                                                due_date=None
                                      ).order_by('creation')
    for task in tasks:
        if is_for_future(task.due_date):
            future_tasks.append(task)
    return future_tasks

def get_no_date_tasks(tasklist):
    no_date_tasks = []
    tasks = SimpleTask.objects.filter(
                                      tasklist=tasklist, due_date=None,
                                      is_done=False
                                      ).order_by('creation')
    for task in tasks:
        no_date_tasks.append(task)
    return no_date_tasks

def get_finished_tasks(tasklist):
    finished_tasks = []
    tasks = SimpleTask.objects.filter(
                                      tasklist=tasklist, is_done=True
                                      ).order_by('creation')
    for task in tasks:
        finished_tasks.append(task)
    return finished_tasks
