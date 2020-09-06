from django.test import TestCase, Client
from django.utils import timezone
import datetime
import random
from datetime import date
from tasks.models import TaskList, SimpleTask
from django.contrib.auth.models import User


class TasksViewsTest(TestCase):

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

    def test_tasks_dashboard(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')

    def test_tasks_dashboard_not_auth(self):
        self.client.get('/logout')
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/tasks')

    def test_tasks_dashboard_tasklist_id(self):
        self.add_data()
        tl = TaskList.objects.create(user=self.user, name="Sport",
                                     color="#333333")
        response = self.client.get('/show_tasklist/' + str(tl.id))
        tasklist_to_show = response.context['tasklist_to_show']
        self.assertEqual(tasklist_to_show.id, tl.id)

    def test_add_task_adds_task(self):

        tl = TaskList.objects.create(user=self.user, name="Sport",
                                     color="#333333")
        self.client.post('/addtask', {
            'name': 'Footing',
            'due_date': date.today(),
            'description': '',
            'tasklists': tl.id,
            'importance': "",
            'emergency': True,
        })

        self.assertTrue(SimpleTask.objects.filter(
            name="Footing", due_date=date.today()).exists()
            )

    def test_add_task_not_auth(self):
        self.client.get('/logout')
        tl = TaskList.objects.create(user=self.user, name="Sport",
                                     color="#333333")
        response = self.client.post('/addtask', {
            'name': 'Footing',
            'due_date': date.today(),
            'description': '',
            'tasklists': tl.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/addtask')

    def test_change_task_state(self):
        self.add_data()
        task = SimpleTask.objects.get(name="tâche 2")
        state_before = task.is_done
        self.client.post('/changestate', {
            'task_id': task.id,
        })
        task_after = SimpleTask.objects.get(id=task.id)
        state_after = task_after.is_done
        self.assertEqual(state_after, not state_before)

    def test_change_task_state_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        SimpleTask.objects.get(name="tâche 2")
        response = self.client.get('/changestate')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/changestate')

    def test_del_task(self):
        self.add_data()
        task = SimpleTask.objects.get(name="tâche 4")
        self.client.post('/deltask', {
            'task_id': task.id,
        })
        is_still_existing = SimpleTask.objects.filter(id=task.id).exists()
        self.assertFalse(is_still_existing)

    def test_del_task_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        task = SimpleTask.objects.get(name="tâche 4")
        response = self.client.post('/deltask', {
            'task_id': task.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/deltask')

    def test_update_task(self):
        self.add_data()
        id = SimpleTask.objects.get(name="tâche 3").id
        self.client.post('/updatetask', {
            'task_id': id,
            'name': 'Handball',
            'due_date': date.today(),
            'description': 'Le lundi et jeudi',
            'tasklists': TaskList.objects.get(name="Loisirs").id,
            'importance': True,
            'emergency': False,
        })

        updated_task = SimpleTask.objects.get(id=id)

        self.assertEqual(updated_task.name, "Handball")
        self.assertEqual(updated_task.description, "Le lundi et jeudi")
        self.assertEqual(updated_task.tasklist.name, "Loisirs")

    def test_update_task_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        id = SimpleTask.objects.get(name="tâche 3").id

        response = self.client.post('/updatetask', {
            'task_id': id,
            'name': 'Handball',
            'due_date': date.today(),
            'description': 'Le lundi et jeudi',
            'tasklists': TaskList.objects.get(name="Loisirs").id
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/updatetask')

    def test_show_tasklist(self):
        self.add_data()
        tasklist = TaskList.objects.get(name="Loisirs")
        response = self.client.get('/show_tasklist/' + str(tasklist.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')

    def test_show_tasklist_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        tasklist = TaskList.objects.get(name="Loisirs")
        response = self.client.get('/show_tasklist/' + str(tasklist.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, ('/login?next=/show_tasklist/'
                                        + str(tasklist.id)))

    def test_show_all_tasklists(self):
        self.add_data()
        response = self.client.get('/show_tasklist/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')

    def test_show_all_tasklists_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        response = self.client.get('/show_tasklist/0')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/show_tasklist/0')

    def test_sort_by_all(self):
        parameters = ['all', 'current', 'finished', 'important', 'urgent']
        for param in parameters:
            response = self.client.get('/sort_by/' + param + '/0')
            self.assertEqual(response.status_code, 200)

    def test_sort_by_all_not_auth(self):
        self.client.get('/logout')
        parameters = ['all', 'current', 'finished', 'important', 'urgent']
        for param in parameters:
            response = self.client.get('/sort_by/' + param + '/0')
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response,
                                 '/login?next=/sort_by/' + param + '/0')

    def test_sort_by_one_tasklist(self):
        self.add_data()
        tasklist = TaskList.objects.get(user=self.user, name="Loisirs",
                                        color="#55b37e")

        parameters = ['all', 'current', 'finished', 'important', 'urgent']
        for param in parameters:
            response = self.client.get('/sort_by/' + param +
                                       '/' + str(tasklist.id))
            self.assertEqual(response.status_code, 200)

    def test_sort_by_one_tasklist_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        tasklist = TaskList.objects.get(user=self.user, name="Loisirs",
                                        color="#55b37e")
        parameters = ['all', 'current', 'finished', 'important', 'urgent']
        for param in parameters:
            response = self.client.get('/sort_by/' + param +
                                       '/' + str(tasklist.id))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, ('/login?next=/sort_by/'
                                            + param + '/' + str(tasklist.id)))

    def test_add_category(self):
        self.add_data()
        self.client.post('/addcategory', {
            'list_name': 'Tâches ménagères',
            'list_color': '#262626',
        })
        self.assertTrue(TaskList.objects.filter(name="Tâches ménagères",
                                                color="#262626",
                                                user=self.user).exists())

    def test_add_category_not_auth(self):
        self.client.get('/logout')
        response = self.client.post('/addcategory', {
            'list_name': 'Tâches ménagères',
            'list_color': '#262626',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/addcategory')

    def test_edit_category(self):
        self.add_data()
        tasklist_to_change = TaskList.objects.get(user=self.user,
                                                  name="Loisirs",
                                                  color="#55b37e")

        self.client.post('/editcategory', {
            'list_id': tasklist_to_change.id,
            'list_name': 'Tâches ménagères',
            'list_color': '#262626',
        })

        list_changed = TaskList.objects.get(id=tasklist_to_change.id)
        self.assertEqual(list_changed.name, "Tâches ménagères")
        self.assertEqual(list_changed.color, "#262626")

    def test_edit_category_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        tasklist_to_change = TaskList.objects.get(name="Loisirs",
                                                  color="#55b37e")

        response = self.client.post('/editcategory', {
            'list_id': tasklist_to_change.id,
            'list_name': 'Tâches ménagères',
            'list_color': '#262626',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/editcategory')

    def test_deletecategory(self):
        self.add_data()
        tasklist_to_del = TaskList.objects.get(user=self.user,
                                               name="Loisirs",
                                               color="#55b37e")

        self.client.post('/deletecategory', {
            'list_id': tasklist_to_del.id,
        })
        existing = TaskList.objects.filter(id=tasklist_to_del.id).exists()
        self.assertFalse(existing)

    def test_deletecategory_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        tasklist_to_del = TaskList.objects.get(name="Loisirs",
                                               color="#55b37e")

        response = self.client.post('/deletecategory', {
            'list_id': tasklist_to_del.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/deletecategory')

    def test_edit_task_not_auth(self):
        self.client.get('/logout')
        self.add_data()
        task_to_edit = SimpleTask.objects.get(name="tâche 1")
        response = self.client.get('/edittask/' + str(task_to_edit.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, ('/login?next=/edittask/'
                                        + str(task_to_edit.id)))
