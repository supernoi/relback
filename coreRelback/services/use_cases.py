from coreRelback.domain.entities import BackupStatus

class AuditBackupUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, db_id: int) -> BackupStatus:
        """
        Executes backup audit logic independent of Django requests.
        """
        data = self.repository.get_last_backup(db_id)
        
        # Pure business logic detached from Django models
        is_completed = data.get("status") == 'COMPLETED'
        
        return BackupStatus(
            db_name=data.get("name", "Unknown"),
            is_ok=is_completed,
            last_run=data.get("last_run"),
            status_message="OK" if is_completed else "Backup incomplete or missing"
        )
