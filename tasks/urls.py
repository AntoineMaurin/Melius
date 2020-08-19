from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks', views.taskspage),
    path('addtask', views.addtask),
    path('changestate/<int:id>', views.change_task_state),
    path('deltask/<int:id>', views.deltask),
    path('edittask/<int:id>', views.edit_task),
    path('updatetask/<int:id>', views.update_task),
]
