from django.db.models import Q
from ..models import Customer


def get_customers_by_rm(relationship_manager, name=None, email=None):
    query = Q(relationship_manager=relationship_manager)
    if name:
        query &= Q(name__icontains=name)
    if email:
        query &= Q(email__icontains=email)
    return Customer.objects.filter(query)


def get_customer_by_email(email):
    return Customer.objects.get(email=email)
