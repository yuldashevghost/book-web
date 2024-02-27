from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.books.models import BookReview
from apps.books.tasks import send_email


@receiver(post_save, sender=BookReview)
def send_email_author(sender, instance, created, **kwargs):
    if created:
        send_email.delay("")