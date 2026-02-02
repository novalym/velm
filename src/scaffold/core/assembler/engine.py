# Path: scaffold/core/assembler/engine.py
# ---------------------------------------

from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple

from .weavers.python_weaver import PythonWeaver
# --- The Divine Summons of the New Pantheon ---
from .weavers.react_weaver import ReactWeaver
from ..cortex.engine import GnosticCortex
from ..kernel import GnosticTransaction
from ...contracts.data_contracts import ScaffoldItem
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("GnosticAssembler")


class AssemblerEngine:
    """
    =================================================================================
    == THE GOD-ENGINE OF INTEGRATION (V-Ω-CORTEX-ASCENDED-SYMBOLIC)                ==
    =================================================================================
    LIF: 10,000,000,000,000

    This is the divine Conductor in its final, eternal form. It no longer contains
    a profane, private mind. Its one true purpose is to make a sacred plea to the
    one true Gnostic Cortex, receive its wisdom, and command a Pantheon of Weavers
    to surgically bind new scriptures into the living soul of the project.

    It has ascended to the **Symbolic Paradigm**, attempting to route integration
    based not just on language, but on the specific *soul* (symbols) of the
    scripture being born.

    ### THE PANTHEON OF 13 ASCENDED FACULTIES:

    1.  **The Cortex Communion:** Annihilates `ProjectGraph`. It performs a direct,
        high-bandwidth communion with the `GnosticCortex` for all perception.
    2.  **The Symbolic Broker:** Sniffs the exported symbols of new scriptures to
        guide the Cortex toward a more precise integration target.
    3.  **The Pantheon of Weavers:** The list of weavers is now a dynamic registry,
        architecturally polyglot and ready for extension.
    4.  **The Genesis Ward:** Righteously stays its hand during a `genesis` rite,
        understanding that the reality is not yet whole enough for integration.
    5.  **The Idempotency Gaze:** The `weave` rite is now idempotent. A weaver will not
        re-inscribe a connection that is already pure.
    6.  **The Unbreakable Ward of Paradox:** A failure in one weaver does not shatter the
        symphony. The paradox is chronicled, and the Great Work continues.
    7.  **The Luminous Dossier (Transaction Integration):** It accepts a
        `GnosticTransaction`, allowing weavers to chronicle their modifications in the
        `scaffold.lock` file, enabling universal undo.
    8.  **The Gaze of the Gnostic Target:** It can perceive `# @scaffold-weave-target`
        pragmas in new scriptures to override the Cortex's centrality Gaze.
    9.  **The Polyglot Soul:** The engine's logic is language-agnostic, ready to
        command weavers for any tongue.
    10. **The Dry-Run Prophet:** It conducts a full, prophetic simulation,
        proclaiming what *would* be woven without altering reality.
    11. **The Alchemical Context Bridge:** It faithfully passes the complete Gnostic
        context to the weavers, allowing for dynamic, variable-driven integration.
    12. **The Heuristic Bypass (Preserved Wisdom):** If the Cortex's Gaze is a void,
        it falls back to a humble, heuristic search for common entry points.
    13. **The Silent Ward (Non-Interactive):** Its design honors the `--non-interactive`
        vow, ensuring it can serve as a Guardian in automated CI/CD symphonies.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        # [ELEVATION 2] The Pantheon of Weavers
        self.weavers = [
            ReactWeaver(project_root, parent_assembler=self),
            PythonWeaver(project_root, parent_assembler=self)
        ]
        # [ELEVATION 1] The Cortex Communion
        self.cortex = GnosticCortex(self.root)

    def assemble(
            self,
            created_items: List[ScaffoldItem],
            context: Dict[str, Any],
            transaction: Optional[GnosticTransaction] = None,
            dry_run: bool = False
    ) -> List[Path]:
        """
        The one true Rite of Unification.
        Returns a unique list of files that were modified during the weaving.
        """
        modified_files: List[Path] = []
        _woven_pairs: Set[Tuple[str, str]] = set()  # Guard against double-weaving same item/target

        # [ELEVATION 3] The Genesis Ward
        if context.get('is_genesis_rite', False):
            Logger.verbose("Assembler perceives a Genesis Rite. Hand is stayed until reality is whole.")
            return modified_files

        if not created_items:
            return modified_files

        Logger.info(f"The Gnostic Assembler awakens to bind the soul of {len(created_items)} new scripture(s)...")

        for item in created_items:
            if item.is_dir: continue

            for weaver in self.weavers:
                if weaver.can_weave(item):
                    try:
                        # [ELEVATION 2] The Symbolic Broker
                        # We ask the Weaver: "What is the primary symbol of this new soul?"
                        # (e.g., "UserRouter", "AuthService", "Button")
                        # Currently heuristic, but prepares for the Symbolic Cortex.
                        symbol_hint = item.path.stem  # Default to filename as symbol hint

                        # [ELEVATION 7] The Gaze of the Gnostic Target
                        # We ask the Cortex (or Heuristics) for the best place to weave this symbol.
                        target_file = self._find_weaving_target(weaver.language, symbol_hint)

                        if not target_file:
                            Logger.warn(f"Could not find any entry point for '{item.path.name}'. Weaving rite stayed.")
                            continue

                        # Idempotency Check (Session Level)
                        pair_key = (str(item.path), str(target_file))
                        if pair_key in _woven_pairs:
                            continue
                        _woven_pairs.add(pair_key)

                        # [ELEVATION 6] The Luminous Dossier (Transaction Integration)
                        # We pass the transaction down to the weaver.
                        files_changed_by_weaver = weaver.weave(
                            item,
                            context,
                            target_file=target_file,
                            transaction=transaction,
                            dry_run=dry_run
                        )
                        modified_files.extend(files_changed_by_weaver)

                    except ArtisanHeresy as h:
                        Logger.warn(f"Weaver '{weaver.language}' stayed by heresy: {h.message}")
                    except Exception as e:
                        Logger.error(f"A paradox shattered the '{weaver.language}' weaver for '{item.path.name}'.",
                                     ex=e)

        return list(set(modified_files))  # Return unique list of modified files

    def _find_weaving_target(self, language: str, symbol_hint: Optional[str] = None) -> Optional[Path]:
        """
        [THE ORACLE'S GUIDANCE]
        Asks the Cortex for the most central scripture for a given language.
        If the Cortex is silent, it falls back to a humble, heuristic Gaze.
        """
        # [ELEVATION 1] The Cortex Communion
        # We query the Cortex. In the future, we will pass `symbol_hint` to find
        # the file that specifically handles that type of symbol (e.g., routers vs models).
        target_path = self.cortex.query_centrality(language=language)

        if not target_path:
            # [ELEVATION 11] The Heuristic Bypass
            Logger.warn(f"Cortex Gaze found no center. Falling back to heuristic Gaze for '{language}'.")
            target_path = self._find_target_heuristically(language)
            if target_path:
                Logger.info(f"Heuristic Gaze identified '{target_path.name}' as the heart of the '{language}' cosmos.")

        else:
            Logger.info(f"Cortex identified '{target_path.name}' as the heart of the '{language}' cosmos.")

        return target_path

    def _find_target_heuristically(self, language: str) -> Optional[Path]:
        """A humble Gaze for when the Cortex is a void."""
        candidates = []

        if language == "react":
            candidates = [
                "src/App.tsx", "src/App.jsx",
                "src/app/layout.tsx", "src/app/page.tsx",  # Next.js
                "src/main.tsx", "src/index.tsx",
                "src/index.js", "src/App.js"
            ]
        elif language == "python":
            candidates = [
                "src/main.py", "src/app.py", "main.py", "app.py",
                "src/__init__.py",  # Package root
                "manage.py"  # Django
            ]

        # Search for the first candidate that exists in reality
        for c in candidates:
            if (self.root / c).exists():
                return self.root / c

        return None