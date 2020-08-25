from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks', views.tasks_dashboard),
    path('addtask', views.addtask),
    path('deltask/<int:id>', views.deltask),
    path('edittask/<int:id>', views.edit_task),
    path('updatetask', views.update_task),
    path('changestate/<int:id>', views.change_task_state),
    path('addcategory', views.addcategory),
    path('editcategory', views.editcategory),
    path('deletecategory', views.deletecategory),
    path('show_tasklist/<int:id>', views.show_tasklist),
    path('show_all_tasklists', views.show_all_tasklists),
    path('sort_by_all/<int:id>', views.sort_by_all),
    path('sort_by_current/<int:id>', views.sort_by_current),
    path('sort_by_finished/<int:id>', views.sort_by_finished),
]
