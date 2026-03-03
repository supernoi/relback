"""
Domain-layer unit tests for Relback.

These tests run WITHOUT any database or Oracle connection.
They test entities, use cases, and the cron expansion logic in isolation
using stub / in-memory repositories.
"""
import datetime
from typing import List, Optional
from unittest import TestCase

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
from coreRelback.services.use_cases import (
    AuditBackupUseCase,
    CreateClientUseCase,
    CreateDatabaseUseCase,
    CreateHostUseCase,
    DeleteClientUseCase,
    DeleteHostUseCase,
    GenerateScheduleUseCase,
    GetDashboardStatsUseCase,
    GetScheduleReportUseCase,
    UpdateClientUseCase,
    UpdateDatabaseUseCase,
    UpdateHostUseCase,
)


# ---------------------------------------------------------------------------
# In-memory stub repositories (no DB required)
# ---------------------------------------------------------------------------

class StubClientRepo(IClientRepository):
    def __init__(self):
        self._store: dict = {}
        self._next_id = 1

    def get_all(self) -> List[ClientEntity]:
        return list(self._store.values())

    def get_by_id(self, client_id: int) -> Optional[ClientEntity]:
        return self._store.get(client_id)

    def count(self) -> int:
        return len(self._store)

    def create(self, name: str, description, created_by_id: int) -> ClientEntity:
        entity = ClientEntity(id_client=self._next_id,
                              name=name, description=description)
        self._store[self._next_id] = entity
        self._next_id += 1
        return entity

    def update(self, client_id: int, name: str, description, updated_by_id: int) -> ClientEntity:
        entity = ClientEntity(id_client=client_id,
                              name=name, description=description)
        self._store[client_id] = entity
        return entity

    def delete(self, client_id: int) -> None:
        self._store.pop(client_id, None)


class StubHostRepo(IHostRepository):
    def __init__(self):
        self._store: dict = {}
        self._next_id = 1

    def get_all(self) -> List[HostEntity]:
        return list(self._store.values())

    def get_by_id(self, host_id: int) -> Optional[HostEntity]:
        return self._store.get(host_id)

    def count(self) -> int:
        return len(self._store)

    def create(self, hostname: str, description: str, ip: str, client_id: int, created_by_id: int) -> HostEntity:
        entity = HostEntity(id_host=self._next_id, hostname=hostname, ip=ip,
                            description=description, client_id=client_id)
        self._store[self._next_id] = entity
        self._next_id += 1
        return entity

    def update(self, host_id: int, hostname: str, description: str, ip: str, client_id: int, updated_by_id: int) -> HostEntity:
        entity = HostEntity(id_host=host_id, hostname=hostname, ip=ip,
                            description=description, client_id=client_id)
        self._store[host_id] = entity
        return entity

    def delete(self, host_id: int) -> None:
        self._store.pop(host_id, None)


class StubDatabaseRepo(IDatabaseRepository):
    def __init__(self):
        self._store: dict = {}
        self._next_id = 1

    def get_all(self) -> List[DatabaseEntity]:
        return list(self._store.values())

    def get_by_id(self, database_id: int) -> Optional[DatabaseEntity]:
        return self._store.get(database_id)

    def count(self) -> int:
        return len(self._store)

    def create(self, db_name: str, description: str, client_id: int, host_id: int, dbid: int, created_by_id: int) -> DatabaseEntity:
        entity = DatabaseEntity(id_database=self._next_id, db_name=db_name, dbid=dbid,
                                description=description, host_id=host_id, client_id=client_id)
        self._store[self._next_id] = entity
        self._next_id += 1
        return entity

    def update(self, database_id: int, db_name: str, description: str, client_id: int, host_id: int, dbid: int, updated_by_id: int) -> DatabaseEntity:
        entity = DatabaseEntity(id_database=database_id, db_name=db_name, dbid=dbid,
                                description=description, host_id=host_id, client_id=client_id)
        self._store[database_id] = entity
        return entity

    def delete(self, database_id: int) -> None:
        self._store.pop(database_id, None)


