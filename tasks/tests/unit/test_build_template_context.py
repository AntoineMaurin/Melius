from django.test import TestCase
from tasks.build_template_context import BuildTemplateContext
from django.contrib.auth.models import User
from tasks.models import TaskList, SimpleTask


class BuildTemplateContextTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username="test@test.com",
                                        email="test@test.com",
                                        password="testpassword")
        self.email = user.email
        tasklist = TaskList.objects.create(user=user, name="Loisirs",
                                           color="#55b37e")

        self.tasks = SimpleTask.objects.filter(tasklist__user=user)

        self.all_keys = ['overdue_tasks', 'due_today_tasks',
                         'due_tommorow_tasks', 'future_tasks', 'no_date_tasks',
                         'finished_tasks', 'all_tasklists', 'tasklist_to_show']

        self.current_keys =  ['overdue_tasks', 'due_today_tasks',
                             'due_tommorow_tasks', 'future_tasks',
                             'no_date_tasks', 'all_tasklists',
                             'tasklist_to_show']

        self.finished_keys = ['finished_tasks', 'all_tasklists',
                              'tasklist_to_show']

        self.urgent_keys = ['urgent_tasks', 'all_tasklists',
                            'tasklist_to_show']

        self.important_keys = ['important_tasks', 'all_tasklists',
                               'tasklist_to_show']

        self.matrix_keys = ['important_urgent', 'important_non_urgent',
                            'non_important_urgent', 'non_important_non_urgent',
                            'matrix_backlog']

    def test_display_all(self):
        test_obj = BuildTemplateContext('all', self.tasks)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.all_keys)

    def test_display_current(self):
        test_obj = BuildTemplateContext('current', self.tasks)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.current_keys)

    def test_display_finished(self):
        test_obj = BuildTemplateContext('finished', self.tasks)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.finished_keys)

    def test_display_urgent(self):
        test_obj = BuildTemplateContext('urgent', self.tasks)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.urgent_keys)

    def test_display_important(self):
        test_obj = BuildTemplateContext('important', self.tasks)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.important_keys)

    def test_display_matrix(self):
        test_obj = BuildTemplateContext('matrix', self.tasks)
        response = test_obj.get_data()
        self.assertTrue(isinstance(response, dict))

        for key in response.keys():
            self.assertTrue(key in self.matrix_keys)
