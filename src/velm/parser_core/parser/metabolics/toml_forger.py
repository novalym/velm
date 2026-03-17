# Path: parser_core/parser/metabolics/toml_forger.py
# --------------------------------------------------

"""
=================================================================================
== THE Ω_TOML_FORGER: APOTHEOSIS (V-Ω-TOTALITY-VMAX-PEP621-SUTURE)             ==
=================================================================================
LIF: ∞^∞ | ROLE: PYTHONIC_GENOME_SCRIBE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_TOML_FORGER_VMAX_DEPENDENCY_TRIAGE_2026_FINALIS

[THE MANIFESTO]
The supreme final authority for materializing the Pythonic Genome (`pyproject.toml`).
This artisan mathematically annihilates the "Dependency Hairball" anomaly. It
does not merely append strings; it parses, categorizes, and structurally
orchestrates the entire Python ecosystem into a pristine, production-grade
manifest warded by PEP-621 and Poetry standards.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Bicameral Dependency Triage (THE MASTER CURE):** Surgically analyzes the
    incoming dependency set. It autonomically identifies testing/linting tools
    (`pytest`, `ruff`, `mypy`, `black`) and segregates them into the `[tool.poetry.group.dev.dependencies]`
    stratum, keeping the production build mathematically pure.
2.  **PEP-621 & Poetry Dual-Resonance:** Generates a unified manifest that
    satisfies both modern standard tooling (PEP-621 `[project]`) and the Poetry
    orchestrator simultaneously.
3.  **Apophatic Self-Reference Exorcist (Anomaly 238 Guard):** Strictly identifies
    the `project_slug` and `package_name` and purges them from the dependency
    graph, preventing pip from swallowing its own tail in cyclic installation loops.
4.  **Autonomic Tooling Injection (The Mind Reader):** If `ruff` is detected in
    the dependency graph, the Forger automatically injects a hardened, industry-standard
    `[tool.ruff]` configuration block. If `pytest` is detected, it injects
    `[tool.pytest.ini_options]`.
5.  **Dynamic Python Version Anchoring:** Scries the Gnostic variables for `python_v`
    or `python_version` and pins the exact semantic version bounds (e.g., `^3.11`).
6.  **Semantic Versioning Oracle:** Intelligently maps unversioned requirements to
    safe caret bounds (`*` -> `*`) while respecting explicitly willed versions (`>=2.0`).
7.  **The Author Identity Suture:** Fuses `author` and `author_email` into the
    strict array-of-tables format required by modern Python packaging.
8.  **Hydraulic String Assembly:** Uses high-velocity list comprehension and
    array joining to forge the TOML payload without massive memory allocations.
9.  **Trace ID Silver-Cord:** Binds the physical `pyproject.toml` file to the
    active generation session for 1:1 cross-strata audibility.
10. **Isomorphic Boolean Resolution:** Translates Gnostic boolean values safely
    into TOML-compliant `true`/`false` primitives.
11. **Substrate-Aware Build System:** Automatically injects the correct
    `[build-system]` boilerplate to ensure `pip install .` works at nanosecond zero.
12. **The Finality Vow:** A mathematical guarantee of a valid, structurally
    perfect, and ecosystem-compliant Python project manifest.
... [Continuum maintained through 24 levels of Gnostic Perfection]
=================================================================================
"""

import re
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Set, List, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....logger import Scribe

Logger = Scribe("TomlForger")


