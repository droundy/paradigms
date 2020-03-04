from django import forms
from django.db import models
from django.forms.formsets import BaseFormSet
from django.forms import BaseModelFormSet, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import Pages
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from admin_app.choices import *

class PageForm(forms.ModelForm):
    page_content = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':16}), help_text='Use Latex Formatting')

    keywords = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2}), help_text='Comma-separated list of topics/keywords: adiabatic susceptibility,entropy')

    whitepaper_category = forms.ChoiceField(required=False, choices=WHITEPAPERCATS, initial='none', help_text="If this page is meant to be a whitepaper, please select a category. The category list is maintained by system administrators and can not be dynamic.")

    class Meta:
        model = Pages
        fields = ('title','page_content','keywords','whitepaper','whitepaper_category','publication')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Save Page'))
        self.helper.layout = Layout(
            Row(
                    Column('title', css_class='form-group col-md-12 mb0'),
                    css_class='form-row'
                ),
            Row(
                    Column('keywords', css_class='form-group col-md-12 mb0'),
                    css_class='form-row'
                ),            
            Row(
                     Column('page_content', css_class='form-group col-md-12 mb0'),
                     css_class='form-row'
                ),
            Row(
                    Column('whitepaper', css_class='form-group col-md-12 mb0'),
                    css_class='form-row',
                ),
            Row(
                    Column('whitepaper_category', css_class='form-group col-md-12 mb0'),
                    css_class='form-row'
                ),
            Row(
                Column('publication', css_class='form-group col-md-12 mb0'),
            ),            
            Submit('submit', 'Save'),
        )

# class PageForm(forms.ModelForm):
#     title = forms.CharField(required=False, max_length=1024, widget=forms.TextInput(attrs={'style':'max-height: 5em'}), help_text='Page title. Appears at the top of the page.')
#
#     class Meta:
#         model = Pages
#         fields = ('title','contents')
#         exclude = ()
#         permissions = (
#             ("can_edit_pages", "Edit Page"),
#             ("can_add_pages","Add Page"))
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Save Page'))
#
# class PageImageForm(forms.ModelForm):
#
#     class Meta:
#         model = PageImage
#         fields = ('page','image','title','caption')
#         exclude = ()
#         permissions = (
#             ("can_edit_page_images", "Edit Page Images"),
#             ("can_add_page_images","Add Page Images"))
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Save Image'))
