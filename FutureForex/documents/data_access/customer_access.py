from django.db.models import Q
from ..models import Customer


# Get
def get_customer_by_email(email):
    try:
        return Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return None


# Filter
def get_customers_by_rm(relationship_manager_id, name=None, email=None):
    query = Q(relationship_manager=relationship_manager_id)
    if name:
        query &= Q(name__icontains=name)
    if email:
        query &= Q(email__icontains=email)
    return Customer.objects.filter(query)
