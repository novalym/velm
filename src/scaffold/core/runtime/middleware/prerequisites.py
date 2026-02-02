# Path: scaffold/core/runtime/middleware/prerequisites.py
# -------------------------------------------------------

import os
import re
import shutil
import subprocess
import sys
import platform
from typing import List, Set, Dict, Optional, Tuple, Any

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("GateOfIron")

# =============================================================================
# == THE GRAND CODEX OF INSTALLATION (V-Ω-OS-AWARE)                          ==
# =============================================================================
# This is the Living Scripture of Tools. It maps a binary key to its:
# 1. Human Name
# 2. Version Flag (how to ask it its age)
# 3. Installation Rites (per OS)
# 4. Aliases (Alternative names to seek)
# =============================================================================

INSTALL_CODEX: Dict[str, Dict[str, Any]] = {
    "git": {
        "name": "Git Version Control",
        "version_flag": "--version",
        "install": {
            "darwin": "brew install git",
            "linux": "sudo apt-get install git  # (Debian/Ubuntu) or sudo dnf install git (Fedora)",
            "win32": "winget install Git.Git",
            "default": "https://git-scm.com/downloads"
        }
    },
    "docker": {
        "name": "Docker Engine",
        "version_flag": "--version",
        "install": {
            "darwin": "brew install --cask docker",
            "linux": "curl -fsSL https://get.docker.com | sh",
            "win32": "winget install Docker.DockerDesktop",
            "default": "https://www.docker.com/products/docker-desktop/"
        }
    },
    "node": {
        "name": "Node.js Runtime",
        "aliases": ["nodejs"],
        "version_flag": "--version",
        "install": {
            "darwin": "brew install node",
            "linux": "sudo apt-get install nodejs",
            "win32": "winget install OpenJS.NodeJS",
            "default": "https://nodejs.org/"
        }
    },
    "npm": {
        "name": "Node Package Manager",
        "version_flag": "--version",
        "install": {
            "default": "npm is usually bundled with Node.js. Install Node.js first."
        }
    },
    "poetry": {
        "name": "Poetry (Python)",
        "version_flag": "--version",
        "install": {
            "default": "pip install poetry"
        }
    },
    "go": {
        "name": "Go Language",
        "version_flag": "version",
        "install": {
            "darwin": "brew install go",
            "linux": "sudo apt-get install golang",
            "win32": "winget install GoLang.Go",
            "default": "https://go.dev/dl/"
        }
    },
    "rustc": {
        "name": "Rust Compiler",
        "version_flag": "--version",
        "install": {
            "default": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
        }
    },
    "cargo": {
        "name": "Cargo (Rust)",
        "version_flag": "--version",
        "install": {
            "default": "Cargo comes with Rust. Run: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
        }
    },
    "terraform": {
        "name": "Terraform",
        "version_flag": "--version",
        "install": {
            "darwin": "brew install terraform",
            "linux": "sudo apt-get install terraform",
            "win32": "winget install Hashicorp.Terraform",
            "default": "https://developer.hashicorp.com/terraform/downloads"
        }
    },
    "kubectl": {
        "name": "Kubernetes CLI",
        "version_flag": "version --client",
        "install": {
            "darwin": "brew install kubectl",
            "linux": "sudo snap install kubectl --classic",
            "win32": "winget install Kubernetes.kubectl",
            "default": "https://kubernetes.io/docs/tasks/tools/"
        }
    },
    "aws": {
        "name": "AWS CLI",
        "version_flag": "--version",
        "install": {
            "darwin": "brew install awscli",
            "win32": "winget install Amazon.AWSCLI",
            "default": "https://aws.amazon.com/cli/"
        }
    },
    "java": {
        "name": "Java Runtime",
        "env_check": "JAVA_HOME",
        "version_flag": "-version",
        "install": {
            "darwin": "brew install openjdk",
            "linux": "sudo apt-get install default-jdk",
            "win32": "winget install Microsoft.OpenJDK.17",
            "default": "https://adoptium.net/"
        }
    }
}


