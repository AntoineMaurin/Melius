from django.urls import reverse, resolve
from django.test import TestCase
from tasks import views
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from tasks.models import SimpleTask, TaskList


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
        url = reverse(views.tasks_dashboard)
        self.assertEqual(resolve(url).func, views.tasks_dashboard)

    def test_addtask_url_is_resolved(self):
        url = reverse(views.addtask)
        self.assertEqual(resolve(url).func, views.addtask)

    def test_deltask_url_is_resolved(self):
        url = reverse(views.deltask)
        self.assertEqual(resolve(url).func, views.deltask)

    def test_edit_task_url_is_resolved(self):
        url = reverse(views.edit_task, args=[self.task_id])
        self.assertEqual(resolve(url).func, views.edit_task)

    def test_update_task_url_is_resolved(self):
        url = reverse(views.update_task)
        self.assertEqual(resolve(url).func, views.update_task)

    def test_change_task_state_url_is_resolved(self):
        url = reverse(views.change_task_state)
        self.assertEqual(resolve(url).func, views.change_task_state)

    def test_addcategory_url_is_resolved(self):
        url = reverse(views.addcategory)
        self.assertEqual(resolve(url).func, views.addcategory)

    def test_editcategory_url_is_resolved(self):
        url = reverse(views.editcategory)
        self.assertEqual(resolve(url).func, views.editcategory)

    def test_deletecategory_url_is_resolved(self):
        url = reverse(views.deletecategory)
        self.assertEqual(resolve(url).func, views.deletecategory)

    def test_show_tasklist_url_is_resolved(self):
        url = reverse(views.show_tasklist, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, views.show_tasklist)

    def test_sort_by_all_url_is_resolved(self):
        parameters = ['all', 'current', 'finished', 'important', 'urgent']
        for param in parameters:
            url = reverse(views.sort_by, args=[param, 0])
            self.assertEqual(resolve(url).func, views.sort_by)

    def test_sort_by_tasklist_url_is_resolved(self):
        parameters = ['all', 'current', 'finished', 'important', 'urgent']
        for param in parameters:
            url = reverse(views.sort_by, args=[param, self.tasklist_id])
            self.assertEqual(resolve(url).func, views.sort_by)
