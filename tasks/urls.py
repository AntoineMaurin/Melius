from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks', views.tasks_dashboard),
    path('addtask', views.addtask),
    path('addcategory', views.addcategory),
    path('changestate/<int:id>', views.change_task_state),
    path('deltask/<int:id>', views.deltask),
    path('edittask/<int:id>', views.edit_task),
    path('updatetask/<int:id>', views.update_task),
    path('show_tasklist/<int:id>', views.show_tasklist),
    path('sort_by_all/<int:id>', views.sort_by_all),
    path('sort_by_current/<int:id>', views.sort_by_current),
    path('sort_by_finished/<int:id>', views.sort_by_finished),
]
