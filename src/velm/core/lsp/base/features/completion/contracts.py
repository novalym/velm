# Path: core/lsp/base/features/completion/contracts.py
# ----------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_CONTEXT_IMMUTABLE_V100
# SYSTEM: CEREBRAL_CORTEX | ROLE: STATE_SNAPSHOT

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from .models import CompletionItem


@dataclass(frozen=True)
class CompletionContext:
    """
    =============================================================================
    == THE PROPHETIC CONTEXT (V-Ω-TOTALITY-V100)                               ==
    =============================================================================
    Captures the absolute state of the reality at the exact moment of the trigger.
    Passed to every Prophet to inform their vision.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Isomorphic Spatial Anchor:** Includes `project_root` to ensure relative
        path completions are mathematically absolute.
    2.  **Full-Spectrum Content:** Carries `full_content` to allow the Artisan
        to scan for variables outside the current line's view.
    3.  **Geometric Coordinate:** Precise `{line, character}` and `offset`
        for compatibility with different tokenizer strategies.
    4.  **Aura Perception:** `context_type` (form/will/soul) identifies if we
        are in a Blueprint, Symphony, or Code block.
    5.  **Lexical State:** `is_inside_jinja` and `is_inside_comment` flags
        prevent "Gnostic Noise" in strings/comments.
    6.  **Metabolic Chronometry:** `start_time_ns` allows providers to self-throttle
        to maintain 60fps interaction speed.
    7.  **Causal Lineage:** Suture for `trace_id` and `session_id` for
        distributed forensic debugging.
    8.  **Trigger Dialect:** Decodes LSP `trigger_kind` into human-readable
        intents (INVOKED vs CHARACTER).
    9.  **Hierarchy Awareness:** `parent_block` identifies if we are inside
        an @if gate or a %% maestro block.
    10. **Token Memory:** `token_budget` signals to providers how many
        suggestions the UI can comfortably materialize.
    11. **User Identity:** `persona` mapping to filter suggestions by
        Architect Grade (Initiate vs Master).
    12. **Holographic Metadata:** `client_info` helps tune snippet output
        for specific IDE capabilities.
    """

    # --- I. SPATIAL & IDENTITY ---
    uri: str
    project_root: str
    session_id: str

    # --- II. TEXTUAL SOUL ---
    full_content: str
    line_text: str
    line_prefix: str  # Matter to the left of the cursor

    # --- III. GEOMETRIC COORDINATES ---
    position: Dict[str, int]  # {'line': L, 'character': C}
    offset: int  # Flat byte offset from dawn of file

    # --- IV. TRIGGER PHYSICS ---
    trigger_character: Optional[str]
    trigger_kind: int  # 1=Invoked, 2=TriggerChar, 3=Incomplete
    language_id: str  # 'scaffold', 'symphony', 'python', etc.

    # --- V. AURA & STATE ---
    context_type: str  # 'form', 'will', 'logic', 'metadata', 'soul'
    is_inside_jinja: bool
    is_inside_comment: bool
    is_inside_string: bool
    parent_block: Optional[str] = None
    trace_id: str = "0xVOID"

    # --- VI. METABOLIC METRICS ---
    start_time_ns: int = field(default_factory=time.perf_counter_ns)
    token_budget: int = 50
    persona: str = "architect"

    # [ASCENSION 12]: HOLOGRAPHIC METADATA
    client_info: Dict[str, Any] = field(default_factory=dict)

    @property
    def elapsed_ms(self) -> float:
        """Calculates the age of this context context in milliseconds."""
        return (time.perf_counter_ns() - self.start_time_ns) / 1_000_000


class CompletionProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF THE PROPHET (INTERFACE)                                 ==
    =============================================================================
    The abstract contract for all sources of foresight.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the prophetic source."""
        pass

    @property
    def priority(self) -> int:
        """
        Determines the sort weight (0-100).
        Higher numbers appear first in the UI.
        """
        return 50

    @abstractmethod
    def provide(self, context: CompletionContext) -> List[CompletionItem]:
        """
        [THE RITE OF PROPHECY]
        Analyzes the context and proclaims potential futures.
        """
        pass

    def resolve(self, item: CompletionItem) -> CompletionItem:
        """
        [THE RITE OF RESOLUTION]
        Lazy-loads heavy Gnosis (like Markdown docs) when the user focuses
        on a specific suggestion. Default is instant revelation.
        """
        return item