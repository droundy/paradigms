from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import Problem
from django_ace import AceWidget

class ProblemForm(forms.ModelForm):

    # problem_latex = forms.CharField(widget=AceWidget(mode='latex', showprintmargin=False, maxlines=1000, minlines=30, wordwrap=True, fontsize=30))

    # widgets = {
    #     "problem_latex": forms.Textarea(),
    # }
    topics = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={'style':'max-height: 5em'}), help_text='Comma-separated list of topics: adiabatic susceptibility,entropy')

    course = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder':'ph123'}), help_text='Courses that might use this problem')

    class Meta:
        model = Problem
        fields = ('problem_title','problem_latex','created_date','published_date','author','id','attribution','old_name','topics','course')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Problem'))
