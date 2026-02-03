# Path: artisans/guild/registry.py
# --------------------------------

import json
import shutil
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from ...contracts.heresy_contracts import ArtisanHeresy


class GuildRegistry:
    """The Librarian of the Federated Networks."""

    GUILDS_ROOT = Path.home() / ".scaffold" / "guilds"
    CONFIG_PATH = Path.home() / ".scaffold" / "guild_subscriptions.json"

    def __init__(self, engine):
        self.engine = engine
        self.GUILDS_ROOT.mkdir(parents=True, exist_ok=True)
        if not self.CONFIG_PATH.exists():
            self.CONFIG_PATH.write_text("{}")

    def _load_config(self) -> Dict:
        return json.loads(self.CONFIG_PATH.read_text())

    def _save_config(self, config: Dict):
        self.CONFIG_PATH.write_text(json.dumps(config, indent=2))

    def fetch_guild(self, uri: str, alias: str) -> Path:
        """Clones or pulls the remote guild repository."""
        target_path = self.GUILDS_ROOT / alias

        # Git Strategy
        if uri.endswith(".git") or uri.startswith("git@") or uri.startswith("https://github"):
            if target_path.exists():
                subprocess.run(["git", "pull"], cwd=target_path, check=True)
            else:
                subprocess.run(["git", "clone", uri, str(target_path)], check=True)

        # S3/HTTP Strategy (Prophecy)
        # else: ...

        # Save subscription
        config = self._load_config()
        config[alias] = {"uri": uri, "last_sync": time.ctime(), "path": str(target_path)}
        self._save_config(config)

        return target_path

    def update_all(self) -> int:
        config = self._load_config()
        count = 0
        for alias, info in config.items():
            try:
                self.fetch_guild(info["uri"], alias)
                count += 1
            except Exception as e:
                print(f"Failed to update guild '{alias}': {e}")
        return count

    def link_guild_resources(self, guild_path: Path):
        """
        Merges Guild templates and policies into the Global Forge.
        Uses symlinks to keep them live-updated.
        """
        # 1. Templates
        src_templates = guild_path / "templates"
        dest_templates = Path.home() / ".scaffold" / "templates" / f"guild_{guild_path.name}"

        if src_templates.exists():
            if dest_templates.exists() or dest_templates.is_symlink():
                # Idempotent cleanup
                if dest_templates.is_dir() and not dest_templates.is_symlink():
                    shutil.rmtree(dest_templates)
                else:
                    dest_templates.unlink()

            # Create Symlink
            try:
                dest_templates.symlink_to(src_templates)
            except OSError:
                # Fallback for Windows without Admin: Copy
                shutil.copytree(src_templates, dest_templates)

        # 2. Policies (Future: Merge JSONs)

    def list_subscriptions(self) -> List[Dict]:
        config = self._load_config()
        return [{"alias": k, **v} for k, v in config.items()]

    def get_upstream_uri(self, alias: str) -> Optional[str]:
        return self._load_config().get(alias, {}).get("uri")

    def push_bundle(self, bundle_path: Path, uri: str):
        # Implementation depends on protocol. For Git, commit and push?
        pass

