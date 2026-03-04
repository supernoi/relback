"""
Management command: check_backup_sla

Runs CheckBackupSlaUseCase for the given date range and sends alerts for any SLA breaches.
Use from cron or a scheduler (e.g. daily after backup windows close).

Usage:
    python manage.py check_backup_sla
    python manage.py check_backup_sla --days 2
    python manage.py check_backup_sla --dry-run   # no notification sent, only stdout
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from coreRelback.gateways.repositories import DjangoScheduleRepository
from coreRelback.gateways.notifications import StubNotificationGateway, WebhookNotificationGateway
from coreRelback.services.use_cases import CheckBackupSlaUseCase


def _get_rman_repo():
    from coreRelback.gateways.repositories import DemoRmanRepository, OracleRmanRepository
    if getattr(settings, "DEMO_MODE", False):
        return DemoRmanRepository()
    return OracleRmanRepository()


def _get_notification_gateway():
    if getattr(settings, "SLA_ALERT_WEBHOOK_URL", None):
        return WebhookNotificationGateway()
    return StubNotificationGateway()


class Command(BaseCommand):
    help = "Check backup SLA for the last N days and send alerts for breaches."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=1,
            help="Number of days to check (default: 1).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only print breaches; do not send notifications.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]

        schedule_repo = DjangoScheduleRepository()
        rman_repo = _get_rman_repo()
        use_case = CheckBackupSlaUseCase(schedule_repo=schedule_repo, rman_repo=rman_repo)

        breaches = use_case.execute(days=days)

        if not breaches:
            self.stdout.write(self.style.SUCCESS("No SLA breaches."))
            return

        self.stdout.write(self.style.WARNING(f"SLA breaches: {len(breaches)}"))
        for b in breaches:
            self.stdout.write(f"  - {b.db_name} @ {b.schedule_start} ({b.policy_name or '?'})")

        if not dry_run:
            gateway = _get_notification_gateway()
            gateway.send_sla_breaches(breaches)
            self.stdout.write("Notification sent.")
        else:
            self.stdout.write("Dry run — no notification sent.")
