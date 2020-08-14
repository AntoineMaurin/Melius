from django.urls import path
from tasks import views

urlpatterns = [
    path('addtask', views.addtask),
    path('deltask/<int:id>', views.deltask),
]
