from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render
from .models import Customer, DocumentRequest, File, Notification, Document
from .forms import FileUploadForm
from .data_access import is_document_request_invalid_status, get_customers_by_rm,  create_notification, update_document_request_status_from_url, UploadUrlEnum, get_rm_by_document_request, get_notifications_by_rm, get_document_requests_aggragated
import logging
logger = logging.getLogger(__name__)
RM_ID = "1"


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
            new_file = File(
                name=form.cleaned_data['name'], url=request.FILES["url"])
            new_file.save()
            # Update the status of the Document Request
            update_document_request_status_from_url(
                request_id, UploadUrlEnum.COMPLETED)
            # Create notification for RM of the customer
            create_notification(id=get_rm_by_document_request(request_id), type="FileUpload",
                                text="A new file has been uploaded by Customer {}")
            return HttpResponse("Success")
    # Render Upload form
    else:
        form = FileUploadForm()
    return render(request, "upload_file.html", {"form": form})


class CustomerListView(ListView):
    model = Customer
    context_object_name = "customer_list"
    template_name = "customer_list.html"
    paginate_by = 10

    def get_queryset(self):
        name_filter = self.request.GET.get("name")
        email_filter = self.request.GET.get("email")
        new_context = get_customers_by_rm(
            RM_ID, name=name_filter, email=email_filter)
        return new_context


class DocumentRequestView(ListView):
    model = DocumentRequest
    context_object_name = "document_list"
    template_name = "documentrequest_list.html"
    paginate_by = 10

    def get_queryset(self):
        email_filter = self.request.GET.get('email')
        status_filter = self.request.GET.get('status')
        new_context = get_document_requests_aggragated(
            RM_ID, email=email_filter, status=status_filter)
        return new_context


class NotificationView(ListView):
    model = Notification
    context_object_name = "notification_list"
    queryset = get_notifications_by_rm(RM_ID)
