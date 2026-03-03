from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class BackupStatus:
    db_name: str
    is_ok: bool
    last_run: datetime
    status_message: Optional[str] = None
