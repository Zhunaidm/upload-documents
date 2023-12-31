from django.urls import path

from .views import (
    CustomerListView,
    DocumentView,
    NotificationView,
    upload_file,
    create_document_request,
    mark_notification_read,
    get_unread_notification_count,
    mark_all_notifications_read,
    download_document,
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/documents/customers/")),
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("documents/", DocumentView.as_view(), name="document_list"),
    path("documents/create", create_document_request, name="create_document_request"),
    path("documents/download/<str:url>", download_document, name="download_document"),
    path("notifications/", NotificationView.as_view(), name="notification_list"),
    path(
        "notifications/read/<str:notification_id>/",
        mark_notification_read,
        name="mark_notification_read",
    ),
    path(
        "notifications/read/all>",
        mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
    path(
        "notifications/unread/",
        get_unread_notification_count,
        name="get_unread_notification_count",
    ),
    path("upload/<str:request_id>", upload_file, name="upload_file"),
]

# Serve File uploads locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
