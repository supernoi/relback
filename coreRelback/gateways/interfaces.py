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
    ClientEntity,
    HostEntity,
    DatabaseEntity,
    BackupPolicyEntity,
    ScheduleEntry,
    BackupJobResult,
    DashboardStats,
)


class IClientRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ClientEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...


class IHostRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[HostEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...


class IDatabaseRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DatabaseEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...


class IBackupPolicyRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[BackupPolicyEntity]:
        ...

    @abstractmethod
    def get_active(self) -> List[BackupPolicyEntity]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def count_active(self) -> int:
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
    """
    @abstractmethod
    def get_backup_jobs(
        self,
        db_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> List[BackupJobResult]:
        ...
