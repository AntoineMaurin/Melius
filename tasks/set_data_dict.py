from django.contrib.auth.models import User
from tasks.models import TaskList, SimpleTask


class SetDataDict:

    def __init__(self, display, tasklist_to_show, user_mail):
        self.display = display
        self.tasklist_to_show = tasklist_to_show
        self.user_mail = user_mail

    def get_data(self):

        all_tasklists = TaskList.get_tasklists_from_user(self.user_mail)

        if self.tasklist_to_show:
            overdue_tasks = SimpleTask.get_overdue_tasks_list(self.tasklist_to_show)
            due_today_tasks = SimpleTask.get_today_tasks_list(self.tasklist_to_show)
            due_tommorow_tasks = SimpleTask.get_tomorrow_tasks_list(self.tasklist_to_show)
            future_tasks = SimpleTask.get_future_tasks(self.tasklist_to_show)
            no_date_tasks = SimpleTask.get_no_date_tasks(self.tasklist_to_show)
            finished_tasks = SimpleTask.get_finished_tasks(self.tasklist_to_show)
        else:
            user = User.objects.get(email=self.user_mail)
            all_tasks = SimpleTask.get_all_tasks_by_user(user)

            overdue_tasks = SimpleTask.get_overdue_tasks(all_tasks)
            due_today_tasks = SimpleTask.get_due_today_tasks(all_tasks)
            due_tommorow_tasks = SimpleTask.get_due_tomorrow_tasks(all_tasks)
            future_tasks = SimpleTask.get_upcoming_tasks(all_tasks)
            no_date_tasks = SimpleTask.get_no_due_date_tasks(all_tasks)
            finished_tasks = SimpleTask.get_completed_tasks(all_tasks)

        all_data = {'overdue_tasks': overdue_tasks,
                    'due_today_tasks': due_today_tasks,
                    'due_tommorow_tasks': due_tommorow_tasks,
                    'future_tasks': future_tasks,
                    'no_date_tasks': no_date_tasks,
                    'finished_tasks': finished_tasks,
                    'all_tasklists': all_tasklists,
                    'tasklist_to_show': self.tasklist_to_show}

        dict = {}
        keys_list = self.get_keys()

        for k, v in all_data.items():
            if k in keys_list:
                dict[k] = v

        return dict

    def get_keys(self):

        if self.display == 'all':
            return ['overdue_tasks', 'due_today_tasks', 'due_tommorow_tasks',
                    'future_tasks', 'no_date_tasks', 'finished_tasks',
                    'all_tasklists', 'tasklist_to_show']

        elif self.display == 'current':
            return ['overdue_tasks', 'due_today_tasks',
                    'due_tommorow_tasks', 'future_tasks', 'no_date_tasks',
                    'all_tasklists', 'tasklist_to_show']

        elif self.display == 'finished':

            return ['finished_tasks', 'all_tasklists', 'tasklist_to_show']
