"""
REST API serializers for backup audit (Phase 17).

Serialization is from domain entities (BackupJobResult) to JSON only;
no Django models in the public API contract.
"""
from rest_framework import serializers


class BackupJobResultSerializer(serializers.Serializer):
    """Read-only representation of a backup job from the audit use case."""

    db_name = serializers.CharField()
    dbid = serializers.IntegerField()
    status = serializers.CharField()
    start_time = serializers.DateTimeField(allow_null=True)
    end_time = serializers.DateTimeField(allow_null=True)
    backup_type = serializers.CharField(allow_null=True)
    output_bytes_display = serializers.CharField(allow_null=True)
    time_taken_display = serializers.CharField(allow_null=True)
    output_device_type = serializers.CharField(allow_null=True)
    session_key = serializers.IntegerField(allow_null=True)
    input_type = serializers.CharField(allow_null=True)
    severity = serializers.CharField(allow_null=True)


class AuditSummarySerializer(serializers.Serializer):
    """Read-only summary counts for the backup audit response."""

    total = serializers.IntegerField()
    successful = serializers.IntegerField()
    failed = serializers.IntegerField()
    running = serializers.IntegerField()
    oracle_available = serializers.BooleanField()


def backup_job_to_dict(job):
    """Map a BackupJobResult entity to a dict for BackupJobResultSerializer."""
    status_str = job.status.value if hasattr(job.status, "value") else str(job.status)
    return {
        "db_name": job.db_name,
        "dbid": job.dbid,
        "status": status_str,
        "start_time": job.start_time,
        "end_time": job.end_time,
        "backup_type": job.backup_type,
        "output_bytes_display": job.output_bytes_display,
        "time_taken_display": job.time_taken_display,
        "output_device_type": job.output_device_type,
        "session_key": job.session_key,
        "input_type": job.input_type,
        "severity": job.severity,
    }


def build_audit_summary(jobs, oracle_available):
    """Build summary dict from list of BackupJobResult and oracle_available flag."""
    from coreRelback.domain.entities import BackupStatusValue

    successful = sum(1 for j in jobs if j.status == BackupStatusValue.COMPLETED)
    failed = sum(
        1 for j in jobs
        if j.status in (BackupStatusValue.FAILED, BackupStatusValue.INTERRUPTED)
    )
    running = sum(1 for j in jobs if j.status == BackupStatusValue.RUNNING)
    return {
        "total": len(jobs),
        "successful": successful,
        "failed": failed,
        "running": running,
        "oracle_available": oracle_available,
    }
