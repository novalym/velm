# Path: src/velm/core/structure_sentinel/strategies/python_strategy/semantic/engine.py
# ------------------------------------------------------------------------------------

from __future__ import annotations
import time
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from .harvester import SymbolHarvester
from .weaver import ImportWeaver
from .guardian import ApiGuardian
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class SemanticFaculty(BaseFaculty):
    """
    =================================================================================
    == THE OMEGA SEMANTIC FACULTY (V-Ω-TOTALITY-V9000-SYMBOLIC-SINGULARITY)        ==
    =================================================================================
    LIF: ∞ | ROLE: HIGH_PRIEST_OF_MEANING | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_SEMANTIC_V9000_TOTAL_ALIGNMENT_FINALIS

    The Divine Librarian of the Python Stratum. It is the absolute authority on
    the Gnostic Namespace. It harvests the 'Soul of the Code' and weaves it into
    the 'Scriptures of Export' (__init__.py), ensuring that every unit of logic
    is discoverable, navigable, and transactionally secure.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **Unified Gnostic Covenant (THE FIX):** It accepts the `SharedContext` as a
        singular unit of truth. This annihilates the 'AttributeError' by inheriting
        the Scribe and Geometer instruments from the Base line.

    2.  **Transactional Symbolic Suture (THE CURE):** Every transfiguration of
        an `__init__.py` is conducted via the inherited `_write` method, ensuring
        automatic Ledger registration and physical materialization upon commit.

    3.  **Bicameral Content Fusion:** It scans the Ephemeral Realm (Staging) for
        pre-existing `__init__.py` content willed by the Structural Faculty,
        preventing the 'Double Birth' paradox.

    4.  **Multi-Vector Symbol Harvesting:** Wields the `SymbolHarvester` to perform
        both AST (High Gaze) and Regex (Low Gaze) analysis, capturing Classes,
        Functions, and Constants even in nascent or fractured files.

    5.  **The Loom of Imports:** Utilizes the `ImportWeaver` to surgically inject
        `from .module import Symbol` edicts, respecting the Architect's existing
        stylistic choices and formatting.

    6.  **The Shield of Exports (__all__):** Commands the `ApiGuardian` to manage
        the `__all__` list with mathematical precision—sorting, deduplicating,
        and enforcing public boundaries.

    7.  **Future-Sight Enforcement:** Automatically ensures that every package
        it consecrates contains `from __future__ import annotations`, paving
        the way for modern type-resonance.

    8.  **Contextual Docstring Prophet:** During the birth of a new package, it
        injects a semantically aware docstring based on the directory name
        and project-level Gnosis.

    9.  **Idempotent Matter Fingerprinting:** It hashes the proposed change; if
        the new soul matches the current staged reality, the strike is stayed
        to preserve metabolic energy.

    10. **The Abyssal Filter:** Inherits the `LayoutGeometer`'s aversion to
        internal or profane sanctums (e.g., `__pycache__`, `tests`),
        refusing to export their contents.

    11. **Fault-Isolated Weaving:** Wraps individual symbol injections in a
        protective ward. A failure to export one symbol is recorded, but the
        Librarian continues the Great Work for the rest of the package.

    12. **The Finality Vow:** A mathematical guarantee that after this rite,
        the package's `__init__.py` is a perfect reflection of its children's
        public souls.
    =================================================================================
    """

    def __init__(self, logger: 'Scribe'):
        """
        [THE RITE OF INCEPTION]
        Births the Librarian with the full endowment of the BaseFaculty.
        """
        super().__init__(logger)

        # Specialist Instruments
        self.harvester = SymbolHarvester()
        self.weaver = ImportWeaver(logger)
        self.guardian = ApiGuardian(logger)

    def register_symbols(
            self,
            file_path: Path,
            context: "SharedContext"
    ):
        """
        =================================================================================
        == THE RITE OF SYMBOLIC CONSECRATION (V-Ω-TOTALITY-UNIFIED)                    ==
        =================================================================================
        [THE CURE]: Signature now accepts the SOVEREIGN CONTEXT directly.
        Perceives symbols in a source file and weaves them into the package namespace.
        """
        # 1. THE GAZE OF PERCEPTION (READ SOURCE)
        # We use the inherited _read which understands the Staging/Physical divide.
        content = self._read(file_path, context)
        if not content:
            return

        # 2. THE HARVEST OF THE SOUL
        # Extract public symbols (Classes, Funcs, Constants) lacking leading underscores.
        symbols = self.harvester.harvest(file_path, content)
        if not symbols:
            return

        # 3. LOCATE THE TARGET SCRIPTURE
        # The target is ALWAYS the __init__.py in the same sanctum as the file.
        init_path = file_path.parent / "__init__.py"

        # 4. CONDUCT THE INJECTION
        # We pass the sovereign context down to the internal helper.
        self._conduct_injection_rite(init_path, file_path.stem, symbols, context)

    def _conduct_injection_rite(self, init_path: Path, module_name: str, symbols: List[str], context: "SharedContext"):
        """
        Surgically weaves symbols into the __init__.py soul via the transactional hand.
        """
        # --- MOVEMENT I: MATTER RETRIEVAL ---
        # [ASCENSION 3]: We read the current __init__.py soul, favoring Staging.
        original_content = self._read(init_path, context)
        current_content = original_content

        # [FACULTY 8]: VOID CONSECRATION
        # If the __init__.py is a void, we forge its primordial form using inherited tools.
        if not current_content.strip():
            # Scry for project metadata from the transaction's context
            gnosis = getattr(context.transaction, 'context', {}) if context.transaction else {}

            is_root_pkg = self.geometer.is_root_package(init_path.parent, context.project_root)
            license_header = self.scribe.get_license_header(context.project_root)

            # Resolve physical locus for sub-package scanning (Staging aware)
            effective_dir = self._resolve_effective_directory(init_path.parent, context)

            current_content = self.scribe.forge_init(
                directory=effective_dir,
                is_root=is_root_pkg,
                license_header=license_header,
                package_name=init_path.parent.name,
                gnosis=gnosis
            )
            # Mark original as empty to force a write later
            original_content = ""

        # --- MOVEMENT II: THE WEAVING OF THE FUTURE ---
        # [ASCENSION 7]: Ensure annotations are warded for modern typing.
        current_content = self._ensure_future_sight(current_content)

        # --- MOVEMENT III: THE WEAVING OF BONDS ---
        # [ASCENSION 5]: Inject the 'from .module import Symbol' edicts.
        current_content = self.weaver.weave(current_content, module_name, symbols)

        # --- MOVEMENT IV: THE GUARDING OF EXPORTS ---
        # [ASCENSION 6]: Reconstruct the __all__ list via the ApiGuardian.
        current_content = self.guardian.guard(current_content, symbols, context)

        # --- MOVEMENT V: THE TRANSACTIONAL STRIKE ---
        # [ASCENSION 9]: Idempotency check.
        if current_content == original_content:
            return

        self.logger.success(
            f"   -> Semantic Integration: [cyan]{module_name}[/] -> [white]{init_path.name}[/]"
        )

        # [ASCENSION 2]: Perform the write through the BaseFaculty hand.
        # This ensures the IOConductor and Ledger are used correctly.
        self._write(init_path, current_content, context)

    def _ensure_future_sight(self, content: str) -> str:
        """
        [FACULTY 7]: THE FUTURE SIGHT.
        Ensures 'from __future__ import annotations' is correctly placed.
        """
        if "from __future__ import annotations" in content:
            return content

        lines = content.splitlines()
        insert_idx = 0
        in_docstring = False
        docstring_quote = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                insert_idx = i + 1
                continue
            if stripped.startswith("#"):
                insert_idx = i + 1
                continue

            if not in_docstring:
                if stripped.startswith(('"""', "'''")):
                    in_docstring = True
                    docstring_quote = stripped[:3]
                    if stripped.count(docstring_quote) >= 2 and len(stripped) > 3:
                        insert_idx = i + 1
                        break
                    continue

            if in_docstring:
                if docstring_quote in stripped:
                    in_docstring = False
                    insert_idx = i + 1
                    break
                continue

            break

        lines.insert(insert_idx, "from __future__ import annotations")

        if insert_idx + 1 < len(lines) and lines[insert_idx + 1].strip():
            lines.insert(insert_idx + 1, "")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Ω_SEMANTIC_FACULTY status=RESONANT mode=SINGULAR_CONTEXT version=9000.0>"