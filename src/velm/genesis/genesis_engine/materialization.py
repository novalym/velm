# Path: src/velm/genesis/genesis_engine/materialization.py
# --------------------------------------------------------
# =========================================================================================
# == THE OMEGA MATERIALIZER (V-Ω-TOTALITY-V10000-UNBREAKABLE)                            ==
# =========================================================================================
# LIF: INFINITY | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_SUPREME
# AUTH: Ω_MATERIALIZATION_V10000_GEOMETRIC_SYNC
# =========================================================================================

from __future__ import annotations

import time
import json
import ast
import os
import platform
import hashlib
import gc
from pathlib import Path
from typing import Dict, Any, List, Optional, TYPE_CHECKING, Tuple, Union

from rich.panel import Panel
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from ...core.blueprint_scribe.scribe import BlueprintScribe
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.data_contracts import GnosticArgs, InscriptionAction, GnosticLineType
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
    == THE DIVINE HAND (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                             ==
    =================================================================================
    The physical executor of the Genesis Engine.
    """

    def _write_and_materialize(
            self: 'GenesisEngine',
            final_gnosis: Dict[str, Any],
            gnostic_plan: List['ScaffoldItem'],
            post_run_commands: List[Any],
            parser: 'ApotheosisParser'
    ) -> 'QuantumRegisters':
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC MANIFESTATION (V-Ω-TOTALITY-V10000)               ==
        =================================================================================
        LIF: INFINITY | ANNIHILATES: [VOID MANIFEST], [ROOT SCHISM], [STAGING GHOSTS]
        =================================================================================
        """
        self.logger.info("Initiating the Rite of Materialization...")

        # [FACULTY 0] THE GNOSTIC WARD OF PURITY
        if not isinstance(final_gnosis, dict):
            raise ArtisanHeresy("Genesis Paradox: Gnostic Dowry is profane.")

        # --- MOVEMENT I: THE MENTOR'S GAZE ---
        if not getattr(self.cli_args, 'preview', False) and not getattr(self.cli_args, 'dry_run', False):
            self._conduct_mentor_guidance(final_gnosis)

        # --- MOVEMENT II: THE TRANSACTIONAL ADOPTION (THE CURE) ---
        # [ASCENSION 1]: We scry for an existing transaction womb.
        # This prevents the 'Staging Void' heresy by working within the Architect's portal.
        master_tx = getattr(self, 'transaction', None)

        project_slug = final_gnosis.get('project_slug', 'new-project')
        tx_name = f"Genesis: {final_gnosis.get('project_name', project_slug)}"
        is_simulation = getattr(self.cli_args, 'dry_run', False) or getattr(self.cli_args, 'preview', False)

        # [THE TRINITY NORMALIZER]
        normalized_commands = self._normalize_post_run_commands(post_run_commands)

        if master_tx:
            self.logger.verbose(f"Lattice Sync: Adopting Master Transaction '{master_tx.tx_id[:8]}'.")
            return self._conduct_materialization_rite(
                final_gnosis, gnostic_plan, normalized_commands, parser, master_tx, is_simulation
            )
        else:
            # Fallback for direct Engine usage
            self.logger.warn("No master transaction manifest. Forging a temporary reality.")
            from ...core.kernel.transaction import GnosticTransaction
            # Default to root for the BP if no sub-transaction is willed
            blueprint_path = self.project_root / "scaffold.scaffold"
            with GnosticTransaction(self.project_root, tx_name, blueprint_path, use_lock=True,
                                    simulate=is_simulation) as tx:
                self.transaction = tx
                return self._conduct_materialization_rite(
                    final_gnosis, gnostic_plan, normalized_commands, parser, tx, is_simulation
                )

    def _conduct_materialization_rite(
            self: 'GenesisEngine',
            final_gnosis: Dict[str, Any],
            gnostic_plan: List['ScaffoldItem'],
            normalized_commands: List[Tuple],
            parser: 'ApotheosisParser',
            tx: 'GnosticTransaction',
            is_simulation: bool
    ) -> 'QuantumRegisters':
        """
        The internal core of the materialization symphony.
        """
        from ...creator import create_structure

        # [ASCENSION 6]: Direct-Object Injection
        gnostic_passport = GnosticArgs.from_namespace(self.cli_args)

        # --- MOVEMENT IV: THE RITE OF CREATION ---
        # We bestow the complete plan upon the Creator.
        # This populates the staging area.
        registers = create_structure(
            scaffold_items=gnostic_plan,
            base_path=self.project_root,
            post_run_commands=normalized_commands,
            pre_resolved_vars=final_gnosis,
            args=gnostic_passport,
            transaction=tx
        )

        # [ASCENSION 2]: ITEM SUTURE
        self.items = gnostic_plan
        self.post_run_commands = normalized_commands

        if not is_simulation:
            # --- MOVEMENT V: THE GEOMETRIC SYNC (THE CURE) ---
            # [ASCENSION 12]: We scry the 'registers' to find where the creator
            # ACTUALLY put the files (respecting the Root Folding).
            actual_form_root = registers.logical_root
            self.logger.verbose(f"Geometric Sync: Creator anchored reality at [dim]{actual_form_root}[/dim]")

            # --- MOVEMENT VI: THE ENRICHMENT ---
            self._forge_devcontainer_scripture(actual_form_root, tx, final_gnosis)
            self._ensure_license_presence(actual_form_root, tx, final_gnosis)

            # [ASCENSION 3]: ATOMIC BLUEPRINT ETCHING
            # We inscribe the blueprint into the SAME root the files landed in.
            self._inscribe_chronicle_blueprint_surgical(
                target_root=actual_form_root,
                items=gnostic_plan,
                commands=normalized_commands,
                gnosis=final_gnosis,
                tx=tx
            )

            # [ASCENSION 10]: ADJUDICATION
            if hasattr(self, 'adjudicator'):
                self.adjudicator.conduct_dynamic_ignore()

        return registers

    # =============================================================================
    # == INTERNAL FACULTIES                                                      ==
    # =============================================================================

    def _normalize_post_run_commands(self, commands: List[Any]) -> List[Tuple[str, int, Optional[List[str]]]]:
        """[THE CURE]: Guarantees the Sacred Trinity."""
        normalized = []
        for cmd in commands:
            if isinstance(cmd, tuple):
                if len(cmd) == 3:
                    normalized.append(cmd)
                elif len(cmd) == 2:
                    normalized.append((cmd[0], cmd[1], None))
                else:
                    normalized.append((str(cmd[0]), 0, None))
            elif isinstance(cmd, str):
                normalized.append((cmd, 0, None))
        return normalized

    def _inscribe_chronicle_blueprint_surgical(self, target_root: Path, items: List[ScaffoldItem],
                                               commands: List[Tuple], gnosis: Dict,
                                               tx: GnosticTransaction):
        """
        [ASCENSION 12]: THE SURGICAL SCRIBE.
        Etches the blueprint directly into the staging area at the correct anchor.
        """
        self.logger.info("The Architect's Scribe is chronicling the Great Work...")

        try:
            # 1. Materialize the content
            scribe = BlueprintScribe(project_root=self.project_root, alchemist=self.alchemist)
            blueprint_content = scribe.transcribe(
                items=items,
                commands=commands,
                gnosis=gnosis,
                rite_type='genesis'
            )

            # 2. Coordinate Resolution
            # We must target the Logical Root within the transaction.
            target_bp_path = target_root / "scaffold.scaffold"

            # [THE CURE]: If the target_root is absolute (which it is from registers),
            # we must ensure atomic_write treats it as relative to the sanctum
            # OR use the transaction's staging resolver.

            # 3. Atomic Inscription to Staging
            atomic_write(
                target_path=target_bp_path,
                content=blueprint_content,
                logger=self.logger,
                sanctum=self.project_root,
                transaction=tx
            )

            self.logger.success(f"Sacred Blueprint manifest at: [dim]{target_bp_path.name}[/dim]")

        except Exception as e:
            self.logger.error(f"Scribe Fracture: Failed to chronicle: {e}")

    def _forge_devcontainer_scripture(self, project_root: Path, tx: GnosticTransaction, gnosis: Dict[str, Any]):
        """[ASCENSION 9] The DevContainer Foundry."""
        if not gnosis.get('use_vscode') and not gnosis.get('use_devcontainer'):
            return

        config = {
            "name": gnosis.get('project_name', project_root.name),
            "image": "mcr.microsoft.com/devcontainers/python:3.12",
            "customizations": {
                "vscode": {
                    "settings": {"editor.formatOnSave": True, "python.analysis.typeCheckingMode": "basic"},
                    "extensions": ["ms-python.python", "charliermarsh.ruff", "GitHub.copilot"]
                }
            },
            "features": {"ghcr.io/devcontainers/features/docker-in-docker:2": {}}
        }

        atomic_write(
            target_path=project_root / ".devcontainer" / "devcontainer.json",
            content=json.dumps(config, indent=4),
            logger=self.logger,
            sanctum=self.project_root,
            transaction=tx
        )

    def _ensure_license_presence(self, root: Path, tx: GnosticTransaction, gnosis: Dict):
        """Ensures the legal soul is manifest."""
        license_type = gnosis.get('license')
        if not license_type or license_type.lower() == 'none': return

        content = f"{license_type} License\n\nCopyright (c) {time.strftime('%Y')} {gnosis.get('author', 'The Architect')}\n"
        atomic_write(root / "LICENSE", content, self.logger, self.project_root, transaction=tx)

    def _conduct_mentor_guidance(self, gnosis: Dict):
        """Consults the laws of existence to provide architectural guidance."""
        try:
            from ...jurisprudence_core.genesis_jurisprudence import GENESIS_CODEX
            for law in GENESIS_CODEX:
                if law.validator(gnosis):
                    msg = law.message(gnosis) if callable(law.message) else law.message
                    self.console.print(Panel(msg, title=f"Mentor: {law.title}", border_style="yellow"))
        except Exception:
            pass

# == SCRIPTURE SEALED: THE MATERIALIZATION SINGULARITY IS OMEGA ==