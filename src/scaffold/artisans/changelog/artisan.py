# Path: scaffold/artisans/changelog/artisan.py
# --------------------------------------------

import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ChangelogRequest
from ...help_registry import register_artisan
from ...utils import atomic_write


@register_artisan("changelog")
class ChangelogArtisan(BaseArtisan[ChangelogRequest]):
    """
    =============================================================================
    == THE CHRONICLE SCRIBE (V-Ω-CONVENTIONAL-COMMITS)                         ==
    =============================================================================
    LIF: 10,000,000,000

    Parses git history into a human-readable CHANGELOG.md.
    """

    # Regex for "type(scope): description"
    COMMIT_REGEX = re.compile(r"^(\w+)(?:\(([^)]+)\))?:\s*(.*)")

    TYPE_MAP = {
        "feat": "✨ Features",
        "fix": "🐛 Bug Fixes",
        "docs": "📚 Documentation",
        "style": "💎 Styling",
        "refactor": "♻️ Refactoring",
        "perf": "🚀 Performance",
        "test": "🧪 Testing",
        "chore": "🔧 Chore",
        "build": "👷 Build System",
        "ci": "💚 CI"
    }

    def execute(self, request: ChangelogRequest) -> ScaffoldResult:
        if not (self.project_root / ".git").is_dir():
            return self.failure("This sanctum is not a Git repository.")

        # 1. Determine Range
        start_ref = request.from_ref
        if not start_ref:
            start_ref = self._get_latest_tag()

        range_spec = f"{start_ref}..HEAD" if start_ref else "HEAD"
        self.logger.info(f"Reading Chronicle from [cyan]{range_spec}[/cyan]...")

        # 2. Harvest Commits
        commits = self._get_commits(range_spec)
        if not commits:
            return self.success("No changes detected in the timeline.")

        # 3. Categorize
        groups = defaultdict(list)
        for subject, hash_short in commits:
            match = self.COMMIT_REGEX.match(subject)
            if match:
                ctype, scope, desc = match.groups()
                category = self.TYPE_MAP.get(ctype, "Other")
                entry = f"- **{scope}:** {desc}" if scope else f"- {desc}"
            else:
                category = "Other"
                entry = f"- {subject}"

            groups[category].append(f"{entry} ({hash_short})")

        # 4. Forge Markdown
        version_title = request.next_version or "Unreleased"
        date_str = time.strftime("%Y-%m-%d")

        lines = [f"## {version_title} ({date_str})"]

        for category, title in self.TYPE_MAP.items():  # Use order from map
            if title in groups:
                lines.append(f"\n### {title}")
                lines.extend(groups[title])

        if "Other" in groups:
            lines.append("\n### 📜 Other Changes")
            lines.extend(groups["Other"])

        lines.append("\n---")
        new_entry = "\n".join(lines)

        # 5. Inscribe
        changelog_path = self.project_root / request.output_file

        current_content = ""
        if changelog_path.exists():
            current_content = changelog_path.read_text(encoding='utf-8')
            # Prepend new entry
            final_content = f"# Changelog\n\n{new_entry}\n\n" + current_content.replace("# Changelog\n\n", "")
        else:
            final_content = f"# Changelog\n\n{new_entry}\n"

        atomic_write(changelog_path, final_content, self.logger, self.project_root)

        return self.success(
            f"Changelog updated for {version_title}.",
            artifacts=[Artifact(path=changelog_path, type="file", action="modified")]
        )

    def _get_latest_tag(self) -> Optional[str]:
        try:
            return subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=self.project_root, text=True, stderr=subprocess.DEVNULL
            ).strip()
        except subprocess.CalledProcessError:
            return None  # No tags found, start from beginning

    def _get_commits(self, range_spec: str) -> List[tuple]:
        """Returns list of (subject, hash) tuples."""
        # Use simple log if no range (i.e. first run)
        cmd = ["git", "log", "--pretty=format:%s|%h"]
        if ".." in range_spec:
            cmd.append(range_spec)

        try:
            output = subprocess.check_output(cmd, cwd=self.project_root, text=True)
            commits = []
            for line in output.splitlines():
                if "|" in line:
                    subject, h = line.rsplit("|", 1)
                    commits.append((subject, h))
            return commits
        except subprocess.CalledProcessError:
            return []