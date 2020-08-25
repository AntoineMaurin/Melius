from django.test import TestCase, Client
from django.utils import timezone
import datetime
import random
from datetime import date
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User
from tasks.views import *

class TasksViewsTest(TestCase):

    # def add_data(self):
    #
    #     is_done = (True, False)
    #
    #     tasklist_1 = TaskList.objects.create(user=user, name="Loisirs",
    #                                          color="#55b37e")
    #
    #     tasklist_2 = TaskList.objects.create(user=user, name="Travail",
    #                                          color="#ffad10")
    #
    #     for i in range(5):
    #         SimpleTask.objects.create(tasklist=tasklist_1,
    #                                   name=str("tâche " + str(i)),
    #                                   due_date=date.today() + datetime.timedelta(days=i),
    #                                   description=str("Description tâche " + str(i)),
    #                                   creation=timezone.now(),
    #                                   is_done=random.choice(is_done))
    #
    #     for j in range(5):
    #         SimpleTask.objects.create(tasklist=tasklist_2,
    #                                   name=str("tâche " + str(j)),
    #                                   due_date=date.today() + datetime.timedelta(days=j),
    #                                   description=str("Description tâche " + str(j)),
    #                                   creation=timezone.now(),
    #                                   is_done=random.choice(is_done))
    #
    #     print("data added !")

    def add_data(self):

        user = User.objects.create_user(username="test@test.com",
                                        password="testpassword")

        is_done = (True, False)
        tasklist_1 = TaskList.objects.create(user=user, name="Loisirs",
                                             color="#55b37e")

        for i in range(5):
            SimpleTask.objects.create(tasklist=tasklist_1,
                                      name=str("tâche " + str(i)),
                                      due_date=date.today() + datetime.timedelta(days=i),
                                      description="Description tâche " + str(i),
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

    def test_tasks_dashboard_not_auth(self):
        self.client.get('/logout')
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/tasks')

    def test_tasks_dashboard_auth(self):

        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')

    def test_add_task(self):
        # self.add_data()

        tl = TaskList.objects.create(user=self.user, name="Sport",
                                     color="#333333")
        response = self.client.post('/addtask', {
            'name': 'Footing',
            'due_date': date.today(),
            'description': '',
            'tasklists': tl.id
        })

        self.assertTrue(SimpleTask.objects.filter(
            name="Footing", due_date=date.today()).exists()
            )


    # def test_change_task_state(self):
    #     response = self.client.get('/changestate/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')
    #     self.failUnless(isinstance(response.context['form'], UserLoginForm))
    #
    #
    #
    # def test_register_get(self):
    #     response = self.client.get('/register')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'register.html')
    #     self.failUnless(isinstance(response.context['form'], UserRegisterForm))
    #
    # def test_logout_get(self):
    #     response = self.client.get('/logout')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/login')
    #
    # def test_register_success(self):
    #     response = self.client.post('/register', {
    #         'email': 'thetest@test.com',
    #         'pw1': 'testtest',
    #         'pw2': 'testtest'
    #     })
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertRedirects(response, '/login')
    #
    # def test_register_fails(self):
    #     response = self.client.post('/register', {
    #         'email': 'anothertest@test.com',
    #         'pw1': 'testtest',
    #         'pw2': 'wrongconfirm'
    #     })
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(User.objects.count(), 0)
    #     self.assertTemplateUsed(response, 'register.html')
    #     self.failUnless(isinstance(response.context['form'], UserRegisterForm))
    #
    # def test_login_success_post(self):
    #
    #     user = User.objects.create_user(username='test@test.com',
    #                                     email='test@test.com',
    #                                     password='testtest')
    #
    #     response = self.client.post('/login', {
    #         'username': 'test@test.com',
    #         'password': 'testtest'
    #     })
    #
    #     TaskList.objects.create(user=user)
    #     #
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, '/tasks')
    #
    #     user = auth.get_user(self.client)
    #     self.assertEquals(user.is_authenticated, True)
    #
    # def test_login_fails(self):
    #     user = User.objects.create_user(username='test@test.com',
    #                                     email='test@test.com',
    #                                     password='testtest')
    #
    #     response = self.client.post('/login', {
    #         'username': 'test@test.com',
    #         'password': 'wrongpassword'
    #     })
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')
    #
    #     user = auth.get_user(self.client)
    #     self.assertFalse(user.is_authenticated)
    #
    # def test_logout(self):
    #     """Creates account, connect, and disconnect to check the efficiency of
    #     the logout view"""
    #
    #     user = User.objects.create_user(username='test@test.com',
    #                                     email='test@test.com',
    #                                     password='testtest')
    #
    #     TaskList.objects.create(user=user)
    #
    #     self.client.post('/login', {
    #         'username': 'test@test.com',
    #         'password': 'testtest'
    #     })
    #
    #     user = auth.get_user(self.client)
    #     self.assertTrue(user.is_authenticated)
    #
    #     response = self.client.get('/logout')
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, '/login')
    #
    #     disconnected_user = auth.get_user(self.client)
    #     self.assertFalse(disconnected_user.is_authenticated)
