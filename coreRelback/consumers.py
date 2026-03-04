"""
WebSocket consumers for real-time Reports (Phase 18).

Emits backup job state as JSON at connect and every N seconds.
"""
import asyncio
import json
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


def _get_jobs_payload():
    """
    Sync: run AuditBackupUseCase and return JSON-serializable dict
    { "jobs": [...], "summary": {...}, "oracle_available": bool }.
    """
    from django.conf import settings
    from coreRelback.views import _get_rman_repo
    from coreRelback.services.use_cases import AuditBackupUseCase
    from coreRelback.domain.entities import BackupStatusValue

    from_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    to_dt = datetime.datetime.now()
    repo = _get_rman_repo()
    backup_jobs = AuditBackupUseCase(repo).execute(from_date=from_dt, to_date=to_dt)
    oracle_available = bool(backup_jobs)

    if backup_jobs:
        today = datetime.date.today()
        jobs_data = []
        for j in backup_jobs:
            status_str = j.status.value if hasattr(j.status, "value") else str(j.status)
            jobs_data.append({
                "policy_name": j.input_type or "-",
                "hostname": j.db_name,
                "db_name": j.db_name,
                "backup_type": j.backup_type or j.input_type or "-",
                "start_time": j.start_time.isoformat() if j.start_time else None,
                "end_time": j.end_time.isoformat() if j.end_time else None,
                "status": status_str,
                "time_taken_display": j.time_taken_display,
                "output_bytes_display": j.output_bytes_display,
                "session_key": j.session_key or 0,
            })
        successful = sum(1 for j in backup_jobs if j.status == BackupStatusValue.COMPLETED)
        failed = sum(
            1 for j in backup_jobs
            if j.status in (BackupStatusValue.FAILED, BackupStatusValue.INTERRUPTED)
        )
        running = sum(1 for j in backup_jobs if j.status == BackupStatusValue.RUNNING)
        today_count = sum(
            1 for j in backup_jobs
            if j.start_time and j.start_time.date() == today
        )
    else:
        jobs_data = []
        successful = failed = running = today_count = 0

    return {
        "jobs": jobs_data,
        "summary": {
            "total": len(jobs_data),
            "successful": successful,
            "failed": failed,
            "running": running,
            "today_jobs": today_count,
        },
        "oracle_available": oracle_available,
    }


class ReportsJobsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket endpoint: sends backup jobs payload on connect and every INTERVAL_SEC.
    """

    INTERVAL_SEC = 30

    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return
        await self.accept()
        await self._send_payload()
        self._task = asyncio.create_task(self._periodic_send())

    async def disconnect(self, close_code):
        if getattr(self, "_task", None):
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _send_payload(self):
        payload = await sync_to_async(_get_jobs_payload)()
        await self.send(text_data=json.dumps(payload))

    async def _periodic_send(self):
        while True:
            await asyncio.sleep(self.INTERVAL_SEC)
            await self._send_payload()
