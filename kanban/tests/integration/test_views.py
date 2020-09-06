from django.test import TestCase, Client
from django.utils import timezone
import datetime
import random
from datetime import date
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User


class KanbanViewsTest(TestCase):

    def add_data(self):

        is_done = (True, False)
        self.tasklist_1 = TaskList.objects.create(user=self.user,
                                                  name="Loisirs",
                                                  color="#55b37e")

        for i in range(5):
            SimpleTask.objects.create(tasklist=self.tasklist_1,
                                      name=str("tâche " + str(i)),
                                      due_date=(date.today() +
                                                datetime.timedelta(days=i)),
                                      description=("Description tâche "
                                                   + str(i)),
                                      creation=timezone.now(),
                                      is_done=random.choice(is_done))

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="test@test.com",
                                             password="testpassword")

        self.client.post('/login', {
            'username': 'test@test.com',
            'password': 'testpassword'
        })

    def tearDown(self):
        self.client.get('/logout')

    def test_kanbanpage(self):
        response = self.client.get('/kanban')
        kanban_keys = ['backlog', 'in_progress', 'finished']
        for key in kanban_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kanban.html')

    def test_kanbanpage_not_auth(self):
        self.client.get('/logout')
        response = self.client.get('/kanban')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/kanban')

    def test_one_category_kanbanpage_tasklist_id(self):
        self.add_data()
        response = self.client.get('/kanban_one_category/' + str(
            self.tasklist_1.id))
        kanban_keys = ['backlog', 'in_progress', 'finished']
        for key in kanban_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kanban.html')

    def test_one_category_kanbanpage_id_zero(self):
        self.add_data()
        response = self.client.get('/kanban_one_category/0')
        kanban_keys = ['backlog', 'in_progress', 'finished']
        for key in kanban_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kanban.html')

    def test_one_category_kanbanpage_tasklist_id_not_auth(self):
        self.add_data()
        self.client.get('/logout')
        response = self.client.get('/kanban_one_category/' + str(
            self.tasklist_1.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/kanban_one_category/' +
            str(self.tasklist_1.id))

    def test_set_in_progress(self):
        self.add_data()
        task = SimpleTask.objects.get(name="tâche 2")
        response = self.client.post('/setinprogress', {
            'task_id': task.id,
            })
        updated_task = SimpleTask.objects.get(id=task.id)
        self.assertTrue(updated_task.in_progress)

    def test_set_in_progress_not_auth(self):
        self.add_data()
        self.client.get('/logout')
        task = SimpleTask.objects.get(name="tâche 2")
        response = self.client.post('/setinprogress', {
            'task_id': task.id,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/setinprogress')

    def test_set_back_in_progress(self):
        self.add_data()
        task = SimpleTask.objects.create(tasklist=self.tasklist_1,
                                         name="finished task",
                                         due_date=date.today(),
                                         description="Tâche terminée.",
                                         creation=timezone.now(),
                                         in_progress=False,
                                         is_done=True)

        response = self.client.post('/setbackinprogress', {
            'task_id': task.id,
            })
        updated_task = SimpleTask.objects.get(id=task.id)
        self.assertTrue(updated_task.in_progress)
        self.assertFalse(updated_task.is_done)

    def test_set_back_in_progress_not_auth(self):
        self.add_data()
        self.client.get('/logout')
        task = SimpleTask.objects.get(name="tâche 2")
        response = self.client.post('/setbackinprogress', {
            'task_id': task.id,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/setbackinprogress')

    def test_cancel_in_progress(self):
        self.add_data()
        task = SimpleTask.objects.create(tasklist=self.tasklist_1,
                                         name="finished task",
                                         due_date=date.today(),
                                         description="Tâche terminée.",
                                         creation=timezone.now(),
                                         is_done=False,
                                         in_progress=True)

        response = self.client.post('/cancelinprogress', {
            'task_id': task.id,
            })
        updated_task = SimpleTask.objects.get(id=task.id)
        self.assertFalse(updated_task.in_progress)
        self.assertFalse(updated_task.is_done)

    def test_cancel_in_progress_not_auth(self):
        self.add_data()
        self.client.get('/logout')
        task = SimpleTask.objects.get(name="tâche 2")
        response = self.client.post('/cancelinprogress', {
            'task_id': task.id,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/cancelinprogress')

    def test_set_finished(self):
        self.add_data()
        task = SimpleTask.objects.create(tasklist=self.tasklist_1,
                                         name="finished task",
                                         due_date=date.today(),
                                         description="Tâche terminée.",
                                         creation=timezone.now(),
                                         is_done=False,
                                         in_progress=True)

        response = self.client.post('/setfinished', {
            'task_id': task.id,
            })
        updated_task = SimpleTask.objects.get(id=task.id)
        self.assertFalse(updated_task.in_progress)
        self.assertTrue(updated_task.is_done)

    def test_set_finished_not_auth(self):
        self.add_data()
        self.client.get('/logout')
        task = SimpleTask.objects.get(name="tâche 2")
        response = self.client.post('/setfinished', {
            'task_id': task.id,
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/setfinished')
