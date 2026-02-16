# Path: src/velm/jurisprudence/genesis_jurisprudence.py
# =========================================================================================
# == THE SACRED CODEX OF GENESIS JURISPRUDENCE (V-Ω-TOTALITY-V24000-OMEGA-FINALIS)       ==
# =========================================================================================
# LIF: INFINITY | ROLE: ARCHITECTURAL_CONSCIENCE | RANK: OMEGA_SUPREME
# AUTH: Ω_JURISPRUDENCE_V24K_SUBSTRATE_AWARE_2026_FINALIS
# =========================================================================================

import shutil
import os
import sys
import re
from typing import List, Dict, Any, Callable
from .. import utils
from ..contracts.law_contracts import GnosticLaw

# =============================================================================
# == INTERNAL ORGANS: THE SENSORY HELPERS                                    ==
# =============================================================================

def is_ether_plane() -> bool:
    """Perceives if the Engine is breathing in the WASM substrate."""
    return os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

def scry_variable_entropy(val: Any) -> float:
    """Measures the chaotic density of a variable string."""
    import math
    s = str(val)
    if not s: return 0.0
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return - sum([p * math.log(p) / math.log(2.0) for p in prob])

# =============================================================================
# == THE GRAND PANOPTICON OF LAWS                                            ==
# =============================================================================

