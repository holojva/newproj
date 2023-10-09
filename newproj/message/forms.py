from django import forms
class ChangeStatusForm(forms.Form) :
    # message_status = forms.ChoiceField(choices=[(1, "Да"), (2,"Нет")])
    text_input = forms.CharField()