from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Customer, File, Notification, FileType, Document, UploadStatusEnum, NotificationType
from .forms import FileUploadForm, DocumentRequestForm
from .data_access.customer_access import get_customer_by_email, get_customers_by_rm
from .data_access.document_access import update_document_status_from_url, get_documents_filtered, get_rm_by_document, get_customer_email_from_url
from .data_access.notification_access import create_notification, get_notifications_by_rm, update_notification_status, get_unread_notifications_by_rm_count, mark_all_rm_notifications_read
from .utilities import generate_presigned_url, check_valid_upload_request
import logging

logger = logging.getLogger(__name__)
RM_ID = "1"

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
            update_document_status_from_url(
                request_id, UploadStatusEnum.COMPLETED)
            # Create notification for RM of the customer
            create_notification(id=get_rm_by_document(request_id), type=NotificationType.FILE_UPLOAD.value,
                                text=f"A new file has been uploaded by Customer {get_customer_email_from_url(request_id)}")
            return HttpResponse("Successfully Uploaded File.")
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
            new_document_request = Document(
                customer=customer, name=name, type=type, presigned_url=generate_presigned_url())
            new_document_request.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseBadRequest("Bad Request")
    
def mark_notification_read(request, notification_id):
    update_notification_status(id=notification_id, read=True)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def mark_all_notifications_read(request):
    mark_all_rm_notifications_read(id=RM_ID)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def get_unread_notification_count(request):
    unread_count = get_unread_notifications_by_rm_count(id=RM_ID)
    return JsonResponse({"unread_count" : unread_count})

class CustomerListView(ListView):
    model = Customer
    context_object_name = "customer_list"
    template_name = "customer_list.html"

    def get_queryset(self):
        name_filter = self.request.GET.get("name")
        email_filter = self.request.GET.get("email")
        return get_customers_by_rm(
            RM_ID, name=name_filter, email=email_filter)


class DocumentRequestView(ListView):
    model = Document
    context_object_name = "document_list"
    template_name = "document_list.html"

    def get_queryset(self):
        email_filter = self.request.GET.get('email')
        status_filter = self.request.GET.get('status')
        document_list = get_documents_filtered(
            RM_ID, email=email_filter, status=status_filter)
        customers = get_customers_by_rm(RM_ID)
        return {"document_list": document_list, "customers": customers}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["document_list"] = queryset['document_list']
        context["document_types"] = [
            {"name": item.name, "value": item.value} for item in FileType]
        context["customers"] = queryset['customers']

        return context


class NotificationView(ListView):
    model = Notification
    context_object_name = "notification_list"
    template_name = "notification_list.html"
    queryset = get_notifications_by_rm(RM_ID)
    def get_queryset(self):
        read_filter = self.request.GET.get("read")
        return get_notifications_by_rm(RM_ID, read=read_filter)
