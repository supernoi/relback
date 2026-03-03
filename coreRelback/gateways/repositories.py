"""
Django ORM Repository Implementations.

These are the concrete adapters for the interfaces defined in interfaces.py.
They translate between Django Model instances and pure domain Entities.
Views and Use Cases receive Entities, never Model instances.
"""
from datetime import date, datetime
from typing import List, Optional

from coreRelback.domain.entities import (
    BackupDestination,
    BackupJobResult,
    BackupPolicyEntity,
    BackupStatusValue,
    BackupType,
    ClientEntity,
    DatabaseEntity,
    DashboardStats,
    HostEntity,
    PolicyStatus,
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


# ---------------------------------------------------------------------------
# ORM Repositories
# ---------------------------------------------------------------------------

class DjangoClientRepository(IClientRepository):
    def get_all(self) -> List[ClientEntity]:
        from coreRelback.models import Client
        return [
            ClientEntity(id_client=c.id_client, name=c.name or "", description=c.description)
            for c in Client.objects.all()
        ]

    def count(self) -> int:
        from coreRelback.models import Client
        return Client.objects.count()


class DjangoHostRepository(IHostRepository):
    def get_all(self) -> List[HostEntity]:
        from coreRelback.models import Host
        return [
            HostEntity(
                id_host=h.id_host,
                hostname=h.hostname,
                ip=h.ip,
                description=h.description,
                client_id=h.client_id,
            )
            for h in Host.objects.select_related("client").all()
        ]

    def count(self) -> int:
        from coreRelback.models import Host
        return Host.objects.count()


class DjangoDatabaseRepository(IDatabaseRepository):
    def get_all(self) -> List[DatabaseEntity]:
        from coreRelback.models import Database
        return [
            DatabaseEntity(
                id_database=d.id_database,
                db_name=d.db_name,
                dbid=d.dbid,
                description=d.description,
                host_id=d.host_id,
                client_id=d.client_id,
                last_resync=d.last_resync,
            )
            for d in Database.objects.select_related("host", "client").all()
        ]

    def count(self) -> int:
        from coreRelback.models import Database
        return Database.objects.count()


class DjangoBackupPolicyRepository(IBackupPolicyRepository):
    def get_all(self) -> List[BackupPolicyEntity]:
        from coreRelback.models import BackupPolicy
        return [self._to_entity(p) for p in BackupPolicy.objects.select_related("database", "host", "client").all()]

    def get_active(self) -> List[BackupPolicyEntity]:
        from coreRelback.models import BackupPolicy
        return [
            self._to_entity(p)
            for p in BackupPolicy.objects.filter(status__iexact="ACTIVE").select_related("database", "host", "client")
        ]

    def count(self) -> int:
        from coreRelback.models import BackupPolicy
        return BackupPolicy.objects.count()

    def count_active(self) -> int:
        from coreRelback.models import BackupPolicy
        return BackupPolicy.objects.filter(status__iexact="ACTIVE").count()

    @staticmethod
    def _to_entity(p) -> BackupPolicyEntity:
        return BackupPolicyEntity(
            id_policy=p.id_policy,
            policy_name=p.policy_name,
            backup_type=BackupType(p.backup_type) if p.backup_type in BackupType._value2member_map_ else BackupType.DB_FULL,
            destination=BackupDestination(p.destination) if p.destination in BackupDestination._value2member_map_ else BackupDestination.DISK,
            status=PolicyStatus(p.status.upper()),
            minute=p.minute,
            hour=p.hour,
            day=p.day,
            month=p.month,
            day_week=p.day_week,
            duration=int(p.duration),
            size_backup=p.size_backup,
            database_id=p.database_id,
            host_id=p.host_id,
            client_id=p.client_id,
            description=p.description,
        )


class DjangoScheduleRepository(IScheduleRepository):
    def get_upcoming(self, from_date: date, to_date: date) -> List[ScheduleEntry]:
        from coreRelback.models import Schedule
        qs = (
            Schedule.objects
            .select_related("backup_policy", "backup_policy__database", "backup_policy__host")
            .filter(schedule_start__date__gte=from_date, schedule_start__date__lte=to_date)
            .order_by("schedule_start")
        )
        return [
            ScheduleEntry(
                id_schedule=s.id_schedule,
                policy_id=s.backup_policy_id,
                schedule_start=s.schedule_start,
                policy_name=s.backup_policy.policy_name if s.backup_policy else None,
                hostname=s.backup_policy.host.hostname if s.backup_policy and s.backup_policy.host else None,
                db_name=s.backup_policy.database.db_name if s.backup_policy and s.backup_policy.database else None,
                backup_type=s.backup_policy.backup_type if s.backup_policy else None,
            )
            for s in qs
        ]

    def clear_all(self) -> None:
        from coreRelback.models import Schedule
        Schedule.objects.all().delete()

    def bulk_create(self, entries: List[ScheduleEntry]) -> None:
        from coreRelback.models import BackupPolicy, Schedule
        objs = [
            Schedule(backup_policy_id=e.policy_id, schedule_start=e.schedule_start)
            for e in entries
        ]
        Schedule.objects.bulk_create(objs, ignore_conflicts=True)


# ---------------------------------------------------------------------------
# Oracle RMAN Catalog Gateway (read-only)
# ---------------------------------------------------------------------------

class OracleRmanRepository(IOracleRmanRepository):
    """
    Concrete read-only gateway for Oracle RMAN Catalog queries.
    This class isolates all python-oracledb / cx_Oracle interactions.
    Replace the stub body with real connections when Oracle Catalog is available.
    """

    def get_backup_jobs(
        self,
        db_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> List[BackupJobResult]:
        # TODO: Replace with real Oracle connection using python-oracledb.
        # Example:
        #   import oracledb
        #   conn = oracledb.connect(user=..., password=..., dsn=...)
        #   cursor = conn.cursor()
        #   cursor.execute(RMAN_QUERY, params)
        #   rows = cursor.fetchall()
        #   return [self._row_to_entity(r) for r in rows]
        return []

    @staticmethod
    def _row_to_entity(row: tuple) -> BackupJobResult:
        return BackupJobResult(
            db_name=row[0],
            dbid=row[1],
            start_time=row[2],
            end_time=row[3],
            status=BackupStatusValue(row[4]) if row[4] in BackupStatusValue._value2member_map_ else BackupStatusValue.UNKNOWN,
            backup_type=row[5],
            output_bytes_display=row[6],
            time_taken_display=row[7],
            output_device_type=row[8],
            session_key=row[9],
            input_type=row[10],
        )
