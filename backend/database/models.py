"""
Questo modulo contiene le definizioni, sottoforma di classi, delle tabelle presenti nel database.
"""
import datetime

from sqlalchemy import Integer, String, LargeBinary, Column, Boolean, ForeignKey, Float, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from backend.database.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ext_id = Column(Integer, nullable=False, unique=True)
    username = Column(String, unique=True, nullable=False)
    owner_of = relationship("Lobby", back_populates="owner")
    participates = relationship("Participation", back_populates="user")


class Participation(Base):
    __tablename__ = "participation"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lobby_id = Column(UUID(as_uuid=True), ForeignKey("lobby.id"))
    lobby = relationship("Lobby", back_populates="participants")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="participates")


class Lobby(Base):
    __tablename__ = "lobby"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    is_hotjoinable = Column(Boolean, nullable=False)
    is_open = Column(Boolean, nullable=False)
    is_running = Column(Boolean, nullable=False)
    password = Column(String, nullable=False)
    frontend_uri = Column(String, nullable=False)
    gamestate = Column(JSON)

    owner = relationship("User", back_populates="owner_of")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    participants = relationship("Participation", back_populates="lobby")