# Path: scaffold/core/structure_sentinel/strategies/python_strategy/structural/layout.py
# --------------------------------------------------------------------------------------


import functools
import re
import sys
from pathlib import Path
from typing import Set, List, Optional, Dict, Any

# [FACULTY 1] The Fault-Tolerant TOML Oracle
try:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import toml as tomllib
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False


class LayoutGeometer:
    """
    =============================================================================
    == THE GEOMETER (V-Ω-SPATIAL-ORACLE-ULTIMA)                                ==
    =============================================================================
    LIF: 10,000,000,000,000

    The Sovereign of Space.
    Calculates the shape, identity, and boundaries of the Python Cosmos.
    """

    # [FACULTY 8] The Grimoire of the Abyss (Profane Directories)
    ABYSS_PATTERNS = {
        # Identity & Config
        '.git', '.svn', '.hg', '.idea', '.vscode', '.scaffold', '.ruff_cache',
        # Build & Dist
        'build', 'dist', 'target', 'egg-info', '.eggs', 'wheels',
        # Environments
        'venv', '.venv', 'env', '.env', '__pypackages__',
        # Cache & Temporary
        '__pycache__', '.pytest_cache', '.mypy_cache', '.coverage', 'htmlcov', '.tox', '.nox',
        # Dependencies
        'node_modules', 'vendor',
        # Static & Templates (Often non-package dirs in Django/Flask)
        'static', 'media', 'templates', 'public', 'assets'
    }

    # [FACULTY 11] The Indicators of a Sovereign Domain
    ROOT_MARKERS = {
        'pyproject.toml', 'setup.py', 'setup.cfg', 'requirements.txt',
        'tox.ini', 'noxfile.py', 'Pipfile', 'poetry.lock'
    }

    # [FACULTY 2] Monorepo Container Names
    WORKSPACE_CONTAINERS = {'packages', 'apps', 'libs', 'components', 'services', 'lambdas'}

    # [FACULTY 7] Non-Package Root Directories
    NON_PACKAGE_DIRS = {'tests', 'docs', 'scripts', 'bin', 'examples', 'tools', 'utils', 'ci'}

    def __init__(self):
        # [FACULTY 9] Ephemeral cache for this session
        self._config_cache: Dict[Path, Dict[str, Any]] = {}

    def is_root_package(self, directory: Path, project_root: Path) -> bool:
        """
        [THE RITE OF SOVEREIGNTY]
        Determines if this directory is the top-level package root.
        This is where `__version__` and `py.typed` belong.
        """
        resolved_dir = directory.resolve()
        resolved_root = project_root.resolve()

        # 1. [FACULTY 4] The Oracle of Configuration (pyproject.toml)
        # If the configuration explicitly names this package, it is the Root.
        declared_packages = self._consult_pyproject_oracle(resolved_root)
        if directory.name in declared_packages:
            return True

        # 2. [FACULTY 3] The Src-Layout Vindicator
        # Structure: root/src/package_name
        if directory.parent.name == 'src' and directory.parent.parent == resolved_root:
            return True

        # 3. [FACULTY 2] The Monorepo Navigator
        # Structure: root/packages/pkg_name/src/pkg_name OR root/packages/pkg_name
        for parent in directory.parents:
            if parent == resolved_root: break

            if parent.name in self.WORKSPACE_CONTAINERS and parent.parent == resolved_root:
                # We are inside a monorepo workspace.

                # A. Src Layout within Workspace
                # root/packages/my-lib/src/my_lib
                if directory.parent.name == 'src' and directory.parent.parent.parent == parent:
                    return True

                # B. Flat Layout within Workspace
                # root/packages/my-lib/my_lib (where my-lib is the container for the package code)
                # This is tricky. Often the dir under 'packages' IS the package root if it has __init__.py
                # But typically: packages/library-a/library_a/__init__.py
                if directory.parent.parent == parent and self._has_root_markers(directory.parent):
                    return True

        # 4. [FACULTY 7] The Flat Layout Heuristic
        # Structure: root/package_name
        if directory.parent == resolved_root:
            # Must have sibling config files to be a root package
            if self._has_root_markers(resolved_root):
                # Guard: Exclude common non-package folders
                if directory.name.lower() not in self.NON_PACKAGE_DIRS:
                    # Also ensure it doesn't start with '.' or '_'
                    if not directory.name.startswith(('.', '_')):
                        return True

        # 5. [FACULTY 6] The Django App Detector
        # Structure: root/app_name (containing apps.py or models.py)
        if (directory / "apps.py").exists() or (directory / "models.py").exists():
            # A Django app is a root in its own right contextually
            return True

        return False

    def is_namespace_package(self, directory: Path) -> bool:
        """
        [FACULTY 5] THE NAMESPACE DIVINER
        Checks for markers indicating this should be a PEP 420 namespace.
        """
        # 1. Explicit Marker (Scaffold Specific)
        if (directory / ".namespace").exists():
            return True

        # 2. Heuristic: Common Namespace Names
        if directory.name in {"plugins", "extensions", "contrib", "namespace"}:
            return True

        # 3. Implicit PEP 420 check (Future)
        # If it has subdirectories that ARE packages, but has no __init__.py itself.
        # This is handled by the StructuralEngine's flow logic usually.

        return False

    def should_be_typed(self, directory: Path, project_root: Path) -> bool:
        """
        [FACULTY 10] THE TYPED SENTRY
        Decides if a directory deserves the `py.typed` marker.
        Strict adherence to PEP 561: Only the root package needs the marker.
        """
        return self.is_root_package(directory, project_root)

    def is_abyss(self, directory: Path) -> bool:
        """
        [FACULTY 8] THE ABYSS WARD
        Identifies profane directories that must not be consecrated.
        """
        name = directory.name

        # 1. Exact Match
        if name in self.ABYSS_PATTERNS: return True

        # 2. Prefix Match (Hidden/Dunder)
        # Exception: current directory '.'
        if name != '.' and name.startswith('.'): return True
        if name.startswith('__') and name != '__init__.py': return True

        # 3. Suffix Match (Extensions treated as dirs)
        if name.endswith('.egg-info'): return True
        if name.endswith('.dist-info'): return True

        return False

    def _has_root_markers(self, directory: Path) -> bool:
        """[FACULTY 11] Checks for the presence of sacred configuration files."""
        for marker in self.ROOT_MARKERS:
            if (directory / marker).exists():
                return True
        return False

    def _consult_pyproject_oracle(self, project_root: Path) -> Set[str]:
        """
        [FACULTY 1 & 9] THE CONFIGURATION ORACLE
        Parses pyproject.toml to find explicitly declared packages.
        Uses a Regex Fallback if TOML libraries are missing.
        Cached for infinite speed.
        """
        pyproject = project_root / "pyproject.toml"
        if pyproject not in self._config_cache:
            self._config_cache[pyproject] = self._parse_pyproject(pyproject)

        return self._config_cache[pyproject]

    def _parse_pyproject(self, path: Path) -> Set[str]:
        packages = set()
        if not path.exists():
            return packages

        try:
            content = path.read_text(encoding='utf-8')

            # [FACULTY 1] Strategy A: True TOML Parsing
            if TOML_AVAILABLE:
                try:
                    data = tomllib.loads(content) if 'tomllib' in sys.modules else tomllib.loads(content)

                    # [FACULTY 4] PEP 621 (Standard)
                    if "project" in data:
                        if "name" in data["project"]:
                            packages.add(data["project"]["name"].replace("-", "_"))

                    # Poetry (Legacy/Alternative)
                    if "tool" in data and "poetry" in data["tool"]:
                        # Poetry packages list
                        pkgs = data["tool"]["poetry"].get("packages", [])
                        for p in pkgs:
                            if "include" in p: packages.add(p["include"])

                        # Poetry Name
                        if "name" in data["tool"]["poetry"]:
                            packages.add(data["tool"]["poetry"]["name"].replace("-", "_"))

                    # Setuptools (Legacy)
                    if "tool" in data and "setuptools" in data["tool"]:
                        if "packages" in data["tool"]["setuptools"]:
                            packages.update(data["tool"]["setuptools"]["packages"])

                    return packages
                except Exception:
                    # Fallback to regex if TOML parsing fails (e.g. syntax error)
                    pass

            # [FACULTY 1] Strategy B: The Regex Sage (Fallback)
            # Look for name = "x" in [project] or [tool.poetry]
            match_name = re.search(r'^name\s*=\s*["\']([\w-]+)["\']', content, re.MULTILINE)
            if match_name:
                packages.add(match_name.group(1).replace("-", "_"))

            # Look for packages = [{include = "x"}]
            match_include = re.findall(r'include\s*=\s*["\']([\w-]+)["\']', content)
            packages.update(match_include)

        except Exception:
            pass

        return packages