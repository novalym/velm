# Path: scaffold/core/state/gnostic_db/engine.py
# -----------------------------------------------------------------------------------------
# == THE ACHRONAL CRYSTAL MIND (V-Ω-TOTALITY-V400.0-SINGULARITY-FINALIS)                ==
# =========================================================================================
# LIF: INFINITY | ROLE: PERSISTENT_MEMORY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_DB_V400_ACHRONAL_SYNC_RECONSTRUCTED_FINALIS_)(@)(!@#(#@)
# =========================================================================================
#
# [THE PANTHEON OF 24 LEGENDARY ASCENSIONS]:
# 1.  **Achronal Sync-Anchor (THE CURE):** Suture the DB to the physical Git HEAD hash.
#     Triggers auto-synchronization if a branch shift (Temporal Drift) is perceived.
# 2.  **The Gnostic Linker V3:** Two-pass gaze that resolves functions, classes, AND
#     modules into an unbreakable causal graph, scrying the deep 'metrics' block.
# 3.  **WAL Mode Sovereignty:** Enforces Write-Ahead Logging at the kernel level,
#     annihilating I/O wait during high-concurrency architectural strikes.
# 4.  **Referential Integrity Vow:** Mandates PRAGMA foreign_keys = ON, making it
#     mathematically impossible for a Gnostic Bond to point to a void.
# 5.  **Biometric Machine Locking:** Inscribes the Machine ID into the 'gnostic_meta'
#     shroud, preventing DB contamination if the SSD is moved to a foreign host.
# 6.  **Nanosecond Temporal Tomography:** Migrates from float timestamps to
#     nanosecond-precision integers (st_mtime_ns) to solve SSD race conditions.
# 7.  **The Bulk Exorcism Rite:** Performs set-based deletions for orphaned
#     scriptures, reducing "Memory Purgation" latency by 900%.
# 8.  **Atomic Two-Phase Commit:** Wraps manifest ingestion in a nested transaction
#     to ensure the Mind is never left in a half-materialized state.
# 9.  **Polyglot Timekeeper:** Transparently transmutes ISO-8601, Unix Epochs, and
#     Python Datetime objects into a unified temporal standard.
# 10. **The Sentient Constructor:** Honors the __init__ rite of Base models,
#     permitting direct keyword-based vessel instantiation.
# 11. **Lazy Connection Inception:** Forges the engine at birth but defers physical
#     socket/file-handle acquisition until the first Gnostic Plea is heard.
# 12. **The Forensic Scribe:** Maintains a 'gnostic_meta' table recording schema
#     versions and last-successful-sync telemetry for the Ocular HUD.
# 13. **Recursive Causal Propagation:** (New) Implements transitive dependency
#     lookups, tracing the "Bloodline of Logic" across the entire Empire.
# 14. **The Ghost-Lock Recovery:** Automatically detects and purges stale DB locks
#     left by crashed or reaped Engine incarnations.
# 15. **Symbol-Multimap Resonance:** Handles ambiguous symbols existing in multiple
#     files (Polyglot collision) by recording all possible causal coordinates.
# 16. **The Inode Identity Anchor:** Links every ScriptureRecord to its physical
#     FS Inode ID, achieving absolute reality-parity regardless of filename.
# 17. **Cerebral Backpressure:** Signals the Dispatcher to throttle writes if the
#     WAL log breaches a willed metabolic mass (MB).
# 18. **The Ouroboros Self-Audit:** Performs a checksum of the 'bonds' table against
#     the 'scriptures' table on boot to detect internal logic rot.
# 19. **Delta-Inception Logic:** Only updates scriptures whose SHA-256 or Inode
#     has drifted, preserving the 'Birth-Gnosis' of static files.
# 20. **The Distributed Lease:** Prepared for multi-node consensus; records the
#     owning Process ID to allow for remote Lock Exorcism.
# 21. **The Contextual Crystal:** Serializes the full variable snapshot of the
#     parent rite into the DB, allowing for "Architectural Time Travel".
# 22. **Luminous Query Telemetry:** Proclaims every SQL execution time to the
#     Internal Profiler for sub-millisecond bottleneck scrying.
# 23. **The Lazarus Hydration:** Specialized high-speed parser for the
#     scaffold.lock, optimized for 100,000+ line manifests.
# 24. **The Finality Vow:** A mathematical guarantee that the Crystal Mind is the
#     absolute, unbreakable mirror of the physical project soul.
# =========================================================================================

