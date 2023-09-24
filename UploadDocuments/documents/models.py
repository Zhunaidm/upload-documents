from django.db import models
from enum import Enum
from .constants import CHAR_MAX_LENGTH, LARGE_CHAR_MAX_LENGTH


class UploadStatusEnum(models.IntegerChoices):
    PENDING = (1, "pending")
    COMPLETED = (2, "completed")


class FileType(Enum):
    ID = "Identity Document"
    ADDRESS = "Proof of Address"
    OTHER = "Other"


class NotificationType(Enum):
    FILE_UPLOAD = "FileUpload"


class RelationshipManager(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    email = models.EmailField(unique=True)
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    url = models.FileField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    # Unused for now. Can contain the email text sent to the Customer
    email_blurb = models.CharField(max_length=LARGE_CHAR_MAX_LENGTH, default="")
    type = models.CharField(max_length=CHAR_MAX_LENGTH)
    status = models.IntegerField(
        choices=UploadStatusEnum.choices, default=UploadStatusEnum.PENDING
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    presigned_url = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.CASCADE
    )
    type = models.CharField(max_length=CHAR_MAX_LENGTH)
    text = models.CharField(max_length=LARGE_CHAR_MAX_LENGTH)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
