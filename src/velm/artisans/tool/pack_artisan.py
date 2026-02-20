# Path: src/velm/artisans/tool/pack_artisan.py
# --------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: GNOSTIC_ENCAPSULATOR | RANK: OMEGA_SUPREME
# AUTH: Ω_PACKER_V3000_VESSEL_SMITH_2026_FINALIS

import os
import sys
import time
import json
import traceback
import uuid
import zipfile
import hashlib
import platform
import getpass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Final, Set

# --- THE DIVINE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.requests import PackRequest
from ...interfaces.base import ScaffoldResult, Artifact
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...logger import Scribe

Logger = Scribe("PackArtisan")


@register_artisan("pack")
class PackArtisan(BaseArtisan[PackRequest]):
    """
    =================================================================================
    == THE PACK ARTISAN: OMEGA POINT (V-Ω-TOTALITY-V3000-VESSEL-SMITH)             ==
    =================================================================================
    The Supreme Encapsulator of Gnosis. Transmutes physical directories and
    templates into bit-perfect, portable .vessel shards.
    """

    # [FACULTY 5]: THE EXORCISM GRIMOIRE
    # Patterns to be purged from the Vessel to maintain Gnostic Purity.
    ENTROPY_PATTERNS: Final[Set[str]] = {
        ".git", ".github", ".scaffold", "scaffold.lock", "__pycache__",
        "node_modules", "venv", ".venv", ".DS_Store", "Thumbs.db", ".env"
    }

    def execute(self, request: PackRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF ENCAPSULATION (EXECUTE)                                    ==
        =============================================================================
        """
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: SOURCE RESOLUTION (THE CURE) ---
        # [ASCENSION 1]: Resolve if we are packing a local dir or a global template.
        source_path, archetype_name = self._resolve_source(request)

        # [ASCENSION 10]: VOID SOURCE WARD
        if not source_path.exists() or not source_path.is_dir():
            raise ArtisanHeresy(
                f"Void Source: The sanctum '{source_path}' is unmanifest or not a directory.",
                severity=HeresySeverity.CRITICAL
            )

        # --- MOVEMENT II: FORGE COORDINATES ---
        target_name = request.output_name or f"{archetype_name or source_path.name}.vessel"
        if not target_name.endswith(".vessel"):
            target_name += ".vessel"

        target_path = (self.project_root / target_name).resolve()
        temp_vessel = target_path.with_suffix(".vessel.tmp")

        self.logger.info(f"Initiating the Rite of Encapsulation for [cyan]{source_path.name}[/cyan]...")
        self._radiate_hud_pulse("PACK_START", "#a855f7", request.trace_id)

        try:
            # --- MOVEMENT III: THE RITE OF THE VESSEL (PACKING) ---
            # [ASCENSION 3, 7, 9]: We weave the manifest and the matter into a single zip.
            manifest, file_count, total_bytes = self._forge_vessel(
                source_path,
                temp_vessel,
                archetype_name or source_path.name,
                request
            )

            # --- MOVEMENT IV: ATOMIC FINALIZATION ---
            # [ASCENSION 8, 9]: Move and Sync
            if target_path.exists():
                target_path.unlink()
            os.replace(temp_vessel, target_path)

            # Force physical commitment
            fd = os.open(target_path, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)

            # --- MOVEMENT V: THE REVELATION ---
            duration_s = (time.perf_counter_ns() - start_ns) / 1_000_000_000
            self._radiate_hud_pulse("PACK_COMPLETE", "#64ffda", request.trace_id)

            return self.success(
                message=f"Gnostic Vessel '{target_path.name}' forged and sealed.",
                data={
                    "manifest": manifest,
                    "file_count": file_count,
                    "total_bytes": total_bytes,
                    "duration": duration_s,
                    "merkle_root": manifest["integrity"]["merkle_root"]
                },
                artifacts=[Artifact(
                    path=target_path,
                    type="file",
                    action="created",
                    size_bytes=total_bytes,
                    checksum=manifest["integrity"]["merkle_root"]
                )]
            )

        except Exception as fracture:
            self._radiate_hud_pulse("PACK_FRACTURED", "#ef4444", request.trace_id)
            if temp_vessel.exists():
                temp_vessel.unlink()

            Logger.critical(f"Encapsulation Symphony Fractured: {fracture}")
            return self.failure(
                message=f"Encapsulation Failure: {str(fracture)}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == INTERNAL RITES (THE FORGE)                                          ==
    # =========================================================================

    def _resolve_source(self, request: PackRequest) -> Tuple[Path, Optional[str]]:
        """[FACULTY 1]: Resolves the physical coordinates of the Gnosis."""
        raw_source = str(request.source_path)

        # Path A: Explicit Local Directory
        local_path = Path(raw_source).resolve()
        if local_path.is_dir():
            return local_path, None

        # Path B: Global Template Library
        template_sanctum = Path.home() / ".scaffold" / "templates"
        named_template = template_sanctum / f"template.{raw_source}.scaffold"

        if named_template.exists():
            # If it's a single file template, we treat its parent as the source?
            # No, we wrap the single file into a virtual directory context
            return template_sanctum, raw_source

        return local_path, None

    def _forge_vessel(
            self,
            source: Path,
            dest: Path,
            name: str,
            request: PackRequest
    ) -> Tuple[Dict[str, Any], int, int]:
        """
        =============================================================================
        == THE VESSEL FORGE (V-Ω-TOTALITY)                                         ==
        =============================================================================
        [ASCENSION 2, 3, 5, 7]: Conducts the multi-pass walk to generate hashes,
        excise entropy, and inscribe the manifest.
        """
        file_registry: Dict[str, str] = {}
        total_bytes = 0
        file_count = 0

        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as vessel:
            # --- MOVEMENT I: THE MATTER SCAN ---
            # We perform a recursive walk, building the Merkle registry
            for root, dirs, files in os.walk(source):
                # [ASCENSION 5]: Entropy Excision
                dirs[:] = [d for d in dirs if d not in self.ENTROPY_PATTERNS]

                for f in files:
                    if f in self.ENTROPY_PATTERNS: continue

                    phys_path = Path(root) / f
                    rel_path = phys_path.relative_to(source)

                    # [ASCENSION 7]: POSIX Normalization
                    archive_path = rel_path.as_posix()

                    # Calculate Atomic Hash
                    file_hash = self._hash_file(phys_path)
                    file_registry[archive_path] = file_hash

                    # Inscribe Matter
                    vessel.write(phys_path, archive_path)

                    total_bytes += phys_path.stat().st_size
                    file_count += 1

            # --- MOVEMENT II: THE MANIFEST FORGE ---
            # [ASCENSION 3, 6]: Provenance Inscription
            manifest = {
                "vessel_version": "1.0",
                "rite_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "provenance": {
                    "name": name,
                    "architect": getpass.getuser(),
                    "host": platform.node(),
                    "os": platform.system(),
                    "engine_v": str(getattr(self.engine, 'version', '0.0.0'))
                },
                "content": {
                    "files": file_registry,
                    "count": file_count,
                    "mass_bytes": total_bytes
                },
                "integrity": {
                    "merkle_root": self._compute_merkle_root(file_registry)
                }
            }

            # Inscribe Manifest into the heart of the vessel
            vessel.writestr("vessel.json", json.dumps(manifest, indent=2))

        return manifest, file_count, total_bytes

    def _hash_file(self, path: Path) -> str:
        """Calculates a SHA256 fingerprint for a single file."""
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _compute_merkle_root(self, registry: Dict[str, str]) -> str:
        """
        [FACULTY 2]: Forges a single root hash from all file hashes.
        Ensures the order is deterministic via sorting.
        """
        hasher = hashlib.sha256()
        for path in sorted(registry.keys()):
            hasher.update(path.encode())
            hasher.update(registry[path].encode())
        return hasher.hexdigest()

    def _radiate_hud_pulse(self, type_label: str, color: str, trace: str):
        """[ASCENSION 11]: Atmospheric Telemetry."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "GNOSTIC_PACKER",
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_PACK_ARTISAN status=RESONANT substrate='IRON'>"
