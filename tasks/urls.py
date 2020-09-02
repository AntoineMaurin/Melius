from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks', views.tasks_dashboard),
    path('addtask', views.addtask),
    path('deltask', views.deltask),
    path('edittask/<int:id>', views.edit_task),
    path('updatetask', views.update_task),
    path('changestate', views.change_task_state),
    path('changematrixtaskstate', views.change_matrix_task_state),
    path('addcategory', views.addcategory),
    path('editcategory', views.editcategory),
    path('deletecategory', views.deletecategory),
    path('show_tasklist/<int:id>', views.show_tasklist),
    path('sort_by/<str:type>/<int:id>', views.sort_by),
    path('coveys_matrix', views.coveys_matrix_page),
    path('covey_sort_backlog/<int:id>', views.covey_sort_backlog),
    path('update_matrix_task', views.update_matrix_task),
    path('retire_task_from_matrix', views.retire_task_from_matrix),
    path('kanban', views.kanbanpage),
    path('setinprogress', views.set_in_progress),
    path('setbackinprogress', views.set_back_in_progress),
    path('cancelinprogress', views.cancel_in_progress),
    path('setfinished', views.set_finished),
    path('kanban_one_category/<int:id>', views.one_category_kanbanpage),
]
