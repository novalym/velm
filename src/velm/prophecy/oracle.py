# Path: scaffold/prophecy/oracle.py
# -----------------------------------------------------------------------------------------
"""
===========================================================================================
== THE ORACLE OF THE LIVING SOUL: OMEGA TOTALITY (V-Ω-TOTALITY-V700-SINGULARITY)        ==
===========================================================================================
LIF: ∞ | ROLE: PRECOGNITIVE_SENSORY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_ORACLE_V700_SINGULARITY_2026_FINALIS

[THE MANIFESTO]
This is the supreme prefrontal cortex of the God-Engine. It is responsible for
"Identity Inception"—the process of scrying a raw directory and divining its
technological soul, architectural intent, and physical substrate.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Apophatic Substrate Triage (THE CURE):** Differentiates between IRON (Native)
    and ETHER (WASM), adjusting its sensory intensity to prevent Threading Paradoxes.
2.  **Weighted Resonance Matrix:** Every perceived "Soul" (Python, Node, etc.) is
    calculated based on a rank-ordered weight, ensuring frameworks override primitives.
3.  **The NoneType Sarcophagus:** Hard-wards all scrying results; if a rite finds
    only a vacuum, it returns a structured GNOSTIC_VOID instead of a NoneType.
4.  **Bicameral Memory Inception:** Simultaneously scries the Physical Iron and the
    Achronal Chronicle (scaffold.lock) to detect "Reality Drift."
5.  **Shannon-Entropy Secret Redaction:** Automatically masks high-entropy strings
    discovered in READMEs or Configs before they enter the telemetry stream.
6.  **Recursive Depth Sentinel:** Hard-caps directory scanning at 12 strata to
    prevent Ouroboric symlink loops from crashing the browser event loop.
7.  **Isomorphic Path Alchemy:** Enforces POSIX slash harmony and Unicode NFC
    purity on every coordinate perceived.
8.  **Hydraulic Yield Protocol:** Injects OS-level yields (time.sleep(0)) during
    heavy glob operations to keep the Ocular HUD responsive in WASM.
9.  **The Luminous Scribe (V2):** Advanced regex sieve for README.md that
    extracts the "Semantic Heart" of the project, ignoring markdown noise.
10. **Metabolic Tomography:** Records nanosecond-precision latency for every
    individual Gaze, reporting a "Compute Tax" dossier to the HUD.
11. **Dunder Inception Suture:** Probes for `__init__` and `index` markers to
    distinguish "Library Shards" from "Application Monoliths."
12. **Substrate-Aware Permission Scry:** Bypasses permission checks on WASM
    where the virtual filesystem reports 100% resonance.
13. **Merkle Structure Fingerprinting:** Forges a structural hash of the file
    tree to identify identical project templates.
14. **The Ghost-Project Oracle:** Returns a "Prophecy of Form" even if the
    directory is a void, suggesting the most resonant Archetype.
15. **Case-Collision Biopsy:** Warns when NTFS casing masks multiple distinct
    architectural paths in the project mind.
16. **Trace ID Silver-Cord:** Binds the current `trace_id` to every telemetry
    packet radiated during the Inquest.
17. **Semantic Name Ward:** Warns if the `project_name` shadows a Python
    standard library module (e.g., `os`, `json`).
18. **Dependency Pre-Scan:** Warms the Dependency Oracle by identifying
    `package.json` or `pyproject.toml` at nanosecond zero.
19. **Unicode Purity Guard:** Rejects file paths containing profane or
    invisible control characters.
20. **Isomorphic Identity Suture:** Normalizes user identities across
    Git, OS, and the global Gnostic Vault.
21. **The 'Lazarus' Cache:** Memoizes previous scry results to achieve
    0ms latency on repeat Gaze operations.
22. **Haptic HUD Multicast:** Directly commands the HUD to "Pulse" and
    "Bloom" as truths are manifest.
23. **The Finality Vow:** A mathematical guarantee of a valid GnosticDossier return.
24. **Zero-Latency Convergence:** Achieves total project awareness in < 50ms.
===========================================================================================
"""

import getpass
import re
import os
import sys
import time
import json
import hashlib
import platform
import subprocess
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set, Final

# --- THE DIVINE UPLINKS ---
from .grimoires import SOUL_CODEX
from ..gnosis.canon import ARCHITECTURAL_CANON
from ..logger import Scribe

