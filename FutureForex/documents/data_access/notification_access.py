from django.db.models import Q
from ..models import Notification, NotificationStatus


# Filter
def get_notifications_by_rm(
    relationship_manager_id, status="All", type="All", sort="desc"
):
    query = Q(relationship_manager=relationship_manager_id)
    if status and status != "All":
        query &= Q(status=status)
    if type and type != "All":
        query &= Q(type=type)
    if sort == "desc":
        ordering = "-created_at"
    else:
        ordering = "created_at"
    return Notification.objects.filter(query).order_by(ordering)


def get_unread_notifications_by_rm_count(relationship_manager_id):
    return Notification.objects.filter(
        relationship_manager=relationship_manager_id, status=NotificationStatus.UNREAD
    ).count()


# Create
def create_notification(relationship_manager_id, type, text):
    return Notification.objects.create(
        relationship_manager=relationship_manager_id, type=type, text=text
    )


# Update
def update_notification_status(notification_id, status):
    return Notification.objects.filter(pk=notification_id).update(status=status)


def mark_all_notifications_read_by_rm(relationship_manager_id):
    return Notification.objects.filter(
        relationship_manager=relationship_manager_id
    ).update(status=NotificationStatus.READ)
