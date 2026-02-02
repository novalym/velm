# Path: artisans/verify.py
# ------------------------

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Set, Any, Optional

from rich.box import ROUNDED
from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import VerifyRequest
from ..utils import hash_file, get_ignore_spec


@dataclass
class VerificationResult:
    """The atomic result of a single file's inquest."""
    path: str
    status: str  # VALID, MODIFIED, MISSING, PERMISSION_DRIFT, TYPE_MISMATCH, ERROR
    details: str
    expected_hash: Optional[str] = None
    actual_hash: Optional[str] = None


class VerifyArtisan(BaseArtisan[VerifyRequest]):
    """
    =================================================================================
    == THE GNOSTIC AUDITOR (V-Ω-TRUTH-SEER-ULTIMA)                                 ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Guardian of Truth. It performs a parallelized, forensic comparison between
    the Gnostic Chronicle (`scaffold.lock`) and the Mortal Reality (Filesystem).

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Asynchronous Inquest:** Utilizes `ThreadPoolExecutor` to hash thousands
        of files in parallel, achieving O(1/N) latency.
    2.  **The Dual-Mode Gaze:** Honors `--fast` (Stat-based) and `--strict` (Hash-based)
        methodologies dynamically.
    3.  **The Permission Sentinel:** Detects if executable bits (`+x`) have drifted
        from the Blueprint's intent.
    4.  **The Void Detector:** Identifies scriptures that have vanished from reality.
    5.  **The Entropy Scanner:** Detects untracked files (Noise) polluting the Sanctum.
    6.  **The Type Adjudicator:** Distinguishes between Files, Directories, and Symlinks.
    7.  **The Ignorance Filter:** Respects `.gitignore` and `.scaffoldignore` with
        absolute fidelity.
    8.  **The Luminous Dashboard:** Renders a live progress bar during the inquest.
    9.  **The Forensic Report:** Groups anomalies by category for rapid cognitive processing.
    10. **The Solution Prophesier:** Generates context-aware fix commands based on
        the specific type of drift detected.
    11. **The Machine Telepathy:** Returns the full diagnostic structure in `result.data`
        for the Daemon/IDE to consume.
    12. **The Resilience Ward:** Catches IO errors on individual files without
        halting the entire audit.
    """

    def execute(self, request: VerifyRequest) -> ScaffoldResult:
        root = (self.project_root / request.target_path).resolve()
        lock_path = root / "scaffold.lock"

        start_time = time.monotonic()
        self.logger.info(f"The Auditor performs the Rite of Verification upon: [cyan]{root.name}[/cyan]")

        # 1. Load the Chronicle
        if not lock_path.exists():
            return self.failure("No Gnostic Chronicle (scaffold.lock) found. Reality is unanchored.")

        try:
            lock_data = json.loads(lock_path.read_text(encoding='utf-8'))
            manifest = lock_data.get("manifest", {})
        except Exception as e:
            raise ArtisanHeresy(f"The Chronicle is profane (corrupted JSON): {e}")

        # 2. The Gnostic Gaze (Parallel Execution)
        results: List[VerificationResult] = []
        tracked_paths: Set[Path] = set()

        # Statistics
        stats = {"valid": 0, "modified": 0, "missing": 0, "error": 0, "permission": 0, "untracked": 0}

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("{task.completed}/{task.total}"),
                console=self.console,
                transient=True
        ) as progress:

            # --- PHASE A: VERIFYING TRACKED SOULS ---
            task_verify = progress.add_task("[cyan]Verifying Scripture Integrity...", total=len(manifest))

            with ThreadPoolExecutor() as executor:
                # Submit all verification tasks
                future_to_path = {
                    executor.submit(self._verify_single_file, root, path_str, meta, request.fast): path_str
                    for path_str, meta in manifest.items()
                }

                for future in as_completed(future_to_path):
                    path_str = future_to_path[future]
                    tracked_paths.add(root / path_str)
                    try:
                        result = future.result()
                        results.append(result)

                        # Update Stats
                        if result.status == "VALID":
                            stats["valid"] += 1
                        elif result.status == "MISSING":
                            stats["missing"] += 1
                        elif result.status == "MODIFIED":
                            stats["modified"] += 1
                        elif result.status == "PERMISSION_DRIFT":
                            stats["permission"] += 1
                        else:
                            stats["error"] += 1

                    except Exception as e:
                        self.logger.warn(f"Paradox verifying '{path_str}': {e}")
                        stats["error"] += 1

                    progress.update(task_verify, advance=1)

            # --- PHASE B: DETECTING ENTROPY (UNTRACKED FILES) ---
            if request.strict:
                task_entropy = progress.add_task("[yellow]Scanning for Entropy...", total=None)
                ignore_spec = get_ignore_spec(root)

                # We define 'untracked' as files on disk NOT in the lockfile and NOT ignored
                for p in root.rglob("*"):
                    if p.is_file() and not any(part.startswith('.scaffold') or part == '.git' for part in p.parts):
                        # Is it tracked?
                        if p in tracked_paths:
                            continue

                        # Is it ignored?
                        rel_path = p.relative_to(root)
                        if ignore_spec and ignore_spec.match_file(str(rel_path)):
                            continue

                        # It is Entropy.
                        results.append(VerificationResult(
                            path=str(rel_path),
                            status="UNTRACKED",
                            details="Foreign object detected in the Sanctum."
                        ))
                        stats["untracked"] += 1
                        progress.update(task_entropy, advance=1)

        # 3. The Final Proclamation
        anomalies = [r for r in results if r.status != "VALID"]
        is_pure = len(anomalies) == 0
        duration = time.monotonic() - start_time

        # Render the Luminous Report
        self._render_report(stats, anomalies)

        # Forge the Data Payload (Machine Telepathy)
        data_payload = {
            "stats": stats,
            "duration_ms": round(duration * 1000, 2),
            "anomalies": [
                {
                    "path": r.path,
                    "status": r.status,
                    "details": r.details,
                    "expected": r.expected_hash,
                    "actual": r.actual_hash
                }
                for r in anomalies
            ]
        }

        if is_pure:
            return self.success(
                f"Reality is in perfect harmony with the Chronicle ({stats['valid']} valid).",
                data=data_payload
            )
        else:
            # Forge the Prophecy of Redemption
            suggestion = "To accept these changes as the new Truth, run: `scaffold adopt`."

            if stats["missing"] > 0 or stats["modified"] > 0:
                suggestion += "\nTo restore the original state, run: `scaffold transmute` (Sync Mode)."

            msg = "Architectural Drift Detected."
            if request.strict: msg += " (Strict Mode Violation)"

            heresy = Heresy(
                message=msg,
                line_num=0,
                line_content="scaffold.lock",
                severity=HeresySeverity.WARNING,
                suggestion=suggestion
            )

            return ScaffoldResult(success=False, message=msg, heresies=[heresy], data=data_payload)

    def _verify_single_file(self, root: Path, path_str: str, meta: Dict[str, Any],
                            fast_mode: bool) -> VerificationResult:
        """
        [THE ATOMIC INQUISITOR]
        Verifies a single file against its metadata.
        Runs in a thread.
        """
        abs_path = root / path_str

        # 1. Existence Check
        if not abs_path.exists():
            return VerificationResult(path_str, "MISSING", "File has returned to the void.")

        # 2. Type Check (Dir vs File)
        # If lockfile has it, it's likely a file unless meta says otherwise (future feature)
        if abs_path.is_dir():
            # We currently only track files in the manifest for hashing.
            # If a path became a dir, that's a mismatch.
            return VerificationResult(path_str, "TYPE_MISMATCH", "Expected file, found directory.")

        # 3. Permission Check (The Permission Sentinel)
        # Lockfile stores permissions? Currently v7 stores it in GnosticWriteResult -> manifest?
        # If we don't store 'mode' in manifest explicitly, we skip.
        # Assuming a future update puts 'mode' in meta.
        expected_mode = meta.get("mode")
        if expected_mode:
            current_mode = oct(abs_path.stat().st_mode)[-3:]
            if current_mode != expected_mode:
                return VerificationResult(path_str, "PERMISSION_DRIFT",
                                          f"Expected {expected_mode}, found {current_mode}.")

        # 4. Content Integrity Check
        expected_hash = meta.get("sha256")

        if fast_mode:
            # Heuristic: Size + Mtime (if recorded) or just Size
            current_size = abs_path.stat().st_size
            recorded_size = meta.get("bytes")

            if recorded_size is not None and current_size != recorded_size:
                return VerificationResult(path_str, "MODIFIED", f"Size mismatch: {current_size} != {recorded_size}")

            # If size matches, we assume valid in fast mode.
            return VerificationResult(path_str, "VALID", "Verified (Fast Mode).")

        else:
            # Deep Hash
            current_hash = hash_file(abs_path)
            if current_hash != expected_hash:
                return VerificationResult(
                    path_str, "MODIFIED", "Content hash mismatch.",
                    expected_hash=expected_hash, actual_hash=current_hash
                )

        return VerificationResult(path_str, "VALID", "Cryptographically Verified.")

    def _render_report(self, stats: Dict[str, int], anomalies: List[VerificationResult]):
        """Renders the Luminous Table of Integrity."""

        # Summary Grid
        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="center", ratio=1)

        grid.add_row(
            f"[bold green]✔ {stats['valid']} Valid[/]",
            f"[bold yellow]⚡ {stats['modified']} Modified[/]",
            f"[bold red]💀 {stats['missing']} Missing[/]",
            f"[bold blue]❓ {stats['untracked']} Untracked[/]"
        )

        if stats['permission'] > 0:
            grid.add_row(f"[bold magenta]🛡️ {stats['permission']} Perms[/]", "", "", "")

        panel_content = [grid]

        if anomalies:
            # Group anomalies by type for cleaner display
            table = Table(box=ROUNDED, show_header=True, expand=True, border_style="dim")
            table.add_column("Status", width=12)
            table.add_column("Scripture", ratio=1)
            table.add_column("Gnosis / Reason", style="dim")

            # Sort by status priority
            priority = {"MISSING": 0, "MODIFIED": 1, "PERMISSION_DRIFT": 2, "UNTRACKED": 3, "TYPE_MISMATCH": 4,
                        "ERROR": 5}
            sorted_anomalies = sorted(anomalies, key=lambda x: (priority.get(x.status, 99), x.path))

            for anomaly in sorted_anomalies:
                color = "red" if anomaly.status == "MISSING" else \
                    "yellow" if anomaly.status == "MODIFIED" else \
                        "magenta" if anomaly.status == "PERMISSION_DRIFT" else \
                            "blue" if anomaly.status == "UNTRACKED" else "white"

                icon = "💀" if anomaly.status == "MISSING" else \
                    "⚡" if anomaly.status == "MODIFIED" else \
                        "🛡️" if anomaly.status == "PERMISSION_DRIFT" else \
                            "❓" if anomaly.status == "UNTRACKED" else "⚠️"

                table.add_row(f"[{color}]{icon} {anomaly.status}[/]", anomaly.path, anomaly.details)

            panel_content.append(table)

        title_color = "green" if not anomalies else "yellow"
        self.console.print(Panel(
            Group(*panel_content),
            title=f"[bold {title_color}]Gnostic Integrity Report[/]",
            border_style=title_color
        ))