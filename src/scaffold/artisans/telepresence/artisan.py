# Path: scaffold/artisans/telepresence/artisan.py
# ----------------------------------------------
import base64
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import TelepresenceRequest
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

# --- THE DIVINE SUMMONS OF THE SPECIALIST PANTHEON ---
from .shadow_vault import ShadowVault
from .causal_slicer import CausalSlicer
from .url_projector import URLProjector
from .maestro_bridge import MaestroBridge

Logger = Scribe("TelepresenceArtisan")


class TelepresenceArtisan(BaseArtisan[TelepresenceRequest]):
    """
    =================================================================================
    == THE ASTRAL PROJECTIONIST (V-Ω-UNIVERSAL-CONDUCTOR-FINALIS++)                ==
    =================================================================================
    LIF: 10,000,000,000,000 | AUTH_CODE: ()@#()#@()#@()

    This is the ultimate, hyper-elevated bridge of the Scaffold Engine.
    It unifies the Mortal (Disk), Ethereal (Memory), and Celestial (Remote) planes.
    """

    def __init__(self, engine):
        super().__init__(engine)
        # Specialist Artisans are forged at birth
        self.vault = ShadowVault(self.project_root)
        self.slicer = CausalSlicer(self.engine)
        self.projector = URLProjector(self.project_root)
        self.maestro = MaestroBridge(self.project_root)

    def execute(self, request: TelepresenceRequest) -> ScaffoldResult:
        """The Grand Rite of Telepathic Triage."""

        # 1. THE ANCHOR OF RELATIVITY
        # Resolve URLs or local paths to their respective realities.
        is_celestial = request.path.startswith(('http', 'git@'))
        session_id = request.session_id or "global"

        if not is_celestial:
            target_abs = (self.project_root / request.path).resolve()
            if not str(target_abs).startswith(str(self.project_root)):
                raise ArtisanHeresy(f"Boundary Violation: '{request.path}' escapes the Sanctum.")

        try:
            # --- MOVEMENT I: KINETIC WILL (REMOTE EXECUTION) ---
            if request.operation == 'conduct_edict':
                # Striking across the void: Executing shell commands on the server.
                res = self.maestro.conduct_remote_edict(request.new_path, request.variables)
                return self.success("Remote Edict Concluded", data=res)

            # --- MOVEMENT II: CELESTIAL PROJECTION (URLS) ---
            elif request.operation == 'project_url':
                # Inhabiting remote repos as virtual local projects.
                return self.projector.mount(request.path)

            # --- MOVEMENT III: SHADOW REALITY (DREAMING) ---
            elif request.operation.startswith('shadow_'):
                return self._handle_shadow_rites(request)

            # --- MOVEMENT IV: CAUSAL PROPHECY (THE ORACLE) ---
            elif request.operation in ('causal_slice', 'impact_prophecy'):
                return self._handle_causal_rites(request)

            # --- MOVEMENT V: HYBRID PERCEPTION (SCRYING) ---
            elif request.operation == 'stat':
                return self._conduct_hybrid_stat(request)
            elif request.operation == 'read':
                return self._conduct_hybrid_read(request)
            elif request.operation == 'readdir':
                return self._conduct_hybrid_readdir(request)

            # --- MOVEMENT VI: PHYSICAL MATERIALIZATION (MATTER) ---
            elif request.operation == 'write':
                return self._conduct_physical_write(request)

            return self.failure(f"Heresy: Unknown Gnostic Verb '{request.operation}'")

        except Exception as e:
            Logger.critical(f"Telepresence Paradox on line {request.path}: {e}", exc_info=True)
            return self.failure(str(e))

    # -------------------------------------------------------------------------
    # INTERNAL CONDUCTORS
    # -------------------------------------------------------------------------

    def _handle_shadow_rites(self, req: TelepresenceRequest) -> ScaffoldResult:
        """Handles the AI's Ethereal Plane operations."""
        if req.operation == 'shadow_write':
            data = base64.b64decode(req.content_base64)
            self.vault.write(req.session_id, req.path, data)

            # Broadcast the change to the IDE Nervous System
            self._broadcast_change(req.path, "shadow_update")
            return self.success(f"Shadow forged: {req.path}")

        if req.operation == 'shadow_commit':
            # Collapse the dream into matter (Materialization)
            count = self.vault.materialize(req.session_id, req.path)
            self._broadcast_change(req.path, "physical_materialization")
            return self.success(f"Materialized {count} shadow scriptures.")

        return self.failure("Hollow Shadow Rite.")

    def _handle_causal_rites(self, req: TelepresenceRequest) -> ScaffoldResult:
        """Performs Causal Slicing and Architectural Health Prophecy."""
        if req.operation == 'impact_prophecy':
            shadow_data = self.vault.read(req.session_id, req.path)
            # Prophesy PageRank delta
            delta = self.slicer.prophesy_delta(req.path, shadow_data)
            return self.success("Impact Prophecy Sealed.", data=delta)

        if req.operation == 'causal_slice':
            slice_gnosis = self.slicer.extract_slice(req.path, req.depth)
            return self.success("Causal Slice forged.", data=slice_gnosis)

    def _conduct_hybrid_read(self, req: TelepresenceRequest) -> ScaffoldResult:
        """Reads from Shadow if present, else Physical Disk."""
        shadow_content = self.vault.read(req.session_id, req.path)

        if shadow_content is not None:
            return self.success("Shadow perceived", data={
                "content": base64.b64encode(shadow_content).decode('utf-8'),
                "reality": "shadow"
            })

        # Fallback to matter
        target = self.project_root / req.path
        if target.is_file():
            content = target.read_bytes()
            return self.success("Matter perceived", data={
                "content": base64.b64encode(content).decode('utf-8'),
                "reality": "physical"
            })

        return self.failure("Void encountered", data={"code": "FileNotFound"})

    def _conduct_hybrid_stat(self, req: TelepresenceRequest) -> ScaffoldResult:
        """Union-Gaze for file statistics."""
        rel_path = req.path.replace('\\', '/').lstrip('/')

        # Check Shadow First
        virtual_meta = self.vault.scry_metadata(req.session_id, rel_path)
        if virtual_meta:
            return self.success("Shadow Stat", data=virtual_meta)

        # Check Physical
        abs_path = self.project_root / rel_path
        if abs_path.exists():
            st = abs_path.stat()
            res = {
                "type": 1 if abs_path.is_file() else 2,
                "size": st.st_size,
                "mtime": st.st_mtime * 1000,
                "is_shadow": False
            }
            # Inject Cortex Gnosis (LIF: 100x)
            if req.include_gnosis:
                memory = self.engine.cortex.perceive()
                g = memory.find_gnosis_by_path(Path(rel_path))
                if g: res["gnosis"] = {"centrality": g.centrality_score, "lang": g.language}
            return self.success("Physical Stat", data=res)

        return self.failure("Void", data={"code": "FileNotFound"})

    def _conduct_physical_write(self, req: TelepresenceRequest) -> ScaffoldResult:
        """The Hand of Matter: Writes to disk and pulses the Nervous System."""
        target = self.project_root / req.path
        data = base64.b64decode(req.content_base64)
        from ...utils import atomic_write
        atomic_write(target, data, self.logger, self.project_root)

        self._broadcast_change(req.path, "physical_update")
        self.engine.cortex.ingest_file(target)
        return self.success("Matter transfigured.")

    def _broadcast_change(self, rel_path: str, update_type: str):
        """[THE NERVOUS SYSTEM] Signals the VS Code Scrying Pool."""
        self.logger.info(f"Broadcast: {update_type} on {rel_path}", tags=["NEURAL_LINK"], extra_payload={
            "method": "scaffold/fileChanged",
            "params": {"uri": f"scaffold-remote:/{rel_path}", "type": update_type}
        })