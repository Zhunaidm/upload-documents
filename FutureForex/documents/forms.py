from django import forms
from .models import (
    File,
    UploadStatusEnum,
    NotificationStatus,
    NotificationType,
    FileType,
)


SORT_CHOICES = [("asc", "Ascending"), ("desc", "Descending")]


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["url"]


class DocumentRequestForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    type = forms.ChoiceField(choices=FileType.choices)


class DocumentFilterForm(forms.Form):
    email = forms.CharField(required=False)
    # Add an All option to the status filter
    status_choices = list(UploadStatusEnum.choices)
    status_choices.insert(0, ("", "All"))
    status = forms.ChoiceField(choices=status_choices, required=False, initial="All")
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial="desc")


class NotificationFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=NotificationStatus.choices, required=False, initial="All"
    )
    type = forms.ChoiceField(
        choices=NotificationType.choices, required=False, initial="All"
    )
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial="desc")


class CustomerFilterForm(forms.Form):
    email = forms.CharField(required=False)
    name = forms.CharField(required=False)
