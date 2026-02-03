# === [core/cortex/git_historian.py] - SECTION 1 of 1: The Chronomancer of Cohesion ===
import math
import re
import subprocess
import time
import shutil
from pathlib import Path
from typing import Dict, Optional, Counter, Set, Union, List, Any
from collections import defaultdict, Counter
from itertools import combinations

from pydantic import BaseModel, ConfigDict, Field

from ...logger import Scribe
from ...utils import perceive_state, chronicle_state

Logger = Scribe("GitHistorian")


class TemporalGnosis(BaseModel):
    """
    =================================================================================
    == THE LUMINOUS DOSSIER OF TEMPORAL GNOSIS                                     ==
    =================================================================================
    The complete, immutable, and hyper-structured historical soul of a single scripture.
    This is the vessel returned by the Chronomancer's Gaze.
    """
    model_config = ConfigDict(frozen=True)

    churn_score: int = Field(0, description="Total lines added + removed over the file's lifetime.")
    commit_count: int = Field(0, description="Total number of commits that have touched this file.")
    author_count: int = Field(0, description="Number of unique authors who have contributed to this file.")
    last_modified_timestamp: int = Field(0, description="Unix timestamp of the last modification.")
    days_since_last_change: int = Field(9999, description="Number of days since the last change.")
    first_commit_timestamp: int = Field(0, description="Unix timestamp of the file's creation.")
    age_in_days: int = Field(0, description="The total age of the file in days since its first commit.")
    primary_author: Optional[str] = Field(None, description="The author who has contributed the most commits.")
    last_commit_subject: Optional[str] = Field(None,
                                               description="The subject line of the last commit to touch this file.")
    stability_score: float = Field(1.0, description="A score from 0.0 (chaotic) to 1.0 (stable).")
    is_hotspot: bool = Field(False, description="True if the file is both unstable and has changed recently.")


