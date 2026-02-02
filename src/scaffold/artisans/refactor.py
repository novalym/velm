# Path: artisans/refactor.py
# --------------------------

from pathlib import Path
from typing import Dict, Any

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import RefactorRequest
from ..parser_core.parser import parse_structure
from ..utils import atomic_write


@register_artisan("refactor")
class RefactorArtisan(BaseArtisan[RefactorRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF ARCHITECTURAL EVOLUTION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000

    This divine artisan awakens the **Quantum Forge** (`RefactorPad`), a visual Gnostic
    interface for restructuring reality. It has been ascended to become a sentient
    Guardian of the Timeline, ensuring every refactoring rite is safe, idempotent,
    and profoundly intelligent. It has been bestowed with the **Law of Gnostic Trust**,
    annihilating the catastrophic Heresy of the Redundant Gaze for all time.

    ### THE PANTHEON OF 12 LEGENDARY FACULTIES:

    1.  **The Annihilation of the Redundant Gaze:** The profane `_perceive_reality` rite
        has been returned to the void. The Conductor now performs a single, pure Gaze.

    2.  **The Law of Gnostic Trust:** It performs a sacred `adopt` rite to anchor
        reality and then trusts the Gnosis proclaimed by that rite as the one true
        "Before" state. The engine now trusts itself.

    3.  **The Unbreakable Anchor:** Its first act is to summon the `AdoptArtisan`,
        forging a perfect `scaffold.lock` and a pure blueprint of the present.

    4.  **The Gnostic Bridge of Causality:** It correctly captures the `blueprint_content`
        from the `adopt` rite's `ScaffoldResult`, creating an unbreakable Gnostic
        thread between the two artisans.

    5.  **The Hyper-Performant Mind:** By eliminating the second, unveiled scan, its Gaze
        is now instantaneous, annihilating the "18,000 scripture" heresy.

    6.  **The AI Adjudicator Bridge:** Seamlessly loads an AI-generated blueprint
        (`--from-blueprint`) into the "After" pane for visual review and modification.

    7.  **The Unbreakable TUI Summoner:** It performs a shielded, just-in-time import of
        `textual` and the `RefactorPad`, preventing dependency heresies from shattering
        the core engine.

    8.  **The Gnostic Triage:** Intelligently adjudicates the outcome of the TUI session,
        distinguishing between a saved plan, a completed execution, and a stayed rite.

    9.  **The Luminous Voice:** Its every action is proclaimed to the Gnostic Chronicle,
        providing a clear audit trail of its symphony.

    10. **The Unbreakable Ward of Paradox:** Its entire symphony is shielded by `try...except`
        blocks, transmuting any paradox into a luminous `ArtisanHeresy`.

    11. **The Sovereign Soul:** Its purpose is pure orchestration. It contains no UI or
        file-writing logic itself; it delegates these sacred duties.

    12. **The Final Word:** It is the one true, safe, and intelligent gateway to the most
        powerful refactoring engine in the Scaffold cosmos.
    =================================================================================
    """

    def execute(self, request: RefactorRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE GRAND CONDUCTOR OF ARCHITECTURAL EVOLUTION (V-Ω-ETERNAL-APOTHEOSIS)     ==
        =================================================================================
        This is the divine, five-movement symphony that orchestrates the entire rite of
        visual refactoring with absolute, unbreakable Gnostic purity. It has been
        ascended with the Law of Holistic Perception, ensuring no scripture is ever
        annihilated by omission.
        =================================================================================
        """
        self.logger.info("The Architect prepares to reshape reality...")
        target_blueprint_path = (self.project_root / request.blueprint_path).resolve()

        # --- MOVEMENT I: THE RITE OF ANCHORING & HOLISTIC PERCEPTION ---
        self.logger.info("Anchoring current reality and perceiving its complete Gnostic soul...")
        from ..interfaces.requests import AdoptRequest
        from ..artisans.adopt import AdoptArtisan

        adopt_request = AdoptRequest(
            target_path=".",
            # We adopt to a temporary, in-memory name, as the final scripture will be
            # the result of the Pad's session. This keeps the primary blueprint clean.
            output_file=f"__anchor__{request.blueprint_path}",
            project_root=self.project_root,
            force=True,
            non_interactive=True,
            verbosity=-1
        )
        adopt_result = AdoptArtisan(self.engine).execute(adopt_request)
        if not adopt_result.success:
            raise ArtisanHeresy("Failed to anchor reality. The Gnostic Chronicle could not be forged.")
        self.logger.success("Reality anchored. The timeline is pure.")

        # --- MOVEMENT II: THE PERCEPTION OF THE "BEFORE" REALITY (THE LAW OF GNOSTIC TRUST) ---
        self.logger.verbose("Perceiving 'Before' state from the pure Gnosis of the Anchor rite...")

        # We capture the blueprint content of the *entire project* from the adoption rite.
        holistic_blueprint_content = adopt_result.data.get("blueprint_content")
        if not holistic_blueprint_content:
            raise ArtisanHeresy("A paradox occurred: The Anchor rite failed to proclaim its forged scripture.")

        # We now parse this complete scripture to get the true "Before" state.
        _, before_items, _, _, _, _ = parse_structure(
            self.project_root / "__holistic_anchor__.scaffold",
            content_override=holistic_blueprint_content
        )

        # The extraction of meta-gnosis remains a pure rite, now performed on the true target.
        meta_gnosis = self._extract_meta_gnosis(target_blueprint_path)

        # --- MOVEMENT III: THE FORGING OF THE "AFTER" PROPHECY ---
        self.logger.verbose("Forging the initial 'After' prophecy...")
        after_items = [item.model_copy(deep=True) for item in before_items]
        if request.from_blueprint:
            source_path = (self.project_root / request.from_blueprint).resolve()
            if not source_path.exists():
                return self.failure(f"AI prophecy not found: {source_path}")

            self.logger.info(f"Loading AI prophecy from: [cyan]{source_path.name}[/cyan]")
            _, parsed_items, _, _, _, _ = parse_structure(source_path)
            after_items = parsed_items

        # --- MOVEMENT IV: THE SUMMONS OF THE QUANTUM FORGE ---
        self.logger.info("The Quantum Forge awakens. The Architect's Gaze is summoned...")
        try:
            from ..studio.pads.refactor_pad import RefactorPad

            pad = RefactorPad(
                before_items=before_items,
                after_items=after_items,
                meta_gnosis=meta_gnosis,
                project_root=self.project_root,
                engine=self.engine
            )

            final_scripture = pad.run()

            # --- MOVEMENT V: THE GNOSTIC TRIAGE & FINAL PROCLAMATION ---
            if final_scripture is None:
                return self.success("The Refactor Rite was stayed by the Architect.")

            if isinstance(final_scripture, str):
                self.logger.info("Architect chose to 'Save Plan Only'. Inscribing the prophecy...")
                atomic_write(target_blueprint_path, final_scripture, self.logger, self.project_root)
                self.logger.success(f"Refactoring plan inscribed to [cyan]{target_blueprint_path.name}[/cyan].")
                self.console.print(
                    f"To make this reality manifest, speak: [bold]scaffold transmute {request.blueprint_path}[/bold]")

            # If the result is not a string or None, it means the execution happened within the TUI.
            return self.success(
                "The Refactor Rite is complete.",
                data={"path": str(target_blueprint_path)}
            )

        except ImportError as e:
            raise ArtisanHeresy("The RefactorPad requires 'textual'.", suggestion="Speak: `pip install textual`",
                                child_heresy=e)
        except Exception as e:
            raise ArtisanHeresy("The Quantum Forge shattered during the rite.", child_heresy=e)

    def _extract_meta_gnosis(self, path: Path) -> Dict[str, Any]:
        """
        =================================================================================
        == THE META-GNOSIS HARVESTER (V-Ω-ETERNAL. THE KEEPER OF CONTEXT)              ==
        =================================================================================
        Surgically extracts `$$` variables and `%% post-run` commands from a blueprint.
        This ensures that the Architect's high-level logic and context are preserved
        across the refactoring rite, even when the `RefactorPad` itself does not yet
        have a UI to edit them. It is the unbreakable vow of context preservation.
        =================================================================================
        """
        gnosis = {"variables": {}, "commands": [], "edicts": []}
        if path.exists():
            try:
                # We perform a full parse to capture all high-level Gnosis.
                _, _, commands_with_lines, edicts, variables, _ = parse_structure(path)

                gnosis["variables"] = variables
                gnosis["commands"] = commands_with_lines
                gnosis["edicts"] = edicts

                self.logger.verbose(
                    f"Harvested {len(variables)} variables and {len(commands_with_lines)} commands from '{path.name}'.")

            except Exception as e:
                self.logger.warn(f"Could not harvest meta-gnosis from '{path.name}'. Starting fresh. Heresy: {e}")
        return gnosis