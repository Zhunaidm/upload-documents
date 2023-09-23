from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from .models import Customer, File, Notification, FileType, Document, UploadStatusEnum
from .forms import FileUploadForm, DocumentRequestForm
from .data_access import is_document_invalid_status, get_document_by_url, get_customer_by_email, get_customers_by_rm,  create_notification, update_document_request_status_from_url, get_rm_by_document, get_notifications_by_rm, get_document_aggragated
from .utilities import generate_presigned_url,is_valid_url
import logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)
RM_ID = "1"


def check_valid_upload_request(id):
    if not is_valid_url(id):
        return False
    document = get_document_by_url(id)
    if document is None:
        return False  # Return False if the document_request is not found
    #  check if expired
    current_date = datetime.now()
    date_to_compare_datetime = datetime.combine(document.created_at, datetime.min.time())
    date_difference = current_date - date_to_compare_datetime
    if date_difference >= timedelta(days=7):
        return False
    return is_document_invalid_status(document)


def upload_file(request, request_id):
    if (not check_valid_upload_request(request_id)):
        return HttpResponse(f"Upload for request {request_id} is no longer valid")
    # Submit Upload request
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = File(
                name=form.cleaned_data['name'], url=request.FILES["url"])
            new_file.save()
            # Update the status of the Document Request
            update_document_request_status_from_url(
                request_id, UploadStatusEnum.COMPLETED)
            # Create notification for RM of the customer
            create_notification(id=get_rm_by_document(request_id), type="FileUpload",
                                text="A new file has been uploaded by Customer {}")
            return HttpResponse("Success")
    # Render Upload form
    else:
        form = FileUploadForm()
    return render(request, "upload_file.html", {"form": form})

def create_document_request(request):
    if request.method == "POST":
        form = DocumentRequestForm(request.POST)
        if form.is_valid():
            # Extract form data from the validated form
            email = form.cleaned_data['email']
            customer = get_customer_by_email(email)
            name = form.cleaned_data['name']
            type = form.cleaned_data['type']        
            new_document_request = Document(customer=customer, name=name, type=type, presigned_url=generate_presigned_url())
            new_document_request.save()
            return HttpResponse("Success")
    else:
        return HttpResponseBadRequest("Bad Request")


class CustomerListView(ListView):
    model = Customer
    context_object_name = "customer_list"
    template_name = "customer_list.html"

    def get_queryset(self):
        name_filter = self.request.GET.get("name")
        email_filter = self.request.GET.get("email")
        new_context = get_customers_by_rm(
            RM_ID, name=name_filter, email=email_filter)
        return new_context


class DocumentRequestView(ListView):
    model = Document
    context_object_name = "document_list"
    template_name = "documentrequest_list.html"

    def get_queryset(self):
        email_filter = self.request.GET.get('email')
        status_filter = self.request.GET.get('status')
        document_list = get_document_aggragated(
            RM_ID, email=email_filter, status=status_filter)
        customers = get_customers_by_rm(RM_ID)
        return {"document_list": document_list, "customers": customers}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["document_list"] = queryset['document_list']
        context["document_types"] =  [{"name": item.name, "value": item.value} for item in FileType]
        context["customers"] = queryset['customers']

        return context


class NotificationView(ListView):
    model = Notification
    context_object_name = "notification_list"
    queryset = get_notifications_by_rm(RM_ID)
