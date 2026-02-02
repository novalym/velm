# Path: scaffold/core/structure_sentinel/strategies/python_strategy/structural/content.py
# ---------------------------------------------------------------------------------------

import ast
import datetime
import unicodedata
import re
from pathlib import Path
from typing import Optional, List, Dict, Any


class ContentScribe:
    """
    =============================================================================
    == THE CONTENT SCRIBE (V-Ω-OMNISCIENT-ARCHITECT-PRIME)                     ==
    =============================================================================
    LIF: INFINITY

    The Gnostic Poet of the Python structure.
    It forges scriptures (`__init__.py`, `py.typed`) that are context-aware,
    legally compliant, stylistically pure, and syntactically validated.

    It adheres strictly to the Sacred Order of Pythonic definition:
    1. Encoding Cookie (if required)
    2. License/Copyright Header (Temporal Aware)
    3. Module Docstring (Templated & Semantic)
    4. Future Imports (Time Travel)
    5. Standard Imports (Sub-packages with Shadow Filter)
    6. Extended Metadata (__version__, __author__, __credits__, __status__)
    7. The Sacred Anchor (__all__) - Now Pure Code
    """

    # [FACULTY 3] The Contextual Poet's Expanded Dictionary
    DOCSTRING_MAP = {
        # Core Architecture
        "api": "API endpoints, route definitions, and request handlers for {{project_name}}.",
        "core": "Core business logic, domain entities, and use cases.",
        "domain": "Pure domain logic, entities, and business rules (Hexagonal Core).",
        "infrastructure": "External adapters, database connections, and third-party integrations.",
        "interfaces": "Abstract base classes and protocol definitions.",

        # Data & State
        "models": "Data models, Pydantic schemas, and database ORM definitions.",
        "schemas": "Data transfer objects (DTOs) and serialization schemas.",
        "migrations": "Database schema evolution scripts.",
        "repositories": "Data access layer and persistence logic.",

        # Application Logic
        "services": "Business service layer implementations and orchestrators.",
        "utils": "Shared utility functions, helpers, and common tools.",
        "lib": "Reusable library components and foundational logic.",
        "exceptions": "Custom exception hierarchy and error handling.",
        "handlers": "Event handlers and message consumers.",

        # Configuration & Entry
        "config": "Configuration management and environment settings.",
        "routers": "FastAPI route definitions and sub-applications.",
        "dependencies": "Dependency injection providers and container configuration.",
        "cli": "Command-line interface entry points and command definitions.",
        "main": "Application entry point and bootstrap logic.",

        # Extensibility
        "plugins": "Plugin architecture and extension points.",
        "middleware": "Request/Response processing hooks and interceptors.",

        # Quality Assurance
        "tests": "Test suite, fixtures, and verification logic.",
        "types": "Type definitions, aliases, and protocols.",
    }

    def forge_init(
            self,
            directory: Path,
            is_root: bool,
            license_header: str,
            package_name: Optional[str] = None,
            gnosis: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        [THE RITE OF FORGING V7 - GOD-TIER]
        Forges the soul of an `__init__.py` file with extended metadata and dynamic templating.
        """
        lines = []
        dir_name = package_name or directory.name
        gnosis = gnosis or {}

        # [FACULTY 10] The Encoding Sentinel
        lines.append("# -*- coding: utf-8 -*-")

        # [FACULTY 8 & 31] The License Alchemist & Header Deduplication
        if license_header and license_header.strip() not in str(gnosis):
            lines.append(license_header)

        # [FACULTY 1 & 13 & 30] The Gnostic Templater & Docstring Trimmer
        raw_desc = self.DOCSTRING_MAP.get(dir_name.lower(), f"The `{dir_name}` package.")
        project_name = gnosis.get("project_name", "the project")
        desc = raw_desc.replace("{{project_name}}", project_name).strip()

        # [FACULTY 29] Quote Style Harmonizer
        lines.append(f'"""')
        lines.append(f"{desc}")
        lines.append(f"")
        lines.append(f"Auto-consecrated by the Scaffold God-Engine.")
        lines.append(f'"""')
        lines.append("")

        # [FACULTY 2] The Future Sight
        lines.append("from __future__ import annotations")
        lines.append("")

        # [FACULTY 4, 15, 22, 26, 33] Sub-Package Radar, Shadow Filter, Sorted Lexicon, Path Sanitizer, Import Categorizer
        try:
            sub_packages = []
            for d in directory.iterdir():
                if d.is_dir() and (d / "__init__.py").exists():
                    # [FACULTY 15] Shadow Filter
                    if d.name.startswith(("_", ".")): continue
                    if d.name in ("__pycache__", ".pytest_cache", ".git"): continue

                    # [FACULTY 26] Path Sanitizer (Must be valid identifier)
                    if not d.name.isidentifier(): continue

                    sub_packages.append(d.name)

            if sub_packages:
                lines.append("# --- Sub-Package Exports ---")
                for pkg in sorted(sub_packages):
                    lines.append(f"from . import {pkg}")
                lines.append("")
        except OSError:
            pass

        # [FACULTY 5, 14, 21, 27, 30] Metadata Pantheon, Dunder Sorter
        if is_root:
            lines.append("# --- Metadata ---")

            # Prepare metadata for sorting
            metadata_lines = []

            version = gnosis.get("version", "0.1.0")
            metadata_lines.append(f'__version__ = "{version}"')

            # [FACULTY 21] Dynamic Status
            status = "Development" if version.startswith("0.") else "Production"
            metadata_lines.append(f'__status__ = "{status}"')

            author = gnosis.get("author")
            email = gnosis.get("author_email")

            if author and email:
                metadata_lines.append(f'__author__ = "{author} <{email}>"')
            elif author:
                metadata_lines.append(f'__author__ = "{author}"')

            if gnosis.get("maintainer"):
                metadata_lines.append(f'__maintainer__ = "{gnosis["maintainer"]}"')

            if gnosis.get("license"):
                metadata_lines.append(f'__license__ = "{gnosis["license"]}"')

            if gnosis.get("credits"):
                metadata_lines.append(f'__credits__ = {gnosis["credits"]}')

            # [FACULTY 27] Sort Dunders
            lines.extend(sorted(metadata_lines))
            lines.append("")

        # [FACULTY 20] The Timestamped Seal
        if gnosis.get("timestamp_creation"):
            timestamp = datetime.datetime.now().isoformat()
            lines.append(f"# Generated at: {timestamp}")

        # [FACULTY 18] The Strict Spacer
        # Ensure exactly one blank line before __all__ if there is preceding content
        if lines and lines[-1] != "":
            lines.append("")

        # [FACULTY 25] THE AST COMPATIBILITY WARD (THE FIX)
        # We revert to standard assignment `__all__ = []` instead of `__all__: list[str] = []`.
        # This ensures the ApiGuardian (which looks for ast.Assign) perceives it correctly
        # and does not append a duplicate.
        lines.append("__all__ = []")
        lines.append("")

        # [FACULTY 23] The ASCII Guard (Normalization)
        raw_content = "\n".join(lines)
        normalized_content = unicodedata.normalize('NFKC', raw_content)

        # [FACULTY 28] The Final Newline Sentinel & Polish
        # Collapse excessive newlines (max 2)
        final_content = re.sub(r'\n{3,}', '\n\n', normalized_content).strip() + "\n"

        # [FACULTY 24] The Final Validator
        self._validate_syntax(final_content, f"__init__.py for {dir_name}")

        return final_content

    def forge_marker(self) -> str:
        """
        [FACULTY 16] The PyTyped Professor.
        """
        return (
            "# Marker file for PEP 561.\n"
            "# This package supports type checking.\n"
            "# See: https://www.python.org/dev/peps/pep-0561/\n"
        )

    def get_license_header(self, root: Path) -> str:
        """
        [FACULTY 8] The License Alchemist.
        """
        for name in ["LICENSE", "LICENSE.txt", "COPYING", "LICENSE.md"]:
            license_file = root / name
            if license_file.exists():
                try:
                    with open(license_file, 'r', encoding='utf-8') as f:
                        lines_to_scan = [f.readline().strip() for _ in range(10)]
                        copyright_line = next((l for l in lines_to_scan if "copyright" in l.lower()), None)

                        if copyright_line:
                            return f"# {copyright_line}"

                        first_line = lines_to_scan[0] if lines_to_scan else ""
                        if any(t in first_line.lower() for t in ['mit', 'apache', 'gnu', 'bsd']):
                            year = datetime.datetime.now().year
                            return f"# {first_line} (Copyright {year})"

                except Exception:
                    pass
        return ""

    def _validate_syntax(self, content: str, context: str):
        """
        [FACULTY 24] The Syntax Hypervisor.
        """
        try:
            ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"ContentScribe generated invalid Python syntax for {context}: {e}")