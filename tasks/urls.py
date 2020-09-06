from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks', views.tasks_dashboard),
    path('addtask', views.addtask),
    path('deltask', views.deltask),
    path('edittask/<int:id>', views.edit_task),
    path('updatetask', views.update_task),
    path('changestate', views.change_task_state),
    path('addcategory', views.addcategory),
    path('editcategory', views.editcategory),
    path('deletecategory', views.deletecategory),
    path('show_tasklist/<int:id>', views.show_tasklist),
    path('sort_by/<str:type>/<int:id>', views.sort_by),
]
