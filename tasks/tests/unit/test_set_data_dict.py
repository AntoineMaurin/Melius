from django.test import TestCase
from tasks.set_data_dict import SetDataDict
from django.contrib.auth.models import User
from tasks.models import TaskList


class SetDataDictTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="test@test.com",
                                        email="test@test.com",
                                        password="testpassword")
        self.email = user.email
        self.tasklist = TaskList.objects.create(user=user, name="Loisirs",
                                                color="#55b37e")

        self.all_keys = ['overdue_tasks', 'due_today_tasks',
                         'due_tommorow_tasks', 'future_tasks', 'no_date_tasks',
                         'finished_tasks', 'all_tasklists', 'tasklist_to_show']

        self.current_keys =  ['overdue_tasks', 'due_today_tasks',
                             'due_tommorow_tasks', 'future_tasks',
                             'no_date_tasks', 'all_tasklists',
                             'tasklist_to_show']

        self.finished_keys = ['finished_tasks', 'all_tasklists',
                              'tasklist_to_show']

    def test_display_all(self):
        test_obj = SetDataDict('all', self.tasklist, self.email)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.all_keys)

    def test_display_all_no_tasklist(self):
        test_obj = SetDataDict('all', None, self.email)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.all_keys)

    def test_display_current(self):
        test_obj = SetDataDict('current', self.tasklist, self.email)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.current_keys)

    def test_display_current_no_tasklist(self):
        test_obj = SetDataDict('current', None, self.email)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.current_keys)

    def test_display_finished(self):
        test_obj = SetDataDict('finished', self.tasklist, self.email)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.finished_keys)

    def test_display_finished_no_tasklist(self):
        test_obj = SetDataDict('finished', None, self.email)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.finished_keys)
