from tasks.models import TaskList, SimpleTask
import datetime

def convert_to_clean_date(due_date):
    if isinstance(due_date, str):
        due_date = convert_into_date_type(due_date)
    return due_date.strftime("%d %b")

def convert_into_date_type(str_date):
     return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()
