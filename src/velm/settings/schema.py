# Path: scaffold/settings/schema.py

"""
=================================================================================
== THE CODEX OF CONFIGURATION (V-Ω-ULTRA-DEFINITIVE)                           ==
=================================================================================
LIF: 10,000,000,000

This scripture defines the shape of the Architect's Will. It is the immutable
schema for the `config.json` souls found in the Global (`~/.scaffold/`) and
Local (`./.scaffold/`) sanctums.

It covers:
1.  **Core Identity:** Who is the Architect?
2.  **Runtime Governance:** How should code execute? (System vs Hermetic vs Docker)
3.  **Celestial Vessels:** Specific Docker images and resource limits.
4.  **Hermetic Versions:** Pinned versions for managed runtimes.
5.  **The Gnostic Inquisitor:** Rules for linting and analysis.
6.  **The AI Co-Architect:** Parameters for the Gambit Engine (Future).
7.  **Network & Telemetry:** Timeouts and connection logic.
"""
from dataclasses import dataclass
from typing import List, Any, Optional, Dict


@dataclass
class SettingDef:
    key: str
    default: Any
    description: str
    category: str
    options: Optional[List[Any]] = None  # For choice-based settings
    value_type: str = "str"  # 'str', 'int', 'bool', 'float', 'list' for TUI parsing helper
    secret: bool = False  # If True, the TUI should mask this value


