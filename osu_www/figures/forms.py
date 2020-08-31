from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import Figure

class FigureForm(forms.ModelForm):
    class Meta:
        model = Figure
        fields = ('file', 'title')
