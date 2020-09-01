# from django.test import TestCase
# from tasks.build_template_context import BuildTemplateContext
# from django.contrib.auth.models import User
# from tasks.models import TaskList
#
#
# class BuildTemplateContextTest(TestCase):
#
#     def setUp(self):
#         user = User.objects.create_user(username="test@test.com",
#                                         email="test@test.com",
#                                         password="testpassword")
#         self.email = user.email
#         self.tasklist = TaskList.objects.create(user=user, name="Loisirs",
#                                                 color="#55b37e")
#
#         self.all_keys = ['overdue_tasks', 'due_today_tasks',
#                          'due_tommorow_tasks', 'future_tasks', 'no_date_tasks',
#                          'finished_tasks', 'all_tasklists', 'tasklist_to_show']
#
#         self.current_keys =  ['overdue_tasks', 'due_today_tasks',
#                              'due_tommorow_tasks', 'future_tasks',
#                              'no_date_tasks', 'all_tasklists',
#                              'tasklist_to_show']
#
#         self.finished_keys = ['finished_tasks', 'all_tasklists',
#                               'tasklist_to_show']
#
#         self.urgent_keys = ['urgent_tasks', 'all_tasklists',
#                             'tasklist_to_show']
#
#         self.important_keys = ['important_tasks', 'all_tasklists',
#                                'tasklist_to_show']
#
#
#     def test_display_all(self):
#         test_obj = BuildTemplateContext('all', self.tasklist, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.all_keys)
#
#     def test_display_all_no_tasklist(self):
#         test_obj = BuildTemplateContext('all', None, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.all_keys)
#
#     def test_display_current(self):
#         test_obj = BuildTemplateContext('current', self.tasklist, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.current_keys)
#
#     def test_display_current_no_tasklist(self):
#         test_obj = BuildTemplateContext('current', None, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.current_keys)
#
#     def test_display_finished(self):
#         test_obj = BuildTemplateContext('finished', self.tasklist, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.finished_keys)
#
#     def test_display_finished_no_tasklist(self):
#         test_obj = BuildTemplateContext('finished', None, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.finished_keys)
#
#     def test_display_urgent(self):
#         test_obj = BuildTemplateContext('urgent', self.tasklist, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.urgent_keys)
#
#     def test_display_urgent_all_tasks(self):
#         tasks = SimpleTask.get_all_tasks_by_user(self.email)
#         test_obj = BuildTemplateContext('urgent', tasks)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.urgent_keys)
#
#     def test_display_important(self):
#         test_obj = BuildTemplateContext('important', self.tasklist, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.important_keys)
#
#     def test_display_important_no_tasklist(self):
#         test_obj = BuildTemplateContext('important', None, self.email)
#         response = test_obj.get_data()
#         self.assertTrue(isinstance(response, dict))
#
#         for key in response.keys():
#             self.assertTrue(key in self.important_keys)
