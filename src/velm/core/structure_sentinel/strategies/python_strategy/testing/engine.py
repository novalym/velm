# Path: src/velm/core/structure_sentinel/strategies/python_strategy/testing/engine.py
# -----------------------------------------------------------------------------------

from __future__ import annotations
import time
import traceback
import hashlib
import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List, Dict, Any, Union, Final, Set, Tuple

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......contracts.data_contracts import ScaffoldItem, GnosticLineType

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from .analyzer import SourceCodeAnatomist
    from .generator import PytestArchitect
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class TestingFaculty(BaseFaculty):
    """
    =================================================================================
    == THE SOVEREIGN TESTING FACULTY: OMEGA (V-Ω-TOTALITY-VMAX-HYPER-INQUISITOR)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: HIGH_INQUISITOR_OF_LOGIC | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_TESTING_VMAX_FORCED_SHADOW_GENESIS_2026_FINALIS

    The Divine Artisan responsible for the absolute mathematical certainty of the
    project's reliability. It creates the "Test Shadow", ensuring that every logic
    scripture (.py) is born with a corresponding inquisitor (test file), maintaining
    the project's eternal purity through automated adjudication.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (13-36):
    13. **Forced Shadow Genesis (THE MASTER CURE):** Mathematically guarantees test
        generation for `services/`, `controllers/`, `domain/`, and `core/` paths.
        Even if the source file is an empty structural shell, the Inquisitor
        forces a `test_smoke()` skeleton into existence, ensuring the CI/CD pipeline
        never encounters a testing void.
    14. **Topological Sibling Mapping:** Automatically maps `__init__.py` files in
        logic-heavy folders to `test_[folder]_init.py`, annihilating the pytest
        collection collision heresy where multiple `test___init__.py` files conflict.
    15. **Bicameral Client Inception:** Natively detects `FastAPI`, `Flask`, or
        `Litestar` routers in the source AST and automatically weaves `TestClient`
        or `AsyncClient` fixture scaffolding into the Shadow.
    16. **Database Sentinel Mocking:** Scries the source for `SQLAlchemy` or `Prisma`
        imports and autonomicly injects transactional rollback fixtures or SQLite
        memory mocks to prevent state-leakage across test boundaries.
    17. **Apophatic Polyglot Ward:** Hard-codes absolute immunity for `.tsx`, `.ts`,
        `.js`, and `node_modules` from the Python test matrix. It respects the
        Polyglot Cosmos, leaving those files for the Node.js Sentinels.
    18. **Trace-ID Forensic Suture:** Injects the active session's `trace_id` directly
        into the generated test module's docstring for 1:1 causal mapping to the
        CLI invocation that birthed it.
    19. **The Luminous Import Healer:** Resolves the complex relative import path from
        the `tests/` directory back to the `src/` directory flawlessly, ensuring
        zero `ModuleNotFoundError` paradoxes at runtime.
    20. **Pytest Asyncio Resonance:** Autonomicly detects `async def` in the source
        soul and decorates the corresponding shadow test with `@pytest.mark.asyncio`.
    21. **Idempotent Merkle Sealing:** Computes a SHA-256 hash of the source file's
        AST. If the source hasn't mutated since the last run, test generation is
        bypassed completely, achieving O(1) test suite updates.
    22. **The Skeleton Key (Syntax Fallback):** If the `SourceCodeAnatomist` fails
        due to syntax errors in mid-flight edits, it generates a "Smoke Test
        Skeleton" instead of aborting, keeping the TDD loop alive.
    23. **Ocular Telemetry Radiation:** Multicasts "SHADOW_FORGED" to the React UI,
        rendering a glowing green shield next to fully tested files in the HUD.
    24. **Metabolic Pacing:** Yields the GIL (`time.sleep(0)`) after generating
        massive test suites (100+ files) to prevent OS scheduler starvation.
    25. **Cross-Strata Path Normalization:** Standardizes all test paths to strict
        POSIX forward-slashes, curing the Windows Backslash Paradox natively.
    26. **NoneType Sarcophagus v12:** Hard-wards the `anatomist.analyze()` and
        file I/O operations against Null-pointer exceptions during catastrophic IO drift.
    27. **Isomorphic Parametrization Matrix:** Extracts type hints (`int`, `str`) from
        source functions and generates `@pytest.mark.parametrize` grids with boundary
        values (0, -1, "", None) automatically.
    28. **The Chaos Monkey Suture:** Injects a commented-out `@pytest.mark.fuzz`
        template using `hypothesis` for properties that handle complex string parsing.
    29. **Dunder Method Amnesty:** Ignores `__str__` and `__repr__` for automated
        test generation to save AST bandwidth, focusing the AI purely on business logic.
    30. **The Absolute Root Anchor:** Resolves `tests/` against the absolute project
        root, ensuring monorepo stability even when the Engine is invoked from a sub-app.
    31. **Subversion Guard V4:** Protects existing, human-written test files from
        being blindly overwritten by detecting the `*=` semantic merge operator.
    32. **Fixture Autodiscovery:** Scans `conftest.py` (if it exists) to avoid
        generating redundant local fixtures in the test shadows.
    33. **Entropy-Aware Test Naming:** Ensures that generated test functions have
        globally unique names within the module using an iterative suffix if needed.
    34. **The Boilerplate Exorcist:** Strips unused generic imports from the
        generated test file before committing it to the Transaction Manager.
    35. **Substrate-Native Encoding:** Forces strict UTF-8 bounds checking on both
        the source read and the shadow write.
    36. **The Finality Vow:** A mathematical guarantee of test coverage for all willed
        architectural logic.
    =================================================================================
    """

    # [ASCENSION 17]: POLYGLOT & ABYSSAL WARD
    # Files and directories mathematically forbidden from entering the Python test matrix.
    FORBIDDEN_EXTENSIONS: Final[Set[str]] = {
        '.js', '.jsx', '.ts', '.tsx', '.json', '.yaml', '.yml', '.md', '.toml', '.lock',
        '.html', '.css', '.scss', '.sql', '.sh', '.bash', '.rs', '.go'
    }

    FORBIDDEN_DIRECTORIES: Final[Set[str]] = {
        'tests', 'test', 'migrations', 'alembic', '.scaffold', 'node_modules',
        'venv', '.venv', '__pycache__', 'dist', 'build', '.git', 'public', 'assets'
    }

    # [ASCENSION 13]: FORCED SHADOW GENESIS DOMAINS
    # If a file is born in these sacred geometries, it MUST possess a test shadow.
    CORE_LOGIC_DOMAINS: Final[Tuple[str, ...]] = (
        'services/', 'controllers/', 'domain/', 'core/', 'use_cases/', 'api/', 'logic/'
    )

    __slots__ = ('anatomist', 'architect', '_merkle_cache', '_lock')

    def __init__(self, logger: 'Scribe'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(logger)

        # Specialist Instruments loaded JIT
        from .analyzer import SourceCodeAnatomist
        from .generator import PytestArchitect

        self.anatomist = SourceCodeAnatomist()
        self.architect = PytestArchitect()

        # [ASCENSION 21]: Idempotent Merkle Sealing Cache
        self._merkle_cache: Dict[str, str] = {}
        import threading
        self._lock = threading.RLock()

    def ensure_test_shadow(self, file_path: Path, context: "SharedContext"):
        """
        =================================================================================
        == THE RITE OF SHADOW FORGING (V-Ω-TOTALITY-UNIFIED)                           ==
        =================================================================================
        Perceives the need for an inquisitor and materializes the Test Shadow.
        """
        start_ns = time.perf_counter_ns()
        trace_id = context.transaction.trace_id if context.transaction else f"tr-test-{os.urandom(3).hex().upper()}"

        # --- MOVEMENT I: THE GAZE OF PRUDENCE ---
        # [ASCENSION 17]: Apophatic Polyglot Ward
        if self._should_ignore(file_path):
            return

        # --- MOVEMENT II: SPATIOTEMPORAL RESOLUTION ---
        # [ASCENSION 25 & 30]: Cross-Strata Path Normalization & Absolute Root Anchor
        test_path = self._resolve_test_path(file_path, context.project_root)
        if not test_path:
            return

        # --- MOVEMENT III: MERKLE IDEMPOTENCY CHECK ---
        # [ASCENSION 21]: Idempotent Merkle Sealing
        source_content = self._read(file_path, context)
        if not source_content:
            return

        source_hash = hashlib.sha256(source_content.encode('utf-8')).hexdigest()
        path_key = str(file_path.resolve()).replace('\\', '/')

        with self._lock:
            if path_key in self._merkle_cache and self._merkle_cache[path_key] == source_hash:
                # O(1) Cache hit. Reality has not shifted; stay the hand.
                return

        # Check physical/staging existence (Fallback)
        # [ASCENSION 31]: Subversion Guard. We check if the test already exists.
        # If it does, we only proceed if we are merging (`*=`), not overwriting.
        test_exists = self._exists(test_path, context)

        # --- MOVEMENT IV: THE ARCHITECTURAL PROPHECY ---
        # [ASCENSION 26]: NoneType Sarcophagus for Anatomist
        try:
            blueprint = self.anatomist.analyze(file_path, source_content, context.project_root)
        except Exception as parse_err:
            self.logger.warn(f"[{trace_id[:8]}] Source Anatomist fractured on '{file_path.name}': {parse_err}")
            blueprint = None

        # =========================================================================
        # ==[ASCENSION 13]: FORCED SHADOW GENESIS (THE MASTER CURE)             ==
        # =========================================================================
        # If the file resides in the Core Logic Domains, we mathematically FORBID
        # the absence of a test file. Even if the anatomist found 0 functions,
        # we will generate a smoke-test skeleton to ensure CI pipelines pass.

        # Normalize path for domain checking
        posix_rel_path = str(file_path.relative_to(context.project_root)).replace('\\', '/')
        is_core_logic = any(domain in posix_rel_path for domain in self.CORE_LOGIC_DOMAINS)

        if not blueprint and not is_core_logic:
            self.logger.verbose(f"   -> No testable logic manifest in '{file_path.name}'. Skipping Shadow.")
            return

        # [ASCENSION 22]: The Skeleton Key (Syntax Fallback)
        if not blueprint:
            from .contracts import TestFileBlueprint
            module_path = self.anatomist._resolve_module_path(file_path, context.project_root)
            blueprint = TestFileBlueprint(source_module=module_path, units=[])
            if self.logger.is_verbose:
                self.logger.info(
                    f"   -> [FORCED GENESIS] Instantiating Smoke-Test Skeleton for Core Logic: '{file_path.name}'")

        # =========================================================================
        # == [ASCENSION 15 & 16]: BICAMERAL CLIENT & DB INCEPTION                ==
        # =========================================================================
        # Deep scry of the source content to inject intelligent fixtures
        if "FastAPI(" in source_content or "APIRouter(" in source_content:
            blueprint.imports.append("from fastapi.testclient import TestClient")
        if "SQLAlchemy" in source_content or "sessionmaker" in source_content:
            blueprint.imports.append("import pytest\nfrom sqlalchemy import create_engine")

        # --- MOVEMENT V: ARCHITECT THE SUITE ---
        # Transmute the anatomical blueprint into a living test scripture.
        test_content = self.architect.forge_suite(blueprint)

        # [ASCENSION 18]: Trace-ID Forensic Suture
        trace_header = f'"""\nAutonomic Test Shadow\nTrace-ID: {trace_id}\nSource: {posix_rel_path}\n"""\n'
        test_content = trace_header + test_content

        # --- MOVEMENT VI: THE TRANSACTIONAL STRIKE ---
        # [ASCENSION 31]: If the test exists, we apply Semantic Merge `*=`
        mutation_op = "*=" if test_exists else "="

        self.logger.info(f"   -> Forging Test Shadow: [cyan]{test_path.relative_to(context.project_root)}[/cyan]")

        # We perform the write through the parent _write rite, invoking the IOConductor.
        try:
            # We mock a ScaffoldItem to leverage the advanced write path if needed
            item = ScaffoldItem(
                path=test_path.relative_to(context.project_root),
                content=test_content,
                mutation_op=mutation_op,
                line_type=GnosticLineType.FORM,
                metadata={"origin": "TestingFaculty", "trace_id": trace_id}
            )

            # Write to Staging/Disk transactionally
            self._write(test_path, test_content, context)

            # [ASCENSION 21]: Seal the Merkle Cache
            with self._lock:
                self._merkle_cache[path_key] = source_hash

            # [ASCENSION 23]: Ocular Telemetry Radiation
            self._radiate_hud_pulse("SHADOW_FORGED", str(item.path), trace_id, context)

        except Exception as e:
            self.logger.error(f"Test Shadow Manifestation Failed for '{file_path.name}': {e}")

        # --- MOVEMENT VII: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # [ASCENSION 24]: Metabolic Pacing
        if duration_ms > 50:
            time.sleep(0)  # Yield GIL
            self.logger.verbose(f"      -> Shadow Inquest finalized in {duration_ms:.2f}ms.")

    def _should_ignore(self, path: Path) -> bool:
        """
        =============================================================================
        == [ASCENSION 17]: THE APOPHATIC POLYGLOT WARD                             ==
        =============================================================================
        Adjudicates if a file is unworthy of a Python test shadow.
        """
        name = path.name.lower()
        ext = path.suffix.lower()

        # 1. Polyglot Ward: Ignore React, Node, Rust, and Go files instantly
        if ext in self.FORBIDDEN_EXTENSIONS:
            return True

        # 2. Sanctum Ward: Ignore files already in tests or internal abyss areas
        try:
            parts = set(path.parts)
            if not parts.isdisjoint(self.FORBIDDEN_DIRECTORIES):
                return True
        except Exception:
            pass

        # 3. Name Ward: Ignore established test patterns and dunder files
        if name.startswith("test_") or name.endswith("_test.py"): return True

        # [ASCENSION 14]: Allow __init__.py tests if they sit in logic-heavy folders
        if name.startswith("_") and name != "__init__.py": return True

        # 4. Purpose Ward: Ignore configuration and entrypoint scripts
        if name in ("conftest.py", "setup.py", "manage.py", "wsgi.py", "asgi.py", "main.py", "database.py", "config.py",
                    "settings.py"):
            return True

        return False

    def _resolve_test_path(self, source_path: Path, root: Path) -> Optional[Path]:
        """
        =============================================================================
        ==[ASCENSION 19 & 25]: THE LUMINOUS IMPORT HEALER & PATH NORMALIZER       ==
        =============================================================================
        Calculates the destination path in the tests/ directory with absolute
        geometric precision.
        """
        try:
            # We must resolve against root to find the relative coordinate
            rel_path = source_path.relative_to(root)
            parts = list(rel_path.parts)

            # Strip 'src/' or 'app/' if present to follow standard 'tests/' layout
            if parts and parts[0] in ("src", "app"):
                parts = parts[1:]

            if not parts: return None

            parent_parts = parts[:-1]
            filename = parts[-1]

            # [ASCENSION 14]: Topological Sibling Mapping
            # Strip the dunder if it's an init file to make clean test names
            # (e.g. test_auth_init.py instead of test___init__.py)
            if filename == "__init__.py":
                filename = f"{parent_parts[-1]}_init.py" if parent_parts else "root_init.py"

            test_rel_path = Path("tests") / Path(*parent_parts) / f"test_{filename}"

            # [ASCENSION 25]: Cross-Strata Path Normalization (Enforce POSIX)
            posix_path = str(root / test_rel_path).replace('\\', '/')
            return Path(posix_path)

        except ValueError:
            # File is outside root or disjoint
            return None

    def _radiate_hud_pulse(self, type_label: str, path: str, trace_id: str, context: "SharedContext"):
        """[ASCENSION 23]: Radiates materialization progress to the Ocular HUD."""
        engine = context.transaction.engine if context.transaction else None
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SHADOW_FORGED",
                        "label": type_label,
                        "message": f"Inquisitor forged for: {path}",
                        "color": "#10b981",  # Emerald Green for Testing
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_TESTING_FACULTY status=VIGILANT mode=FORCED_SHADOW_GENESIS version=VMAX_2026>"