# =================================================================================
# == THE GREAT TABLE OF SETTINGS                                                 ==
# =================================================================================
DEFAULT_SETTINGS_SCHEMA = [

    # -----------------------------------------------------------------------------
    # I. CORE IDENTITY (The Soul of the Architect)
    # -----------------------------------------------------------------------------
    SettingDef(
        "core.editor",
        "code",
        "The command to summon your text editor (e.g., 'code -r', 'vim', 'nano').",
        "Core"
    ),
    SettingDef(
        "core.author",
        "The Architect",
        "Default author name used in file headers and metadata.",
        "Core"
    ),
    SettingDef(
        "core.license",
        "MIT",
        "Default license for new projects.",
        "Core",
        options=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "None"]
    ),
    SettingDef(
        "core.shell",
        "bash",
        "Preferred shell for '>>' commands (bash, zsh, powershell, cmd).",
        "Core",
        options=["bash", "zsh", "powershell", "cmd", "fish"]
    ),

    # -----------------------------------------------------------------------------
    # II. RUNTIME GOVERNANCE (The Rules of Execution)
    # -----------------------------------------------------------------------------
    SettingDef(
        "runtimes.strategy",
        "auto",
        "Execution Strategy for Polyglot Rites:\n"
        " • 'auto': Try Hermetic/Docker if configured, fallback to System.\n"
        " • 'system': Use host PATH only (Lightweight).\n"
        " • 'hermetic': Use ~/.scaffold/runtimes only (Reproducible).\n"
        " • 'docker': Run everything in containers (Ultimate Isolation).",
        "Runtimes",
        options=["auto", "system", "hermetic", "docker"]
    ),
    SettingDef(
        "runtimes.isolation_level",
        "process",
        "Default isolation for local rites. 'process' is standard, 'chroot' is future.",
        "Runtimes",
        options=["process", "chroot"]
    ),
    SettingDef(
        "runtimes.prefer_venv",
        True,
        "If True, Polyglot Artisan will prioritize a .venv in the project root.",
        "Runtimes",
        value_type="bool"
    ),

    # -----------------------------------------------------------------------------
    # III. CELESTIAL VESSELS (Docker Configuration)
    # -----------------------------------------------------------------------------
    # Images
    SettingDef("docker.image.python", "python:3.11-slim", "Default vessel for Python rites.", "Docker"),
    SettingDef("docker.image.node", "node:20-alpine", "Default vessel for Node.js/TS rites.", "Docker"),
    SettingDef("docker.image.go", "golang:1.22-alpine", "Default vessel for Go rites.", "Docker"),
    SettingDef("docker.image.rust", "rust:1.75-alpine", "Default vessel for Rust rites.", "Docker"),
    SettingDef("docker.image.ruby", "ruby:3.2-alpine", "Default vessel for Ruby rites.", "Docker"),

    # Policies
    SettingDef(
        "docker.pull_policy",
        "missing",
        "When to summon images from the Registry.",
        "Docker",
        options=["missing", "always", "never"]
    ),
    SettingDef(
        "docker.network_mode",
        "bridge",
        "Default network mode for ephemeral vessels (bridge, host, none).",
        "Docker",
        options=["bridge", "host", "none"]
    ),

    # Resource Limits (The Ward of Finitude)
    SettingDef("docker.limit.memory", "512m", "Default memory limit for ephemeral vessels.", "Docker"),
    SettingDef("docker.limit.cpus", "1.0", "Default CPU quota for ephemeral vessels.", "Docker"),
    SettingDef("docker.mount_mode", "cached", "Volume mount consistency (consistent, cached, delegated).", "Docker"),

    # -----------------------------------------------------------------------------
    # IV. THE HERMETIC FORGE (Managed Runtime Versions)
    # -----------------------------------------------------------------------------
    SettingDef("hermetic.python.version", "3.11", "Target version for Managed Python.", "Hermetic"),
    SettingDef("hermetic.node.version", "20", "Target version for Managed Node.js.", "Hermetic"),
    SettingDef("hermetic.go.version", "1.22", "Target version for Managed Go.", "Hermetic"),
    # (The RuntimeManager uses these defaults if specific versions aren't requested)

    # -----------------------------------------------------------------------------
    # V. THE GNOSTIC INQUISITOR (Analysis & Linting)
    # -----------------------------------------------------------------------------
    SettingDef(
        "analysis.level",
        "standard",
        "Strictness of the Gnostic Gaze.",
        "Analysis",
        options=["lenient", "standard", "strict", "paranoid"]
    ),
    SettingDef(
        "analysis.check_secrets",
        True,
        "Scan for hardcoded secrets/keys in blueprints and code.",
        "Analysis",
        value_type="bool"
    ),
    SettingDef(
        "analysis.check_complexity",
        True,
        "Analyze cyclomatic complexity of generated code.",
        "Analysis",
        value_type="bool"
    ),
    SettingDef(
        "analysis.max_lines",
        300,
        "Threshold for 'Monolithic File' warning.",
        "Analysis",
        value_type="int"
    ),
    SettingDef(
        "analysis.forbidden_patterns",
        [],
        "List of regex patterns that invoke a Heresy if found.",
        "Analysis",
        value_type="list"
    ),

    # -----------------------------------------------------------------------------
    # VI. THE AI CO-ARCHITECT (Gambit Integration - Future)
    # -----------------------------------------------------------------------------
    SettingDef("ai.model", "gpt-4-turbo", "The mind of the Co-Architect.", "AI"),
    SettingDef("ai.temperature", 0.7, "Creativity level (0.0 - 1.0).", "AI", value_type="float"),
    SettingDef("ai.max_tokens", 4096, "Context window limit.", "AI", value_type="int"),
    SettingDef("ai.api_base", "https://api.openai.com/v1", "Base URL for the AI Oracle.", "AI"),
    SettingDef("ai.api_key", "", "Secret key for the AI Oracle.", "AI", secret=True),

    # -----------------------------------------------------------------------------
    # VII. THE CELESTIAL FORGE (Templates)
    # -----------------------------------------------------------------------------
    SettingDef(
        "forge.auto_update",
        True,
        "Check for updates to Celestial Archetypes automatically.",
        "Forge",
        value_type="bool"
    ),
    SettingDef("forge.gist_token", "", "GitHub Token for private Gists.", "Forge", secret=True),
    SettingDef("forge.index_url", "https://github.com/scaffold/index", "URL of the Community Template Index.", "Forge"),

    # -----------------------------------------------------------------------------
    # VIII. NETWORK & TELEMETRY
    # -----------------------------------------------------------------------------
    SettingDef("network.timeout", 30, "Default timeout (seconds) for network rites.", "Network", value_type="int"),
    SettingDef("network.proxy", "", "HTTP/HTTPS Proxy URL.", "Network"),
    SettingDef("network.verify_ssl", True, "Verify SSL certificates.", "Network", value_type="bool"),

    SettingDef("telemetry.enabled", False, "Allow Scaffold to learn from anonymous usage data (Future).", "Telemetry",
               value_type="bool"),
    # --- NEW SECTION: IX. THE LUMINOUS REALM (UI & UX) ---
    SettingDef(
        "ui.theme",
        "default",
        "Visual theme for the Gnostic Studio and Pads.",
        "UI",
        options=["default", "cyberpunk", "monokai"]
    ),
    SettingDef(
        "ui.audible_cues",
        False,
        "Enable subtle sound effects for key events.",
        "UI",
        value_type="bool"
    ),

]


def get_default_config() -> Dict[str, Any]:
    """Forges the primal state of configuration."""
    return {s.key: s.default for s in DEFAULT_SETTINGS_SCHEMA}


def get_schema_map() -> Dict[str, SettingDef]:
    """Returns a map for O(1) schema lookups by key."""
    return {s.key: s for s in DEFAULT_SETTINGS_SCHEMA}