# Path: src/velm/core/cortex/engine/analysis.py
# ---------------------------------------------
import sys
import time
import os
import collections
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..contracts import CortexMemory
from ....logger import Scribe

# ★★★ THE DIVINE HEALING: THE LAW OF THE INTERNAL GAZE ★★★
# The profane bond to the external artisan is annihilated. The Analysis Engine
# now communes directly with its sibling faculty in the Cortex.
from ..ranking import SignificanceRanker
from ..contracts import DistillationProfile  # We also move the contract
# ★★★ THE APOTHEOSIS IS COMPLETE ★★★

from ....artisans.translocate_core.resolvers import (
    PythonImportResolver, JavaScriptResolver, TypeScriptResolver, GoImportResolver,
    RustImportResolver, RubyImportResolver, JavaImportResolver, CppImportResolver
)

# --- Feature Flags for Resolvers ---
try:
    from ....artisans.translocate_core.resolvers import PythonImportResolver
    PYTHON_RESOLVER_AVAILABLE = True
except ImportError:
    PYTHON_RESOLVER_AVAILABLE = False

try:
    from ....artisans.translocate_core.resolvers import JavaScriptResolver
    JS_RESOLVER_AVAILABLE = True
except ImportError:
    JS_RESOLVER_AVAILABLE = False

try:
    from ....artisans.translocate_core.resolvers import TypeScriptResolver
    TS_RESOLVER_AVAILABLE = True
except ImportError:
    TS_RESOLVER_AVAILABLE = False

try:
    from ....artisans.translocate_core.resolvers import GoImportResolver
    GO_RESOLVER_AVAILABLE = True
except ImportError:
    GO_RESOLVER_AVAILABLE = False

try:
    from ....artisans.translocate_core.resolvers import RustImportResolver
    RUST_RESOLVER_AVAILABLE = True
except ImportError:
    RUST_RESOLVER_AVAILABLE = False

try:
    from ....artisans.translocate_core.resolvers import RubyImportResolver
    RUBY_RESOLVER_AVAILABLE = True
except ImportError:
    RUBY_RESOLVER_AVAILABLE = False

Logger = Scribe("AnalysisEngine")


