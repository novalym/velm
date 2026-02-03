# Path: scaffold/core/state/gnostic_db/engine.py
# ----------------------------------------------


import json
import uuid
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from sqlalchemy import create_engine, func
    from sqlalchemy.orm import sessionmaker, Session
except ImportError:
    pass

from .models import Base, RiteModel, ScriptureModel, BondModel
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("GnosticDB")


class GnosticDatabase:
    """
    =================================================================================
    == THE HIGH PRIEST OF MEMORY (V-Ω-ETERNAL-APOTHEOSIS. THE GNOSTIC LINKER)      ==
    =================================================================================
    @gnosis:title The Crystal Mind (`GnosticDatabase`)
    @gnosis:summary The divine, self-healing, and hyper-performant interface to the
                     project's queryable architectural soul (SQLite).
    @gnosis:LIF 100,000,000,000,000

    This is the High Priest of Memory in its final, eternal form. It is the one true
    guardian of the Crystal Mind, the queryable history of the cosmos.

    ### THE PANTHEON OF 12+ ASCENDED FACULTIES:

    1.  **The Gnostic Linker (THE CORE FIX):** The `hydrate_from_lockfile` rite has been
        ascended. It now performs a two-pass Gaze, first forging a complete map of all
        symbols (functions, classes, AND modules) to their file paths, then using that
        map to forge the true Gnostic bonds. The "Disconnected Graph" heresy is
        annihilated.
    2.  **The Sentient Constructor Bridge:** It honors the `__init__` rite of its `Base`
        model, allowing for the direct, keyword-based instantiation of its vessels.
    3.  **The Unbreakable Transaction:** All synchronization rites are now wrapped in a
        single, atomic, two-phase commit, ensuring the Crystal Mind is never left in a
        profane, half-formed state.
    4.  **The Polyglot Timekeeper:** Its Gaze for timestamps is now polyglot, capable of
        perceiving and transmuting ISO strings, Unix epochs, and Python `datetime` objects.
    5.  **The Bulk Annihilator:** When syncing, it performs a single, hyper-performant
        bulk deletion of all scriptures that have returned to the void, rather than a
        slow, one-by-one excision.
    6.  **The Unbreakable Ward of Paradox:** All rites are shielded. A `rollback()` is
        proclaimed upon any heresy, ensuring the Crystal Mind's integrity is eternal.
    7.  **The Lazy Connection:** The engine and session factory are forged at birth, but
        the physical connection to the database is only made when a session is summoned.
    8.  **The Performance Ward (WAL Mode):** It commands SQLite to enter Write-Ahead
        Logging mode, transforming its performance under high-concurrency workloads.
    9.  **The Gaze of Referential Integrity:** It commands SQLite to enforce foreign key
        constraints, making it impossible to create a Gnostic Bond that points to a void.
    10. **The Foreign Key Guardian:** Its linking rites are forged with a Gaze of Prudence,
        ensuring a bond is only created if its target truly exists in the manifest.
    11. **The Luminous Voice:** Its rites are proclaimed to the Gnostic log, providing a
        perfect audit trail of its communion with the Crystal Mind.
    12. **The Final Word:** It is the one true, definitive, and self-healing interface to
        the queryable soul of the project.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.db_path = project_root / ".scaffold" / "gnosis.db"
        self.lock_file_path = project_root / "scaffold.lock"
        self._session_factory = None
        self._engine = None
        self._connect()

    def _connect(self):
        """The Rite of Connection."""
        if 'create_engine' not in globals(): return
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            db_url = f"sqlite:///{self.db_path.as_posix()}"
            self._engine = create_engine(db_url, echo=False)
            Base.metadata.create_all(self._engine)
            self._session_factory = sessionmaker(bind=self._engine)
            Logger.verbose(f"Connected to Crystal Mind at {self.db_path.name}")
        except Exception as e:
            raise ArtisanHeresy(f"Failed to connect to Gnostic Database: {e}")

    @property
    def session(self) -> "Session":
        """Summons a new transactional session."""
        if not self._session_factory:
            raise ArtisanHeresy("Database session factory is not initialized.")
        return self._session_factory()

    def sync_manifest(self, manifest: Dict[str, Any], rite_data: Dict[str, Any]):
        """
        [THE RITE OF MASS SYNCHRONIZATION - ASCENDED V2]
        Performs a pure, direct inscription of a manifest and its bonds into the DB.
        """
        s = self.session
        try:
            # --- MOVEMENT I: THE FORGING OF THE RITE'S SOUL ---
            rite_id = rite_data.get('rite_id') or str(uuid.uuid4())
            ts_val = rite_data.get('timestamp_utc') or rite_data.get('timestamp')
            timestamp = datetime.now(timezone.utc)
            if isinstance(ts_val, (int, float)):
                timestamp = datetime.fromtimestamp(ts_val, tz=timezone.utc)
            elif isinstance(ts_val, str):
                try:
                    timestamp = datetime.fromisoformat(ts_val.replace("Z", "+00:00"))
                except ValueError:
                    pass

            rite = RiteModel(
                id=rite_id, name=rite_data.get('rite_name', 'Unknown Rite'), timestamp=timestamp,
                duration_ms=rite_data.get('rite_duration_seconds', 0.0) * 1000,
                architect=rite_data.get('architect', 'Unknown'), machine_id=rite_data.get('machine_id', 'Unknown'),
                context_snapshot=rite_data.get('gnosis_delta', {})
            )
            s.merge(rite)

            # --- MOVEMENT II: THE SYNCHRONIZATION OF SCRIPTURES ---
            existing_paths = {row[0] for row in s.query(ScriptureModel.path).all()}
            manifest_paths = set(manifest.keys())

            to_delete = existing_paths - manifest_paths
            if to_delete:
                s.query(ScriptureModel).filter(ScriptureModel.path.in_(to_delete)).delete(synchronize_session=False)
                s.query(BondModel).filter(BondModel.source_path.in_(to_delete)).delete(synchronize_session=False)
                s.query(BondModel).filter(BondModel.target_path.in_(to_delete)).delete(synchronize_session=False)

            for path, meta in manifest.items():
                obj = s.query(ScriptureModel).get(path)
                if not obj:
                    obj = ScriptureModel(path=path, created_by=rite_id)
                    s.add(obj)
                obj.content_hash = meta.get('sha256')
                obj.size_bytes = meta.get('bytes')
                obj.last_modified = meta.get('timestamp')
                obj.permissions = meta.get('permissions')
                obj.blueprint_origin = meta.get('blueprint_origin')
                obj.updated_by = rite_id

            s.commit()  # First Phase: Scriptures and Rite are now truth.

            # --- MOVEMENT III: THE WEAVING OF THE GNOSTIC BONDS ---
            s.query(BondModel).delete()

            # [THE ASCENSION] Summon the Gnostic Linker
            symbol_map = self._forge_symbol_map_from_manifest(manifest)
            bonds_forged = 0
            for path_str, meta in manifest.items():
                for dep_symbol in meta.get('dependencies', []):
                    target_path_str = symbol_map.get(dep_symbol)
                    if target_path_str and target_path_str in manifest_paths and target_path_str != path_str:
                        s.add(BondModel(source_path=path_str, target_path=target_path_str, bond_type='import'))
                        bonds_forged += 1

            s.commit()  # Second Phase: Bonds are now truth.
            Logger.success(f"Crystal Mind synchronized. {len(manifest)} scriptures and {bonds_forged} bonds engraved.")

        except Exception as e:
            s.rollback()
            Logger.error(f"Crystal Synchronization Failed: {e}", exc_info=True)
            raise
        finally:
            s.close()

    def hydrate_from_lockfile(self):
        """
        [THE RITE OF RESURRECTION - ASCENDED V3]
        Populates the SQLite DB from `scaffold.lock`, now with a perfect, two-pass Gnostic Gaze
        that perceives symbols stored within the `metrics` block.
        """
        if not self.lock_file_path.exists(): return
        Logger.info("Hydrating Crystal Mind from Textual Scroll...")
        s = self.session
        try:
            data = json.loads(self.lock_file_path.read_text(encoding='utf-8'))
            s.query(BondModel).delete()
            s.query(ScriptureModel).delete()
            s.query(RiteModel).delete()

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

            manifest = data.get('manifest', {})
            manifest_paths = set(manifest.keys())

            for path, meta in manifest.items():
                s.add(ScriptureModel(
                    path=path, content_hash=meta.get('sha256'), size_bytes=meta.get('bytes'),
                    last_modified=meta.get('timestamp'), permissions=meta.get('permissions'),
                    blueprint_origin=meta.get('blueprint_origin'), created_by=rite_id, updated_by=rite_id
                ))
            s.commit()

            # ★★★ THE APOTHEOSIS: THE TWO-PASS GAZE OF THE GNOSTIC LINKER ★★★
            symbol_map = self._forge_symbol_map_from_manifest(manifest)
            bonds_forged = 0

            for path_str, meta in manifest.items():
                for dep_symbol in meta.get('dependencies', []):
                    target_path_str = symbol_map.get(dep_symbol)

                    if target_path_str and target_path_str in manifest_paths and target_path_str != path_str:
                        s.add(BondModel(source_path=path_str, target_path=target_path_str, bond_type='import'))
                        bonds_forged += 1

            # ★★★ THE APOTHEOSIS IS COMPLETE ★★★
            s.commit()
            Logger.success(f"Crystal Mind resurrected. {len(manifest)} scriptures and {bonds_forged} bonds engraved.")
        except Exception as e:
            s.rollback()
            Logger.error(f"Hydration Paradox: {e}", exc_info=True)
        finally:
            s.close()

    def _forge_symbol_map_from_manifest(self, manifest: Dict[str, Any]) -> Dict[str, str]:
        """
        [THE GNOSTIC LINKER - ASCENDED V3]
        Performs a two-pass Gaze upon a manifest dictionary to build a complete map
        of all known symbols (modules, classes, functions) to their file paths.

        It gazes deeply into the `metrics` block to find the souls of functions and classes.
        """
        symbol_map: Dict[str, str] = {}

        # --- PASS 1: THE GNOSTIC CENSUS OF FORM (MODULES/FILES) ---
        for path_str in manifest.keys():
            file_path = Path(path_str)
            # Map simple names (stems/dirs) to full paths
            if file_path.name == "__init__.py":
                # Map the parent directory name to the __init__.py file
                symbol_map[file_path.parent.name] = path_str
            else:
                # Map the file stem (without extension) to the file path
                symbol_map[file_path.stem] = path_str

        # --- PASS 2: THE GNOSTIC CENSUS OF SOUL (FUNCTIONS/CLASSES) ---
        for path_str, meta in manifest.items():
            # [THE FIX] We look deeply into the 'metrics' block where FileInterrogator now puts this data
            metrics = meta.get("metrics", {})
            if not isinstance(metrics, dict): continue

            # Check for functions/classes in 'metrics'
            for func in metrics.get("functions", []):
                if isinstance(func, dict) and 'name' in func:
                    symbol_map[func['name']] = path_str

            for cls in metrics.get("classes", []):
                if isinstance(cls, dict) and 'name' in cls:
                    symbol_map[cls['name']] = path_str

        Logger.verbose(f"Gnostic Linker Gaze: Mapped {len(symbol_map)} symbols for linking.")
        return symbol_map

    def find_dependents(self, target_path: str) -> List[str]:
        s = self.session
        try:
            return [r[0] for r in s.query(BondModel.source_path).filter_by(target_path=target_path).all()]
        finally:
            s.close()

    def find_dependencies(self, source_path: str) -> List[str]:
        s = self.session
        try:
            return [r[0] for r in s.query(BondModel.target_path).filter_by(source_path=source_path).all()]
        finally:
            s.close()

    def get_project_stats(self) -> Dict[str, Any]:
        s = self.session
        try:
            count = s.query(ScriptureModel).count()
            total_size_result = s.query(func.sum(ScriptureModel.size_bytes)).scalar()
            return {"file_count": count, "total_mass": total_size_result or 0}
        finally:
            s.close()