# scaffold/semantic_injection/directives/ui_knowledge/react/__init__.py

"""
=================================================================================
== THE REACT PANTHEON (V-Ω-INIT)                                               ==
=================================================================================
This sanctum aggregates all React/Tailwind component generators.
Importing this package automatically registers all React components into the
Global ComponentRegistry.
=================================================================================
"""

# We import these submodules for their side-effects (Registration Decorators).
from . import atoms
from . import charts
from . import data_display
from . import disclosure
from . import feedback
from . import forms_advanced
from . import menus
from . import molecules
from . import navigation_complex
from . import overlays
from . import structures
from . import visuals

# No public exports are needed; the Registry is a Singleton.

