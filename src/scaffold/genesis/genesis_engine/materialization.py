# Path: scaffold/genesis/genesis_engine/materialization.py
# --------------------------------------------------------


from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, Any, List, Optional, TYPE_CHECKING, Tuple

from rich.panel import Panel
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from ...core.blueprint_scribe import BlueprintScribe
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.data_contracts import GnosticArgs
from ...utils import atomic_write

if TYPE_CHECKING:
    from .engine import GenesisEngine
    from ...contracts.data_contracts import ScaffoldItem
    from ...parser_core.parser.engine import ApotheosisParser
    from ...creator import QuantumRegisters
    from ...core.kernel.transaction import GnosticTransaction

Logger = Scribe("GenesisMaterialization")


class MaterializationMixin:
    """
    =================================================================================
    == THE FORGE OF GENESIS (V-Ω-ETERNAL-APOTHEOSIS. THE HEALED MENTOR)            ==
    =================================================================================
    The divine Hand of the Genesis Engine.
    """

    def parser_factory(self: 'GenesisEngine') -> 'ApotheosisParser':
        """A divine factory to summon a pure Parser, preventing circular Gnosis."""
        from ...parser_core.parser import ApotheosisParser
        return ApotheosisParser()

    def _write_and_materialize(
            self: 'GenesisEngine',
            final_gnosis: Dict[str, Any],
            gnostic_plan: List['ScaffoldItem'],
            post_run_commands: List[Tuple[str, int, Optional[List[str]]]],
            parser: 'ApotheosisParser'
    ) -> 'QuantumRegisters':
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC MANIFESTATION (V-Ω-TRINITY-AWARE-HEALED)          ==
        =================================================================================
        """
        # [FACULTY 0] THE GNOSTIC WARD OF PURITY
        if not isinstance(final_gnosis, dict):
            raise ArtisanHeresy(
                f"Genesis Paradox: The Gnostic Dowry is profane. Expected Dict, received {type(final_gnosis).__name__}.",
                severity=HeresySeverity.CRITICAL
            )

        # --- MOVEMENT I: THE MENTOR'S GAZE (GUIDANCE) ---
        if not self.cli_args.preview and not self.cli_args.audit and not self.cli_args.dry_run:
            from ...jurisprudence_core.genesis_jurisprudence import GENESIS_CODEX

            for law in GENESIS_CODEX:
                try:
                    if law.validator(final_gnosis):
                        raw_msg = law.message(final_gnosis) if callable(law.message) else law.message
                        raw_sug = law.suggestion(final_gnosis) if callable(law.suggestion) else law.suggestion
                        proclamation = Text.from_markup(
                            f"{raw_msg}\n\n[dim]Suggestion:[/dim] [green]{raw_sug or 'None'}[/green]")
                        self.console.print(Panel(
                            proclamation,
                            title=f"[yellow]Mentor's Guidance: {law.title}[/yellow]",
                            border_style="yellow"
                        ))
                except Exception as e:
                    Logger.warn(f"The Mentor stumbled on law '{law.key}': {e}")

        # --- MOVEMENT II: THE INQUISITOR'S AUDIT ---
        # [[[ THE DIVINE HEALING: THE RITE OF PURIFICATION ]]]
        # We ensure we only judge items that have a path.
        pure_form_plan = [item for item in gnostic_plan if item.path is not None]

        if not pure_form_plan:
            self.logger.warn("The Gnostic Gaze perceived a void. The final plan is pure of form.")
            from ...creator.registers import QuantumRegisters
            from ...core.sanctum.local import LocalSanctum

            # [FIX] THE ANCHOR OF THE VOID
            return QuantumRegisters(
                sanctum=LocalSanctum(self.project_root),
                transaction=None,
                gnosis=final_gnosis,
                project_root=self.project_root
            )
        else:
            self.logger.info("Awakening the Gnostic Mentor for a final architectural inquest...")
            from ...jurisprudence_core.jurisprudence import conduct_architectural_inquest

            lint_panels = conduct_architectural_inquest(pure_form_plan)
            if lint_panels and not self.cli_args.silent:
                self.console.rule("[bold yellow]Gnostic Mentor's Final Adjudication[/bold yellow]", style="yellow")
                for panel in lint_panels: self.console.print(panel)

        # --- MOVEMENT III: THE BLUEPRINT CHRONICLE ---
        self.logger.info("The Architect's Scribe awakens to chronicle the Great Work...")

        project_slug = final_gnosis.get('project_slug', 'new-project')
        chronicle_path = self.project_root / project_slug / "scaffold.scaffold"

        try:
            scribe = BlueprintScribe(project_root=self.project_root, alchemist=self.alchemist)

            # [FACULTY 1] THE DIVINE ADAPTER: Transmute Trinity to Duality
            scribe_commands = [(cmd, line) for cmd, line, _ in post_run_commands]

            final_scripture = scribe.transcribe(
                items=gnostic_plan,
                commands=scribe_commands,
                gnosis=final_gnosis,
                rite_type='genesis'
            )

            if not self.cli_args.dry_run and not self.cli_args.preview and not self.cli_args.audit:
                chronicle_path.parent.mkdir(exist_ok=True, parents=True)
                atomic_write(chronicle_path, final_scripture, self.logger, self.project_root)
                self.logger.success("The sacred `scaffold.scaffold` chronicle has been forged.")
            else:
                self.logger.info("Simulation Mode: Blueprint chronicle generation verified but not written.")

        except Exception as e:
            self.logger.warn(f"A minor paradox occurred while chronicling the genesis rite: {e}")

        # --- MOVEMENT IV: THE TRANSACTIONAL MANIFESTATION ---
        from ...creator import create_structure
        from ...core.kernel.transaction import GnosticTransaction

        try:
            tx_name = f"Genesis: {final_gnosis.get('project_name', project_slug)}"
            is_simulation = self.cli_args.dry_run or self.cli_args.preview or self.cli_args.audit

            # [THE HEALING] We transmute the Namespace to GnosticArgs here
            gnostic_passport = GnosticArgs.from_namespace(self.cli_args)

            def invoke_quantum_creator(tx: Optional[GnosticTransaction] = None) -> 'QuantumRegisters':
                # [THE APOTHEOSIS] We pass the GnosticArgs object
                return create_structure(
                    scaffold_items=gnostic_plan,
                    base_path=self.project_root,
                    post_run_commands=post_run_commands,
                    pre_resolved_vars=final_gnosis,
                    args=gnostic_passport,  # Pass the transmuted object
                    transaction=tx
                )

            if is_simulation:
                return invoke_quantum_creator(None)
            else:
                # We target the project root for the transaction lock
                with GnosticTransaction(self.project_root, tx_name, chronicle_path, use_lock=True) as tx:

                    # [THE FIX] BIND THE TRANSACTION TO THE ENGINE INSTANCE
                    # This enables the GnosticAdjudicator (self.adjudicator) to perceive the write dossier.
                    self.transaction = tx

                    try:
                        # 1. Materialize
                        registers = invoke_quantum_creator(tx)

                        # 2. Post-Flight Rites (Inside Transaction for safety)
                        # [FACULTY 11] DevContainer
                        self._forge_devcontainer_scripture(self.project_root / project_slug, tx, final_gnosis)

                        # [FACULTY 9] Dynamic Ignore
                        self.adjudicator.conduct_dynamic_ignore()

                    finally:
                        # Release the binding to keep the engine stateless between runs
                        self.transaction = None

                    return registers

        except ArtisanHeresy:
            raise
        except Exception as e:
            raise ArtisanHeresy(
                "A catastrophic paradox occurred during the final Rite of Materialization.",
                child_heresy=e
            ) from e

    # --- INTERNAL FACULTIES ---

    def _forge_devcontainer_scripture(self, project_root: Path, tx: GnosticTransaction, gnosis: Dict[str, Any]):
        """
        [FACULTY 11] THE DEVCONTAINER FOUNDRY (V-Ω-ENVIRONMENTAL-GNOSIS)
        Analyzes the final Gnosis to forge a `.devcontainer.json` file.
        """
        if not gnosis.get('use_vscode') and not gnosis.get('use_devcontainer'):
            return

        devcontainer_dir = project_root / ".devcontainer"
        devcontainer_json_path = devcontainer_dir / "devcontainer.json"

        if devcontainer_json_path.exists():
            return

        self.logger.verbose("The DevContainer Foundry awakens...")

        project_type = gnosis.get('project_type', 'generic')
        db_type = gnosis.get('database_type', 'none')

        config = {
            "name": gnosis.get('project_name', project_root.name),
            "image": f"mcr.microsoft.com/devcontainers/{'python:3' if 'python' in project_type else 'javascript-node:18'}",
            "customizations": {
                "vscode": {
                    "extensions": ["ms-python.python"] if 'python' in project_type else ["dbaeumer.vscode-eslint"]
                }
            }
        }

        # Database integration hint
        if db_type in ['postgres', 'mysql']:
            config['features'] = {
                "ghcr.io/devcontainers/features/docker-in-docker:2": {}
            }

        import json
        content = json.dumps(config, indent=4)

        # Inscribe within transaction
        atomic_write(devcontainer_json_path, content, self.logger, self.project_root, transaction=tx)
        self.logger.success("DevContainer scripture forged.")