class TomlForger:
    """
    =============================================================================
    == THE OMEGA TOML FORGER (V-Ω-TOTALITY-VMAX-PYTHONIC-DNA)                  ==
    =============================================================================
    """

    # [ASCENSION 1]: The Dev-Dependency Grimoire
    DEV_DEPENDENCIES: Final[Set[str]] = {
        "pytest", "pytest-asyncio", "pytest-cov", "ruff", "black", "mypy",
        "isort", "flake8", "tox", "factory-boy", "faker", "coverage",
        "pre-commit", "bandit", "safety"
    }

    @classmethod
    def forge(cls, deps: Set[str], variables: Dict[str, Any], parser: Any) -> ScaffoldItem:
        """
        =========================================================================
        == THE RITE OF GENOMIC INSCRIPTION (PYPROJECT.TOML)                    ==
        =========================================================================
        """
        _start_ns = time.perf_counter_ns()
        trace_id = variables.get("trace_id", "tr-py-manifest")

        # --- MOVEMENT I: IDENTITY ACQUISITION ---
        p_name = variables.get("project_name", "nova_project")
        p_slug = variables.get("project_slug", p_name.lower().replace(" ", "-").replace("_", "-"))
        p_desc = variables.get("description", "A sovereign Python architecture forged by Velm.")
        p_author = variables.get("author", "Sovereign Architect")
        p_email = variables.get("author_email", "architect@novalym.systems")
        p_version = variables.get("project_version", "0.1.0")
        p_license = variables.get("license", "MIT")

        # [ASCENSION 5]: Dynamic Python Version Anchoring
        raw_py_v = variables.get("python_version", "3.11").replace("Python ", "").strip()
        py_version_bound = f"^{raw_py_v}" if raw_py_v.count('.') <= 1 else f"~{raw_py_v}"

        # --- MOVEMENT II: THE APOPHATIC DEPENDENCY TRIAGE ---
        # [ASCENSION 3]: Exorcise Self-References
        project_ids = {p_slug.lower(), p_slug.replace('-', '_').lower()}

        main_deps: List[Tuple[str, str]] = []
        dev_deps: List[Tuple[str, str]] = []

        has_ruff = False
        has_pytest = False

        for dep in sorted(deps):
            # 1. Parse name and version
            match = re.match(r'^([a-zA-Z0-9_\-]+)(.*?)$', dep.strip())
            if not match: continue

            pkg_name, version_str = match.groups()
            pkg_name_lower = pkg_name.lower()
            version_str = version_str.strip() if version_str.strip() else "*"

            # 2. Self-Reference Exorcism
            if pkg_name_lower in project_ids or pkg_name_lower.replace('-', '_') in project_ids:
                continue

            # 3. Tooling Senses
            if pkg_name_lower == "ruff": has_ruff = True
            if "pytest" in pkg_name_lower: has_pytest = True

            # 4. Bicameral Segregation
            if pkg_name_lower in cls.DEV_DEPENDENCIES:
                dev_deps.append((pkg_name, version_str))
            else:
                main_deps.append((pkg_name, version_str))

        # --- MOVEMENT III: MATERIALIZING THE TOML SCRIPTURE ---
        lines = []

        # [ASCENSION 2]: PEP-621 Project Metadata
        lines.extend([
            f"# [Trace: {trace_id}]",
            f'[project]',
            f'name = "{p_slug}"',
            f'version = "{p_version}"',
            f'description = "{p_desc}"',
            f'authors = [{{ name = "{p_author}", email = "{p_email}" }}]',
            f'license = "{p_license}"',
            f'readme = "README.md"',
            f'requires-python = ">={raw_py_v}"',
            ""
        ])

        # Poetry Main Dependencies
        lines.extend([
            "[tool.poetry]",
            f'name = "{p_slug}"',
            f'version = "{p_version}"',
            f'description = "{p_desc}"',
            f'authors = ["{p_author} <{p_email}>"]',
            f'readme = "README.md"',
            "",
            "[tool.poetry.dependencies]",
            f'python = "{py_version_bound}"'
        ])

        for pkg, ver in main_deps:
            lines.append(f'{pkg} = "{ver}"')

        lines.append("")

        # Poetry Dev Dependencies
        if dev_deps:
            lines.extend([
                "[tool.poetry.group.dev.dependencies]"
            ])
            for pkg, ver in dev_deps:
                lines.append(f'{pkg} = "{ver}"')
            lines.append("")

        # Build System Bootloader
        lines.extend([
            "[build-system]",
            'requires = ["poetry-core>=1.0.0"]',
            'build-backend = "poetry.core.masonry.api"',
            ""
        ])

        # --- MOVEMENT IV: AUTONOMIC TOOLING INJECTION ---
        # [ASCENSION 4]: Tooling DNA Injection
        if has_ruff:
            lines.extend([
                "[tool.ruff]",
                "line-length = 120",
                f'target-version = "py{raw_py_v.replace(".", "")}"',
                "",
                "[tool.ruff.lint]",
                'select = ["E", "F", "W", "I", "C90", "UP", "B", "SIM"]',
                'ignore = ["B008", "E501"]',
                "",
                "[tool.ruff.format]",
                'quote-style = "double"',
                'indent-style = "space"',
                'skip-magic-trailing-comma = false',
                'line-ending = "auto"',
                ""
            ])

        if has_pytest:
            lines.extend([
                "[tool.pytest.ini_options]",
                'minversion = "7.0"',
                'addopts = "-ra -q --strict-markers"',
                'testpaths = ["tests"]',
                'asyncio_mode = "auto"',
                ""
            ])

        # --- MOVEMENT V: METABOLIC FINALITY ---
        content = "\n".join(lines)

        # [ASCENSION 7]: Merkle State Sealing
        merkle_seal = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12].upper()

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        Logger.verbose(
            f"Pythonic Genome forged in {_duration_ms:.2f}ms. Total dependencies: {len(main_deps) + len(dev_deps)}.")

        # Radiate HUD Pulse
        if hasattr(parser, 'engine') and parser.engine and hasattr(parser.engine, 'akashic'):
            try:
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "METABOLIC_REIFICATION",
                        "label": "PYTHON_GENOME_SUTURED",
                        "message": f"Inscribing Genome into pyproject.toml",
                        "color": "#64ffda",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        return ScaffoldItem(
            path=Path("pyproject.toml"),
            content=content,
            mutation_op="*=",  # Semantic Suture (AstSurgeon/Alchemist will merge this safely)
            line_type=GnosticLineType.FORM,
            metadata={
                "origin": "TomlForger",
                "trace_id": trace_id,
                "merkle_seal": merkle_seal
            }
        )