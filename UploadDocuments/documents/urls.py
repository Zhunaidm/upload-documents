from django.urls import path

from .views import CustomerListView, DocumentRequestView, upload_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer_list"),
    path("requests", DocumentRequestView.as_view(), name="document_list"),
    path("upload/<str:request_id>", upload_file, name="upload_file"),   
]

# Serve File uploads locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
