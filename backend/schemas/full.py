"""
Questo modulo contiene i modelli per ottenere i dati completi su un'entità.
"""
import typing as t
from uuid import UUID

from backend.schemas import read, base

__all__ = (
    "UserFull",
    "LobbyFull"
)


class UserFull(read.UserRead):
    owner_of: t.List[read.LobbyRead]
    participations: t.List["ParticipationFull"]


class ParticipationFull(base.RESTORMModel):
    id: UUID
    lobby: read.LobbyRead
    user: read.UserRead


class LobbyFull(read.LobbyRead):
    owner: read.UserRead
    participants: t.List["ParticipationFull"]
