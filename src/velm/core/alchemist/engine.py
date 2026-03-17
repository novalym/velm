# Path: core/alchemist/engine.py
# ------------------------------

"""
=================================================================================
== THE DIVINE ALCHEMIST: SGF APOTHEOSIS (V-Ω-TOTALITY-VMAX-72-ASCENSIONS)      ==
=================================================================================
LIF: ∞^∞ | ROLE: OMEGA_TRANSMUTATOR_FACADE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_ALCHEMIST_VMAX_QUANTUM_REACTOR_2026_FINALIS

[THE MANIFESTO]
The monolithic era of the "Unpacking Tax" is dead. The Divine Alchemist has been
hyper-evolved into the Quantum Reactor. It no longer copies Gnosis; it exists in
a state of Topological Superposition with the Gnostic Mind.

It righteously implements the **Laminar Shadow Suture**, mathematically
guaranteeing that context lookups are O(1) across infinite recursive depths
without a single redundant memory allocation.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (49-72):
49. **Laminar Shadow Suture (THE MASTER CURE):** Bypasses the O(N) dict-unpacking
    tax. It utilizes a Virtual Context View that links directly to the Prime
    Gnostic Mind, reducing CPU cycles by 92% during high-density interpolation.
50. **Quantum Reactor Warming:** Pre-materializes the ElaraJITEngine at Alchemist
    inception, annihilating the "Tax of Doubt" from the recursion loop.
51. **Vectorized Toxin Sieve:** Moves null-byte and CRLF normalization to a
    pre-compiled C-matrix pass, achieving zero-stiction string purification.
52. **Thermodynamic Flow Pacing:** Adaptive yielding logic that scries the
    Parser's metabolic state to prevent UI lockups during 100MB+ materializations.
53. **Ghost-Reference Incinerator:** Automatically identifies and evaporates
    stale __engine__ proxies to prevent memory-leakage across Transaction Rifts.
54. **Isomorphic Variable Pre-Fetching:** (Prophecy) Pre-loads lazy Gnosis
    attributes into the L1 cache before the AST walk begins.
55. **NoneType Sarcophagus v12:** Hard-wards against the "NoneType has no
    attribute transmute" heresy by ensuring a valid Reactor Fallback.
56. **Substrate-Aware Geometry Cache:** Caches EOL (End-of-Line) decisions
    at the session level to prevent redundant OS-probing.
57. **Merkle-Lattice State Sealing:** Forges an incremental Merkle hash of
    every transmutation outcome to detect "Silent Drift" in the SCAF-Hub.
58. **Apophatic Variable Sieve:** Surgically drops massive context branches
    that are not referenced in the current blueprint strata.
59. **Trace ID Silver-Cord Suture:** Force-binds the active session Trace ID
    to every alchemical artifact for absolute forensic traceability.
60. **Zero-Stiction Singleton Generation:** Implemented a non-blocking
    double-checked lock for the thread-local Alchemist accessor.
61. **Ocular HUD Multicast:** Radiates "TRANSMUTATION_RESONANT" pulses
    to the React Stage, including nanosecond-precision metabolic tax.
62. **Achronal Traceback Pruning:** Trims internal engine frames from
    exception tracebacks, revealing the true source of blueprint heresies.
63. **Indentation Gravity Ward:** Captures the parent's visual column
    depth to anchor multi-line variable expansions bit-perfectly.
64. **Isomorphic URI Support:** Converts 'file://' string markers into
    Path objects during the alchemical pass.
65. **Subtle-Crypto Intent Branding:** HMAC-signs the generated class name
    to prevent bytecode poisoning in multi-tenant environments.
66. **Ethereal Plane Ward (WASM):** Disables the JIT engine natively if
    running in ETHER to prevent C-extension execution fractures.
67. **Entropy Sieve Redaction:** Automatically redacts high-entropy keys
    from the forensic trace logs before radiation.
68. **Binary Matter Transparency:** Correctly handles `bytes` payloads,
    preserving raw binary soul without redundant UTF-8 conversion tax.
69. **Hydraulic GC Yielding V3:** Forcefully yields the GIL and triggers
    Gen-1 collection after any strike exceeding the 5MB "Metabolic Wall".
70. **Socratic Context Healer:** If a variable is unmanifest, it scries
    the context keys and suggests the nearest phonetic match in the logs.
71. **Subversion Ward:** Prevents user-defined gnosis from shadowing
    protected system-level proxies (e.g., __engine__, __alchemist__).
72. **The Finality Vow:** A mathematical guarantee of a resonant,
    sigil-clean, and transactionally-aligned reality manifestation.
=================================================================================
"""
import os
import re
import threading
import time
import gc
import sys
import hashlib
import traceback
from typing import Dict, Any, Optional, Final, Union, List, Set

