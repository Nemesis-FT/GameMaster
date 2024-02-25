"""
Questo modulo contiene gli schemi JSON per la creazione e modifica di oggetti nel database.
"""
import typing as t
from uuid import UUID
from datetime import datetime

from backend.database import models
from backend.schemas import base

__all__ = (
    "LobbyEdit"
)


class LobbyEdit(base.RESTORMModel):
    name: str
    is_hotjoinable: bool
    is_open: bool
    is_running: bool
    password: str
    frontend_uri: str
