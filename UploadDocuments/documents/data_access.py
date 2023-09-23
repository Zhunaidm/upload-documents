from .models import UploadUrlEnum
from .models import Customer, Document, DocumentRequest, Notification
from django.db.models import Q


def get_customers_by_rm(relationship_manager, name=None, email=None):
    query = Q(relationship_manager=relationship_manager)
    if name:
        query &= Q(name__icontains=name)
    if email:
        query &= Q(email__icontains=email)
    return Customer.objects.filter(query)


def get_documents_by_customer(customer_id):
    return Document.objects.filter(customer_id=customer_id)


def get_document_requests(customer_id):
    return DocumentRequest.objects.filter(customer_id=customer_id)


def update_document_request_status_from_url(url, status):
    return DocumentRequest.objects.filter(presigned_url=url).update(status=status)


def create_notification(id, type, text):
    return Notification.objects.create(relationship_manager=id, type=type, text=text)


def get_notifications_by_rm(id):
    return Notification.objects.filter(relationship_manager=id)


def is_document_request_invalid_status(document_request):
    return document_request.status == UploadUrlEnum.PENDING


def get_rm_by_document_request(url):
    document_request = DocumentRequest.objects.get(presigned_url=url)
    customer = document_request.document.customer
    return customer.relationship_manager


def get_document_requests_aggragated(id, email=None, status="All"):
    query = Q(document__customer__relationship_manager_id=id)

    if email:
        query &= Q(document__customer__email__icontains=email)

    if status and status != 'All':
        query &= Q(status=status)

    return DocumentRequest.objects.select_related('document__customer__relationship_manager').filter(query)
