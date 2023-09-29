from django.views.generic.list import ListView
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
    FileResponse,
)
from django.shortcuts import render, get_object_or_404
from .models import (
    Customer,
    File,
    Notification,
    FileType,
    Document,
    UploadStatus,
    NotificationType,
    NotificationStatus,
)
from .forms import (
    FileUploadForm,
    DocumentRequestForm,
    DocumentFilterForm,
    NotificationFilterForm,
    CustomerFilterForm,
    CreateDocumentRequestForm,
)
from .data_access.customer_access import get_customer_by_email, get_customers_by_rm
from .data_access.document_access import (
    update_document_status_from_upload_id,
    get_documents_filtered,
    get_rm_by_document_upload_id,
    get_customer_email_from_upload_id,
    get_file_from_upload_id,
    add_file_to_document_from_upload_id,
    create_document,
)
from .data_access.notification_access import (
    create_notification,
    get_notifications_by_rm,
    update_notification_status,
    get_unread_notifications_by_rm_count,
    mark_all_notifications_read_by_rm,
)
from .data_access.email_template_access import get_email_template_by_file_type
from .utilities import (
    generate_upload_id,
    is_valid_upload_request,
    fill_email_template,
)
from .constants import RM_ID, FROM_EMAIL, EXPIRY_DAYS
import logging
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def upload_file(request, upload_id):
    if not is_valid_upload_request(upload_id=upload_id):
        return HttpResponse(f"Upload for request {upload_id} is no longer valid")
    # Submit Upload request
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = File(name=request.FILES["url"].name, url=request.FILES["url"])
            new_file.save()
            # Attach file to Document
            add_file_to_document_from_upload_id(upload_id=upload_id, file=new_file)
            # Update the status of the Document Request
            update_document_status_from_upload_id(
                upload_id=upload_id, status=UploadStatus.COMPLETED
            )
            # Create notification for RM of the customer
            create_notification(
                relationship_manager_id=get_rm_by_document_upload_id(
                    upload_id=upload_id
                ),
                type=NotificationType.FILE_UPLOAD.value,
                text=f"A new file has been uploaded by Customer {get_customer_email_from_upload_id(upload_id=upload_id)}",
            )
            return HttpResponse("Successfully Uploaded File.")
    # Render Upload form
    else:
        form = FileUploadForm()
    return render(request, "upload_file.html", {"form": form})


def create_document_request(request):
    if not request.method == "POST":
        return HttpResponseBadRequest("Bad Request")

    form = DocumentRequestForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        customer = get_customer_by_email(email=email)
        name = form.cleaned_data["name"]
        file_type = form.cleaned_data["file_type"]

        # Generate upload id and link
        upload_id = generate_upload_id()
        upload_link = request.build_absolute_uri(f"/documents/upload/{upload_id}")
        # Get email template and fill in placeholders
        email_template = get_email_template_by_file_type(file_type=file_type)
        subject = email_template.subject
        replacement_dict = {
            "upload_link": upload_link,
            "expire_days": EXPIRY_DAYS,
            "rm_name": customer.relationship_manager.name,
        }
        body = fill_email_template(email_template, replacement_dict)
        # Send email to customer
        email = EmailMessage(
            subject=subject, body=body, from_email=FROM_EMAIL, to=[email]
        )
        email.send()
        # Create the document object
        create_document(
            customer=customer,
            name=name,
            file_type=file_type,
            email_blurb=email.message().as_string(),
            upload_id=upload_id,
        )

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return HttpResponseBadRequest("Bad Request")


def download_document(request, upload_id):
    file = get_file_from_upload_id(upload_id=upload_id)
    # Return 404 to the user if they try to download a file that does not exist
    obj = get_object_or_404(File, id=file.pk)
    file_path = obj.url.path
    # Download file by setting as_attachment
    response = FileResponse(open(file_path, "rb"), as_attachment=True)
    return response


def mark_notification_read(request, notification_id):
    update_notification_status(
        notification_id=notification_id, status=NotificationStatus.READ
    )
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def mark_all_notifications_read(request):
    mark_all_notifications_read_by_rm(relationship_manager_id=RM_ID)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def get_unread_notification_count(request):
    unread_count = get_unread_notifications_by_rm_count(relationship_manager_id=RM_ID)
    return JsonResponse({"unread_count": unread_count})


