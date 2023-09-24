from django.db.models import Q
from ..models import Notification


def create_notification(id, type, text):
    return Notification.objects.create(relationship_manager=id, type=type, text=text)


def update_notification_status(id, read):
    return Notification.objects.filter(pk=id).update(read=read)


def mark_all_rm_notifications_read(id):
    return Notification.objects.filter(relationship_manager=id).update(read=True)


def get_notifications_by_rm(id, read="All", sort="desc"):
    query = Q(relationship_manager=id)
    if read and read != "All":
        query &= Q(read=read)
    if sort == "desc":
        ordering = "-created_at"
    else:
        ordering = "created_at"
    return Notification.objects.filter(query).order_by(ordering)


def get_unread_notifications_by_rm_count(id):
    return Notification.objects.filter(relationship_manager=id, read=False).count()
