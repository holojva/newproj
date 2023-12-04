from django import forms
import datetime


MESSAGE_TYPES = (
    (1, "Работа"),
    (2, "Спорт"),
    (3, "Учеба"),
)

YEARS = tuple(range(2023,int(datetime.date.today().year)+5))
class ChangeStatusForm(forms.Form) :
    text_input = forms.CharField()


class CreateTasksForm(forms.Form) :
    text_input = forms.CharField(max_length=100)
    types_of_tasks = forms.ChoiceField(
        choices=MESSAGE_TYPES
    )
    date = forms.DateTimeField()
    important = forms.ChoiceField(
        choices=((1, "Важное задание"), (0, "Heважное задание"))
    )