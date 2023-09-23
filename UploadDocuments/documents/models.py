from django.db import models
from enum import Enum

NAME_MAX_LENGTH = 100

class UploadStatusEnum(models.IntegerChoices):
    PENDING = (1, "pending")
    COMPLETED = (2, "completed")
    EXPIRED = (3, "expired")
    REVOKED = (4, "revoked")

class FileType(Enum):
    ID = "Identity Document"
    ADDRESS = "Proof of Address"
    OTHER = "Other"

class RelationshipManager(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)

class Customer(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    email = models.EmailField()
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.CASCADE)
    
class File(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    url = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    email_blurb = models.CharField(max_length=1000, default="")
    type = models.CharField(max_length=30)
    status = models.IntegerField(
        choices=UploadStatusEnum.choices, default=UploadStatusEnum.PENDING)    
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    presigned_url = models.UUIDField()
    created_at = models.DateField(auto_now_add=True)


class Notification(models.Model):
    relationship_manager = models.ForeignKey(
        RelationshipManager, on_delete=models.CASCADE)
    type = models.CharField(max_length=NAME_MAX_LENGTH)
    text = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