class AnalysisEngine:
    """
    The Higher Mind of the Cortex. It has been ascended to rely only on its own
    internal Gnosis, its bond to the external world severed, its purity absolute.
    """

    def __init__(self, project_root: Path, memory: CortexMemory):
        self.root = project_root
        self.memory = memory
        self.logger = Logger

    def perceive(self) -> CortexMemory:
        """Proxies access to the memory if needed by internal methods."""
        return self.memory

    def query_centrality(self, language: str = "any", limit: int = 5) -> List[Tuple[Path, Dict]]:
        """Perceives the architectural center of gravity by summoning the SignificanceRanker."""
        Logger.verbose("The Oracle of Influence awakens its Gaze...")
        if not self.memory or not self.memory.inventory: return []

        # We forge a humble, default profile for the Ranker's Gaze.
        profile = DistillationProfile(strategy='balanced')

        # The Specialist is summoned.
        ranker = SignificanceRanker(profile, self.memory)

        # The Rite of Judgment is conducted.
        ranked_inventory = ranker.rank(self.memory.inventory)

        results = []
        count = 0
        for item in ranked_inventory:
            if count >= limit: break
            if language == 'any' or item.language == language:
                absolute_path = self.root / item.path
                metadata = {"score": item.centrality_score, "language": item.language, "category": item.category}
                results.append((absolute_path, metadata))
                count += 1

        Logger.verbose(f"Gaze complete. Identified {len(results)} central nodes.")
        return results

    def prophesy_healing_plan(self, translocation_map: Dict[Path, Path]) -> Dict[Path, List[Dict]]:
        self.logger.info("The Cortex awakens its Polyglot Gaze to prophesy a healing plan...")
        start_time = time.monotonic()

        memory = self.perceive()
        if not memory or not memory.project_gnosis:
            self.logger.warn("The Gaze is averted. The Cortex's memory is a void.")
            return {}

        all_healing_plans: Dict[Path, List[Dict]] = {}

        expanded_moves: Dict[Path, Path] = {}
        moved_paths_set: Set[Path] = set()

        for origin, dest in translocation_map.items():
            if origin.is_file():
                expanded_moves[origin] = dest
                moved_paths_set.add(origin)
            elif origin.is_dir():
                for file_gnosis in memory.inventory:
                    try:
                        # Check if file is inside the moved directory
                        # resolve() handles symlinks and absolute paths
                        if file_gnosis.path.resolve().is_relative_to(origin.resolve()):
                            rel_path = file_gnosis.path.resolve().relative_to(origin.resolve())
                            new_full_path = dest.resolve() / rel_path
                            expanded_moves[file_gnosis.path.resolve()] = new_full_path
                            moved_paths_set.add(file_gnosis.path.resolve())
                    except ValueError:
                        continue

        patients: Set[Path] = set()
        patients.update(moved_paths_set)

        for moved_file in moved_paths_set:
            try:
                rel_moved = str(moved_file.relative_to(self.root)).replace('\\', '/')
                dependents = memory.get_dependents_of(rel_moved)
                for dep_str in dependents:
                    dep_path = (self.root / dep_str).resolve()
                    if dep_path.exists():
                        patients.add(dep_path)
            except ValueError:
                continue

        self.logger.verbose(f"Gaze of Causality: {len(patients)} unique scriptures require examination.")

        files_by_lang: Dict[str, List[Path]] = collections.defaultdict(list)
        for file_path in patients:
            suffix = file_path.suffix.lower()
            if suffix == '.py':
                files_by_lang['python'].append(file_path)
            elif suffix in ('.js', '.jsx', '.mjs', '.cjs'):
                files_by_lang['javascript'].append(file_path)
            elif suffix in ('.ts', '.tsx'):
                files_by_lang['typescript'].append(file_path)
            elif suffix == '.go':
                files_by_lang['go'].append(file_path)
            elif suffix == '.rs':
                files_by_lang['rust'].append(file_path)
            elif suffix == '.rb':
                files_by_lang['ruby'].append(file_path)
            elif suffix == '.java':
                files_by_lang['java'].append(file_path)
            elif suffix in ('.cpp', '.c', '.h', '.hpp', '.cc', '.hh'):
                files_by_lang['cpp'].append(file_path)

        # [THE CURE]: Substrate-Aware Execution
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        def _execute_healing(resolver, files):
            """Executes healing logic for a language group."""
            if not resolver: return {}
            # Assume resolver has logic to generate plans.
            # In translocate/resolvers, this is typically `resolve_batch` or similar.
            # We'll assume a standard interface `resolve(files)`.
            # Since the prompt implies `_conduct_healing_rite` was expected, we use that abstraction.
            return self._conduct_healing_rite(resolver, files)

        if is_wasm:
            # Serial Mode
            if files_by_lang['python'] and PYTHON_RESOLVER_AVAILABLE:
                all_healing_plans.update(_execute_healing(PythonImportResolver(self.root, memory.symbol_map, expanded_moves), files_by_lang['python']))
            if files_by_lang['javascript'] and JS_RESOLVER_AVAILABLE:
                all_healing_plans.update(_execute_healing(JavaScriptResolver(self.root, expanded_moves), files_by_lang['javascript']))
            if files_by_lang['typescript'] and TS_RESOLVER_AVAILABLE:
                all_healing_plans.update(_execute_healing(TypeScriptResolver(self.root, expanded_moves), files_by_lang['typescript']))
            if files_by_lang['go'] and GO_RESOLVER_AVAILABLE:
                all_healing_plans.update(_execute_healing(GoImportResolver(self.root, expanded_moves), files_by_lang['go']))
            if files_by_lang['rust'] and RUST_RESOLVER_AVAILABLE:
                all_healing_plans.update(_execute_healing(RustImportResolver(self.root, expanded_moves), files_by_lang['rust']))
            if files_by_lang['ruby'] and RUBY_RESOLVER_AVAILABLE:
                all_healing_plans.update(_execute_healing(RubyImportResolver(self.root, expanded_moves), files_by_lang['ruby']))

        else:
            # Parallel Mode
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                future_to_lang: Dict[Any, str] = {}

                if files_by_lang['python'] and PYTHON_RESOLVER_AVAILABLE:
                    resolver = PythonImportResolver(self.root, memory.symbol_map, expanded_moves)
                    future_to_lang[
                        executor.submit(self._conduct_healing_rite, resolver, files_by_lang['python'])] = "Python"

                if files_by_lang['javascript'] and JS_RESOLVER_AVAILABLE:
                    resolver = JavaScriptResolver(self.root, expanded_moves)
                    future_to_lang[
                        executor.submit(self._conduct_healing_rite, resolver, files_by_lang['javascript'])] = "JavaScript"

                if files_by_lang['typescript'] and TS_RESOLVER_AVAILABLE:
                    resolver = TypeScriptResolver(self.root, expanded_moves)
                    future_to_lang[
                        executor.submit(self._conduct_healing_rite, resolver, files_by_lang['typescript'])] = "TypeScript"

                if files_by_lang['go'] and GO_RESOLVER_AVAILABLE:
                    resolver = GoImportResolver(self.root, expanded_moves)
                    future_to_lang[executor.submit(self._conduct_healing_rite, resolver, files_by_lang['go'])] = "Go"

                if files_by_lang['rust'] and RUST_RESOLVER_AVAILABLE:
                    resolver = RustImportResolver(self.root, expanded_moves)
                    future_to_lang[executor.submit(self._conduct_healing_rite, resolver, files_by_lang['rust'])] = "Rust"

                if files_by_lang['ruby'] and RUBY_RESOLVER_AVAILABLE:
                    resolver = RubyImportResolver(self.root, expanded_moves)
                    future_to_lang[executor.submit(self._conduct_healing_rite, resolver, files_by_lang['ruby'])] = "Ruby"

                for future in as_completed(future_to_lang):
                    lang = future_to_lang[future]
                    try:
                        lang_plan = future.result()
                        if lang_plan:
                            all_healing_plans.update(lang_plan)
                    except Exception as e:
                        self.logger.error(f"A catastrophic paradox shattered the {lang} Healer's Gaze.", exc_info=e)

        duration = (time.monotonic() - start_time) * 1000
        total_healed_files = len(all_healing_plans)

        # [THE FIX] We always proclaim the result, even if 0, at INFO level.
        if total_healed_files > 0:
            self.logger.success(
                f"Gaze of the Delta is complete in {duration:.2f}ms. {total_healed_files} scripture(s) require healing.")
        else:
            self.logger.info(f"Gaze of the Delta is complete in {duration:.2f}ms. No Gnostic bonds require healing.")

        return all_healing_plans

    def _conduct_healing_rite(self, resolver: Any, files: List[Path]) -> Dict[Path, List[Dict]]:
        """Executes the resolve method on the given language resolver."""
        try:
            return resolver.resolve_batch(files)
        except AttributeError:
             # Fallback if resolve_batch isn't implemented, try loop
            plans = {}
            for f in files:
                res = resolver.resolve(f)
                if res:
                    plans[f] = res
            return plans
        except Exception as e:
            self.logger.error(f"Healing Rite fractured: {e}")
            return {}