from django.db import models
from enum import Enum
from .constants import CHAR_MAX_LENGTH


class UploadStatusEnum(models.IntegerChoices):
    PENDING = (1, "pending")
    COMPLETED = (2, "completed")


class FileType(Enum):
    ID = "Identity Document"
    ADDRESS = "Proof of Address"
    OTHER = "Other"


class NotificationType(Enum):
    FILE_UPLOAD = "FileUpload"


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
        RelationshipManager, on_delete=models.CASCADE
    )


class File(BaseModel):
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    url = models.FileField(upload_to="uploads/")


class Document(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    # Unused for now. Can contain the email text sent to the Customer
    email_blurb = models.TextField()
    type = models.CharField(max_length=CHAR_MAX_LENGTH)
    status = models.IntegerField(
        choices=UploadStatusEnum.choices, default=UploadStatusEnum.PENDING
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    upload_id = models.UUIDField(unique=True)


class Notification(BaseModel):
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.CASCADE
    )
    type = models.CharField(max_length=CHAR_MAX_LENGTH)
    text = models.TextField()
    read = models.BooleanField(default=False)
