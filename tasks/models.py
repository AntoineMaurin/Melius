from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class TaskList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class SimpleTask(models.Model):
    tasklist = models.ForeignKey(TaskList,
                                 on_delete=models.CASCADE,
                                 default=None)
    name = models.CharField(max_length=150)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(default=None)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.name
