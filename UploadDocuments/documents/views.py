from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render
from .models import Customer, Document, DocumentRequest, File
from .forms import FileUploadForm
from .models import UploadUrlEnum
import logging
logger = logging.getLogger(__name__)
RM_ID = "1"

def get_customers_by_rm(relationship_manager):
    return Customer.objects.filter(relationship_manager=relationship_manager)

def get_documents_by_customer(customer_id):
    return Document.objects.filter(customer_id=customer_id)

def get_document_requests(customer_id):
    return DocumentRequest.objects.filter(customer_id=customer_id)

def update_document_request_status(id, status):
    return DocumentRequest.objects.filter(presigned_url=id).update(status=status)

def is_document_request_invalid_status(document_request):
    return document_request.status == UploadUrlEnum.PENDING

def check_valid_upload_request(id):
    document_request = DocumentRequest.objects.filter(presigned_url=id)
    if not document_request.exists():
        return False  # Return False if the document_request is not found    
    logger.warning(document_request)
    return is_document_request_invalid_status(document_request)


def upload_file(request, request_id):
    if (not check_valid_upload_request(request_id)):
        return HttpResponse(f"Upload for request {request_id} is no longer valid")
    # Submit Upload request
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = File(name=form.cleaned_data['name'], url=request.FILES["url"])
            new_file.save()
            return HttpResponse("Success")
    # Render Upload form
    else:
        form = FileUploadForm()
    return render(request, "upload_file.html", {"form": form})


class CustomerListView(ListView):
    model = Customer
    context_object_name = "customer_list"
    queryset = get_customers_by_rm(RM_ID)
    
class DocumentRequestView(ListView):
    model = DocumentRequest
    context_object_name = "document_list"
    queryset = get_customers_by_rm(RM_ID)
   