class CustomerListView(ListView):
    model = Customer
    context_object_name = "customer_list"
    template_name = "customer_list.html"

    def get_queryset(self):
        # Unbound the form if there is not GET request data
        # https://medium.com/apollo-data-solutions-blog/django-initial-values-for-a-bound-form-fde7b363f79e
        # https://stackoverflow.com/questions/43091200/initial-not-working-on-form-inputs
        if len(self.request.GET):
            filter_form = CustomerFilterForm(self.request.GET)
        else:
            filter_form = CustomerFilterForm()
        if filter_form.is_valid():
            name_filter = filter_form.cleaned_data["name"]
            email_filter = filter_form.cleaned_data["email"]
            customer_list = get_customers_by_rm(
                relationship_manager_id=RM_ID, name=name_filter, email=email_filter
            )
        else:
            customer_list = get_customers_by_rm(relationship_manager_id=RM_ID)
        document_form = CreateDocumentRequestForm()
        return {
            "customer_list": customer_list,
            "filter_form": filter_form,
            "document_form": document_form,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["customer_list"] = queryset["customer_list"]
        context["filter_form"] = queryset["filter_form"]
        context["document_form"] = queryset["document_form"]
        context["UploadStatus"] = UploadStatus

        return context


class DocumentView(ListView):
    model = Document
    context_object_name = "document_list"
    template_name = "document_list.html"

    def get_queryset(self):
        # Unbound the form if there is not GET request data
        # https://medium.com/apollo-data-solutions-blog/django-initial-values-for-a-bound-form-fde7b363f79e
        # https://stackoverflow.com/questions/43091200/initial-not-working-on-form-inputs
        if len(self.request.GET):
            filter_form = DocumentFilterForm(self.request.GET)
        else:
            filter_form = DocumentFilterForm()

        if filter_form.is_valid():
            email_filter = filter_form.cleaned_data["email"]
            status_filter = filter_form.cleaned_data["status"]
            sort_filter = filter_form.cleaned_data["sort"]
            document_list = get_documents_filtered(
                relationship_manager_id=RM_ID,
                email=email_filter,
                status=status_filter,
                sort=sort_filter,
            )
        else:
            document_list = get_documents_filtered(relationship_manager_id=RM_ID)
        customers = get_customers_by_rm(relationship_manager_id=RM_ID)
        document_form = CreateDocumentRequestForm()
        return {
            "document_list": document_list,
            "customers": customers,
            "filter_form": filter_form,
            "document_form": document_form,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["filter_form"] = queryset["filter_form"]
        context["document_form"] = queryset["document_form"]
        context["document_list"] = queryset["document_list"]
        context["customers"] = queryset["customers"]
        context["UploadStatus"] = UploadStatus

        return context


class NotificationView(ListView):
    model = Notification
    context_object_name = "notification_list"
    template_name = "notification_list.html"
    queryset = get_notifications_by_rm(RM_ID)

    # Unbound the form if there is not GET request data
    # https://medium.com/apollo-data-solutions-blog/django-initial-values-for-a-bound-form-fde7b363f79e
    # https://stackoverflow.com/questions/43091200/initial-not-working-on-form-inputs
    def get_queryset(self):
        if len(self.request.GET):
            filter_form = NotificationFilterForm(self.request.GET)
        else:
            filter_form = NotificationFilterForm()

        if filter_form.is_valid():
            status_filter = filter_form.cleaned_data["status"]
            type_filter = filter_form.cleaned_data["type"]
            sort_filter = filter_form.cleaned_data["sort"]
            notification_list = get_notifications_by_rm(
                relationship_manager_id=RM_ID,
                status=status_filter,
                type=type_filter,
                sort=sort_filter,
            )
        else:
            notification_list = get_notifications_by_rm(relationship_manager_id=RM_ID)
        return {"notification_list": notification_list, "filter_form": filter_form}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["filter_form"] = queryset["filter_form"]
        context["notification_list"] = queryset["notification_list"]
        context["NotificationStatus"] = NotificationStatus

        return context
