from django.urls import path
from tasks import views

urlpatterns = [
    path('addtask', views.addtask),
    path('deltask/<int:id>', views.deltask),
    path('updatetask/<int:id>', views.update_task),
    path('edittask/<int:id>', views.edit_task),
]
