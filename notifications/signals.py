# notifications/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .tasks import send_login_notification

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    When a user logs in, a Celery task is dispatched to send a notification.
    """
    message = f"User {user.email} just logged in."
    # The user's ID is passed to the Celery task.
    send_login_notification.delay(user.id, message)