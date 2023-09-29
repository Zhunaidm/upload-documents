from django.db.models import Q
from ..models import EmailTemplate


def get_email_template_by_file_type(file_type):
    try:
        return EmailTemplate.objects.get(file_type=file_type)
    except EmailTemplate.DoesNotExist:
        return None
