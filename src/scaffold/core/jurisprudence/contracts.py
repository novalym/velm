# Path: scaffold/core/jurisprudence/contracts.py
# ----------------------------------------------

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, List


@dataclass
class AdjudicationContext:
    """
    =============================================================================
    == THE VESSEL OF JUDGMENT (V-Ω-SANCTUM-AWARE)                              ==
    =============================================================================
    LIF: 100,000,000,000

    This immutable vessel has been ascended. It now carries not just the root of
    the cosmos, but the specific, evolving sanctum (CWD) from which judgment
    must be passed.
    """

    # --- The Universal Constants ---
    project_root: Path

    # === THE DIVINE HEALING ===
    # The vessel is now bestowed with the Gnosis of the current reality.
    cwd: Path
    # ==========================

    # --- The Memory of the Alchemist (Variables) ---
    variables: Dict[str, Any] = field(default_factory=dict)

    # --- The Context of Mutation (Patch Mode) ---
    file_content_buffer: Optional[str] = None
    target_file_path: Optional[Path] = None

    # --- The Context of Execution (Symphony Mode) ---
    last_process_result: Optional[Any] = None

    # --- The Context of Genesis (Form Mode) ---
    generated_manifest: List[str] = field(default_factory=list)