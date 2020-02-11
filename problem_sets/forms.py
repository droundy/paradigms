from django.forms import inlineformset_factory
from django import forms
from django.forms.formsets import BaseFormSet
from django.forms import BaseModelFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from admin_app.models import ProblemSet, ProblemSetItems, Problem

from admin_app.choices import *

class ProblemSetForm(forms.ModelForm):
    class Meta:
        model = ProblemSet
        fields = ('title','instructions','author','author_info')
        exclude=()

    instructions = forms.CharField(
                    widget=forms.Textarea(
                        attrs={'style':'max-height: 15em',
                        'rows':6,
                        'placeholder': 'Instructions',
                        'class': 'form-control',
                    }),
                    help_text='Shows up in search results and directory pages. May contain latex',
                    required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields['author'].label = "Editor"
        self.fields['author_info'].label = "Author Information"
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Problem Set'))

# class ProblemGroupForm(forms.ModelForm):
class ProblemGroupForm(forms.ModelForm):

    instructions = forms.CharField(
                    widget=forms.Textarea(
                        attrs={'style':'max-height: 60em',
                        'rows':6,
                        'placeholder': 'Overview paragraph',
                        'class': 'form-control',
                    }),
                    help_text='Shows up in search results and directory pages. May contain latex',
                    required=False)

    class Meta:
        model = ProblemSet
        fields = ('title','date_added','published_date','instructions','author','author_info')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Problem Set'))

class BaseProblemGroupForm(BaseFormSet):

    instructions = forms.CharField(
                    widget=forms.Textarea(
                        attrs={'style':'max-height: 60em',
                        'rows':6,
                        'placeholder': 'Instructions',
                        'class': 'form-control',
                    }),
                    help_text='Shows up in search results and directory pages. May contain latex',
                    required=False)

    class Meta:
        model = ProblemSet
        fields = ('title','date_added','published_date','instructions','author','author_info')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Problem Set'))

ProblemGroupItemsFormset = inlineformset_factory(
    ProblemSet,
    ProblemSetItems,
    form=BaseProblemGroupForm,
    fields=(
        'item_position',
        'problem',
        'item_instructions',),
    )