def _make_policy(id_policy: int = 1, status: PolicyStatus = PolicyStatus.ACTIVE) -> BackupPolicyEntity:
    return BackupPolicyEntity(
        id_policy=id_policy,
        policy_name="FULL_DAILY",
        backup_type=BackupType.DB_FULL,
        destination=BackupDestination.DISK,
        status=status,
        minute="0",
        hour="2",
        day="*",
        month="*",
        day_week="*",
        duration=120,
        size_backup="10G",
    )


class StubPolicyRepo(IBackupPolicyRepository):
    def __init__(self, policies=None):
        self._policies = list(policies or [_make_policy()])
        self._next_id = 2

    def get_all(self) -> List[BackupPolicyEntity]:
        return self._policies

    def get_active(self) -> List[BackupPolicyEntity]:
        return [p for p in self._policies if p.status == PolicyStatus.ACTIVE]

    def get_by_id(self, policy_id: int) -> Optional[BackupPolicyEntity]:
        return next((p for p in self._policies if p.id_policy == policy_id), None)

    def count(self) -> int:
        return len(self._policies)

    def count_active(self) -> int:
        return sum(1 for p in self._policies if p.status == PolicyStatus.ACTIVE)

    def create(self, policy_name, client_id, database_id, host_id, backup_type,
               destination, minute, hour, day, month, day_week, duration, size_backup,
               status, description, created_by_id):
        p = _make_policy(id_policy=self._next_id)
        self._next_id += 1
        self._policies.append(p)
        return p

    def update(self, policy_id, policy_name, client_id, database_id, host_id, backup_type,
               destination, minute, hour, day, month, day_week, duration, size_backup,
               status, description, updated_by_id):
        return self.get_by_id(policy_id)

    def delete(self, policy_id: int) -> None:
        self._policies = [
            p for p in self._policies if p.id_policy != policy_id]


class StubScheduleRepo(IScheduleRepository):
    def __init__(self):
        self._entries: List[ScheduleEntry] = []
        self.cleared = False

    def get_upcoming(self, from_date, to_date) -> List[ScheduleEntry]:
        return [e for e in self._entries if from_date <= e.schedule_start.date() <= to_date]

    def clear_all(self) -> None:
        self._entries.clear()
        self.cleared = True

    def bulk_create(self, entries: List[ScheduleEntry]) -> None:
        self._entries.extend(entries)


class StubRmanRepo(IOracleRmanRepository):
    def __init__(self, jobs=None):
        self._jobs = jobs or []

    def get_backup_jobs(self, **kwargs) -> List[BackupJobResult]:
        return list(self._jobs)


# ---------------------------------------------------------------------------
# Entity Tests
# ---------------------------------------------------------------------------

class BackupJobResultEntityTest(TestCase):
    def test_is_ok_completed(self):
        job = BackupJobResult(db_name="ORCL", dbid=1,
                              status=BackupStatusValue.COMPLETED)
        self.assertTrue(job.is_ok)

    def test_is_ok_failed(self):
        job = BackupJobResult(db_name="ORCL", dbid=1,
                              status=BackupStatusValue.FAILED)
        self.assertFalse(job.is_ok)

    def test_severity_mapping(self):
        """Severity tokens must match DaisyUI semantic names (updated in Phase 2)."""
        cases = {
            BackupStatusValue.COMPLETED:   "success",
            BackupStatusValue.RUNNING:     "info",
            BackupStatusValue.WARNING:     "warning",
            BackupStatusValue.FAILED:      "error",       # was "danger" pre-Phase 2
            BackupStatusValue.INTERRUPTED: "interrupted",
            BackupStatusValue.UNKNOWN:     "neutral",     # was "danger" pre-Phase 2
        }
        for status, expected in cases.items():
            job = BackupJobResult(db_name="ORCL", dbid=1, status=status)
            self.assertEqual(job.severity, expected,
                             f"Severity mismatch for {status}")


# ---------------------------------------------------------------------------
# Use Case Tests
# ---------------------------------------------------------------------------

