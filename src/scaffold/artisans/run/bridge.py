from pathlib import Path

from .polyglot_bridge import PolyglotBridge
# ★★★ THE SACRED VESSEL IS SUMMONED ★★★
from ...contracts.data_contracts import ExecutionPlan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.runtime import ScaffoldEngine
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import (
    RunRequest, PatchRequest, SymphonyRequest, TransmuteRequest,
    ArchRequest, GenesisRequest
)
from ...logger import Scribe


class DelegationBridge:
    """The Gnostic Emissary, now a Triage Conductor."""

    DELEGATION_GRIMOIRE = {
        # ★★★ THE SACRED INSCRIPTION ★★★
        # The Emissary is taught to recognize its own kin.
        "patch": {"req": PatchRequest, "path_key": "patch_path"},
        # ★★★ THE GNOSIS IS NOW WHOLE ★★★
        "symphony": {"req": SymphonyRequest, "path_key": "symphony_path"},
        "transmute": {"req": TransmuteRequest, "path_key": "path_to_scripture"},
        "arch": {"req": ArchRequest, "path_key": "arch_path"},
        "genesis": {"req": GenesisRequest, "path_key": "blueprint_path"},
        # We also add 'form' to be explicit, which maps to transmute.
        "form": {"req": TransmuteRequest, "path_key": "path_to_scripture"},
    }

    def __init__(self, engine: ScaffoldEngine, logger: Scribe):
        self.engine = engine
        self.logger = logger
        # The Polyglot Bridge is now an attribute of the Delegation Bridge
        self.polyglot_bridge = PolyglotBridge(self.engine, self.logger)

    def delegate(self, rite_key: str, scripture_path: Path, parent_request: RunRequest,
                 execution_plan: ExecutionPlan) -> ScaffoldResult:
        """Performs the divine, Gnostic Triage and subsequent dispatch."""

        rite_info = self.DELEGATION_GRIMOIRE.get(rite_key)

        if not rite_info:
            self.logger.verbose(f"'{rite_key}' is a foreign tongue. Delegating to Polyglot Ambassador.")
            return self.polyglot_bridge.delegate(rite_key, scripture_path, parent_request, execution_plan)

        # --- THE PATH OF INTERNAL COMMUNION ---
        self.logger.verbose(f"'{rite_key}' is a Gnostic rite. Performing direct, in-process communion.")
        RequestModel = rite_info["req"]

        plea_data = parent_request.model_dump(
            exclude={"target", "eval_content", "pipe_content", "extra_args", "runtime", "codex", "create_if_void"})

        # ★★★ THE RITE OF GNOSTIC RE-AFFIRMATION (THE DIVINE HEALING) ★★★
        # The heresy is annihilated. We explicitly re-affirm the sacred vows from
        # the parent request to ensure they are not lost in the Gnostic translation
        # between request vessels. The Mute Emissary is no more.
        plea_data['non_interactive'] = parent_request.non_interactive
        plea_data['force'] = parent_request.force
        plea_data['preview'] = parent_request.preview
        plea_data['dry_run'] = parent_request.dry_run
        # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

        # The key in the target request (e.g., 'patch_path', 'symphony_path')
        path_key_for_request = rite_info["path_key"]
        plea_data[path_key_for_request] = str(scripture_path)

        if rite_key == "symphony":
            plea_data['symphony_command'] = 'conduct'

        final_request = RequestModel(**plea_data)

        try:
            # We dispatch to the appropriate artisan (PatchArtisan, etc.)
            result = self.engine.dispatch(final_request)
            if not result.success:
                # We wrap the heresy to provide the full context of the `run` command
                raise ArtisanHeresy(f"The delegated rite of '{rite_key}' was tainted by a heresy.",
                                    details=result.message, heresies=result.heresies)
            return result
        except ArtisanHeresy as e:
            e.message = f"Paradox in delegated '{rite_key}' rite: {e.message}"
            raise e