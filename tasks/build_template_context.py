from tasks.models import SimpleTask


class BuildTemplateContext:

    def __init__(self, display, tasks):
        self.display = display
        self.tasks = tasks

    def get_data(self):
        overdue_tasks = SimpleTask.get_overdue_tasks(self.tasks)
        due_today_tasks = SimpleTask.get_today_tasks(self.tasks)
        due_tommorow_tasks = SimpleTask.get_tomorrow_tasks(self.tasks)
        future_tasks = SimpleTask.get_future_tasks(self.tasks)
        no_date_tasks = SimpleTask.get_no_date_tasks(self.tasks)
        finished_tasks = SimpleTask.get_finished_tasks(self.tasks)
        urgent_tasks = SimpleTask.get_urgent_tasks(self.tasks)
        important_tasks = SimpleTask.get_important_tasks(self.tasks)

        important_urgent = SimpleTask.get_important_urgent_tasks(self.tasks)
        important_non_urgent = SimpleTask.get_important_non_urgent_tasks(
            self.tasks)
        non_important_urgent = SimpleTask.get_non_important_urgent_tasks(
            self.tasks)
        non_important_non_urgent = SimpleTask. \
            get_non_important_non_urgent_tasks(self.tasks)

        matrix_backlog = SimpleTask.get_matrix_backlog_tasks(self.tasks)

        all_data = {'overdue_tasks': overdue_tasks,
                    'due_today_tasks': due_today_tasks,
                    'due_tommorow_tasks': due_tommorow_tasks,
                    'future_tasks': future_tasks,
                    'no_date_tasks': no_date_tasks,
                    'finished_tasks': finished_tasks,
                    'urgent_tasks': urgent_tasks,
                    'important_tasks': important_tasks,
                    'important_urgent': important_urgent,
                    'important_non_urgent': important_non_urgent,
                    'non_important_urgent': non_important_urgent,
                    'non_important_non_urgent': non_important_non_urgent,
                    'matrix_backlog': matrix_backlog}

        dict = {}
        keys_list = self.content_to_return()

        for k, v in all_data.items():
            if k in keys_list:
                dict[k] = v

        return dict

    def content_to_return(self):

        if self.display == 'all':
            return ['overdue_tasks', 'due_today_tasks', 'due_tommorow_tasks',
                    'future_tasks', 'no_date_tasks', 'finished_tasks']

        elif self.display == 'current':
            return ['overdue_tasks', 'due_today_tasks',
                    'due_tommorow_tasks', 'future_tasks', 'no_date_tasks']

        elif self.display == 'urgent':
            return ['urgent_tasks']

        elif self.display == 'important':
            return ['important_tasks']

        elif self.display == 'finished':
            return ['finished_tasks']

        elif self.display == 'matrix':
            return ['important_urgent', 'important_non_urgent',
                    'non_important_urgent', 'non_important_non_urgent',
                    'matrix_backlog']
