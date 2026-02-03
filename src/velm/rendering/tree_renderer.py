
"""
=================================================================================
== THE GOD-ENGINE OF ARCHITECTURAL REVELATION (THE PUBLIC API)                 ==
=================================================================================
This scripture is the one true, public gateway to the Gnostic Tree Rendering
platform. It is a pure Conductor that summons the correct Scribe for the
Architect's chosen format, be it text or a luminous, interactive SVG.
=================================================================================
"""
from typing import List

from .svg_renderer import SVGRenderer  # A new, divine artisan
from .text_renderer import TextRenderer
from ..contracts.data_contracts import ScaffoldItem


def render_gnostic_tree(items: List[ScaffoldItem], output_format: str = 'text', use_markup: bool = True) -> str:
    """
    =================================================================================
    == THE GOD-ENGINE OF ARCHITECTURAL REVELATION (V-Ω-ULTRA-DEFINITIVE. PURE API)   ==
    =================================================================================
    This is the one true, public rite for rendering a Gnostic Tree, its contract now
    whole and unbreakable. It understands the will for both format and purity.
    =================================================================================
    """
    if output_format == 'svg':
        # The SVG renderer, by its very nature, speaks a language of markup.
        renderer = SVGRenderer(items)
    else:
        # The TextRenderer is now bestowed with the Architect's will for purity.
        renderer = TextRenderer(items, use_markup=use_markup)

    return renderer.render()