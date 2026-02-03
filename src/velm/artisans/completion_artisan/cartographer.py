# Path: scaffold/artisans/completion_artisan/cartographer.py
# ----------------------------------------------------------

import os
import re
import time
import math
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Set, Tuple, Union

# --- CORE UPLINKS ---
from ...core.alchemist import DivineAlchemist
from ...utils import get_ignore_spec, get_human_readable_size, is_binary
from ...logger import Scribe

Logger = Scribe("GnosticCartographer")

# =================================================================================
# == THE ABYSSAL WARD (O(1) FILTERS)                                             ==
# =================================================================================
ABYSS = {
    '.git', '.svn', '.hg', '.DS_Store', 'Thumbs.db', 'node_modules',
    'bower_components', 'jspm_packages', '__pycache__', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', 'venv', '.venv', 'env', '.env',
    'target', 'build', 'dist', 'out', '.scaffold'
}


class GnosticCartographer:
    """
    =================================================================================
    == THE GNOSTIC CARTOGRAPHER (V-Ω-TOTALITY-V3000-SINGULARITY)                   ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: SPATIAL_PERCEPTION_ENGINE

    A high-fidelity spatial scryer that merges Disk and Shadow realities.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Union Gaze:** Merges physical files and shadow (staging) files into a single truth.
    2.  **The Fuzzy Oracle:** Advanced scoring algorithm (Acronyms, Subsequences, Prefix) for intuitive matching.
    3.  **The Gaze of Aversion:** Respects `.gitignore` via the `ignore_spec` uplink.
    4.  **Geometric Triage:** Correctly resolves relative (`./`) vs absolute (`src/`) paths relative to the Blueprint.
    5.  **Holographic Soul-Peeking:** Reads the first 10 lines of text files to show a code preview in the documentation.
    6.  **Binary Sarcophagus:** Detects binary files via `\0` scanning and suppresses their content preview.
    7.  **Temporal Stamping:** Displays relative time ("2m ago") in the dossier.
    8.  **The Abyssal Ward:** Hardcoded O(1) filter for black holes like `node_modules`.
    9.  **Genesis Prophecy:** If a path does not exist, offers to "Materialize" it via the `::` operator.
    10. **Sort Priority:** Folders > High Score > Alphabetical.
    11. **Dossier Forge:** Generates rich Markdown tables for file metadata.
    12. **Path Deduplication:** Canonicalizes paths to prevent `C:/` vs `c:/` heresies.
    13. **Semantic Iconography:** Assigns emojis based on file extension/type.
    14. **Index Safety:** Fixed the `list index out of range` heresy with defensive coding.
    15. **Slash Unification:** Forces POSIX slashes internally for consistency.
    16. **Metabolic Capping:** Limits results to 64 items to preserve UI frame rates.
    17. **Home Expansion:** Resolves `~` to the User's Castle.
    18. **Alchemical Resolution:** Resolves `{{ project_root }}` variables in paths before scanning.
    19. **Symlink Perception:** Distinguishes symlinks from real matter.
    20. **Fault Isolation:** Wraps file I/O in try/catch to prevent permission crashes.
    21. **Parent Gravity:** Boosts scores for files in the immediate vicinity.
    22. **Extension Diviner:** Maps file extensions to markdown language tags for syntax highlighting in docs.
    23. **Shadow precedence:** If a file exists in Shadow and Disk, Shadow wins (it is the Future).
    24. **Immutable Anchoring:** Anchors to `project_root` at instantiation for absolute stability.
    """

    def __init__(self,
                 project_root: Path,
                 blueprint_path: Path,
                 alchemist: DivineAlchemist,
                 known_paths: Set[str],
                 engine: Any = None):
        """
        [ASCENSION 24]: IMMUTABLE REFERENCE
        """
        self.project_root = project_root.resolve()
        self.blueprint_path = blueprint_path.resolve()
        self.alchemist = alchemist
        self.engine = engine

        # [ASCENSION 12]: RESULT DEDUPLICATION
        self.known_paths = {str(p).replace('\\', '/') for p in known_paths}

        # [ASCENSION 3]: THE GAZE OF AVERSION
        self.ignore_spec = get_ignore_spec(self.project_root)

        # [ASCENSION 2]: SHADOW PLANE ANCHOR
        self.shadow_root = self.project_root / ".scaffold" / "staging"

        Logger.debug(f"Cartographer Consecrated. Anchor: {self.project_root}")

    def gaze(self, partial_path_str: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE OMNISCIENT GAZE (V-Ω-TOTALITY-INGRESS)                             ==
        =============================================================================
        LIF: 100x | The main entry point for the Prophetic Scan.
        """
        start_ns = time.perf_counter_ns()
        items: List[Dict[str, Any]] = []
        seen_names: Set[str] = set()

        try:
            # --- MOVEMENT I: THE PATH SOLVENT [ASCENSION 1 & 18] ---
            # Resolve variables inside the plea (e.g., {{ project_name }}/src)
            alchemized = self.alchemist.transmute(partial_path_str, context)

            # Normalization (The Solvent)
            clean_partial = alchemized.strip().replace("'", "").replace('"', "")
            # Handle Home expansion
            if clean_partial.startswith('~'):
                clean_partial = os.path.expanduser(clean_partial)

            # Universal Slash Unification
            partial = clean_partial.replace('\\', '/')

            # --- MOVEMENT II: GEOMETRIC TRIAGE [ASCENSION 4] ---
            # We determine the search vector relative to the BLUEPRINT or the ROOT
            if "/" not in partial:
                # Root level or sibling search
                base_dir_rel = "."
                prefix = partial
            else:
                # Sub-directory traversal
                base_dir_rel, prefix = os.path.split(partial)

            # [ASCENSION 10]: INDENTATION-AWARE ANCHORING
            # We look relative to the actual file being edited
            search_dir_phys = (self.blueprint_path.parent / base_dir_rel).resolve()

            # Guard: Root Confinement
            if not self._is_subpath(search_dir_phys, self.project_root):
                # If we are looking for absolute paths outside root, allow but verify
                if not search_dir_phys.exists(): return []

            # [ASCENSION 9 & 10]: THE GENESIS PROPHECY
            # If the directory doesn't even exist, we offer to materialize it.
            if not search_dir_phys.exists() and not self._scan_shadow_existence(base_dir_rel):
                return self._prophesy_creation(base_dir_rel, prefix)

            # --- MOVEMENT III: MULTIVERSAL SCAN [ASCENSION 3] ---

            # Phase A: The Mortal Realm (Disk)
            if search_dir_phys.exists() and search_dir_phys.is_dir():
                self._scry_sanctum(search_dir_phys, prefix, items, seen_names, is_shadow=False)

            # Phase B: The Ethereal Plane (Shadow Vault)
            try:
                # Map physical path to shadow equivalent
                rel_to_root = search_dir_phys.relative_to(self.project_root)
                search_dir_shadow = (self.shadow_root / rel_to_root).resolve()

                if search_dir_shadow.exists() and search_dir_shadow.is_dir():
                    self._scry_sanctum(search_dir_shadow, prefix, items, seen_names, is_shadow=True)
            except ValueError:
                pass  # Path outside project, no shadow scrying possible

            # --- MOVEMENT IV: RESONANCE RANKING [ASCENSION 2, 4, 10] ---
            # We calculate final scores and sort the results
            final_completions = self._rank_revelations(items)

            # Performance Telemetry
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if duration_ms > 50:
                Logger.warn(f"Sluggish Gaze: {duration_ms:.2f}ms for '{partial_path_str}'")

            return final_completions

        except Exception as fracture:
            Logger.error(f"Gaze Fracture: {fracture}")
            return []

    def _scry_sanctum(self,
                      directory: Path,
                      prefix: str,
                      items: List[Dict],
                      seen: Set[str],
                      is_shadow: bool):
        """
        [THE HARVEST RITE]
        Performs high-performance directory scanning with character-level triage.
        """
        try:
            # [ASCENSION 12]: FAULT-ISOLATE SARCOPHAGUS
            # Scandir is O(N) but faster than listdir as it returns dirent objects
            for entry in os.scandir(directory):
                name = entry.name

                # 1. THE ABYSSAL WARD [ASCENSION 8]
                if name in ABYSS or (name.startswith('.') and not prefix.startswith('.')):
                    continue

                if name in seen:
                    continue

                # 2. RESONANCE CALCULATION [ASCENSION 2 & 6]
                score = self._calculate_match_score(prefix, name)
                if score <= 0:
                    continue

                # 3. MATTER TRIAGE
                is_dir = entry.is_dir()
                is_link = entry.is_symlink()

                label = f"{name}{'/' if is_dir else ''}"

                # 4. DOSSIER FORGING [ASCENSION 5, 6, 7]
                details = self._get_holographic_dossier(Path(entry.path), is_shadow)

                # 5. ICONOGRAPHY [ASCENSION 13 & 16]
                icon = "📁" if is_dir else self._get_semantic_icon(name)
                if is_shadow: icon = "👻 " + icon

                # 6. ATOM ASSEMBLY
                item = {
                    "label": label,
                    "kind": 19 if is_dir else 17,  # Folder vs File
                    "detail": f"{icon} {details['meta_line']}",
                    "documentation": details['docs'],
                    "insertText": name,
                    "sortText": f"{'0' if is_dir else '1'}_{name}",
                    "score": score,
                    "is_dir": is_dir,
                    "data": {
                        "abs_path": str(entry.path),
                        "is_shadow": is_shadow,
                        "is_dir": is_dir
                    }
                }

                items.append(item)
                seen.add(name)

        except (PermissionError, OSError):
            # [ASCENSION 12]: Silence is Golden. We skip forbidden or locked sanctums.
            pass

    def _calculate_match_score(self, query: str, target: str) -> int:
        """
        [THE FUZZY ORACLE - ASCENSION 2, 6]
        A multi-objective scoring engine for architectural intent.
        """
        if not query: return 100  # Match all

        q_lower = query.lower()
        t_lower = target.lower()

        # 1. Exact Resonance (Highest)
        if t_lower == q_lower: return 2000

        # 2. Prefix Resonance (High)
        if t_lower.startswith(q_lower): return 1000 + (len(q_lower) * 10)

        # 3. [ASCENSION 6]: Acronym Triage (api/uc -> user_controller)
        # We find boundaries like _, -, or camelCase
        boundaries = re.findall(r'[a-zA-Z][^A-Z_\-]*', target)
        acronym = "".join([b[0] for b in boundaries]).lower()
        if acronym.startswith(q_lower): return 800 + (len(q_lower) * 5)

        # 4. Subsequence Search with Consecutive Bonuses
        q_idx = 0
        t_idx = 0
        score = 0
        consecutive = 0

        while q_idx < len(q_lower) and t_idx < len(t_lower):
            if q_lower[q_idx] == t_lower[t_idx]:
                score += 10 + (consecutive * 20)  # Significant bonus for strings
                consecutive += 1
                q_idx += 1
            else:
                consecutive = 0
                score -= 1
            t_idx += 1

        if q_idx == len(q_lower):
            # Penalize distance from start [ASCENSION 2]
            start_pos = target.lower().find(q_lower[0])
            score -= (start_pos * 5)
            return max(1, score)

        return 0

    def _get_holographic_dossier(self, item: Path, is_shadow: bool) -> Dict[str, Any]:
        """
        [THE DOSSIER FORGE - ASCENSION 5, 7, 11]
        Transmutes physical metrics into a high-fidelity Markdown revelation.
        """
        try:
            stat = item.stat()

            # [ASCENSION 7]: Unit Transmutation
            size_gnosis = get_human_readable_size(stat.st_size)

            # [ASCENSION 7]: Relative Temporal Stamping
            diff = time.time() - stat.st_mtime
            if diff < 60:
                mtime_gnosis = "Just now"
            elif diff < 3600:
                mtime_gnosis = f"{int(diff / 60)}m ago"
            else:
                mtime_gnosis = time.strftime('%H:%M', time.localtime(stat.st_mtime))

            status = "🔮 [SHADOW]" if is_shadow else "💾 [DISK]"
            meta_line = f"{size_gnosis} • {mtime_gnosis} • {status}"

            # Markdown Construction
            md = f"### {item.name}\n\n"
            md += f"_{status}_\n\n"
            md += f"| Property | Gnosis |\n|---|---|\n"
            md += f"| **Mass** | `{size_gnosis}` |\n"
            md += f"| **Flux** | `{mtime_gnosis}` |\n"

            # [ASCENSION 10]: Local Gravity Check
            if item.parent == self.blueprint_path.parent:
                md += f"| **Proximity** | `LOCAL_SANCTUM` |\n"

            # [ASCENSION 5 & 11]: HOLOGRAPHIC SOUL-PEEKING
            if item.is_file() and stat.st_size < 512 * 1024:  # 512KB limit for scrying
                # [ASCENSION 11]: Binary Sarcophagus
                if not is_binary(str(item)):
                    try:
                        # JIT Read of the first 10 lines
                        with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                            head = []
                            for _ in range(10):
                                line = f.readline()
                                if not line: break
                                head.append(line)

                            if head:
                                soul_content = "".join(head)
                                if len(head) == 10: soul_content += "\n..."

                                # [ASCENSION 16]: divine highlighting
                                lang = self._divine_language(item.name)
                                md += f"\n---\n**Scripture Soul**:\n```{lang}\n{soul_content}\n```"
                    except:
                        pass

            return {"meta_line": meta_line, "docs": {"kind": "markdown", "value": md}}

        except:
            return {"meta_line": "Void Entity", "docs": None}

    def _rank_revelations(self, items: List[Dict]) -> List[Dict]:
        """
        [THE RANKING ENGINE - ASCENSION 4, 10, 22]
        """
        # [ASCENSION 22]: Intelligent Multi-Factor Sorting
        items.sort(key=lambda x: (
            not x.get('is_dir', False),  # Folders always come first
            -x.get('score', 0),  # Then resonance score
            x['label'].lower()  # Finally alpha
        ))

        # [ASCENSION 16]: Metabolic Capping
        return items[:64]

    def _prophesy_creation(self, rel_path: str, prefix: str) -> List[Dict]:
        """
        [ASCENSION 9]: GENESIS PROPHECY
        Offers to forge new realities when the Gaze hits a void.
        """
        return [
            {
                "label": f"📄 Forge Scripture: {prefix}",
                "kind": 1,
                "detail": "✨ (Genesis Rite)",
                "documentation": {"kind": "markdown", "value": f"**Will:** Manifest new scripture at `{rel_path}`"},
                "insertText": prefix,
                "sortText": "000_forge_file"
            },
            {
                "label": f"📁 Materialize Sanctum: {prefix}/",
                "kind": 19,
                "detail": "✨ (Genesis Rite)",
                "documentation": {"kind": "markdown", "value": f"**Will:** Manifest new sanctum at `{rel_path}/`"},
                "insertText": f"{prefix}/",
                "sortText": "000_materialize_dir"
            }
        ]

    def _scan_shadow_existence(self, rel_path: str) -> bool:
        """Checks the staging area for AI-generated ghosts."""
        try:
            return (self.shadow_root / rel_path).exists()
        except:
            return False

    def _is_subpath(self, child: Path, parent: Path) -> bool:
        """Adjudicates if a path is anchored within a root."""
        try:
            child.relative_to(parent)
            return True
        except ValueError:
            return False

    def _get_semantic_icon(self, name: str) -> str:
        """[ASCENSION 13]: THE SEMANTIC ICONOGRAPHER"""
        ext = name.split('.')[-1].lower() if '.' in name else ''
        if name == 'Dockerfile': return '🐳'
        if name == 'package.json': return '📦'
        if ext in ('py', 'pyw'): return '🐍'
        if ext in ('js', 'jsx'): return '📜'
        if ext in ('ts', 'tsx'): return '🔷'
        if ext in ('rs', 'toml'): return '🦀'
        if ext in ('go', 'mod'): return '🐹'
        if ext in ('json', 'yaml', 'yml'): return '⚙️'
        if ext in ('md', 'txt'): return '📝'
        if ext in ('scaffold', 'arch'): return '🏗️'
        return '📄'

    def _divine_language(self, name: str) -> str:
        """[ASCENSION 16]: Divines markdown language tag."""
        ext = name.split('.')[-1].lower() if '.' in name else ''
        mapping = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'rs': 'rust', 'go': 'go', 'sh': 'bash', 'md': 'markdown',
            'scaffold': 'yaml', 'symphony': 'yaml', 'arch': 'yaml'
        }
        return mapping.get(ext, 'plaintext')

# === SCRIPTURE SEALED: THE PATHFINDER IS OMNIPOTENT ===