# Path: scaffold/artisans/history/differ.py

import difflib
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax

# --- THE DIVINE SUMMONS OF THE GNOSTIC CONTRACTS ---
from .contracts import RiteGnosis
from ...core.state.contracts import LedgerOperation, RiteLedger, LedgerEntry
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import is_binary, get_human_readable_size
from ...logger import Scribe

Logger = Scribe("TemporalDiffer")


class TemporalDiffer:
    """
    =================================================================================
    == THE ALCHEMICAL TRANSMUTER OF CAUSALITY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)      ==
    =================================================================================
    LIF: ∞ (THE SUPREME JUDGE OF TIME)

    This is the divine artisan that perceives the divergence between timelines.
    It is the core engine for the Temporal Schism (Revert) and the Cherry-Pick rite.
    =================================================================================
    """

    def __init__(self, console: Console):
        self.console = console

    # =============================================================================
    # == I. THE RITE OF COMPARISON (MANIFEST DIFFING)                            ==
    # =============================================================================

    def compare(self, manifest_a: Dict, manifest_b: Dict) -> List[Dict[str, Any]]:
        """
        [FACULTY 1] The Gnostic Gaze of Divergence.
        Compares two manifests to identify Created, Modified, and Deleted souls.
        """
        paths_a = set(manifest_a.keys())
        paths_b = set(manifest_b.keys())

        created = paths_a - paths_b
        deleted = paths_b - paths_a
        common = paths_a.intersection(paths_b)

        modified = {
            p for p in common
            if manifest_a[p].get('sha256') != manifest_b[p].get('sha256')
        }

        diffs = []
        for p in sorted(list(created)):
            diffs.append({"path": p, "status": "CREATED", "meta": manifest_a[p]})
        for p in sorted(list(deleted)):
            diffs.append({"path": p, "status": "DELETED", "meta": manifest_b[p]})
        for p in sorted(list(modified)):
            diffs.append({"path": p, "status": "MODIFIED", "meta_new": manifest_a[p], "meta_old": manifest_b[p]})

        self._proclaim_diff_summary(diffs)
        return diffs

    # =============================================================================
    # == II. THE TEMPORAL SCHISM (REVERT PATCH FORGING)                         ==
    # =============================================================================

    def forge_revert_patch(self, rite_to_revert: RiteGnosis, project_root: Path) -> str:
        """
        [FACULTY 2 & 4 & 6] The Rite of Reverse Alchemy.
        Forges a .patch.scaffold scripture to surgically undo a specific rite.
        """
        Logger.info(f"Forging Reverse Patch for Rite: [cyan]{rite_to_revert.rite_id[:8]}[/cyan]")

        patch_lines = [
            f"# == Gnostic Revert Patch == ",
            f"# Target Rite: {rite_to_revert.rite_name}",
            f"# Target ID:   {rite_to_revert.rite_id}",
            f"# Generated:   {os.getlogin()} on {Path.cwd().name}",
            f"#",
            f"# This scripture contains the Gnostic Inverse of the original will.",
            ""
        ]

        # 1. Fetch the Ledger (The Memory of the Event)
        ledger_path = project_root / ".scaffold" / "trash" / rite_to_revert.rite_id / "ledger.json"

        if not ledger_path.exists():
            Logger.error(f"Ledger for rite {rite_to_revert.rite_id[:8]} is a void. Reversion is blinded.")
            return "# HERESY: Ledger not found. Cannot calculate reverse alchemy."

        try:
            ledger_data = RiteLedger.model_validate_json(ledger_path.read_text(encoding='utf-8'))
        except Exception as e:
            Logger.error(f"Ledger corruption perceived: {e}")
            return f"# HERESY: Ledger at {ledger_path.name} is profane."

        # 2. Iterate and Invert (The Great Transmutation)
        # We walk the ledger BACKWARDS to ensure correct physical reconstruction.
        for entry in reversed(ledger_data.entries):
            self._forge_inverse_edict(entry, patch_lines)

        patch_lines.append("\n# --- End of Temporal Reversion ---")
        return "\n".join(patch_lines)

    def _forge_inverse_edict(self, entry: LedgerEntry, lines: List[str]):
        """[FACULTY 11] Forges a single reverse edict line or block."""
        if not entry.inverse_action:
            return

        op = entry.inverse_action.op
        params = entry.inverse_action.params

        # Add a forensic comment for the Architect
        lines.append(f"# [FORENSICS] Reversing {entry.operation} by {entry.actor}")

        if op == LedgerOperation.WRITE_FILE:
            path = params['path']
            content_bytes = entry.snapshot_content

            if content_bytes is not None:
                # [FACULTY 4] The Heredoc Purifier
                content_str = self._decode_and_purify(content_bytes)
                delimiter = '"""' if '"""' not in content_str else "'''"

                lines.append(f"{path} :: {delimiter}")
                lines.append(content_str)
                lines.append(delimiter)
            else:
                # If there was no snapshot content, it was a creation,
                # so the inverse is a deletion, but handled below.
                pass

        elif op == LedgerOperation.DELETE_FILE:
            path = params['path']
            # We use the Maestro's Will for deletion in a patch
            if "%% post-run" not in lines:
                lines.append("%% post-run")
            lines.append(f"    rm -f {path}")

        elif op == LedgerOperation.RMDIR:
            path = params['path']
            if "%% post-run" not in lines:
                lines.append("%% post-run")
            lines.append(f"    rmdir {path}")

        elif op == LedgerOperation.EXEC_SHELL:
            # [FACULTY 6] Maestro's Counter-Edict
            commands = params.get("commands", [])
            if commands:
                if "%% post-run" not in lines:
                    lines.append("%% post-run")
                for cmd in commands:
                    lines.append(f"    {cmd} # [REVERSE-EDICT]")

    # =============================================================================
    # == III. CHERRY-PICKING (RITE REPLICATION)                                  ==
    # =============================================================================

    def forge_cherry_pick_blueprint(self, rite: RiteGnosis) -> str:
        """
        [FACULTY 12] Forges a blueprint that replicates the soul of a past rite.
        """
        lines = [
            f"# == Gnostic Cherry-Pick: {rite.rite_name} ==",
            f"# Replicating Gnosis from {rite.rite_id[:8]}",
            ""
        ]

        # 1. Inject Variables (The Delta)
        if rite.gnosis_delta:
            lines.append("# --- Replicated Gnosis ---")
            for k, v in rite.gnosis_delta.items():
                lines.append(f"$$ {k} = {json.dumps(v)}")
            lines.append("")

        # 2. Inject Manifest (The Form)
        lines.append("# --- Replicated Form ---")
        for path, meta in rite.manifest.items():
            # We only pick what was ACTUALLY created or modified in this specific rite.
            if meta.get('action') in ('CREATED', 'TRANSFIGURED', 'TRANSLOCATED'):
                # In a true pick, we'd need the file content.
                # For this version, we forge the structure.
                lines.append(f"{path} << (Summoned from {rite.rite_id[:8]})")

        # 3. Inject Edicts (The Will)
        if rite.edicts:
            lines.append("\n%% post-run")
            for cmd in rite.edicts:
                lines.append(f"    {cmd}")

        return "\n".join(lines)

    # =============================================================================
    # == IV. INTERNAL ARTISANS (HELPERS)                                         ==
    # =============================================================================

    def _decode_and_purify(self, data: bytes) -> str:
        """[FACULTY 8] The Gaze of Forgiveness for Binary Souls."""
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            Logger.warn("Non-UTF8 soul perceived. Using Latin-1 fallback.")
            return data.decode('latin-1')

    def _proclaim_diff_summary(self, diffs: List[Dict]):
        """[FACULTY 9] The Luminous TUI Scribe."""
        if not diffs:
            self.console.print(
                Panel("[bold green]Timeline is in perfect harmony. No divergence perceived.[/bold green]"))
            return

        table = Table(title="[bold yellow]Gnostic Differential Dossier[/bold yellow]", box=None)
        table.add_column("State", width=12, justify="center")
        table.add_column("Scripture", style="cyan")
        table.add_column("Mass", justify="right", style="dim")

        for d in diffs:
            status = d['status']
            color = "green" if status == "CREATED" else "red" if status == "DELETED" else "yellow"
            icon = "✨" if status == "CREATED" else "💀" if status == "DELETED" else "⚡"

            meta = d.get('meta', d.get('meta_new', {}))
            size = get_human_readable_size(meta.get('bytes', 0))

            table.add_row(f"[{color}]{icon} {status}[/]", d['path'], size)

        self.console.print(Panel(table, border_style="yellow"))

    def compute_merkle_root(self, manifest: Dict) -> str:
        """[FACULTY 5] Calculates the Merkle Root of a manifest for integrity checks."""
        hasher = hashlib.sha256()
        # Sort paths to ensure deterministic root
        for path in sorted(manifest.keys()):
            file_hash = manifest[path].get('sha256', '')
            hasher.update(path.encode('utf-8'))
            hasher.update(file_hash.encode('utf-8'))
        return hasher.hexdigest()