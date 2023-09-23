from django.db.models import Q
from ..models import Notification

def create_notification(id, type, text):
    return Notification.objects.create(relationship_manager=id, type=type, text=text)

def update_notification_status(id, read):
    return Notification.objects.filter(pk=id).update(read=read)

def get_notifications_by_rm(id, type=None, text=None, read="All"):
    query = Q(relationship_manager=id)
    if type:
        query &= Q(type=type)
    if text:
        query &= Q(text__icontains=text)    
    if read and read != 'All':
        query &= Q(read=read)    
    return Notification.objects.filter(query)

def get_unread_notifications_by_rm_count(id):
     return Notification.objects.filter(relationship_manager=id, read=False).count()
