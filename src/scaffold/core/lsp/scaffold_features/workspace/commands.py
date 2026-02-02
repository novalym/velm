# Path: core/lsp/scaffold_features/workspace/commands.py
# ------------------------------------------------------
import logging
from typing import List, Any, Dict
from ...base.features.workspace.commands.router import CommandRouter
from ...base.utils.uri import UriUtils

Logger = logging.getLogger("ScaffoldCommands")


class ScaffoldCommandProvider:
    """
    [THE HAND OF THE MAESTRO]
    Defines the actual logic for Scaffold-specific kinetic commands.
    """

    def __init__(self, server: Any):
        self.server = server

    def register_rites(self, router: CommandRouter):
        """Binds Gnostic string IDs to internal Python methods."""
        router.register("scaffold.heal", self.h_heal)
        router.register("scaffold.transmute", self.h_transmute)
        router.register("scaffold.architect.fix", self.h_architect_fix)
        router.register("scaffold.runRite", self.h_run_generic_rite)

    def h_heal(self, uri: str, diagnostic: Dict[str, Any]):
        """[RITE]: HEAL - Dispatches the RepairArtisan."""
        if not hasattr(self.server, 'relay_request'): return

        fs_path = str(UriUtils.to_fs_path(uri))
        Logger.info(f"Initiating Redemption for: {fs_path}")

        return self.server.relay_request("repair", {
            "file_path": fs_path,
            "heresy_key": diagnostic.get("code"),
            "context": {"diagnostic": diagnostic}
        })

    def h_transmute(self, uri: str):
        """[RITE]: TRANSMUTE - Syncs blueprint to disk."""
        fs_path = str(UriUtils.to_fs_path(uri))
        return self.server.relay_request("transmute", {
            "path_to_scripture": fs_path
        })

    def h_architect_fix(self, uri: str, context: Any):
        """[RITE]: NEURAL_FIX - Summons the AI Architect."""
        return self.server.relay_request("architect", {
            "mode": "fix",
            "file_path": str(UriUtils.to_fs_path(uri)),
            "context": context
        })

    def h_run_generic_rite(self, rite_name: str, params: Dict[str, Any]):
        """[RITE]: GENERIC_GATEWAY - Routes any registered artisan."""
        return self.server.relay_request(rite_name, params)