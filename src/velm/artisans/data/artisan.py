# Path: artisans/data/artisan.py
# ------------------------------

import re
import json
import shutil
import time
from pathlib import Path
from typing import Generator, Any, Dict, List

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import DataRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import atomic_write, get_human_readable_size

# Lazy load faker to avoid startup cost
try:
    from faker import Faker

    FAKE = Faker()
except ImportError:
    FAKE = None


@register_artisan("data")
class DataArtisan(BaseArtisan[DataRequest]):
    """
    =================================================================================
    == THE ALCHEMIST OF STATE (V-Ω-SANITIZING-STREAM)                              ==
    =================================================================================
    LIF: 10,000,000,000

    Manages the fluid essence of the application. It treats data not as static
    bytes, but as a living stream that must be purified (sanitized) before it
    leaves the production sanctum.
    """

    # Gnostic Regex for PII detection
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_REGEX = re.compile(r'\b\+?1?\d{9,15}\b')

    def execute(self, request: DataRequest) -> ScaffoldResult:
        if request.data_command == "clone":
            return self._conduct_clone_rite(request)
        elif request.data_command == "snapshot":
            return self._conduct_snapshot_rite(request)
        elif request.data_command == "seed":
            return self._conduct_seed_rite(request)

        return self.failure(f"Unknown data rite: {request.data_command}")

    def _conduct_clone_rite(self, request: DataRequest) -> ScaffoldResult:
        """
        Stream data from Source to Destination, applying the Mask of Anonymity.
        """
        source = request.source
        dest = request.destination or "local_dump.json"

        if not source:
            raise ArtisanHeresy("The Clone Rite requires a source.")

        self.logger.info(f"Initiating Data Clone from [cyan]{source}[/cyan] to [cyan]{dest}[/cyan]...")

        # Simulating a stream from a source (File or Mock DB)
        # In a real implementation, this would connect to Postgres/MySQL
        try:
            source_path = Path(source)
            if not source_path.exists():
                raise ArtisanHeresy(f"Source void: {source}")

            # We perform the transmutation line by line to simulate streaming
            processed_lines = []

            with open(source_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if request.anonymize:
                        line = self._sanitize_line(line)
                    processed_lines.append(line)

            # Inscribe result
            dest_path = self.project_root / dest
            atomic_write(dest_path, "".join(processed_lines), self.logger, self.project_root)

            return self.success(
                f"Data cloned and purified.",
                artifacts=[Artifact(path=dest_path, type="file", action="created")]
            )

        except Exception as e:
            raise ArtisanHeresy(f"The Transmutation of State failed: {e}", child_heresy=e)

    def _sanitize_line(self, text: str) -> str:
        """The Mask of Anonymity."""

        def replace_email(match):
            return FAKE.email() if FAKE else "redacted@example.com"

        def replace_phone(match):
            return FAKE.phone_number() if FAKE else "+15550000000"

        text = self.EMAIL_REGEX.sub(replace_email, text)
        text = self.PHONE_REGEX.sub(replace_phone, text)
        return text

    def _conduct_snapshot_rite(self, request: DataRequest) -> ScaffoldResult:
        """Freezes the current state into a time capsule."""
        name = request.snapshot_name or f"snapshot_{int(time.time())}"
        target_dir = self.project_root / ".scaffold" / "snapshots" / name

        if target_dir.exists():
            raise ArtisanHeresy(f"Snapshot '{name}' already exists.")

        self.logger.info(f"Freezing state to [cyan]{target_dir}[/cyan]...")

        try:
            # Heuristic: Snapshot 'data', 'db', or 'storage' directories
            target_dir.mkdir(parents=True)
            sources = ["data", "db", "storage", ".sqlite"]
            count = 0

            for src in sources:
                src_path = self.project_root / src
                if src_path.exists():
                    if src_path.is_file():
                        shutil.copy2(src_path, target_dir / src_path.name)
                    else:
                        shutil.copytree(src_path, target_dir / src)
                    count += 1

            if count == 0:
                self.logger.warn("No obvious state containers found (data/db). Snapshot is empty.")

            return self.success(f"State frozen: {name}")

        except Exception as e:
            raise ArtisanHeresy(f"Snapshot failed: {e}")

    def _conduct_seed_rite(self, request: DataRequest) -> ScaffoldResult:
        """Summons the Demiurge to populate the void."""
        if not FAKE:
            return self.failure("The 'faker' artisan is required. pip install faker")

        self.logger.info("The Alchemist creates gold from lead (Seeding)...")
        # Logic to look for a seed.py or similar
        seed_script = self.project_root / "seeds.py"
        if seed_script.exists():
            from ...utils.invocation import invoke_scaffold_command
            return invoke_scaffold_command(["run", "python", str(seed_script)], cwd=self.project_root)

        return self.success("Seeding complete (Mock).")