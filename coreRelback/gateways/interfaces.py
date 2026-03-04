"""
Gateway Interfaces for Relback.

Abstract base classes that define the contracts (ports) for all data access.
Services depend ONLY on these interfaces, never on Django ORM or Oracle drivers directly.
This enforces the Dependency Inversion Principle.
"""
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional

from coreRelback.domain.entities import (
    BackupJobResult,
    BackupLogEntry,
    BackupPolicyEntity,
    ClientEntity,
    DatabaseEntity,
    HostEntity,
    ScheduleEntry,
    SlaBreach,
)


class IClientRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ClientEntity]:
        ...

    @abstractmethod
    def get_by_id(self, client_id: int) -> Optional[ClientEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def create(self, name: str, description: Optional[str], created_by_id: int) -> ClientEntity:
        ...

    @abstractmethod
    def update(self, client_id: int, name: str, description: Optional[str], updated_by_id: int) -> ClientEntity:
        ...

    @abstractmethod
    def delete(self, client_id: int) -> None:
        ...


class IHostRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[HostEntity]:
        ...

    @abstractmethod
    def get_by_id(self, host_id: int) -> Optional[HostEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def create(self, hostname: str, description: str, ip: str, client_id: int, created_by_id: int) -> HostEntity:
        ...

    @abstractmethod
    def update(self, host_id: int, hostname: str, description: str, ip: str, client_id: int, updated_by_id: int) -> HostEntity:
        ...

    @abstractmethod
    def delete(self, host_id: int) -> None:
        ...


class IDatabaseRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DatabaseEntity]:
        ...

    @abstractmethod
    def get_by_id(self, database_id: int) -> Optional[DatabaseEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def create(self, db_name: str, description: str, client_id: int, host_id: int, dbid: int, created_by_id: int) -> DatabaseEntity:
        ...

    @abstractmethod
    def update(self, database_id: int, db_name: str, description: str, client_id: int, host_id: int, dbid: int, updated_by_id: int) -> DatabaseEntity:
        ...

    @abstractmethod
    def delete(self, database_id: int) -> None:
        ...


class IBackupPolicyRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[BackupPolicyEntity]:
        ...

    @abstractmethod
    def get_active(self) -> List[BackupPolicyEntity]:
        ...

    @abstractmethod
    def get_by_id(self, policy_id: int) -> Optional[BackupPolicyEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def count_active(self) -> int:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def delete(self, policy_id: int) -> None:
        ...


class IScheduleRepository(ABC):
    @abstractmethod
    def get_upcoming(self, from_date: date, to_date: date) -> List[ScheduleEntry]:
        ...

    @abstractmethod
    def clear_all(self) -> None:
        ...

    @abstractmethod
    def bulk_create(self, entries: List[ScheduleEntry]) -> None:
        ...


class IOracleRmanRepository(ABC):
    """
    Read-only gateway to the Oracle RMAN Catalog.
    Implementations MUST never perform write operations against catalog tables.
    Multi-tenant (Phase 19): client_id scopes to that client's catalog when set.
    """
    @abstractmethod
    def get_backup_jobs(
        self,
        db_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        client_id: Optional[int] = None,
    ) -> List[BackupJobResult]:
        ...

    @abstractmethod
    def get_backup_job_detail(
        self,
        db_key: int,
        session_key: int,
        client_id: Optional[int] = None,
    ) -> Optional[BackupJobResult]:
        """Return a single BackupJobResult for the given db_key/session_key."""
        ...

    @abstractmethod
    def get_backup_log(
        self,
        db_key: int,
        session_key: int,
        client_id: Optional[int] = None,
    ) -> List[BackupLogEntry]:
        """Return RMAN output lines from RC_RMAN_OUTPUT for the given session."""
        ...


class INotificationGateway(ABC):
    """Port for sending SLA breach alerts (email, webhook, etc.)."""

    @abstractmethod
    def send_sla_breaches(self, breaches: List[SlaBreach]) -> None:
        """Send a notification for the given list of SLA breaches. Must not raise."""
        ...
