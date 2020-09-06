from django.urls import reverse, resolve
from django.test import TestCase
from matrix.views import coveys_matrix_page, covey_sort_backlog, \
    update_matrix_task, retire_task_from_matrix, change_matrix_task_state
from django.contrib.auth.models import User
from tasks.models import TaskList, SimpleTask
from django.utils import timezone
from datetime import date


class MatrixUrlsTest(TestCase):

    def setUp(self):
        self.add_data()
        self.task_id = SimpleTask.objects.get(name="tâche 1",
                                              description="Description :)").id

        self.tasklist_id = TaskList.objects.get(name="Loisirs",
                                                color="#55b37e").id

    def add_data(self):

        user = User.objects.create_user(username="test@test.com",
                                        password="testpassword")

        tasklist = TaskList.objects.create(user=user, name="Loisirs",
                                           color="#55b37e")

        SimpleTask.objects.create(tasklist=tasklist,
                                  name="tâche 1",
                                  due_date=date.today(),
                                  description="Description :)",
                                  creation=timezone.now(),
                                  is_done=False)

    def test_coveys_matrix_page_url_is_resolved(self):
        url = reverse(coveys_matrix_page)
        self.assertEqual(resolve(url).func, coveys_matrix_page)

    def test_covey_sort_backlog_url_is_resolved(self):
        url = reverse(covey_sort_backlog, args=[self.task_id])
        self.assertEqual(resolve(url).func, covey_sort_backlog)

    def test_update_matrix_task_url_is_resolved(self):
        url = reverse(update_matrix_task)
        self.assertEqual(resolve(url).func, update_matrix_task)

    def test_retire_task_from_matrix_url_is_resolved(self):
        url = reverse(retire_task_from_matrix)
        self.assertEqual(resolve(url).func, retire_task_from_matrix)

    def test_change_matrix_task_state_url_is_resolved(self):
        url = reverse(change_matrix_task_state)
        self.assertEqual(resolve(url).func, change_matrix_task_state)
