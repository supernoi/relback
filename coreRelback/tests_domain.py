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
    GenerateScheduleUseCase,
    GetDashboardStatsUseCase,
    GetScheduleReportUseCase,
)


# ---------------------------------------------------------------------------
# In-memory stub repositories (no DB required)
# ---------------------------------------------------------------------------

class StubClientRepo(IClientRepository):
    def get_all(self) -> List[ClientEntity]:
        return [ClientEntity(id_client=1, name="Acme")]

    def count(self) -> int:
        return 1


class StubHostRepo(IHostRepository):
    def get_all(self) -> List[HostEntity]:
        return [HostEntity(id_host=1, hostname="srv01", ip="10.0.0.1")]

    def count(self) -> int:
        return 1


class StubDatabaseRepo(IDatabaseRepository):
    def get_all(self) -> List[DatabaseEntity]:
        return [DatabaseEntity(id_database=1, db_name="ORCL", dbid=12345)]

    def count(self) -> int:
        return 1


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
        self._policies = policies or [_make_policy()]

    def get_all(self) -> List[BackupPolicyEntity]:
        return self._policies

    def get_active(self) -> List[BackupPolicyEntity]:
        return [p for p in self._policies if p.status == PolicyStatus.ACTIVE]

    def count(self) -> int:
        return len(self._policies)

    def count_active(self) -> int:
        return sum(1 for p in self._policies if p.status == PolicyStatus.ACTIVE)


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
        cases = {
            BackupStatusValue.COMPLETED: "success",
            BackupStatusValue.RUNNING: "info",
            BackupStatusValue.WARNING: "warning",
            BackupStatusValue.FAILED: "danger",
            BackupStatusValue.UNKNOWN: "danger",
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
        use_case = GetDashboardStatsUseCase(
            client_repo=StubClientRepo(),
            host_repo=StubHostRepo(),
            database_repo=StubDatabaseRepo(),
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
