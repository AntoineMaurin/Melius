from django.urls import path
from tasks import views

urlpatterns = [
    path('addtask', views.addtask),
    path('deltask/<int:id>', views.deltask),
    path('updateform/<int:id>', views.open_update_form),
    path('edittask/<int:id>', views.edit_task),
]
