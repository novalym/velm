# Path: core/structure_sentinel/strategies/python_strategy/structural/layout.py
# -----------------------------------------------------------------------------
# =========================================================================================
# == THE GEOMETER (V-Ω-SPATIAL-ORACLE-V24000-RECURSIVE-ROOT)                             ==
# =========================================================================================
# LIF: ∞ | ROLE: TOPOLOGICAL_NAVIGATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_GEOMETER_V24000_RECURSIVE_ROOT_FINALIS
#
# [ASCENSION UPDATE]: The `is_root_package` rite has been ascended. It now
# recursively gazes UPWARDS from the target directory to find the `pyproject.toml`
# Anchor. This fixes the blind spot where `src/package_name` was not recognized
# as a root because the config file lived in `.` (the parent of `src`).
# =========================================================================================

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
    """The Sovereign of Space."""

    # [FACULTY 8] The Grimoire of the Abyss
    ABYSS_PATTERNS = {
        '.git', '.svn', '.hg', '.idea', '.vscode', '.scaffold', '.ruff_cache',
        'build', 'dist', 'target', 'egg-info', '.eggs', 'wheels',
        'venv', '.venv', 'env', '.env', '__pypackages__',
        '__pycache__', '.pytest_cache', '.mypy_cache', '.coverage', 'htmlcov', '.tox', '.nox',
        'node_modules', 'vendor',
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
    NON_PACKAGE_DIRS = {'tests', 'docs', 'scripts', 'bin', 'examples', 'tools', 'utils', 'ci', 'src'}

    def __init__(self):
        # [FACULTY 9] Ephemeral cache for this session
        self._config_cache: Dict[Path, Dict[str, Any]] = {}

    def is_root_package(self, directory: Path, project_root: Path) -> bool:
        """
        [THE RITE OF SOVEREIGNTY]
        Determines if this directory is the top-level package root.
        """
        resolved_dir = directory.resolve()
        resolved_root = project_root.resolve()

        # 1. [FACULTY 4] The Oracle of Configuration
        # Does the project config explicitly claim this directory name?
        declared_packages = self._consult_pyproject_oracle(resolved_root)
        if directory.name in declared_packages:
            return True

        # 2. [FACULTY 12]: THE RECURSIVE ROOT GAZE (THE CURE)
        # We check if a ROOT_MARKER exists in the parent hierarchy.
        # If we are in `src/pkg`, we look at `src/` then `root/`.
        # If `root/pyproject.toml` exists, and we are not a `NON_PACKAGE_DIR` (like tests),
        # then we are a root package candidate.

        # Check standard Src Layout
        if directory.parent.name == 'src':
            # Verify the grandparent has the marker
            if self._has_root_markers(directory.parent.parent):
                return True

        # Check Flat Layout
        if self._has_root_markers(directory.parent):
            # Guard against false positives
            if directory.name.lower() not in self.NON_PACKAGE_DIRS and not directory.name.startswith(('.', '_')):
                return True

        # 3. [FACULTY 6] Django App Detector
        if (directory / "apps.py").exists() or (directory / "models.py").exists():
            return True

        return False

    def is_namespace_package(self, directory: Path) -> bool:
        """[FACULTY 5] THE NAMESPACE DIVINER"""
        if (directory / ".namespace").exists(): return True
        if directory.name in {"plugins", "extensions", "contrib", "namespace"}: return True
        return False

    def should_be_typed(self, directory: Path, project_root: Path) -> bool:
        """[FACULTY 10] THE TYPED SENTRY"""
        return self.is_root_package(directory, project_root)

    def is_abyss(self, directory: Path) -> bool:
        """[FACULTY 8] THE ABYSS WARD"""
        name = directory.name
        if name in self.ABYSS_PATTERNS: return True
        if name != '.' and name.startswith('.'): return True
        if name.startswith('__') and name != '__init__.py': return True
        if name.endswith('.egg-info'): return True
        return False

    def _has_root_markers(self, directory: Path) -> bool:
        """[FACULTY 11] Checks for sacred configuration files."""
        for marker in self.ROOT_MARKERS:
            if (directory / marker).exists():
                return True
        return False

    def _consult_pyproject_oracle(self, project_root: Path) -> Set[str]:
        """[FACULTY 1 & 9] THE CONFIGURATION ORACLE"""
        pyproject = project_root / "pyproject.toml"
        if pyproject not in self._config_cache:
            self._config_cache[pyproject] = self._parse_pyproject(pyproject)
        return self._config_cache[pyproject]

    def _parse_pyproject(self, path: Path) -> Set[str]:
        packages = set()
        if not path.exists(): return packages

        try:
            content = path.read_text(encoding='utf-8')
            if TOML_AVAILABLE:
                try:
                    data = tomllib.loads(content) if 'tomllib' in sys.modules else tomllib.loads(content)

                    if "project" in data:
                        if "name" in data["project"]:
                            packages.add(data["project"]["name"].replace("-", "_"))

                    if "tool" in data and "poetry" in data["tool"]:
                        pkgs = data["tool"]["poetry"].get("packages", [])
                        for p in pkgs:
                            if "include" in p: packages.add(p["include"])
                        if "name" in data["tool"]["poetry"]:
                            packages.add(data["tool"]["poetry"]["name"].replace("-", "_"))

                    if "tool" in data and "setuptools" in data["tool"]:
                        if "packages" in data["tool"]["setuptools"]:
                            packages.update(data["tool"]["setuptools"]["packages"])

                    return packages
                except Exception:
                    pass

            # Regex Fallback
            match_name = re.search(r'^name\s*=\s*["\']([\w-]+)["\']', content, re.MULTILINE)
            if match_name:
                packages.add(match_name.group(1).replace("-", "_"))

            match_include = re.findall(r'include\s*=\s*["\']([\w-]+)["\']', content)
            packages.update(match_include)

        except Exception:
            pass

        return packages