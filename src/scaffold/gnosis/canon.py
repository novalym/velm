# Path: scaffold/gnosis/canon.py

"""
=================================================================================
== THE GNOSTIC CANON OF ARCHITECTURAL PRIMITIVES (V-Ω-LEGENDARY++. THE STANDARD LIB) ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000

This is not a file of code. It is the living, eternal soul of the Scaffold God-Engine's
intelligence. It is the sacred, declarative "Standard Library" of the Scaffold
language, a Gnostic Grimoire that teaches every artisan in our cosmos the one true
vocabulary of architectural intent.

This Canon is the divine brain of the `OracleOfTheLivingSoul`, transforming it from
a collection of hardcoded heuristics into a true, data-driven, and infinitely
extensible Gnostic AI. To teach the engine a new "official" variable, to give it a
new sense, an artisan must only inscribe a new `GnosticPrimitive` into this scripture.
=================================================================================
"""
from __future__ import annotations

import datetime
import getpass
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Dict, Any, Callable, List, Optional, TYPE_CHECKING

from .. import utils

# A sacred, Gnostic plea to prevent a paradox of circular Gnosis at runtime.
if TYPE_CHECKING:
    from ..prophecy.oracle import OracleOfTheLivingSoul


# =================================================================================
# == I. THE SACRED CONTRACT: THE SOUL OF A GNOSTIC PRIMITIVE                     ==
# =================================================================================

@dataclass(frozen=True)
class GnosticPrimitive:
    """
    The sacred, immutable vessel for a single law in the Gnostic Canon. It is a
    self-aware entity that teaches the God-Engine its name, its purpose, its nature,
    and the divine rite required to perceive its truth in any given reality.
    """
    key: str
    """The one true, snake_case name of the primitive (e.g., 'use_docker')."""

    gnosis_type: str
    """The soul of the primitive's value ('boolean', 'choice', 'string', 'version', 'multiline')."""

    category: str
    """The Gnostic category for UI grouping (e.g., 'Core Identity', 'Toolchain')."""

    description: str
    """A luminous, human-readable scripture of the primitive's divine purpose."""

    prophecy_rite: Callable[['OracleOfTheLivingSoul'], Any]
    """The divine rite the Oracle uses to prophesy this Gnosis from a manifest reality."""

    default_value: Optional[Any] = None
    """The righteous default if the Prophecy finds only a void. Essential for `--quick`."""

    choices: List[str] = field(default_factory=list)
    """For 'choice' types, the pantheon of valid Gnostic values."""

    validation_rule: Optional[str] = None
    """A Gnostic law from the Jurisprudence codex to validate this primitive's value."""

    is_declarative: bool = True
    """If True, this primitive can be declared by an Architect to command the engine's will."""


# =================================================================================
# == II. THE PANTHEON OF PROPHETIC RITES (THE ORACLE'S SENSES)                   ==
# =================================================================================
# These are the divine, pure artisans that the Canon commands the Oracle to summon.
# Each is a master of a single, Gnostic Gaze.

def _prophesy_project_name(oracle: 'OracleOfTheLivingSoul') -> Optional[str]:
    """Perceives the project's name from its manifest, its Git soul, or its sanctum."""
    # The Gaze of Gnostic Precedence is honored.
    if manifest_name := oracle.dossier.get("manifest_name"):
        return manifest_name
    if git_repo := oracle.dossier.get("git_repo"):
        return git_repo
    return oracle.project_root.name.lower().replace(" ", "-")


