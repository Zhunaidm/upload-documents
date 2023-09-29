import uuid
from .models import UploadStatus
from .data_access.document_access import get_document_by_upload_id
from datetime import timedelta
from django.utils import timezone
from .constants import EXPIRY_DAYS


def generate_upload_id():
    return uuid.uuid4()


def is_valid_upload_id(upload_id):
    try:
        uuid.UUID(str(upload_id))
        return True
    except ValueError:
        return False


def is_document_valid_status(document):
    # The only valid status for now is Pending. This can eventually be extended if other checks are necessary
    return document.status == UploadStatus.PENDING


def is_url_expired(created_at):
    current_date = timezone.now()
    date_difference = current_date - created_at
    return date_difference >= timedelta(days=EXPIRY_DAYS)


def is_valid_upload_request(upload_id):
    # Check if provided url is valid
    if not is_valid_upload_id(upload_id=upload_id):
        return False
    # Check if url exists in DB
    document = get_document_by_upload_id(upload_id=upload_id)
    if document is None:
        return False
    # Check if the status is valid i.e document has not been uploaded using this url already and not expired
    return is_document_valid_status(document=document) and not is_url_expired(
        created_at=document.created_at
    )


def fill_email_template(email_template, replacement_dict):
    body = email_template.body

    for placeholder, replacement in replacement_dict.items():
        body = body.replace(f"%{placeholder}%", str(replacement))

    if "%" in body:
        raise ValueError("Unreplaced '%' characters in body", body)

    return body
