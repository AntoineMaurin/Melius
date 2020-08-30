from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks', views.tasks_dashboard),
    path('addtask', views.addtask),
    path('deltask/<int:id>', views.deltask),
    path('edittask/<int:id>', views.edit_task),
    path('updatetask', views.update_task),
    path('changestate', views.change_task_state),
    path('changematrixtaskstate', views.change_matrix_task_state),
    path('addcategory', views.addcategory),
    path('editcategory', views.editcategory),
    path('deletecategory', views.deletecategory),
    path('show_tasklist/<int:id>', views.show_tasklist),
    path('show_all_tasklists', views.show_all_tasklists),
    path('sort_by_all/<int:id>', views.sort_by_all),
    path('sort_by_current/<int:id>', views.sort_by_current),
    path('sort_by_finished/<int:id>', views.sort_by_finished),
    path('sort_by_urgent/<int:id>', views.sort_by_urgent),
    path('sort_by_important/<int:id>', views.sort_by_important),
    path('coveys_matrix', views.coveys_matrix_page),
    path('update_matrix_task', views.update_matrix_task),
    path('retire_task_from_matrix', views.retire_task_from_matrix),
    path('kanban', views.kanbanpage),
]
