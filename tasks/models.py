from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date
from django.db.models import Q


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
    is_important = models.BooleanField(default=None, null=True)
    is_urgent = models.BooleanField(default=None, null=True)
    in_progress = models.BooleanField(default=None, null=True)

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

    def get_overdue_tasks(tasks):
        today = date.today()
        # if the parameter is a container object
        if hasattr(tasks, "__getitem__"):
            list = []
            for task in tasks:
                if task.due_date:
                    if SimpleTask.objects.filter(id=task.id,
                                                 due_date__lt=today,
                                                 is_done=False):
                                                    list.append(task)
            return list
        else:
            return SimpleTask.objects.filter(tasklist=tasks,
                                             due_date__lt=today,
                                             is_done=False)

    def get_today_tasks(tasks):

        today = date.today()

        if hasattr(tasks, "__getitem__"):
            list = []
            for task in tasks:
                if task.due_date:
                    if SimpleTask.objects.filter(id=task.id,
                                                due_date=today,
                                                is_done=False):
                                                    list.append(task)
            return list
        else:
            return SimpleTask.objects.filter(tasklist=tasks, due_date=today,
                                             is_done=False)



    def get_tomorrow_tasks(tasks):
        tomorrow = date.today() + datetime.timedelta(days=1)

        if hasattr(tasks, "__getitem__"):
            list = []
            for task in tasks:
                if task.due_date:
                    if SimpleTask.objects.filter(id=task.id,
                                                due_date=tomorrow,
                                                is_done=False):
                                                    list.append(task)
            return list
        else:
            return SimpleTask.objects.filter(tasklist=tasks, due_date=tomorrow,
                                             is_done=False)

    def get_future_tasks(tasks):
        tomorrow = date.today() + datetime.timedelta(days=1)
        if hasattr(tasks, "__getitem__"):
            list = []
            for task in tasks:
                if task.due_date:
                    if SimpleTask.objects.filter(id=task.id,
                                                due_date__gt=tomorrow,
                                                is_done=False):
                                                    list.append(task)
            return list
        else:
            return SimpleTask.objects.filter(tasklist=tasks,
                                             due_date__gt=tomorrow,
                                             is_done=False)

    def get_no_date_tasks(tasks):

        if hasattr(tasks, "__getitem__"):

            list = []
            for task in tasks:
                if SimpleTask.objects.filter(id=task.id,
                                            due_date=None,
                                            is_done=False):
                                                list.append(task)
            return list


        else:
            return SimpleTask.objects.filter(tasklist=tasks, due_date=None,
                                             is_done=False)


    def get_finished_tasks(tasks):
        if hasattr(tasks, "__getitem__"):

            list = []
            for task in tasks:
                if SimpleTask.objects.filter(id=task.id,
                                            is_done=True):
                                                list.append(task)
            return list

        else:
            return SimpleTask.objects.filter(tasklist=tasks, is_done=True)

    def get_important_urgent_tasks(user):

        return SimpleTask.objects.filter(tasklist__user=user,
                                         is_important=True,
                                         is_urgent=True,
                                         is_done=False)

    def get_important_non_urgent_tasks(user):

        return SimpleTask.objects.filter(tasklist__user=user,
                                         is_important=True,
                                         is_urgent=False,
                                         is_done=False)

    def get_non_important_urgent_tasks(user):

        return SimpleTask.objects.filter(tasklist__user=user,
                                         is_important=False,
                                         is_urgent=True,
                                         is_done=False)

    def get_non_important_non_urgent_tasks(user):

        return SimpleTask.objects.filter(tasklist__user=user,
                                         is_important=False,
                                         is_urgent=False,
                                         is_done=False)

    def get_urgent_tasks(tasks):
        if hasattr(tasks, "__getitem__"):

            list = []
            for task in tasks:
                if SimpleTask.objects.filter(id=task.id,
                                            is_done=False,
                                            is_urgent=True):
                                                list.append(task)
            return list

        else:
            return SimpleTask.objects.filter(tasklist=tasks, is_done=False,
                                             is_urgent=True)

    def get_important_tasks(tasks):
        if hasattr(tasks, "__getitem__"):

            list = []
            for task in tasks:
                if SimpleTask.objects.filter(id=task.id,
                                            is_done=False,
                                            is_important=True):
                                                list.append(task)
            return list

        else:
            return SimpleTask.objects.filter(tasklist=tasks, is_done=False,
                                             is_important=True)

    def get_finished_tasks_not_in_matrix(user):
        return SimpleTask.objects.filter(~Q(is_important__in = ['True', 'False'], is_urgent__in = ['True', 'False']), tasklist__user=user, is_done=False)
