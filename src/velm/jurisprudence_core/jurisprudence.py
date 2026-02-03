# scaffold/jurisprudence_core/jurisprudence.py

from typing import List, Any, Optional, Dict
from pathlib import Path
from rich.panel import Panel
from rich.text import Text
from rich.console import Group

# --- THE SACRED IMPORTS OF THE GNOSTIC CONTRACTS ---
from ..contracts.data_contracts import ScaffoldItem
from ..contracts.heresy_contracts import Heresy, HeresySeverity
from ..core.jurisprudence.contracts import AdjudicationContext
from ..core.jurisprudence.adjudicator import VowAdjudicator

# --- THE SACRED IMPORTS OF THE UNIFIED CORE ---
from .heresy_codex import HERESY_CODEX
from .architectural_grimoire import PROPHETIC_ARCHITECTURAL_GRIMOIRE


def forge_heresy_vessel(
        key: str,
        line_num: int = 1,
        line_content: str = "",
        details: str = "",
        # ★★★ THE MISSING ARGUMENT ★★★
        internal_line: Optional[int] = None
) -> Heresy:
    """
    Forges a Heresy. If internal_line (0-indexed) is provided,
    it will be preserved. Otherwise, it will be derived.
    """
    # Logic to get message/code from Grimoire based on 'key'...

    return Heresy(
        code=key,
        message=f"Gnostic Paradox: {key.replace('_', ' ').title()}",
        line_num=line_num,
        internal_line=internal_line,  # Pass it through!
        line_content=line_content,
        details=details
    )

def conduct_architectural_inquest(items: List[ScaffoldItem]) -> List[Panel]:
    """
    The Grand Rite of Adjudication.
    Iterates through the Prophetic Architectural Grimoire and judges the reality.
    Returns a list of luminous Panels containing the Mentor's guidance.
    """
    panels = []

    # 1. The Gaze upon the Cosmos (Blueprint Level)
    for prophecy in PROPHETIC_ARCHITECTURAL_GRIMOIRE:
        if prophecy.get("scope") == "BLUEPRINT":
            if prophecy["detector"](items):
                panels.append(_forge_adjudication_panel(prophecy, None, items))

    # 2. The Gaze upon the Atom (Item Level)
    for item in items:
        for prophecy in PROPHETIC_ARCHITECTURAL_GRIMOIRE:
            if prophecy.get("scope") == "ITEM":
                if prophecy["detector"](item):
                    panels.append(_forge_adjudication_panel(prophecy, item, items))

    return panels

def _forge_adjudication_panel(prophecy: Dict[str, Any], item: Optional[ScaffoldItem],
                              all_items: List[ScaffoldItem]) -> Panel:
    """Forges a luminous panel for the Mentor's guidance."""
    prophecy_data = prophecy["prophecy"]
    suggestion_rite = prophecy_data["suggestion_rite"]

    # The rite is bestowed with the full Gnosis it may require.
    suggestion = suggestion_rite(item or all_items)

    title = "Architectural Guidance"
    style = "yellow"

    content = Group(
        Text(suggestion, style="white"),
        Text(f"\nScope: {prophecy.get('scope')}", style="dim")
    )

    return Panel(content, title=f"[bold {style}]{title}[/]", border_style=style)

def forge_adjudicator(context: Dict[str, Any] = None):
    """
    =================================================================================
    == THE GOD-ENGINE OF JURISPRUDENCE FORGING (V-Ω-ETERNAL-APOTHEOSIS-HEALED)     ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE)

    This is the divine artisan in its final, eternal, and ultra-definitive form.
    The profane concept of a "headless" adjudicator has been annihilated. It now
    understands the one true, sacred law: An Adjudicator cannot exist without a
    complete `AdjudicationContext`.

    It now forges and returns the one true `VowAdjudicator`, its soul consecrated
    with a pure, Gnostically-aware context, healing the `TypeError` heresy for
    all time.
    """
    # --- THE FORGING OF THE GNOSTIC CONTEXT ---
    gnostic_context_vars = context or {}

    # The `LogicWeaver` must be taught to place its project_root in the context.
    # For now, we gracefully fall back to the Current Working Directory if not provided.
    project_root = gnostic_context_vars.pop('project_root', Path.cwd())

    # The sacred vessel is forged.
    # [THE CURE] We inject 'cwd' using the project_root as the anchor.
    adjudication_context = AdjudicationContext(
        project_root=project_root,
        variables=gnostic_context_vars,
        cwd=project_root
    )

    # The High Adjudicator is summoned, its soul whole and pure.
    return VowAdjudicator(adjudication_context)