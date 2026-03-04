"""
REST API views for backup audit (Phase 17).

Endpoints call use cases and return JSON; no Django models in the response.
"""
import datetime

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from coreRelback.views import _get_rman_repo
from coreRelback.services.use_cases import AuditBackupUseCase
from .serializers import (
    BackupJobResultSerializer,
    AuditSummarySerializer,
    backup_job_to_dict,
    build_audit_summary,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def backup_audit_list(request):
    """
    List backup job results from the audit use case (Oracle RMAN or demo).

    Query params (optional):
        from_date: ISO date (YYYY-MM-DD)
        to_date: ISO date (YYYY-MM-DD)
        db_name: filter by database name

    Returns JSON: { "jobs": [...], "summary": { "total", "successful", "failed", "running", "oracle_available" } }
    """
    from_date = request.query_params.get("from_date")
    to_date = request.query_params.get("to_date")
    db_name = request.query_params.get("db_name") or None

    from_dt = None
    to_dt = None
    if from_date:
        try:
            from_dt = datetime.datetime.strptime(from_date, "%Y-%m-%d").replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        except ValueError:
            pass
    if to_date:
        try:
            to_dt = datetime.datetime.strptime(to_date, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        except ValueError:
            pass

    # When no Oracle (e.g. ORACLE_CATALOG=None), use case returns []; summary still returned
    repo = _get_rman_repo()
    jobs = AuditBackupUseCase(repo).execute(
        db_name=db_name, from_date=from_dt, to_date=to_dt
    )
    oracle_available = bool(jobs)

    jobs_data = [backup_job_to_dict(j) for j in jobs]
    summary = build_audit_summary(jobs, oracle_available)

    jobs_serializer = BackupJobResultSerializer(jobs_data, many=True)
    summary_serializer = AuditSummarySerializer(summary)

    return Response({
        "jobs": jobs_serializer.data,
        "summary": summary_serializer.data,
    })
