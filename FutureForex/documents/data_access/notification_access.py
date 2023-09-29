from django.db.models import Q
from ..models import Notification


def create_notification(relationship_manager_id, type, text):
    return Notification.objects.create(
        relationship_manager=relationship_manager_id, type=type, text=text
    )


def update_notification_status(notification_id, read):
    return Notification.objects.filter(pk=notification_id).update(read=read)


def mark_all_rm_notifications_read(relationship_manager_id):
    return Notification.objects.filter(
        relationship_manager=relationship_manager_id
    ).update(read=True)


def get_notifications_by_rm(relationship_manager_id, read="All", sort="desc"):
    query = Q(relationship_manager=relationship_manager_id)
    if read and read != "All":
        query &= Q(read=read)
    if sort == "desc":
        ordering = "-created_at"
    else:
        ordering = "created_at"
    return Notification.objects.filter(query).order_by(ordering)


def get_unread_notifications_by_rm_count(relationship_manager_id):
    return Notification.objects.filter(
        relationship_manager=relationship_manager_id, read=False
    ).count()
