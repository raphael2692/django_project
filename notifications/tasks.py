# notifications/tasks.py
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def send_login_notification(user_id, message):
    """
    Sends a notification to a specific user's notification channel.
    """
    channel_layer = get_channel_layer()
    # The group name is now dynamically created based on the user's ID.
    group_name = f"user_{user_id}_notifications"
    
    # The notification is sent to the user-specific group.
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
        },
    )