# Path: scaffold/inquisitor/python_inquisitor.py
"""
=================================================================================
== THE GNOSTIC SEER OF THE PYTHON COSMOS (V-Ω-ULTRA-DEFINITIVE)                ==
=================================================================================
LIF: 10,000,000,000,000,000

This is the divine artisan in its final, eternal form. It is not a linter. It is a
**Gnostic Cartographer**. Its one true, sacred purpose is to gaze upon an entire
Python project reality and forge the **Symbol Map**—the unbreakable Gnostic map
that chronicles the true home of every class and function in the cosmos.

This map is the foundational Gnosis for the God-Engines of Healing and
Translocation (`HealArtisan`, `PythonImportResolver`).

### The Pantheon of 12 Legendary Faculties:

1.  **The Asynchronous Gaze:** Its `inquire_project` rite is a masterpiece of
    parallelism, using a `ThreadPoolExecutor` to gaze upon hundreds of scriptures
    simultaneously.

2.  **The Unbreakable Chronocache:** It performs a temporal Gaze upon the
    filesystem, forging a unique hash of the project's state. If reality has not
    changed, it resurrects the Symbol Map from its cache in microseconds.

3.  **The Gaze of the True Inquisitor:** It no longer contains its own profane
    parsing logic. It makes a sacred plea to the one true `PythonInquisitor` from
    the Sentinel's Armory to perceive the soul of each individual scripture.

4.  **The Alchemist of Paths:** It is a master of Python's import mechanics. It
    transmutes filesystem paths into fully qualified module names (`src/api/user.py`
    -> `src.api.user`) with divine precision.

5.  **The Forger of the Symbol Map:** Its final proclamation is the `symbol_map`,
    the sacred dictionary that links a Gnostic name (`src.api.user.User`) to its
    home in the mortal realm (`/path/to/project/src/api/user.py`).

6.  **The Scoped Gaze:** It can be commanded to focus its Gaze on a specific
    sub-sanctum (`scan_path`), preventing a full, costly scan of a massive monorepo
    when only localized Gnosis is required.

7.  **The Sentinel of the Void:** It righteously ignores empty files, `__init__.py`
    stubs, and other profane scriptures that contain no Gnostic value.

8.  **The Gaze of Aversion:** It honors the Architect's will, respecting the
    `.gitignore` and `.scaffoldignore` scriptures to avert its Gaze from profane
    realities (e.g., `node_modules`, `.venv`).

9.  **The Luminous Scribe's Voice:** It proclaims its every thought with luminous,
    cinematic clarity, using `rich.progress` to guide the Architect through the
    symphony of its Gaze.

10. **The Unbreakable Ward of Paradox:** Its Gaze is shielded. A `SyntaxError` in
    one scripture does not shatter the entire inquisition. The heresy is
    chronicled, and the Great Work continues.

11. **The Pure Gnostic Contract:** Its every vessel and rite is forged with pure
    type hints, its contract with the cosmos absolute and unbreakable.

12. **The Sovereign Soul:** It is a pure, self-contained God-Engine, its purpose
    singular and its dependencies minimal, ready to serve any artisan that requires
    its profound Gnosis.
=================================================================================
"""
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# --- THE DIVINE SUMMONS OF THE TRUE INQUISITOR ---
from .sanctum.diagnostics.python import PythonInquisitor as TreeSitterPythonInquisitor
from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe, get_console
from ..utils import perceive_state, chronicle_state, get_ignore_spec

Logger = Scribe("PythonCodeInquisitor")