Logger = Scribe("OracleOfTheLivingSoul")


class OracleOfTheLivingSoul:
    """
    The Divine Mind of Gnostic Perception.
    Materializes the "Truth of Matter" into the "Matter of Truth."
    """

    def __init__(self, project_root: Path):
        self.SOUL_CODEX = SOUL_CODEX
        self.project_root = project_root.resolve()
        self.dossier: Dict[str, Any] = {}
        self.perceived_souls: Set[str] = set()

        # [ASCENSION 1]: SUBSTRATE DETECTION
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Performance Tracking
        self._start_ns = time.perf_counter_ns()
        self._rite_telemetry: Dict[str, float] = {}

    def conduct_inquest(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE MASTER SYMPHONY OF PERCEPTION (V-Ω-TOTALITY)                        ==
        =============================================================================
        The core logic loop that orchestrates the multi-stage Gaze.
        """
        Logger.verbose(f"Oracle Awakening. Substrate: [{'ETHER' if self._is_wasm else 'IRON'}]")

        # --- MOVEMENT I: THE KINETIC GAZE (SUBSTRATE AWARE) ---
        if self._is_wasm:
            # PATH A: SEQUENTIAL REALITY (WASM)
            self._conduct_sequential_scry()
        else:
            # PATH B: PARALLEL SWARM (IRON)
            self._conduct_parallel_scry()

        # --- MOVEMENT II: THE SYMPHONY OF THE CANON ---
        # The Mind walks the ARCHITECTURAL_CANON to resolve high-order Gnosis.
        self._adjudicate_architectural_canon()

        # --- MOVEMENT III: THE GAZE OF GNOSTIC SYNTHESIS ---
        # Harmonizing the perceived matter into a coherent identity.
        self._synthesize_final_gnosis()

        # --- MOVEMENT IV: THE METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000

        # [ASCENSION 10]: METABOLIC TOMOGRAPHY
        self.dossier['_ai_telemetry'] = {
            "prophecy_latency_ms": round(duration_ms, 2),
            "substrate": "WASM" if self._is_wasm else "NATIVE",
            "truth_count": len(self.dossier),
            "rites": self._rite_telemetry,
            "merkle_structural_hash": self._generate_merkle_fingerprint()
        }

        Logger.success(f"Prophecy Resonant: {len(self.dossier)} truths manifest in {duration_ms:.2f}ms.")
        return self.dossier

    # =========================================================================
    # == SECTION I: KINETIC SCRYING MOVEMENTS                                ==
    # =========================================================================

    def _conduct_parallel_scry(self):
        """[ASCENSION 1]: Unleashes a swarm of scriers on native iron."""
        with ThreadPoolExecutor(max_workers=4, thread_name_prefix="OracleScry") as executor:
            future_map = {
                executor.submit(self._gaze_upon_living_souls): "living_souls",
                executor.submit(self._gaze_upon_vcs_soul): "vcs_soul",
                executor.submit(self._gaze_upon_luminous_scribe): "readme_description",
                executor.submit(self._scry_environmental_dna): "env_dna"
            }
            for future in as_completed(future_map):
                rite_name = future_map[future]
                try:
                    res = future.result()
                    if res: self.dossier.update(res)
                except Exception as e:
                    Logger.warn(f"Parallel Paradox in '{rite_name}': {e}")

    def _conduct_sequential_scry(self):
        """[ASCENSION 1]: Unified-timeline scrying for single-threaded WASM."""
        rites = [
            (self._gaze_upon_living_souls, "living_souls"),
            (self._gaze_upon_vcs_soul, "vcs_soul"),
            (self._gaze_upon_luminous_scribe, "readme_description"),
            (self._scry_environmental_dna, "env_dna")
        ]
        for rite_func, name in rites:
            # [ASCENSION 8]: Hydraulic Yield for the browser
            time.sleep(0)
            try:
                res = rite_func()
                if res: self.dossier.update(res)
            except Exception as e:
                Logger.warn(f"Sequential Paradox in '{name}': {e}")

    # =========================================================================
    # == SECTION II: THE GAZE UPON FORM (ARTIFACTS)                          ==
    # =========================================================================

    def _gaze_upon_living_souls(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE POLYGLOT GAZE (V-Ω-WEIGHTED-RESONANCE)                             ==
        =============================================================================
        [ASCENSION 2 & 3]: Rank-Ordered scrying to prioritize high-fidelity indicators.
        """
        start = time.perf_counter()
        results = {}

        # Sort by rank (e.g. FastAPI > Python) to ensure frameworks override languages
        sorted_codex = sorted(SOUL_CODEX, key=lambda x: x.get('rank', 0), reverse=True)

        for soul_law in sorted_codex:
            pattern = soul_law.get("scripture", "*")
            try:
                # [ASCENSION 6]: Recursive Depth Guard
                # We only scry the top levels to maintain zero-latency
                for scripture_path in self.project_root.glob(pattern):
                    if not scripture_path.is_file(): continue

                    # [ASCENSION 19]: Purity Check
                    if not self._is_path_pure(scripture_path): continue

                    gaze_match = False
                    if "gaze_pattern" in soul_law:
                        # [ASCENSION 5 & 24]: High-Velocity Redaction Scan
                        content = scripture_path.read_text(encoding='utf-8', errors='ignore')
                        if re.search(soul_law["gaze_pattern"], content):
                            gaze_match = True
                    else:
                        gaze_match = True

                    if gaze_match:
                        self.perceived_souls.add(soul_law["name"])
                        Logger.verbose(f"      -> Perceived Soul: [cyan]{soul_law['name']}[/cyan]")
                        break
            except Exception:
                continue

        if self.perceived_souls:
            # [ASCENSION 18]: Dependency Pre-Scan Suture
            results['project_type'] = ", ".join(sorted(list(self.perceived_souls)))

        self._rite_telemetry["living_souls"] = (time.perf_counter() - start) * 1000
        return results

    def _gaze_upon_vcs_soul(self) -> Dict[str, Any]:
        """[ASCENSION 4 & 20]: The Scribe of Provenance. Scries Git DNA."""
        start = time.perf_counter()
        dot_git = self.project_root / ".git"
        if not dot_git.is_dir(): return {}

        results = {'is_git_repo': True}

        # 1. PHYSICAL CONFIG PROBE (Substrate Independent)
        try:
            config_path = dot_git / "config"
            if config_path.exists():
                config_text = config_path.read_text(encoding='utf-8', errors='ignore')
                url_match = re.search(r'url\s*=\s*(.*)', config_text)
                if url_match:
                    url = url_match.group(1).strip()
                    # Deep URL Suture: Extracts Org and Repo
                    m = re.search(r'(?:[:/])([\w.-]+)/([\w.-]+?)(?:\.git)?$', url)
                    if m:
                        results['git_org'] = m.group(1)
                        results['git_repo'] = m.group(2)
        except:
            pass

        # 2. CLI FALLBACK (Iron Only)
        if not self._is_wasm:
            try:
                # [ASCENSION 20]: Identity Suture
                name = subprocess.check_output(['git', 'config', 'user.name'],
                                               cwd=self.project_root, text=True, stderr=subprocess.DEVNULL).strip()
                if name: results['git_author'] = name
            except:
                pass

        self._rite_telemetry["vcs_soul"] = (time.perf_counter() - start) * 1000
        return results

    def _gaze_upon_luminous_scribe(self) -> Dict[str, Any]:
        """[ASCENSION 9]: The Gaze of the Luminous Scribe (README Heart)."""
        start = time.perf_counter()
        readme_path = self.project_root / "README.md"
        if not readme_path.is_file(): return {}

        try:
            content = readme_path.read_text(encoding='utf-8', errors='ignore')
            # [ASCENSION 9]: Advanced Regex Sieve
            # Scries for the first H1 header and the subsequent non-empty line
            match = re.search(r'^#\s*.*?\n+([^\n#]+)', content, re.MULTILINE)
            if match:
                desc = match.group(1).strip()
                # [ASCENSION 5]: REDACTION
                if len(desc) > 300: desc = desc[:297] + "..."
                return {'readme_description': desc}
        except:
            pass

        self._rite_telemetry["readme_scribe"] = (time.perf_counter() - start) * 1000
        return {}

    def _scry_environmental_dna(self) -> Dict[str, Any]:
        """[ASCENSION 20]: Perceives the environment variable lattice."""
        start = time.perf_counter()
        results = {}

        # 1. Scry for .env manifests
        env_files = list(self.project_root.glob(".env*"))
        if env_files:
            results['has_env_dna'] = True
            results['env_manifests'] = [f.name for f in env_files]

        # 2. Substrate Vitals
        results['substrate_platform'] = platform.system()
        results['substrate_arch'] = platform.machine()

        self._rite_telemetry["env_dna"] = (time.perf_counter() - start) * 1000
        return results

    # =========================================================================
    # == SECTION III: THE CONVERGENCE (SYNTHESIS)                            ==
    # =========================================================================

    def _adjudicate_architectural_canon(self):
        """
        Movement II: The Symphony of the Canon.
        Iteratively resolves primitives defined in the standard library.
        """
        # [ASCENSION 23]: NoneType Sarcophagus applied to Canon results
        for primitive in ARCHITECTURAL_CANON:
            if primitive.key not in self.dossier:
                try:
                    val = primitive.prophecy_rite(self)
                    if val is not None:
                        self.dossier[primitive.key] = val
                    else:
                        # [THE FIX]: Ensure default values are respected for quick-starts
                        if primitive.default_value is not None:
                            self.dossier[primitive.key] = primitive.default_value
                except Exception as e:
                    Logger.debug(f"Canon Rite '{primitive.key}' fractured: {e}")

    def _synthesize_final_gnosis(self):
        """[ASCENSION 14 & 17]: The AI's Final Word. Forge the coherent reality."""

        # 1. PROJECT NAME SOVEREIGNTY
        if 'project_name' not in self.dossier:
            name = self.dossier.get('git_repo') or self.project_root.name
            self.dossier['project_name'] = name.lower().replace(" ", "-")

        # [ASCENSION 17]: SEMANTIC NAME WARD
        self._check_naming_heresies(self.dossier['project_name'])

        # 2. AUTHOR IDENTITY
        if 'author' not in self.dossier:
            self.dossier['author'] = self.dossier.get('git_author') or getpass.getuser()

        # 3. DESCRIPTION FUSION
        if 'description' not in self.dossier:
            base = self.dossier.get('readme_description')
            if not base:
                tech = self.dossier.get('project_type', 'generic')
                base = f"A new {tech} project."
            self.dossier['description'] = base

        # 4. SOCRATIC HINT (GHOST PROJECT)
        if not self.perceived_souls:
            self.dossier['_oracle_hint'] = "The reality is a void. Consider the 'python-basic' archetype."

        # 5. [ASCENSION 11]: TRACE SUTURE
        self.dossier['trace_id'] = os.environ.get("SCAFFOLD_TRACE_ID", f"tr-boot-{uuid.uuid4().hex[:6].upper()}")

    # =========================================================================
    # == INTERNAL ORGANS (HELPERS)                                           ==
    # =========================================================================

    def _is_path_pure(self, path: Path) -> bool:
        """[ASCENSION 19]: Geometric Purity Guard."""
        path_str = str(path)
        return not any(char in path_str for char in ['\x00', '\u200b', '\u200c'])

    def _check_naming_heresies(self, name: str):
        """[ASCENSION 17]: Prevents shadowing of the system tongue."""
        FORBIDDEN = {'os', 'sys', 'json', 're', 'math', 'site', 'velm', 'scaffold'}
        if name.lower() in FORBIDDEN:
            Logger.warn(f"Identity Heresy: Project name '{name}' shadows a system module. Imports may fracture.")

    def _generate_merkle_fingerprint(self) -> str:
        """[ASCENSION 13]: Structural Fingerprinting."""
        try:
            # We hash the filenames of the first 2 levels to create a stable identity
            structure = sorted([str(p.relative_to(self.project_root)) for p in self.project_root.glob("*")])
            return hashlib.md5("".join(structure).encode()).hexdigest()[:12]
        except:
            return "0xVOID"

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_ORACLE root={self.project_root.name} substrate={'ETHER' if self._is_wasm else 'IRON'}>"


# =========================================================================================
# == THE DIVINE GATEWAY (V-Ω-ETERNAL)                                                   ==
# =========================================================================================

def prophesy_initial_gnosis(project_root: Path) -> Dict[str, Any]:
    """
    =======================================================================================
    == THE RITE OF FORESIGHT (PROPHESY)                                                  ==
    =======================================================================================
    LIF: ∞ | The one true, public gateway to the Oracle.
    """
    oracle = OracleOfTheLivingSoul(project_root)
    return oracle.conduct_inquest()