import logging
from datetime import timedelta

from django.utils.timezone import now



def db_cleaning_manager():
    """Cleaner function for old db objects"""
    from Admin.models import Message

    threshold_date = now() - timedelta(days=7)  # Delete data older than 7 days
    deleted_count, _ = Message.objects.filter(created_at__lt=threshold_date).delete()
    logging.info(f"Deleted {deleted_count} old messages")

    return deleted_count
