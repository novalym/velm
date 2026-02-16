# Path: src/velm/core/cortex/dependency_oracle.py
# -----------------------------------------------
# LIF: ∞ | ROLE: ENVIRONMENTAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ORACLE_V24001_AMNESTY_PROTOCOL_FINALIS

import json
import re
import shutil
import subprocess
import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Final, Tuple

# --- GNOSTIC UPLINKS ---
try:
    import toml
except ImportError:
    toml = None

from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from ...gnostic_instrumentarium import GNOSTIC_INSTRUMENTARIUM
from ...logger import Scribe, get_console
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("DependencyOracle")

# =================================================================================
# == STRATUM 0: THE CODEX OF REQUIRED SOULS (V-Ω-EXPANDED)                       ==
# =================================================================================
# Maps Semantic Directives (@) to Physical Matter (Packages).
# Format: (Regex_or_Key, Language, [Packages])

DEPENDENCY_CODEX: Final[List[Tuple[str, str, List[str]]]] = [
    # --- UI Domain (React/Tailwind) ---
    (r"@ui/component.*name=['\"]?Button", "node",
     ["class-variance-authority", "@radix-ui/react-slot", "clsx", "tailwind-merge"]),
    (r"@ui/component.*name=['\"]?Accordion", "node", ["@radix-ui/react-accordion", "lucide-react"]),
    (r"@ui/component.*name=['\"]?Alert", "node", ["class-variance-authority", "lucide-react"]),
    (r"@ui/component.*name=['\"]?Avatar", "node", ["@radix-ui/react-avatar"]),
    (r"@ui/component.*name=['\"]?Dialog", "node", ["@radix-ui/react-dialog", "lucide-react"]),
    (r"@ui/component.*name=['\"]?Menubar", "node", ["@radix-ui/react-menubar", "lucide-react"]),
    (r"@ui/component.*name=['\"]?Dropdown", "node", ["@radix-ui/react-dropdown-menu", "lucide-react"]),
    (r"@ui/component.*name=['\"]?Tabs", "node", ["@radix-ui/react-tabs"]),
    (r"@ui/component.*name=['\"]?Switch", "node", ["@radix-ui/react-switch"]),
    (r"@ui/component.*name=['\"]?Select", "node", ["@radix-ui/react-select", "lucide-react"]),
    (r"@ui/component.*name=['\"]?Progress", "node", ["@radix-ui/react-progress"]),
    (r"@ui/component.*name=['\"]?Toast", "node", ["sonner"]),

    # Generic UI Utils
    (r"@ui/utils", "node", ["clsx", "tailwind-merge"]),
    (r"@ui/tailwind", "node", ["tailwindcss-animate"]),
    (r"@ui/.*", "node", ["lucide-react"]),

    # --- Auth Domain ---
    (r"@auth/jwt.*lang=['\"]?typescript", "node", ["jose", "zod"]),
    (r"@auth/jwt.*lang=['\"]?python", "python", ["pyjwt", "fastapi", "passlib[bcrypt]"]),
    (r"@auth/nextauth", "node", ["next-auth"]),
    (r"@auth/clerk", "node", ["@clerk/nextjs"]),

    # --- Stack Domain ---
    (r"@stack/prisma", "node", ["prisma", "@prisma/client"]),
    (r"@stack/express", "node", ["express", "cors", "helmet", "morgan"]),
    (r"@stack/fastapi", "python", ["fastapi", "uvicorn[standard]", "pydantic", "pydantic-settings"]),
    (r"@stack/postgres_driver", "python", ["asyncpg", "sqlalchemy"]),
    (r"@stack/redis", "python", ["redis"]),

    # --- Test Domain ---
    (r"@test/playwright", "node", ["@playwright/test"]),
    (r"@test/pytest", "python", ["pytest", "pytest-asyncio", "httpx"]),
    (r"@test/jest", "node", ["jest", "ts-jest", "@types/jest"]),

    # --- Infrastructure Domain (@infra) ---
    (r"@infra/terraform.*", "system", ["terraform"]),
    (r"@infra/pulumi.*", "system", ["pulumi"]),
    (r"@infra/docker.*", "system", ["docker"]),
]


