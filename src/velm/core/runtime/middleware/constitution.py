# Path: scaffold/core/runtime/middleware/constitution.py
# ------------------------------------------------------

import re
import sys
import platform
from pathlib import Path
from typing import Optional

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest, RunRequest, GenesisRequest, TransmuteRequest, SymphonyRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .... import __version__

# Try to import packaging for semantic version comparison
try:
    from packaging.specifiers import SpecifierSet
    from packaging.version import parse as parse_version

    PACKAGING_AVAILABLE = True
except ImportError:
    PACKAGING_AVAILABLE = False


class ConstitutionMiddleware(Middleware):
    """
    =============================================================================
    == THE GUARDIAN OF THE CONSTITUTION (V-Ω-COMPATIBILITY-WARD)               ==
    =============================================================================
    LIF: 10,000,000,000

    Reads the Gnostic Header of a scripture to enforce versioning, OS requirements,
    and deprecation warnings BEFORE the Parser attempts to read the body.

    Directives supported in file headers:
    # @require-scaffold: >=2.0.0
    # @require-os: linux, darwin
    # @deprecated: "This blueprint is obsolete. Use 'api_v2.scaffold'."
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. Identify the Scripture
        target_path = self._resolve_target_scripture(request)

        if target_path and target_path.exists() and target_path.is_file():
            # 2. The Gnostic Gaze (Header Scan)
            self._adjudicate_constitution(target_path)

        return next_handler(request)

    def _resolve_target_scripture(self, request: BaseRequest) -> Optional[Path]:
        """
        Extracts the path of the primary scripture from the request.
        Handles both Path objects and strings robustly.
        """
        path_obj = None

        # 1. Extract the raw object (which might be Path or str)
        if isinstance(request, (GenesisRequest, TransmuteRequest)):
            path_obj = request.blueprint_path or "scaffold.scaffold"
        elif isinstance(request, SymphonyRequest):
            path_obj = request.symphony_path
        elif isinstance(request, RunRequest):
            path_obj = request.target

        # 2. The Gaze of the Void
        if path_obj is None:
            return None

        # 3. Transmute to String for Protocol Analysis
        # [THE FIX] We explicitly cast to str to handle WindowsPath/PosixPath objects
        path_str = str(path_obj)

        # 4. The Gaze of the Remote
        if path_str.startswith(('http://', 'https://', 'git@', 'git://')):
            # We cannot check the constitution of a remote file before fetching it.
            return None

        # 5. The Anchor of Reality
        # If it's already an absolute path (which Path objects often are when resolved),
        # Path / AbsolutePath returns AbsolutePath.
        # Path / RelativePath returns Joined Path.
        return (request.project_root or Path.cwd()) / path_str

    def _adjudicate_constitution(self, path: Path):
        """Reads the header and enforces the laws."""
        try:
            # Read only the first 2KB to find headers without reading 100MB files
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                header = f.read(2048)
        except Exception:
            return  # Binary or unreadable, skip checks

        # 1. Deprecation Check
        dep_match = re.search(r'#\s*@deprecated:\s*"(.*?)"', header)
        if dep_match:
            self.logger.warn(f"CONSTITUTIONAL WARNING: This scripture is deprecated.\n   Reason: {dep_match.group(1)}")

        # 2. OS Requirement
        os_match = re.search(r'#\s*@require-os:\s*([a-zA-Z0-9_, ]+)', header)
        if os_match:
            allowed_os = [s.strip().lower() for s in os_match.group(1).split(',')]
            current_os = platform.system().lower()

            # Map win32 to windows for user friendliness
            if current_os == 'win32': current_os = 'windows'
            if 'windows' in allowed_os and current_os == 'win32': current_os = 'windows'

            if current_os not in allowed_os:
                raise ArtisanHeresy(
                    f"OS Incompatibility Heresy: Scripture requires {allowed_os}, but this reality is '{current_os}'.",
                    severity=HeresySeverity.CRITICAL
                )

        # 3. Version Requirement
        ver_match = re.search(r'#\s*@require-scaffold:\s*([0-9a-zA-Z.,<>=! ]+)', header)
        if ver_match and PACKAGING_AVAILABLE:
            specifiers = ver_match.group(1).strip()
            try:
                spec = SpecifierSet(specifiers)
                current_ver = parse_version(__version__)
                if not spec.contains(current_ver):
                    raise ArtisanHeresy(
                        f"Version Mismatch Heresy: Scripture requires Scaffold {specifiers}, but this engine is v{__version__}.",
                        suggestion="Please upgrade Scaffold: `pip install --upgrade scaffold-cli`"
                    )
            except Exception as e:
                if not isinstance(e, ArtisanHeresy):
                    self.logger.warn(f"Could not parse version constraint '{specifiers}': {e}")