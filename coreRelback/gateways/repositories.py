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
            ClientEntity(id_client=c.id_client, name=c.name or "",
                         description=c.description)
            for c in Client.objects.all()
        ]

    def get_by_id(self, client_id: int) -> Optional[ClientEntity]:
        from coreRelback.models import Client
        try:
            c = Client.objects.get(pk=client_id)
            return ClientEntity(id_client=c.id_client, name=c.name or "", description=c.description)
        except Client.DoesNotExist:
            return None

    def count(self) -> int:
        from coreRelback.models import Client
        return Client.objects.count()

    def create(self, name: str, description: Optional[str], created_by_id: int) -> ClientEntity:
        from coreRelback.models import Client
        c = Client.objects.create(
            name=name, description=description, created_by_id=created_by_id)
        return ClientEntity(id_client=c.id_client, name=c.name or "", description=c.description)

    def update(self, client_id: int, name: str, description: Optional[str], updated_by_id: int) -> ClientEntity:
        from coreRelback.models import Client
        Client.objects.filter(pk=client_id).update(
            name=name, description=description, updated_by_id=updated_by_id
        )
        return self.get_by_id(client_id)

    def delete(self, client_id: int) -> None:
        from coreRelback.models import Client
        Client.objects.filter(pk=client_id).delete()


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

    def get_by_id(self, host_id: int) -> Optional[HostEntity]:
        from coreRelback.models import Host
        try:
            h = Host.objects.get(pk=host_id)
            return HostEntity(id_host=h.id_host, hostname=h.hostname, ip=h.ip,
                              description=h.description, client_id=h.client_id)
        except Host.DoesNotExist:
            return None

    def count(self) -> int:
        from coreRelback.models import Host
        return Host.objects.count()

    def create(self, hostname: str, description: str, ip: str, client_id: int, created_by_id: int) -> HostEntity:
        from coreRelback.models import Host
        h = Host.objects.create(
            hostname=hostname, description=description, ip=ip,
            client_id=client_id, created_by_id=created_by_id
        )
        return HostEntity(id_host=h.id_host, hostname=h.hostname, ip=h.ip,
                          description=h.description, client_id=h.client_id)

    def update(self, host_id: int, hostname: str, description: str, ip: str, client_id: int, updated_by_id: int) -> HostEntity:
        from coreRelback.models import Host
        Host.objects.filter(pk=host_id).update(
            hostname=hostname, description=description, ip=ip,
            client_id=client_id, updated_by_id=updated_by_id
        )
        return self.get_by_id(host_id)

    def delete(self, host_id: int) -> None:
        from coreRelback.models import Host
        Host.objects.filter(pk=host_id).delete()


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

    def get_by_id(self, database_id: int) -> Optional[DatabaseEntity]:
        from coreRelback.models import Database
        try:
            d = Database.objects.get(pk=database_id)
            return DatabaseEntity(id_database=d.id_database, db_name=d.db_name, dbid=d.dbid,
                                  description=d.description, host_id=d.host_id,
                                  client_id=d.client_id, last_resync=d.last_resync)
        except Database.DoesNotExist:
            return None

    def count(self) -> int:
        from coreRelback.models import Database
        return Database.objects.count()

    def create(self, db_name: str, description: str, client_id: int, host_id: int, dbid: int, created_by_id: int) -> DatabaseEntity:
        from coreRelback.models import Database
        d = Database.objects.create(
            db_name=db_name, description=description, client_id=client_id,
            host_id=host_id, dbid=dbid, created_by_id=created_by_id
        )
        return DatabaseEntity(id_database=d.id_database, db_name=d.db_name, dbid=d.dbid,
                              description=d.description, host_id=d.host_id, client_id=d.client_id)

    def update(self, database_id: int, db_name: str, description: str, client_id: int, host_id: int, dbid: int, updated_by_id: int) -> DatabaseEntity:
        from coreRelback.models import Database
        Database.objects.filter(pk=database_id).update(
            db_name=db_name, description=description, client_id=client_id,
            host_id=host_id, dbid=dbid, updated_by_id=updated_by_id
        )
        return self.get_by_id(database_id)

    def delete(self, database_id: int) -> None:
        from coreRelback.models import Database
        Database.objects.filter(pk=database_id).delete()


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

    def get_by_id(self, policy_id: int) -> Optional[BackupPolicyEntity]:
        from coreRelback.models import BackupPolicy
        try:
            return self._to_entity(BackupPolicy.objects.get(pk=policy_id))
        except BackupPolicy.DoesNotExist:
            return None

    def create(
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
        from coreRelback.models import BackupPolicy
        p = BackupPolicy.objects.create(
            policy_name=policy_name, client_id=client_id, database_id=database_id,
            host_id=host_id, backup_type=backup_type, destination=destination,
            minute=minute, hour=hour, day=day, month=month, day_week=day_week,
            duration=duration, size_backup=size_backup, status=status,
            description=description, created_by_id=created_by_id,
        )
        return self._to_entity(p)

    def update(
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
        from coreRelback.models import BackupPolicy
        BackupPolicy.objects.filter(pk=policy_id).update(
            policy_name=policy_name, client_id=client_id, database_id=database_id,
            host_id=host_id, backup_type=backup_type, destination=destination,
            minute=minute, hour=hour, day=day, month=month, day_week=day_week,
            duration=duration, size_backup=size_backup, status=status,
            description=description, updated_by_id=updated_by_id,
        )
        return self.get_by_id(policy_id)

    def delete(self, policy_id: int) -> None:
        from coreRelback.models import BackupPolicy
        BackupPolicy.objects.filter(pk=policy_id).delete()

    @staticmethod
    def _to_entity(p) -> BackupPolicyEntity:
        return BackupPolicyEntity(
            id_policy=p.id_policy,
            policy_name=p.policy_name,
            backup_type=BackupType(
                p.backup_type) if p.backup_type in BackupType._value2member_map_ else BackupType.DB_FULL,
            destination=BackupDestination(
                p.destination) if p.destination in BackupDestination._value2member_map_ else BackupDestination.DISK,
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
            Schedule(backup_policy_id=e.policy_id,
                     schedule_start=e.schedule_start)
            for e in entries
        ]
        Schedule.objects.bulk_create(objs, ignore_conflicts=True)


# ---------------------------------------------------------------------------
# Oracle RMAN Catalog Gateway (read-only)
# ---------------------------------------------------------------------------

class OracleRmanRepository(IOracleRmanRepository):
    """
    Concrete read-only gateway for Oracle RMAN Catalog queries.

    Queries RC_BACKUP_JOB_DETAILS (standard Recovery Catalog view, Oracle 10g+)
    using python-oracledb thin mode.  Connection config comes from
    ``settings.ORACLE_CATALOG``; returns an empty list gracefully when
    the catalog is unavailable or not configured.
    """

    # Column order must match _row_to_entity tuple unpacking below.
    _SQL = """\
SELECT
    DB_NAME,
    DBID,
    START_TIME,
    END_TIME,
    STATUS,
    INPUT_TYPE,
    OUTPUT_BYTES_DISPLAY,
    TIME_TAKEN_DISPLAY,
    OUTPUT_DEVICE_TYPE,
    SESSION_KEY,
    INPUT_TYPE
FROM RC_BACKUP_JOB_DETAILS
{where}
ORDER BY START_TIME DESC
FETCH FIRST 500 ROWS ONLY"""

    def get_backup_jobs(
        self,
        db_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> List[BackupJobResult]:
        from coreRelback.gateways.oracle_catalog import get_catalog_connection
        import logging as _log
        _logger = _log.getLogger(__name__)

        conn = get_catalog_connection()
        if conn is None:
            return []

        # Build WHERE dynamically to avoid NULL bind-variable issues in Oracle.
        conditions: list = []
        params: dict = {}
        if db_name:
            conditions.append("DB_NAME = :db_name")
            params["db_name"] = db_name
        if from_date:
            conditions.append("START_TIME >= :from_date")
            params["from_date"] = from_date
        if to_date:
            conditions.append("START_TIME < :to_date + INTERVAL '1' DAY")
            params["to_date"] = to_date

        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = self._SQL.format(where=where_clause)

        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return [self._row_to_entity(row) for row in cursor]
        except Exception as exc:
            _logger.error("RMAN catalog query failed: %s", exc)
            return []


    @staticmethod
    def _row_to_entity(row: tuple) -> BackupJobResult:
        return BackupJobResult(
            db_name=row[0],
            dbid=row[1],
            start_time=row[2],
            end_time=row[3],
            status=BackupStatusValue(
                row[4]) if row[4] in BackupStatusValue._value2member_map_ else BackupStatusValue.UNKNOWN,
            backup_type=row[5],
            output_bytes_display=row[6],
            time_taken_display=row[7],
            output_device_type=row[8],
            session_key=row[9],
            input_type=row[10],
        )
