"""
=================================================================================
== THE SCHEMA OF THE CRYSTAL MIND (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)              ==
=================================================================================
@gnosis:title The Schema of the Crystal Mind
@gnosis:summary The divine, self-aware, and unbreakable schema for the Gnostic Database.
@gnosis:LIF 10,000,000,000,000

This scripture defines the SQLAlchemy ORM models. It serves as the DNA for the
SQLite database. It has been ascended to its final, eternal form, its soul now
a pantheon of Gnostic faculties that ensure performance, integrity, and sentient
self-awareness.
=================================================================================
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

try:
    from sqlalchemy import (
        Column, String, Integer, Float, ForeignKey,
        JSON, DateTime, Text, Boolean, event
    )
    from sqlalchemy.orm import declarative_base, relationship, DeclarativeBase
    from sqlalchemy.engine import Engine


    # [FACULTY 1] The Sentient Constructor
    # We forge a new Base that understands keyword arguments, annihilating the TypeError heresy.
    class Base(DeclarativeBase):
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


    SQL_AVAILABLE = True
except ImportError:
    # Gnostic Ward for environments without SQLAlchemy
    Base = object
    SQL_AVAILABLE = False


    # Dummy decorators/types for linting if sqla is missing
    def event_listens_for(*args, **kwargs):
        return lambda x: x


    event = type('event', (), {'listens_for': event_listens_for})
    Column = String = Integer = Float = ForeignKey = JSON = DateTime = Text = Boolean = lambda *a, **k: None
    relationship = lambda *a, **k: None

# [FACULTY 2] The Unbreakable Ward of Performance (WAL Mode)
# This rite is conducted only if the SQLAlchemy artisan is manifest.
if SQL_AVAILABLE:
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """
        Enables Write-Ahead Logging (WAL) for massive concurrency improvements.
        Enables Foreign Keys for referential integrity.
        """
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class MetaModel(Base):
    """
    [FACULTY 3] The Chronomancer's Seal (Schema Versioning).
    Ensures the database structure matches the Engine's expectations, enabling
    future, automated schema migrations.
    """
    __tablename__ = 'gnostic_meta'
    key = Column(String(50), primary_key=True)
    value = Column(String(255))

    def __repr__(self):
        return f"<Meta(key='{self.key}', value='{self.value}')>"


class RiteModel(Base):
    """
    [FACULTY 4] The Chronicle of an Action.
    Records every Genesis, Transmutation, or Run event, serving as the immutable
    history of the project's becoming.
    """
    __tablename__ = 'rites'

    id = Column(String(36), primary_key=True, comment="The unique, immutable soul (UUID) of this rite.")
    name = Column(String(255), nullable=False,
                  comment="The sacred, human-readable name of the rite (e.g., 'Genesis: my-app').")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                       comment="The precise moment the rite was conducted.")
    duration_ms = Column(Float, default=0.0, comment="The duration of the rite in milliseconds.")
    architect = Column(String(100), comment="The name of the Architect who conducted the rite.")
    machine_id = Column(String(100), comment="The host reality where the rite was conducted.")
    command_line = Column(Text, comment="The exact, raw plea spoken by the Architect.")
    context_snapshot = Column(JSON, comment="The Gnostic context (variables) that governed this rite.")

    # [FACULTY 5] The Law of Bidirectional Gnosis (Relationships)
    # A Rite creates or updates many Scriptures, and this bond is eternal.
    scriptures_created = relationship("ScriptureModel", back_populates="creator_rite",
                                      foreign_keys="ScriptureModel.created_by")
    scriptures_updated = relationship("ScriptureModel", back_populates="updater_rite",
                                      foreign_keys="ScriptureModel.updated_by")

    def __repr__(self) -> str:
        """[FACULTY 6] The Luminous Soul (`__repr__`)"""
        return f"<Rite(id='{self.id[:8]}', name='{self.name}')>"


class ScriptureModel(Base):
    """
    [FACULTY 7] The Dossier of a File.
    Records the Gnostic essence of a single file at a specific moment in time.
    """
    __tablename__ = 'scriptures'

    path = Column(String, primary_key=True, comment="The pure, project-relative path to the scripture.")
    content_hash = Column(String(64), comment="SHA256 fingerprint of the scripture's soul.")
    size_bytes = Column(Integer)
    last_modified = Column(Float, comment="The Unix timestamp of the last known modification.")
    permissions = Column(String(10), comment="The scripture's permissions in octal form (e.g., '755').")
    language = Column(String(50), comment="The perceived programming language of the scripture.")
    is_binary = Column(Boolean, default=False)
    blueprint_origin = Column(String(255), comment="The blueprint or archetype that birthed this scripture.")

    # The Gnostic Lineage: Who created and last transfigured this soul?
    created_by = Column(String(36), ForeignKey('rites.id'), nullable=True)
    updated_by = Column(String(36), ForeignKey('rites.id'), nullable=True)

    creator_rite = relationship("RiteModel", foreign_keys=[created_by], back_populates="scriptures_created")
    updater_rite = relationship("RiteModel", foreign_keys=[updated_by], back_populates="scriptures_updated")

    # The Gnostic Graph: The web of causality (dependencies).
    dependencies = relationship(
        "BondModel",
        foreign_keys="[BondModel.source_path]",
        back_populates="source",
        cascade="all, delete-orphan"
    )
    dependents = relationship(
        "BondModel",
        foreign_keys="[BondModel.target_path]",
        back_populates="target",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Scripture(path='{self.path}')>"


class BondModel(Base):
    """
    [FACULTY 8] The Graph of Connections.
    Represents a single, unbreakable Gnostic bond (import, reference, usage)
    between two scriptures. This is the atom of the dependency graph.
    """
    __tablename__ = 'bonds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # [FACULTY 9] The Oracle's Index for hyper-performant graph queries.
    source_path = Column(String, ForeignKey('scriptures.path', ondelete="CASCADE"), index=True)
    target_path = Column(String, ForeignKey('scriptures.path', ondelete="CASCADE"), index=True)
    bond_type = Column(String(50), default='import', comment="The nature of the bond (e.g., 'import', 'call', 'seed').")

    # [FACULTY 10] The Vessel of Infinite Gnosis (`JSON` Type) for deep metadata.
    metadata_json = Column(JSON, nullable=True, comment="Gnosis about the bond, like the specific symbol imported.")

    source = relationship("ScriptureModel", foreign_keys=[source_path], back_populates="dependencies")
    target = relationship("ScriptureModel", foreign_keys=[target_path], back_populates="dependents")

    def __repr__(self) -> str:
        return f"<Bond('{self.source_path}' -> '{self.target_path}')>"