class OracleRmanRepository:
    """
    Interface Gateway to separate Django or Oracle logic from pure business layers.
    """
    def get_last_backup(self, db_id: int) -> dict:
        """
        Retrieves the last backup info for a given database.
        Implement actual DB calls like cx_Oracle/python-oracledb or Django ORM here.
        """
        # Mock logic to show decoupling layer
        return {
            "name": f"DB_{db_id}",
            "status": "COMPLETED",
            "last_run": "2026-03-03T12:00:00"
        }
