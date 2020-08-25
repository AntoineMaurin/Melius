from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='Sans nom', null=True)
    color = models.CharField(max_length=30, default='#21756b')

    def __str__(self):
        return self.name

    def get_tasklists_from_user(user_mail):
        return TaskList.objects.filter(user__email=user_mail)

    def get_tasklist_by_id(id=id):
        return TaskList.objects.get(id=id)

class SimpleTask(models.Model):
    tasklist = models.ForeignKey(TaskList,
                                 on_delete=models.CASCADE,
                                 default=None)
    name = models.CharField(max_length=150)
    due_date = models.DateField(null=True, blank=True)
    due_date_clean_display = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(default=None)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_all_tasks_by_user(user):
        return SimpleTask.objects.filter(tasklist__user=user)

    def get_all_done_tasks_by_user(user):
        return SimpleTask.objects.filter(tasklist__user=user, is_done=True)

    def get_all_undone_tasks_by_user(user):
        return SimpleTask.objects.filter(tasklist__user=user, is_done=False)

    def get_tasks_with_due_date_from_tasklist(tasklist):
        return SimpleTask.objects.filter(tasklist=tasklist).exclude(due_date=None)

    def get_task_with_id(id):
        return SimpleTask.objects.get(id=id)

    def get_overdue_tasks_list(tasklist):
        today = date.today()
        return SimpleTask.objects.filter(tasklist=tasklist, due_date__lt=today,
                                         is_done=False)

    def get_today_tasks_list(tasklist):
        today = date.today()
        return SimpleTask.objects.filter(tasklist=tasklist, due_date=today,
                                         is_done=False)

    def get_tomorrow_tasks_list(tasklist):
        tomorrow = date.today() + datetime.timedelta(days=1)
        return SimpleTask.objects.filter(tasklist=tasklist, due_date=tomorrow,
                                         is_done=False)

    def get_future_tasks(tasklist):
        tomorrow = date.today() + datetime.timedelta(days=1)
        return SimpleTask.objects.filter(tasklist=tasklist,
                                         due_date__gt=tomorrow,
                                         is_done=False)

    def get_no_date_tasks(tasklist):
         return SimpleTask.objects.filter(tasklist=tasklist, due_date=None,
                                          is_done=False)

    def get_finished_tasks(tasklist):
        return SimpleTask.objects.filter(tasklist=tasklist, is_done=True)

    def get_overdue_tasks(tasks):
        today = date.today()
        list = []
        for task in tasks:
            if task.due_date:
                if SimpleTask.objects.filter(id=task.id, due_date__lt=today,
                                             is_done=False):
                                                list.append(task)
        return list

    def get_due_today_tasks(tasks):
        today = date.today()
        list = []
        for task in tasks:
            if task.due_date:
                if SimpleTask.objects.filter(id=task.id, due_date=today,
                                             is_done=False):
                                                list.append(task)
        return list

    def get_due_tomorrow_tasks(tasks):
        tomorrow = date.today() + datetime.timedelta(days=1)
        list = []
        for task in tasks:
            if task.due_date:
                if SimpleTask.objects.filter(id=task.id, due_date=tomorrow,
                                             is_done=False):
                                                list.append(task)
        return list

    def get_upcoming_tasks(tasks):
        tomorrow = date.today() + datetime.timedelta(days=1)
        list = []
        for task in tasks:
            if task.due_date:
                if SimpleTask.objects.filter(id=task.id, due_date__gt=tomorrow,
                                             is_done=False):
                                                list.append(task)
        return list

    def get_no_due_date_tasks(tasks):
        list = []
        for task in tasks:
            if SimpleTask.objects.filter(id=task.id, due_date=None,
                                         is_done=False):
                                            list.append(task)
        return list

    def get_completed_tasks(tasks):
        list = []
        for task in tasks:
            if SimpleTask.objects.filter(id=task.id, is_done=True):
                list.append(task)
        return list
