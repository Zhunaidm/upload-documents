from django.urls import path

from .views import CustomerListView, DocumentRequestView, upload_file, NotificationView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url='/documents/customers/')),
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("documents/", DocumentRequestView.as_view(), name="document_list"),
    path("notifications/", NotificationView.as_view(), name="notification_list"),
    path("upload/<str:request_id>", upload_file, name="upload_file"),
]

# Serve File uploads locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
