from django.db.models import signals

from .tasks import process_stack_task


def process_stack_callback(sender, instance, signal, *args, **kwargs):
    process_stack_task.delay(instance.pk)


def connect(sender):
    signals.post_save.connect(process_stack_callback, sender=sender)
