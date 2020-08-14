from django.contrib import admin
from tasks.models import SimpleTask, TaskList


admin.site.register(SimpleTask)
admin.site.register(TaskList)
