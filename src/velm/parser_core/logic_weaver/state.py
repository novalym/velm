# Path: src/velm/parser_core/logic_weaver/state.py
# ------------------------------------------------
# LIF: ∞ | ROLE: KEEPER_OF_TRUTH | RANK: OMEGA_SUPREME
# AUTH: Ω_STATE_V100_LIVE_REFERENCE_TOTALITY
# =========================================================================================

from typing import Dict, Any, Set, List, Optional, Union
from pathlib import Path
from contextlib import contextmanager
from ...logger import Scribe
from ...utils import find_project_root

Logger = Scribe("LogicState")


class GnosticContext:
    """
    =================================================================================
    == THE GNOSTIC CONTEXT (V-Ω-TOTALITY-V100.0-LIVE-REFERENCE)                    ==
    =================================================================================
    The Sovereign Soul of the Logic Weaver.
    It maintains the absolute synchronicity between Thought (Variables) and
    Reality (Manifested Files).
    """

    def __init__(self, raw_shared_context: Dict[str, Any]):
        """
        The Rite of Inception.
        [THE CURE]: We bind to the reference of the shared dictionary.
        No copy is made. The Mind and the Hand are now one.
        """
        self._context = raw_shared_context

        # 1. THE RITE OF CONTEXTUAL ANCHORING
        # Ensure we have a physical root to ground the logic.
        if 'project_root' not in self._context:
            found_root, _ = find_project_root(Path.cwd())
            self._context['project_root'] = found_root or Path.cwd()

        # [ASCENSION 7]: TYPE INVARIANT ENFORCEMENT
        if isinstance(self._context['project_root'], str):
            self._context['project_root'] = Path(self._context['project_root'])

        # 2. THE VIRTUAL REALITY ENGINE (SYNCED)
        # [ASCENSION 3]: We initialize the manifest as a list inside the shared dict
        # so that external adjudicators (like the Validator) can perceive it.
        if 'generated_manifest' not in self._context:
            self._context['generated_manifest'] = []

        # 3. INITIAL PURIFICATION
        self.purify()

    def purify(self):
        """
        [ASCENSION 5]: ACHRONAL BOOLEAN PURIFICATION.
        Transmutes string truths into logical bits in-place.
        """
        for k, v in list(self._context.items()):
            if isinstance(v, str):
                lower_v = v.lower().strip()
                if lower_v in ('true', 'yes', '1', 'on'):
                    self._context[k] = True
                elif lower_v in ('false', 'no', '0', 'off'):
                    self._context[k] = False

    def register_virtual_file(self, path: Path):
        """
        [ASCENSION 4]: GEOMETRIC PATH NORMALIZATION.
        Inscribes a path into the shared Virtual Reality manifest.
        """
        # Force POSIX style to prevent Windows-mangled hashes
        clean_path = str(path).replace('\\', '/')

        manifest: List[str] = self._context['generated_manifest']
        if clean_path not in manifest:
            manifest.append(clean_path)
            Logger.verbose(f"Lattice: Inscribed virtual file: [dim]{clean_path}[/dim]")

    @contextmanager
    def mask(self, overrides: Dict[str, Any]):
        """
        [ASCENSION 2]: TRANSACTIONAL MASKING (SCOPED TRUTH).
        Temporarily overlays variables for a specific logical branch.
        Restores the original truth upon exit.
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

    def get(self, key: str, default: Any = None) -> Any:
        """
        [ASCENSION 6]: THE DEFENSIVE GAZE.
        Gracefully resolves variables from the live context.
        """
        return self._context.get(key, default)

    @property
    def raw(self) -> Dict[str, Any]:
        """
        Returns the LIVE reference to the Gnostic Soul.
        Use this to feed the Alchemist or Adjudicator.
        """
        return self._context

    @property
    def project_root(self) -> Path:
        """Type-safe accessor for the Gnostic Anchor."""
        return self._context['project_root']

    def scry(self) -> str:
        """
        [ASCENSION 9]: FORENSIC STATE TOMOGRAPHY.
        Exports a sanitized, JSON-safe view of the current truth.
        """
        import json

        def _sanitize(val):
            if isinstance(val, Path): return str(val)
            if isinstance(val, set): return list(val)
            return val

        safe_truth = {k: _sanitize(v) for k, v in self._context.items()
                      if not k.startswith('_')}  # Hide internal meta

        return json.dumps(safe_truth, indent=2)

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_CONTEXT entries={len(self._context)} state=RESONANT>"

# == SCRIPTURE SEALED: THE KEEPER OF TRUTH IS UNBREAKABLE ==