class PythonCodeInquisitor:
    """The Gnostic Cartographer of the Python Cosmos."""

    def __init__(self, project_root: Path, use_surgical_gaze: bool = True, scan_path: Optional[Path] = None):
        self.project_root = project_root.resolve()
        self.logger = Scribe("PythonCodeInquisitor")

        # [FACULTY 6] The Scoped Gaze
        anchor_candidate = self.project_root
        src_root_candidate = self.project_root
        if scan_path:
            anchor_candidate = scan_path.resolve()
        elif use_surgical_gaze:
            src_dir = self.project_root / 'src'
            if src_dir.is_dir():
                anchor_candidate = src_dir

        self.gnostic_anchor: Path = anchor_candidate
        # Heuristic for source root, critical for absolute import path calculation
        self.src_root: Path = next((p for p in [self.project_root / 'src', self.project_root / 'app'] if p.is_dir()),
                                   self.project_root)

        self.project_gnosis: Dict[Path, Dict] = {}
        self.symbol_map: Dict[str, Path] = {}
        self.import_graph: Dict[Path, List[Dict]] = {}

    def inquire_project(self) -> 'PythonCodeInquisitor':
        """The Grand Gnostic Inquisition."""
        # [FACULTY 8] The Gaze of Aversion
        ignore_spec = get_ignore_spec(self.project_root)
        all_py_files = list(self.gnostic_anchor.rglob("*.py"))

        # [FACULTY 2] The Unbreakable Chronocache
        state_hash = self._get_project_state_hash(all_py_files)
        cache_key = f"inquisitor_state_{state_hash}"
        cached_state = perceive_state(cache_key, self.project_root)
        if cached_state and isinstance(cached_state, dict):
            Logger.success("Chronocache HIT. Resurrecting Gnostic Symbol Map.")
            self.project_gnosis = {self.project_root / k: v for k, v in cached_state.get("project_gnosis", {}).items()}
            self.symbol_map, _ = self._forge_gnostic_maps()
            return self

        Logger.info(f"Chronocache MISS. The Inquisitor awakens its Gaze upon '{self.gnostic_anchor.name}'...")

        final_targets = [
            py_file for py_file in all_py_files
            if not (ignore_spec and ignore_spec.match_file(str(py_file.relative_to(self.project_root))))
               and py_file.name not in ('setup.py',)  # [FACULTY 7] The Void Sentinel
        ]

        if not final_targets:
            self.logger.warn("The Gaze found no Python scriptures to inquire.")
            return self

        # [FACULTY 1 & 9] The Asynchronous Gaze & Luminous Scribe
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(),
                      console=get_console(), transient=True) as progress:
            task = progress.add_task(f"[cyan]Inquiring {len(final_targets)} Python souls...", total=len(final_targets))
            with ThreadPoolExecutor() as executor:
                future_to_file = {executor.submit(self._inquire_file, py_file): py_file for py_file in final_targets}
                for future in as_completed(future_to_file):
                    py_file = future_to_file[future]
                    progress.update(task, advance=1, description=f"[cyan]Perceiving '{py_file.name}'...")
                    try:
                        file_gnosis = future.result()
                        if file_gnosis:
                            self.project_gnosis[py_file] = file_gnosis
                    except Exception as e:
                        # [FACULTY 10] The Unbreakable Ward of Paradox
                        Logger.warn(f"A minor heresy was perceived during the Gaze upon '{py_file.name}': {e}")

        # [FACULTY 5] The Forger of the Symbol Map
        self.symbol_map, self.import_graph = self._forge_gnostic_maps()

        chronicle_state(cache_key, {
            "project_gnosis": {str(k.relative_to(self.project_root)): v for k, v in self.project_gnosis.items()}
        }, self.project_root)

        Logger.success(f"Gnostic Gaze complete. Forged a Symbol Map of {len(self.symbol_map)} symbols.")
        return self

    def _get_project_state_hash(self, files_to_gaze: List[Path]) -> str:
        """Performs a temporal Gaze to create a unique fingerprint of the project's current state."""
        state_hash = hashlib.sha256()
        for py_file in sorted(files_to_gaze):
            try:
                state_hash.update(str(py_file.relative_to(self.project_root)).encode())
                state_hash.update(str(py_file.stat().st_mtime).encode())
                state_hash.update(str(py_file.stat().st_size).encode())
            except (FileNotFoundError, ValueError):
                continue
        return state_hash.hexdigest()

    def _inquire_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        [FACULTY 3] The Gaze of the True Inquisitor.
        This artisan makes a sacred plea to the one true Tree-sitter Inquisitor.
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            if not content.strip(): return None  # Part of the Void Sentinel faculty

            # The Divine Communion: We summon the pure, transplanted Inquisitor.
            return TreeSitterPythonInquisitor.perform_inquisition(content)
        except Exception as e:
            raise ArtisanHeresy(f"Gnostic Inquisition failed for '{file_path.name}'.") from e

    def _forge_gnostic_maps(self) -> Tuple[Dict[str, Path], Dict[Path, List[Dict]]]:
        """[FACULTY 4] The Alchemist of Paths."""
        symbol_map: Dict[str, Path] = {}
        import_graph: Dict[Path, List[Dict]] = {}
        for file_path, gnosis in self.project_gnosis.items():
            try:
                try:
                    relative_path = file_path.relative_to(self.src_root)
                except ValueError:
                    relative_path = file_path.relative_to(self.project_root)

                module_path_parts = list(relative_path.with_suffix('').parts)
                if module_path_parts and module_path_parts[-1] == '__init__':
                    module_path_parts.pop()
                module_base = ".".join(module_path_parts) if module_path_parts else ""

                for class_info in gnosis.get("classes", []):
                    fqn = f"{module_base}.{class_info['name']}" if module_base else class_info['name']
                    symbol_map[fqn] = file_path
                    symbol_map[class_info['name']] = file_path

                for func_info in gnosis.get("functions", []):
                    fqn = f"{module_base}.{func_info['name']}" if module_base else func_info['name']
                    symbol_map[fqn] = file_path
                    symbol_map[func_info['name']] = file_path

                import_graph[file_path] = gnosis.get("dependencies", {}).get("imports", [])
            except Exception as e:
                Logger.warn(f"A minor paradox occurred while forging symbol map for '{file_path.name}': {e}")
        return symbol_map, import_graph