class GetDashboardStatsUseCaseTest(TestCase):
    def test_returns_correct_counts(self):
        client_repo = StubClientRepo()
        client_repo.create(name="Acme", description=None, created_by_id=1)
        host_repo = StubHostRepo()
        host_repo.create(hostname="srv01", description="",
                         ip="10.0.0.1", client_id=1, created_by_id=1)
        db_repo = StubDatabaseRepo()
        db_repo.create(db_name="ORCL", description="", client_id=1,
                       host_id=1, dbid=12345, created_by_id=1)
        use_case = GetDashboardStatsUseCase(
            client_repo=client_repo,
            host_repo=host_repo,
            database_repo=db_repo,
            policy_repo=StubPolicyRepo(),
        )
        stats = use_case.execute()
        self.assertIsInstance(stats, DashboardStats)
        self.assertEqual(stats.clients_count, 1)
        self.assertEqual(stats.hosts_count, 1)
        self.assertEqual(stats.databases_count, 1)
        self.assertEqual(stats.policies_count, 1)
        self.assertEqual(stats.active_policies_count, 1)


class GenerateScheduleUseCaseTest(TestCase):
    def test_generates_entries_for_active_policies(self):
        policy_repo = StubPolicyRepo()
        schedule_repo = StubScheduleRepo()
        use_case = GenerateScheduleUseCase(
            policy_repo=policy_repo, schedule_repo=schedule_repo)

        count = use_case.execute(reference_date=datetime.date(2026, 3, 3))

        self.assertTrue(schedule_repo.cleared,
                        "Should have cleared schedules before regenerating")
        self.assertGreater(
            count, 0, "Should have created at least one schedule entry")
        self.assertEqual(len(schedule_repo._entries), count)

    def test_inactive_policies_are_skipped(self):
        policy_repo = StubPolicyRepo(
            policies=[_make_policy(status=PolicyStatus.INACTIVE)])
        schedule_repo = StubScheduleRepo()
        use_case = GenerateScheduleUseCase(
            policy_repo=policy_repo, schedule_repo=schedule_repo)

        count = use_case.execute(reference_date=datetime.date(2026, 3, 3))
        self.assertEqual(
            count, 0, "Inactive policies should not generate schedules")

    def test_execute_range_clears_once_and_accumulates(self):
        """execute_range must call clear_all exactly once regardless of range size."""
        class CountingScheduleRepo(StubScheduleRepo):
            def __init__(self):
                super().__init__()
                self.clear_count = 0

            def clear_all(self):
                super().clear_all()
                self.clear_count += 1

        # Specific policy: only matches 2026-03-03 (day=3, month=3)
        policy = BackupPolicyEntity(
            id_policy=3, policy_name="RANGE_TEST",
            backup_type=BackupType.DB_FULL,
            destination=BackupDestination.DISK,
            status=PolicyStatus.ACTIVE,
            minute="0", hour="2", day="3", month="3", day_week="*",
            duration=10, size_backup="1G",
        )
        policy_repo = StubPolicyRepo(policies=[policy])
        schedule_repo = CountingScheduleRepo()
        use_case = GenerateScheduleUseCase(
            policy_repo=policy_repo, schedule_repo=schedule_repo)

        # Range spans 3 days — clear must fire only once
        use_case.execute_range(
            from_date=datetime.date(2026, 3, 3),
            to_date=datetime.date(2026, 3, 5),
        )

        self.assertEqual(schedule_repo.clear_count, 1,
                         "execute_range must clear exactly once, not once per day")
        self.assertGreater(len(schedule_repo._entries), 0,
                           "At least one entry should be generated")

    def test_cron_wildcard_generates_all_hours(self):
        policy = BackupPolicyEntity(
            id_policy=2, policy_name="ARCH_HOURLY",
            backup_type=BackupType.ARCHIVELOG,
            destination=BackupDestination.DISK,
            status=PolicyStatus.ACTIVE,
            minute="0", hour="*", day="3", month="3", day_week="*",
            duration=10, size_backup="1G",
        )
        policy_repo = StubPolicyRepo(policies=[policy])
        schedule_repo = StubScheduleRepo()
        use_case = GenerateScheduleUseCase(
            policy_repo=policy_repo, schedule_repo=schedule_repo)

        count = use_case.execute(reference_date=datetime.date(2026, 3, 3))
        self.assertEqual(count, 24, "Wildcard hour should produce 24 entries")


