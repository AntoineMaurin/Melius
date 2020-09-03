from django.urls import path
from matrix import views

urlpatterns = [
    path('coveys_matrix', views.coveys_matrix_page),
    path('covey_sort_backlog/<int:id>', views.covey_sort_backlog),
    path('update_matrix_task', views.update_matrix_task),
    path('retire_task_from_matrix', views.retire_task_from_matrix),
    path('changematrixtaskstate', views.change_matrix_task_state),
]