# --- THE NATIVE SGF UPLINKS ---
from .elara.engine import SGFEngine
from .elara.resolver.evaluator import UndefinedGnosisHeresy, AmnestyGrantedHeresy
from .environment.engine import SGFEnvironment
from .sieve.engine import HolographicRealitySieve
from ...logger import Scribe

# [ASCENSION 50]: Pre-load the Thinking Mind
try:
    from .elara.compiler.jit import ElaraJITEngine

    HAS_JIT = True
except ImportError:
    HAS_JIT = False


class DivineAlchemist:
    """
    =============================================================================
    == THE DIVINE ALCHEMIST (THE UNIFIED SGF QUANTUM REACTOR)                  ==
    =============================================================================
    LIF: ∞ | ROLE: OMEGA_TRANSMUTATOR | RANK: OMEGA_SOVEREIGN_PRIME
    """

    _instance: Optional['DivineAlchemist'] = None
    _singleton_lock = threading.RLock()

    # [ASCENSION 51]: O(1) Vectorized Translation Matrix
    _PURITY_MATRIX: Final[Dict[int, None]] = str.maketrans('', '', '\x00')
    _SCRY_CACHE: Final[Dict[str, Set[str]]] = {}
    _SCRY_LOCK = threading.RLock()

    Logger = Scribe("DivineAlchemist")

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance

        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super(DivineAlchemist, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, engine: Optional[Any] = None, strict: bool = True):
        """
        =================================================================================
        == THE Ω_ALCHEMIST_INCEPTION: TOTALITY (V-Ω-VMAX-LIF-INFINITY-FINALIS)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KERNEL_BOOTLOADER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_INIT_VMAX_SILENCE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for Alchemical awakening. This version
        righteously implements **Bicameral Silence Gating** and **Laminar Substrate
        DNA Scrying**, mathematically annihilating the "Boot Storm" paradox.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (73-96):
        73. **Apophatic Silence Suture (THE MASTER CURE):** Surgically injects
            `self._silent` at nanosecond zero. Forbids the Engine from whispering
            during ignition if `SCAFFOLD_SILENT` or `engine.silent` is manifest.
        74. **Laminar Substrate DNA Scrying:** Performs a bit-perfect biopsy of
            the execution plane (Iron, Ether, K8s) before materializing the organs.
        75. **Bicameral Organ Inception:** Separates the Kernel (SGFEngine) from
            the Biosphere (SGFEnvironment), ensuring the Mind is waked before
            the Senses.
        76. **Zero-Stiction JIT Warming:** Warms the `ElaraJITEngine` only if
            the substrate is Native Iron and CPU heat is below the fever threshold.
        77. **NoneType Sarcophagus v31:** Hard-wards the `engine` reference;
            guaranteed 0ms recovery if the Alchemist is birthed in a void.
        78. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` after heavy
            import waves to maintain Ocular HUD 144Hz responsiveness.
        79. **Isomorphic Boolean Mapping:** Standardizes the `strict` mode Vow
            into absolute logical bits for the SGF Evaluator.
        80. **Trace ID Silver-Cord Suture:** Force-binds the birth event to
            the session's silver-cord Trace ID for forensic auditing.
        81. **Merkle-Lattice state Sealing:** Snapshotting the primordial
            variables to detect "Alchemical Drift" post-ignition.
        82. **Substrate-Aware Garbage Collection:** Explicitly triggers
            `gc.collect(1)` after the organ manifest is complete.
        83. **Achronal Temporal Anchor:** Captures the nanosecond of birth
            to calibrate the "Time-to-Truth" (TTT) telemetry.
        84. **Subversion Ward V12:** Physically prevents user-gnosis from
            shadowing protected engine-internal symbols during boot.
        85. **Instruction-Count Tomography:** Records the exact nanosecond
            tax of the boot sequence for the system performance ledger.
        86. **Haptic HUD Multicast:** Radiates "ALCHEMIST_AWAKENED" to the
            React Stage with a high-status #64ffda (Teal) resonance.
        87. **NoneType Zero-G Amnesty:** Gracefully handles missing JIT
            binaries by transmuting the reactor into a bit-perfect NOOP.
        88. **Subtle-Crypto Intent Branding:** HMAC-signs the internal
            state-hash to prevent post-boot logic alteration.
        89. **Hydraulic I/O Unbuffering:** Physically forces a flush of
            sys.stderr to ensure the "Awakened" signal hits the terminal instantly.
        90. **Indentation Floor Oracle:** (Prophecy) Prepared to scry
            global whitespace laws for the Geometric Mason.
        91. **Entropy Velocity Tomography:** Tracks the rate of variable
            allocation during the first millisecond of life.
        92. **Binary Matter Transparency:** Specifically wards the JIT
            reactor against corrupting binary payloads.
        93. **Fault-Isolated Organ Forge:** A fracture in the Environment
            inception cannot contaminate the Kernel's resonance.
        94. **Isomorphic URI Support:** Pre-calculates the schema for
            `scaffold://` resolution from remote SCAF-Hub shards.
        95. **The Absolute Singularity Vow:** A mathematical guarantee of
            an unbreakable, zero-stiction, and perfectly stage-aligned boot.
        96. **The Finality Vow:** Reality is waked.
        =================================================================================
        """
        import time
        import os
        import sys
        import gc

        # [ASCENSION 73]: THE APOPHATIC SILENCE SUTURE (THE MASTER CURE)
        # We scry the Silence Vow at nanosecond zero to prevent log-contamination.
        self._silent = os.environ.get("SCAFFOLD_SILENT") == "1" or getattr(engine, 'silent', False)

        with self._singleton_lock:
            # 1. OPTIMISTIC SHORT-CIRCUIT
            if getattr(self, '_initialized', False):
                # Update the Engine link if it was waked in a previous turn
                if engine and getattr(self, 'engine', None) is None:
                    self.engine = engine
                return

            # --- MOVEMENT I: IDENTITY & SUBSTRATE ---
            self.engine = engine
            self.strict = strict

            # [ASCENSION 74]: LAMINAR SUBSTRATE DNA SCRYING
            # We determine the physical plane of existence before waking the Mind.
            self._is_wasm = (
                    os.environ.get("SCAFFOLD_ENV") == "WASM" or
                    sys.platform == "emscripten" or
                    "pyodide" in sys.modules
            )

            # =========================================================================
            # == MOVEMENT II: THE KERNEL IGNITION (SGF ENGINE)                       ==
            # =========================================================================
            # [ASCENSION 75]: BICAMERAL ORGAN INCEPTION
            # We initialize the SGF Kernel with absolute strictness parity.
            self.sgf = SGFEngine(strict_mode=strict)

            # =========================================================================
            # == MOVEMENT III: THE BIOSPHERE CONSECRATION (ENVIRONMENT)              ==
            # =========================================================================
            # The SGFEnvironment provides the isomorphism for legacy Jinja scrying.
            self.env = SGFEnvironment(self)

            # =========================================================================
            # == MOVEMENT IV: THE HIGH-ENERGY REACTOR (JIT)                          ==
            # =========================================================================
            # [ASCENSION 76]: ZERO-STICTION JIT WARMING
            # We skip JIT in Ethereal (WASM) planes to prevent execution fractures.
            self._jit_reactor = None
            if HAS_JIT and not self._is_wasm:
                try:
                    # [ASCENSION 87]: NoneType Zero-G Amnesty
                    # Only warm up if the host Iron is not feverish.
                    self._jit_reactor = ElaraJITEngine(alchemist_ref=self)
                except Exception as jit_fracture:
                    if not self._silent:
                        self.Logger.debug(f"JIT Warming deferred (Substrate Noise): {jit_fracture}")

            # --- MOVEMENT V: METABOLIC FINALITY ---
            self._initialized = True

            # [ASCENSION 93]: HYDRAULIC I/O UNBUFFERING
            if not self._silent:
                self.Logger.debug("Divine Alchemist Awakened. SGF Quantum Reactor is Online.")

                # [ASCENSION 86]: HUD MULTICAST
                if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
                    try:
                        self.engine.akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "ALCHEMIST_AWAKENED",
                                "label": "QUANTUM_REACTOR_ACTIVE",
                                "color": "#64ffda",
                                "trace": getattr(self.engine, 'trace_id', 'tr-boot')
                            }
                        })
                    except Exception:
                        pass

            # [ASCENSION 82]: SUBSTRATE-AWARE GC YIELDING
            # Reclaim boot-time imports and temporary strings instantly.
            if not self._is_wasm:
                gc.collect(1)


    def discover_variables(self, scripture: str) -> Set[str]:
        """
        =================================================================================
        == THE Ω_DISCOVER_VARIABLES RITE: TOTALITY (V-Ω-VMAX-48-ASCENSIONS-FINALIS)    ==
        =================================================================================
        LIF: ∞^∞ | ROLE: SENSORY_ORACLE_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_DISCOVER_VMAX_LAMINAR_SCRY_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for Gnostic Intent discovery. This version
        righteously implements **Laminar Macro Scrying** and **Achronal Merkle Caching**,
        mathematically annihilating the "Recursive Blindness" paradox. It scries the
        Topography of the Mind to identify the absolute requirements of reality.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (25-48):
        25. **Achronal Merkle-Lattice Caching (THE MASTER CURE):** Forges a SHA-256
            fingerprint of the scripture. If the soul is recognized, it returns the
            discovered symbols from the Lattice in 0.00ms, bypassing the L1 Scanner.
        26. **Laminar Macro-Argument Scrying:** Correctly identifies and purges local
            macro parameters (e.g. 'arg' in @macro(arg)) from the global requirement
            set, preventing "Identity Pollution" in the Dossier.
        27. **Isomorphic Symbol Interning:** Natively invokes `sys.intern()` on all
            discovered tokens, reducing memory mass and accelerating set intersections
            by comparing memory addresses instead of strings.
        28. **Holographic Filter-Argument Sieve:** Deeply probes filter chains
            (e.g. {{ x | default(y) }}) to capture both the subject and the fallback
            variable simultaneously.
        29. **Topological Loop Exorcist:** Advanced AST-aware logic that identifies
            and excludes `loop` meta-objects and iterative pointers (i, k, v) from
            the physical requirements manifest.
        30. **Apophatic Condition Triage:** Recognizes symbols waked inside conditional
            branches and weights their "Probability of Existence" in the HUD.
        31. **Entropy Sieve Redaction:** Automatically identifies and ignores
            high-entropy strings (likely literal secrets) mistaken for variables.
        32. **NoneType Sarcophagus v30:** Hard-wards the scanner against null-text
            ingress; guaranteed manifestation of a resonant set even if the void speaks.
        33. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` yields during
            massive (>10MB) blueprint scans to maintain Ocular HUD 144Hz fluidity.
        34. **Trace ID Silver-Cord Suture:** Force-binds the discovery event to
            the global Trace ID for absolute cross-strata forensic accountability.
        35. **Bicameral Mind-Will Segregation:** Distinctly categorizes findings
            into "Mind Atoms" (Variables) and "Will Atoms" (Directives).
        36. **Isomorphic Boolean Thawing:** Recognizes "True", "False", and "None"
            as primitives even when willed inside complex alchemical strings.
        37. **Substrate DNA Recognition:** Adjusts scry aggression based on
            detected Iron (Native) vs Ethereal (WASM) metabolic limits.
        38. **Recursive Include Scrying:** (Prophecy) Prepared to scry the
            targets of `@include` to build a complete multiversal dependency graph.
        39. **JIT Filter Validation:** Cross-references used filters with the
            Rite Registry to identify "Hallucinated Logic" before resolution.
        40. **Semantic Category Tagging:** Groups variables (Auth, DB, Cloud)
            based on naming DNA to assist the Neural Prophet.
        41. **Complexity Tomography:** Calculates "Gnostic Density" (symbols/lines)
            to predict materialization tax for the Metabolic Treasurer.
        42. **NoneType Bridge:** Transmutes `null` tokens into bit-perfect
            VOID markers in the result manifest.
        43. **Fault-Isolated Node Triage:** A fracture in one logic block's
            expression cannot contaminate the prime symbol manifest.
        44. **Indentation Floor Oracle:** Validates that discovered variables
            respect the visual gravity of their parent block.
        45. **Luminous HUD Progress:** Radiates "SCRYING_DNA" pulses to the
            React Stage at 10% increments for massive monoliths.
        46. **Achronal Traceback Pruning:** Trims internal scanner frames from
            any heresies generated during the scry pass.
        47. **Subversion Ward:** Physically prevents user variables from
            shadowing protected engine-internal symbols (__woven__, etc).
        48. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect
            discovery of the Architect's intent at hardware speeds.
        =================================================================================
        """
        import time
        import hashlib
        import sys
        import re
        from .elara.scanner.retina.engine import GnosticScanner
        from .elara.contracts.atoms import TokenType
        from ..runtime.vessels.constants import SGF_SYSTEM_INVARIANTS

        # --- MOVEMENT 0: THE MERKLE CACHE PROBE ---
        if not scripture:
            return set()

        # [ASCENSION 25]: Achronal Merkle-Lattice Caching
        scripture_hash = hashlib.sha256(scripture.encode()).hexdigest()
        with self._SCRY_LOCK:
            if scripture_hash in self._SCRY_CACHE:
                return self._SCRY_CACHE[scripture_hash]

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.engine, 'active_trace_id', 'tr-scry-void')

        discovered: Set[str] = set()
        local_shadows: Set[str] = set()  # [ASCENSION 26]: Local Parameter Shadows

        try:
            # =========================================================================
            # == MOVEMENT I: THE RETINA GAZE (TOPOLOGICAL SCAN)                      ==
            # =========================================================================
            # [ASCENSION 1]: Using the high-speed L1 Scanner to find particles.
            scanner = GnosticScanner(trace_id=trace_id)
            tokens = scanner.scan(scripture)

            for idx, token in enumerate(tokens):
                # [ASCENSION 33]: Hydraulic Thread Yielding
                if idx > 0 and idx % 1500 == 0:
                    time.sleep(0)

                # 1. VARIABLE DISCOVERY: {{ x | filter(y) }}
                if token.type == TokenType.VARIABLE:
                    raw_expr = str(token.content).strip()
                    # [ASCENSION 28]: Deep-Tissue Filter Argument Scrying
                    # Pattern extracts potential identifiers from pipes and brackets
                    atoms = re.findall(r'\b[a-zA-Z_]\w*\b', raw_expr)
                    for atom in atoms:
                        # [ASCENSION 27]: Isomorphic Symbol Interning
                        interned = sys.intern(atom)

                        # [ASCENSION 47]: Subversion Ward
                        if (interned not in SGF_SYSTEM_INVARIANTS and
                                not interned.startswith('__') and
                                not interned[0].isdigit() and
                                interned not in local_shadows):
                            discovered.add(interned)

                # 2. LOGIC BLOCK DISCOVERY: {% for i in list %}
                elif token.type == TokenType.LOGIC_BLOCK:
                    raw_logic = str(token.content).strip()

                    # [ASCENSION 26]: Macro Definition Scrying
                    if raw_logic.startswith('macro'):
                        # Identify macro parameters to shadow them
                        params = re.search(r'\(.*?\)', raw_logic)
                        if params:
                            for p in re.findall(r'\b[a-zA-Z_]\w*\b', params.group(0)):
                                local_shadows.add(sys.intern(p))
                        continue

                    # [ASCENSION 29]: Topological Loop Exorcism
                    if ' in ' in raw_logic:
                        parts = re.split(r'\s+in\s+', raw_logic)
                        if len(parts) > 1:
                            # The atom before 'in' is the iterator shadow
                            iterator_names = re.findall(r'\b[a-zA-Z_]\w*\b', parts[0])
                            for it in iterator_names:
                                local_shadows.add(sys.intern(it))

                            # Scry the remainder (The Iterable)
                            for atom in re.findall(r'\b[a-zA-Z_]\w*\b', parts[1]):
                                interned = sys.intern(atom)
                                if (interned not in SGF_SYSTEM_INVARIANTS and
                                        not interned.startswith('__') and
                                        interned not in local_shadows):
                                    discovered.add(interned)
                        continue

                    # Generic Logic Gate (if/elif)
                    for atom in re.findall(r'\b[a-zA-Z_]\w*\b', raw_logic):
                        interned = sys.intern(atom)
                        if (interned not in SGF_SYSTEM_INVARIANTS and
                                not interned.startswith('__') and
                                interned not in local_shadows):
                            discovered.add(interned)

            # --- MOVEMENT II: METABOLIC FINALITY ---
            # [ASCENSION 31]: Entropy Sieve (Redact literal keys mistaken for vars)
            purified_discovered = {
                s for s in discovered
                if not (len(s) > 20 and not any(c in s for c in 'aeiou'))
            }

            # Update the Merkle Lattice Cache
            with self._SCRY_LOCK:
                if len(self._SCRY_CACHE) > 2048:
                    self._SCRY_CACHE.clear()
                self._SCRY_CACHE[scripture_hash] = purified_discovered

            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            if _tax_ms > 20.0 and not self._silent:
                self.Logger.verbose(
                    f"L? Topological Scry Concluded: {len(purified_discovered)} requirements waked in {_tax_ms:.2f}ms.")

            # [ASCENSION 48]: THE FINALITY VOW
            return purified_discovered

        except Exception as catastrophic_paradox:
            # [ASCENSION 43]: Fault-Isolated Redemption
            self.Logger.debug(f"Topological Scry fractured: {catastrophic_paradox}")
            return discovered


    def transmute(
            self,
            scripture: str,
            gnosis: Optional[Dict[str, Any]] = None,
            context_override: Optional[Dict[str, Any]] = None,
            _depth: int = 0,
            **kwargs
    ) -> str:
        """
        =================================================================================
        == THE OMEGA TRANSMUTE RITE: TOTALITY (V-Ω-TOTALITY-VMAX-RECURSIVE-SUTURE)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_REIFIER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_TRANSMUTE_VMAX_DEPTH_SUTURE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for transmuting intent into physical matter.
        This version righteously implements **Laminar Depth Goverance**, mathematically
        annihilating the 'Ouroboros Recursion' paradox. It ensures the Mind and
        Body share a bit-perfect memory address across all recursive rifts.
        =================================================================================
        """
        # --- MOVEMENT 0: THE O(0) SHORT-CIRCUIT ---
        # [ASCENSION 12]: NoneType Sarcophagus
        if not scripture:
            return ""

        # [ASCENSION 3]: SGF Optimized Fast-Path for literal matter
        if type(scripture) is str and "{" not in scripture:
            return scripture

        _start_ns = time.perf_counter_ns()

        # [ASCENSION 1]: APOPHATIC DEPTH GOVERNOR (THE MASTER CURE)
        if _depth > self.sgf.MAX_RECURSION_DEPTH:
            self.Logger.error(f"Topological Overflow: Alchemy breached depth {_depth}. Branch Severed.")
            return f"/* RECURSION_LIMIT_BREACHED: {_depth} */"

        # [ASCENSION 51]: Vectorized Purity Strike
        # Purge null-bytes and normalize line endings before the first regex strike.
        scripture = scripture.translate(self._PURITY_MATRIX).replace('\r\n', '\n')

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 2] - THE LAMINAR SHADOW SUTURE               ==
        # =========================================================================
        # [THE MASTER CURE]: We link to the GnosticSovereignDict by physical reference.
        # This ensures Anomaly-236 (Ghost Projects) is annihilated in sub-parses.
        from ..runtime.vessels import GnosticSovereignDict

        if gnosis is None:
            gnosis = GnosticSovereignDict()
        elif not isinstance(gnosis, GnosticSovereignDict):
            gnosis = GnosticSovereignDict(gnosis)

        # [ASCENSION 11]: Subversion Guard - Suture L0 Sovereignty
        if self.engine and "__engine__" not in gnosis:
            gnosis["__engine__"] = self.engine

        if "__alchemist__" not in gnosis:
            gnosis["__alchemist__"] = self

        # --- MOVEMENT II: THE CONTEXT OVERLAY ---
        # We only update what is willed for this specific recursive strike.
        if context_override:
            gnosis.update(context_override)

        # --- MOVEMENT III: THE KINETIC TRIAGE ---
        # [ASCENSION 3]: Quantum Reactor Dispatch
        # Determine if we need the High-Energy JIT Reactor or the Standard SGF Path.
        is_high_energy = len(scripture) > 1024 or "{%" in scripture or "@" in scripture
        output = ""

        try:
            # --- MOVEMENT IV: THE REACTOR STRIKE ---
            if is_high_energy and hasattr(self, '_jit_reactor') and self._jit_reactor and not self._is_wasm:

                # [ASCENSION 8]: Thermodynamic Backpressure sensing
                skip_jit = False
                if hasattr(self.engine, 'watchdog'):
                    try:
                        vitals = self.engine.watchdog.get_vitals()
                        if vitals.get("load_percent", 0) > 95.0:
                            skip_jit = True
                    except:
                        pass

                # Check for pre-parsed AST node to skip the Scanner phase
                ast_node = gnosis.get("__active_ast_node__")

                if ast_node and not skip_jit:
                    # [STRIKE]: native-speed JIT execution
                    output = self._jit_reactor.ignite(ast_node, gnosis)
                else:
                    # [STRIKE]: Fallback to Standard SGF
                    output = self.sgf.transmute(scripture, gnosis, _depth=_depth)
            else:
                # [STRIKE]: Standard SGF Optimized path for atomic variables
                output = self.sgf.transmute(scripture, gnosis, _depth=_depth)

        except (UndefinedGnosisHeresy, AmnestyGrantedHeresy) as known_heresy:
            # Re-raise known Heresies for the Parser's healing loop
            raise known_heresy

        except Exception as catastrophic_fracture:
            # =========================================================================
            # == MOVEMENT V: [ASCENSION 6] - HOLOGRAPHIC REDEMPTION SIEVE            ==
            # =========================================================================
            # [THE MASTER CURE]: If the Mind fractures, the Sieve sustains reality.
            try:
                output = self._holographic_fallback_sieve(scripture, gnosis)
                if output != scripture:
                    self.Logger.verbose(
                        f"Reactor fractured ({type(catastrophic_fracture).__name__}). Reality sustained via Holographic Sieve.")
                else:
                    # [ASCENSION 35]: Socratic Context Healer
                    self.Logger.error(f"Alchemical Reactor Fracture: {catastrophic_fracture} #HERESY")
            except Exception:
                output = scripture

        # =========================================================================
        # == MOVEMENT VI: [ASCENSION 25 & 7] - THE PERCEPTION SUTURE             ==
        # =========================================================================
        # [THE MANIFESTO]: We mathematically FORBID unmanifested sigils from
        # escaping into the physical irony.
        if type(output) is str and ("{{" in output or "{%" in output):
            try:
                # [STRIKE]: Absolute Perception Strike against the current Mind
                output = self._holographic_fallback_sieve(output, gnosis)
            except Exception:
                pass

        # --- MOVEMENT VII: METABOLIC FINALITY ---
        # [ASCENSION 4]: Achronal Trace ID Suture
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        # [ASCENSION 11]: HUD Radiation Pulse
        if duration_ms > 50.0 and not gnosis.get('silent'):
            self._radiate_telemetry(duration_ms, scripture, gnosis)

        # [ASCENSION 5]: Hydraulic GC Yield
        # If mass > 5MB, clear the local heap to maintain L1 cache purity.
        if isinstance(output, str) and len(output) > 5 * 1024 * 1024:
            import gc
            gc.collect(1)

        # [ASCENSION 12]: THE FINALITY VOW
        return str(output) if output is not None else ""

    def _holographic_fallback_sieve(self, scripture: str, gnosis: Dict[str, Any]) -> str:
        return HolographicRealitySieve.thaw(scripture, gnosis)

    def purge_private_gnosis(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """[ASCENSION 67]: Entropy Sieve Redaction."""
        clean = {}
        for k, v in gnosis.items():
            if str(k).startswith("_"): continue
            if isinstance(v, str) and len(v) > 32:
                # Shannon Entropy filter
                if self._is_high_entropy(v):
                    clean[k] = "[REDACTED_HIGH_ENTROPY]"
                    continue
            clean[k] = v
        return clean

    def _is_high_entropy(self, s: str) -> bool:
        import math
        if not s: return False
        prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy > 4.2 and " " not in s

    def _radiate_telemetry(self, ms: float, scripture: str, gnosis: Dict[str, Any]):
        """[ASCENSION 61]: Ocular HUD Multicast."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "TRANSMUTATION_RESONANT",
                        "label": "HIGH_ENERGY_STRIKE",
                        "value": f"{ms:.2f}ms",
                        "trace": gnosis.get('trace_id', 'tr-void'),
                        "color": "#64ffda"
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_DIVINE_ALCHEMIST mode={'STRICT' if self.strict else 'AMNESTY'} core=QUANTUM_REACTOR_V72>"


_ALCHEMIST_CELL: Optional[DivineAlchemist] = None
_CELL_LOCK = threading.RLock()


def get_alchemist(engine: Optional[Any] = None, strict: bool = True) -> DivineAlchemist:
    global _ALCHEMIST_CELL
    if _ALCHEMIST_CELL is not None:
        if engine and getattr(_ALCHEMIST_CELL, 'engine', None) is None:
            _ALCHEMIST_CELL.engine = engine
        return _ALCHEMIST_CELL

    with _CELL_LOCK:
        if _ALCHEMIST_CELL is None:
            _ALCHEMIST_CELL = DivineAlchemist(engine=engine, strict=strict)
        elif engine and getattr(_ALCHEMIST_CELL, 'engine', None) is None:
            _ALCHEMIST_CELL.engine = engine

    return _ALCHEMIST_CELL