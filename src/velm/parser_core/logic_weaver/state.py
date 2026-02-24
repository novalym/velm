# Path: src/velm/parser_core/logic_weaver/state.py
# ------------------------------------------------
# LIF: ∞ | ROLE: KEEPER_OF_TRUTH | RANK: OMEGA_SUPREME
# AUTH: Ω_STATE_V200_MULTIVERSAL_RECURSION_FINALIS
# =========================================================================================

import json
import time
import hashlib
import uuid
from typing import Dict, Any, Set, List, Optional, Union, Generator
from pathlib import Path
from contextlib import contextmanager
from ...logger import Scribe
from ...utils import find_project_root

Logger = Scribe("GnosticState")


class GnosticContext:
    """
    =================================================================================
    == THE GNOSTIC CONTEXT (V-Ω-TOTALITY-V200.0-MULTIVERSAL-RECURSION)             ==
    =================================================================================
    LIF: ∞ | ROLE: NEURAL_STACK_GOVERNOR | RANK: OMEGA_SUPREME

    The Sovereign Soul of the Logic Weaver. It has been ascended to manage
    recursive variable inheritance across disparate file strata.
    =================================================================================
    """

    __slots__ = ('_context', 'parent', 'id', 'name', 'depth', 'provenance', '_locks')

    def __init__(
            self,
            raw_shared_context: Dict[str, Any],
            parent: Optional['GnosticContext'] = None,
            name: str = "root",
            depth: int = 0
    ):
        """
        The Rite of Inception.
        Sutures this context into the neural lineage of the Multiverse.
        """
        # [THE CURE]: Lazarus Self-Healing for raw dicts
        self._context = raw_shared_context if raw_shared_context is not None else {}
        self.parent = parent
        self.id = str(uuid.uuid4())[:8].upper()
        self.name = name
        self.depth = depth
        self.provenance: Dict[str, str] = {}  # Maps key -> source_script_name
        self._locks: Set[str] = set()  # Keys warded against mutation

        # [ASCENSION 7]: ROOT INHERITANCE
        if 'project_root' not in self._context:
            if self.parent:
                self._context['project_root'] = self.parent.project_root
            else:
                found_root, _ = find_project_root(Path.cwd())
                self._context['project_root'] = found_root or Path.cwd()

        # Enforce Path Integrity
        if isinstance(self._context['project_root'], str):
            self._context['project_root'] = Path(self._context['project_root'])

        # [ASCENSION 3]: VIRTUAL REALITY SYNC
        if 'generated_manifest' not in self._context:
            if self.parent:
                # Share the manifest reference with the parent
                self._context['generated_manifest'] = self.parent.raw.get('generated_manifest', [])
            else:
                self._context['generated_manifest'] = []

        self.purify()

        if self.depth == 0:
            Logger.verbose(f"Multiversal Cortex Initialized. ID: {self.id}")

    # =========================================================================
    # == RITE I: VARIABLE RESOLUTION (THE DIRECT GAZE)                       ==
    # =========================================================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        [ASCENSION 2]: PROTOPLAST INHERITANCE.
        Scries the local mind, then righteously ascends to the parent if
        the truth is unmanifest in this stratum.
        """
        # 1. Local Search
        if key in self._context:
            return self._context[key]

        # 2. Recursive Ascent
        if self.parent:
            return self.parent.get(key, default)

        # 3. Final Fallback
        return default

    def set(self, key: str, value: Any, source: str = "internal", lock: bool = False):
        """
        Inscribes truth into the local stratum.
        """
        if key in self._locks:
            raise PermissionError(f"Gnostic Schism: Key '{key}' is warded against mutation.")

        self._context[key] = value
        self.provenance[key] = source
        if lock:
            self._locks.add(key)

        # Multicast shift to HUD
        self._radiate_vitals(key, value)

    def __getitem__(self, key: str) -> Any:
        """Luminous alias for get() to support dictionary-style access."""
        res = self.get(key)
        if res is None:
            raise KeyError(f"Variable '{key}' is unmanifest in the current lineage.")
        return res

    # =========================================================================
    # == RITE II: TEMPORAL MANIPULATION (MASKING)                            ==
    # =========================================================================

    @contextmanager
    def mask(self, overrides: Dict[str, Any]) -> Generator['GnosticContext', None, None]:
        """
        [ASCENSION 3]: SHADOW-LOOM MASKING.
        Temporarily overlays variables for a specific logical branch.
        """
        original_state = {}
        added_keys = set()

        for k, v in overrides.items():
            if k in self._context:
                original_state[k] = self._context[k]
            else:
                added_keys.add(k)
            self._context[k] = v

        try:
            yield self
        finally:
            # Restore the original reality
            for k, v in original_state.items():
                self._context[k] = v
            for k in added_keys:
                del self._context[k]

    def spawn_child(self, name: str) -> 'GnosticContext':
        """
        [ASCENSION 14]: BICAMERAL FISSION.
        Creates a new context stratum that inherits from this one.
        """
        if self.depth > 50:
            raise RecursionError("Ouroboros Error: Gnostic depth limit reached.")

        return GnosticContext(
            raw_shared_context={},  # Empty local mind
            parent=self,
            name=name,
            depth=self.depth + 1
        )

    # =========================================================================
    # == RITE III: ALCHEMICAL PURIFICATION                                   ==
    # =========================================================================

    def purify(self):
        """
        [ASCENSION 5 & 11]: APOPHATIC TRUTH FILTERING.
        Transmutes string truths into logical bits in-place.
        """
        for k, v in list(self._context.items()):
            if isinstance(v, str):
                lower_v = v.lower().strip()
                # Thaw Booleans
                if lower_v in ('true', 'yes', '1', 'on', 'resonant'):
                    self._context[k] = True
                elif lower_v in ('false', 'no', '0', 'off', 'fractured'):
                    self._context[k] = False
                # Thaw Numbers
                elif lower_v.isdigit():
                    self._context[k] = int(lower_v)

    def register_virtual_file(self, path: Path):
        """
        [ASCENSION 4]: GEOMETRIC PATH NORMALIZATION.
        Inscribes a path into the shared Virtual Reality manifest.
        """
        clean_path = str(path).replace('\\', '/')
        manifest: List[str] = self._context['generated_manifest']

        if clean_path not in manifest:
            manifest.append(clean_path)
            if self.depth == 0:
                Logger.verbose(f"Lattice: Inscribed virtual atom: [dim]{clean_path}[/dim]")

    # =========================================================================
    # == RITE IV: FORENSIC TOMOGRAPHY (SCRYING)                               ==
    # =========================================================================

    def scry(self, include_parents: bool = True) -> str:
        """
        [ASCENSION 15]: HOLOGRAPHIC TOMOGRAPHY.
        Exports a sanitized, JSON-safe view of the variable hierarchy.
        """
        return json.dumps(self._export_dict(include_parents), indent=2)

    def _export_dict(self, include_parents: bool = True) -> Dict[str, Any]:
        """Recursively builds the holographic data map."""

        def _sanitize(val):
            if isinstance(val, Path): return str(val)
            if isinstance(val, set): return list(val)
            return val

        # Local Stratum
        data = {k: _sanitize(v) for k, v in self._context.items()
                if not k.startswith('_')}  # Redact Shadow Variables

        if include_parents and self.parent:
            data[f"PARENT_{self.parent.name.upper()}"] = self.parent._export_dict(True)

        return data

    @property
    def fingerprint(self) -> str:
        """[ASCENSION 6]: MERKLE-STATE FINGERPRINTING."""
        canonical = json.dumps(self._export_dict(False), sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    @property
    def raw(self) -> Dict[str, Any]:
        """Returns the LIVE reference to the local Gnostic stratum."""
        return self._context

    @property
    def project_root(self) -> Path:
        """Absolute Gnostic Anchor."""
        return self._context.get('project_root', Path.cwd())

    # =========================================================================
    # == INTERNAL METABOLISM                                                 ==
    # =========================================================================

    def _radiate_vitals(self, key: str, value: Any):
        """[ASCENSION 13]: HUD Multicast."""
        # Only broadcast top-level changes to avoid Ocular noise
        if self.depth == 0 and not key.startswith('_'):
            try:
                # We access engine via a loose reference if available
                engine = self._context.get('_engine_link')
                if engine and hasattr(engine, 'akashic') and engine.akashic:
                    engine.akashic.broadcast({
                        "method": "novalym/gnosis_shift",
                        "params": {
                            "key": key,
                            "value": str(value),
                            "trace_id": self._context.get('trace_id', 'unknown')
                        }
                    })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_CONTEXT[{self.name}] id={self.id} depth={self.depth} hash={self.fingerprint[:8]}>"

