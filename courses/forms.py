from django import forms
from django.forms.formsets import BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from admin_app.choices import *

#################### ACTIVITY FORM #########################
class CourseForm(forms.Form):
    instructor = forms.CharField(label='Instructor', max_length=100)
    instructor = forms.CharField(label='Instructor', max_length=100)

    def __init__(self, *args, **kwargs):
        if 'days' in kwargs:
            days = kwargs.pop('days')
        else:
            days = []
        super(CourseForm, self).__init__(*args, **kwargs)
        for i in range(len(days)):
            d = days[i]
            self.fields['day-' + str(i)] = forms.CharField(label=d)


    @property
    def day_fields(self):
        ''' return the day fields '''
        return [f for f in self if f.name[:4] == 'day-']