class GetScheduleReportUseCaseTest(TestCase):
    def _build_repo_with_entry(self) -> StubScheduleRepo:
        repo = StubScheduleRepo()
        repo._entries.append(
            ScheduleEntry(
                id_schedule=1,
                policy_id=1,
                schedule_start=datetime.datetime(2026, 3, 3, 2, 0),
                policy_name="FULL_DAILY",
            )
        )
        return repo

    def test_returns_entries_within_range(self):
        repo = self._build_repo_with_entry()
        use_case = GetScheduleReportUseCase(schedule_repo=repo)
        entries = use_case.execute(
            from_date=datetime.date(2026, 3, 3),
            to_date=datetime.date(2026, 3, 3),
        )
        self.assertEqual(len(entries), 1)

    def test_returns_empty_outside_range(self):
        repo = self._build_repo_with_entry()
        use_case = GetScheduleReportUseCase(schedule_repo=repo)
        entries = use_case.execute(
            from_date=datetime.date(2026, 3, 4),
            to_date=datetime.date(2026, 3, 5),
        )
        self.assertEqual(len(entries), 0)


class AuditBackupUseCaseTest(TestCase):
    def test_running_job_older_than_4h_becomes_warning(self):
        old_start = datetime.datetime.now() - datetime.timedelta(hours=5)
        jobs = [
            BackupJobResult(
                db_name="ORCL", dbid=1,
                status=BackupStatusValue.RUNNING,
                start_time=old_start,
            )
        ]
        use_case = AuditBackupUseCase(rman_repo=StubRmanRepo(jobs=jobs))
        result = use_case.execute()
        self.assertEqual(result[0].status, BackupStatusValue.WARNING)

    def test_recent_running_job_stays_running(self):
        recent_start = datetime.datetime.now() - datetime.timedelta(hours=1)
        jobs = [
            BackupJobResult(
                db_name="ORCL", dbid=1,
                status=BackupStatusValue.RUNNING,
                start_time=recent_start,
            )
        ]
        use_case = AuditBackupUseCase(rman_repo=StubRmanRepo(jobs=jobs))
        result = use_case.execute()
        self.assertEqual(result[0].status, BackupStatusValue.RUNNING)


# ---------------------------------------------------------------------------
# CRUD Use Case Tests
# ---------------------------------------------------------------------------

class CreateClientUseCaseTest(TestCase):
    def test_create_returns_entity_with_correct_name(self):
        repo = StubClientRepo()
        entity = CreateClientUseCase(repo).execute(
            name="Globo", description="TV", created_by_id=1)
        self.assertEqual(entity.name, "Globo")
        self.assertEqual(entity.description, "TV")

    def test_create_increments_count(self):
        repo = StubClientRepo()
        CreateClientUseCase(repo).execute(
            name="X", description=None, created_by_id=1)
        CreateClientUseCase(repo).execute(
            name="Y", description=None, created_by_id=1)
        self.assertEqual(repo.count(), 2)


class UpdateClientUseCaseTest(TestCase):
    def test_update_changes_name(self):
        repo = StubClientRepo()
        created = repo.create(name="Old", description=None, created_by_id=1)
        updated = UpdateClientUseCase(repo).execute(
            client_id=created.id_client, name="New", description="desc", updated_by_id=1
        )
        self.assertEqual(updated.name, "New")
        self.assertEqual(updated.description, "desc")


class DeleteClientUseCaseTest(TestCase):
    def test_delete_removes_entity(self):
        repo = StubClientRepo()
        created = repo.create(
            name="ToRemove", description=None, created_by_id=1)
        self.assertEqual(repo.count(), 1)
        DeleteClientUseCase(repo).execute(created.id_client)
        self.assertEqual(repo.count(), 0)


