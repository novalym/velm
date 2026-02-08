# Path: src/velm/core/kernel/transaction/chronicle_bridge.py
# ----------------------------------------------------------

import json
import time
import re
import os
from pathlib import Path
from typing import TYPE_CHECKING, List, Dict, Any, Set, Tuple, Optional, Final

# --- THE DIVINE SUMMONS OF PERCEPTION ---
from ....inquisitor import get_treesitter_gnosis
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....logger import Scribe

if TYPE_CHECKING:
    from ..transaction.facade import GnosticTransaction

Logger = Scribe("ChronicleBridge")


class ChronicleBridge:
    """
    =================================================================================
    == THE CHRONICLE BRIDGE (V-Ω-TOTALITY-V315-OMNISCIENT-LINKER)                  ==
    =================================================================================
    LIF: ∞ | ROLE: CAUSAL_LATTICE_ARCHITECT | RANK: OMEGA_SUPREME
    AUTH: Ω_BRIDGE_V315_BOND_WEAVER_FINALIS

    The sentient conduit between Kinetic Will and Eternal History. It ensures that
    the Gnostic Graph is never fragmented and the timeline is perfectly reproducible.
    """

    # [ASCENSION 4]: POSIX NORMALIZATION
    PATH_SEP: Final[str] = "/"

    def __init__(self, transaction: "GnosticTransaction"):
        self.tx = transaction
        self.project_root = transaction.project_root.resolve()

        # Internal caches for the Two-Pass Gaze
        self._symbol_to_path: Dict[str, str] = {}
        self._path_to_module: Dict[str, str] = {}
        self._ast_cache: Dict[str, Dict[str, Any]] = {}

    def seal_chronicle(self):
        """
        =============================================================================
        == THE RITE OF SEALING (V-Ω-TOTALITY)                                      ==
        =============================================================================
        Gathers all Gnosis from the transaction and commands the High Scribe to
        inscribe the new reality into the eternal chronicle.
        """
        if not self.tx.write_dossier and not self.tx.edicts_executed:
            Logger.verbose("Hollow rite perceived. The Chronicle remains a void.")
            return

        Logger.info(f"The Chronicle Bridge awakens. Sealing the history of '{self.tx.rite_name}'...")
        start_time = time.monotonic()

        # 1. LOAD THE ANCESTRAL SCROLL
        old_lock_data = {}
        main_lock_path = self.tx.project_root / "scaffold.lock"
        if main_lock_path.exists():
            try:
                old_lock_data = json.loads(main_lock_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                Logger.warn("Previous chronicle is profane. Forging a new timeline.")

        # 2. [THE FIX]: THE TWO-PASS GNOSTIC ENRICHMENT
        # This is where we weave the bonds that were missing.
        enriched_dossier_list = self._enrich_dossier()

        # 3. SUMMON THE FACADE
        from ..chronicle import update_chronicle

        update_chronicle(
            project_root=self.tx.project_root,
            blueprint_path=self.tx.blueprint_path,
            rite_dossier={},  # Plan info is now derived from enriched dossier
            old_lock_data=old_lock_data,
            write_dossier=enriched_dossier_list,
            final_vars=self.tx.context,
            rite_name=self.tx.rite_name,
            edicts_executed=self.tx.edicts_executed,
            heresies_perceived=self.tx.heresies_perceived
        )

        duration = (time.monotonic() - start_time) * 1000
        Logger.success(f"Chronicle sealed with perfect causal alignment in {duration:.2f}ms.")

    def _enrich_dossier(self) -> List[GnosticWriteResult]:
        """
        =============================================================================
        == THE RITE OF GNOSTIC ENRICHMENT (V-Ω-DEEP-RECURSIVE-GAZE)                ==
        =============================================================================
        [THE CURE]: Performs two sequential passes over the transfigured matter to
        guarantee that no symbol or bond remains a mystery.
        """
        # 1. IDENTIFY TARGETS
        # We only scan scriptures that have been Modified, Created, or Adopted.
        items_to_scan = [
            res for res in self.tx.write_dossier.values()
            if res.success and res.action_taken in (
                InscriptionAction.CREATED,
                InscriptionAction.TRANSFIGURED,
                InscriptionAction.SYMBIOTIC_MERGE,
                InscriptionAction.ADOPTED
            )
        ]

        if not items_to_scan:
            return list(self.tx.write_dossier.values())

        Logger.verbose(f"Linker: Performing Two-Pass Gaze upon {len(items_to_scan)} transfigured soul(s)...")

        # --- PASS 1: THE CENSUS OF SOULS (Symbol Discovery) ---
        self._conduct_symbol_census(items_to_scan)

        # --- PASS 2: THE WEAVING OF BONDS (Dependency Resolution) ---
        self._weave_causal_bonds(items_to_scan)

        return list(self.tx.write_dossier.values())

    def _conduct_symbol_census(self, items: List[GnosticWriteResult]):
        """
        Builds the global map of Symbol -> Path and Path -> Module.
        """
        for result in items:
            try:
                # [ASCENSION 7]: Prioritize Staged content for "Future Truth"
                staged_path = self.tx.get_staging_path(result.path)
                if not staged_path.is_file():
                    continue

                content = staged_path.read_bytes().decode('utf-8', errors='ignore')

                # Divination: Get AST Gnosis
                gnosis = get_treesitter_gnosis(staged_path, content)
                path_posix = result.path.as_posix()
                self._ast_cache[path_posix] = gnosis

                if not gnosis or "error" in gnosis:
                    continue

                # 1. MAP THE MODULE SOUL
                # src/velm/core.py -> velm.core
                module_path = self._divine_module_path(result.path)
                self._path_to_module[path_posix] = module_path
                self._symbol_to_path[module_path] = path_posix

                # 2. MAP THE SYMBOL SOULS (Functions & Classes)
                for func in gnosis.get("functions", []):
                    name = func.get('name')
                    if name:
                        self._symbol_to_path[name] = path_posix
                        self._symbol_to_path[f"{module_path}.{name}"] = path_posix

                for cls in gnosis.get("classes", []):
                    name = cls.get('name')
                    if name:
                        self._symbol_to_path[name] = path_posix
                        self._symbol_to_path[f"{module_path}.{name}"] = path_posix

                # [ASCENSION 1 & 9]: ENRICH METRICS
                metrics = gnosis.get("metrics", {})
                # Embed structural souls for future DB hydration
                metrics["functions"] = [{"n": f['name'], "l": f['start_point'][0] + 1} for f in
                                        gnosis.get("functions", [])]
                metrics["classes"] = [{"n": c['name'], "l": c['start_point'][0] + 1} for c in gnosis.get("classes", [])]
                result.metrics = metrics

            except Exception as e:
                Logger.debug(f"Census fracture for '{result.path}': {e}")

    def _weave_causal_bonds(self, items: List[GnosticWriteResult]):
        """
        Resolves imported symbols to their true file origins.
        """
        for result in items:
            path_posix = result.path.as_posix()
            gnosis = self._ast_cache.get(path_posix)
            if not gnosis:
                continue

            # [FACULTY 11]: The Forensic Scribe
            # Extract symbols willed for import
            imports = gnosis.get("dependencies", {}).get("imported_symbols", [])
            resolved_paths: Set[str] = set()

            for imp in imports:
                # [ASCENSION 2]: ACHRONAL RELATIVE RESOLUTION
                # We handle relative imports (., .., ...) by resolving them against the current module
                target_path = self._resolve_symbol_locus(imp, path_posix)

                if target_path:
                    # [ASCENSION 8]: GHOST SUPPRESSION
                    if target_path != path_posix:  # No self-bonds
                        resolved_paths.add(target_path)

            # Inscribe the bonds into the manifest item
            result.dependencies = sorted(list(resolved_paths))

            if result.dependencies:
                Logger.verbose(f"   -> {result.path.name}: Wove {len(result.dependencies)} causal bond(s).")

    def _divine_module_path(self, file_path: Path) -> str:
        """
        [ASCENSION 4]: Forces a file path into a Python module dotted-string.
        src/velm/core/__init__.py -> velm.core
        """
        # 1. Strip extension
        stem = file_path.with_suffix('')

        # 2. Split to parts
        parts = list(stem.parts)

        # 3. Handle Pythonic conventions
        if parts and parts[-1] == "__init__":
            parts.pop()

        # 4. Handle common root prefixes (src, lib)
        if parts and parts[0] in ('src', 'lib'):
            parts.pop(0)

        return ".".join(parts)

    def _resolve_symbol_locus(self, symbol_fqn: str, source_path_posix: str) -> Optional[str]:
        """
        [THE OMNISCIENT RESOLVER]
        Attempts to find the file providing a specific symbol.
        """
        # 1. DIRECT HIT
        if symbol_fqn in self._symbol_to_path:
            return self._symbol_to_path[symbol_fqn]

        # 2. RELATIVE RITE
        # If the symbol starts with dots, it is a relative import plea.
        if symbol_fqn.startswith('.'):
            return self._resolve_relative_plea(symbol_fqn, source_path_posix)

        # 3. FRAGMENTATION SCRYING
        # If 'velm.core.logic.execute' isn't found, try 'velm.core.logic', then 'velm.core'
        parts = symbol_fqn.split('.')
        for i in range(len(parts) - 1, 0, -1):
            parent_fqn = ".".join(parts[:i])
            if parent_fqn in self._symbol_to_path:
                return self._symbol_to_path[parent_fqn]

        return None

    def _resolve_relative_plea(self, plea: str, source_path: str) -> Optional[str]:
        """
        [ASCENSION 2]: Resolves '.' and '..' imports.
        """
        # Count leading dots
        dots_match = re.match(r'^(\.+)', plea)
        if not dots_match:
            return None

        dot_count = len(dots_match.group(1))
        remainder = plea[dot_count:]

        # Resolve path hierarchy
        source_p = Path(source_path)
        # 1 dot = current dir, 2 dots = parent, etc.
        # Path.parents[0] is parent, [1] is grandparent
        try:
            target_dir = source_p.parents[dot_count - 1]

            # If there's a remainder (e.g. from .module import symbol)
            if remainder:
                # Form a candidate module path
                # This requires knowing the project's module root.
                # For simplicity, we check if the physical file exists in the manifest.
                candidate_path = (target_dir / remainder.replace('.', '/')).as_posix()

                # Check for .py or /__init__.py
                for ext in ['.py', '/__init__.py']:
                    full_cand = candidate_path + ext
                    if full_cand in self.tx.write_dossier:
                        return full_cand
            else:
                # Just 'from .. import *'
                return target_dir.as_posix()
        except (IndexError, ValueError):
            pass

        return None

    def __repr__(self) -> str:
        return f"<Ω_CHRONICLE_BRIDGE transaction={self.tx.tx_id[:8]} status=RESONANT>"

# == SCRIPTURE SEALED: THE CAUSAL LATTICE IS OMNISCIENT ==