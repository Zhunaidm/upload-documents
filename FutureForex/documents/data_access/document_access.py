from django.db.models import Q
from ..models import Document


def get_rm_by_document(upload_id):
    document = Document.objects.get(upload_id=upload_id)
    customer = document.customer
    return customer.relationship_manager


def get_documents_by_customer(customer_id):
    return Document.objects.filter(customer_id=customer_id)


def get_document_by_upload_id(upload_id):
    return Document.objects.get(upload_id=upload_id)


def update_document_status_from_upload_id(upload_id, status):
    return Document.objects.filter(upload_id=upload_id).update(status=status)


def add_file_to_document(upload_id, file):
    return Document.objects.filter(upload_id=upload_id).update(file=file)


def get_customer_email_from_upload_id(upload_id):
    document = Document.objects.get(upload_id=upload_id)
    return document.customer.email


def get_file_from_upload_id(upload_id):
    document = Document.objects.get(upload_id=upload_id)
    return document.file


def create_document(customer, name, type, upload_id):
    return Document.objects.create(
        customer=customer, name=name, type=type, upload_id=upload_id
    )


def get_documents_filtered(relationship_manager_id, email=None, status="All", sort="desc"):
    query = Q(customer__relationship_manager_id=relationship_manager_id)

    if email:
        query &= Q(customer__email__icontains=email)

    if status and status != "All":
        query &= Q(status=status)

    if sort == "desc":
        ordering = "-created_at"
    else:
        ordering = "created_at"

    return (
        Document.objects.select_related("customer__relationship_manager")
        .filter(query)
        .order_by(ordering)
    )
