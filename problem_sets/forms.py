from django.forms import inlineformset_factory
from django import forms
from django.forms.formsets import BaseFormSet
from django.forms import BaseModelFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from admin_app.models import ProblemSet, ProblemSetItems, Problem

from admin_app.choices import *

class ProblemSetAddForm(forms.ModelForm):
    class Meta:
        model = ProblemSet
        fields = ('title','course','instructions','due_date','author','author_info','publication','course')
        exclude=()

    due_date = forms.SplitDateTimeField(
        label="Due Date and Time", widget=forms.SplitDateTimeWidget(
            date_attrs=({'class':'form-control', 'type':'date'}), # or override the ID, "id":id
            time_attrs=({'class':'form-control', 'type':'time'})
        ),
        required=False
    )
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
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb0'),
                css_class='form-row'
            ),
            Row(
                Column('course', css_class='form-group col-md-4 mb0'),
                Column('due_date', css_class='form-group col-md-4 mb0'),
                Column('publication', css_class='form-group col-md-4 mb0'),
                css_class='form-row'
            ),
            'instructions',
            Row(
                Column('author', css_class='form-group col-md-6 mb0'),
                Column('author_info', css_class='form-group col-md-6 mb0'),
                css_class='form-row'
            )

        ) # End layout

class ProblemSetEditForm(forms.ModelForm):
    
    # due_date = forms.DateField(
    #     widget=forms.TextInput(
    #         attrs={'type': 'date'}
    #     ),
    #     required=False
    # )

    due_date = forms.SplitDateTimeField(
        label="Due Date and Time", widget=forms.SplitDateTimeWidget(
            date_attrs=({'class':'form-control', 'type':'date'}), # or override the ID, "id":id
            time_attrs=({'class':'form-control', 'type':'time'})
        ),
        required=False
    )
    
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
        fields = ('title','course','instructions','due_date','author','author_info','publication')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Problem Set'))
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb0'),
                css_class='form-row'
            ),
            Row(
                Column('course', css_class='form-group col-md-4 mb0'),
                Column('due_date', css_class='form-group col-md-4 mb0'),
                Column('publication', css_class='form-group col-md-4 mb0'),
                css_class='form-row'
            ),
            'instructions',
            Row(
                Column('author', css_class='form-group col-md-6 mb0'),
                Column('author_info', css_class='form-group col-md-6 mb0'),
                css_class='form-row'
            ))

class BaseProblemSetForm(BaseFormSet):

    # due_date = forms.DateField(
    #     widget=forms.TextInput(
    #         attrs={'type': 'date'}
    #     ),
    #     required=False
    # )

    due_date = forms.SplitDateTimeField(
        label="Due Date and Time", widget=forms.SplitDateTimeWidget(
            date_attrs=({'class':'form-control', 'type':'date'}), # or override the ID, "id":id
            time_attrs=({'class':'form-control', 'type':'time'})
        ),
        required=False
    )

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
        fields = ('title','course','instructions','due_date','author','author_info','publication','course')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Problem Set'))
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb0'),
                css_class='form-row'
            ),
            Row(
                Column('course', css_class='form-group col-md-4 mb0'),
                Column('due_date', css_class='form-group col-md-4 mb0'),
                Column('publication', css_class='form-group col-md-4 mb0'),
                css_class='form-row'
            ),
            'instructions',
            Row(
                Column('author', css_class='form-group col-md-6 mb0'),
                Column('author_info', css_class='form-group col-md-6 mb0'),
                css_class='form-row'
            ))

ProblemSetItemsFormset = inlineformset_factory(
    ProblemSet,
    ProblemSetItems,
    form=BaseProblemSetForm,
    fields=(
        'item_position',
        'problem',
        'item_instructions',),
    )
