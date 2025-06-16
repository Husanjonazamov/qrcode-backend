from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.api.models import GenerateModel


@receiver(post_save, sender=GenerateModel)
def GenerateSignal(sender, instance, created, **kwargs): ...