def _prophesy_author_from_git(oracle: 'OracleOfTheLivingSoul') -> Optional[str]:
    """Performs a deep Gaze into the project's Git soul for the Architect's name."""
    if not (oracle.project_root / ".git").is_dir(): return None
    try:
        return subprocess.check_output(
            ['git', 'config', 'user.name'],
            text=True, stderr=subprocess.DEVNULL, cwd=oracle.project_root
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _prophesy_author_from_os(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the Architect's mortal name from the OS as a fallback."""
    return getpass.getuser()


def _prophesy_description_from_readme(oracle: 'OracleOfTheLivingSoul') -> Optional[str]:
    """Faculty 8: The Gaze of the Luminous Scribe."""
    readme_path = oracle.project_root / "README.md"
    if readme_path.is_file():
        try:
            content = readme_path.read_text(encoding='utf-8', errors='ignore')
            # A divine regex that finds the first meaningful paragraph after any title.
            match = re.search(r'^(?:#.*?\n+)+([A-Za-z].*)', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        except Exception:
            return None
    return None


def _prophesy_version_from_manifest(oracle: 'OracleOfTheLivingSoul') -> Optional[str]:
    """Faculty 1 Ascended: The Polyglot Scribe's Gaze for version."""
    # This rite depends on the Gaze for manifests, which will be forged in the Oracle.
    # It demonstrates the power of a stateful, multi-stage Gaze.
    return oracle.dossier.get("manifest_version")


def _prophesy_from_living_souls(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the primary technological soul(s) of the project."""
    # This is a pure delegation to the _gaze_upon_living_souls rite.
    if oracle.perceived_souls:
        # A Gaze of Gnostic Causality: Prioritize frameworks over base languages
        ranked_souls = sorted(list(oracle.perceived_souls), key=lambda s: next((item['rank'] for item in oracle.SOUL_CODEX if item['name'] == s), 0), reverse=True)
        return ", ".join(ranked_souls)
    return "generic"

def _prophesy_from_vcs_soul(oracle: 'OracleOfTheLivingSoul') -> bool:
    """Perceives the soul of version control."""
    return (oracle.project_root / ".git").is_dir()

def _prophesy_from_container_soul(oracle: 'OracleOfTheLivingSoul') -> bool:
    """Perceives the soul of containerization."""
    return (oracle.project_root / "Dockerfile").is_file() or \
           (oracle.project_root / "docker-compose.yml").is_file()

def _prophesy_from_maestros_will(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the project's chosen Maestro for conducting rites."""
    if (oracle.project_root / "Makefile").is_file(): return "make"
    # A deeper Gaze into package.json
    pkg_path = oracle.project_root / "package.json"
    if pkg_path.is_file():
        try:
            content = pkg_path.read_text(encoding='utf-8')
            if (oracle.project_root / "pnpm-lock.yaml").is_file(): return "pnpm"
            if (oracle.project_root / "yarn.lock").is_file(): return "yarn"
            if "scripts" in json.loads(content): return "npm"
        except Exception: pass
    return "none"

def _prophesy_testing_framework(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the chosen Inquisitor for adjudicating the project's purity."""
    # A Gaze of Gnostic Causality
    if "Poetry (Python)" in oracle.perceived_souls or "Python" in oracle.perceived_souls:
        if "pytest" in (oracle.project_root / "pyproject.toml").read_text(): return "pytest"
        if any((oracle.project_root / "tests").glob("test_*.py")): return "pytest" # A reasonable prophecy
    if "Node.js" in oracle.perceived_souls:
        pkg_content = (oracle.project_root / "package.json").read_text()
        if "jest" in pkg_content: return "jest"
        if "vitest" in pkg_content: return "vitest"
        if "mocha" in pkg_content: return "mocha"
    return "none"


def _prophesy_architectural_pattern(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the grand architectural philosophy of the project."""
    src = oracle.project_root / "src"
    if not src.is_dir(): return "monolithic"  # Default for simple structures

    # A Gaze for the signature sanctums of different patterns
    if (src / "domains").is_dir() or (src / "modules").is_dir():
        return "modular-monolith"
    if (src / "services").is_dir() and len(list((src / "services").iterdir())) > 2:
        return "microservice-style"
    if (src / "functions").is_dir() or (src / "handlers").is_dir() and not (src / "controllers").is_dir():
        return "serverless"
    if (src / "controllers").is_dir() and (src / "models").is_dir():
        return "mvc"  # A more specific form of monolithic

    return "monolithic"


def _prophesy_auth_method(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the sacred key that guards the gates of the reality."""
    # This Gaze is complex and requires deep content analysis, a future ascension.
    # For now, we prophesy based on common framework defaults.
    if "FastAPI" in oracle.perceived_souls or "Express" in oracle.perceived_souls:
        return "jwt"
    if "Django" in oracle.perceived_souls:
        return "session-cookies"
    return "none"


def _prophesy_license(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the project's sacred vow to the cosmos."""
    license_path = next((p for p in oracle.project_root.glob('LICENSE*')), None)
    if license_path and license_path.is_file():
        content = license_path.read_text(encoding='utf-8').lower()
        if "mit license" in content: return "MIT"
        if "apache license" in content: return "Apache-2.0"
        if "gnu general public license" in content: return "GPL-3.0"
        return "Custom"
    return "None"


def _prophesy_ci_provider(oracle: 'OracleOfTheLivingSoul') -> str:
    """Perceives the celestial realm chosen for CI/CD symphonies."""
    if (oracle.project_root / ".github/workflows").is_dir(): return "github"
    if (oracle.project_root / ".gitlab-ci.yml").is_file(): return "gitlab"
    if (oracle.project_root / "Jenkinsfile").is_file(): return "jenkins"
    return "none"



def _prophesy_runtime_python_version(oracle: 'OracleOfTheLivingSoul') -> str:
    """
    [THE ORACLE OF THE RUNTIME]
    Perceives the python version of the current reality.
    Returns MAJOR.MINOR (e.g., "3.11").
    """
    v = sys.version_info
    return f"{v.major}.{v.minor}"



# =================================================================================
# == III. THE GNOSTIC CANON (THE STANDARD LIBRARY OF ARCHITECTURE)               ==
# =================================================================================

ARCHITECTURAL_CANON: List[GnosticPrimitive] = [

    # --- MOVEMENT I: THE PRIMITIVES OF CORE IDENTITY ---
    # These primitives define the absolute, fundamental soul of a project.

    GnosticPrimitive(
        key="project_name",
        gnosis_type="string",
        category="Core Identity",
        description="The sacred, unique, kebab-case name of the new reality.",
        prophecy_rite=_prophesy_project_name,
        validation_rule="slug"
    ),
    GnosticPrimitive(
        key="author",
        gnosis_type="string",
        category="Core Identity",
        description="The name of the Architect or Guild forging this Great Work.",
        prophecy_rite=lambda o: _prophesy_author_from_git(o) or _prophesy_author_from_os(o)
    ),
    GnosticPrimitive(
        key="description",
        gnosis_type="multiline",
        category="Core Identity",
        description="The luminous, one-sentence Gnostic essence of the project's purpose.",
        prophecy_rite=_prophesy_description_from_readme,
        default_value="A new reality forged by the Scaffold God-Engine."
    ),
    GnosticPrimitive(
        key="version",
        gnosis_type="version",
        category="Core Identity",
        description="The project's version, following the sacred laws of SemVer.",
        prophecy_rite=_prophesy_version_from_manifest,
        default_value="0.1.0",
        validation_rule="version"  # A future law in our jurisprudence
    ),
    GnosticPrimitive(
        key="python_version",
        gnosis_type="version",
        category="Toolchain",
        description="The target Python version for the project.",
        prophecy_rite=_prophesy_runtime_python_version,
        default_value="3.11",
        validation_rule="min_length(3)" # Simple validation for now
    ),

    # ... The symphony will continue in the next proclamation ...
]

# =================================================================================
# == III. THE GNOSTIC CANON (CONTINUED)                                          ==
# =================================================================================

ARCHITECTURAL_CANON.extend([

    # --- MOVEMENT II: THE PRIMITIVES OF THE GNOSTIC TOOLCHAIN ---
    # These primitives define the core technologies and their sacred artisans.

    GnosticPrimitive(
        key="project_type",
        gnosis_type="string",
        category="Toolchain",
        description="The primary technological soul(s) of the project (e.g., 'React', 'FastAPI', 'Python').",
        prophecy_rite=_prophesy_from_living_souls,
        is_declarative=False  # This is perceived, not declared by the user.
    ),
    GnosticPrimitive(
        key="use_poetry",
        gnosis_type="boolean",
        category="Toolchain",
        description="Whether to use Poetry for Python dependency management.",
        prophecy_rite=lambda o: "Poetry (Python)" in o.perceived_souls,
        default_value=True
    ),
    GnosticPrimitive(
        key="database_type",
        gnosis_type="choice",
        category="Toolchain",
        description="The divine artisan that shall guard the project's data.",
        prophecy_rite=lambda o: "PostgreSQL" if "PostgreSQL" in o.perceived_souls else "none",
        default_value="none",
        choices=['none', 'postgres', 'mysql', 'sqlite', 'mongodb', 'redis', 'dynamodb']
    ),
    GnosticPrimitive(
        key="frontend_framework",
        gnosis_type="choice",
        category="Toolchain",
        description="The artistic school that shall shape the user's reality.",
        prophecy_rite=lambda o: next(
            (s for s in ["react", "vue", "svelte", "nextjs"] if s.capitalize() in o.perceived_souls), "none"),
        default_value="none",
        choices=['none', 'react', 'vue', 'svelte', 'nextjs', 'vanilla-js']
    ),
    GnosticPrimitive(
        key="testing_framework",
        gnosis_type="choice",
        category="Toolchain",
        description="The Inquisitor that shall adjudicate the project's purity.",
        prophecy_rite=_prophesy_testing_framework,
        default_value="pytest",  # A reasonable default for many projects
        choices=['pytest', 'unittest', 'jest', 'vitest', 'mocha', 'go test', 'cargo test', 'junit', 'none']
    ),

    # ... The symphony will continue in the next proclamation ...
])

# =================================================================================
# == III. THE GNOSTIC CANON (CONTINUED)                                          ==
# =================================================================================

ARCHITECTURAL_CANON.extend([

    # --- MOVEMENT III: THE PRIMITIVES OF ARCHITECTURAL PHILOSOPHY ---
    # These primitives define the high-level patterns of structure and security.

    GnosticPrimitive(
        key="project_structure_pattern",
        gnosis_type="choice",
        category="Architecture",
        description="The grand architectural philosophy the project follows.",
        prophecy_rite=_prophesy_architectural_pattern,
        default_value="modular-monolith",
        choices=['monolithic', 'modular-monolith', 'microservice-style', 'mvc', 'serverless']
    ),
    GnosticPrimitive(
        key="auth_method",
        gnosis_type="choice",
        category="Architecture",
        description="The sacred key that shall guard the gates of this reality.",
        prophecy_rite=_prophesy_auth_method,
        default_value="none",
        choices=['none', 'jwt', 'oauth2', 'session-cookies', 'api-key']
    ),
    GnosticPrimitive(
        key="env_vars_setup",
        gnosis_type="boolean",
        category="Architecture",
        description="Whether the project uses a `.env` file for configuration.",
        prophecy_rite=lambda o: (o.project_root / ".env.example").is_file() or (o.project_root / ".env").is_file(),
        default_value=True
    ),
    GnosticPrimitive(
        key="default_port",
        gnosis_type="string",  # String to allow for env var placeholders
        category="Architecture",
        description="The port on which this reality listens to the cosmos.",
        prophecy_rite=lambda o: "3000" if "Node.js" in o.perceived_souls else "8000",
        default_value="8000",
        validation_rule="port_or_env_var"  # A future law
    ),

    # ... The symphony will conclude in the final proclamation ...
])

# =================================================================================
# == III. THE GNOSTIC CANON (CONCLUDED)                                          ==
# =================================================================================

ARCHITECTURAL_CANON.extend([

    # --- MOVEMENT IV: THE PRIMITIVES OF THE DEVOPS & MENTORSHIP REALM ---
    # These primitives define the project's lifecycle and its communion with the Architect.

    GnosticPrimitive(
        key="license",
        gnosis_type="choice",
        category="DevOps",
        description="The project's sacred vow to the cosmos.",
        prophecy_rite=_prophesy_license,
        default_value="MIT",
        choices=["MIT", "Apache-2.0", "GPL-3.0", "Custom", "None"]
    ),
    GnosticPrimitive(
        key="use_git",
        gnosis_type="boolean",
        category="DevOps",
        description="Whether the project is a consecrated Git sanctum.",
        prophecy_rite=_prophesy_from_vcs_soul,
        default_value=True
    ),
    GnosticPrimitive(
        key="use_ci",
        gnosis_type="choice",
        category="DevOps",
        description="The celestial realm chosen for CI/CD symphonies.",
        prophecy_rite=_prophesy_ci_provider,
        default_value="github",
        choices=["none", "github", "gitlab", "jenkins", "circleci"]
    ),
    GnosticPrimitive(
        key="use_docker",
        gnosis_type="boolean",
        category="DevOps",
        description="Whether the project is a containerized reality.",
        prophecy_rite=_prophesy_from_container_soul,
        default_value=True
    ),
    GnosticPrimitive(
        key="use_vscode",
        gnosis_type="boolean",
        category="Mentorship",
        description="Whether to forge scriptures for a luminous experience in VS Code.",
        prophecy_rite=lambda o: (o.project_root / ".vscode").is_dir(),
        default_value=True
    ),
    GnosticPrimitive(
        key="project_goals",
        gnosis_type="multiline",
        category="Mentorship",
        description="The ultimate destiny of this project, for the AI Co-Architect's Gaze.",
        prophecy_rite=lambda o: None,  # This must be proclaimed by the Architect.
        default_value=""
    ),
    GnosticPrimitive(
        key="ai_code_generation_consent",
        gnosis_type="boolean",
        category="Mentorship",
        description="Whether to grant the AI Co-Architect the authority to synthesize code.",
        prophecy_rite=lambda o: False,  # Consent must be explicit.
        default_value=False
    )
])

# =================================================================================
# == IV. THE DIVINE GRIMOIRE OF ALCHEMICAL DERIVATION (V-Ω-LEGENDARY++)          ==
# =================================================================================
# This sacred codex teaches the God-Engine how to forge new Gnosis from old. It is
# the declarative brain of the Prescient Alchemist, a symphony of causality that
# transforms simple truths into a rich, interconnected tapestry of Gnostic reality.
# =================================================================================

DERIVED_GNOSIS_CODEX: List[Dict[str, Any]] = [

    # --- MOVEMENT I: THE ALCHEMY OF NAMING (THE CORE SOUL) ---
    # These rites forge the fundamental naming conventions from the project's one true name.

    {
        "target": "project_slug",
        "source": "project_name",
        "rite": lambda src: utils.generate_derived_names(str(src)).get('name_slug')
    },
    {
        "target": "project_pascal",
        "source": "project_name",
        "rite": lambda src: utils.generate_derived_names(str(src)).get('name_pascal')
    },
    {
        "target": "project_title",
        "source": "project_name",
        "rite": lambda src: utils.generate_derived_names(str(src)).get('name_title')
    },
    {
        "target": "project_snake",
        "source": "project_name",
        "rite": lambda src: utils.generate_derived_names(str(src)).get('name_snake')
    },
    {
        "target": "project_const",
        "source": "project_name",
        "rite": lambda src: utils.generate_derived_names(str(src)).get('name_const')
    },

    # --- MOVEMENT II: THE ALCHEMY OF THE COSMOS (VCS & DEVOPS) ---
    # These rites forge the Gnosis of the project's place in the wider cosmos.

    {
        "target": "git_repo_url",
        "source": ["git_org", "git_repo"],
        "rite": lambda org, repo: f"https://github.com/{org}/{repo}.git" if org and repo else None
    },
    {
        "target": "docker_image_name",
        "source": ["git_org", "project_slug"],
        # The Gnostic Fallback: If git_org is a void, it gracefully uses 'my-org'.
        "rite": lambda org, slug: f"{str(org).lower() if org else 'my-org'}/{slug}"
    },

    # --- MOVEMENT III: THE ALCHEMY OF PROVENANCE (METADATA) ---
    # These rites forge the Gnosis of the project's own history and covenant.

    {
        "target": "license_year",
        "source": [],  # This rite requires no source; it is a pure temporal Gaze.
        "rite": lambda: str(datetime.date.today().year)
    },
    {
        "target": "author_email",
        "source": "author",
        # A humble prophecy: it forges an email from the author's name.
        "rite": lambda author: f"{str(author).lower().replace(' ', '.')}@example.com" if author else None
    },

    # --- MOVEMENT IV: THE ALCHEMY OF THE REALM (CONFIGURATION) ---
    # These rites forge Gnosis for specific technological souls.

    {
        "target": "python_package_name",
        "source": "project_slug",
        # The Pythonic Transmutation: Replaces hyphens with underscores.
        "rite": lambda slug: str(slug).replace('-', '_')
    },
    {
        "target": "db_name",
        "source": "project_slug",
        "rite": lambda slug: f"{str(slug).replace('-', '_')}_db"
    },
    {
        "target": "db_test_name",
        "source": "project_slug",
        "rite": lambda slug: f"{str(slug).replace('-', '_')}_test_db"
    },

    # --- MOVEMENT V: THE PROPHECY OF FUTURE ASCENSIONS ---
    # This is a sacred vessel, a placeholder for the infinite Gnosis we can teach.
    # A future artisan could add:
    # {
    #     "target": "helm_chart_name",
    #     "source": "project_slug",
    #     "rite": lambda slug: f"{slug}-chart"
    # },
    # {
    #     "target": "npm_package_scope",
    #     "source": "git_org",
    #     "rite": lambda org: f"@{str(org).lower()}" if org else None
    # }
]