# Path: scaffold/prophecy/oracle.py
# =========================================================================================
# == THE ORACLE OF THE LIVING SOUL: OMEGA POINT (V-Ω-TOTALITY-V500.12-ISOMORPHIC)        ==
# =========================================================================================
# LIF: ∞ | ROLE: PROPHETIC_LOGIC_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ORACLE_V500_WASM_SUTURE_2026_FINALIS
# =========================================================================================

import getpass
import re
import os
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set

# --- THE DIVINE UPLINKS ---
from .grimoires import SOUL_CODEX
from ..gnosis.canon import ARCHITECTURAL_CANON
from ..logger import Scribe

Logger = Scribe("OracleOfTheLivingSoul")


class OracleOfTheLivingSoul:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC PROPHECY (V-Ω-TOTALITY-V500-FINALIS)              ==
    =================================================================================
    LIF: ∞ | ROLE: INTROSPECTIVE_AI

    The divine, sentient God-Engine of Gnostic Perception. It performs a multi-stage,
    substrate-aware Gaze upon any project reality to prophesy its one true soul.
    =================================================================================
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.dossier: Dict[str, Any] = {}
        self.perceived_souls: Set[str] = set()

        # [THE CURE]: SUBSTRATE DETECTION
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Timing metrics for Metabolic Tomography
        self._metrics: Dict[str, float] = {}

    def conduct_inquest(self) -> Dict[str, Any]:
        """
        The Master Symphony of Perception.
        [THE FIX]: Now substrate-aware to prevent Threading Paradoxes in WASM.
        """
        start_ns = time.perf_counter_ns()
        Logger.verbose(f"The Introspective AI awakening on substrate: [{'ETHER' if self._is_wasm else 'IRON'}]")

        # --- MOVEMENT I: THE KINETIC GAZE (I/O RITES) ---
        # [ASCENSION 1 & 2]: We adjudicate based on the Ethereal Plane's laws.
        if self._is_wasm:
            # PATH A: ETHER PLANE (SEQUENTIAL)
            # In WASM, we must conduct our scrying in a single, unified timeline.
            self._conduct_sequential_scry()
        else:
            # PATH B: IRON CORE (PARALLEL)
            # On native iron, we unleash a swarm of scriers to maximize velocity.
            self._conduct_parallel_scry()

        # --- MOVEMENT II: THE SYMPHONY OF THE CANON ---
        # The Mind walks the Declarative Grimoire to resolve secondary Gnosis.
        self._adjudicate_architectural_canon()

        # --- MOVEMENT III: THE GAZE OF GNOSTIC SYNTHESIS ---
        # The AI's final word: Harmonizing the perceived matter into a coherent identity.
        self._synthesize_final_gnosis()

        # Final Telemetry Pulse
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.dossier['_ai_telemetry'] = {
            "prophecy_latency_ms": round(duration_ms, 2),
            "substrate": "WASM" if self._is_wasm else "NATIVE",
            "truth_count": len(self.dossier)
        }

        Logger.success(f"Prophecy Complete. {len(self.dossier)} Gnostic truths manifest in {duration_ms:.2f}ms.")
        return self.dossier

    # =========================================================================
    # == SECTION I: KINETIC SCRYING MOVEMENTS                                ==
    # =========================================================================

    def _conduct_parallel_scry(self):
        """Swarm-based scrying for high-performance native environments."""
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_map = {
                executor.submit(self._gaze_upon_living_souls): "living_souls",
                executor.submit(self._gaze_upon_vcs_soul): "vcs_soul",
                executor.submit(self._gaze_upon_luminous_scribe): "readme_description",
            }
            for future in as_completed(future_map):
                rite_name = future_map[future]
                try:
                    res = future.result()
                    if res: self.dossier.update(res)
                except Exception as e:
                    Logger.warn(f"Parallel Paradox in '{rite_name}': {e}")

    def _conduct_sequential_scry(self):
        """Unified-timeline scrying for single-threaded WASM environments."""
        rites = [
            (self._gaze_upon_living_souls, "living_souls"),
            (self._gaze_upon_vcs_soul, "vcs_soul"),
            (self._gaze_upon_luminous_scribe, "readme_description")
        ]
        for rite_func, name in rites:
            try:
                res = rite_func()
                if res: self.dossier.update(res)
            except Exception as e:
                Logger.warn(f"Sequential Paradox in '{name}': {e}")

    # =========================================================================
    # == SECTION II: THE GAZE UPON FORM (ARTIFACTS)                          ==
    # =========================================================================

    def _gaze_upon_living_souls(self) -> Dict[str, Any]:
        """[FACULTY 2]: The Polyglot Gaze. Identifies technical souls."""
        results = {}
        # [ASCENSION 3]: Rank-Ordered scrying to prioritize high-fidelity indicators.
        sorted_codex = sorted(SOUL_CODEX, key=lambda x: x.get('rank', 0), reverse=True)

        for soul_law in sorted_codex:
            pattern = soul_law.get("scripture", "*")
            try:
                # [ASCENSION 10]: Efficient glob scrying
                for scripture_path in self.project_root.glob(pattern):
                    if not scripture_path.is_file(): continue

                    gaze_match = False
                    if "gaze_pattern" in soul_law:
                        # [ASCENSION 8]: Encoding Resilience
                        content = scripture_path.read_text(encoding='utf-8', errors='ignore')
                        if re.search(soul_law["gaze_pattern"], content):
                            gaze_match = True
                    else:
                        gaze_match = True

                    if gaze_match:
                        self.perceived_souls.add(soul_law["name"])
                        Logger.verbose(f"      -> Perceived '{soul_law['name']}' in '{scripture_path.name}'")
                        break  # Only need one proof per type
            except Exception:
                continue

        if self.perceived_souls:
            results['project_type'] = ", ".join(sorted(list(self.perceived_souls)))
        return results

    def _gaze_upon_vcs_soul(self) -> Dict[str, Any]:
        """[FACULTY 4]: The Scribe of Provenance. Scries Git DNA."""
        dot_git = self.project_root / ".git"
        if not dot_git.is_dir(): return {}

        results = {}

        # [ASCENSION 4]: Substrate-Aware Git Scrying
        # We first attempt a physical probe to avoid the 'subprocess' ward in WASM.
        try:
            config_path = dot_git / "config"
            if config_path.exists():
                config_text = config_path.read_text(encoding='utf-8', errors='ignore')
                url_match = re.search(r'url\s*=\s*(.*)', config_text)
                if url_match:
                    url = url_match.group(1).strip()
                    # [ASCENSION 9]: Deep URL Suture
                    m = re.search(r'(?:[:/])([\w.-]+)/([\w.-]+?)(?:\.git)?$', url)
                    if m:
                        results['git_org'] = m.group(1)
                        results['git_repo'] = m.group(2)
        except:
            pass

        # Fallback to CLI for high-fidelity author Gnosis (Iron only)
        if not results and not self._is_wasm:
            try:
                name = subprocess.check_output(['git', 'config', 'user.name'],
                                               cwd=self.project_root, text=True, stderr=subprocess.DEVNULL).strip()
                if name: results['git_author'] = name
            except:
                pass

        return results

    def _gaze_upon_luminous_scribe(self) -> Dict[str, Any]:
        """[FACULTY 8]: The Gaze of the Luminous Scribe (README)."""
        readme_path = self.project_root / "README.md"
        if not readme_path.is_file(): return {}

        try:
            # [ASCENSION 8]: V2 Header Sieve
            content = readme_path.read_text(encoding='utf-8', errors='ignore')
            # Scries for the first H1 header and the subsequent non-empty line
            match = re.search(r'^#\s*.*?\n+([^\n#]+)', content, re.MULTILINE)
            if match:
                return {'readme_description': match.group(1).strip()}
        except:
            pass
        return {}

    # =========================================================================
    # == SECTION III: THE CONVERGENCE (SYNTHESIS)                            ==
    # =========================================================================

    def _adjudicate_architectural_canon(self):
        """Movement II: The Symphony of the Canon."""
        for primitive in ARCHITECTURAL_CANON:
            if primitive.key not in self.dossier:
                try:
                    # Each rite is shielded by the Oracle's presence
                    val = primitive.prophecy_rite(self)
                    if val is not None:
                        self.dossier[primitive.key] = val
                except:
                    pass

    def _synthesize_final_gnosis(self):
        """[FACULTY 6]: The AI's Final Word. Forge the coherent reality."""

        # 1. Project Name Sovereignty
        # Hierarchy: git_repo > project_name > directory_name
        if 'project_name' not in self.dossier:
            name = self.dossier.get('git_repo') or self.project_root.name
            self.dossier['project_name'] = name.lower().replace(" ", "-")

        # 2. Author Identity
        # [ASCENSION 10]: Hierarchy: git_author > user > default
        if 'author' not in self.dossier:
            self.dossier['author'] = self.dossier.get('git_author') or getpass.getuser()

        # 3. Semantic Description Fusion
        # [ASCENSION 6]: Merges tech-soul with purpose.
        if 'description' not in self.dossier:
            base = self.dossier.get('readme_description')
            if not base:
                tech = self.dossier.get('project_type', 'generic')
                base = f"A new {tech} project."
            self.dossier['description'] = base

        # 4. [ASCENSION 11]: Socratic Suggestion
        if not self.perceived_souls:
            self.dossier['_oracle_hint'] = "The reality is a void. Consider the 'python-basic' archetype."

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_ORACLE root={self.project_root.name} substrate={'ETHER' if self._is_wasm else 'IRON'}>"


# =========================================================================================
# == THE DIVINE GATEWAY (V-Ω-ETERNAL)                                                   ==
# =========================================================================================

def prophesy_initial_gnosis(project_root: Path) -> Dict[str, Any]:
    """
    The one true, public gateway to the Oracle.
    Forges the mind and commands the conduct of the Inquest.
    """
    oracle = OracleOfTheLivingSoul(project_root)
    return oracle.conduct_inquest()