GENESIS_CODEX: List[GnosticLaw] = [

    # =============================================================================
    # == STRATUM 0: THE LAWS OF THE SUBSTRATE (AMNESTY & TOOLS)                  ==
    # =============================================================================
    
    GnosticLaw(
        key="poetry_without_iron",
        validator=lambda g: (
            g.get('project_type') in ['python', 'poetry'] and 
            g.get('use_poetry') and 
            not utils.is_poetry_installed() and 
            not is_ether_plane() # [THE CURE]
        ),
        title="The Mute Artisan (Poetry)",
        message="The Gaze perceives a will for Poetry, but the `poetry` artisan is not manifest in this reality's PATH.",
        elucidation="The 'Poetry' project type requires a physical binary on Iron. In the Ether (WASM), this is amnestied.",
        context_key="use_poetry",
        severity="WARNING",
        suggestion="Install Poetry globally (`pip install poetry`) or switch to the WASM-native 'pip/venv' strategy."
    ),

    GnosticLaw(
        key="docker_without_iron",
        validator=lambda g: (
            g.get('use_docker') and 
            not shutil.which('docker') and 
            not is_ether_plane() # [THE CURE]
        ),
        title="The Unforged Vessel (Docker)",
        message="The Gaze perceives a will for containerization, but the `docker` artisan is a void in this reality.",
        elucidation="Containerization relies on the Docker daemon. Without it, Dockerfiles cannot be built.",
        context_key="use_docker",
        severity="CRITICAL",
        suggestion="Install Docker Desktop or enable the 'Shadow Strike' remote execution mode."
    ),

    # =============================================================================
    # == STRATUM 1: THE LAWS OF ARCHITECTURAL HARMONY                            ==
    # =============================================================================

    GnosticLaw(
        key="database_for_frontend",
        validator=lambda g: g.get('database_type') != 'none' and g.get('project_type') in ['frontend-vanilla', 'react-vite'],
        title="The Gnostic Schism of Realms",
        message=lambda g: f"A divine artisan of data, '{g.get('database_type')}', has been summoned for a frontend-only reality.",
        elucidation="Frontend-only projects suggest a misunderstanding of architectural boundaries when requesting a DB.",
        context_key="database_type",
        severity="WARNING",
        suggestion="Set the database type to 'none' for a pure frontend project and use an API instead."
    ),

    GnosticLaw(
        key="monolith_with_microservice_auth",
        validator=lambda g: g.get('project_structure_pattern') == 'monolithic' and g.get('auth_method') == 'jwt',
        title="A Soul Divided (Architecture & Auth)",
        message="A 'monolithic' form was chosen with 'JWT' authentication. Session cookies are often superior for monoliths.",
        elucidation="Traditional stateful sessions are often simpler and more secure for unified applications.",
        context_key="auth_method",
        severity="INFO",
        suggestion="Consider using 'session-cookies' for a more harmonious monolithic architecture."
    ),

    GnosticLaw(
        key="circular_dependency_intent",
        validator=lambda g: g.get('project_name') and g.get('frontend_framework') == g.get('backend_framework'),
        title="The Ouroboros Logic",
        message="The blueprint suggests the same framework for both Frontend and Backend.",
        elucidation="Unless using a meta-framework like Next.js, this usually signals a circular dependency in intent.",
        context_key="project_name",
        severity="WARNING",
        suggestion="Verify that your frontend and backend choices are distinct or unified under a meta-framework."
    ),

    # =============================================================================
    # == STRATUM 2: THE LAWS OF THE PROJECT'S SOUL (NAMING & METADATA)           ==
    # =============================================================================

    GnosticLaw(
        key="casing_heresy_in_name",
        validator=lambda g: g.get('project_name') and (g.get('project_name') != utils.to_slug_case(g.get('project_name'))),
        title="A Profane Form (Project Name)",
        message=lambda g: f"Project name '{g.get('project_name')}' contains profane characters or casing.",
        elucidation="Project names should be in 'kebab-case' for universal compatibility with package managers.",
        context_key="project_name",
        severity="WARNING",
        suggestion=lambda g: f"Consider renaming to '{utils.to_slug_case(g.get('project_name', ''))}'."
    ),

    GnosticLaw(
        key="vague_project_name",
        validator=lambda g: g.get('project_name') and g.get('project_name').lower() in ['test', 'app', 'project', 'new-project', 'sentinel'],
        title="The Nameless Soul",
        message=lambda g: f"The name '{g.get('project_name')}' is generic and lacks a unique Gnostic identity.",
        elucidation="A unique name is the first act of bestowing a soul upon a new reality.",
        context_key="project_name",
        severity="INFO",
        suggestion="Choose a more specific name (e.g., 'sentinel-api-v1') to avoid multiversal collisions."
    ),

    GnosticLaw(
        key="missing_progenitor_license",
        validator=lambda g: not g.get('license') or g.get('license') == 'none',
        title="The Unlicensed Reality",
        message="No license scripture has been willed for this project.",
        elucidation="Unlicensed code is a void of ownership. It cannot be legally adopted by the Guild or the public.",
        context_key="license",
        severity="WARNING",
        suggestion="Choose a license (MIT, Apache-2.0, Proprietary) to define the project's sovereignty."
    ),

    # =============================================================================
    # == STRATUM 3: THE LAWS OF SECURITY & PURITY                                ==
    # =============================================================================

    GnosticLaw(
        key="high_entropy_placeholder",
        validator=lambda g: any(scry_variable_entropy(v) > 4.5 for v in g.values() if isinstance(v, str) and len(v) > 16),
        title="High-Entropy Matter Leak",
        message="A variable contains a high-entropy string that resembles a raw secret or key.",
        elucidation="Blueprint variables should never contain raw secrets. These should be warded via '@secret' rites.",
        category="SECURITY",
        severity="CRITICAL",
        suggestion="Replace raw keys with Gnostic placeholders and use 'scaffold with' to inject secrets at runtime."
    ),

    GnosticLaw(
        key="missing_git_ward",
        validator=lambda g: g.get('use_git') and not g.get('add_gitignore'),
        title="The Unguarded Chronicle",
        message="A Git chronicle was willed, but no '.gitignore' ward was manifest.",
        elucidation="Without a .gitignore, profane system matter (node_modules, pycache) will leak into the Akasha.",
        context_key="use_git",
        severity="WARNING",
        suggestion="Enable '.gitignore' materialization to keep the project's history pure."
    ),

    # =============================================================================
    # == STRATUM 4: THE LAWS OF THE MAESTRO (ACTION & WILL)                      ==
    # =============================================================================

    GnosticLaw(
        key="silent_symphony_edict",
        validator=lambda g: g.get('use_ci') and not g.get('test_command'),
        title="A Mute Symphony",
        message="A CI pipeline was willed, but no test edict (command) was proclaimed.",
        elucidation="CI is a rite of adjudication. If there is no command to run, the CI is an empty gesture.",
        context_key="use_ci",
        severity="WARNING",
        suggestion="Proclaim a `test_command` (e.g., 'pytest' or 'npm test') to animate the CI."
    ),

    GnosticLaw(
        key="root_execution_heresy",
        validator=lambda g: g.get('run_as_root') or g.get('use_sudo'),
        title="The Heresy of Absolute Power",
        message="The blueprint contains edicts that demand 'root' or 'sudo' authority.",
        elucidation="Executing as root is a security risk that can lead to host-substrate collapse.",
        category="SECURITY",
        severity="WARNING",
        suggestion="Refactor edicts to run within user-space or use isolated container volumes."
    ),

    # =============================================================================
    # == STRATUM 5: THE LAWS OF THE MULTIVERSE (PERSISTENCE)                     ==
    # =============================================================================

    GnosticLaw(
        key="lockfile_bypass_vow",
        validator=lambda g: g.get('skip_lockfile'),
        title="The Amnesiac Reality",
        message="The Gnostic Chronicle (scaffold.lock) has been willed into the void.",
        elucidation="A project without a lockfile has no memory. It cannot be verified or healed by the Engine.",
        context_key="skip_lockfile",
        severity="WARNING",
        suggestion="Enable the lockfile to ensure your architecture is recoverable across timelines."
    ),

    GnosticLaw(
        key="heavy_matter_monolith",
        validator=lambda g: g.get('file_count_estimate', 0) > 100 and g.get('project_structure_pattern') == 'monolithic',
        title="The Heavy-Matter Monolith",
        message="A high-mass monolithic form is being willed.",
        elucidation="Large monoliths suffer from metabolic friction. Consider a 'Domain-Driven' structure.",
        category="ARCHITECTURE",
        severity="INFO",
        suggestion="Explore the 'Modular' or 'Domain-Driven' archetypes for better cognitive scaling."
    )
]
