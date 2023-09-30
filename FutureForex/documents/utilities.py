import uuid
from .models import UploadStatus
from .data_access.document_access import get_document_by_upload_id
from datetime import timedelta
from django.utils import timezone
from .constants import EXPIRY_DAYS


def generate_upload_id():
    return uuid.uuid4()


def is_upload_id_expired(created_at):
    current_date = timezone.now()
    date_difference = current_date - created_at
    return date_difference >= timedelta(days=EXPIRY_DAYS)


def is_document_upload_valid(document):
    # Check if the status is Pending and the upload_id has not expired
    return document.status == UploadStatus.PENDING and not is_upload_id_expired(
        created_at=document.created_at
    )


def is_valid_upload_request(upload_id):
    # Check if upload_id exists in DB
    document = get_document_by_upload_id(upload_id=upload_id)
    return document and is_document_upload_valid(document=document)


def fill_email_template(email_template, replacement_dict):
    body = email_template.body

    for placeholder, replacement in replacement_dict.items():
        body = body.replace(f"%{placeholder}%", str(replacement))

    if "%" in body:
        raise ValueError("Unreplaced '%' characters in body", body)

    return body
