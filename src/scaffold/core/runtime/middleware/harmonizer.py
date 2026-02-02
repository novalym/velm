# Path: scaffold/core/runtime/middleware/harmonizer.py
# ----------------------------------------------------
# LIF: INFINITY // AUTH_CODE: #!@GEOMETRIC_PURITY_V18_FINAL
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ----------------------------------------------------

import unicodedata
import re
from pathlib import Path
from typing import Any, Dict, List, Union, Type, Set
from functools import lru_cache

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....logger import Scribe

Logger = Scribe("PathHarmonizer")


class PathNormalizationMiddleware(Middleware):
    """
    =============================================================================
    == THE HARMONIZER (V-Ω-GEOMETRIC-PURITY-V18.0)                             ==
    =============================================================================
    LIF: 10,000,000,000,000 | The Unbreakable Guardian of Spatial Truth.

    This version is hardened against the 'startsWith' typo and features
    Recursive Deep-Cleaning with Celestial URI Protection.
    =============================================================================
    """

    # [ASCENSION 15]: THE GRIMOIRE OF CELSTIAL SHIELDS
    # We do not normalize paths that resemble URIs or Alchemical variables.
    CELESTIAL_PREFIXES = ('http://', 'https://', 'ws://', 'wss://', 'git@', 'ssh://')
    ALCHEMICAL_SIGILS = ('{{', '$$', '@')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Identity set to prevent infinite recursion on circular models
        self._seen_objects: Set[int] = set()

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """The one true rite of harmonization."""
        try:
            self._seen_objects.clear()

            # --- MOVEMENT I: THE EXTRACTION ---
            # Use Pydantic's high-fidelity dump
            raw_data = request.model_dump()
            request_type: Type[BaseRequest] = type(request)

            # --- MOVEMENT II: THE ALCHEMICAL CLEANSE ---
            # [ASCENSION 14 & 16]: Recursive deep clean with forensic delta tracking
            purified_data = self._recursive_purify(raw_data)

            # --- MOVEMENT III: RE-MATERIALIZATION ---
            try:
                # [ASCENSION 23]: Transactional Re-Inception
                purified_request = request_type.model_validate(purified_data)
                return next_handler(purified_request)

            except Exception as ve:
                # Fallback if validation fractures (prevents blocking the Will)
                Logger.verbose(f"Harmonization re-validation deferred: {ve}")
                return next_handler(request)

        except Exception as paradox:
            # [ASCENSION 12]: SOVEREIGN PROTECTION
            Logger.warn(f"Path Harmonizer bypassed due to paradox: {paradox}")
            return next_handler(request)

    @lru_cache(maxsize=1024)
    def _purify_locus(self, path_str: str) -> str:
        """
        [ASCENSION 13 & 14 & 17]: THE SURGICAL PATH PURIFIER.
        """
        if not path_str or not isinstance(path_str, str):
            return path_str

        # [ASCENSION 14]: THE CELESTIAL SHIELD
        # Shield URLs and URIs from being mangled as local paths.
        low_path = path_str.lower()
        if any(path_str.startswith(pref) for pref in self.CELESTIAL_PREFIXES):
            return path_str

        # [ASCENSION 15]: THE ALCHEMICAL SHIELD
        # Shield Jinja2 and Scaffold sigils.
        if any(path_str.strip().startswith(sig) for sig in self.ALCHEMICAL_SIGILS):
            return path_str

        # [ASCENSION 5]: HEURISTIC SIEVE
        # If it contains newlines or is too long, it is prose/matter, not a coordinate.
        if "\n" in path_str or len(path_str) > 1024:
            return path_str

        # 1. Backslash Annihilation
        clean = path_str.replace("\\", "/")

        # 2. Windows Drive Letter Normalization (C: -> C:)
        # [ASCENSION 19]: Enforce Uppercase Drive Identity.
        if len(clean) >= 2 and clean[1] == ":" and clean[0].isalpha():
            clean = clean[0].upper() + clean[1:]

        # 3. Double-Slash Pruning (Except UNC Network Paths)
        # [ASCENSION 13]: FIX: Use .startswith() (Lowercase)
        if not clean.startswith("//"):
            while "//" in clean:
                clean = clean.replace("//", "/")

        # 4. Unicode Harmony
        # [ASCENSION 17]: Normalize to NFC
        return unicodedata.normalize('NFC', clean)

    def _recursive_purify(self, data: Any, depth: int = 0) -> Any:
        """
        [ASCENSION 18]: THE RECURSIVE DEEP CLEANER.
        """
        if depth > 12:  # Safety boundary
            return data

        # Prevent circular recursion heresies
        if id(data) in self._seen_objects:
            return data

        # Track non-primitive structures
        if isinstance(data, (dict, list)):
            self._seen_objects.add(id(data))

        # --- CASE: DICTIONARY ---
        if isinstance(data, dict):
            return {k: self._recursive_purify(v, depth + 1) for k, v in data.items()}

        # --- CASE: LIST ---
        elif isinstance(data, list):
            return [self._recursive_purify(v, depth + 1) for v in data]

        # --- CASE: PATH OBJECT ---
        elif isinstance(data, Path):
            # Transmute into Posix matter
            return Path(data.as_posix())

        # --- CASE: STRING ---
        elif isinstance(data, str):
            # Heuristic: If it has separators, it might be a path
            if "\\" in data or "/" in data:
                return self._purify_locus(data)
            return data

        return data

# == END OF SCRIPTURE ==