class CreateHostUseCaseTest(TestCase):
    def test_create_host_stores_entity(self):
        repo = StubHostRepo()
        entity = CreateHostUseCase(repo).execute(
            hostname="db-host-01", description="Oracle host", ip="192.168.1.10",
            client_id=1, created_by_id=1,
        )
        self.assertEqual(entity.hostname, "db-host-01")
        self.assertEqual(entity.ip, "192.168.1.10")
        self.assertEqual(repo.count(), 1)


class UpdateHostUseCaseTest(TestCase):
    def test_update_host_changes_hostname(self):
        repo = StubHostRepo()
        created = repo.create("h1", "", "1.1.1.1", 1, 1)
        updated = UpdateHostUseCase(repo).execute(
            host_id=created.id_host, hostname="h1-renamed", description="",
            ip="1.1.1.2", client_id=1, updated_by_id=1,
        )
        self.assertEqual(updated.hostname, "h1-renamed")


class DeleteHostUseCaseTest(TestCase):
    def test_delete_host_removes_it(self):
        repo = StubHostRepo()
        created = repo.create("srv", "", "2.2.2.2", 1, 1)
        DeleteHostUseCase(repo).execute(created.id_host)
        self.assertIsNone(repo.get_by_id(created.id_host))


class CreateDatabaseUseCaseTest(TestCase):
    def test_create_database_stores_entity(self):
        repo = StubDatabaseRepo()
        entity = CreateDatabaseUseCase(repo).execute(
            db_name="PROD", description="Production", client_id=1, host_id=1, dbid=9999, created_by_id=1,
        )
        self.assertEqual(entity.db_name, "PROD")
        self.assertEqual(entity.dbid, 9999)
        self.assertEqual(repo.count(), 1)


class UpdateDatabaseUseCaseTest(TestCase):
    def test_update_database_changes_db_name(self):
        repo = StubDatabaseRepo()
        created = repo.create("OLD_DB", "", 1, 1, 1, 1)
        updated = UpdateDatabaseUseCase(repo).execute(
            database_id=created.id_database, db_name="NEW_DB", description="",
            client_id=1, host_id=1, dbid=2, updated_by_id=1,
        )
        self.assertEqual(updated.db_name, "NEW_DB")


# ---------------------------------------------------------------------------
# BackupStatusValue — Phase 2: INTERRUPTED enum + DaisyUI severity mapping
# ---------------------------------------------------------------------------

class BackupStatusValueEnumTest(TestCase):
    """Verify all expected RMAN status values exist in the enum."""

    def test_all_expected_values_present(self):
        expected = {"COMPLETED", "FAILED", "RUNNING", "WARNING", "INTERRUPTED", "UNKNOWN"}
        actual = {v.value for v in BackupStatusValue}
        self.assertEqual(expected, actual)

    def test_interrupted_is_string_enum(self):
        self.assertEqual(BackupStatusValue.INTERRUPTED, "INTERRUPTED")
        self.assertIsInstance(BackupStatusValue.INTERRUPTED, str)


class BackupJobResultSeverityTest(TestCase):
    """Verify BackupJobResult.severity returns correct DaisyUI token for every status."""

    def _job(self, status: BackupStatusValue) -> BackupJobResult:
        return BackupJobResult(db_name="TESTDB", dbid=1, status=status)

    def test_completed_severity(self):
        self.assertEqual(self._job(BackupStatusValue.COMPLETED).severity, "success")

    def test_running_severity(self):
        self.assertEqual(self._job(BackupStatusValue.RUNNING).severity, "info")

    def test_warning_severity(self):
        self.assertEqual(self._job(BackupStatusValue.WARNING).severity, "warning")

    def test_failed_severity_is_error_not_danger(self):
        """Regression: changed from 'danger' to DaisyUI token 'error' in Phase 2."""
        self.assertEqual(self._job(BackupStatusValue.FAILED).severity, "error")

    def test_interrupted_severity(self):
        self.assertEqual(self._job(BackupStatusValue.INTERRUPTED).severity, "interrupted")

    def test_unknown_severity_is_neutral_not_danger(self):
        """Regression: changed from 'danger' to DaisyUI token 'neutral' in Phase 2."""
        self.assertEqual(self._job(BackupStatusValue.UNKNOWN).severity, "neutral")
