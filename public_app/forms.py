from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import Problem, CourseLearningOutcome
from django_ace import AceWidget

class ProblemForm(forms.ModelForm):

    # problem_latex = forms.CharField(widget=AceWidget(mode='latex', showprintmargin=False, maxlines=1000, minlines=30, wordwrap=True, fontsize=30))

    # widgets = {
    #     "problem_latex": forms.Textarea(),
    # }
    topics = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={'style':'max-height: 5em'}), help_text='Comma-separated list of topics: adiabatic susceptibility,entropy')

    course = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder':'ph123'}), help_text='Courses that might use this problem')

    learning_outcomes = forms.ModelMultipleChoiceField(required=False,
                                                       queryset=CourseLearningOutcome.objects.all().order_by('course__number'),
                                                       widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Problem
        fields = ('problem_title','publication','problem_latex','created_date','published_date','author','id','attribution','old_name','topics','course')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        if self.instance.dayproblem_set.exists():
            courses = set()
            for d in self.instance.dayproblem_set.all():
                courses.add(d.day.taught.course)
            self.fields['learning_outcomes'].queryset = CourseLearningOutcome.objects.filter(course__in=courses)
        elif self.instance.course:
            self.fields['learning_outcomes'].queryset = CourseLearningOutcome.objects.filter(course__number=self.instance.course).order_by('course__number')
        self.fields['learning_outcomes'].widget.attrs['class'] = 'checkboxes'
        self.helper.add_input(Submit('submit', 'Save Problem'))
