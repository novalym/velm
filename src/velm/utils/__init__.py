# ========================================================================================
# ==   SANCTUM: The Gateway of Explicit Gnosis (V-Ω-Bisection-Healed)                 ==
# ==   PURPOSE: To serve as the one, true, and stable gateway to all utility artisans,  ==
# ==            annihilating the paradox of circularity through explicit proclamation.  ==
# ========================================================================================
__version__ = "0.1.0"
from .archetype_utils import *
# --- I. THE PROCLAMATION OF THE PURE FOUNDATION ---
# The Gnosis from the new, pure converters codex is summoned first. It has no
# dependencies and can be proclaimed with absolute safety. This makes its Gnosis
# available for all subsequent proclamations. The Ouroboros is slain.
from .converters import *
# --- II. THE PROCLAMATION OF THE CORE SCRIBES ---
# With the foundational Gnosis now manifest, the Nexus can safely summon the
# application-aware scribes, which may depend on the rites proclaimed above.
from .core_utils import *
from .core_utils import _resilient_rename
from .ephemeral_server import *
from .gnosis_discovery import *
from .resolve_gnostic_content import resolve_gnostic_content_v2

# --- III. THE FORGING OF THE CODEX OF PROCLAIMED GNOSIS ---
# The Codex is now a complete and pure chronicle of all available Gnosis.
__all__ = [
    # From converters.py
    'to_pascal_case',
    'to_snake_case',
    'to_camel_case',
    'to_kebab_case',
    'to_upper_case',
    'to_lower_case',

    # From core_utils.py (example names)
    '_resilient_rename',
    'is_binary_extension',
    'is_binary',
    'atomic_write',
    'get_git_branch',
    'get_git_commit',
    'find_project_root',
    'hash_file',
    'perform_alchemical_resolution',
    'set_language_context',
    'inherit_project_gnosis',
    'summon_editor_for_multiline_soul',
    'to_string_safe',
    'is_poetry_installed',
    'is_git_installed',
    'get_os_type',
    'is_valid_path_segment',
    'gnostic_glob',
    'generate_derived_names',
    'get_ignore_spec',
    'perceive_state',
    'chronicle_state',
    #gnosis_discovery.py
    'discover_required_gnosis',
    #archetype_utils.py
    'get_all_known_kits',
    'get_all_known_archetypes',
    'commune_with_celestial_sanctum',
    'get_human_readable_size',
    # ... and any other function from core_utils you wish to expose
    #resolve_gnostic_content
    'resolve_gnostic_content_v2',
    #ephemeral_server.py
    'launch_ephemeral_server'
]

