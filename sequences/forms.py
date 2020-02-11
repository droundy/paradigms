from django import forms
from django.forms.formsets import BaseFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from admin_app.models import Sequence, SequenceItems

from admin_app.choices import *

#################### ACTIVITY FORM #########################
class SequenceForm(forms.ModelForm):
    class Meta:
        model = Sequence
        fields = ('title','date_added','overview_paragraph','author_info')
        exclude=()

    overview_paragraph = forms.CharField(
                    widget=forms.Textarea(
                        attrs={'style':'max-height: 15em',
                        'rows':6,
                        'placeholder': 'Overview paragraph',
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
        self.helper.add_input(Submit('submit', 'Save Sequence'))

class ItemUpdateForm(forms.ModelForm):

    class Meta:
        model = SequenceItems
        fields = '__all__'
        exclude=()
        widgets = {
            'sequence': forms.HiddenInput(),
            'problem': forms.HiddenInput(),
            'activity': forms.HiddenInput(),
            }
# DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    item_position = forms.DecimalField(
                    max_digits=5,
                    decimal_places=2,
                    widget=forms.NumberInput(
                        attrs={
                        'class': 'form-control',
                        'placeholder': 'Position',
                        }
                    ),
                    help_text='Sequence order. Decimal. Sorted in ascending order after saving.',
                    required=False)
    role_in_sequence = forms.CharField(
                    max_length=1024,
                    widget=forms.Textarea(
                        attrs={'style':'max-height: 6em',
                        'rows':4,
                        'placeholder': 'Role in sequence.',
                        'class': 'form-control',
                    }),
                    help_text='Appears above activity or problem on sequence page.',
                    required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_position'].label = ""
        self.fields['role_in_sequence'].label = ""
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('item_position', css_class='form-group col-sm-1 mb-0'),
                Column('role_in_sequence', css_class='form-group col-sm-11 mb0'),
                css_class='form-row'
            ),

        )
