"""
Questo modulo contiene i modelli per ottenere i dati parziali su un'entità.
"""
from datetime import datetime
from uuid import UUID

from backend.schemas import edit, base

__all__ = (
    "UserRead"
    "LobbyRead"
)


class UserRead(base.RESTORMModel):
    id: UUID
    ext_id: int
    username: str


class LobbyRead(base.RESTORMModel):
    id: UUID
    name: str
    is_hotjoinable: bool
    is_open: bool
    is_running: bool
    frontend_uri: str
    owner_id: UUID