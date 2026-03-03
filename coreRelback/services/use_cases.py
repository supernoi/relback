"""
Use Cases (Interactors) for Relback.

Each class represents ONE business action following the Single Responsibility Principle.
They receive gateway interfaces (never ORM models directly) and return domain entities.
Views are the only callers of these classes.
"""
import datetime
from typing import List, Optional

from coreRelback.domain.entities import (
    BackupJobResult,
    BackupLogEntry,
    BackupPolicyEntity,
    BackupStatusValue,
    ClientEntity,
    DatabaseEntity,
    DashboardStats,
    HostEntity,
    ScheduleEntry,
)
from coreRelback.gateways.interfaces import (
    IBackupPolicyRepository,
    IClientRepository,
    IDatabaseRepository,
    IHostRepository,
    IOracleRmanRepository,
    IScheduleRepository,
)


class GetDashboardStatsUseCase:
    """Returns aggregated stats for the dashboard index page."""

    def __init__(
        self,
        client_repo: IClientRepository,
        host_repo: IHostRepository,
        database_repo: IDatabaseRepository,
        policy_repo: IBackupPolicyRepository,
    ):
        self._clients = client_repo
        self._hosts = host_repo
        self._databases = database_repo
        self._policies = policy_repo

    def execute(self) -> DashboardStats:
        return DashboardStats(
            clients_count=self._clients.count(),
            hosts_count=self._hosts.count(),
            databases_count=self._databases.count(),
            policies_count=self._policies.count(),
            active_policies_count=self._policies.count_active(),
        )


class GetScheduleReportUseCase:
    """Returns schedule entries for the report view, filtered by date range."""

    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedules = schedule_repo

    def execute(
        self,
        from_date: Optional[datetime.date] = None,
        to_date: Optional[datetime.date] = None,
        days: int = 2,
    ) -> List[ScheduleEntry]:
        today = datetime.date.today()
        from_date = from_date or today
        to_date = to_date or (today + datetime.timedelta(days=days - 1))
        return self._schedules.get_upcoming(from_date=from_date, to_date=to_date)


class GenerateScheduleUseCase:
    """
    Generates schedule forecasts for all active backup policies.
    Replaces the raw cron expansion logic in schedule_generator.py with a
    Clean Architecture compatible interactor.
    """

    def __init__(
        self,
        policy_repo: IBackupPolicyRepository,
        schedule_repo: IScheduleRepository,
    ):
        self._policies = policy_repo
        self._schedules = schedule_repo

    def execute(self, reference_date: Optional[datetime.date] = None, *, clear: bool = True) -> int:
        """
        Generates schedules for a single reference_date.
        By default clears ALL existing schedules first (safe for single-day calls).
        Pass `clear=False` when calling inside a date-range loop to avoid
        wiping entries already created for previous days.
        Returns the number of schedule entries created.
        """
        reference_date = reference_date or datetime.date.today()
        if clear:
            self._schedules.clear_all()

        active_policies = self._policies.get_active()
        entries: List[ScheduleEntry] = []

        for policy in active_policies:
            expanded = self._expand_cron(policy, reference_date)
            entries.extend(expanded)

        self._schedules.bulk_create(entries)
        return len(entries)

    def execute_range(
        self,
        from_date: datetime.date,
        to_date: datetime.date,
    ) -> int:
        """
        Clears schedules once, then generates for every date in [from_date, to_date].
        Returns total number of entries created.
        """
        self._schedules.clear_all()
        total = 0
        current = from_date
        while current <= to_date:
            total += self.execute(current, clear=False)
            current += datetime.timedelta(days=1)
        return total

    # ------------------------------------------------------------------
    # Cron expansion helpers (pure logic — no DB dependency)
    # ------------------------------------------------------------------

    @staticmethod
    def _expand_field(field: str, min_val: int, max_val: int) -> set:
        result: set = set()
        if field == "*":
            return set(range(min_val, max_val + 1))
        for part in field.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                result.update(range(start, end + 1))
            else:
                try:
                    result.add(int(part))
                except ValueError:
                    pass
        return result

    def _expand_cron(self, policy, reference_date: datetime.date) -> List[ScheduleEntry]:
        minutes = self._expand_field(policy.minute, 0, 59)
        hours = self._expand_field(policy.hour, 0, 23)
        days = self._expand_field(policy.day, 1, 31)
        months = self._expand_field(policy.month, 1, 12)
        weekdays = self._expand_field(policy.day_week, 0, 6)

        entries = []
        for month in months:
            for day in days:
                try:
                    candidate = datetime.date(reference_date.year, month, day)
                except ValueError:
                    continue
                if candidate < reference_date:
                    continue
                if policy.day_week != "*" and candidate.weekday() not in weekdays:
                    continue
                for hour in hours:
                    for minute in minutes:
                        schedule_dt = datetime.datetime(
                            candidate.year, candidate.month, candidate.day, hour, minute
                        )
                        entries.append(
                            ScheduleEntry(
                                id_schedule=0,  # will be assigned by DB on insert
                                policy_id=policy.id_policy,
                                schedule_start=schedule_dt,
                                policy_name=policy.policy_name,
                                backup_type=policy.backup_type.value
                                if hasattr(policy.backup_type, "value")
                                else policy.backup_type,
                            )
                        )
        return entries


