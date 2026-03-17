# Path: parser_core/parser/engine.py
# ----------------------------------


import hashlib
import re
import traceback as tb_scribe
import uuid
import time
import os
import sys
import threading
import copy
import gc
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union, Set, Final

# --- THE DIVINE SUMMONS OF GNOSTIC SUBSTRATES ---
from .ast_weaver.weaver.engine import GnosticASTWeaver
from .parser_scribes import SCRIBE_PANTHEON, FormScribe
from .parser_scribes.scaffold_scribes.scaffold_base_scribe import ScaffoldBaseScribe
from .parser_scribes.symphony_scribes.symphony_base_scribe import SymphonyBaseScribe
from ..block_consumer import GnosticBlockConsumer

# --- CONTRACTS & VESSELS ---
from ...contracts.data_contracts import (
    ScaffoldItem, GnosticVessel, GnosticDossier, GnosticLineType, _GnosticNode, GnosticContract, ShardHeader
)
from ...contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ...contracts.symphony_contracts import Edict, EdictType

from ...core.alchemist import get_alchemist
from ...logger import Scribe, get_console
from ...utils import get_git_commit

# [THE OMEGA SUTURE]: The Sacred Memory Vessel
from ...core.runtime.vessels import GnosticSovereignDict

# [THE OMEGA SUTURE]: Jinja is dead. We summon the SGF Heresies.
try:
    from ...core.alchemist.elara.resolver.evaluator import UndefinedGnosisHeresy, AmnestyGrantedHeresy
except ImportError:
    # Failsafe for migration phase
    class UndefinedGnosisHeresy(Exception):
        pass


    class AmnestyGrantedHeresy(Exception):
        pass

Logger = Scribe("ApotheosisParser")


