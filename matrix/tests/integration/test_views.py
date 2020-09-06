from django.test import TestCase, Client
from django.utils import timezone
import datetime
import random
from datetime import date
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User


class MatrixViewsTest(TestCase):

    def add_data(self):

        is_done = (True, False)
        tasklist_1 = TaskList.objects.create(user=self.user, name="Loisirs",
                                             color="#55b37e")

        for i in range(5):
            SimpleTask.objects.create(tasklist=tasklist_1,
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

    def test_coveys_matrix_page(self):
        response = self.client.get('/coveys_matrix')
        coveys_keys = ['backlog', 'matrix_data']
        for key in coveys_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stephen_covey_matrix.html')

    def test_coveys_matrix_page_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        response = self.client.get('/coveys_matrix')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/coveys_matrix')

    def test_covey_sort_backlog(self):
        self.add_data()
        tasklist = TaskList.objects.get(name='Loisirs')
        response = self.client.get('/covey_sort_backlog/' + str(tasklist.id))
        coveys_keys = ['backlog', 'matrix_data']
        for key in coveys_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stephen_covey_matrix.html')

    def test_covey_sort_backlog_with_random_id(self):
        self.add_data()
        response = self.client.get('/covey_sort_backlog/564314')
        coveys_keys = ['backlog', 'matrix_data']
        for key in coveys_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stephen_covey_matrix.html')

    def test_covey_sort_backlog_with_zero_id(self):
        self.add_data()
        response = self.client.get('/covey_sort_backlog/0')
        coveys_keys = ['backlog', 'matrix_data']
        for key in coveys_keys:
            self.assertIn(key, response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stephen_covey_matrix.html')

    def test_update_matrix_task(self):
        self.add_data()
        task_to_update = SimpleTask.objects.get(name="tâche 1")

        response = self.client.post('/update_matrix_task', {
            'task_id': task_to_update.id,
            'destination': 'top-right'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stephen_covey_matrix.html')

    def test_update_matrix_task_updates_task(self):
        self.add_data()
        task_to_update = SimpleTask.objects.get(name="tâche 1")

        self.client.post('/update_matrix_task', {
            'task_id': task_to_update.id,
            'destination': 'top-right'
        })
        updated_task = SimpleTask.objects.get(id=task_to_update.id)

        self.assertTrue(updated_task.is_important)
        self.assertFalse(updated_task.is_urgent)

    def test_update_matrix_task_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        task_to_update = SimpleTask.objects.get(name="tâche 1")

        response = self.client.post('/update_matrix_task', {
            'task_id': task_to_update.id,
            'destination': 'top-right'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/update_matrix_task')

    def test_retire_task_from_matrix(self):
        self.add_data()
        task = SimpleTask.objects.get(name="tâche 4")
        task.is_urgent = True
        task.is_important = False
        task.save()
        self.client.post('/retire_task_from_matrix', {
            'task_id': task.id,
        })
        updated_task = SimpleTask.objects.get(id=task.id)
        self.assertEquals(updated_task.is_urgent, None)
        self.assertEquals(updated_task.is_important, None)

    def test_retire_task_from_matrix_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        task = SimpleTask.objects.get(tasklist__user=self.user,
                                      name="tâche 4")
        response = self.client.post('/retire_task_from_matrix', {
            'task_id': task.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/retire_task_from_matrix')
