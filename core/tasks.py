from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from project.celery import app # Import the celery app

@app.task
def send_login_notification(user_id, user_email):
    """
    Sends a notification to the user's channel group.
    """
    message = f"Welcome back, {user_email}! You have successfully logged in (via Celery)."

    # 1. Log to the Celery worker console
    print(f"CELERY TASK (console): Sending notification to user {user_id}")

    # 2. Send notification to the browser via Channels
    channel_layer = get_channel_layer()
    group_name = f'notifications_{user_id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send.notification',
            'message': message
        }
    )