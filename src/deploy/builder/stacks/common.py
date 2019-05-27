from django.db.models import signals

# from .models import Stack
from .tasks import build_stack


def user_post_save(sender, instance, signal, *args, **kwargs):
    build_stack.delay(instance.pk)


def connect(sender):
    signals.post_save.connect(user_post_save, sender=sender)
