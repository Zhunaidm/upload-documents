from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["url"]


class DocumentRequestForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    type = forms.CharField(max_length=100)