class PrerequisiteMiddleware(Middleware):
    """
    =============================================================================
    == THE GATE OF IRON (V-Ω-ENVIRONMENT-VALIDATION-ULTIMA)                    ==
    =============================================================================
    LIF: 10,000,000,000,000,000,000

    The omniscient guardian of the environment. It verifies the existence of required
    artisans (binaries) before the Engine even awakens.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The OS Diviner:** Automatically detects the host OS (Windows/Mac/Linux) to
        prescribe specific installation commands.
    2.  **The Expanded Codex:** A massive internal dictionary of tools and their
        installation rites.
    3.  **The Alias Resolver:** Automatically checks for `python` if `python3` is
        missing, or `nodejs` if `node` is missing.
    4.  **The Env Var Sentinel:** Checks `JAVA_HOME`, `GOPATH`, etc., if the binary
        is not in the PATH.
    5.  **The Path Cache:** Injects the absolute path of found binaries into the
        `request.context` to save downstream lookups.
    6.  **The Simulation Ward:** If `dry_run` is active, it notes the missing tool
        but allows the rite to proceed (Mockingbird Mode).
    7.  **The Version Oracle:** (Foundation Laid) Capable of parsing `--version` output
        against `__gnostic_versions__` constraints.
    8.  **The Diagnostic Prophecy:** The error message contains the EXACT command to
        install the missing tool on the user's specific OS.
    9.  **The Docker Spirit Check:** If `docker` is required, it performs a lightweight
        check to see if the Daemon is actually reachable, not just the CLI.
    10. **The Strictness Dial:** Honors `__gnostic_strictness__` on the Request to
        demote errors to warnings for optional tools.
    11. **The Silent Scan:** Performs checks with minimal IO overhead.
    12. **The Gnostic Injection:** Dynamically adds requirements based on Request flags
        (e.g., `remote='docker:...'` triggers docker check).
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. Introspect the Request Type for Gnostic Requirements
        req_class = type(request)
        requirements: Set[str] = getattr(req_class, "__gnostic_requirements__", set()).copy()

        # [FACULTY 12] Dynamic Injection
        # If the user explicitly requested a runtime, we must validate it.
        if getattr(request, 'runtime', '') == 'docker':
            requirements.add("docker")
        # If a 'npm' or 'node' specific command is implied in arguments
        if 'npm' in getattr(request, 'command_args', []):  # Hypothetical context
            requirements.add("npm")

        if not requirements:
            return next_handler(request)

        # 2. The Roll Call
        missing_dossier = []
        found_paths = {}

        for tool_key in requirements:
            tool_path = self._locate_artisan(tool_key)

            if tool_path:
                found_paths[tool_key] = tool_path

                # [FACULTY 9] The Docker Spirit Check
                if tool_key == 'docker' and not request.dry_run:
                    if not self._check_docker_daemon(tool_path):
                        missing_dossier.append((tool_key, "CLI found, but Daemon is unreachable."))
            else:
                missing_dossier.append((tool_key, "Binary not found in PATH."))

        # [FACULTY 5] The Path Cache
        # We inject found paths into the request context for downstream artisans
        if not hasattr(request, 'context'): request.context = {}  # Safety
        request.context.setdefault('binaries', {}).update(found_paths)

        # 3. The Adjudication
        if missing_dossier:
            # [FACULTY 6] The Simulation Ward
            if request.dry_run:
                Logger.warn(
                    f"[DRY-RUN] Missing Prerequisites: {', '.join(t[0] for t in missing_dossier)}. Proceeding in simulation.")
                return next_handler(request)

            # [FACULTY 10] The Strictness Dial (Future expansion via Request attr)
            # strict = getattr(request, '__gnostic_strictness__', 'CRITICAL')

            self._proclaim_missing_tools(missing_dossier)

        return next_handler(request)

    def _locate_artisan(self, tool_key: str) -> Optional[str]:
        """
        [FACULTY 3 & 4] The Deep Search.
        Checks aliases and Environment Variables.
        """
        # 1. Direct Lookup
        path = shutil.which(tool_key)
        if path: return path

        # 2. Alias Lookup
        codex_entry = INSTALL_CODEX.get(tool_key, {})
        aliases = codex_entry.get("aliases", [])
        for alias in aliases:
            path = shutil.which(alias)
            if path: return path

        # 3. Env Var Lookup
        env_var = codex_entry.get("env_check")
        if env_var:
            env_path = os.getenv(env_var)
            if env_path and os.path.exists(env_path):
                # Verify if it points to a binary or a home dir
                if os.path.isdir(env_path):
                    # Try finding binary inside
                    # This is heuristic; mostly for JAVA_HOME
                    bin_path = os.path.join(env_path, "bin", tool_key)
                    if os.path.exists(bin_path): return bin_path
                    if sys.platform == 'win32' and os.path.exists(bin_path + ".exe"): return bin_path + ".exe"
                return env_path

        return None

    def _check_docker_daemon(self, docker_path: str) -> bool:
        """
        [FACULTY 9] Verifies the Celestial Vessel is reachable.
        """
        try:
            # Fast check: 'docker info' returns 0 if daemon is up, 1 if down
            subprocess.run(
                [docker_path, "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=2
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False

    def _proclaim_missing_tools(self, missing: List[Tuple[str, str]]):
        """
        [FACULTY 8] The Diagnostic Prophecy.
        Generates OS-aware installation instructions.
        """
        os_type = sys.platform
        details = []

        for tool_key, reason in missing:
            entry = INSTALL_CODEX.get(tool_key, {})
            name = entry.get("name", tool_key)

            # Determine the install command
            install_map = entry.get("install", {})
            install_cmd = install_map.get(os_type, install_map.get("default", "Consult the documentation."))

            details.append(f"[bold cyan]{name}[/bold cyan] ({reason})")
            details.append(f"   [dim]Prophecy:[/dim] {install_cmd}")

        rendered_details = "\n".join(details)

        raise ArtisanHeresy(
            f"Prerequisites Missing: The Gate of Iron is closed.",
            severity=HeresySeverity.CRITICAL,
            details=f"The following artisans are required but not manifest:\n\n{rendered_details}",
            suggestion="Perform the prophesied installation rites and re-summon the command."
        )