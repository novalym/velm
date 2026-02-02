# path: scaffold/core/kernel/artifact_hoarder.py

import json
import time
import hashlib
import zipfile
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from ....logger import Scribe
from ....utils import atomic_write, get_human_readable_size
from ....contracts.heresy_contracts import ArtisanHeresy

if TYPE_CHECKING:
    from ..transaction.facade import GnosticTransaction
    from ....interfaces.base import ScaffoldResult

Logger = Scribe("GnosticHistorian")


class ArtifactHoarder:
    """
    =================================================================================
    == THE KEEPER OF THE ETERNAL TIMELINE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)           ==
    =================================================================================
    The Gnostic Historian. It forges a complete, forensically-sound, and eternally
    reproducible dossier for every significant rite conducted by the God-Engine.
    It is the Black Box Recorder of the Scaffold Cosmos.
    =================================================================================
    """

    ARTIFACTS_ROOT = ".scaffold/chronicles"

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self.artifacts_path = self.root / self.ARTIFACTS_ROOT
        self.artifacts_path.mkdir(parents=True, exist_ok=True)

    def inscribe_rite_dossier(
            self,
            transaction: "GnosticTransaction",
            result: "ScaffoldResult",
            exc_info: Optional[tuple] = None
    ) -> Optional[Path]:
        """
        The one true rite of forensic archival. Receives the complete state of a
        concluded rite and enshrines it for eternity.
        Returns the path to the sacred time capsule of the rite.
        """
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            rite_name_safe = transaction.rite_name.replace(":", "_").replace(" ", "_")
            archive_name = f"{timestamp}_{rite_name_safe}_{transaction.tx_id[:8]}"
            archive_path = self.artifacts_path / f"{archive_name}.zip"

            Logger.verbose(f"Historian awakened. Forging time capsule for rite '{transaction.rite_name}'...")

            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # --- Movement I: The Gnostic Manifest ---
                manifest = self._forge_manifest(transaction, result, exc_info)
                zf.writestr("manifest.json", json.dumps(manifest, indent=2))

                # --- Movement II: The Luminous Proclamation ---
                readme = self._forge_readme(manifest)
                zf.writestr("README.md", readme)

                # --- Movement III: The Quantum State Snapshot ---
                # Archive the final, intended state of all modified files from staging.
                if transaction.staging_manager.staging_root.exists():
                    for res in transaction.write_dossier.values():
                        staged_path = transaction.get_staging_path(res.path)
                        if staged_path.is_file():
                            try:
                                zf.writestr(f"reality_snapshot/{res.path.as_posix()}", staged_path.read_bytes())
                            except Exception as e:
                                Logger.warn(f"Could not archive staged soul for '{res.path}': {e}")

            Logger.success(
                f"Gnostic Chronicle for rite '{transaction.rite_name}' enshrined at: [dim]{archive_path.relative_to(self.root)}[/dim]")
            return archive_path

        except Exception as e:
            # The Unbreakable Ward: The historian must never shatter its caller.
            Logger.error(
                f"META-HERESY: The Gnostic Historian's hand faltered. The chronicle may be incomplete. Reason: {e}",
                exc_info=True)
            return None

    def _forge_manifest(self, tx: "GnosticTransaction", result: "ScaffoldResult", exc_info: Optional[tuple]) -> Dict[
        str, Any]:
        """[FACULTY 6] Forges the rich, hyper-structured Gnostic Dossier."""
        from .... import __version__
        import platform, getpass

        # --- The Environmental Hologram ---
        environmental_gnosis = {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "scaffold_version": __version__,
            "user": getpass.getuser(),
            "host": platform.node(),
            "cwd": str(Path.cwd()),
            "environment_variables": {k: v for k, v in os.environ.items() if k.startswith("SC_") or k in ["PATH"]}
        }

        # --- Heresy Chronicle ---
        heresy_dossier = None
        if exc_info:
            exc_type, exc_value, exc_tb = exc_info
            heresy_dossier = {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "traceback": traceback.format_exc(),
                # Prophecy: A future GnosticError object would be serialized here.
            }

        # --- The Final Manifest ---
        manifest = {
            "rite_name": tx.rite_name,
            "transaction_id": tx.tx_id,
            "timestamp_utc": datetime.now().isoformat(),
            "status": "SUCCESS" if result.success else ("FAILURE" if exc_info else "WARNING"),
            "duration_seconds": result.duration_seconds,
            "gnostic_context": tx.context,
            "environmental_gnosis": environmental_gnosis,
            "result_message": result.message,
            "heresies_perceived": [h.model_dump() for h in result.heresies],
            "catastrophic_heresy": heresy_dossier,
            "artifacts_manifest": [a.model_dump(mode='json') for a in result.artifacts],
            "edicts_executed": tx.edicts_executed
        }
        return manifest

    def _forge_readme(self, manifest: Dict[str, Any]) -> str:
        """[FACULTY 11] Forges the human-readable summary of the rite."""
        lines = [f"# Gnostic Chronicle: {manifest['rite_name']}"]
        lines.append(
            f"> **Status:** {manifest['status']} | **Duration:** {manifest['duration_seconds']:.3f}s | **Timestamp:** {manifest['timestamp_utc']}")
        lines.append("\n---\n")

        # Summary
        lines.append("## Summary of the Great Work")
        lines.append(manifest['result_message'])

        # Artifacts
        if artifacts := manifest.get('artifacts_manifest'):
            lines.append("\n## Transfigured Reality")
            for art in artifacts:
                lines.append(
                    f"- **{art['action']}**: `{art['path']}` ({get_human_readable_size(art.get('size_bytes', 0))})")

        # Edicts
        if edicts := manifest.get('edicts_executed'):
            lines.append("\n## Maestro's Will")
            lines.append("```bash")
            lines.extend(edicts)
            lines.append("```")

        # Heresy
        if heresy := manifest.get('catastrophic_heresy'):
            lines.append("\n## Catastrophic Paradox")
            lines.append(f"**{heresy['type']}:** {heresy['message']}")
            lines.append("\n```")
            lines.append(heresy['traceback'])
            lines.append("```")

        return "\n".join(lines)