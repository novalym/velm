# === [scaffold/artisans/distill/core/oracle/diviner.py] - SECTION 1 of 1: The Ascended Diviner ===
import time
from pathlib import Path
from typing import Set, Dict, List, Optional, Any

from .....logger import Scribe
from .contracts import OracleContext
from .....contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("OracleDiviner")


class OracleDiviner:
    """
    =================================================================================
    == THE FACULTY OF DIVINATION (V-Ω-SYMBOLIC-RESOLVER-ULTIMA)                    ==
    =================================================================================
    LIF: 100,000,000,000,000 (THE SEER OF SEEDS)

    The Second Movement of the Oracle.
    It transmutes the Architect's vague Intent (Keywords, Natural Language, Errors)
    into concrete, physical Seed Files that serve as the roots of the Distillation.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Symbolic Resolution (THE FIX):** Uses the Cortex's `symbol_multimap` to
        map abstract symbols ("MyClass") to physical files ("src/my_class.py").
    2.  **The JIT Awakening:** Lazily imports heavy semantic and forensic engines only
        when required, preventing circular import heresies.
    3.  **The Physical Gaze:** Checks if a focus keyword matches an exact file path
        on disk before attempting symbolic lookup.
    4.  **The Fuzzy Resonance:** If symbolic lookup fails, scans all known file paths
        for substring matches (e.g., "auth" matches "src/auth/service.py").
    5.  **The Semantic Seer:** If `profile.feature` is set, summons the `SemanticEngine`
        (RAG/Vector) to find files conceptually related to the request.
    6.  **The Forensic Detective:** If `profile.problem_context` is set, summons the
        `ForensicInquisitor` to parse stack traces and indict guilty files.
    7.  **The Contextual Scribe:** Annotates every seed file with the *reason* for its
        selection ("Explicit Focus", "Symbol: User", "Semantic Hit").
    8.  **The Deduplication Ward:** Ensures a file is not added multiple times for
        different reasons, though all reasons are chronicled.
    9.  **The Path Normalizer:** Forces all seed paths to be POSIX-style relative
        strings, ensuring harmony with the Graph and Ranker.
    10. **The Telemetric Pulse:** Records precise timing data for the divination rite.
    11. **The Unbreakable Ward:** Gracefully handles missing memory or empty profiles.
    12. **The Intent Analyst:** Uses the `IntentAnalyzer` to expand natural language
        queries into broader search terms.
    """

    def __init__(self, root: Path, silent: bool = False):
        self.root = root
        self.silent = silent

        # --- FACULTY 2: THE JIT AWAKENING (HEALED) ---
        try:
            # [FIX]: New Core Imports
            from .....core.semantics.engine import SemanticEngine
            from .....core.semantics.intent import IntentAnalyzer
            self.semantics_cls = SemanticEngine
            self.intent_cls = IntentAnalyzer
        except ImportError as e:
            if not self.silent: Logger.warn(f"Semantic faculty is dormant ({e}).")
            self.semantics_cls = None
            self.intent_cls = None

        try:
            from ..forensics.engine import ForensicInquisitor
            self.forensics_cls = ForensicInquisitor
        except ImportError:
            if not self.silent: Logger.warn("Forensic faculty is dormant. Error log analysis is disabled.")
            self.forensics_cls = None

    def divine(self, context: OracleContext):
        """
        The Grand Rite of Divination.
        Populates `context.seed_files` and `context.context_reasons`.
        """
        t0 = time.time()

        # --- MOVEMENT I: THE STRUCTURAL GAZE (FOCUS) ---
        self._divine_structural_seeds(context)

        # --- MOVEMENT II: THE SEMANTIC GAZE (INTENT) ---
        self._divine_semantic_seeds(context)

        # --- MOVEMENT III: THE FORENSIC GAZE (PROBLEM) ---
        self._divine_forensic_seeds(context)

        duration = (time.time() - t0) * 1000
        context.record_stat('divination_ms', duration)

        if not self.silent and context.seed_files:
            Logger.info(f"Divination complete. {len(context.seed_files)} seed(s) identified.")

    def _divine_structural_seeds(self, context: OracleContext):
        """
        [FACULTY 1 & 3 & 4] The Symbolic and Physical Resolution.
        Maps `profile.focus_keywords` to file paths.
        """
        profile = context.profile
        if not profile.focus_keywords:
            return

        # We need the memory to look up symbols
        memory = context.memory
        if not memory:
            # Fallback to simple path checking if memory is void
            for keyword in profile.focus_keywords:
                if (self.root / keyword).exists():
                    self._add_seed(context, keyword, "Explicit Focus")
            return

        for keyword in profile.focus_keywords:
            found = False

            # 1. The Physical Gaze (Exact Path)
            # We check if the keyword is a valid path relative to root
            potential_path = self.root / keyword
            if potential_path.exists():
                norm_path = str(potential_path.relative_to(self.root)).replace('\\', '/')
                self._add_seed(context, norm_path, "Explicit Focus")
                found = True

            # 2. The Symbolic Gaze (Symbol Resolution)
            # We check if the keyword is a Class, Function, or Module name known to the Cortex.
            if keyword in memory.symbol_multimap:
                files = memory.symbol_multimap[keyword]
                for f in files:
                    self._add_seed(context, f, f"Symbol: {keyword}")
                found = True

            # 2b. The Qualified Symbolic Gaze (e.g. "my_module.MyClass")
            # If exact match failed, try splitting by dot
            if not found and '.' in keyword:
                simple_name = keyword.split('.')[-1]
                if simple_name in memory.symbol_multimap:
                    files = memory.symbol_multimap[simple_name]
                    for f in files:
                        self._add_seed(context, f, f"Symbol: {keyword}")
                    found = True

            # 3. The Fuzzy Resonance (Path Substring)
            # If it's not a specific file or symbol, maybe it's a directory or partial name.
            if not found:
                keyword_lower = keyword.lower()
                for file_gnosis in memory.inventory:
                    path_str = str(file_gnosis.path).replace('\\', '/')
                    if keyword_lower in path_str.lower():
                        self._add_seed(context, path_str, f"Path Resonance: {keyword}")
                        found = True

            if not found and not self.silent:
                Logger.verbose(f"   -> The Oracle found no resonance for focus keyword: '{keyword}'")

    def _divine_semantic_seeds(self, context: OracleContext):
        """[FACULTY 5 & 12] Semantic Search."""
        profile = context.profile
        if not profile.feature or not self.semantics_cls or not context.memory:
            return

        if not self.silent: Logger.info("Consulting Semantic Memory for intent...")

        engine = self.semantics_cls(self.root, silent=True)
        # Note: SemanticEngine handles intent analysis internally now
        semantic_hits = engine.search(
            profile.feature,
            context.memory,
            limit=5,  # Top 5 relevant files
            interactive=profile.interactive_mode
        )

        if semantic_hits:
            if not self.silent: Logger.success(f"Semantic Resonance found {len(semantic_hits)} matches.")
            for f in semantic_hits:
                self._add_seed(context, f, "Semantic Resonance")

    def _divine_forensic_seeds(self, context: OracleContext):
        """[FACULTY 6] Forensic Analysis."""
        profile = context.profile
        if not profile.problem_context or not self.forensics_cls:
            return

        if not self.silent: Logger.info("Conducting Forensic Inquest on problem context...")

        inquisitor = self.forensics_cls(silent=True)
        temp_scores = {}
        # The Inquisitor updates temp_scores in-place based on stack trace parsing
        inquisitor.gaze(profile.problem_context, temp_scores)

        forensic_hits = list(temp_scores.keys())
        if forensic_hits:
            if not self.silent: Logger.success(f"Forensics identified {len(forensic_hits)} implicated files.")
            for path in forensic_hits:
                self._add_seed(context, path, "Forensic Trace")

    def _add_seed(self, context: OracleContext, path: str, reason: str):
        """[FACULTY 7, 8, 9] Adds a seed with normalization and reasoning."""
        # Normalize to POSIX
        clean_path = path.replace('\\', '/')

        # Verify existence in the current reality (if we have memory)
        if context.memory:
            # Check if this path exists in the inventory keys
            # (Inventory keys are usually relative posix paths)
            if clean_path not in context.memory.project_gnosis and not any(
                    str(f.path).replace('\\', '/') == clean_path for f in context.memory.inventory):
                # It might be a directory?
                if (self.root / clean_path).is_dir():
                    # If directory, expand to all files inside?
                    # For V1, we leave directory expansion to the user or fuzzy match
                    pass
                else:
                    # Logger.verbose(f"   -> Seed '{clean_path}' not found in Cortex Memory. Ignoring.")
                    pass
                    # We can still add it if it exists on disk but missed by scanner (e.g. ignored file)
                    if (self.root / clean_path).exists():
                        pass
                    else:
                        return

        context.seed_files.add(clean_path)
        context.add_reason(clean_path, reason)