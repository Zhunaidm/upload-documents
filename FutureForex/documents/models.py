from django.db import models
from enum import Enum
from .constants import CHAR_MAX_LENGTH


class UploadStatusEnum(models.IntegerChoices):
    PENDING = (1, "Pending")
    COMPLETED = (2, "Completed")


class FileType(models.IntegerChoices):
    ID = (1, "Identity Document")
    ADDRESS = (2, "Proof of Address")
    OTHER = (3, "Other")


class NotificationType(models.IntegerChoices):
    FILE_UPLOAD = (1, "FileUpload")


class NotificationStatus(models.IntegerChoices):
    UNREAD = (1, "Unread")
    READ = (2, "Read")


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class RelationshipManager(BaseModel):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)


class Customer(BaseModel):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    email = models.EmailField(unique=True)
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.SET_NULL, null=True
    )


class File(BaseModel):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    url = models.FileField(upload_to="uploads/")


class Document(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    # Unused for now. Can contain the email text sent to the Customer
    email_blurb = models.TextField()
    type = models.IntegerField(choices=NotificationType.choices)
    status = models.IntegerField(
        choices=UploadStatusEnum.choices, default=UploadStatusEnum.PENDING
    )
    file = models.ForeignKey(File, on_delete=models.SET_NULL, blank=True, null=True)
    upload_id = models.UUIDField(unique=True)


class Notification(BaseModel):
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.CASCADE
    )
    type = models.IntegerField(choices=NotificationType.choices)
    text = models.TextField()
    status = models.IntegerField(
        choices=NotificationStatus.choices, default=NotificationStatus.UNREAD
    )
