from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import Activity

from admin_app.choices import *

#################### ACTIVITY FORM #########################
class ActivityForm(forms.ModelForm):
    topics = forms.CharField(required=False, max_length=1024, widget=forms.Textarea(attrs={'style':'max-height: 5em', 'rows':4}), help_text='Comma-separated list of topics: adiabatic susceptibility,entropy')

    keywords = forms.CharField(required=False, max_length=1024, widget=forms.Textarea(attrs={'rows':4}), help_text='Comma-separated list of keywords: keyword1,keyword two,keywordthree')

    associated_paper_links = forms.CharField(required=False, max_length=2048, widget=forms.Textarea(attrs={'rows':4}), help_text='Comma-separated list of URLs with http/https prefix: http://foo.com/index.html,https://otherfoo.net/paper/name')

    equipment_required = forms.CharField(required=False, max_length=4096, widget=forms.Textarea(attrs={'style':'max-height: 5em', 'rows':4, 'placeholder':'None'}), help_text='Enter "None" if no equipment is required for this activity')

    course = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder':'ph123'}), help_text='Quick search field for courses that might be using this activity')

    author_info = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder':'ph123'}), help_text='Displayed like an activity Byline. Can include names, email addresses, etc.')

    instructor_guide = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':16}), help_text='Latex is accepted and encouraged in the Instructor\'s Guide.')

    time_estimate = forms.ChoiceField(choices=TIMEESTIMATECHOICES, initial=5)

    type_of_beast = forms.ChoiceField(choices=TYPEOFBEASTCHOICES, help_text='Ingredient Type?')

    publication_status = forms.ChoiceField(choices=PUBLICATIONSTATUSCHOICES, initial="Draft")

    prerequisite_knowledge = forms.CharField(required=False,  widget=forms.Textarea(attrs={'rows':6}), help_text='Comma-separated list of topics: adiabatic susceptibility,entropy')

    activity_image = forms.ImageField(required=False)

    class Meta:
        model = Activity
        fields = ('id','title','overview_paragraph','time_estimate','what_students_learn','type_of_beast','notes','equipment_required','topics','instructor_guide','publication_status','publication_date','prerequisite_knowledge','activity_image','keywords','author','associated_paper_links','program_learning_outcomes','course_learning_outcomes','learning_progression_concepts','course','author_info','old_name')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['instructor_guide'].label = "Instructor's Guide"
        self.fields['author'].label = "Editor"
        self.fields['author_info'].label = "Author Information"
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Activity'))

# class ActivityForm(forms.ModelForm):
# time_estimate = EnumField(choices:[
#     ('5'='Under 5 Minutes'),
#     ('10'='5-10 Minutes'),
#     ('30'='15-30 Minutes'),
#     ('60'='1 Hour'),
#     ('120'='2+ Hours'),
# ])

#################### ACTIVITY FORM READ ONLY #########################
class ActivityFormReadOnly(forms.ModelForm):
    topics = forms.CharField(required=False, max_length=1024, widget=forms.Textarea(attrs={'style':'max-height: 5em', 'rows':4, 'disabled':True}), help_text='Comma-separated list of topics: adiabatic susceptibility,entropy')

    keywords = forms.CharField(required=False, max_length=1024, widget=forms.Textarea(attrs={'rows':4}), help_text='Comma-separated list of keywords: keyword1,keyword two,keywordthree')

    associated_paper_links = forms.CharField(required=False, max_length=2048, widget=forms.Textarea(attrs={'rows':4}), help_text='Comma-separated list of URLs with http/https prefix: http://foo.com/index.html,https://otherfoo.net/paper/name')

    equipment_required = forms.CharField(required=False, max_length=4096, widget=forms.Textarea(attrs={'style':'max-height: 5em', 'rows':4, 'placeholder':'None'}), help_text='Enter "None" if no equipment is required for this activity')

    course = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder':'ph123'}), help_text='Quick search field for courses that might be using this activity')

    author_info = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'placeholder':'ph123'}), help_text='Displayed like an activity Byline. Can include names, email addresses, etc.')

    instructor_guide = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':16}), help_text='Latex is accepted and encouraged in the Instructor\'s Guide.')

    time_estimate = forms.ChoiceField(choices=TIMEESTIMATECHOICES, initial=5)

    type_of_beast = forms.ChoiceField(choices=TYPEOFBEASTCHOICES, help_text='test')

    publication_status = forms.ChoiceField(choices=PUBLICATIONSTATUSCHOICES, initial="Draft")

    prerequisite_knowledge = forms.CharField(required=False,  widget=forms.Textarea(attrs={'rows':6}), help_text='Comma-separated list of topics: adiabatic susceptibility,entropy')

    class Meta:
        model = Activity
        fields = ('id','title','overview_paragraph','time_estimate','what_students_learn','type_of_beast','notes','equipment_required','topics','instructor_guide','publication_status','publication_date','prerequisite_knowledge','activity_image','keywords','author','associated_paper_links','program_learning_outcomes','course_learning_outcomes','learning_progression_concepts','course','author_info','old_name')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['instructor_guide'].label = "Instructor's Guide"
        self.fields['author'].label = "Editor"
        self.fields['author_info'].label = "Author Information"
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Activity'))

        # for nam, field in self.fields.items():
        #     field.disabled = True