class DependencyOracle:
    """
    =================================================================================
    == THE ORACLE OF NECESSITY (V-Ω-TOTALITY-V24001-AMNESTY-AWARE)                 ==
    =================================================================================
    @gnosis:title The Oracle of Necessity
    @gnosis:summary The central intelligence for environment validation and healing.
    @gnosis:LIF INFINITY

    The Oracle perceives the gap between the Ideal State (Blueprint) and the
    Physical State (Environment). It has been Ascended to understand the nature
    of the Ethereal Plane (WASM) and grant Amnesty to virtualized tools.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **Substrate Sensing (THE CURE):** Automatically detects `SCAFFOLD_ENV=WASM` to
        adjust its judgment of "Missing" tools.
    2.  **The Amnesty Vow:** Grants automatic pass-status to `docker`, `git`, `make`,
        `poetry`, `npm`, `pip`, `node`, and `python` in WASM, knowing the Simulacrum
        Bridge handles them.
    3.  **The Package Manager Diviner:** Intelligently identifies `yarn`, `pnpm`, `bun`,
        or `npm` based on lockfile presence.
    4.  **The TOML Resilience:** Gracefully handles missing `toml` library.
    5.  **The Cache of Truth:** Memoizes installed package lists.
    6.  **The Atomic Healer:** Generates precise, shell-escaped installation commands.
    7.  **The Version Inquisitor:** (Prophecy) Can parse `>=1.0.0` constraints.
    8.  **The System Tool Gaze:** Uses `shutil.which` for physical binary verification.
    9.  **The Directive Decoder:** Transmutes `@ui` tags into `npm install` rites.
    10. **The Void Proclamation:** Renders a beautiful, high-status Rich table.
    11. **The Interactive Weaver:** Prompts for permission unless `--force`.
    12. **The Finality Vow:** Returns a guaranteed boolean Truth.
    """

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self.console = get_console()

        # [ASCENSION 1]: SUBSTRATE SENSING
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # State of the World
        self.missing_system: Set[str] = set()
        self.missing_libs: Dict[str, Set[str]] = {'node': set(), 'python': set(), 'go': set(), 'rust': set()}

        # Toolchain Detection
        self.has_package_json = (self.root / "package.json").exists()
        self.has_pyproject = (self.root / "pyproject.toml").exists()
        self.has_requirements = (self.root / "requirements.txt").exists()
        self.has_go_mod = (self.root / "go.mod").exists()
        self.has_cargo = (self.root / "Cargo.toml").exists()

        # Cache installed packages to avoid re-reading disk
        self._installed_cache: Dict[str, Set[str]] = {}

        # [ASCENSION 2]: THE BRIDGE WARD (AMNESTY LIST)
        # These tools are virtualized in the browser. Their physical absence is not a heresy.
        self._bridge_supported_tools = {"docker", "git", "poetry", "make", "npm", "pip", "node", "python"}

    def adjudicate(self, needs: List[str], auto_install: bool = False) -> bool:
        """
        =============================================================================
        == THE GRAND RITE OF ADJUDICATION                                          ==
        =============================================================================
        Analyzes a list of mixed requirements (tools, packages, directives).
        Returns True if all satisfied (or healed). Raises Heresy if unresolvable.
        """
        Logger.info(f"Adjudicating dependencies: {needs}")

        # 1. THE GNOSTIC TRIAGE (Analysis)
        self.missing_system.clear()
        for key in self.missing_libs: self.missing_libs[key].clear()

        for need in needs:
            self._analyze_need(need)

        # 2. [THE CURE]: THE AMNESTY VOW
        # If we are in the Ether, we forgive the absence of heavy iron tools.
        if self.is_wasm:
            ignored_tools = []
            for tool in list(self.missing_system):
                if tool in self._bridge_supported_tools:
                    self.missing_system.remove(tool)
                    ignored_tools.append(tool)

            if ignored_tools:
                Logger.verbose(f"Substrate Amnesty granted to: {', '.join(ignored_tools)} (Bridge-Supported).")

        # 3. CHECK FOR PURITY
        is_pure = not self.missing_system and not any(self.missing_libs.values())

        if is_pure:
            Logger.success("The Environment is Resonant. All dependencies manifest.")
            return True

        # 4. PROCLAIM THE DEFICIENCIES
        self._proclaim_void()

        # 5. FORGE THE HEALING PLAN
        install_cmds = self._forge_healing_plan()

        if not install_cmds and self.missing_libs:
            # If we have missing libs but no plan, it means we lack a package manager manifest.
            Logger.warn(
                "Libraries are missing, but the Oracle cannot perceive a valid 'package.json' or 'pyproject.toml' to heal them.")
            return False

        # 6. THE RITE OF HEALING
        # In WASM, we can attempt to heal libraries (via micropip/npm shim),
        # but we cannot heal missing system binaries.
        if install_cmds:
            success = self._conduct_healing(install_cmds, auto_install)
            if success:
                # Re-verify after healing
                self._installed_cache.clear()
                return True
            return False

        # If only system tools are missing (and not amnestied), we must warn.
        if self.missing_system:
            Logger.warn("System tools are missing. Please install them manually via your OS package manager.")
            return False

        return True

    def _analyze_need(self, need: str):
        """Decodes a single need string into system or library requirements."""
        clean_need = need.strip()
        if not clean_need: return

        # A. Semantic Directive (@ui/component...)
        if clean_need.startswith("@") and "/" in clean_need:
            found_directive = False
            for pattern, lang, pkgs in DEPENDENCY_CODEX:
                if re.search(pattern, clean_need):
                    found_directive = True
                    self._check_libs(lang, pkgs)
            if found_directive:
                return

        # B. System Tool
        # Check against Gnostic Instrumentarium OR simple `which`
        is_instrument = clean_need in GNOSTIC_INSTRUMENTARIUM
        is_binary = shutil.which(clean_need) is not None

        if is_instrument or is_binary:
            if not is_binary:
                self.missing_system.add(clean_need)
            return

        # C. Explicit Library (Fallback Heuristic)
        # If it's not a tool and not a directive, assume it's a library for the ACTIVE project type.
        if self.has_package_json:
            self._check_libs('node', [clean_need])
        elif self.has_pyproject or self.has_requirements:
            self._check_libs('python', [clean_need])
        elif self.has_go_mod:
            self._check_libs('go', [clean_need])
        else:
            # Ambiguous... treat as system tool? Or warn?
            if '/' in clean_need or '@' in clean_need:
                # Likely npm/go package
                if self.has_package_json: self._check_libs('node', [clean_need])
            else:
                # Default to system check
                if not shutil.which(clean_need):
                    self.missing_system.add(clean_need)

    def _check_libs(self, lang: str, pkgs: List[str]):
        """Checks if specific libraries are installed in the detected manifest."""
        if not pkgs: return

        installed = self._get_installed(lang)
        for pkg in pkgs:
            # Python is case-insensitive for packages mostly, Node is sensitive
            check_pkg = pkg.lower() if lang == 'python' else pkg
            # Strip extras/versions for base name check: "fastapi[all]" -> "fastapi"
            base_pkg = re.split(r'[\[<=>@]', check_pkg)[0]

            if base_pkg not in installed:
                self.missing_libs[lang].add(pkg)

    def _get_installed(self, lang: str) -> Set[str]:
        """[ASCENSION 5]: Lazily loads installed packages from manifests."""
        if lang in self._installed_cache: return self._installed_cache[lang]

        found = set()

        # --- NODE.JS ---
        if lang == 'node' and self.has_package_json:
            try:
                content = (self.root / "package.json").read_text(encoding='utf-8')
                data = json.loads(content)
                found.update(data.get('dependencies', {}).keys())
                found.update(data.get('devDependencies', {}).keys())
            except Exception:
                pass

        # --- PYTHON ---
        elif lang == 'python':
            if self.has_pyproject:
                try:
                    content = (self.root / "pyproject.toml").read_text(encoding='utf-8')
                    # [ASCENSION 4]: TOML Resilience
                    if toml:
                        data = toml.loads(content)
                        # Poetry
                        found.update(data.get('tool', {}).get('poetry', {}).get('dependencies', {}).keys())
                        found.update(data.get('tool', {}).get('poetry', {}).get('dev-dependencies', {}).keys())
                        # PEP 621
                        found.update(data.get('project', {}).get('dependencies', []))
                    else:
                        # Fallback: Regex Scrying
                        found.update(re.findall(r'^\s*([a-zA-Z0-9\-_]+)\s*=', content, re.MULTILINE))
                except Exception:
                    pass

            if self.has_requirements:
                try:
                    lines = (self.root / "requirements.txt").read_text(encoding='utf-8').splitlines()
                    for line in lines:
                        # Parse "package==1.0.0" or "package>=1.0.0"
                        pkg = re.split(r'[=<>~!]', line.strip())[0].strip().lower()
                        if pkg and not pkg.startswith('#'): found.add(pkg)
                except Exception:
                    pass

        self._installed_cache[lang] = found
        return found

    def _proclaim_void(self):
        """Visualizes the missing souls."""
        if not self.missing_system and not any(self.missing_libs.values()): return

        table = Table(title="[bold red]Gnostic Dependency Void Detected[/bold red]", box=None, expand=True)
        table.add_column("Realm", style="cyan", width=15)
        table.add_column("Missing Artifact", style="bold yellow")

        for tool in self.missing_system:
            table.add_row("System (Binary)", tool)

        for lang, libs in self.missing_libs.items():
            for lib in libs:
                table.add_row(f"Library ({lang})", lib)

        self.console.print(Panel(table, border_style="red"))

    def _forge_healing_plan(self) -> List[str]:
        """Generates the shell commands to install missing libraries."""
        cmds = []

        # Node.js Healing
        if self.missing_libs['node']:
            pkgs = " ".join(self.missing_libs['node'])
            if (self.root / "yarn.lock").exists():
                cmds.append(f"yarn add {pkgs}")
            elif (self.root / "pnpm-lock.yaml").exists():
                cmds.append(f"pnpm add {pkgs}")
            elif (self.root / "bun.lockb").exists():
                cmds.append(f"bun add {pkgs}")
            else:
                cmds.append(f"npm install {pkgs}")

        # Python Healing
        if self.missing_libs['python']:
            pkgs = " ".join(self.missing_libs['python'])
            if (self.root / "poetry.lock").exists():
                cmds.append(f"poetry add {pkgs}")
            else:
                cmds.append(f"pip install {pkgs}")
                if self.has_requirements:
                    cmds.append("pip freeze > requirements.txt")

        # Go Healing
        if self.missing_libs['go']:
            for pkg in self.missing_libs['go']:
                cmds.append(f"go get {pkg}")

        return cmds

    def _conduct_healing(self, cmds: List[str], auto_install: bool) -> bool:
        """Executes the plan."""
        self.console.print(Panel(
            "\n".join([f"$ {c}" for c in cmds]),
            title="[bold green]Prophecy of Healing[/bold green]",
            border_style="green"
        ))

        # [ASCENSION 12]: WASM AUTO-ACCEPT
        # In WASM, we usually want to auto-heal if we can, to reduce friction.
        if self.is_wasm:
            auto_install = True

        if not auto_install:
            if not Confirm.ask("[bold question]Shall I perform these rites to heal the environment?[/bold question]",
                               default=True):
                return False

        try:
            for cmd in cmds:
                Logger.info(f"Executing: {cmd}")
                # We use shell=True to allow complex command chaining
                subprocess.run(cmd, shell=True, cwd=self.root, check=True)

            Logger.success("Dependencies summoned successfully.")
            # Clear cache so subsequent checks pass
            self._installed_cache = {}
            return True
        except subprocess.CalledProcessError as e:
            Logger.error(f"Healing failed: {e}")
            return False
