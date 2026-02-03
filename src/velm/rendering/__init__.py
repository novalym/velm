# scaffold/rendering/tree_renderer.py

from pathlib import Path
from typing import List, Union, Optional, Any

from rich.console import Group as RenderableGroup

from .json_renderer import JSONRenderer
# --- THE DIVINE SUMMONS ---
from .svg_renderer import SVGRenderer
from .text_renderer import TextRenderer
from .lfg_scribe import LogicFlowGraphScribe
from ..contracts.data_contracts import ScaffoldItem, GnosticLineType
from ..contracts.heresy_contracts import ArtisanHeresy


def render_gnostic_tree(
        items: List[ScaffoldItem],
        output_format: str = 'text',
        use_markup: bool = True,
        project_root: Optional[Path] = None,
        **kwargs: Any  # <--- THE POLYMORPHIC CONDUIT
) -> Union[str, RenderableGroup]:
    """
    =================================================================================
    == THE GOD-ENGINE OF ARCHITECTURAL REVELATION (V-Ω-PURIFIED-ULTIMA)            ==
    =================================================================================
    LIF: 10,000,000,000

    This is the one true, public rite for rendering a Gnostic Tree. It is a divine,
    polyglot Conductor that gazes upon the Architect's will (`output_format`) and
    summons the correct Scribe from the Pantheon to proclaim the project's soul.

    It enforces the **Law of Visual Truth**: It performs a final, paranoid filtration
    to ensure that abstract thoughts (`LOGIC`, `VARIABLES`, `COMMENTS`) never
    manifest as physical ghosts in the visual tree.

    Args:
        items (List[ScaffoldItem]): The pure Gnostic Plan to be rendered.
        output_format (str): The desired tongue ('text', 'svg', 'json').
        use_markup (bool): The vow for the 'text' Scribe to speak with or
                           without luminous `rich` markup.
        project_root (Optional[Path]): The sacred sanctum of the project root.
        **kwargs (Any): Supplemental Gnosis (e.g., enabled_inquisitors).

    Returns:
        Union[str, RenderableGroup]: The final scripture proclaimed by the Scribe.
    =================================================================================
    """
    # --- MOVEMENT I: THE RITE OF SANCTUM ADJUDICATION ---
    resolved_project_root = project_root or Path.cwd()

    # --- MOVEMENT II: THE RITE OF FINAL PURIFICATION (THE UNBREAKABLE WARD) ---
    # We act as the final filter. Even if the upstream Titan faltered,
    # this artisan ensures no Logic Ghosts or Variable Phantoms can pass.
    pure_items = [
        item for item in items
        if item.line_type not in (
            GnosticLineType.LOGIC,
            GnosticLineType.VARIABLE,
            GnosticLineType.COMMENT,
            GnosticLineType.VOID
        )
        # We also filter out items that have no path, unless they are root markers.
        and item.path is not None
    ]

    # --- MOVEMENT III: THE DIVINE TRIAGE OF WILL ---
    try:
        if output_format == 'svg':
            # The Celestial Scribe is summoned with the sacred Gnosis of the sanctum.
            renderer = SVGRenderer(pure_items, resolved_project_root, **kwargs)

        elif output_format == 'json':
            # The Machine's Scribe is summoned.
            renderer = JSONRenderer(pure_items, **kwargs)

        else:  # Default to 'text'
            # The Luminous Scribe is summoned, honoring the vow of `use_markup`.
            renderer = TextRenderer(pure_items, use_markup=use_markup, **kwargs)

        # --- MOVEMENT IV: THE FINAL PROCLAMATION ---
        return renderer.render()

    except Exception as e:
        # The Unbreakable Ward of Paradox.
        raise ArtisanHeresy(
            f"A catastrophic paradox occurred within the '{output_format}' Scribe.",
            details=f"{type(e).__name__}: {str(e)}"
        ) from e




# --- THE DIVINE CODEX OF PROCLAMATION ---
# We proclaim the sacred, public API of this sanctum to the cosmos,
# ensuring all who commune with it know its one true name.
__all__ = ["render_gnostic_tree","LogicFlowGraphScribe"]