from tasks.models import TaskList, SimpleTask
from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from datetime import date


class TasksModelsTest(TestCase):

    def setUp(self):
        self.add_data()

    def add_data(self):

        self.user = User.objects.create_user(username="test@test.com",
                                             email="test@test.com",
                                             password="testpassword")

        self.tasklist_1 = TaskList.objects.create(user=self.user,
                                                  name="Loisirs",
                                                  color="#55b37e")
        self.tasklist_2 = TaskList.objects.create(user=self.user,
                                                  name="Travail",
                                                  color="#333333")

        for i in range(5):
            SimpleTask.objects.create(tasklist=self.tasklist_1,
                                      name=("loisir " + str(i)),
                                      due_date=(date.today()
                                                + datetime.timedelta(days=i)),
                                      description=("Description loisir "
                                                    + str(i)),
                                      creation=timezone.now(),
                                      is_done=True)

        for j in range(5):
            SimpleTask.objects.create(tasklist=self.tasklist_2,
                                      name=("travail " + str(j)),
                                      due_date=(date.today()
                                                + datetime.timedelta(days=j)),
                                      description=("Description travail "
                                                    + str(j)),
                                      creation=timezone.now(),
                                      is_done=False)


    def test_get_tasklists_from_user(self):

        tl = TaskList.get_tasklists_from_user(self.user.email)
        self.assertTrue(isinstance(tl[0], TaskList))
        self.assertEqual(tl[0].name, "Loisirs")

    def test_get_tasklist_by_id(self):

        tl = TaskList.get_tasklist_by_id(self.tasklist_1.id)
        self.assertTrue(isinstance(tl, TaskList))
        self.assertEqual(tl.name, self.tasklist_1.name)
        self.assertEqual(tl.color, self.tasklist_1.color)

    def test_get_tasks_from_tasklist(self):
        tasks = SimpleTask.get_tasks_from_tasklist(self.tasklist_1)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertEquals(task.tasklist, self.tasklist_1)

    def test_get_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        self.assertEquals(len(all_tasks), 10)
        for task in all_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_all_done_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_done_tasks_by_user(self.user)
        for task in all_tasks:
            self.assertTrue(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_all_undone_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_undone_tasks_by_user(self.user)
        for task in all_tasks:
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_tasks_with_due_date_from_tasklist(self):
        tasks = SimpleTask.get_tasks_with_due_date_from_tasklist(self.tasklist_1)
        for task in tasks:
            self.assertTrue(isinstance(task.due_date, date))
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_task_with_id(self):
        first_task = SimpleTask.objects.all()[:1]
        task = SimpleTask.get_task_with_id(first_task[0].id)
        self.assertTrue(isinstance(task, SimpleTask))
        self.assertEquals(task.id, first_task[0].id)

    def test_get_overdue_tasks_with_all_tasks_by_user(self):
        today = date.today()
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        overdue_tasks = SimpleTask.get_overdue_tasks(all_tasks)
        for task in overdue_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date < today)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_overdue_tasks_with_tasks_from_tasklist(self):
        today = date.today()
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        overdue_tasks = SimpleTask.get_overdue_tasks(tasklist_tasks)
        for task in overdue_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date < today)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_today_tasks_with_all_tasks_by_user(self):
        today = date.today()
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        today_tasks = SimpleTask.get_today_tasks(all_tasks)
        for task in today_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date == today)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_today_tasks_with_tasks_from_tasklist(self):
        today = date.today()
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_2)
        today_tasks = SimpleTask.get_today_tasks(tasklist_tasks)
        for task in today_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date == today)
            self.assertEquals(task.tasklist.user, self.user)


    def test_get_tomorrow_tasks_with_all_tasks_by_user(self):
        tomorrow = date.today() + datetime.timedelta(days=1)
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        tomorrow_tasks = SimpleTask.get_tomorrow_tasks(all_tasks)
        for task in tomorrow_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date == tomorrow)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_tomorrow_tasks_with_tasks_from_tasklist(self):
        tomorrow = date.today() + datetime.timedelta(days=1)
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        tomorrow_tasks = SimpleTask.get_tomorrow_tasks(tasklist_tasks)
        for task in tomorrow_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date == tomorrow)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_future_tasks_with_all_tasks_by_user(self):
        tomorrow = date.today() + datetime.timedelta(days=1)
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        future_tasks = SimpleTask.get_future_tasks(all_tasks)
        for task in future_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date > tomorrow)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_future_tasks_with_tasks_from_tasklist(self):
        tomorrow = date.today() + datetime.timedelta(days=1)
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        future_tasks = SimpleTask.get_future_tasks(tasklist_tasks)
        for task in future_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date > tomorrow)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_no_date_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        no_date_tasks = SimpleTask.get_no_date_tasks(all_tasks)
        for task in no_date_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date is None)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_no_date_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_2)
        no_date_tasks = SimpleTask.get_no_date_tasks(tasklist_tasks)
        for task in no_date_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.due_date is None)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_finished_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        finished_tasks = SimpleTask.get_finished_tasks(all_tasks)
        for task in finished_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_finished_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_2)
        finished_tasks = SimpleTask.get_finished_tasks(tasklist_tasks)
        for task in finished_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_important_urgent_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        tasks = SimpleTask.get_important_urgent_tasks(all_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_important)
            self.assertTrue(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_important_urgent_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        tasks = SimpleTask.get_important_urgent_tasks(tasklist_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_important)
            self.assertTrue(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_important_non_urgent_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        tasks = SimpleTask.get_important_non_urgent_tasks(all_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_important)
            self.assertFalse(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_important_non_urgent_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_2)
        tasks = SimpleTask.get_important_non_urgent_tasks(tasklist_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_important)
            self.assertFalse(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_non_important_urgent_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        tasks = SimpleTask.get_non_important_urgent_tasks(all_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertFalse(task.is_important)
            self.assertTrue(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_non_important_urgent_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        tasks = SimpleTask.get_non_important_urgent_tasks(tasklist_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertFalse(task.is_important)
            self.assertTrue(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_non_important_non_urgent_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        tasks = SimpleTask.get_non_important_urgent_tasks(all_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertFalse(task.is_important)
            self.assertFalse(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_non_important_non_urgent_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_2)
        tasks = SimpleTask.get_non_important_urgent_tasks(tasklist_tasks)
        for task in tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertFalse(task.is_important)
            self.assertFalse(task.is_urgent)
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_urgent_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        urgent_tasks = SimpleTask.get_urgent_tasks(all_tasks)
        for task in urgent_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_urgent)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_urgent_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        urgent_tasks = SimpleTask.get_urgent_tasks(tasklist_tasks)
        for task in urgent_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_urgent)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_important_tasks_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        important_tasks = SimpleTask.get_important_tasks(all_tasks)
        for task in important_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_important)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_important_tasks_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_1)
        important_tasks = SimpleTask.get_important_tasks(tasklist_tasks)
        for task in important_tasks:
            self.assertTrue(isinstance(task, SimpleTask))
            self.assertTrue(task.is_important)
            self.assertEquals(task.tasklist.user, self.user)

    def test_get_to_do_tasks_not_in_matrix_with_all_tasks_by_user(self):
        all_tasks = SimpleTask.get_all_tasks_by_user(self.user)
        tasks = SimpleTask.get_to_do_tasks_not_in_matrix(all_tasks)
        for task in tasks:
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)
            self.assertTrue((task.is_urgent not in [True, False]) and (task.is_important not in [True, False]))

    def test_get_to_do_tasks_not_in_matrix_with_tasks_from_tasklist(self):
        tasklist_tasks = SimpleTask.objects.filter(tasklist=self.tasklist_2)
        tasks = SimpleTask.get_to_do_tasks_not_in_matrix(tasklist_tasks)
        for task in tasks:
            self.assertFalse(task.is_done)
            self.assertEquals(task.tasklist.user, self.user)
            self.assertTrue((task.is_urgent not in [True, False]) and (task.is_important not in [True, False]))
