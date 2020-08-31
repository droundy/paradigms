from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import Problem

class HomeworkSearchForm(forms.ModelForm):
    q = forms.CharField(max_length=255)
