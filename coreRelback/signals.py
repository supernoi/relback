from django.db.models.signals import post_save
from django.dispatch import receiver
from coreRelback.models import BackupPolicy
from coreRelback.services.schedule_generator import generate_schedules

@receiver(post_save, sender=BackupPolicy)
def update_schedules_on_policy_save(sender, instance, **kwargs):
    generate_schedules()
