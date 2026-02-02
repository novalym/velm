# Path: artisans/schema/engine.py
# -------------------------------

import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Optional

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("SchemaEngineCore")


class SchemaEngine:
    """
    The Polyglot Adapter for ORMs.
    Currently supports: Alembic (Python), Prisma (Node/Python).
    """

    def __init__(self, root: Path):
        self.root = root

    def divine_stack(self) -> str:
        """Determines which ORM is governing the sanctum."""
        if (self.root / "alembic.ini").exists():
            return "alembic"
        if (self.root / "prisma" / "schema.prisma").exists() or (self.root / "schema.prisma").exists():
            return "prisma"
        return "unknown"

    def check_drift(self, stack: str) -> Tuple[bool, str]:
        """
        Returns (has_drift, details).
        """
        if stack == "alembic":
            # Alembic check returns non-zero if drift?
            # Usually `alembic check` exists in newer versions.
            try:
                res = subprocess.run(
                    ["alembic", "check"],
                    cwd=self.root, capture_output=True, text=True
                )
                if res.returncode != 0:
                    return True, res.stdout or res.stderr
                return False, "Models match Migration History."
            except FileNotFoundError:
                # Fallback check
                return False, "Alembic check command not found (old version?)"

        elif stack == "prisma":
            # Prisma migrate status
            # Exit code 1 usually means drift or unapplied migrations
            res = subprocess.run(
                ["npx", "prisma", "migrate", "status"],
                cwd=self.root, capture_output=True, text=True
            )
            # Prisma output needs parsing.
            if "Following migration have not yet been applied" in res.stdout:
                return True, "Pending migrations detected."
            if "Database schema is not in sync" in res.stdout:
                return True, "Schema drift detected."
            return False, "Sync."

        return False, "Unknown stack."

    def generate_migration(self, stack: str, message: str) -> Optional[Path]:
        """
        Generates the migration file.
        """
        Logger.info(f"Forging migration for {stack}: '{message}'")

        if stack == "alembic":
            try:
                subprocess.run(
                    ["alembic", "revision", "--autogenerate", "-m", message],
                    cwd=self.root, check=True
                )
                # Find the new file (heuristic: newest in versions)
                versions = list((self.root / "alembic" / "versions").glob("*.py"))
                if versions:
                    return max(versions, key=lambda f: f.stat().st_mtime)
            except subprocess.CalledProcessError:
                raise ArtisanHeresy("Alembic failed to autogenerate. Check your model imports in env.py.")

        elif stack == "prisma":
            # Prisma `migrate dev --create-only` generates sql without applying
            try:
                subprocess.run(
                    ["npx", "prisma", "migrate", "dev", "--create-only", "--name", message],
                    cwd=self.root, check=True
                )
                # Prisma puts it in prisma/migrations/<timestamp>_name/migration.sql
                # We return the dir for now
                migrations_dir = self.root / "prisma" / "migrations"
                if migrations_dir.exists():
                    # Find newest dir
                    subdirs = [d for d in migrations_dir.iterdir() if d.is_dir()]
                    if subdirs:
                        newest = max(subdirs, key=lambda d: d.stat().st_mtime)
                        return newest / "migration.sql"
            except subprocess.CalledProcessError:
                raise ArtisanHeresy("Prisma generation failed.")

        return None

    def apply_migration(self, stack: str) -> Tuple[bool, str]:
        """
        Applies pending migrations.
        """
        Logger.info(f"Applying mutations via {stack}...")

        cmd = []
        if stack == "alembic":
            cmd = ["alembic", "upgrade", "head"]
        elif stack == "prisma":
            cmd = ["npx", "prisma", "migrate", "deploy"]

        try:
            res = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, check=True)
            return True, res.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr + e.stdout