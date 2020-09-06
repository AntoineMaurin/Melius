from django.urls import reverse, resolve
from django.test import TestCase
from kanban.views import kanbanpage, one_category_kanbanpage, \
    set_in_progress, set_back_in_progress, cancel_in_progress, set_finished
from django.contrib.auth.models import User
from tasks.models import TaskList, SimpleTask
from django.utils import timezone
from datetime import date


class KanbanUrlsTest(TestCase):

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

    def test_kanban_page_url_is_resolved(self):
        url = reverse(kanbanpage)
        self.assertEqual(resolve(url).func, kanbanpage)

    def test_one_category_kanban_page_url_is_resolved(self):
        url = reverse(one_category_kanbanpage, args=[self.tasklist_id])
        self.assertEqual(resolve(url).func, one_category_kanbanpage)

    def test_one_category_kanban_page_id_zero_url_is_resolved(self):
        url = reverse(one_category_kanbanpage, args=[0])
        self.assertEqual(resolve(url).func, one_category_kanbanpage)

    def test_set_in_progress_url_is_resolved(self):
        url = reverse(set_in_progress)
        self.assertEqual(resolve(url).func, set_in_progress)

    def test_set_back_in_progress_url_is_resolved(self):
        url = reverse(set_back_in_progress)
        self.assertEqual(resolve(url).func, set_back_in_progress)

    def test_cancel_in_progress_url_is_resolved(self):
        url = reverse(cancel_in_progress)
        self.assertEqual(resolve(url).func, cancel_in_progress)

    def test_set_finished_url_is_resolved(self):
        url = reverse(set_finished)
        self.assertEqual(resolve(url).func, set_finished)