class AuditBackupUseCase:
    """
    Evaluates the health of backup jobs from the Oracle RMAN Catalog.
    Returns BackupJobResult entities with computed severity.
    """

    def __init__(self, rman_repo: IOracleRmanRepository):
        self._rman = rman_repo

    def execute(
        self,
        db_name: Optional[str] = None,
        from_date: Optional[datetime.datetime] = None,
        to_date: Optional[datetime.datetime] = None,
    ) -> List[BackupJobResult]:
        jobs = self._rman.get_backup_jobs(
            db_name=db_name, from_date=from_date, to_date=to_date
        )
        # Business rule: any job with no end_time and started > 4h ago is WARNING
        threshold = datetime.datetime.now() - datetime.timedelta(hours=4)
        for job in jobs:
            if job.status == BackupStatusValue.RUNNING and job.start_time and job.start_time < threshold:
                job.status = BackupStatusValue.WARNING
        return jobs


# ---------------------------------------------------------------------------
# Client CRUD Use Cases
# ---------------------------------------------------------------------------

class CreateClientUseCase:
    """Creates a new Client and returns the resulting entity."""

    def __init__(self, client_repo: IClientRepository):
        self._clients = client_repo

    def execute(self, name: str, description: Optional[str], created_by_id: int) -> ClientEntity:
        return self._clients.create(name=name, description=description, created_by_id=created_by_id)


class UpdateClientUseCase:
    """Updates an existing Client and returns the updated entity."""

    def __init__(self, client_repo: IClientRepository):
        self._clients = client_repo

    def execute(self, client_id: int, name: str, description: Optional[str], updated_by_id: int) -> ClientEntity:
        return self._clients.update(
            client_id=client_id, name=name, description=description, updated_by_id=updated_by_id
        )


class DeleteClientUseCase:
    """Removes a Client by id."""

    def __init__(self, client_repo: IClientRepository):
        self._clients = client_repo

    def execute(self, client_id: int) -> None:
        self._clients.delete(client_id)


# ---------------------------------------------------------------------------
# Host CRUD Use Cases
# ---------------------------------------------------------------------------

class CreateHostUseCase:
    def __init__(self, host_repo: IHostRepository):
        self._hosts = host_repo

    def execute(self, hostname: str, description: str, ip: str, client_id: int, created_by_id: int) -> HostEntity:
        return self._hosts.create(
            hostname=hostname, description=description, ip=ip,
            client_id=client_id, created_by_id=created_by_id,
        )


class UpdateHostUseCase:
    def __init__(self, host_repo: IHostRepository):
        self._hosts = host_repo

    def execute(self, host_id: int, hostname: str, description: str, ip: str, client_id: int, updated_by_id: int) -> HostEntity:
        return self._hosts.update(
            host_id=host_id, hostname=hostname, description=description,
            ip=ip, client_id=client_id, updated_by_id=updated_by_id,
        )


class DeleteHostUseCase:
    def __init__(self, host_repo: IHostRepository):
        self._hosts = host_repo

    def execute(self, host_id: int) -> None:
        self._hosts.delete(host_id)


# ---------------------------------------------------------------------------
# Database CRUD Use Cases
# ---------------------------------------------------------------------------

