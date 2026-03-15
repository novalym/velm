# scaffold/semantic_injection/directives/ui_knowledge/__init__.py

"""
=================================================================================
== THE GATEWAY OF FORMS (V-Ω-FACADE)                                           ==
=================================================================================
This is the single entry point for all UI generation logic.
It aggregates the registries from React, Python, Go, and HTML sub-sanctums.
=================================================================================
"""
from typing import List, Tuple, Optional

from . import auth_form
from . import command_palette
from . import data_table
from . import go_ui  # BubbleTea
from . import html_ui  # Pure HTML/CSS
from . import layouts  # <--- ADD THIS
from . import multi_step_wizard
from . import python_ui  # Streamlit/Gradio/Textual
# 2. Summon the Sub-Sanctums (The Registration Side-Effects)
# Importing these packages executes their code, which triggers the
# @ComponentRegistry.register decorators, populating the Memory.
from . import react  # React/Tailwind
# 1. Summon the Registry (The Memory)
from .registry import ComponentRegistry
# 3. Summon the User Loader
from .user_loader import load_user_generators


# 3. The Public Rite (The Facade)
# This is the function that UiDomain calls. It looks up the requested component
# in the now-populated Registry.
def get_deterministic_component(name: str, props_list: List[Tuple[str, str]]) -> Optional[str]:
    """
    The Universal Lookup.
    Now enhanced with the ability to perceive User-Defined Generators.
    """
    # [ELEVATION] Lazy-load user generators from the current context
    # We assume CWD or finding root is safe here.
    load_user_generators()

    generator = ComponentRegistry.get_generator(name)
    if generator:
        return generator(name, props_list)
    return None


__all__ = ["get_deterministic_component", "ComponentRegistry"]