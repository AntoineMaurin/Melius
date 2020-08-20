from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, default=None, null=True)

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