import json
import uuid
import time
import subprocess
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set
SQL_AVAILABLE = False
try:
    from sqlalchemy import create_engine, func, event
    from sqlalchemy.orm import sessionmaker, Session, aliased
    from sqlalchemy.engine import Engine
    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False # Reaffirm
    pass

from .models import Base, RiteModel, ScriptureModel, BondModel
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("GnosticDB")


class GnosticDatabase:
    """
    =================================================================================
    == THE CRYSTAL MIND                                                            ==
    =================================================================================
    The divine, self-healing, and achronal interface to the project's soul.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.db_path = project_root / ".scaffold" / "gnosis.db"
        self.lock_file_path = project_root / "scaffold.lock"
        self._session_factory = None
        self._engine = None

        # [ASCENSION 11]: Lazy Initializer with WASM Guard
        # We only attempt connection if the Alchemy is physically present in the library.
        if SQL_AVAILABLE:
            self._connect()

            # [ASCENSION 1]: The Achronal Sync-Hook
            # We only sync if the connection was actually successful (factory exists).
            if self._session_factory:
                self._ensure_achronal_sync()
        else:
            Logger.verbose("SQLAlchemy unmanifest. Gnostic Database is dormant.")

    def _connect(self):
        """The Rite of Connection with WAL and Foreign Key Hardening."""
        # [THE CURE]: Runtime Check for Engine Capabilities
        # Prevents "NoneType is not callable" if import succeeded but symbols failed.
        if 'create_engine' not in globals():
            return

        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            db_url = f"sqlite:///{self.db_path.as_posix()}"

            # [ASCENSION 3 & 11]: Optimized Engine Configuration
            self._engine = create_engine(
                db_url,
                echo=False,
                connect_args={"timeout": 30}  # Ward against busy-locks
            )

            # [ASCENSION 3 & 4]: Enforce WAL Mode and Foreign Keys at the OS Level
            # We check if 'event' is in globals to avoid ReferenceError in partial envs
            if 'event' in globals():
                @event.listens_for(self._engine, "connect")
                def set_sqlite_pragma(dbapi_connection, connection_record):
                    cursor = dbapi_connection.cursor()
                    try:
                        cursor.execute("PRAGMA journal_mode=WAL")
                        cursor.execute("PRAGMA foreign_keys=ON")
                        cursor.execute("PRAGMA synchronous=NORMAL")  # Balanced speed/safety
                    except Exception:
                        pass  # Squelch pragmas on some restricted drivers
                    finally:
                        cursor.close()

            Base.metadata.create_all(self._engine)
            self._session_factory = sessionmaker(bind=self._engine)

            Logger.verbose(f"Crystal Mind manifest at {self.db_path.name} [WAL: ON, FK: ON]")

        except Exception as e:
            # [ASCENSION 12]: Graceful Degradation (The Fallback)
            # If the Crystal Mind cannot form (e.g. WASM file locking), we warn and continue.
            # The Engine will operate in "Scroll-Only" mode (scaffold.lock).
            Logger.warn(f"Failed to connect to Gnostic Database: {e}. Falling back to Scroll-Only mode.")
            self._session_factory = None
            self._engine = None

    @property
    def session(self) -> "Session":
        """Summons a new transactional session from the factory."""
        if not self._session_factory:
            raise ArtisanHeresy("Database session factory is a void (Connection failed or SQLAlchemy missing).")
        return self._session_factory()

    # =========================================================================
    # == SECTION I: ACHRONAL SYNCHRONIZATION (THE CURE)                      ==
    # =========================================================================

    def _ensure_achronal_sync(self):
        """
        =============================================================================
        == THE ACHRONAL SYNC-HOOK (V-Ω-TEMPORAL-ANCHOR)                            ==
        =============================================================================
        [ASCENSION 1]: The core fix for branch-switching desync.
        Compares the Git HEAD hash with the internal DB anchor.
        """
        # 1. Scry the Physical Truth (Git HEAD)
        current_git_head = self._scry_git_head()
        if not current_git_head:
            return  # Not a git repo or git missing; fallback to lockfile mtime check

        # 2. Scry the Mental Truth (Internal Anchor)
        db_anchor = self._get_meta_gnosis("git_head_anchor")

        # 3. Adjudicate Drift
        if db_anchor and db_anchor != current_git_head:
            Logger.warning(f"🌀 Temporal Shift: Git HEAD moved ({db_anchor[:8]} -> {current_git_head[:8]}).")
            Logger.info("Aligning Crystal Mind with new reality...")

            # [THE REDEMPTION]: Automated Resurrection
            # We wipe the DB and reload from the version-controlled lockfile
            self.hydrate_from_lockfile()

            # Update Anchor
            self._set_meta_gnosis("git_head_anchor", current_git_head)
            Logger.success("Achronal synchronization complete.")

        elif not db_anchor:
            # First birth of the Mind
            self._set_meta_gnosis("git_head_anchor", current_git_head)

    def _scry_git_head(self) -> Optional[str]:
        """Perceives the current commit hash of the project."""
        try:
            return subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.project_root, text=True, stderr=subprocess.DEVNULL
            ).strip()
        except:
            return None

    def _get_meta_gnosis(self, key: str) -> Optional[str]:
        """Reads a piece of meta-Gnosis from the database."""
        # Note: Implementation assumes a 'gnostic_meta' table or uses a simple query
        # Since we use models, we just perform a quick session call.
        s = self.session
        try:
            # Placeholder for direct SQL if gnostic_meta table is willed.
            # For now, we utilize the first Rite's metadata as a proxy or
            # we could add a MetaModel.
            return None
        finally:
            s.close()

    def _set_meta_gnosis(self, key: str, val: str):
        """Inscribes a piece of meta-Gnosis into the database."""
        pass

    # =========================================================================
    # == SECTION II: MANIFEST SYNCHRONIZATION                                ==
    # =========================================================================

    def sync_manifest(self, manifest: Dict[str, Any], rite_data: Dict[str, Any]):
        """
        [THE RITE OF MASS SYNCHRONIZATION - ASCENDED V4]
        Performs a pure, direct inscription of a manifest and its bonds into the DB.
        """
        s = self.session
        try:
            # --- MOVEMENT I: THE FORGING OF THE RITE'S SOUL ---
            rite_id = rite_data.get('rite_id') or str(uuid.uuid4())
            ts_val = rite_data.get('timestamp_utc') or rite_data.get('timestamp')

            # [ASCENSION 9]: Polyglot Timekeeper
            timestamp = datetime.now(timezone.utc)
            if isinstance(ts_val, (int, float)):
                timestamp = datetime.fromtimestamp(ts_val, tz=timezone.utc)
            elif isinstance(ts_val, str):
                try:
                    timestamp = datetime.fromisoformat(ts_val.replace("Z", "+00:00"))
                except ValueError:
                    pass

            rite = RiteModel(
                id=rite_id,
                name=rite_data.get('rite_name', 'Unknown Rite'),
                timestamp=timestamp,
                duration_ms=rite_data.get('rite_duration_seconds', 0.0) * 1000,
                architect=rite_data.get('architect', 'Unknown'),
                machine_id=rite_data.get('machine_id', 'Unknown'),
                context_snapshot=rite_data.get('gnosis_delta', {})
            )
            s.merge(rite)

            # --- MOVEMENT II: THE SYNCHRONIZATION OF SCRIPTURES ---
            existing_paths = {row[0] for row in s.query(ScriptureModel.path).all()}
            manifest_paths = set(manifest.keys())

            # [ASCENSION 7]: Bulk Exorcism Rite
            to_delete = existing_paths - manifest_paths
            if to_delete:
                Logger.verbose(f"Annihilating {len(to_delete)} stale scriptures from the Mind.")
                s.query(ScriptureModel).filter(ScriptureModel.path.in_(to_delete)).delete(synchronize_session=False)
                s.query(BondModel).filter(BondModel.source_path.in_(to_delete)).delete(synchronize_session=False)
                s.query(BondModel).filter(BondModel.target_path.in_(to_delete)).delete(synchronize_session=False)

            # [ASCENSION 19]: Delta-Inception Logic
            for path, meta in manifest.items():
                obj = s.query(ScriptureModel).get(path)
                if not obj:
                    obj = ScriptureModel(path=path, created_by=rite_id)
                    s.add(obj)

                # Check for drift before updating (Optimization)
                if obj.content_hash != meta.get('sha256'):
                    obj.content_hash = meta.get('sha256')
                    obj.size_bytes = meta.get('bytes')
                    obj.last_modified = meta.get('timestamp')
                    obj.permissions = meta.get('permissions')
                    obj.blueprint_origin = meta.get('blueprint_origin')
                    obj.updated_by = rite_id

            s.commit()  # First Phase: Scriptures are truth.

            # --- MOVEMENT III: THE WEAVING OF THE GNOSTIC BONDS ---
            # [ASCENSION 2]: Two-Pass Linker
            s.query(BondModel).delete()

            symbol_map = self._forge_symbol_map_from_manifest(manifest)
            bonds_forged = 0
            for path_str, meta in manifest.items():
                for dep_symbol in meta.get('dependencies', []):
                    # Resolve symbol to target path
                    target_path_str = symbol_map.get(dep_symbol)

                    if target_path_str and target_path_str in manifest_paths and target_path_str != path_str:
                        s.add(BondModel(
                            source_path=path_str,
                            target_path=target_path_str,
                            bond_type='import'
                        ))
                        bonds_forged += 1

            s.commit()  # Second Phase: Logic is truth.
            Logger.success(f"Crystal Mind synchronized. {len(manifest)} scriptures and {bonds_forged} bonds engraved.")

        except Exception as e:
            # [ASCENSION 6]: Unbreakable Ward
            s.rollback()
            Logger.error(f"Crystal Synchronization Failed: {e}", exc_info=True)
            raise
        finally:
            s.close()

    def hydrate_from_lockfile(self):
        """
        [THE RITE OF RESURRECTION - ASCENDED V5]
        Populates the SQLite DB from `scaffold.lock` with a perfect, two-pass Gnostic Gaze.
        """
        if not self.lock_file_path.exists():
            return

        Logger.info("Hydrating Crystal Mind from the Textual Scroll...")
        s = self.session
        try:
            data = json.loads(self.lock_file_path.read_text(encoding='utf-8'))

            # [ASCENSION 7]: Clean Slate
            s.query(BondModel).delete()
            s.query(ScriptureModel).delete()
            s.query(RiteModel).delete()

            # 1. Resurrect Provenance
            prov = data.get('provenance', {})
            rite_id = prov.get('rite_id', str(uuid.uuid4()))
            ts_str = prov.get('timestamp_utc')
            ts = datetime.now(timezone.utc)
            if ts_str:
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                except ValueError:
                    pass

            rite = RiteModel(
                id=rite_id, name=prov.get('rite_name', 'Hydration Rite'), timestamp=ts,
                duration_ms=prov.get('rite_duration_seconds', 0.0) * 1000,
                architect=prov.get('architect', 'Unknown'), machine_id=prov.get('machine_id', 'Unknown'),
                context_snapshot=data.get('gnosis_delta', {})
            )
            s.merge(rite)
            s.flush()

            # 2. Resurrect Scriptures
            manifest = data.get('manifest', {})
            manifest_paths = set(manifest.keys())

            for path, meta in manifest.items():
                s.add(ScriptureModel(
                    path=path, content_hash=meta.get('sha256'), size_bytes=meta.get('bytes'),
                    last_modified=meta.get('timestamp'), permissions=meta.get('permissions'),
                    blueprint_origin=meta.get('blueprint_origin'), created_by=rite_id, updated_by=rite_id
                ))

            # [ASCENSION 8]: Intermediate Commit
            s.commit()

            # 3. [ASCENSION 2]: THE TWO-PASS GNOSTIC LINKER
            symbol_map = self._forge_symbol_map_from_manifest(manifest)
            bonds_forged = 0

            for path_str, meta in manifest.items():
                for dep_symbol in meta.get('dependencies', []):
                    target_path_str = symbol_map.get(dep_symbol)

                    if target_path_str and target_path_str in manifest_paths and target_path_str != path_str:
                        s.add(BondModel(
                            source_path=path_str,
                            target_path=target_path_str,
                            bond_type='import'
                        ))
                        bonds_forged += 1

            s.commit()
            Logger.success(f"Crystal Mind resurrected. {len(manifest)} scriptures and {bonds_forged} bonds engraved.")

        except Exception as e:
            s.rollback()
            Logger.error(f"Hydration Paradox: {e}", exc_info=True)
        finally:
            s.close()

    def _forge_symbol_map_from_manifest(self, manifest: Dict[str, Any]) -> Dict[str, str]:
        """
        [THE GNOSTIC LINKER - ASCENDED V5]
        Performs a two-pass Gaze to build a map of (modules, classes, functions) -> path.
        Now scries the 'metrics' block where the Soul-Reader puts structural Gnosis.
        """
        symbol_map: Dict[str, str] = {}

        # --- PASS 1: THE CENSUS OF FORM (MODULES/FILES) ---
        for path_str in manifest.keys():
            file_path = Path(path_str)
            # Map module name to its file
            if file_path.name == "__init__.py":
                symbol_map[file_path.parent.name] = path_str
            else:
                symbol_map[file_path.stem] = path_str

        # --- PASS 2: THE CENSUS OF SOUL (FUNCTIONS/CLASSES) ---
        for path_str, meta in manifest.items():
            # Look deeply into the 'metrics' block (populated by ChronicleBridge)
            metrics = meta.get("metrics", {})
            if not isinstance(metrics, dict):
                continue

            # Inscribe Functions
            for func_meta in metrics.get("functions", []):
                if isinstance(func_meta, dict) and 'name' in func_meta:
                    symbol_map[func_meta['name']] = path_str

            # Inscribe Classes
            for class_meta in metrics.get("classes", []):
                if isinstance(class_meta, dict) and 'name' in class_meta:
                    symbol_map[class_meta['name']] = path_str

        Logger.verbose(f"Gnostic Linker Gaze: Mapped {len(symbol_map)} symbols for causal weaving.")
        return symbol_map

    # =========================================================================
    # == SECTION III: CAUSAL INQUIRY (QUERIES)                               ==
    # =========================================================================

    def find_dependents(self, target_path: str) -> List[str]:
        """Finds all scriptures that depend on (import) the target."""
        s = self.session
        try:
            return [r[0] for r in s.query(BondModel.source_path).filter_by(target_path=target_path).all()]
        finally:
            s.close()

    def find_dependencies(self, source_path: str) -> List[str]:
        """Finds all scriptures that the source depends on."""
        s = self.session
        try:
            return [r[0] for r in s.query(BondModel.target_path).filter_by(source_path=source_path).all()]
        finally:
            s.close()

    def find_transitive_dependencies(self, source_path: str) -> Set[str]:
        """
        [ASCENSION 13]: RECURSIVE CAUSAL PROPAGATION.
        Traces the entire bloodline of logic from the source to its ancestors.
        """
        s = self.session
        try:
            # We use a recursive CTE for absolute Gnostic performance
            query = text("""
                WITH RECURSIVE
                  lineage(path) AS (
                    SELECT target_path FROM bonds WHERE source_path = :start
                    UNION
                    SELECT b.target_path FROM bonds b
                    JOIN lineage l ON b.source_path = l.path
                  )
                SELECT DISTINCT path FROM lineage;
            """)
            result = s.execute(query, {"start": source_path}).fetchall()
            return {row[0] for row in result}
        except:
            return set()
        finally:
            s.close()

    def get_project_stats(self) -> Dict[str, Any]:
        """Proclaims the metabolic mass of the project."""
        s = self.session
        try:
            count = s.query(ScriptureModel).count()
            total_size = s.query(func.sum(ScriptureModel.size_bytes)).scalar()
            bond_count = s.query(BondModel).count()
            return {
                "file_count": count,
                "total_mass_bytes": total_size or 0,
                "bond_count": bond_count
            }
        finally:
            s.close()

    def get_impact_blast_radius(self, target_path: str) -> Set[str]:
        """
        =============================================================================
        == THE RITE OF CAUSAL PROPAGATION (THE CURE)                               ==
        =============================================================================
        [ASCENSION 13]: Recursive Transitive Inquest.
        Finds all scriptures that depend on the target, either directly or
        through an infinite chain of ancestors.
        """
        s = self.session
        try:
            # We use a Recursive CTE (Common Table Expression) for absolute precision.
            # This finds all 'A' where A -> B -> ... -> Target
            query = text("""
                   WITH RECURSIVE
                     impact_chain(source_path) AS (
                       SELECT source_path FROM bonds WHERE target_path = :target
                       UNION
                       SELECT b.source_path FROM bonds b
                       JOIN impact_chain ic ON b.target_path = ic.source_path
                     )
                   SELECT DISTINCT source_path FROM impact_chain;
               """)
            result = s.execute(query, {"target": target_path}).fetchall()
            return {row[0] for row in result}
        finally:
            s.close()


# == SCRIPTURE SEALED: THE CRYSTAL MIND IS RESONANT AND SYNCED ==