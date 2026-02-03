# Path: scaffold/core/cortex/dependency_oracle.py
# -----------------------------------------------

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Set

import toml
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from ...gnostic_instrumentarium import GNOSTIC_INSTRUMENTARIUM
from ...logger import Scribe, get_console

Logger = Scribe("DependencyOracle")

# =================================================================================
# == THE CODEX OF REQUIRED SOULS (MERGED & EXPANDED)                             ==
# =================================================================================
# Maps Directive Patterns AND Abstract Concepts to Required Packages.
# Format: (Regex_or_Key, Language, [Packages])

DEPENDENCY_CODEX = [
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

    # --- Stack Domain ---
    (r"@stack/prisma", "node", ["prisma", "@prisma/client"]),
    (r"@stack/express", "node", ["express", "cors", "helmet", "morgan"]),
    (r"@stack/fastapi", "python", ["fastapi", "uvicorn[standard]", "pydantic", "pydantic-settings"]),
    (r"@stack/postgres_driver", "python", ["asyncpg", "sqlalchemy"]),

    # --- Test Domain ---
    (r"@test/playwright", "node", ["@playwright/test"]),
    (r"@test/pytest", "python", ["pytest", "pytest-asyncio", "httpx"]),
    # --- Infrastructure Domain (@infra) ---

    # Terraform Requirements
    (r"@infra/terraform.*", "system", ["terraform"]),

    # Pulumi Requirements (System Tool + Python Libs)
    (r"@infra/pulumi.*", "system", ["pulumi"]),
    (r"@infra/pulumi.*", "python", ["pulumi", "pulumi-aws"]),

    # Specific Pulumi Extensions
    (r"@infra/pulumi-fargate", "python", ["pulumi-awsx"]),
]


class DependencyOracle:
    """
    =================================================================================
    == THE ORACLE OF NECESSITY (V-Ω-UNIFIED-OMNISCIENT)                            ==
    =================================================================================
    LIF: 100,000,000,000

    The central intelligence for dependency resolution. It unifies:
    1. **System Gaze:** Checking for CLI tools (git, docker).
    2. **Semantic Gaze:** Decoding `@directives` into package lists.
    3. **Manifest Gaze:** Scanning `package.json` / `pyproject.toml` for existing souls.
    4. **Healing Rite:** Generating and executing the correct install commands for the active toolchain.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.console = get_console()

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

    def adjudicate(self, needs: List[str], auto_install: bool = False) -> bool:
        """
        The Grand Rite.
        Analyzes a list of mixed requirements (tools, packages, directives).
        Returns True if all satisfied (or healed). Raises Heresy if unresolvable failure.
        """
        Logger.info(f"Adjudicating dependencies: {needs}")

        # 1. The Gnostic Triage
        for need in needs:
            self._analyze_need(need)

        # 2. Check for Purity
        is_pure = not self.missing_system and not any(self.missing_libs.values())

        if is_pure:
            Logger.success("The Environment is Pure. All dependencies manifest.")
            return True

        # 3. Proclaim the Deficiencies
        self._proclaim_void()

        # 4. Forge the Plan
        install_cmds = self._forge_healing_plan()

        if not install_cmds and self.missing_libs:
            Logger.warn("Libraries are missing, but the Oracle cannot detect a valid package manager to heal them.")
            return False

        # 5. The Rite of Healing
        if install_cmds:
            return self._conduct_healing(install_cmds, auto_install)

        # If only system tools are missing, we warn but (usually) don't auto-install due to sudo/permissions complexity
        if self.missing_system:
            Logger.warn("System tools are missing. Please install them manually via your OS package manager.")
            return False

        return True

    def _analyze_need(self, need: str):
        """Decodes a single need string into system or library requirements."""
        clean_need = need.strip()

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
        if clean_need in GNOSTIC_INSTRUMENTARIUM or shutil.which(clean_need):
            if not shutil.which(clean_need):
                self.missing_system.add(clean_need)
            return

        # C. Explicit Library (Fallback)
        # If it's not a tool and not a directive, assume it's a library for the ACTIVE project type.
        # Heuristic:
        if self.has_package_json:
            self._check_libs('node', [clean_need])
        elif self.has_pyproject or self.has_requirements:
            self._check_libs('python', [clean_need])
        elif self.has_go_mod:
            self._check_libs('go', [clean_need])
        else:
            # Ambiguous... treat as system tool? Or warn?
            # Let's check if it looks like a package (has / or @)
            if '/' in clean_need or '@' in clean_need:
                # Likely npm/go
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
            # Simple check. For Python, we might need to handle extras [standard]
            base_pkg = re.split(r'[\[<=>]', check_pkg)[0]

            if base_pkg not in installed:
                self.missing_libs[lang].add(pkg)

    def _get_installed(self, lang: str) -> Set[str]:
        """Lazily loads installed packages from manifests."""
        if lang in self._installed_cache: return self._installed_cache[lang]

        found = set()
        if lang == 'node' and self.has_package_json:
            try:
                data = json.loads((self.root / "package.json").read_text(encoding='utf-8'))
                found.update(data.get('dependencies', {}).keys())
                found.update(data.get('devDependencies', {}).keys())
            except:
                pass

        elif lang == 'python':
            if self.has_pyproject:
                try:
                    data = toml.loads((self.root / "pyproject.toml").read_text(encoding='utf-8'))
                    # Poetry
                    found.update(data.get('tool', {}).get('poetry', {}).get('dependencies', {}).keys())
                    # PEP 621
                    found.update(data.get('project', {}).get('dependencies', []))
                except:
                    pass
            if self.has_requirements:
                try:
                    lines = (self.root / "requirements.txt").read_text(encoding='utf-8').splitlines()
                    for line in lines:
                        pkg = line.split('==')[0].split('>=')[0].split('[')[0].strip().lower()
                        if pkg and not pkg.startswith('#'): found.add(pkg)
                except:
                    pass

        self._installed_cache[lang] = found
        return found

    def _proclaim_void(self):
        """Visualizes the missing souls."""
        if not self.missing_system and not any(self.missing_libs.values()): return

        table = Table(title="[bold red]Gnostic Dependency Void Detected[/bold red]", box=None)
        table.add_column("Realm", style="cyan")
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

        # Node
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

        # Python
        if self.missing_libs['python']:
            pkgs = " ".join(self.missing_libs['python'])
            if (self.root / "poetry.lock").exists() or self.has_pyproject:
                cmds.append(f"poetry add {pkgs}")
            else:
                cmds.append(f"pip install {pkgs}")
                cmds.append("pip freeze > requirements.txt")

        # Go
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

        if not auto_install:
            if not Confirm.ask("[bold question]Shall I perform these rites to heal the environment?[/bold question]",
                               default=True):
                return False

        try:
            for cmd in cmds:
                Logger.info(f"Executing: {cmd}")
                subprocess.run(cmd, shell=True, cwd=self.root, check=True)
            Logger.success("Dependencies summoned successfully.")
            # Clear cache so subsequent checks pass
            self._installed_cache = {}
            return True
        except subprocess.CalledProcessError as e:
            Logger.error(f"Healing failed: {e}")
            return False

