from django.urls import path
from kanban import views

urlpatterns = [
    path('kanban', views.kanbanpage),
    path('setinprogress', views.set_in_progress),
    path('setbackinprogress', views.set_back_in_progress),
    path('cancelinprogress', views.cancel_in_progress),
    path('setfinished', views.set_finished),
    path('kanban_one_category/<int:id>', views.one_category_kanbanpage),
]
