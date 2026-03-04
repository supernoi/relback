"""
Domain Entities for Relback.

Pure Python dataclasses — zero dependency on Django, Oracle, or any framework.
These represent the business concepts of the backup monitoring system.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


# ---------------------------------------------------------------------------
# Value Objects / Enums
# ---------------------------------------------------------------------------

class BackupStatusValue(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    WARNING = "WARNING"
    INTERRUPTED = "INTERRUPTED"  # RMAN backup stopped/aborted mid-run
    UNKNOWN = "UNKNOWN"


class BackupType(str, Enum):
    ARCHIVELOG = "ARCHIVELOG"
    DB_FULL = "DB FULL"
    DB_INCR = "DB INCR"
    RECVR_AREA = "RECVR AREA"
    BACKUPSET = "BACKUPSET"


class BackupDestination(str, Enum):
    DISK = "DISK"
    SBT_TAPE = "SBT_TAPE"


class PolicyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


# ---------------------------------------------------------------------------
# Core Entities
# ---------------------------------------------------------------------------

@dataclass
class ClientEntity:
    id_client: int
    name: str
    description: Optional[str] = None


@dataclass
class HostEntity:
    id_host: int
    hostname: str
    ip: str
    description: Optional[str] = None
    client_id: Optional[int] = None


@dataclass
class DatabaseEntity:
    id_database: int
    db_name: str
    dbid: int
    description: Optional[str] = None
    host_id: Optional[int] = None
    client_id: Optional[int] = None
    last_resync: Optional[datetime] = None


@dataclass
class BackupPolicyEntity:
    id_policy: int
    policy_name: str
    backup_type: BackupType
    destination: BackupDestination
    status: PolicyStatus
    minute: str
    hour: str
    day: str
    month: str
    day_week: str
    duration: int
    size_backup: str
    database_id: Optional[int] = None
    host_id: Optional[int] = None
    client_id: Optional[int] = None
    description: Optional[str] = None


@dataclass
class ScheduleEntry:
    id_schedule: int
    policy_id: int
    schedule_start: datetime
    policy_name: Optional[str] = None
    hostname: Optional[str] = None
    db_name: Optional[str] = None
    backup_type: Optional[str] = None


# ---------------------------------------------------------------------------
# Oracle RMAN Catalog Entities (read-only — never persisted by Django)
# ---------------------------------------------------------------------------

@dataclass
class BackupJobResult:
    """Represents a backup job result read from the Oracle RMAN Catalog."""
    db_name: str
    dbid: int
    status: BackupStatusValue
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    backup_type: Optional[str] = None
    output_bytes_display: Optional[str] = None
    time_taken_display: Optional[str] = None
    output_device_type: Optional[str] = None
    session_key: Optional[int] = None
    input_type: Optional[str] = None
    db_key: Optional[int] = None  # RC_BACKUP_JOB_DETAILS DB_KEY; used by Demo and detail view

    @property
    def is_ok(self) -> bool:
        return self.status == BackupStatusValue.COMPLETED

    @property
    def severity(self) -> str:
        """Returns a DaisyUI semantic severity token for UI badge rendering.

        Maps BackupStatusValue → DaisyUI badge variant name used in
        the ``backup_badge`` template tag (Interface Adapter layer).
        NEVER import UI framework names further inward than this property.
        """
        mapping = {
            BackupStatusValue.COMPLETED:   "success",
            BackupStatusValue.RUNNING:     "info",
            BackupStatusValue.WARNING:     "warning",
            BackupStatusValue.FAILED:      "error",
            BackupStatusValue.INTERRUPTED: "interrupted",
            BackupStatusValue.UNKNOWN:     "neutral",
        }
        return mapping.get(self.status, "neutral")


@dataclass
class BackupLogEntry:
    """One line of RMAN output from RC_RMAN_OUTPUT (read-only catalog entity)."""
    recid: int
    output: str
    stamp: Optional[int] = None


@dataclass
class DashboardStats:
    """Aggregated stats for the index page — computed, not stored."""
    clients_count: int
    hosts_count: int
    databases_count: int
    policies_count: int
    active_policies_count: int = 0
    failed_jobs_last_24h: int = 0
    successful_jobs_last_24h: int = 0


@dataclass
class SlaBreach:
    """
    Value object: a backup SLA breach — expected backup window had no successful job.

    Pure domain; no dependency on Django, Oracle, or notification transport.
    """
    db_name: str
    schedule_start: datetime
    policy_name: Optional[str] = None
    hostname: Optional[str] = None
    reason: str = "no_completed_backup_in_window"
