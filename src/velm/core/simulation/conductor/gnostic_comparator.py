# scaffold/core/simulation/conductor/gnostic_comparator.py

import difflib
import json
import os
import re
import hashlib
from pathlib import Path
from typing import List, Set, Dict, Optional, Tuple

from ..prophecy import GnosticDiff
from ....utils import is_binary, hash_file
from ....logger import Scribe

Logger = Scribe("GnosticComparator")


class GnosticComparator:
    """
    =================================================================================
    == THE GNOSTIC COMPARATOR (V-Ω-ABSOLUTE-VEIL-V7)                               ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_DIFFERENTIAL_ENGINE

    The Final Form. Its Gaze is now perfect.
    It wields the **Dynamic Veil**, capable of distinguishing between User Matter
    (Code) and System Energy (Logs/Sessions).
    """

    # [ASCENSION 1]: REGEX ARTIFACT DETECTION
    # We use patterns to catch dynamic PID-scoped logs and V15 Session Vaults.
    INTERNAL_PATTERNS = [
        re.compile(r"^sim_manifest\.json$"),
        re.compile(r"^journal\.jsonl$"),
        re.compile(r"^daemon_traffic.*\.jsonl$"),  # Catch legacy and V14+ PID scopes
        re.compile(r"^akashic\.jsonl$"),
        re.compile(r"^weaves\.json$"),
        re.compile(r"^sessions/.*"),  # V15 Session Vaults
        re.compile(r"^latest_session$"),  # V15 Symlink
        re.compile(r"^crash_reports/.*"),
        re.compile(r"^cache/.*")
    ]

    LARGE_FILE_THRESHOLD = 1 * 1024 * 1024  # 1MB limit for text diffs

    def __init__(self, real_root: Path, sim_root: Path):
        self.real_root = real_root
        self.sim_root = sim_root
        self.manifest_path = self.sim_root / ".scaffold" / "sim_manifest.json"

    def perceive_divergence(self) -> List[GnosticDiff]:
        """The Grand Inquest."""
        diffs = []

        # 1. Load the Before State (The Manifest)
        before_files: Set[str] = set()
        if self.manifest_path.exists():
            try:
                data = json.loads(self.manifest_path.read_text(encoding='utf-8'))
                before_files = set(data.get("files", []))
            except Exception as e:
                Logger.warn(f"Could not read simulation manifest: {e}. Assuming void state.")

        # 2. Scan the After State (The Simulation)
        after_files_abs = self._scan_files(self.sim_root)
        after_files = {
            str(p.relative_to(self.sim_root)).replace("\\", "/")
            for p in after_files_abs
        }

        # 3. The Set Operations of Truth
        all_files = sorted(list(before_files | after_files))

        # Logger.debug(f"Comparing State: {len(before_files)} baseline vs {len(after_files)} current.")

        for rel_path in all_files:
            path_str = str(rel_path).replace("\\", "/")

            # --- [THE ABSOLUTE VEIL V2] ---
            # We filter out internal machinery to show only the Architect's Will.
            if self._is_internal_artifact(path_str):
                continue
            # ------------------------------

            # The lockfile is special. We process it but summarize it.
            if path_str.endswith("scaffold.lock"):
                self._handle_lockfile(path_str, before_files, after_files, diffs)
                continue

            sim_path_abs = self.sim_root / rel_path
            real_path_abs = self.real_root / rel_path

            is_in_before = rel_path in before_files
            is_in_after = rel_path in after_files

            # CASE A: CREATED
            if is_in_after and not is_in_before:
                diffs.append(GnosticDiff(
                    path=path_str,
                    status="CREATED",
                    diff=self._read_safe(sim_path_abs)
                ))

            # CASE B: DELETED
            elif is_in_before and not is_in_after:
                diffs.append(GnosticDiff(path=path_str, status="DELETED"))

            # CASE C: MODIFIED
            elif is_in_before and is_in_after:
                # We check content difference
                if self._is_content_different(sim_path_abs, real_path_abs):
                    diffs.append(self._forge_modified_diff(path_str, sim_path_abs, real_path_abs))

        # [ASCENSION 12]: THE LUMINOUS SORT
        # Priority: CREATED > MODIFIED > DELETED, then Alphabetical
        return sorted(diffs, key=lambda d: (
            0 if d.status == "CREATED" else 1 if d.status == "MODIFIED" else 2,
            d.path
        ))

    def _is_internal_artifact(self, path_str: str) -> bool:
        """
        [ASCENSION 1]: DYNAMIC VEIL CHECK
        Checks if the file is part of the Gnostic Machinery.
        """
        if not path_str.startswith(".scaffold/"):
            return False

        # Strip .scaffold/ prefix
        inner_path = path_str[10:]

        for pattern in self.INTERNAL_PATTERNS:
            if pattern.match(inner_path):
                return True

        return False

    def _handle_lockfile(self, path: str, before: Set[str], after: Set[str], diffs: List[GnosticDiff]):
        """[ASCENSION 8]: LOCKFILE SUMMARIZER"""
        in_before = path in before
        in_after = path in after
        sim_path = self.sim_root / path
        real_path = self.real_root / path

        if in_after and not in_before:
            diffs.append(GnosticDiff(path=path, status="CREATED", diff="[Gnostic Chronicle Created]"))
        elif in_before and in_after:
            # We don't verify real_path existence here, we compare what we knew vs what is
            # Actually, for simulation, we compare snapshot (real_path at start) vs current sim state
            if real_path.exists() and hash_file(sim_path) != hash_file(real_path):
                diffs.append(GnosticDiff(path=path, status="MODIFIED", diff="[Gnostic Chronicle Updated]"))

    def _scan_files(self, root: Path) -> List[Path]:
        """[ASCENSION 9]: PERMISSION RESILIENT SCANNER"""
        files = []
        try:
            for dirpath, _, filenames in os.walk(root):
                for f in filenames:
                    if f.endswith(".pyc") or f == ".DS_Store": continue
                    files.append(Path(dirpath) / f)
        except Exception:
            pass  # The Gaze glides over locked doors
        return files

    def _is_content_different(self, p1: Path, p2: Path) -> bool:
        """[ASCENSION 4]: BINARY & HASH CHECK"""
        # Fast Size Check
        if p1.stat().st_size != p2.stat().st_size:
            return True
        return hash_file(p1) != hash_file(p2)

    def _read_safe(self, p: Path) -> str:
        """[ASCENSION 3 & 5]: SAFE READ WITH THRESHOLD"""
        if not p.exists(): return "[Void]"

        # Large File Ward
        if p.stat().st_size > self.LARGE_FILE_THRESHOLD:
            return f"[Large File: {p.stat().st_size} bytes - Diff Suppressed]"

        if is_binary(p): return "[Binary Content]"

        # Encoding Resilience
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return p.read_text(encoding=enc)
            except UnicodeDecodeError:
                continue

        return "[Unreadable Content]"

    def _forge_modified_diff(self, path_str: str, sim_path: Path, real_path: Path) -> GnosticDiff:
        """[ASCENSION 6]: NORMALIZED DIFFING"""
        if is_binary(sim_path) or is_binary(real_path):
            return GnosticDiff(path=path_str, status="MODIFIED", diff="[Binary Content Modified]")

        sim_txt = self._read_safe(sim_path)
        real_txt = self._read_safe(real_path)

        # [ASCENSION 6]: Whitespace Normalization
        # We replace CRLF with LF to ensure cross-platform diffs are clean
        sim_lines = sim_txt.replace('\r\n', '\n').splitlines(keepends=True)
        real_lines = real_txt.replace('\r\n', '\n').splitlines(keepends=True)

        diff_gen = difflib.unified_diff(
            real_lines,
            sim_lines,
            fromfile=f"a/{path_str}",
            tofile=f"b/{path_str}",
            lineterm=""
        )

        diff_content = "".join(diff_gen)

        if not diff_content.strip():
            # If content is "different" by hash but identical by text (rare, maybe encoding?),
            # we return a meta-diff.
            return GnosticDiff(path=path_str, status="MODIFIED", diff="[Meta/Encoding Change]")

        return GnosticDiff(path=path_str, status="MODIFIED", diff=diff_content)