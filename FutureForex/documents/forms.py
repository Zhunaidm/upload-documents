from django import forms
from .models import (
    File,
    UploadStatusEnum,
    NotificationStatus,
    NotificationType,
    FileType,
)


SORT_CHOICES = [("asc", "Ascending"), ("desc", "Descending")]


# Helper to add the All filter without affection the original Enum
def with_all_choice(choices):
    return [("", "All")] + list(choices)


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
    status = forms.ChoiceField(
        choices=with_all_choice(UploadStatusEnum.choices), required=False, initial="All"
    )
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial="desc")


class NotificationFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=with_all_choice(NotificationStatus.choices),
        required=False,
        initial="All",
    )
    type = forms.ChoiceField(
        choices=with_all_choice(NotificationType.choices), required=False, initial="All"
    )
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial="desc")


class CustomerFilterForm(forms.Form):
    email = forms.CharField(required=False)
    name = forms.CharField(required=False)
