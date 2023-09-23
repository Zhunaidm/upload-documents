from django.db import models

class UploadStatusEnum(models.IntegerChoices):
    PENDING = (1, "pending")
    UPLOADED = (2, "uploaded")

class UploadUrlEnum(models.IntegerChoices):
    PENDING = (1, "pending")
    COMPLETED = (2, "completed")
    EXPIRED = (3, "expired")
    REVOKED = (4, "revoked")

class RelationshipManager(models.Model):
    name = models.CharField(max_length=30)

class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=10)
    relationship_manager = models.ForeignKey(RelationshipManager, on_delete=models.CASCADE)

class File(models.Model):
    name = models.CharField(max_length=30)
    url = models.FileField(upload_to ='uploads/')
    #upload_date = models.DateTimeField(auto_now_add=True)    

class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

class DocumentRequest(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    blurb = models.CharField(max_length=1000)
    status = models.IntegerField(choices=UploadStatusEnum.choices, default=UploadStatusEnum.PENDING)
    presigned_url = models.CharField(max_length=100)
    created_at = models.DateField()    





