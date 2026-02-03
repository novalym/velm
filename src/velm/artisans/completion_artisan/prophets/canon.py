# Path: artisans/completion_artisan/prophets/canon.py
# ---------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_CANON_LIVING_TRUTH_V100
# SYSTEM: CEREBRAL_CORTEX | ROLE: DYNAMIC_INTROSPECTION_ENGINE
# =================================================================================

import time
import threading
import logging
from typing import Dict, List, Any, Optional

# --- CORE UPLINKS ---
from ....logger import Scribe

Logger = Scribe("GnosticCanon")


class GnosticCanon:
    """
    =============================================================================
    == THE GNOSTIC CANON (V-Ω-LIVE-INTROSPECTION-ENGINE)                       ==
    =============================================================================
    LIF: 10,000,000 | ROLE: DYNAMIC_TRUTH_HOLDER

    A self-updating registry that queries the Engine's live state.
    It bridges the gap between the Static Grimoire (Files) and the Living Runtime.

    [CAPABILITIES]:
    1. Polls the Engine via `IntrospectionRequest`.
    2. Caches the Truth to prevent metabolic burnout.
    3. Serves as the Single Source of Truth for Plugin Capabilities.
    """

    def __init__(self, engine):
        self.engine = engine
        self._cache: Dict[str, Any] = {}
        self._last_update = 0.0

        # [ASCENSION 1]: METABOLIC RATE (30s)
        # We refresh knowledge only when necessary to save cycles.
        self._ttl = 30.0

        # [ASCENSION 2]: THREAD SAFETY
        self._lock = threading.RLock()

    def _refresh_gnosis(self):
        """
        [THE RITE OF INTROSPECTION]
        Queries the God-Engine to reveal its internal capabilities.
        """
        now = time.time()

        # 1. TTL CHECK (Optimization)
        if self._cache and (now - self._last_update < self._ttl):
            return

        # 2. ENGINE GUARD
        if not self.engine:
            return

        with self._lock:
            try:
                # [ASCENSION 5]: LAZY IMPORT
                # Prevents circular dependency loops at module level
                from ....interfaces.requests import IntrospectionRequest

                # 3. DISPATCH THE PLEA
                # We ask for "all" topics to get a complete snapshot
                result = self.engine.dispatch(IntrospectionRequest(topic="all"))

                if result.success and result.data:
                    self._cache = result.data
                    self._last_update = now
                    # Logger.debug("Gnostic Canon synchronized with Runtime.")
                else:
                    Logger.warn("Introspection yielded void results.")

            except Exception as e:
                # [ASCENSION 3]: FAIL-OPEN PERSISTENCE
                # If we fail to update, we keep using the old cache rather than crashing.
                Logger.warn(f"Canon Synchronization Fractured: {e}")

    def _get_path(self, *keys) -> Any:
        """
        [ASCENSION 4]: DEEP TRAVERSAL
        Safely navigates the cached dictionary.
        """
        current = self._cache
        for key in keys:
            if not isinstance(current, dict): return None
            current = current.get(key)
        return current

    # =========================================================================
    # == I. THE ALCHEMICAL DOMAIN (FILTERS & FUNCTIONS)                      ==
    # =========================================================================

    @property
    def alchemist_filters(self) -> List[Dict]:
        """Returns dynamically registered Jinja2 filters."""
        self._refresh_gnosis()
        return self._get_path("scaffold_language", "alchemist_grimoire", "filters") or []

    @property
    def alchemist_functions(self) -> List[Dict]:
        """Returns dynamically registered Jinja2 globals/functions."""
        self._refresh_gnosis()
        return self._get_path("scaffold_language", "alchemist_grimoire", "functions") or []

    # =========================================================================
    # == II. THE SCAFFOLD DOMAIN (FORM)                                      ==
    # =========================================================================

    @property
    def scaffold_directives(self) -> List[Dict]:
        """Returns Directives (@if, @plugin) active in the runtime."""
        self._refresh_gnosis()
        return self._get_path("scaffold_language", "directives", "pantheon") or []

    @property
    def scaffold_sigils(self) -> List[Dict]:
        """Returns Sigils ($$, ::) active in the runtime."""
        self._refresh_gnosis()
        return self._get_path("scaffold_language", "sigils") or []

    # =========================================================================
    # == III. THE SYMPHONY DOMAIN (WILL)                                     ==
    # =========================================================================

    @property
    def symphony_edicts(self) -> List[Dict]:
        """Returns Edicts (>>, %%) active in the runtime."""
        self._refresh_gnosis()
        return self._get_path("symphony_language", "edicts", "pantheon") or []

    @property
    def symphony_vows(self) -> List[Dict]:
        """
        [ASCENSION 9]: VOW FLATTENING
        Returns a flat list of all Vows (??) from all categories.
        """
        self._refresh_gnosis()
        categories = self._get_path("symphony_language", "vows", "categories") or []

        flat_vows = []
        for cat in categories:
            pantheon = cat.get("pantheon", [])
            flat_vows.extend(pantheon)

        return flat_vows

    @property
    def symphony_polyglot(self) -> List[Dict]:
        """Returns supported Polyglot languages (py:, rs:)."""
        self._refresh_gnosis()
        return self._get_path("symphony_language", "polyglot_languages") or []