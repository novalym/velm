# Path: src/velm/creator/engine/adjudicator.py
# --------------------------------------------

import time
import threading
from pathlib import Path
from typing import Set, TYPE_CHECKING, Any, Union, List, Optional

# --- THE DIVINE UPLINKS ---
from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ...contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ...logger import Scribe, get_console
from ...core.runtime.middleware.output_veil import OutputRedactionMiddleware

if TYPE_CHECKING:
    from .facade import QuantumCreator
    from ...genesis.genesis_engine.engine import GenesisEngine

Logger = Scribe("GnosticAdjudicator")


class GnosticAdjudicator:
    """
    =================================================================================
    == THE GNOSTIC ADJUDICATOR (V-Ω-TOTALITY-V505-TRANSACTIONAL-VEIL)              ==
    =================================================================================
    LIF: ∞ | ROLE: CONSCIENCE_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ADJUDICATOR_V505_STABLE

    The supreme authority on reality validation. It ensures that the manifest
    world aligns with the Laws of Architecture and the Vows of Security.
    """

    def __init__(self, creator: Union['QuantumCreator', 'GenesisEngine', Any]):
        """The Rite of Inception. Binds the Conscience to the Engine."""
        self.creator = creator
        self.console = get_console()
        self._lock = threading.RLock()
        self.logger = Logger

        # [THE CURE]: DUAL-AXIS ENGINE DISCOVERY
        # We search both the creator's explicit engine link AND the internal_engine fallback.
        # This guarantees the Middleware receives a valid soul.
        active_engine = (
                getattr(creator, 'engine', None) or
                getattr(creator, 'internal_engine', None) or
                (creator.engine if hasattr(creator, 'engine') else None)
        )

        # [ASCENSION 3]: Summon the Sentinel for Entropy Detection
        self.privacy_sentinel = OutputRedactionMiddleware(active_engine)

    def conduct_sentinel_inquest(self):
        """
        =============================================================================
        == THE RITE OF SENTINEL INQUEST (V-Ω-STAGING-AWARE)                        ==
        =============================================================================
        [ASCENSION 2]: Judgement of the Future.
        Scries the files currently held in the Staging Area for architectural heresies.
        """
        # 1. Capability Check
        if not hasattr(self.creator, 'sentinel_conduit') or \
                not self.creator.sentinel_conduit or \
                not self.creator.sentinel_conduit.sentinel_path:
            return

        tx = self.creator.transaction
        if not tx:
            return

        self.logger.info("Sentinel Inquisitor: Gazing into the Ephemeral Realm...")
        self._broadcast_hud("INQUEST_ACTIVE", "#a855f7")

        # 2. The Gaze of the Future
        # We iterate the write dossier, which holds the logical paths of the intended reality.
        for result in tx.write_dossier.values():
            if not result.success: continue

            # [ASCENSION 2]: We only judge what is being Created or Transfigured
            if result.action_taken in (InscriptionAction.CREATED, InscriptionAction.TRANSFIGURED):

                # Fetch path from the Staging Area
                staged_path = self.creator.staging_manager.get_staging_path(result.path)

                if staged_path.exists() and staged_path.is_file():
                    try:
                        # [ASCENSION 11]: NoneType Sarcophagus
                        content = staged_path.read_text(encoding='utf-8', errors='ignore')
                        if not content: continue

                        # Summon the Sentinel to perform the Inquest
                        heresies = self.creator.sentinel_conduit.adjudicate(result.path.name, content)

                        if any(h.severity == HeresySeverity.CRITICAL for h in heresies):
                            self._proclaim_inquest_failure(result.path, heresies)

                    except Exception as e:
                        # [ASCENSION 11]: Resonance Fail-Open
                        self.logger.warn(f"Adjudication deferred for '{result.path}': {e}")

    def conduct_dynamic_ignore(self):
        """
        =============================================================================
        == THE RITE OF TRANSACTIONAL SHROUDING (THE FIX)                           ==
        =============================================================================
        [ASCENSION 1]: Guarantees .gitignore updates are transactional.
        Automatically shields files containing high-entropy secrets.
        """
        tx = self.creator.transaction
        if not tx or not tx.write_dossier:
            return

        with self._lock:
            # 1. THE CENSUS OF SECRETS
            files_to_ignore: Set[str] = set()
            for result in tx.write_dossier.values():
                if result.success and result.security_notes:
                    # We use the relative POSIX path for the ignore record
                    files_to_ignore.add(result.path.as_posix())

            if not files_to_ignore:
                return

            # 2. THE RITE OF THE PREVIOUS LAW
            gitignore_path = Path(".gitignore")
            existing_ignores: Set[str] = set()

            # Use the creator's base_path to check for the current physical truth
            physical_gitignore = self.creator.base_path / gitignore_path

            if physical_gitignore.exists():
                try:
                    content = physical_gitignore.read_text(encoding='utf-8')
                    existing_ignores = {line.strip() for line in content.splitlines()
                                        if line.strip() and not line.startswith('#')}
                except Exception as e:
                    self.logger.warn(f"Gaze clouded upon .gitignore: {e}")

            # 3. THE TRANSMUTATION
            new_entries = files_to_ignore - existing_ignores
            if not new_entries:
                return

            self.logger.info(f"Dynamic Ignorer: Shielding {len(new_entries)} sensitive artifact(s).")
            self._broadcast_hud("VEIL_STRENGTHENED", "#64ffda")

            # [ASCENSION 7]: SEMANTIC METADATA STAMPING
            append_content = "\n# [Velm] Automatic Gnostic Protection\n"
            for entry in sorted(list(new_entries)):
                append_content += f"{entry}\n"

            # 4. THE TRANSACTIONAL STRIKE (THE CURE)
            # We perform the write through the IO Conductor. This ensures:
            # A. The change is written to STAGING, not root.
            # B. The change is added to the Transaction's write_dossier.
            # C. If the transaction fails, the staging file is deleted, leaving .gitignore pure.
            try:
                # Resolve current content (including any staged changes from this same TX)
                # We use the creator's io_conductor logic to handle the read-merge-write cycle

                # [ASCENSION 1]: Materialize final content
                current_full_content = ""
                if physical_gitignore.exists():
                    current_full_content = physical_gitignore.read_text(encoding='utf-8')

                final_content = current_full_content.rstrip() + "\n" + append_content

                # [THE FIX]: Transaction-Anchored Write
                # This call will register the intent with the TransactionManager automatically.
                # It uses InscriptionAction.TRANSFIGURED.
                self.creator.io_conductor.write(
                    logical_path=gitignore_path,
                    content=final_content,
                    metadata={"origin": "System:Adjudicator", "reason": "security_shield"}
                )

                self.logger.success("The Veil of Ignorance has been transactionally updated.")

            except Exception as e:
                # [ASCENSION 11]: Transmutation
                self.logger.error(f"Failed to stage .gitignore update: {e}")

    def _proclaim_inquest_failure(self, path: Path, heresies: List[Heresy]):
        """Proclaims the state of sin to the Architect and halts the Engine."""
        from rich.table import Table
        from rich.panel import Panel

        # [ASCENSION 4]: SOCRATIC CURE PROPHECY
        heresy_table = Table(title=f"[bold red]Heresies Perceived in '{path}'[/bold red]", box=None, expand=True)
        heresy_table.add_column("Ln", style="magenta", width=4)
        heresy_table.add_column("Diagnosis", style="white")
        heresy_table.add_column("Cure", style="cyan")

        for h in heresies:
            # [ASCENSION 4]: We suggest a refactor rite
            cure = h.fix_command or f"velm refactor {path} --prompt 'Fix: {h.message}'"
            heresy_table.add_row(str(h.line_num), h.message, f"[dim]{cure}[/dim]")

        self.console.print(Panel(heresy_table, border_style="red", title="[bold]Ω_INTEGRITY_FRACTURE[/bold]"))

        raise ArtisanHeresy(
            message=f"Materialization Aborted: The artifact '{path}' contains critical heresies.",
            severity=HeresySeverity.CRITICAL,
            suggestion="Review the forensic report and correct the blueprint logic before re-attempting inception."
        )

    def _broadcast_hud(self, label: str, color: str):
        """[ASCENSION 5]: HUD Multicast."""
        if hasattr(self.creator, 'engine') and self.creator.engine.akashic:
            try:
                self.creator.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "ADJUDICATION_EVENT",
                        "label": label,
                        "color": color,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_ADJUDICATOR status=RESONANT mode={type(self.creator).__name__}>"

# == SCRIPTURE SEALED: THE CONSCIENCE IS NOW PURE AND TRANSACTIONAL ==