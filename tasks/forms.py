from django import forms


class SimpleTaskForm(forms.Form):
    name = forms.CharField(max_length=150)
    due_date = forms.DateField(required=False)
    description = forms.CharField(required=False)