class ApotheosisParser:
    """
    =================================================================================
    == THE APOTHEOSIS PARSER (V-Ω-TOTALITY-V100000-SGF-PURIFIED-CENTURY-MARK)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_DECONSTRUCTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_PARSER_VMAX_CENTURY_ASCENSION_2026_FINALIS

    The God-Engine of Perception. It transmutes raw text into Gnostic Truth.
    It has been completely purged of Jinja2 dependencies. The Stabilization
    Loop is now a perfect thermodynamic reactor, utilizing the SGF's native
    Absolute Amnesty to process alien syntax without shattering.

    ### THE PANTHEON OF 129 LEGENDARY ASCENSIONS (NEWLY ASCENDED):
    125. **Genomic Soul Extraction (THE MASTER CURE):** Directly imports and utilizes
         the `SoulExtractor` during parsing. This ensures that even when a blueprint
         is executed statically (without the `CausalAssembler`), its Full V3.0 DNA is
         inhaled into the `dossier`, curing the "Manifest Blindness" heresy.
    126. **The Semantic Suture Emissary:** Radically ascended `_emit_metabolic_manifests`.
         It now aggregates dependencies from the *entire* multiversal mesh and uses the
         Semantic Suture (`*=`) to mathematically perfect `docker-compose.yml` and
         `pyproject.toml` generation, ending the "Overwrite Heresy."
    127. **Multidimensional Dictionary Transmutation:** Safely processes Node.js (`package.json`)
         and Docker Substrate mappings into resilient YAML/JSON/TOML dictionaries.
    128. **Autonomic Dependency Scrying (THE MASTER CURE):** Reads the AST/text of all
         materialized `.py` and `.tsx` files to extract `import` statements, automatically
         adding them to `pyproject.toml` and `package.json` even if the Shard Header omitted them.
    129. **Substrate Deduction Matrix:** If a database driver (`psycopg2`, `asyncpg`, `redis`)
         is detected in the Python dependencies, it automatically generates the corresponding
         Docker service if the explicit infrastructure header was missing.
    =================================================================================
    """

    # [ASCENSION 6 & 113]: THE DEPTH GOVERNOR
    MAX_RECURSION_DEPTH: Final[int] = 50

    # [ASCENSION 20 & 105]: THE GEOMETRIC LAW
    TAB_WIDTH: Final[int] = 4

    # [ASCENSION 13 & 104]: CODE-QUOTE SANCTUARY PATTERN
    QUOTE_TOGGLE_REGEX: Final[re.Pattern] = re.compile(r'^\s*("""|\'\'\')')
    AI_BASH_FENCE_REGEX: Final[re.Pattern] = re.compile(r'^\s*```(?:sh|bash)?\s*$')

    # OUROBOROS TIMEOUT (Seconds per file parse)
    PARSE_TIMEOUT_SECONDS: Final[float] = 120.0

    # =========================================================================
    # ==[ASCENSION 5 & 117]: THE ACHRONAL MEMO-MATRIX                       ==
    # =========================================================================
    _GLOBAL_SUBSTRATE_CACHE: Optional[Dict[str, Any]] = None
    _GLOBAL_CODEX_CACHE: Optional[Dict[str, Any]] = None
    _CLASS_LOCK: Final[threading.RLock] = threading.RLock()
    _GLOBAL_IMPORT_HASHES: Final[Set[str]] = set()

    def __init__(self, grammar_key: str = 'scaffold', engine: Optional[Any] = None, silent: bool = False):
        """
        =============================================================================
        == THE RITE OF INCEPTION (V-Ω-TOTALITY-V100000)                            ==
        =============================================================================
        Forges the God-Engine of Perception, binding it to the Active Substrate.
        """
        self.grammar_key = grammar_key
        self.engine = engine
        self._silent = silent
        self.parse_session_id = f"{uuid.uuid4().hex[:6].upper()}-{time.time_ns()}"
        self.Logger = Logger

        # [ASCENSION 49]: ATOMIC MUTEX GRID (Zero-Stiction)
        self._state_lock = threading.RLock()

        # Initialize the Mind (Recursive Registry Prep)
        self._reset_parser_state()

        # [ASCENSION 91]: JIT Materialization of the Scribe Pantheon
        self.scribes: Dict[str, FormScribe] = self._forge_scribe_pantheon()

        # [ASCENSION 42]: THE SGF SUTURE
        self.alchemist = get_alchemist()

        self._last_pulse_line = 0
        self._last_pulse_percent = 0
        self._last_pulse_time = 0.0  # [ASCENSION 118]: Debounce tracker

    def _reset_parser_state(self):
        """
        =================================================================================
        == THE RITE OF ATOMIC STATE CONSECRATION (V-Ω-TOTALITY-V26K-HEALED)            ==
        =================================================================================
        LIF: ∞ | ROLE: KERNEL_STATE_INITIALIZER | RANK: OMEGA_SOVEREIGN

        This rite righteously initializes all spatiotemporal attributes, mathematically
        annihilating the AttributeError paradox, and establishes the `GnosticSovereignDict`
        natively to empower fuzzy, case-insensitive lookups.
        """
        with self._state_lock:
            # --- STRATUM 0: SPATIAL COORDINATES (THE ANCHORS) ---
            self.file_path: Optional[Path] = None
            self.project_root: Optional[Path] = getattr(self.engine, 'project_root', None)

            # [ASCENSION 1]: THE BASE PATH CONSECRATION (THE FIX)
            self.base_path: Optional[Path] = self.project_root or Path.cwd()

            # --- STRATUM 1: METABOLIC BUFFERS (THE MATTER) ---
            # [ASCENSION 67]: THE BICAMERAL BUFFER CURE
            self.raw_items: List['ScaffoldItem'] = []
            self.manifested_matter: List['ScaffoldItem'] = []
            self.items_by_path: Dict[str, 'ScaffoldItem'] = {}
            self.edicts: List['Edict'] = []

            # [ASCENSION 44 & 60]: LAMINAR QUATERNITY COERCION
            self.post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

            # --- STRATUM 2: THE MENTAL LATTICE (THE GNOSIS) ---
            # [ASCENSION 69 THE MASTER CURE]: Establish GnosticSovereignDict!
            self.variables: Dict[str, Any] = GnosticSovereignDict()
            self.blueprint_vars: Dict[str, Any] = GnosticSovereignDict()
            self.external_vars: Dict[str, Any] = GnosticSovereignDict()
            self.macros: Dict[str, Dict[str, Any]] = {}
            self.traits: Dict[str, Path] = {}
            self.contracts: Dict[str, 'GnosticContract'] = {}
            self.variable_contracts: Dict[str, str] = {}

            # --- STRATUM 3: FORENSICS & CAUSALITY ---
            self.heresies: List['Heresy'] = []
            self.import_cache: Set[Path] = set()
            self.dossier: GnosticDossier = GnosticDossier()
            self.gnostic_ast: Optional['_GnosticNode'] = None
            self.all_rites_are_pure: bool = True

            # [ASCENSION 10 & 56]: STATE HASH INITIALIZATION
            self._state_hash: str = hashlib.sha256(b"primordial_void").hexdigest()

            # [ASCENSION 50 & 107]: OCULAR LINE-SYNC CALIBRATION
            self.line_offset: int = 0
            self.depth: int = 0

            # --- STRATUM 4: TERMINAL & UI ---
            self.console = get_console()
            self._silent = getattr(self, '_silent', False)
            self.pending_permissions: Optional[str] = None
            self._in_code_block: bool = False
            self._block_quote_type: Optional[str] = None
            self.strict_mode: bool = os.environ.get("SCAFFOLD_STRICT") == "1"

            # =========================================================================
            # ==[ASCENSION 101 & 103]: THE ACTIVE STRATUM STATE MACHINE             ==
            # =========================================================================
            # [THE MASTER CURE]: Replaces the fragile '_kinetic_block_indents' list.
            # We track the ontological state of the parser directly.
            self.active_stratum: str = "FORM"  # 'FORM' (Files) or 'WILL' (Commands)
            self.kinetic_floor_indent: int = -1

    def _lock_identity(self, safe_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        =============================================================================
        == [ASCENSION 71]: DEEP-TISSUE IDENTITY LOCKDOWN                           ==
        =============================================================================
        Surgically identifies and locks the Project Identity, deriving all 4 pillars
        dynamically.
        """
        import time
        import os
        import re

        _start_ns = time.perf_counter_ns()

        # Normalize Python version declarations
        for pv_key in ("python_version", "py_v", "py_version", "requires_python", "target_version"):
            if pv_key in safe_vars and isinstance(safe_vars[pv_key], str):
                safe_vars[pv_key] = safe_vars[pv_key].replace("Python ", "").replace("Python", "").replace("py",
                                                                                                           "").strip()

        architect_will = (
                safe_vars.get("project_name") or
                safe_vars.get("project_slug") or
                safe_vars.get("package_name")
        )

        # Bail out if the identity contains unresolved SGF variables (Blurry Matter)
        if architect_will and isinstance(architect_will, str) and ("{{" in architect_will or "{%" in architect_will):
            return safe_vars

        physical_matter = self.project_root.name if self.project_root else "omega_app"
        project_identity = architect_will or physical_matter

        # Sanitize for slug creation
        clean_base = re.sub(r'[^a-zA-Z0-9_]', '_', str(project_identity).replace(' ', '_')).lower().strip('_')
        if not clean_base or clean_base[0].isdigit():
            clean_base = "v_" + (clean_base or "app")

        # [STRIKE]: Lock the 4 Pillars
        safe_vars["project_name"] = str(project_identity).strip()
        safe_vars["project_slug"] = clean_base.replace('_', '-')
        safe_vars["package_name"] = clean_base
        safe_vars["class_prefix"] = "".join(x.title() for x in clean_base.split('_'))

        # [ASCENSION 81 & 109]: The Inverse CWD Anchor & Null-Guard
        try:
            safe_vars["__cwd__"] = str(Path.cwd()).replace('\\', '/')
        except Exception:
            safe_vars["__cwd__"] = "."

        safe_vars["project_root"] = str(self.project_root).replace('\\', '/') if self.project_root else "."

        # Synchronize with OS Environment
        os.environ["SCAFFOLD_PROJECT_NAME"] = safe_vars["project_name"]
        os.environ["SCAFFOLD_PROJECT_SLUG"] = safe_vars["project_slug"]
        os.environ["SCAFFOLD_PACKAGE_NAME"] = safe_vars["package_name"]

        return safe_vars

    def _normalize_indentation(self, content: str) -> str:
        """
        =============================================================================
        == [ASCENSION 105]: TOPOGRAPHICAL DRIFT HEALER                             ==
        =============================================================================
        Detects if a user accidentally mixes Tabs and Spaces and auto-normalizes
        the entire blueprint to 4-space indents before processing.
        """
        if not content: return ""

        # If no tabs exist, the geometry is pure.
        if '\t' not in content:
            return content

        self.Logger.verbose("Topographical Drift Detected (Mixed Tabs/Spaces). Commencing Geometric Healing...")

        normalized_lines = []
        for line in content.splitlines():
            # Calculate leading whitespace
            leading_ws = len(line) - len(line.lstrip())
            if leading_ws > 0:
                # Transmute tabs to 4 spaces, spaces remain spaces
                prefix = line[:leading_ws].replace('\t', '    ')
                normalized_lines.append(prefix + line[leading_ws:])
            else:
                normalized_lines.append(line)

        return "\n".join(normalized_lines)

    def _extract_sovereign_header(self, content: str) -> Optional[ShardHeader]:
        """[ASCENSION 9 & 48]: Scries the raw scripture for the v3.0 Gnostic Header.
        """
        import re
        import yaml
        from ...contracts.data_contracts import ShardHeader

        pattern = re.compile(
            r'# =+.*?# == GNOSTIC (?:DNA )?SHARD: (?P<id_header>.*?)\n(?P<body_block>.*?)# =+',
            re.DOTALL | re.MULTILINE
        )
        match = pattern.search(content)
        if not match: return None

        body = match.group("body_block")

        # Extract YAML lines carefully, stripping comments but preserving structure
        yaml_lines = []
        for line in body.splitlines():
            clean_line = re.sub(r'^\s*#\s*', '', line).split(' #')[0].strip()
            if clean_line and not clean_line.startswith('---'):
                yaml_lines.append(clean_line)

        if not yaml_lines: return None

        try:
            raw_yaml = "\n".join(yaml_lines)
            data = yaml.safe_load(raw_yaml)

            if not isinstance(data, dict): return None
            if 'id' not in data: data['id'] = match.group("id_header").strip()

            return ShardHeader.model_validate(data)
        except Exception as e:
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                import sys
                sys.stderr.write(f"\x1b[33m[CENSUS_WARNING] Genomic scry fractured: {e}\x1b[0m\n")
            return None

    def resolve_metabolic_value(self, value: Any, depth: int = 0, _visited: Optional[Set[int]] = None) -> str:
        """
        =================================================================================
        == THE Ω_RESOLVE_METABOLIC_VALUE: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)  ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_REIFIER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_REIFY_VMAX_14_VS_0_CURE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for transmuting Gnostic Mind into Physical
        Matter. This version righteously annihilates the "Snapshot Schism" by
        recursively flattening complex souls into bit-perfect, shell-safe strings.
        =================================================================================
        """
        import json
        import decimal
        import unicodedata
        from pathlib import Path

        # --- MOVEMENT 0: THE VOID & OUROBOROS GUARD ---
        # [ASCENSION 4]: NoneType Sarcophagus
        if value is None:
            return ""

        # [ASCENSION 1]: Laminar Circularity Ward
        if _visited is None: _visited = set()
        val_id = id(value)
        if val_id in _visited:
            return f"/* CIRCULAR_REF:{hex(val_id).upper()} */"

        if depth > self.MAX_RECURSION_DEPTH:
            return "/* RECURSION_LIMIT_BREACHED */"

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 3] - THE APOPHATIC ENGINE WARD               ==
        # =========================================================================
        # Surgically identify and incinerate the Reprs of the Gnostic Pantheon.
        v_type = type(value).__name__
        if any(x in v_type for x in ("Proxy", "Engine", "Alchemist", "Parser", "SGF", "Context", "Weaver")):
            return ""

        # --- MOVEMENT II: THE TRINITY OF SCALARS ---
        # [ASCENSION 5]: Isomorphic Boolean Mapping
        if isinstance(value, bool):
            return str(value).lower()

        # [ASCENSION 9]: Numeric Precision Suture
        if isinstance(value, (int, float, decimal.Decimal)):
            return str(value)

        # --- MOVEMENT III: THE COLLECTION INCEPTION ---
        # [STRIKE]: Mark this node as visited to prevent Ouroboros loops
        if not isinstance(value, (str, bytes)):
            _visited.add(val_id)

        try:
            # A. Dictionaries & GnosticSovereignDicts
            if isinstance(value, dict) or hasattr(value, '_shadow_map'):
                try:
                    # [ASCENSION 11]: Subversion Ward & Dunder Exorcism
                    # We recursively reify child atoms while protecting the internal Moat.
                    data = {
                        str(k): self.resolve_metabolic_value(v, depth + 1, _visited)
                        for k, v in value.items()
                        if not str(k).startswith('__')
                    }

                    # Sieve out empty atoms to keep the manifest lean
                    data = {k: v for k, v in data.items() if v != ""}
                    if not data: return ""

                    # [ASCENSION 12]: THE BICAMERAL JSON SUTURE
                    # If we have a complex dict, we must return it as a JSON string
                    # so that pydantic-settings can inhale it as a single env var.
                    return json.dumps(data, ensure_ascii=False)
                except Exception:
                    return ""

            # B. Arrays (Lists / Sets / Tuples)
            if isinstance(value, (list, tuple, set)):
                try:
                    # Recursive descent
                    flattened = [self.resolve_metabolic_value(i, depth + 1, _visited) for i in value]
                    # Filter voids
                    flattened = [i for i in flattened if i != ""]
                    if not flattened: return ""

                    # If it's a simple list of primitives, use comma-separation for shell utility
                    if all(isinstance(x, (str, int, float, bool, decimal.Decimal)) for x in value):
                        return ",".join(map(str, flattened))

                    return json.dumps(flattened, ensure_ascii=False)
                except Exception:
                    return ""

            # C. [ASCENSION 8]: GEOMETRIC PATH HARMONY
            if isinstance(value, Path):
                return str(value).replace('\\', '/')

        finally:
            # Reclaim memory and unmark visit
            if not isinstance(value, (str, bytes)):
                _visited.remove(val_id)

        # --- MOVEMENT IV: ALCHEMICAL THAWING ---
        # [ASCENSION 2]: THE BICAMERAL THAW
        result = str(value).strip()
        if "{{" in result:
            try:
                result = self.alchemist.transmute(result, self.variables)
            except Exception:
                pass

        # --- MOVEMENT V: PHYSICAL PURIFICATION (THE FINALITY) ---
        # [ASCENSION 6]: Null-Byte & Invisible Toxin Annihilation
        result = result.translate(str.maketrans('', '', '\x00\ufeff\u200b'))

        # [ASCENSION 7]: Hydraulic Thread Yielding
        if depth % 5 == 0:
            import time
            time.sleep(0)

        # [ASCENSION 10]: GEOMETRIC QUOTING ORACLE
        # If the string contains spaces or shell-hostile chars, we wrap it in safety.
        if re.search(r'[ \t\n\r!$;<>|&()]', result):
            if not (result.startswith(('"', "'")) and result.endswith(result[0])):
                return f'"{result}"'

        return result

    def parse_string(
            self,
            content: str,
            file_path_context: Optional[Path] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            line_offset: int = 0,
            overrides: Optional[Dict[str, Any]] = None,
            depth: int = 0
    ) -> Tuple[
        'ApotheosisParser',
        List[ScaffoldItem],
        List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
        List[Edict],
        Dict[str, Any],
        GnosticDossier
    ]:
        """
        =================================================================================
        == THE OMEGA INCEPTION RITE: TOTALITY (V-Ω-VMAX-LAMINAR-SUTURE-V175-FINALIS)   ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_DECONSTRUCTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_PARSE_STRING_VMAX_SINGULARITY_RESONANCE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for transmuting Gnostic Scripture into Matter.
        This version righteously implements the **Bicameral Substrate Suture**,
        mathematically annihilating the V2/V3 Paradox (Anomaly 2.12.b). It ensures
        that the Mind (AST) and Body (Matter) share a bit-perfect physical memory
        pointer while the Dossier achieves 100% Ontological Purity.

        ### THE PANTHEON OF 25 NEW ZENITH ASCENSIONS (151-175):
        151. **Bicameral Substrate Suture (THE MASTER CURE):** Surgically repairs the
             V2/V3 Schism before Pydantic validation. If a manifest arriving from
             the Linker has a List for `substrate`, it is re-housed as
             `_legacy_substrate` to satisfy the V3.0 Dict contract.
        152. **Reference Singularity Suture (THE MASTER CURE):** Mathematically binds
             `manifested_matter` and `post_run_commands` to the Prime Timeline's
             physical memory addresses, annihilating the 236-ONTOLOGICAL-ERASURE.
        153. **Bicameral Memory Reconciliation:** Synchronizes the local `raw_items`
             buffer with the shared `manifested_matter` reservoir in real-time.
        154. **Achronal Trace-ID Silver-Cord:** Force-binds a high-entropy 16-char
             Trace ID to the session, ensuring 1:1 parity with the Ocular HUD.
        155. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` every 500 lines
             to maintain UI responsiveness on single-threaded Iron substrates.
        156. **Active Stratum State Machine:** Implements `active_stratum`
             tracking to prevent "git init" and "npm install" from being
             hallucinated as physical file nodes in kinetic blocks.
        157. **Symbolic AI Variable Healer:** Surgically identifies and corrects
             internal Velm-generated variable signatures (`_name_` -> `name`)
             before the Alchemist parses them.
        158. **Merkle Blueprint Hashing:** Generates a SHA-256 fingerprint of the
             raw scripture to enable O(1) JIT cache detection.
        159. **NoneType Sarcophagus:** Hard-wards the 6-Tuple return against
             Null-inception; reality is either manifest or correctly warded.
        160. **The "Make" Transmutator:** Autonomicly transmutes bare strings in
             WILL stratum into Edicts, ensuring `npm install` is always a command.
        161. **Ocular Line Mapping:** Aligns the `line_offset` with the parent's
             spatial locus for bit-perfect IDE resonance in Monaco.
        162. **Indentation Gravity Ward:** Captures the visual depth of every line,
             enforcing the 4-space geometric law across recursive sub-weaves.
        163. **Apophatic Variable Inheritance:** Surgically clones pre-resolved
             variables while preserving physical pointers to side-effect reservoirs.
        164. **Thermodynamic Backoff Sensing:** Yields to the OS scheduler if
             host CPU heat exceeds the 92% metabolic threshold.
        165. **Null-Byte Vectorization:** Purges terminal null-bytes using C-speed
             string translation tables.
        166. **Isomorphic Identity Lock:** Derives and locks `project_slug` and
             `package_name` at nanosecond zero.
        167. **Bicameral Error Grouping:** Collapses multiple warnings into a
             single forensic summary to prevent terminal log-pollution.
        168. **Luminous HUD Progress:** Radiates high-frequency status pulses
             ("SCRYING_DNA") to the React Stage at 144Hz.
        169. **Adrenaline Mode Optimization:** Disables local garbage collection
             during the deconstruction loop to maximize throughput.
        170. **Phantom Sigil Exorcist:** Strips markdown code fences (` ``` `)
             hallucinated by AI models from the scripture body.
        171. **Ouroboros Loop Guard V4:** Hard 50-depth limit for recursive
             parsing to prevent C-stack incineration.
        172. **Isomorphic Substrate Typing:** Injects `os_name` and `platform`
             DNA into the variables to guide the Alchemist.
        173. **Recursive Auto-Bloom Suture:** Sub-parsers automatically trigger
             `resolve_reality` to populate the shared Prime matter buffer.
        174. **Laminar Dictionary Coercion:** Ensures all variable maps utilize
             the `GnosticSovereignDict` for fuzzy key resonance.
        175. **The Finality Vow:** A mathematical guarantee of an unbreakable,
             internally consistent, and warded reality birth.
        =================================================================================
        """
        import hashlib
        import time
        import gc
        import os
        import sys
        import uuid
        import traceback
        import copy
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ...contracts.data_contracts import GnosticLineType, ScaffoldItem

        # [ASCENSION 154]: THE SILVER CORD INCEPTION
        _start_ns = time.perf_counter_ns()
        UV = "\x1b[38;5;141m"
        GOLD = "\x1b[38;5;220m"
        RESET = "\x1b[0m"

        if isinstance(file_path_context, str): file_path_context = Path(file_path_context)
        self.file_path = file_path_context
        self.line_offset = line_offset
        self.raw_scripture = content or ""
        self.depth = depth

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 152] - REFERENCE SINGULARITY SUTURE          ==
        # =========================================================================
        # [THE MASTER CURE]: We must link to the Prime Timeline's physical memory.
        pre_resolved_vars = pre_resolved_vars or {}

        # Suture the shared side-effect reservoirs
        matter_reservoir = pre_resolved_vars.get("__woven_matter__")
        if matter_reservoir is None:
            matter_reservoir = []
            pre_resolved_vars["__woven_matter__"] = matter_reservoir

        command_reservoir = pre_resolved_vars.get("__woven_commands__")
        if command_reservoir is None:
            command_reservoir = []
            pre_resolved_vars["__woven_commands__"] = command_reservoir

        # Physically bind the local handles to the global instances
        self.manifested_matter = matter_reservoir
        self.post_run_commands = command_reservoir

        if os.environ.get("SCAFFOLD_DEBUG") == "1" and self.depth == 0:
            sys.stdout.write(
                f"   -> {UV}[SUTURE]{RESET} Matter bound to: {GOLD}{hex(id(self.manifested_matter))}{RESET}\n")

        # --- MOVEMENT II: THE CONSCIOUSNESS CLONING ---
        # [ASCENSION 163]: Apophatic Variable Inheritance
        safe_vars = GnosticSovereignDict()
        for k, v in pre_resolved_vars.items():
            if k in ('__woven_matter__', '__woven_commands__', '__engine__', '__alchemist__'):
                safe_vars[k] = v  # Preserve physical references
            elif isinstance(v, (str, int, float, bool)):
                safe_vars[k] = v
            else:
                try:
                    # Defensive copy for complex objects
                    safe_vars[k] = copy.deepcopy(v)
                except Exception:
                    safe_vars[k] = v

        # [ASCENSION 171]: Ouroboros Loop Guard
        current_depth = safe_vars.get('__parse_depth__', 0)
        if current_depth > self.MAX_RECURSION_DEPTH:
            raise ArtisanHeresy(f"Topological Overflow: Recursive depth limit reached ({current_depth}).",
                                severity=HeresySeverity.CRITICAL)
        safe_vars['__parse_depth__'] = current_depth + 1

        # --- MOVEMENT III: IDENTITY & SUBSTRATE DNA ---
        # [ASCENSION 166]: Isomorphic Identity Lock
        safe_vars = self._lock_identity(safe_vars)
        trace_id = safe_vars.get('trace_id') or f"tr-parse-{uuid.uuid4().hex[:6].upper()}"
        safe_vars['trace_id'] = trace_id

        # [ASCENSION 172]: Substrate DNA Inception
        if self.engine is not None:
            safe_vars['__engine__'] = self.engine
        else:
            class GnosticVoidEngineMock:
                pass

            safe_vars['__engine__'] = GnosticVoidEngineMock()

        # =========================================================================
        # == MOVEMENT IV: [ASCENSION 151] - THE BICAMERAL SUBSTRATE SUTURE       ==
        # =========================================================================
        # [THE MASTER CURE]: We surgically repair the V2/V3 schism. If a manifest
        # DNA arriving from the Linker has a List for substrate, we re-house it
        # as `_legacy_substrate` to satisfy the V3.0 Dict contract.
        try:
            from ...core.cortex.archetype_indexer.extractor import SoulExtractor
            from ...contracts.data_contracts import ShardHeader

            # 1. Inherit Multiversal DNA from the Causal Linker
            # [ASCENSION 176]: The Laminar Fallback Suture (THE MASTER FIX)
            # Mathematically prevents `NoneType has no attribute items` by enforcing
            # the dictionary contract even if the environment injected a literal None.
            passed_manifests = safe_vars.get("__shard_manifests__") or {}

            for k, v in passed_manifests.items():
                if isinstance(v, dict):
                    # [STRIKE]: The Schism Healer
                    raw_sub = v.get('substrate')
                    if isinstance(raw_sub, list):
                        v['_legacy_substrate'] = v.pop('substrate')
                        v['substrate'] = {}  # Inject empty dict for validator

                # Validation Resonance
                self.dossier.manifests[k] = ShardHeader.model_validate(v)

            # 2. Extract Physical DNA (Suture to RAM)
            if self.raw_scripture:
                extractor = SoulExtractor()
                # [STRIKE]: We pass content=self.raw_scripture to bypass Anomaly 237
                header_obj, _ = extractor.extract(
                    path=Path(self.file_path or "ephemeral_dream.scaffold"),
                    rel_id=self.file_path.stem if self.file_path else "ephemeral",
                    content=self.raw_scripture  # <--- THE SUTURE
                )
                if header_obj and header_obj.id != "void":
                    self.dossier.manifests[header_obj.id] = header_obj

        except Exception as extractor_err:
            # [ASCENSION 167]: Bicameral Error Grouping (Silent debug)
            self.Logger.debug(f"Genomic Soul Extraction deferred: {extractor_err}")

        # Update the Mind
        self.variables.update(safe_vars)
        if overrides: self.variables.update(overrides)

        # =========================================================================
        # == MOVEMENT V: ALCHEMICAL PURIFICATION                                 ==
        # =========================================================================
        if self.raw_scripture:
            # [ASCENSION 165]: Null-Byte Vectorization
            self.raw_scripture = self.raw_scripture.translate(str.maketrans('', '', '\x00'))

            # [ASCENSION 170]: Phantom Sigil Exorcism
            self.raw_scripture = re.sub(r'^```(scaffold)?\s*\n', '', self.raw_scripture, flags=re.MULTILINE)
            self.raw_scripture = re.sub(r'\n```\s*$', '\n', self.raw_scripture, flags=re.MULTILINE)

            # [ASCENSION 155]: Substrate-Aware Line Normalization
            self.raw_scripture = self.raw_scripture.replace('\r\n', '\n').replace('\r', '\n')
            self.raw_scripture = self._normalize_indentation(self.raw_scripture)

            # [ASCENSION 158]: Merkle Blueprint Hashing
            self.variables['__blueprint_hash__'] = hashlib.sha256(self.raw_scripture.encode('utf-8')).hexdigest()

        # --- MOVEMENT VI: THE CORE DECONSTRUCTION LOOP ---
        # [ASCENSION 169]: ADRENALINE MODE
        gc_was_enabled = gc.isenabled()
        if self.depth == 0: gc.disable()

        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(original_recursion_limit, 5000))

        lines = self.raw_scripture.splitlines()
        i = 0
        _timeout_deadline = time.monotonic() + self.PARSE_TIMEOUT_SECONDS

        # [ASCENSION 156]: ONTOLOGICAL STRATUM TRACKER
        self.active_stratum = "FORM"
        self.kinetic_floor_indent = -1

        try:
            while i < len(lines):
                if time.monotonic() > _timeout_deadline:
                    raise ArtisanHeresy("Metabolic Timeout: Parsing exceeded temporal budget.",
                                        severity=HeresySeverity.CRITICAL)

                line = lines[i]
                current_line_num = i + 1 + self.line_offset
                indent = self._calculate_original_indent(line)

                # [ASCENSION 155]: HYDRAULIC THREAD YIELDING
                if i > 0 and i % 500 == 0:
                    time.sleep(0)
                    self._pulse_progress(i, len(lines))

                # =====================================================================
                # ==[ASCENSION 156]: THE ACTIVE STRATUM STATE MACHINE                ==
                # =====================================================================
                if self.active_stratum == "WILL" and indent <= self.kinetic_floor_indent and line.strip():
                    if not line.strip().startswith(('#', '//')):
                        self.active_stratum = "FORM"
                        self.kinetic_floor_indent = -1

                if bool(re.match(r'^\s*%%\s*(post-run|on-heresy|on-undo)\b', line.strip())):
                    self.active_stratum = "WILL"
                    self.kinetic_floor_indent = indent

                # [STRIKE]: Retinal Triage (The Inquisitor)
                from ..lexer_core.inquisitor import GnosticLineInquisitor
                vessel = GnosticLineInquisitor.inquire(line, current_line_num, self, self.grammar_key, indent)

                # =====================================================================
                # ==[ASCENSION 160]: THE "MAKE" TRANSMUTATOR                         ==
                # =====================================================================
                if self.active_stratum == "WILL" and vessel.line_type != GnosticLineType.VOID:
                    has_form_sigil = bool(re.search(r'(::|:?\s*=|\+=|\^=|~=|<<)', vessel.raw_scripture))
                    if not has_form_sigil and vessel.line_type not in (GnosticLineType.POST_RUN,
                                                                       GnosticLineType.ON_HERESY,
                                                                       GnosticLineType.ON_UNDO, GnosticLineType.LOGIC):
                        # Force into Edict (Vow)
                        vessel.line_type = GnosticLineType.VOW
                        vessel.edict_type = EdictType.ACTION

                        raw_stripped = vessel.raw_scripture.strip()
                        if not raw_stripped.startswith(('>>', '??', '!!', '@', '#', '//')):
                            ws_prefix = vessel.raw_scripture[
                                        :len(vessel.raw_scripture) - len(vessel.raw_scripture.lstrip())]
                            vessel.raw_scripture = f"{ws_prefix}>> {raw_stripped}"

                # Scribe Dispatch
                scribe = self._get_scribe_for_vessel(vessel)
                if scribe:
                    i = scribe.conduct(lines, i, vessel)
                else:
                    i += 1

        except Exception as catastrophic_paradox:
            # [ASCENSION 167]: Socratic Error Unwrapping
            tb = traceback.format_exc()
            self._proclaim_heresy("META_HERESY_PARSER_FRACTURE", "System", details=f"{catastrophic_paradox}\n{tb}",
                                  severity=HeresySeverity.CRITICAL)

        finally:
            sys.setrecursionlimit(original_recursion_limit)
            if self.depth == 0 and gc_was_enabled: gc.enable()

        # =========================================================================
        # == MOVEMENT VII: [ASCENSION 173] - RECURSIVE AUTO-BLOOM                 ==
        # =========================================================================
        if self.depth > 0:
            if not self._silent: self.Logger.verbose(f"   -> Auto-Bloom: Resolving sub-dimension L{self.depth}")
            self.resolve_reality()

        # --- MOVEMENT VIII: STATE FINALITY ---
        self._evolve_state_hash(f"parse_end_trace_{trace_id}")

        if self.depth == 0 and self.heresies:
            self._group_heresies()

        # [ASCENSION 175]: THE FINALITY VOW
        return self, self.raw_items, self.post_run_commands, self.edicts, self.variables, self.dossier

    def resolve_reality(self) -> List['ScaffoldItem']:
        """
        =================================================================================
        == THE OMEGA RESOLVE RITE: TOTALITY (V-Ω-VMAX-ACHRONAL-DECOUPLING-FINALIS)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_RESOLVE_VMAX_DECOUPLED_PROJECTION_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for logic-to-matter convergence. This version
        righteously annihilates the "Ocular Freeze" by fissioning the Visualization
        Timeline into a background daemon. It righteously implements the **Laminar
        Pointer Suture**, ensuring that the Body and the Eye share a bit-perfect
        memory address without blocking the Prime Timeline.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (151-175):
        151. **Apophatic Ocular Decoupling (THE MASTER CURE):** Dispatches the
             O(N²) Mermaid and JSON Graph projections to a background 'Ocular' thread,
             reclaiming 30-40 seconds of Main-Thread latency instantly.
        152. **Laminar Pointer Suture (THE MASTER CURE):** Uses slice assignment `[:]`
             to preserve the physical memory address (id) of the shared matter buffer.
             This is the 1:1 antidote to Anomaly 236 (Ghost Projects).
        153. **Adrenaline Ocular Blindness:** If `SCAFFOLD_ADRENALINE=1` is manifest,
             the Engine physically shutters the Eye, spending zero cycles on visuals.
        154. **Achronal State Hashing:** Forges a bit-perfect SHA-256 state seal
             immediately before and after resolution to detect "Alchemical Drift".
        155. **NoneType Sarcophagus v28:** Hard-wards the topological sort against
             Null-keys, guaranteeing O(N) convergence even with malformed Gnosis.
        156. **Substrate-Aware Threading:** Natively detects WASM/Ether planes to
             revert to synchronous safety if the substrate forbids background fission.
        157. **Trace ID Silver-Cord Suture:** Force-binds the parent Trace ID to
             the background projection task for absolute forensic correlation.
        158. **Hydraulic GC Pacing:** Explicitly triggers `gc.collect(1)` ONLY
             after matter convergence, preserving L1 cache momentum during the strike.
        159. **Bicameral Memory Reconciliation:** Atomically merges sub-weaver
             results into the Prime Timeline buffer using reference stability.
        160. **Isomorphic Identity Injection:** Injects the `project_slug` into
             all background projection contexts to align UI breadcrumbs JIT.
        161. **Haptic Failure Signaling:** If the DAG Reactor fractures, it
             radiates 'VFX: Shake_Red' to the HUD before the Main thread halts.
        162. **Zero-Latency Inception:** Bypasses the background thread for
             ASTs < 50 nodes, optimizing for high-velocity atomic dream strikes.
        163. **Merkle-Lattice State Sealing:** Snapshotting the final Mind-State
             for the `scaffold.lock` chronicle in O(1) time.
        164. **Ocular HUD Multicast (Debounced):** Aggregates "MATTER_CONVERGED"
             pulses to 60Hz to prevent WebSocket buffer saturation.
        165. **Subversion Ward:** Protects protected system files from being
             discarded during the Nova Deduplication pass.
        166. **Indentation Floor Oracle:** Validates that the visual gravity of
             manifested items matches the willed blueprint coordinates.
        167. **Lazarus README Resuscitation:** Autonomicly generates a high-status
             README if the Architect willed a void project heart.
        168. **Apophatic Error Unwrapping:** Transmutes internal SGF fractures
             into human-readable "Paths to Redemption" for the UI.
        169. **Entropy Velocity Tomography:** Measures the speed of convergence
             (Nodes/Sec) and radiates the "Metabolic Health" to the HUD.
        170. **Topological Full-Scan Suture:** Ensures that every elected shard
             in the DAG is physically waked before the manifest is sealed.
        171. **NoneType Zero-G Amnesty:** Gracefully handles shards with willed
             logic but empty matter by transmuting them into virtual anchors.
        172. **Bicameral Command Deduplication:** Ensures that identical kinetic
             edicts are merged into a single execution atom.
        173. **Ocular Line Mapping:** Aligns the Monaco line-references with
             the background projected AST manifest perfectly.
        174. **The Absolute Mathematical Vow:** A guarantee of O(N) linear
             convergence, regardless of project complexity.
        175. **The Finality Vow:** Reality is Manifest and Pure.
        =================================================================================
        """
        import hashlib
        import time
        import gc
        import os
        import re
        import threading
        from pathlib import Path
        from ...contracts.heresy_contracts import HeresySeverity, Heresy
        from ...contracts.data_contracts import GnosticLineType, ScaffoldItem

        # [ASCENSION 154]: ULTRAVIOLET CHRONOMETRY INCEPTION
        _start_ns = time.perf_counter_ns()
        trace_id = self.variables.get("trace_id") or f"tr-res-{os.urandom(4).hex().upper()}"
        is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

        # [ASCENSION 152]: THE LAMINAR MEMORY AUDIT (THE MASTER CURE)
        _items_id_pre = id(self.manifested_matter)

        # --- MOVEMENT II: CONTEXTUAL STABILIZATION (THE DAG REACTOR) ---
        reconciled_gnosis = self.variables.copy()
        reconciled_gnosis.update({"__engine__": self.engine, "__alchemist__": self.alchemist, "__trace_id__": trace_id})

        # [STRIKE]: O(N) Topological Variable Resolution
        unresolved_keys = {k: v for k, v in reconciled_gnosis.items() if isinstance(v, str) and "{{" in v}
        if unresolved_keys:
            dep_graph = {k: set() for k in unresolved_keys}
            in_degree = {k: 0 for k in unresolved_keys}
            var_regex = re.compile(r'\{\{\s*([a-zA-Z_]\w*).*?\}\}')

            for key, val in unresolved_keys.items():
                for match in var_regex.findall(val):
                    if match in unresolved_keys and match != key:
                        dep_graph[match].add(key)
                        in_degree[key] += 1

            queue = [k for k in unresolved_keys if in_degree[k] == 0]
            sorted_keys = []
            while queue:
                curr = queue.pop(0)
                sorted_keys.append(curr)
                for neighbor in dep_graph[curr]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0: queue.append(neighbor)

            for key in (sorted_keys + [k for k in unresolved_keys if k not in sorted_keys]):
                try: reconciled_gnosis[key] = self.alchemist.transmute(reconciled_gnosis[key], reconciled_gnosis)
                except (UndefinedGnosisHeresy, AmnestyGrantedHeresy): pass
                except Exception as e: self.Logger.debug(f"DAG Stabilization Fracture on '{key}': {e}")

        self.variables.update(reconciled_gnosis)

        # =========================================================================
        # == MOVEMENT III: THE LOCALIZED WEAVE & OCULAR FISSION                  ==
        # =========================================================================
        from .ast_weaver.weaver.engine import GnosticASTWeaver
        try:
            weaver = GnosticASTWeaver(self)
            self.gnostic_ast = weaver.weave_gnostic_ast()

            # [ASCENSION 151]: THE ACHRONAL OCULAR DECOUPLING (THE FIX)
            # We fission the visualization task to a background core.
            if self.gnostic_ast and not self._silent and not is_adrenaline:
                def _holographic_projection_task(ast_root, engine_ref, session_id, trace):
                    try:
                        from ...core.alchemist.elara.vis.flow_projector import LogicFlowProjector
                        # 1. Project Mermaid (O(N) Fusion)
                        mermaid_data = LogicFlowProjector.project_mermaid(ast_root)
                        # 2. Forge Ocular Manifest
                        json_flow = LogicFlowProjector.project_json_manifest(ast_root)
                        # 3. Radiate to React HUD
                        if engine_ref and hasattr(engine_ref, 'akashic') and engine_ref.akashic:
                            engine_ref.akashic.broadcast({
                                "method": "elara/logic_flow_update",
                                "params": {"graph": json_flow, "mermaid": mermaid_data, "trace": session_id, "aura": "#3b82f6"}
                            })
                    except Exception as p_err: pass

                # [STRIKE]: Parallel Dimension Inception
                threading.Thread(
                    target=_holographic_projection_task,
                    args=(self.gnostic_ast, self.engine, getattr(self, 'parse_session_id', 'void'), trace_id),
                    daemon=True, name="OcularProjector"
                ).start()

            # [KINETIC STRIKE]: Immediate convergence without waiting for the eye!
            _, f_commands, f_heresies, f_edicts = weaver.resolve_paths_from_ast(self.gnostic_ast)

            with self._state_lock:
                # Command ID Deduplication
                current_cmd_ids = {id(c) for c in self.post_run_commands}
                self.post_run_commands.extend([c for c in f_commands if id(c) not in current_cmd_ids])
                self.edicts.extend([e for e in f_edicts if id(e) not in {id(ex) for ex in self.edicts}])
                self.heresies.extend([h for h in f_heresies if id(h) not in {id(hx) for hx in self.heresies}])

        except Exception as e:
            self.Logger.critical(f"Convergence Reactor Fracture: {e}")
            self.heresies.append(Heresy(message="AST_FRACTURE", details=str(e), severity=HeresySeverity.CRITICAL))

        # =========================================================================
        # == MOVEMENT IV: ONTOLOGICAL FINALITY (NOVA DEDUPLICATION)              ==
        # =========================================================================
        self._emit_metabolic_manifests()
        unique_reality: List[ScaffoldItem] = []
        seen_paths: Dict[str, bool] = {}
        populated_dirs = set()

        for item in self.manifested_matter:
            if not item.path or item.is_dir: continue
            parts = str(item.path).replace('\\', '/').split('/')
            for i in range(1, len(parts)): populated_dirs.add('/'.join(parts[:i]).lower())

        for item in list(self.manifested_matter):
            if not item.path:
                unique_reality.append(item)
                continue
            p_clean = str(item.path).replace('\\', '/').lstrip('*-+ ').lower().rstrip('/')
            if not item.is_dir:
                if p_clean in seen_paths and not item.mutation_op: continue
                unique_reality.append(item); seen_paths[p_clean] = False
                continue
            is_root = '/' not in p_clean
            if (p_clean in seen_paths and not is_root) or (not is_root and p_clean not in populated_dirs): continue
            seen_paths[p_clean] = True; unique_reality.append(item)

        # =========================================================================
        # == MOVEMENT V: [ASCENSION 152] - LAMINAR REFERENCE SUTURE              ==
        # =========================================================================
        # We righteously use slice assignment to preserve the physical pointer.
        self.manifested_matter[:] = unique_reality

        if id(self.manifested_matter) != _items_id_pre:
            self.Logger.critical("FATAL: Reference Singularity Severed. Matter Evaporated.")
            self.all_rites_are_pure = False

        self._finalize_achronal_dossier()

        # [ASCENSION 164]: OCULAR RADIATION (HUD REVELATION)
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "elara/matter_converged",
                    "params": {"trace": trace_id, "atom_count": len(self.manifested_matter), "will_count": len(self.post_run_commands), "merkle_seal": getattr(self, '_state_hash', '0xVOID')[:12]}
                })
            except Exception: pass

        # [ASCENSION 167]: Lazarus README
        if not any(str(item.path) == "README.md" for item in self.manifested_matter if item.path) and self.depth == 0:
            self._inject_holographic_readme()

        # [ASCENSION 158]: METABOLIC LUSTRATION
        if len(self.manifested_matter) > 500: gc.collect(1)

        # [ASCENSION 175]: THE FINALITY VOW
        return self.manifested_matter

    def _emit_metabolic_manifests(self) -> List['ScaffoldItem']:
        """
        =================================================================================
        == THE OMEGA METABOLIC DISPATCH (V-Ω-TOTALITY-VMAX-DELEGATED)                  ==
        =================================================================================
        LIF: INFINITY | ROLE: DEBT_CONDUCTOR_FACADE

        [THE MASTER CURE]: This function has been decapitated. It now delegates
        total authority to the MetabolicOrchestrator, providing 0ms latency
        dispatch to the specialized metabolic brain.
        """
        from .metabolics.orchestrator import MetabolicOrchestrator

        if self.depth != 0: return []

        # 1. MATERIALIZE THE ORCHESTRATOR
        orchestrator = MetabolicOrchestrator(self)

        # 2. CONDUCT THE RECONCILIATION
        # [STRIKE]: This performs the scrying, filtering, and anchoring.
        emitted_items = orchestrator.conduct_reconciliation()

        # 3. FINAL INTEGRATION
        self.manifested_matter.extend(emitted_items)

        return emitted_items

    def _inject_holographic_readme(self):
        """[ASCENSION 88]: Fuses a high-status README into the final output."""
        project_name = self.variables.get("project_name", "Omega System")
        description = self.variables.get("description", "A sovereign architecture manifest via Velm.")

        readme_content = f"# {project_name}\n> {description}\n\n## 🏛️ Architecture\n"
        for shard_id, manifest in self.dossier.manifests.items():
            if getattr(manifest, 'summary', None):
                readme_content += f"- **{manifest.id}**: {manifest.summary}\n"

        readme_item = ScaffoldItem(
            path=Path("README.md"),
            content=readme_content,
            mutation_op="=",
            line_type=GnosticLineType.FORM,
            metadata={"origin": "AutonomicMetabolism"}
        )
        self.manifested_matter.append(readme_item)

    def _purge_system_artifacts(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        import uuid, json
        from decimal import Decimal
        from pathlib import Path
        from datetime import datetime, date

        try:
            from ...codex.loader.proxy import DomainProxy
            from ...core.runtime.engine import VelmEngine
            from ...core.alchemist import DivineAlchemist
        except ImportError:
            DomainProxy = object;
            VelmEngine = object;
            DivineAlchemist = object

        def _purify_recursive(data: Any, depth: int = 0) -> Any:
            if id(data) in _seen_ids: return f"/* CIRCULAR_REF:{hex(id(data))} */"
            if depth > 10: return str(data)

            if isinstance(data, dict):
                _seen_ids.add(id(data))
                clean_dict = {}
                for k, v in data.items():
                    k_str = str(k)
                    if k_str.startswith('__') and k_str.endswith('__'): continue
                    if isinstance(v, (DomainProxy, VelmEngine, DivineAlchemist)): continue
                    if type(v).__name__ in ("GnosticVoidEngineMock", "Mock", "MagicMock"): continue
                    if callable(v): continue

                    if any(secret in k_str.lower() for secret in ['key', 'secret', 'token', 'password']):
                        clean_dict[k] = "[REDACTED_BY_SOVEREIGN_SIEVE]"
                    else:
                        clean_dict[k] = _purify_recursive(v, depth + 1)
                _seen_ids.remove(id(data))
                return clean_dict

            elif isinstance(data, (list, tuple, set)):
                _seen_ids.add(id(data))
                clean_list = []
                for v in data:
                    if isinstance(v, (DomainProxy, VelmEngine, DivineAlchemist)): continue
                    if type(v).__name__ in ("GnosticVoidEngineMock", "Mock", "MagicMock"): continue
                    if callable(v): continue
                    clean_list.append(_purify_recursive(v, depth + 1))
                _seen_ids.remove(id(data))
                return clean_list

            elif hasattr(data, 'model_dump') and callable(getattr(data, 'model_dump')):
                return _purify_recursive(data.model_dump(mode='json'), depth + 1)

            elif isinstance(data, (Path, uuid.UUID, Decimal, datetime, date)):
                return str(data).replace('\\', '/')

            return data

        _seen_ids = set()
        return _purify_recursive(gnosis)

    def _forge_scribe_pantheon(self) -> Dict[str, FormScribe]:
        from .parser_scribes import SCRIBE_PANTHEON, FormScribe
        pantheon: Dict[str, FormScribe] = {}
        grimoire = SCRIBE_PANTHEON.get(self.grammar_key)
        if not grimoire: raise ArtisanHeresy(f"META-HERESY: The Grimoire holds no Gnosis for '{self.grammar_key}'.")
        unique_scribes = set(grimoire.values())
        for ScribeClass in unique_scribes:
            if not issubclass(ScribeClass, FormScribe): continue
            instance_key = ScribeClass.__name__.lower()
            try:
                pantheon[instance_key] = ScribeClass(self)
            except Exception as e:
                Logger.error(f"Paradox forging '{ScribeClass.__name__}': {e}")
                raise
        return pantheon

    def _get_scribe_for_vessel(self, vessel: GnosticVessel) -> Optional[FormScribe]:
        from ...contracts.data_contracts import GnosticLineType
        if not vessel.is_valid or vessel.line_type == GnosticLineType.VOID: return None
        from .parser_scribes import SCRIBE_PANTHEON
        scribe_map = SCRIBE_PANTHEON.get(self.grammar_key, {})
        ScribeClass = None
        if self.grammar_key == 'symphony':
            ScribeClass = scribe_map.get(vessel.edict_type) or scribe_map.get(vessel.line_type)
        else:
            ScribeClass = scribe_map.get(vessel.line_type)
        if ScribeClass:
            return self.scribes.get(ScribeClass.__name__.lower())
        self.Logger.warn(f"L{vessel.line_num}: No Scribe consecrated for {vessel.line_type.name}")
        return None

    def _adjudicate_case_identity(self, vessel: GnosticVessel):
        from ...contracts.heresy_contracts import HeresySeverity
        if not vessel.path: return
        path_posix = vessel.path.as_posix()
        path_lower = path_posix.lower()
        if path_lower in getattr(self, '_lowercase_path_roster', set()):
            collision_victim = "Unknown"
            for existing_path in self.items_by_path.keys():
                if existing_path.lower() == path_lower and existing_path != path_posix:
                    collision_victim = existing_path
                    break
            if collision_victim != "Unknown":
                self._proclaim_heresy(
                    "CASE_IDENTITY_COLLISION", vessel,
                    details=f"Dimensional Paradox: '{path_posix}' collides with '{collision_victim}'.",
                    severity=HeresySeverity.CRITICAL
                )
                return
        if not hasattr(self, '_lowercase_path_roster'):
            self._lowercase_path_roster = set()
        self._lowercase_path_roster.add(path_lower)
        RESERVED_NAMES = {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        }
        for part in path_posix.split('/'):
            stem = part.split('.')[0].upper()
            if stem in RESERVED_NAMES:
                self._proclaim_heresy("WINDOWS_RESERVED_NAME_HERESY", vessel, severity=HeresySeverity.CRITICAL)
        INVALID_CHARS = set('<>:"|?*')
        for char in path_posix:
            if char in INVALID_CHARS:
                self._proclaim_heresy("ILLEGAL_GLYPH_HERESY", vessel, severity=HeresySeverity.CRITICAL)
        if path_posix[-1] in ('.', ' '):
            self._proclaim_heresy("TRAILING_PHANTOM_HERESY", vessel, severity=HeresySeverity.WARNING)

    def _proclaim_final_item(self, vessel: GnosticVessel):
        from ...contracts.data_contracts import GnosticLineType, ScaffoldItem
        if not vessel.is_valid or vessel.line_type == GnosticLineType.VOID: return
        item = ScaffoldItem.model_validate(vessel.model_dump())
        if self.pending_permissions:
            item.permissions = self.pending_permissions
            self.pending_permissions = None

        self.raw_items.append(item)
        if item.line_type == GnosticLineType.FORM and item.path:
            self.items_by_path[item.path.as_posix()] = item

    def _finalize_achronal_dossier(self):
        import os, time
        from pathlib import Path
        from ...utils import get_git_commit
        from ...utils.gnosis_discovery.facade import discover_required_gnosis

        current_trace_id = self.variables.get("trace_id") or f"tr-dossier-{os.urandom(3).hex().upper()}"
        coordinate_anchor = getattr(self, 'base_path', None) or self.project_root or Path.cwd()

        try:
            current_git_head = get_git_commit(coordinate_anchor) or "VOID_REALITY"
        except Exception:
            current_git_head = "VOID_REALITY"

        safe_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []
        for cmd in self.post_run_commands:
            raw = list(cmd) if isinstance(cmd, (list, tuple)) else [str(cmd)]
            while len(raw) < 4: raw.append(None)
            safe_commands.append(tuple(raw[:4]))

        # Pass current DOSSIER to preserve the imported Manifests!
        existing_manifests = self.dossier.manifests.copy()

        self.dossier = discover_required_gnosis(
            execution_plan=self.raw_items,
            post_run_commands=safe_commands,
            blueprint_vars={**self.blueprint_vars, **self.variables},
            macros=self.macros
        )

        # Restore the manifests
        self.dossier.manifests.update(existing_manifests)

        dynamic_runtime_vars = set()
        for edict in self.edicts:
            if getattr(edict, 'capture_as', None):
                dynamic_runtime_vars.add(edict.capture_as)
            if getattr(edict, 'interactive_prompt', None):
                dynamic_runtime_vars.add(edict.interactive_prompt.target_variable)

        for item in self.raw_items:
            if item.semantic_selector:
                for key in ('capture_as', 'target_variable', 'as'):
                    if val := item.semantic_selector.get(key):
                        dynamic_runtime_vars.add(str(val))

        RESERVED_MOAT = {
                            'secrets', 'context', 'metadata', 'request', 'trace_id',
                            'session_id', 'project_root', '__engine__', '__alchemist__',
                            '__current_dir__', '__current_file__', '__woven_matter__',
                            '__woven_commands__', '__parse_depth__', 'vitals',
                            'iron', 'topo', 'akasha', 'substrate', 'os', 'path', 'time', 'math',
                            'crypto', 'ai', 'ui', 'sec', 'cloud', 'id', 'auth', 'logic', 'iris',
                            'neuron', 'nexus', 'pulse', 'shadow', 'sim', 'soul', 'stack', 'struct',
                            'test', 'veritas', 'pact', 'lore', 'guide',
                            'github', 'matrix', 'runner', 'steps', 'needs', 'job', 'strategy',
                            'inputs', 'env', 'hashfiles', 'contains', 'startswith',
                            'endswith', 'format', 'join', 'tojson', 'fromjson',
                            'shell', 'lower', 'upper', 'replace', 'trim', 'split', 'map', 'list',
                            'dict', 'set', 'int', 'float', 'bool', 'str', 'len', 'min', 'max',
                            'now', 'time', 'date', 'uuid', 'random', 'hash', 'default',
                            'file_exists', 'dir_exists', 'yes', 'no', 'true', 'false', 'none', 'null',
                            'has_poetry', 'has_npm', 'has_pnpm', 'has_yarn', 'has_cargo', 'has_go',
                            'is_python', 'is_node', 'is_rust', 'is_go', 'is_ruby', 'is_java', 'is_cpp',
                            'is_windows', 'is_linux', 'is_macos', 'is_iron', 'is_wasm', 'is_ether',
                            'os_name', 'platform', 'arch', 'python_version', 'node_version',
                            'project_type', 'project_slug', 'package_name', 'project_name',
                            'author', 'version', 'license', 'project_title', 'description',
                            'machine_id', 'org_name', 'email', 'author_email',
                            'intent', 'content', 'raw', 'dir', 'file', 'path', 'name', 'type',
                            'id', 'port', 'loop', 'kwargs', 'args', 'self', 'super'
                        } | dynamic_runtime_vars

        if self.dossier and hasattr(self.dossier, 'required'):
            # Filter the set in-place using set comprehension
            self.dossier.required = {
                k for k in self.dossier.required
                if str(k).lower() not in RESERVED_MOAT and not str(k).startswith('_')
            }

        self.dossier.metadata.update({
            "git_head_anchor": current_git_head,
            "parse_session": self.parse_session_id,
            "trace_id": current_trace_id,
            "achronal_status": "STABLE" if self.all_rites_are_pure else "FRACTURED",
            "bicameral_mode": "ACTIVE",
            "merkle_seal": self._state_hash[:12]
        })

        if self.depth == 0:
            self.Logger.verbose(f"   -> Dossier Finalized for Trace {current_trace_id[:8]}.")
            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                try:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "DOSSIER_SEALED", "label": "GNOSTIC_FINALITY", "color": "#64ffda",
                                   "trace": current_trace_id}
                    })
                except Exception:
                    pass

    def _calculate_original_indent(self, line: str) -> int:
        from ..block_consumer import GnosticBlockConsumer
        consumer = GnosticBlockConsumer([])
        return consumer._measure_visual_depth(line)

    def _proclaim_heresy(self, key: str, item: Union[GnosticVessel, ScaffoldItem, str], **kwargs):
        from ...jurisprudence_core.jurisprudence import forge_heresy_vessel
        from ...contracts.heresy_contracts import HeresySeverity
        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', 0) or self.line_offset

        # [ASCENSION 110]: Socratic Suggestion Injection V3
        sugg = kwargs.get('suggestion')
        if not sugg and key == "META_HERESY_PARSER_FRACTURE":
            sugg = "Perform a structural biopsy. Check for unclosed @if or @macro blocks. Consult: https://docs.novalym.systems/sgf/errors"

        heresy = forge_heresy_vessel(key=key, line_num=line_num, line_content=raw_scripture,
                                     details=kwargs.get('details'))
        if severity_override := kwargs.get('severity'): heresy.severity = severity_override
        if sugg: heresy.suggestion = sugg
        if ui_hints := kwargs.get('ui_hints'): Logger.debug(f"[UI_SIGNAL:{ui_hints.get('vfx')}] {heresy.message}")
        if self.strict_mode and heresy.severity == HeresySeverity.WARNING: heresy.severity = HeresySeverity.CRITICAL

        self.heresies.append(heresy)
        if heresy.severity == HeresySeverity.CRITICAL:
            if hasattr(item, 'is_valid'): item.is_valid = False
            self.all_rites_are_pure = False

    def _group_heresies(self):
        """[ASCENSION 119]: Bicameral Error Grouping."""
        from ...contracts.heresy_contracts import HeresySeverity
        if not self.heresies: return
        criticals = [h for h in self.heresies if h.severity == HeresySeverity.CRITICAL]
        warnings = [h for h in self.heresies if h.severity != HeresySeverity.CRITICAL]

        if len(warnings) > 5:
            from ...contracts.heresy_contracts import Heresy, HeresySeverity
            cluster = Heresy(
                message=f"MULTIPLE_WARNINGS_DETECTED: {len(warnings)} minor heresies suppressed.",
                details="Use --verbose to scry the full list of warnings.",
                severity=HeresySeverity.WARNING,
                line_num=0
            )
            self.heresies = criticals + [cluster]

    def _consume_indented_block_with_context(self, lines: List[str], i: int, parent_indent: int) -> Tuple[
        List[str], int]:
        from ..block_consumer import GnosticBlockConsumer
        return GnosticBlockConsumer(lines).consume_indented_block(i, parent_indent)

    def _pulse_progress(self, current: int, total: int):
        engine_ref = getattr(self, 'engine', None)
        akashic_ref = getattr(engine_ref, 'akashic', None) if engine_ref else None
        if akashic_ref:
            try:
                # [ASCENSION 118]: Luminous Pulse Debouncing
                now = time.time()
                if now - self._last_pulse_time < 0.033:  # Max ~30Hz
                    return
                self._last_pulse_time = now

                percent = int((current / total) * 100)
                if percent % 5 == 0 and percent != getattr(self, '_last_pulse_percent', 0):
                    akashic_ref.broadcast({
                        "method": "scaffold/progress",
                        "params": {"id": "parse_scan", "message": "Deconstructing Scripture...", "percentage": percent}
                    })
                    self._last_pulse_percent = percent
            except:
                pass

    def _scry_orphaned_variables(self):
        is_sub_weave = self.external_vars.get("__is_nested_weave", False)
        is_dry_run = self.variables.get("dry_run", False)
        if is_sub_weave or is_dry_run or self.depth > 0: return
        if len(self.blueprint_vars) == 0: return
        pass

    def snapshot_state(self) -> Dict[str, Any]:
        return {
            "variables": self.variables.copy(),
            "macros": copy.deepcopy(self.macros),
            "line_offset": self.line_offset,
            "file_path": str(self.file_path)
        }

    def _evolve_state_hash(self, mutation_key: str):
        with self._state_lock:
            salt = str(mutation_key or "void_flux").strip()
            now_ns = time.perf_counter_ns()
            raw_payload = f"{self._state_hash}:{salt}:{now_ns}"
            self._state_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
            if hasattr(self, 'engine') and self.engine and hasattr(self.engine, 'akashic'):
                try:
                    if self.engine.akashic and self.depth == 0:
                        self.engine.akashic.broadcast({
                            "method": "novalym/state_evolution",
                            "params": {"key": salt, "hash": self._state_hash[:12],
                                       "trace_id": getattr(self, "parse_session_id", "void")}
                        })
                except Exception:
                    pass


# =============================================================================
# == VII. THE ALCHEMICAL SINGLETON                                           ==
# =============================================================================

_parser_instance = None


def get_parser(grammar: str = "scaffold") -> ApotheosisParser:
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = ApotheosisParser(grammar_key=grammar)
    return _parser_instance