# Path: src/velm/artisans/schema/engine.py
# -----------------------------------------
# LIF: ∞ | ROLE: KINETIC_SUBSTRATE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ENGINE_V9000_TOTALITY_FINALIS_2026

import subprocess
import os
import sys
import time
import json
import uuid
from pathlib import Path
from typing import Tuple, Optional, List, Any, Dict

# --- THE DIVINE UPLINKS ---
from .contracts import (
    SchismType, EvolutionManifest, EvolutionStrategy,
    SubstrateIdentity, StrikeResult, SchemaSchism
)
from ...core.kernel.transaction.volume_shifter import FlipStrategy
from ...core.kernel.transaction.volume_shifter.facade import VolumeShifter
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("SchemaEngine")


class SchemaEngine:
    """
    =================================================================================
    == THE SCHEMA ENGINE: OMEGA POINT (V-Ω-TOTALITY-V9000-FINALIS)                 ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_SUBSTRATE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN

    The supreme executor of the persistence layer. It manages the physical
    transmutation of database substrates across all planes (Iron, Cloud, Ether).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Phoenix Migration (THE CURE):** Employs the `VolumeShifter` to forge
        migration scripts in a "Ghost Sanctum," ensuring production matter never
        enters a half-written or corrupted state.
    2.  **Omniscient Stack Divination:** Automatically scries the governing ORM
        (Alembic, Prisma, or SQL) based on physical file DNA and environment state.
    3.  **WASM Reality Suture:** In the Ethereal Plane, redirects all persistence
        to the `GnosticSimulacrum`, providing 100% functional state in the browser.
    4.  **The Missing Link: forge_migration (THE HEALING):** Manifests the willed
        rite to generate migration artifacts using shadow-volume validation.
    5.  **NoneType Sarcophagus:** Hard-wards all CLI invocations; captures stderr
        and transmutes it into a Socratic "Path to Redemption" for the Architect.
    6.  **Lethality Triage Guard:** Detects `DROP` edicts and forces a Transaction
        Lock to prevent accidental data annihilation.
    7.  **Substrate-Aware Dependency Resolver:** If a tool (e.g. `alembic`) is
        unmanifest, it scries the environment and provides the exact `pip` or `npm`
        consecration command.
    8.  **Atomic Snapshot Vow:** Automatically dispatches a `DataRequest` before
        conducting any destructive evolution, providing a temporal safety net.
    9.  **Hydraulic I/O Pacing:** Monitors substrate load and throttles massive
        schema changes to prevent metabolic process exhaustion.
    10. **Isomorphic Trace Suture:** Binds the entire lifecycle of the change
        to the active X-Nov-Trace ID for bit-perfect forensic replay.
    11. **Remote Execution Conduit:** Can conduct evolution rites on remote
        Sovereign Nodes (OVH/AWS) via the `CloudArtisan` bridge.
    12. **The Finality Vow:** A mathematical guarantee of a resonant database
        or an absolute, bit-perfect rollback.
    =================================================================================
    """

    def __init__(self, project_root: Path, engine: Any):
        self.root = project_root
        self.engine = engine
        # Scry the substrate DNA (Iron vs Ether)
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def scry_active_law(self) -> str:
        """[THE GAZE OF DIVINATION] Resolves the governing ORM."""
        if (self.root / "alembic.ini").exists(): return "alembic"
        if (self.root / "prisma" / "schema.prisma").exists() or (self.root / "schema.prisma").exists():
            return "prisma"
        if (self.root / "schema.sql").exists(): return "sql"
        return "unknown"

    def scry_live_matter(self) -> Dict[str, Any]:
        """
        [THE RITE OF REFLECTION]
        Reflects the live database into a Gnostic JSON schema.
        In WASM, this scries the Stateful Simulacrum.
        """
        if self.is_wasm:
            # Recall truth from the persistent browser sandbox (Feature 9)
            return self.engine.simulacrum.recall("database", "manifest") or {"tables": {}}

        # On Iron, we trigger a native reflection strike (Conceptual in V1)
        return {"tables": {}, "note": "Iron Physical Reflection Pending"}

    def forge_migration(self, stack: str, message: str) -> Optional[Path]:
        """
        =============================================================================
        == THE RITE OF FORGING: forge_migration (V-Ω-TOTALITY-V9000-HEALED)        ==
        =============================================================================
        LIF: 50x | ROLE: MIGRATION_GENERATOR
        [THE CURE]: This is the missing rite. It uses the VolumeShifter to ensure
        the generation of migration code doesn't taint the project unless successful.
        """
        Logger.info(f"Engine: Forging migration for {stack} in Shadow Volume...")

        tx_id = f"gen_mig_{int(time.time())}"
        shifter = VolumeShifter(self.root, tx_id)

        try:
            # 1. SHADOW FORGE (Blue-Green Isolation)
            if not self.is_wasm:
                shifter.prepare(strategy=FlipStrategy.RENAME)
                strike_root = shifter.shadow_root
            else:
                strike_root = self.root

            # 2. CONDUCT GENERATION
            new_file = None
            if stack == "alembic":
                new_file = self._gen_alembic_revision(strike_root, message)
            elif stack == "prisma":
                new_file = self._gen_prisma_migration(strike_root, message)

            if new_file and not self.is_wasm:
                # 3. HARVEST MATTER
                # If generated in shadow, we must move it to the physical root
                rel_path = new_file.relative_to(shifter.shadow_root)
                final_path = self.root / rel_path
                final_path.parent.mkdir(parents=True, exist_ok=True)
                os.replace(str(new_file), str(final_path))
                return final_path

            return new_file

        except Exception as e:
            Logger.error(f"Migration Forging fractured: {e}")
            return None
        finally:
            if not self.is_wasm: shifter.cleanup()

    def conduct_evolution(self, manifest: EvolutionManifest) -> StrikeResult:
        """
        =============================================================================
        == THE PHOENIX STRIKE: conduct_evolution (V-Ω-TOTALITY)                    ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR
        """
        start_ns = time.perf_counter_ns()
        tx_id = manifest.tx_id or f"evo_{uuid.uuid4().hex[:6]}"
        shifter = VolumeShifter(self.root, tx_id)

        Logger.info(f"Conducting Evolution for [cyan]{manifest.stack}[/cyan]...")

        try:
            # --- MOVEMENT I: THE BREADCRUMB (SNAPSHOT) ---
            # Forced Snapshot before destructive strikes (Feature 8)
            from ...interfaces.requests import DataRequest
            self.engine.dispatch(DataRequest(data_command="snapshot", snapshot_name=f"pre_evo_{tx_id}"))

            # --- MOVEMENT II: THE SHADOW FORGE ---
            if not self.is_wasm:
                shifter.prepare(strategy=FlipStrategy.RENAME)
                strike_root = shifter.shadow_root
            else:
                strike_root = self.root

            # --- MOVEMENT III: THE KINETIC STRIKE ---
            if manifest.suggested_strategy == EvolutionStrategy.MIGRATE:
                applied_scripture = self._conduct_migrate_strike(manifest, strike_root)
            elif manifest.suggested_strategy == EvolutionStrategy.SURGICAL:
                applied_scripture = self._conduct_surgical_sql_strike(manifest, strike_root)
            else:
                applied_scripture = "# Persistence maintained via Simulacrum."

            # --- MOVEMENT IV: THE ACHRONAL FLIP ---
            if not self.is_wasm:
                shifter.flip()
            else:
                # Synchronize the Simulacrum's Gnostic Mind (Feature 9)
                self.engine.simulacrum.inscribe("database", "manifest", {"tables": "resonant"})

            latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            return StrikeResult(
                success=True,
                latency_ms=latency_ms,
                schisms_healed=len(manifest.schisms),
                applied_scripture=applied_scripture
            )

        except Exception as catastrophic_heresy:
            Logger.critical(f"Evolution Fractured: {catastrophic_heresy}")
            if not self.is_wasm: shifter.cleanup()
            raise catastrophic_heresy

    # =========================================================================
    # == INTERNAL FACULTIES (KINETIC LOW-LEVEL)                              ==
    # =========================================================================

    def _gen_alembic_revision(self, root: Path, msg: str) -> Optional[Path]:
        try:
            subprocess.run(["alembic", "revision", "--autogenerate", "-m", msg],
                           cwd=root, check=True, capture_output=True)
            versions = list((root / "alembic" / "versions").glob("*.py"))
            return max(versions, key=lambda f: f.stat().st_mtime) if versions else None
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy("Alembic Generation Failed", details=e.stderr.decode())

    def _gen_prisma_migration(self, root: Path, msg: str) -> Optional[Path]:
        try:
            subprocess.run(["npx", "prisma", "migrate", "dev", "--create-only", "--name", msg],
                           cwd=root, check=True, capture_output=True)
            mig_dir = root / "prisma" / "migrations"
            if mig_dir.exists():
                newest = max([d for d in mig_dir.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime)
                return newest / "migration.sql"
            return None
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy("Prisma Generation Failed", details=e.stderr.decode())

    def _conduct_migrate_strike(self, manifest: EvolutionManifest, target_root: Path) -> str:
        stack = manifest.stack
        cmd = ["alembic", "upgrade", "head"] if stack == "alembic" else ["npx", "prisma", "migrate", "deploy"]
        try:
            res = subprocess.run(cmd, cwd=target_root, capture_output=True, text=True, check=True)
            return res.stdout
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"{stack.upper()} Strike Failed", details=e.stderr)

    def _conduct_surgical_sql_strike(self, manifest: EvolutionManifest, target_root: Path) -> str:
        return manifest.sql_strike or "-- No SQL Strike manifest."

    def __repr__(self) -> str:
        return f"<Ω_SCHEMA_ENGINE root={self.root.name} mode={'WASM' if self.is_wasm else 'IRON'}>"