"""
Notification gateway implementations for SLA alerts.

Implementations of INotificationGateway — send_sla_breaches must not raise;
failures are logged and swallowed so the use case / command can complete.
"""
import json
import logging
from typing import List

from django.conf import settings

from coreRelback.domain.entities import SlaBreach
from coreRelback.gateways.interfaces import INotificationGateway

logger = logging.getLogger(__name__)


class StubNotificationGateway(INotificationGateway):
    """No-op implementation: logs breaches only. Use when no alert channel is configured."""

    def send_sla_breaches(self, breaches: List[SlaBreach]) -> None:
        if breaches:
            logger.warning(
                "SLA breaches (stub — not sent): %d — %s",
                len(breaches),
                [b.db_name for b in breaches],
            )


class WebhookNotificationGateway(INotificationGateway):
    """
    POSTs a JSON payload to a configurable URL (e.g. Slack, PagerDuty, custom endpoint).

    URL from settings.SLA_ALERT_WEBHOOK_URL. If empty, no request is sent.
    """

    def send_sla_breaches(self, breaches: List[SlaBreach]) -> None:
        url = getattr(settings, "SLA_ALERT_WEBHOOK_URL", None) or ""
        if not url or not breaches:
            if breaches and not url:
                logger.warning("SLA_ALERT_WEBHOOK_URL not set — %d breach(es) not sent", len(breaches))
            return
        try:
            import urllib.request
            payload = {
                "breaches": [
                    {
                        "db_name": b.db_name,
                        "schedule_start": b.schedule_start.isoformat() if b.schedule_start else None,
                        "policy_name": b.policy_name,
                        "hostname": b.hostname,
                        "reason": b.reason,
                    }
                    for b in breaches
                ],
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status >= 400:
                    logger.warning("Webhook returned %s for SLA alert", resp.status)
        except Exception as exc:
            logger.exception("Webhook SLA alert failed: %s", exc)
