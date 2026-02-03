# Path: artisans/completion_artisan/prophets/base.py
# --------------------------------------------------
# LIF: INFINITY | ROLE: ANCESTRAL_PROPHET_CONTRACT | RANK: SOVEREIGN
# auth_code: Ω_BASE_PROPHET_TOTALITY_V12_SINGULARITY

import time
import logging
import traceback
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

# --- CORE UPLINKS ---
from ....logger import Scribe


class BaseProphet(ABC):
    """
    =================================================================================
    == THE ANCESTRAL PROPHET (V-Ω-TOTALITY-V12-LAZY-BINDING)                       ==
    =================================================================================
    The fundamental soul of every completion provider.
    [THE CURE]: This version uses Lazy Properties to resolve the 'canon' Schism.
    """

    def __init__(self, artisan: Any):
        """
        Consecrates the Prophet and binds it to the Orchestrator.
        """
        # We store a reference to the parent artisan (CompletionArtisan)
        self.artisan = artisan

        # [ASCENSION 7]: Logger Grafting
        self.logger = Scribe(f"Prophet:{self.name}")

        # [ASCENSION 10]: Shadow Awareness
        self.is_shadow_aware = True

    # =============================================================================
    # == [THE FIX]: LAZY FACULTY PROPERTIES                                      ==
    # =============================================================================
    # These properties allow the Prophet to access the Orchestrator's faculties
    # ONLY when they are needed, preventing boot-time AttributeErrors.

    @property
    def canon(self) -> Any:
        """Accesses the Knowledge Base of the Orchestrator."""
        return getattr(self.artisan, 'canon', None)

    @property
    def engine(self) -> Any:
        """Accesses the God-Engine Singleton."""
        return getattr(self.artisan, 'engine', None)

    @property
    def alchemist(self) -> Any:
        """Accesses the Alchemical Transmuter."""
        return getattr(self.artisan, 'alchemist', None)

    @property
    def name(self) -> str:
        """[ASCENSION 2]: Sovereign Identity."""
        return self.__class__.__name__.replace("Prophet", "").upper()

    # =============================================================================
    # == THE RITE OF PROPHECY                                                    ==
    # =============================================================================

    @abstractmethod
    def prophesy(self, ctx: Any) -> List[Dict[str, Any]]:
        """
        [THE SOUL OF THE PROPHET]
        Must be implemented by concrete prophets to provide their specific Gnosis.
        """
        pass

    def speak(self, ctx: Any) -> List[Dict[str, Any]]:
        """
        [THE PUBLIC GATEWAY]
        Executes the prophecy with timing, safety, and aversion logic.
        """
        # [ASCENSION 5]: Lexical Aversion
        if not self.should_speak(ctx):
            return []

        # [ASCENSION 3 & 4]: Timed Execution with Sarcophagus
        start_ns = time.perf_counter_ns()
        try:
            results = self.prophesy(ctx)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if duration_ms > 10:
                self.logger.warn(f"Slow Revelation: {duration_ms:.2f}ms")

            return results or []

        except Exception as fracture:
            # [ASCENSION 4]: Fault Isolation
            self.logger.error(f"Prophetic Fracture: {fracture}")
            # Inscribe autopsy to stderr for the Architect
            # import traceback
            # traceback.print_exc()
            return []

    def should_speak(self, ctx: Any) -> bool:
        """
        [HEURISTIC]: Determines if this prophet has anything to say in the
        current logical spacetime. Override in subclasses for specific gating.
        """
        # Default: Don't speak in comments
        return not ctx.is_inside_comment

    # =============================================================================
    # == ALCHEMICAL HELPERS                                                      ==
    # =============================================================================

    def inject_priority(self, items: List[Dict], priority_score: int) -> List[Dict]:
        """[ASCENSION 6]: Standardizes sortText for the council."""
        prefix = f"{priority_score:03d}_"
        for item in items:
            if 'sortText' not in item:
                item['sortText'] = prefix + item['label']
        return items

    def align_indentation(self, text: str, ctx: Any) -> str:
        """[ASCENSION 11]: Mirrors the Architect's grid."""
        if '\n' not in text:
            return text

        lines = text.split('\n')
        # Preserve first line, indent the rest to match current line
        return lines[0] + '\n' + '\n'.join([f"{ctx.indent_str}{l}" for l in lines[1:]])

# === SCRIPTURE SEALED: THE ANCESTRAL SOUL IS RESTORED ===