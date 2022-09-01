from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from .models import RecordGroup


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FileUploadForm(forms.Form):
    the_file = forms.FileField(label="")

# OCR_FRAMEWORKS = [
#     ('azure', 'Azure'),
#     ('google_vision', 'Google Vision'),
#     ('tesseract', 'Tesseract'),
# ]

# class IndexForm(forms.ModelForm): 
#     class Meta:
#         model = RecordGroup
#         fields = ('oai_endpoint', 'sets', 'records')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
       

    # oai_endpoint = forms.URLField(label = "OAI Endpoint", required = True)
    
    # sets = forms.MultipleChoiceField(
    #     required=False,
    #     label = "Collection Sets",
    #     widget=forms.Select,
    # )

    # records = forms.MultipleChoiceField(
    #     required=False,
    #     label = "Set Records",
    #     widget=forms.Select,
    # )

    # framework = forms.MultipleChoiceField(
    #     required=False,
    #     label = "Choose OCR Framework",
    #     widget=forms.Select,
    #     choices=OCR_FRAMEWORKS,
    # )

