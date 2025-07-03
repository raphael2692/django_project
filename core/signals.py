from django.dispatch import receiver
from allauth.account.signals import user_logged_in
# Import the new task
from .tasks import send_login_notification

@receiver(user_logged_in)
def user_logged_in_receiver(request, user, **kwargs):
    """
    Handles post-login signals by dispatching a Celery task.
    """
    # Log to the Django console immediately
    print(f"SIGNAL (console): User {user.email} logged in. Dispatching Celery task.")

    # Call the Celery task to run in the background
    send_login_notification.delay(user.id, user.email)