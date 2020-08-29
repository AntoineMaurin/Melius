from django.urls import reverse, resolve
from django.test import TestCase
from tasks.views import *
from django.utils import timezone
from datetime import date


class TasksUrlsTest(TestCase):

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

    def test_tasks_dashboard_url_is_resolved(self):
        url = reverse(tasks_dashboard)
        self.assertEqual(resolve(url).func, tasks_dashboard)

    def test_addtask_url_is_resolved(self):
        url = reverse(addtask)
        self.assertEqual(resolve(url).func, addtask)

    def test_deltask_url_is_resolved(self):
        url = reverse(deltask, args=[self.task_id])
        self.assertEqual(resolve(url).func, deltask)

    def test_edit_task_url_is_resolved(self):
        url = reverse(edit_task, args=[self.task_id])
        self.assertEqual(resolve(url).func, edit_task)

    def test_update_task_url_is_resolved(self):
        url = reverse(update_task)
        self.assertEqual(resolve(url).func, update_task)

    def test_change_task_state_url_is_resolved(self):
        url = reverse(change_task_state, args=[self.task_id])
        self.assertEqual(resolve(url).func, change_task_state)

    def test_addcategory_url_is_resolved(self):
        url = reverse(addcategory)
        self.assertEqual(resolve(url).func, addcategory)

    def test_editcategory_url_is_resolved(self):
        url = reverse(editcategory)
        self.assertEqual(resolve(url).func, editcategory)

    def test_deletecategory_url_is_resolved(self):
        url = reverse(deletecategory)
        self.assertEqual(resolve(url).func, deletecategory)

    def test_show_tasklist_url_is_resolved(self):
        url = reverse(show_tasklist, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, show_tasklist)

    def test_show_all_tasklists_url_is_resolved(self):
        url = reverse(show_all_tasklists)
        self.assertEqual(resolve(url).func, show_all_tasklists)

    def test_sort_by_all_url_is_resolved(self):
        url = reverse(sort_by_all, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, sort_by_all)

    def test_sort_by_current_url_is_resolved(self):
        url = reverse(sort_by_current, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, sort_by_current)

    def test_sort_by_finished_url_is_resolved(self):
        url = reverse(sort_by_finished, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, sort_by_finished)

    def test_sort_by_urgent_url_is_resolved(self):
        url = reverse(sort_by_urgent, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, sort_by_urgent)

    def test_sort_by_important_url_is_resolved(self):
        url = reverse(sort_by_important, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, sort_by_important)

    def test_coveys_matrix_page_url_is_resolved(self):
        url = reverse(coveys_matrix_page)
        self.assertEqual(resolve(url).func, coveys_matrix_page)

    def test_update_matrix_task_url_is_resolved(self):
        url = reverse(update_matrix_task)
        self.assertEqual(resolve(url).func, update_matrix_task)
