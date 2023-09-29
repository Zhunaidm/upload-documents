import uuid
from .models import UploadStatusEnum
from .data_access.document_access import get_document_by_upload_id
from datetime import timedelta
from django.utils import timezone
from .constants import EXPIRY_DAYS


def generate_upload_id():
    return uuid.uuid4()


def is_valid_url(url):
    try:
        uuid.UUID(str(url))
        return True
    except ValueError:
        return False


def is_document_valid_status(document):
    return document.status == UploadStatusEnum.PENDING


def check_url_expired(created_at):
    current_date = timezone.now()
    date_difference = current_date - created_at
    return date_difference >= timedelta(days=EXPIRY_DAYS)


def check_valid_upload_request(id):
    # Check if provided url is valid
    if not is_valid_url(id):
        return False
    # Check if url exists in DB
    document = get_document_by_upload_id(id)
    if document is None:
        return False
    # Check if the status is valid i.e document has not been uploaded using this url already and not expired
    return is_document_valid_status(document) and not check_url_expired(
        document.created_at
    )