class CreateDatabaseUseCase:
    def __init__(self, database_repo: IDatabaseRepository):
        self._databases = database_repo

    def execute(self, db_name: str, description: str, client_id: int, host_id: int, dbid: int, created_by_id: int) -> DatabaseEntity:
        return self._databases.create(
            db_name=db_name, description=description, client_id=client_id,
            host_id=host_id, dbid=dbid, created_by_id=created_by_id,
        )


class UpdateDatabaseUseCase:
    def __init__(self, database_repo: IDatabaseRepository):
        self._databases = database_repo

    def execute(self, database_id: int, db_name: str, description: str, client_id: int, host_id: int, dbid: int, updated_by_id: int) -> DatabaseEntity:
        return self._databases.update(
            database_id=database_id, db_name=db_name, description=description,
            client_id=client_id, host_id=host_id, dbid=dbid, updated_by_id=updated_by_id,
        )


class DeleteDatabaseUseCase:
    def __init__(self, database_repo: IDatabaseRepository):
        self._databases = database_repo

    def execute(self, database_id: int) -> None:
        self._databases.delete(database_id)


# ---------------------------------------------------------------------------
# BackupPolicy CRUD Use Cases
# ---------------------------------------------------------------------------

class CreateBackupPolicyUseCase:
    def __init__(self, policy_repo: IBackupPolicyRepository):
        self._policies = policy_repo

    def execute(
        self,
        policy_name: str,
        client_id: int,
        database_id: int,
        host_id: int,
        backup_type: str,
        destination: str,
        minute: str,
        hour: str,
        day: str,
        month: str,
        day_week: str,
        duration: int,
        size_backup: str,
        status: str,
        description: Optional[str],
        created_by_id: int,
    ) -> BackupPolicyEntity:
        return self._policies.create(
            policy_name=policy_name, client_id=client_id, database_id=database_id,
            host_id=host_id, backup_type=backup_type, destination=destination,
            minute=minute, hour=hour, day=day, month=month, day_week=day_week,
            duration=duration, size_backup=size_backup, status=status,
            description=description, created_by_id=created_by_id,
        )


class UpdateBackupPolicyUseCase:
    def __init__(self, policy_repo: IBackupPolicyRepository):
        self._policies = policy_repo

    def execute(
        self,
        policy_id: int,
        policy_name: str,
        client_id: int,
        database_id: int,
        host_id: int,
        backup_type: str,
        destination: str,
        minute: str,
        hour: str,
        day: str,
        month: str,
        day_week: str,
        duration: int,
        size_backup: str,
        status: str,
        description: Optional[str],
        updated_by_id: int,
    ) -> BackupPolicyEntity:
        return self._policies.update(
            policy_id=policy_id, policy_name=policy_name, client_id=client_id,
            database_id=database_id, host_id=host_id, backup_type=backup_type,
            destination=destination, minute=minute, hour=hour, day=day, month=month,
            day_week=day_week, duration=duration, size_backup=size_backup, status=status,
            description=description, updated_by_id=updated_by_id,
        )


class DeleteBackupPolicyUseCase:
    def __init__(self, policy_repo: IBackupPolicyRepository):
        self._policies = policy_repo

    def execute(self, policy_id: int) -> None:
        self._policies.delete(policy_id)


# ---------------------------------------------------------------------------
# Oracle RMAN Catalog — Log Detail Use Case
# ---------------------------------------------------------------------------

class GetBackupDetailUseCase:
    """Fetch execution detail and RMAN output log for one backup session.

    Single Responsibility: retrieve the two Oracle catalog datasets needed
    by the ``report_read_log_detail`` view without leaking gateway details.
    """

    def __init__(self, rman_repo: IOracleRmanRepository):
        self._rman = rman_repo

    def execute(
        self,
        db_key: int,
        session_key: int,
    ) -> dict:
        """Return a dict with keys ``exec_detail`` and ``report_log``.

        Both keys are always present; values are ``None`` / ``[]`` when the
        Oracle catalog is unavailable — the view must handle the empty state
        gracefully.
        """
        exec_detail: Optional[BackupJobResult] = self._rman.get_backup_job_detail(
            db_key=db_key, session_key=session_key
        )
        report_log: List[BackupLogEntry] = self._rman.get_backup_log(
            db_key=db_key, session_key=session_key
        )
        return {
            "exec_detail": exec_detail,
            "report_log": report_log,
            "oracle_available": exec_detail is not None or len(report_log) > 0,
        }