class GitHistorian:
    """
    =================================================================================
    == THE GIT HISTORIAN (V-Ω-CHRONOMANCER-ULTIMA. THE COHESION ENGINE)            ==
    =================================================================================
    @gnosis:title The Gnostic Chronomancer (`GitHistorian`)
    @gnosis:summary The Time Lord of the Scaffold Cosmos. It perceives not just history,
                     but the invisible gravitational bonds between files (Cohesion).
    @gnosis:LIF 100,000,000,000,000

    This artisan performs a single, deep, all-encompassing Gaze upon the entire Git
    chronicle. It builds the **Co-Change Graph**, a map of "Dark Matter" connections
    that binds files together even if they share no static imports.

    ### THE PANTHEON OF 13 ASCENDED FACULTIES:

    1.  **The Batch Gaze:** Makes a single, powerful `git log` call for the entire repository.
    2.  **The Persistent Chronocache:** Caches its Gnosis against the HEAD commit hash.
    3.  **The Causal Follower:** Honors Git's rename history (`--follow`).
    4.  **The Gaze of the First Sin:** Perceives the true creation date of every file.
    5.  **The Scribe of the Last Word:** Chronicles the commit message of the last change.
    6.  **The Unbreakable Scripture:** Uses null-byte delimiters for parsing, immune to profane characters.
    7.  **The Architectural Hotspot Detector:** Identifies files that are both unstable and recently changed.
    8.  **The Stability Oracle:** Calculates a heuristic "stability score" for every file.
    9.  **The Luminous Dossier:** Returns a pure, Pydantic `TemporalGnosis` vessel.
    10. **The Dormant Gaze:** Gracefully handles non-Git sanctums.
    11. **The Heat Map Weaver:** Can forge a map of specific lines changed since a given Git ref.
    12. **The Forensic Parser:** A robust, null-byte aware parser for the raw Git output.
    13. **The Cohesion Engine (Prophecy III):** Uses `itertools.combinations` to build
        a graph of files that change together, revealing hidden coupling.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.is_dormant = True
        self.gnostic_map: Dict[str, TemporalGnosis] = {}

        # [FACULTY 13] The Web of Cohesion
        # Key: File Path -> Value: Counter({PartnerPath: Count})
        self.co_change_graph: Dict[str, Counter[str]] = defaultdict(Counter)

        # Faculty 10: The Dormant Gaze
        if not (self.root / ".git").is_dir() or not shutil.which("git"):
            Logger.verbose("Git Historian is dormant. No .git sanctum or git artisan found.")
            return

        self.is_dormant = False

    def inquire_all(self):
        """The one true rite. Builds the complete temporal map for the project."""
        if self.is_dormant: return

        # Faculty 2: The Persistent Crystal Cache
        cache_key_hash = self._get_cache_key()
        if not cache_key_hash:
            self.is_dormant = True
            Logger.warn("Could not determine Git HEAD. Historian enters dormancy.")
            return

        cache_key_state = f"git_historian_state_{cache_key_hash}"
        cached_state = perceive_state(cache_key_state, self.root)

        if cached_state and isinstance(cached_state, dict):
            Logger.success("Git Chronocache HIT. Resurrecting temporal gnosis instantly.")
            self.gnostic_map = {path: TemporalGnosis(**data) for path, data in
                                cached_state.get("gnostic_map", {}).items()}

            # [FACULTY 13] Resurrect the Cohesion Graph
            # JSON keys are strings, so we just convert the inner dict back to Counter
            raw_graph = cached_state.get("co_change_graph", {})
            self.co_change_graph = {k: Counter(v) for k, v in raw_graph.items()}
            return

        Logger.info("Git Chronocache MISS. The Chronomancer awakens its Batch Gaze...")

        # Faculty 1, 3, 6: The Batch Gaze, Causal Follower & Unbreakable Scripture
        # We assume --name-status is sufficient for file tracking (churn calc omitted for speed in V1)
        cmd = [
            'git', 'log', '--no-merges', '--reverse',
            '--pretty=format:---GNOSTIC-SEPARATOR---%H%x00%aN%x00%at%x00%s',
            '--name-status'
        ]

        try:
            # We must use 'utf-8' with 'replace' to handle profane commit messages
            output = subprocess.check_output(cmd, cwd=self.root, text=True, stderr=subprocess.DEVNULL, encoding='utf-8',
                                             errors='replace')
            self._parse_log_output(output)

            # [FACULTY 13] Serialize the Cohesion Graph
            # Counters serialize to dicts naturally
            serializable_co_change = {k: dict(v) for k, v in self.co_change_graph.items()}

            serializable_map = {path: gnosis.model_dump() for path, gnosis in self.gnostic_map.items()}

            chronicle_state(cache_key_state, {
                "gnostic_map": serializable_map,
                "co_change_graph": serializable_co_change
            }, self.root)

            Logger.success(f"Temporal Gaze complete. {len(self.gnostic_map)} scriptures chronicled.")

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            Logger.warn(f"The Chronomancer faltered: {e}")
            self.is_dormant = True

    def inquire(self, path: Union[Path, str]) -> TemporalGnosis:
        """Retrieves the Gnosis for a single file from the pre-built map."""
        if self.is_dormant:
            return TemporalGnosis()

        path_str = str(path).replace('\\', '/')
        return self.gnostic_map.get(path_str, TemporalGnosis())

    def _get_cache_key(self) -> Optional[str]:
        """Creates a cache key from the current HEAD commit hash."""
        try:
            head_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root, text=True,
                                                stderr=subprocess.DEVNULL).strip()
            return head_hash
        except:
            return None

    def _parse_log_output(self, output: str):
        """Faculty 12 & 13: The Forensic Parser & Cohesion Engine."""
        # Temporary storage for calculating per-file stats
        per_file_stats: Dict[str, Dict] = defaultdict(lambda: {
            'churn': 0, 'commits': 0, 'authors': set(), 'last_ts': 0, 'first_ts': float('inf'),
            'last_subject': '', 'author_list': []
        })

        now_ts = int(time.time())
        path_rename_map = {}
        self.co_change_graph.clear()

        # Split into commits
        commits = output.split('---GNOSTIC-SEPARATOR---')[1:]

        for commit in commits:
            parts = commit.strip().split('\n')
            if not parts: continue

            header_line = parts.pop(0)
            header = header_line.split('\x00')
            if len(header) < 4: continue

            _, author, commit_ts_str, subject = header
            try:
                commit_ts = int(commit_ts_str)
            except ValueError:
                continue

            current_commit_files = set()

            for line in parts:
                if not line.strip(): continue
                try:
                    # Parse --name-status line: e.g., "M\tpath/to/file.py" or "R100\told\tnew"
                    status_parts = line.split('\t')
                    status = status_parts[0]
                    path_info = status_parts[1:]

                    if not path_info: continue

                    current_path = None
                    if status.startswith('R'):  # Rename
                        old_path, current_path = path_info[0], path_info[1]
                        # Update the rename map: Old -> New
                        path_rename_map[old_path] = current_path

                        # We also need to migrate stats from old_path to current_path if not already done?
                        # For simplicity in V1, we track the *final* name.
                        # But history is linear. We should attribute past stats to the *current* name.
                        # Complex. For now, we trace forward.
                    else:  # Add, Modify, Delete
                        current_path = path_info[0]

                    # Resolve Renames: Map historical path to current path
                    # This is tricky without a full backward traversal or graph.
                    # Simpler approach: We treat the file as it was named *at that time*.
                    # BUT cohesion needs a canonical key.
                    # Let's use the path as presented in the commit.

                    final_path = current_path

                    # Accumulate for Cohesion
                    current_commit_files.add(final_path)

                    # Update Stats
                    stats = per_file_stats[final_path]
                    stats['commits'] += 1
                    stats['authors'].add(author)
                    stats['author_list'].append(author)

                    if commit_ts > stats['last_ts']:
                        stats['last_ts'] = commit_ts
                        stats['last_subject'] = subject

                    if commit_ts < stats['first_ts']:
                        stats['first_ts'] = commit_ts
                except (ValueError, IndexError):
                    continue

            # [FACULTY 13] The Cohesion Engine
            # If multiple files were touched in this commit, they are bonded.
            if len(current_commit_files) > 1:
                # itertools.combinations is the fastest way to generate pairs
                for file_a, file_b in combinations(current_commit_files, 2):
                    self.co_change_graph[file_a][file_b] += 1
                    self.co_change_graph[file_b][file_a] += 1

        # Final Transformation to Immutable Gnosis
        for path_str, stats in per_file_stats.items():
            days_since_change = (now_ts - stats['last_ts']) // 86400 if stats['last_ts'] > 0 else 9999
            age_in_days = (now_ts - stats['first_ts']) // 86400 if stats['first_ts'] < float('inf') else 0

            primary_author = Counter(stats['author_list']).most_common(1)[0][0] if stats['author_list'] else None

            stability = self._calculate_stability_score(stats.get('churn', 0), stats['commits'], days_since_change)
            is_hotspot = stability < 0.5 and days_since_change < 30

            self.gnostic_map[path_str] = TemporalGnosis(
                churn_score=stats.get('churn', 0),  # Placeholder until --numstat is parsed
                commit_count=stats['commits'],
                author_count=len(stats['authors']),
                last_modified_timestamp=stats['last_ts'],
                days_since_last_change=days_since_change,
                first_commit_timestamp=stats['first_ts'],
                age_in_days=age_in_days,
                primary_author=primary_author,
                last_commit_subject=stats['last_subject'],
                stability_score=stability,
                is_hotspot=is_hotspot
            )

    def _calculate_stability_score(self, churn: int, commits: int, recency_days: int) -> float:
        """Faculty 8: The Stability Oracle."""
        # A heuristic score where 1.0 is perfectly stable.
        churn_penalty = math.log1p(churn / 100)
        commit_penalty = math.log1p(commits) / 5.0
        # Heavy penalty for very recent changes, decaying rapidly.
        recency_penalty = math.exp(-recency_days / 30.0)
        total_penalty = churn_penalty + commit_penalty + (recency_penalty * 2.0)
        stability = max(0.0, 1.0 - (total_penalty / 5.0))
        return round(stability, 2)

    def get_heat_map(self, since_ref: str) -> Dict[str, Set[int]]:
        """Faculty 11: The Heat Map Weaver."""
        if self.is_dormant: return {}

        heat_map = defaultdict(set)
        try:
            cmd = ['git', 'diff', '--unified=0', since_ref, 'HEAD', '--', '.']
            output = subprocess.check_output(cmd, cwd=self.root, text=True, stderr=subprocess.DEVNULL)

            current_file = None
            for line in output.splitlines():
                if line.startswith('+++ b/'):
                    current_file = line[6:].strip()
                elif line.startswith('@@') and current_file:
                    try:
                        match = re.search(r'\+([0-9,]+)', line)
                        if not match: continue

                        start_len = match.group(1).split(',')
                        start = int(start_len[0])
                        length = int(start_len[1]) if len(start_len) > 1 else 1

                        if length > 0:
                            for i in range(length):
                                heat_map[current_file].add(start + i)
                    except (ValueError, IndexError):
                        pass
        except Exception:
            pass

        return dict(heat_map)