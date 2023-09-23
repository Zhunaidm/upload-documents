from .models import UploadStatusEnum
from .models import Customer, Document, Notification
from django.db.models import Q


def get_customers_by_rm(relationship_manager, name=None, email=None):
    query = Q(relationship_manager=relationship_manager)
    if name:
        query &= Q(name__icontains=name)
    if email:
        query &= Q(email__icontains=email)
    return Customer.objects.filter(query)

def get_customer_by_email(email):
    return Customer.objects.filter(email=email).first()

def get_documents_by_customer(customer_id):
    return Document.objects.filter(customer_id=customer_id)


def get_document_requests(customer_id):
    return Document.objects.filter(customer_id=customer_id)


def update_document_request_status_from_url(url, status):
    return Document.objects.filter(presigned_url=url).first().update(status=status)

def get_document_by_url(url):
    return Document.objects.filter(presigned_url=url).first()

def create_notification(id, type, text):
    return Notification.objects.create(relationship_manager=id, type=type, text=text)


def get_notifications_by_rm(id, type=None, text=None, read="All"):
    query = Q(relationship_manager=id)
    if type:
        query &= Q(type=type)
    if text:
        query &= Q(text__icontains=text)    
    if read and read != 'All':
        query &= Q(read=read)    
    return Notification.objects.filter(query)


def is_document_invalid_status(document):
    return document.status == UploadStatusEnum.PENDING


def get_rm_by_document(url):
    document = Document.objects.get(presigned_url=url)
    customer = document.document.customer
    return customer.relationship_manager


def get_document_aggragated(id, email=None, status="All"):
    query = Q(customer__relationship_manager_id=id)

    if email:
        query &= Q(customer__email__icontains=email)

    if status and status != 'All':
        query &= Q(status=status)

    return Document.objects.select_related('customer__relationship_manager').filter(query)
