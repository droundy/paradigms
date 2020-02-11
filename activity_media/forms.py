from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from admin_app.models import ActivityMedia

class MediaForm(forms.ModelForm):
    class Meta:
        model = ActivityMedia
        fields = ('file', 'title')
