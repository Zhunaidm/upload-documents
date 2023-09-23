from django.db.models import Q
from ..models import Document


def get_rm_by_document(url):
    document = Document.objects.get(presigned_url=url)
    customer = document.customer
    return customer.relationship_manager


def get_documents_by_customer(customer_id):
    return Document.objects.filter(customer_id=customer_id)


def get_document_by_url(url):
    return Document.objects.filter(presigned_url=url).first()


def update_document_status_from_url(url, status):
    return Document.objects.filter(presigned_url=url).update(status=status)


def add_file_to_document(url, file):
    return Document.objects.filter(presigned_url=url).update(file=file)


def get_customer_email_from_url(url):
    document = Document.objects.get(presigned_url=url)
    return document.customer.email


def get_file_from_url(url):
    document = Document.objects.get(presigned_url=url)
    return document.file


def get_documents_filtered(id, email=None, status="All", sort="desc"):
    query = Q(customer__relationship_manager_id=id)

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
