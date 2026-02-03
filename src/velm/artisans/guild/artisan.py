# Path: artisans/guild/artisan.py
# -------------------------------

import json
from pathlib import Path
from typing import Dict, List, Optional

from rich.table import Table
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GuildRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import atomic_write
from .registry import GuildRegistry
from .packer import GuildPacker


@register_artisan("guild")
class GuildArtisan(BaseArtisan[GuildRequest]):
    """
    =================================================================================
    == THE GUILD NEXUS (V-Ω-FEDERATED-GNOSIS)                                      ==
    =================================================================================
    LIF: 100,000,000,000

    The Sovereign of Shared Wisdom. It manages the flow of Gnosis between the
    Architect's local forge and the collective consciousness of the Guild.
    """

    def execute(self, request: GuildRequest) -> ScaffoldResult:
        self.registry = GuildRegistry(self.engine)
        self.packer = GuildPacker(self.project_root)

        if request.guild_command == "publish":
            return self._conduct_publish_rite(request)
        elif request.guild_command == "join":
            return self._conduct_join_rite(request)
        elif request.guild_command == "update":
            return self._conduct_update_rite(request)
        elif request.guild_command == "list":
            return self._conduct_list_rite(request)

        return self.failure(f"Unknown Guild rite: {request.guild_command}")

    def _conduct_publish_rite(self, request: GuildRequest) -> ScaffoldResult:
        """Bundles a local archetype and transmits it to the celestial registry."""
        if not request.target:
            return self.failure("Publishing requires a target archetype name.")

        self.logger.info(f"Preparing to publish archetype '[cyan]{request.target}[/cyan]'...")

        # 1. Pack the Gnosis
        bundle_path = self.packer.pack_archetype(request.target)
        if not bundle_path:
            raise ArtisanHeresy(f"Archetype '{request.target}' not found in local forge.")

        self.logger.info(f"Gnosis bundled at {bundle_path.name}. Transmitting...")

        # 2. Push to Registry (Abstracted)
        # In V1, this might push to S3, Git, or a dedicated API.
        # We simulate a "Remote" copy for now or push to a configured upstream.
        remote_uri = self.registry.get_upstream_uri(request.name or "default")

        if remote_uri:
            self.registry.push_bundle(bundle_path, remote_uri)
            return self.success(f"Archetype published to {remote_uri}")
        else:
            # Fallback: Just return the bundle path for manual distribution
            return self.success(
                f"Bundle created. No upstream configured. Share this file manually.",
                artifacts=[Artifact(path=bundle_path, type="file", action="created")]
            )

    def _conduct_join_rite(self, request: GuildRequest) -> ScaffoldResult:
        """Subscribes to a remote Guild."""
        if not request.target:
            return self.failure("Joining requires a Guild URI (git URL, s3://, or http://).")

        guild_alias = request.name or request.target.split('/')[-1].replace('.git', '')

        self.logger.info(f"Initiating communion with Guild '[cyan]{guild_alias}[/cyan]' at {request.target}...")

        # 1. Fetch
        local_guild_path = self.registry.fetch_guild(request.target, guild_alias)

        # 2. Link / Merge Configs
        self.registry.link_guild_resources(local_guild_path)

        return self.success(f"Joined Guild '{guild_alias}'. Gnosis synchronized.")

    def _conduct_update_rite(self, request: GuildRequest) -> ScaffoldResult:
        """Refreshes Gnosis from all subscribed Guilds."""
        updated = self.registry.update_all()
        return self.success(f"Updated {updated} Guild subscriptions.")

    def _conduct_list_rite(self, request: GuildRequest) -> ScaffoldResult:
        subscriptions = self.registry.list_subscriptions()

        table = Table(title="Guild Subscriptions")
        table.add_column("Alias", style="cyan")
        table.add_column("URI", style="dim")
        table.add_column("Last Sync", style="green")

        for sub in subscriptions:
            table.add_row(sub['alias'], sub['uri'], sub['last_sync'])

        self.console.print(table)
        return self.success("Guild roster proclaimed.")