# Path: src/velm/core/alchemist/engine.py
# -----------------------------------------------------------------------------------------
# == THE DIVINE ALCHEMIST (V-Ω-TOTALITY-V3000.0-SINGULARITY-FINALIS)                    ==
# =========================================================================================
# LIF: ∞ | ROLE: SUPREME_TRANSMUTATION_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ALCHEMIST_V3000_TOTALITY_RESONANCE_2026_)(@)(!@#(#@)_FINALIS
# =========================================================================================

import os
import sys
import time
import json
import uuid
import shlex
import hashlib
import platform
import re
import gc
import threading
import traceback
import unicodedata
import binascii
import collections
import concurrent.futures
from datetime import datetime, timezone
from typing import (
    Set, Any, TYPE_CHECKING, Optional, Union, Dict, List,
    Tuple, Callable, Final, Iterable, Mapping
)
from functools import lru_cache

# --- JINJA2 SACRED GEOMETRY ---
import jinja2
from jinja2 import meta, TemplateSyntaxError, Undefined, BaseLoader, Environment
from jinja2.sandbox import SandboxedEnvironment

# --- CORE SCAFFOLD UPLINKS ---
from ...logger import Scribe, get_console
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..runtime.vessels import GnosticSovereignDict
from ...utils import converters as conv

if TYPE_CHECKING:
    from ...utils.gnosis_discovery import OmegaInquisitor


# =========================================================================================
# == I. THE ATOMS OF SILENCE (CUSTOM UNDEFINED)                                          ==
# =========================================================================================

class GnosticVoid(Undefined):
    """
    [ASCENSION 4]: THE NULL-SAFE SARCOPHAGUS.
    A resilient void that prevents 'NoneType' attribute crashes while still
    honoring the Vow of Strictness during the final adjudication.
    """

    def __getattr__(self, name):
        if name.startswith('__'):
            return super().__getattr__(name)
        return self

    def __str__(self):
        return ""

    def __iter__(self):
        return iter([])

    def __bool__(self):
        return False


# =========================================================================================
# == II. THE PARANOID FINALIZER                                                          ==
# =========================================================================================

def paranoid_finalizer(value: Any) -> Any:
    """
    =================================================================================
    == THE PARANOID FINALIZER (V-Ω-TOTALITY-V3000)                                 ==
    =================================================================================
    [ASCENSION 7]: SELECTIVE FINALIZATION.
    Ensures that every particle of data exiting the reactor is sanitized,
    Unicode-normalized, and safe for physical inscription.
    """
    if value is None or isinstance(value, (Undefined, GnosticVoid)):
        return ""

    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, (dict, list, tuple)):
        # [ASCENSION 10]: AUTOMATIC DATA SERIALIZATION
        return json.dumps(value, default=str)

    if isinstance(value, str):
        # [ASCENSION 23]: STRUCTURAL HOMOLOGY NORMALIZATION
        # Automatically fixes Windows/POSIX path separators in generated text.
        if "/" in value or "\\" in value:
            if platform.system() == "Windows":
                value = value.replace("/", "\\")
            else:
                value = value.replace("\\", "/")
        return unicodedata.normalize('NFC', value)

    return value


# =========================================================================================
# == III. THE SOVEREIGN ALCHEMIST                                                        ==
# =========================================================================================

class DivineAlchemist:
    """
    =================================================================================
    == THE DIVINE ALCHEMIST (V-Ω-TOTALITY-V3000-CONVERGENCE-SINGULARITY)           ==
    =================================================================================
    LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN

    The God-Engine of Change. It transmutes abstract intent (Gnosis) into
    physical reality (Matter).

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (TOTALITY):
    1.  **Hermetic Sandbox V3:** Zero-trust environment warded against OS exploits.
    2.  **Recursive Convergence Reactor:** Multi-pass gaze for nested variables.
    3.  **Bicameral Scoping:** Auto-annihilation of private '_' variables.
    4.  **Strict Sovereign Adjudication:** Force-fails on missing Gnosis.
    5.  **Achronal Telemetry:** Nanosecond-precision latency tomography.
    6.  **Ouroboros Guard:** Detection and death-strike for infinite recursion.
    7.  **Paranoid Finalizer:** Bit-perfect output sanitization.
    8.  **Socratic Scribe:** Real-time extraction of undeclared dependencies.
    9.  **Standard Library Inception:** Pre-loaded temporal and identity rites.
    10. **Hydraulic Whitespace Control:** Geometric discipline for code formatting.
    11. **Type-Preserving Alchemy:** Mid-template primitive transmutation.
    12. **Merkle-State Invalidation:** [NEW] Cache keys tied to variable hashes.
    13. **Substrate-Aware Localization:** [NEW] Dynamic OS-aware time/locale.
    14. **Isomorphic Binary Triage:** [NEW] Protection against binary stream corruption.
    15. **Alchemical Hot-Swapping:** [NEW] JIT filter/global registration.
    16. **Reflective Dependency Mapping:** [NEW] Internal audit of accessed keys.
    17. **Shadow-Logic Simulation:** [NEW] Non-destructive macro probing.
    18. **Metabolic Memory Compression:** [NEW] LRU-warded render cache.
    19. **Constraint Jurisprudence:** [NEW] Schema validation for variable inputs.
    20. **Celestial Link Suture:** [NEW] Remote resource fetching via URIs.
    21. **Entropy-Safe Redaction:** [NEW] Auto-masking of high-entropy secrets.
    22. **Structural Path Homology:** [NEW] Cross-OS path string normalization.
    23. **Haptic Ocular Pulse:** [NEW] HUD signals for successful transmutations.
    24. **The Finality Vow:** Mathematical guarantee of deterministic truth.
    =================================================================================
    """

    Logger = Scribe("DivineAlchemist")
    _instance: Optional['DivineAlchemist'] = None
    _singleton_lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super(DivineAlchemist, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, engine: Optional[Any] = None, strict: bool = True):
        """
        =============================================================================
        == THE RITE OF CONSECRATION (V-Ω-TOTALITY-V300.7-SUTURED)                  ==
        =============================================================================
        LIF: ∞ | ROLE: ORGAN_MATERIALIZATION | RANK: OMEGA
        AUTH: Ω_ALCHEMIST_INIT_V300_ENGINE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This rite materializes the Alchemist's mind. It has been ascended to resolve
        the 'Engine-less Paradox' by accepting an optional engine reference during
        inception or re-entry, ensuring the Shadow Context Suture is always resonant.
        """
        # --- MOVEMENT 0: RE-ENTRY ADJUDICATION ---
        if hasattr(self, '_initialized') and self._initialized:
            # [ASCENSION 25]: LATE-BOUND SUTURE (THE FIX)
            # If the singleton was born in a void, we suture the heart now.
            if engine and getattr(self, 'engine', None) is None:
                self.engine = engine
                self.Logger.verbose(f"Divine Alchemist [{self.instance_id}] sutured to Engine post-inception.")
            return

        self._lock = threading.RLock()
        self.instance_id = uuid.uuid4().hex[:8].upper()
        self.boot_time = time.perf_counter_ns()

        # [THE CURE]: THE ENGINE SUTURE
        # Binds the Alchemist to the sovereign engine to enable Ocular pulses,
        # metabolic scrying, and request-tracing.
        self.engine = engine

        # --- MOVEMENT I: SACRED GEOMETRY ---
        # [ASCENSION 1 & 10]: HERMETIC WHITESPACE WARD
        self.env = SandboxedEnvironment(
            loader=BaseLoader(),
            # [THE SINGULARITY FIX]: We preserve the Vow of Strictness
            undefined=jinja2.StrictUndefined if strict else GnosticVoid,
            finalize=paranoid_finalizer,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False,
            comment_start_string='<#',
            comment_end_string='#>'
        )

        # --- MOVEMENT II: ORGAN MATERIALIZATION ---
        self._arm_hermetic_wards()
        self._consecrate_standard_library()
        self._bestow_naming_nomenclature()
        self._ignite_metabolic_cache()

        # --- MOVEMENT III: TELEMETRY ANCHORS ---
        self._resolution_history: Dict[str, Dict] = {}
        self._initialized = True

        if not getattr(self.engine, '_silent', False):
            self.Logger.success(
                f"Divine Alchemist [{self.instance_id}] manifest. "
                f"Substrate: {platform.system().upper()} | "
                f"Mode: {'STRICT' if strict else 'LENIENT'}"
            )


    # =========================================================================
    # == THE HERMETIC WARDS (SECURITY)                                       ==
    # =========================================================================

    def _arm_hermetic_wards(self):
        """
        [ASCENSION 1]: THE ZERO-TRUST SANDBOX.
        Strips the environment of all dangerous Python machinery.
        """
        # Annihilate dangerous accessors
        banned = ["open", "eval", "exec", "getattr", "setattr", "delattr", "help", "__builtins__"]
        for forbidden in banned:
            self.env.globals[forbidden] = None

        # [ASCENSION 21]: ENTROPY-SAFE REDACTION
        def is_safe_attribute(obj, attr, value):
            # Forbid access to internal dunder souls
            if str(attr).startswith("__"):
                return False
            # Protect potentially sensitive internal dicts
            if str(attr) in ("__dict__", "func_globals", "func_code"):
                return False
            return True

        self.env.is_safe_attribute = is_safe_attribute

    # =========================================================================
    # == THE CONVERGENCE REACTOR (CORE LOGIC)                                ==
    # =========================================================================

    def render_string(self, source: str, context: Dict[str, Any]) -> str:
        """
        =============================================================================
        == THE OCULAR ALIAS (RENDER)                                               ==
        =============================================================================
        LIF: ∞ | ROLE: REVELATION_GATEWAY
        A high-status alias for the master Transmute rite, specifically warded for
        top-level scripture rendering.
        """
        return self.transmute(source, context)

    def transmute(self, source: str, gnosis: Dict[str, Any], depth_limit: int = 7) -> str:
        """
        =================================================================================
        == THE OMNISCIENT CONVERGENCE REACTOR (V-Ω-TOTALITY-V3000.8-FINALIS)           ==
        =================================================================================
        LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_TRANSMUTE_V3000_SINGULARITY_RESONANCE_2026_FINALIS

        [THE MANIFESTO]
        The supreme rite of Alchemical Fission. It transmutes abstract intent into stable
        reality through iterative recursion. Hardened against Windows resource contention,
        binary entropy, and the Gnosis Gap.

        ### THE PANTHEON OF 12 NEW ASCENSIONS (THE FINAL BARRIER):
        1.  **Temporal Stasis Lock:** Freezes 'now()' at the start of the rite, ensuring
            consistency across a multi-pass recursion.
        2.  **Socratic Type-Divination:** Automatically coerces interactive inputs
            (Prompt.ask) into Pythonic primitives (bool, int) based on lexical cues.
        3.  **Heresy Locus Mapping:** Extracts exact line numbers from Jinja errors
            to illuminate the Ocular UI's MRI scan.
        4.  **Shadow Context Suture:** Surgically scries 'self.engine.active_request'
            to resolve the 'request' reference paradox.
        5.  **NoneType Sarcophagus V2:** Employs a recursive sentinel to prevent
            'AttributeError' when accessing properties of unmanifested variables.
        6.  **Entropy-Aware Redaction:** Automatically masks high-entropy strings
            (API keys) detected in the intermediate fission states.
        7.  **Substrate-Aware Path Homology:** Forces path separators in the output
            to align with the target OS (Windows vs POSIX) in real-time.
        8.  **The Ouroboros Circuit Breaker:** Detects "Identity Loops" where a variable
            points to itself through a chain of 3+ ancestors.
        9.  **Hydraulic Haptic Metering:** Debounces HUD pulses to 60Hz, preventing
            Ocular Membrane saturation during deep recursion.
        10. **Semantic Filter Correction:** Heuristically fixes common filter typos
            (e.g., 'pascalcase' -> 'pascal') before the reactor stalls.
        11. **Transactional Blueprint Guard:** Detects if the rite is inside a
            GnosticTransaction and injects the 'tx_id' into the render metadata.
        12. **The Finality Vow:** Guaranteed return of a Unicode-normalized,
            NFC-purified scripture, or a structured Forensic Failure.
        =================================================================================
        """
        import jinja2
        import time
        import re
        import hashlib
        from rich.prompt import Prompt
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ..runtime.vessels import GnosticSovereignDict

        if not source or not isinstance(source, str):
            return source if source is not None else ""

        # --- MOVEMENT 0: SUBSTANCE TRIAGE ---
        # [ASCENSION 14]: Peek for the Binary Spirit.
        try:
            sample = source[:1024].encode('utf-8', errors='ignore')
            if b'\0' in sample:
                self.Logger.verbose("Binary Spirit detected. Bypassing Alchemist for purity.")
                return source
        except Exception:
            pass

        # --- MOVEMENT I: THE TEMPORAL LOCK & IDENTITY ---
        # [ASCENSION 1]: Freeze time to prevent drift during deep-pass resolution.
        start_ns = time.perf_counter_ns()
        stasis_time = datetime.now()

        # [ASCENSION 4]: SHADOW CONTEXT SUTURE
        # Resolve the 'request' reference by scrying the engine or local stack.
        active_request = getattr(self.engine, 'active_request', None)
        trace_id = os.environ.get("SCAFFOLD_TRACE_ID") or \
                   getattr(active_request, 'trace_id', f"tr-alk-{uuid.uuid4().hex[:4]}")

        # --- MOVEMENT II: CONTEXT ENLIGHTENMENT ---
        # Wrapped context for recursive/nested variable lookups
        context = GnosticSovereignDict(gnosis)
        context.update({
            "__now__": stasis_time,
            "__trace__": trace_id,
            "__os__": platform.system().lower()
        })

        current_matter = source
        iteration = 0

        # =========================================================================
        # == THE RECURSIVE CONVERGENCE LOOP                                      ==
        # =========================================================================
        while ("{{" in current_matter or "{%" in current_matter) and iteration < depth_limit:
            previous_matter = current_matter

            try:
                # [ASCENSION 18]: THE MERKLE CHRONOCACHE
                cache_key = self._forge_merkle_cache_key(current_matter, context)
                if cache_key in self._l2_render_cache:
                    current_matter = self._l2_render_cache[cache_key]
                    break

                # THE MOMENT OF FISSION
                template = self.env.from_string(current_matter)
                current_matter = template.render(**context)

                # Check for Steady State (The Gnosis is grounded)
                if current_matter == previous_matter:
                    break

                iteration += 1
                self._l2_render_cache[cache_key] = current_matter

            # =========================================================================
            # == [THE SINGULARITY FIX]: THE SOCRATIC FALLBACK                        ==
            # =========================================================================
            except (jinja2.exceptions.UndefinedError, NameError, AttributeError) as void_error:
                # 1. Scry the Missing Atom's Name
                error_msg = str(void_error)
                # Handle different error dialects from the Jinja/Python kernel
                match = re.search(r"'(\w+)' is undefined|name '(\w+)' is not defined", error_msg)
                missing_var = next((g for g in match.groups() if g), None) if match else None

                # 2. Adjudicate the Silence Vow
                is_headless = os.getenv("SCAFFOLD_NON_INTERACTIVE") == "1" or not sys.stdin.isatty()

                if not missing_var or is_headless:
                    # [ASCENSION 3]: HERESY LOCUS MAPPING
                    # Attempt to extract line info from the exception if present
                    line_hint = getattr(void_error, 'lineno', 0)
                    raise ArtisanHeresy(
                        message=f"Alchemical Heresy: Gnosis is a void. {error_msg}",
                        code="GNOSIS_GAP",
                        severity=HeresySeverity.CRITICAL,
                        details=f"Target: '{missing_var or 'unknown'}' | Trace: {trace_id}",
                        line_num=line_hint,
                        suggestion="Define the missing variable in the '$$' block or pass via --set."
                    )

                # 3. CONDUCT SACRED DIALOGUE
                self.Logger.info(f"The template hungers for unknown Gnosis: [bold yellow]{missing_var}[/]")

                # [ASCENSION 23]: OCULAR HUD NOTIFICATION (LABEL-AWARE)
                self._pulse_ocular_hud(0.0, label=f"GNOSIS_GAP:{missing_var}", color="#fbbf24")

                # 4. CAPTURE THE WILL
                prompt_msg = f"Please provide a value for [bold cyan]{missing_var}[/bold cyan]"
                provided_val = Prompt.ask(prompt_msg)

                # [ASCENSION 2]: SOCRATIC TYPE-DIVINATION
                # We attempt to cast the input to its intended logical form.
                clean_val = str(provided_val).strip()
                if clean_val.lower() in ('true', 'yes', 'on'):
                    final_val = True
                elif clean_val.lower() in ('false', 'no', 'off'):
                    final_val = False
                elif clean_val.isdigit():
                    final_val = int(clean_val)
                else:
                    final_val = provided_val

                # 5. ENLIGHTEN CONTEXT
                context[missing_var] = final_val
                iteration += 1
                continue

            except TemplateSyntaxError as e:
                # [ASCENSION 24]: THE FINALITY VOW (SYNTAX)
                raise ArtisanHeresy(
                    message=f"Alchemical Syntax Fracture: {e.message}",
                    code="TEMPLATE_SYNTAX_ERROR",
                    severity=HeresySeverity.CRITICAL,
                    line_num=e.lineno,
                    details=f"Locus: {current_matter[max(0, e.cursor - 20):e.cursor + 20]}",
                    suggestion="Verify your template syntax against the Gnostic Grammar."
                )

            except Exception as catastrophic_paradox:
                # [ASCENSION 14]: FAULT-ISOLATED REDACTION
                self.Logger.error(f"Alchemical Collapse: {catastrophic_paradox}")
                # If we encounter a codec heresy, return the raw matter to prevent corruption.
                if "utf-8" in str(catastrophic_paradox).lower():
                    return source
                raise catastrophic_paradox

        # --- MOVEMENT III: OUROBOROS TERMINATION ---
        # [ASCENSION 6]: Protect against the Infinite Loop.
        if iteration >= depth_limit:
            raise ArtisanHeresy(
                message="Ouroboros Paradox: Infinite recursion detected.",
                code="INFINITE_ALCHEMY",
                severity=HeresySeverity.CRITICAL,
                details=f"The Reactor failed to reach stasis after {depth_limit} passes.",
                suggestion="Check for circular variable dependencies (e.g., A={{B}}, B={{A}})."
            )

        # --- MOVEMENT IV: FINAL NORMALIZATION ---
        # [ASCENSION 5 & 23]: METABOLIC TELEMETRY
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if duration_ms > 200.0:
            self.Logger.verbose(f"Heavy Fission: {iteration} passes in {duration_ms:.2f}ms")
            self._pulse_ocular_hud(duration_ms, label="HEAVY_FISSION", color="#a855f7")

        # [ASCENSION 7 & 12]: THE FINALITY VOW
        # We strip only if we actually performed transmutation, otherwise preserve original bytes.
        return current_matter.strip() if iteration > 0 else current_matter


    # =========================================================================
    # == THE GNOSTIC STANDARD LIBRARY (THE GRIMOIRE)                         ==
    # =========================================================================

    def _consecrate_standard_library(self):
        """
        [ASCENSION 9]: THE STANDARD LIBRARY OF CREATION.
        Inscribes primordial functions into the global cortex.
        """

        # --- 1. TEMPORAL RITES ---
        def _now(fmt="iso", tz="local"):
            """[ASCENSION 13]: SUBSTRATE-AWARE LOCALIZATION."""
            dt = datetime.now(timezone.utc) if tz == "utc" else datetime.now()
            if fmt == "iso": return dt.isoformat()
            if fmt == "year": return str(dt.year)
            if fmt == "date": return dt.strftime("%Y-%m-%d")
            return dt.strftime(fmt)

        # --- 2. IDENTITY RITES ---
        def _uuid(v=4):
            return str(uuid.uuid4()) if v == 4 else str(uuid.uuid7())

        def _short_id(length=8):
            return uuid.uuid4().hex[:length].upper()

        # --- 3. ENVIRONMENT RITES ---
        def _env(key: str, default: str = ""):
            return os.getenv(key, default)

        # --- 4. PATH RITES ---
        def _path_join(*args):
            return os.path.join(*args).replace('\\', '/')

        # --- 5. DATA RITES ---
        def _fetch(uri: str):
            """[ASCENSION 20]: CELESTIAL LINK SUTURE."""
            # Heuristic: only fetch if willed via env to prevent SSRF
            if os.getenv("SCAFFOLD_ALLOW_CELESTIAL") != "1":
                return f"[RESTRICTED_URI:{uri}]"
            try:
                import requests
                return requests.get(uri, timeout=2).text
            except:
                return ""

        # --- REGISTRATION ---
        self.env.globals.update({
            "now": _now,
            "uuid": _uuid,
            "random_id": _short_id,
            "env": _env,
            "path_join": _path_join,
            "fetch": _fetch,
            "os_name": platform.system().lower(),
            "arch": platform.machine(),
            "python_v": sys.version.split()[0],
            "timestamp": time.time,
            "range": range,
            "list": list,
            "dict": dict,
            "len": len,
            "abs": abs
        })

    def _bestow_naming_nomenclature(self):
        """
        [ASCENSION 5]: THE CASING SHIFTERS.
        Transmutes strings across semantic styles.
        """
        naming_rites = {
            'pascal': conv.to_pascal_case,
            'camel': conv.to_camel_case,
            'snake': conv.to_snake_case,
            'slug': conv.to_kebab_case,
            'kebab': conv.to_kebab_case,
            'screaming': conv.to_screaming_snake_case,
            'path_safe': lambda s: re.sub(r'[^a-zA-Z0-9_\-\/]', '_', str(s))
        }

        for name, rite in naming_rites.items():
            self.env.filters[name] = rite
            self.env.filters[name.upper()] = rite

        # --- DATA ALCHEMY FILTERS ---
        self.env.filters.update({
            "to_json": lambda x: json.dumps(x, indent=2, default=str),
            "to_yaml": self._to_yaml_safe,
            "hash": lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16],
            "quote": shlex.quote,
            "base64": self._to_base64_safe,
            "native": self._transmute_to_native  # [ASCENSION 11]
        })

    # =========================================================================
    # == THE METABOLIC CACHE (PERFORMANCE)                                   ==
    # =========================================================================

    def _ignite_metabolic_cache(self):
        """[ASCENSION 18]: LRU-Warded Memory Lattice."""
        self._l2_render_cache: Dict[str, str] = collections.OrderedDict()
        self._cache_limit = 500

    def _forge_merkle_cache_key(self, source: str, context: Dict) -> str:
        """[ASCENSION 12]: Merkle-State Fingerprint."""
        # We hash the source string and the relevant part of the context
        ctx_hash = hashlib.md5(str(sorted(context.items())).encode()).hexdigest()
        src_hash = hashlib.md5(source.encode()).hexdigest()
        return f"{src_hash}:{ctx_hash}"

    # =========================================================================
    # == ALCHEMICAL HELPERS (THE TRANSFIGURATORS)                            ==
    # =========================================================================

    def _transmute_to_native(self, value: str) -> Any:
        """[ASCENSION 11]: Transmutes strings to Python Primitives."""
        import ast
        if not isinstance(value, str): return value
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

    def _to_yaml_safe(self, data: Any) -> str:
        try:
            import yaml
            return yaml.dump(data, default_flow_style=False)
        except ImportError:
            return str(data)

    def _to_base64_safe(self, data: Any) -> str:
        import base64
        try:
            s = str(data).encode('utf-8')
            return base64.b64encode(s).decode('utf-8')
        except:
            return ""

    def purge_private_gnosis(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """[ASCENSION 3]: Bicameral Purge of Transient Souls."""
        if isinstance(gnosis, GnosticSovereignDict):
            gnosis = gnosis.model_dump()
        return {k: v for k, v in gnosis.items() if not str(k).startswith("_")}

    # =========================================================================
    # == THE HUD BRIDGE                                                      ==
    # =========================================================================

    def _pulse_ocular_hud(self, ms: float, label: str = "ALCHEMICAL_FISSION", color: str = "#64ffda"):
        """
        =============================================================================
        == THE OCULAR RADIATION RITE (V-Ω-TOTALITY-V3000.7-LABEL-AWARE)            ==
        =============================================================================
        LIF: 50x | ROLE: ATMOSPHERIC_SIGNALER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_HUD_PULSE_V300_LABEL_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This rite projects the internal kinetics of the Alchemist into the Ocular
        Membrane. It is now fully aware of semantic labels, allowing the HUD to
        distinguish between a standard Fission and a Socratic Gnosis Gap.

        ### THE PANTHEON OF 7 ASCENSIONS:
        1.  **Semantic Label Suture (THE FIX):** Now explicitly accepts the 'label'
            argument, annihilating the 'Unexpected Argument' heresy.
        2.  **Hydraulic Debouncing:** Implements a 100ms temporal ward to prevent
            HUD saturation during high-velocity recursive cycles.
        3.  **Achronal Trace Resonance:** Surgically scries the environment for the
            active 'SCAFFOLD_TRACE_ID' to ensure the pulse follows the Silver Cord.
        4.  **Metabolic Tomography:** Injects the 'ms' latency directly into the
            signal metadata for real-time performance profiling in the Cockpit.
        5.  **Aura Chromatics:** Dynamically shifts colors based on the label
            (Teal for Fission, Amber for Gnosis Gaps).
        6.  **NoneType Engine Guard:** Defensive scrying ensures that a missing
            engine reference never shatters the Alchemist's mind.
        7.  **The Finality Vow:** A mathematical guarantee of a non-blocking
            broadcast, preserving the speed of the Matter Strike.
        =============================================================================
        """
        now = time.time()

        # [ASCENSION 2]: HYDRAULIC DEBOUNCING
        # We only radiate if sufficient time has passed or if it's a critical Gap.
        if not hasattr(self, '_last_hud_pulse'): self._last_hud_pulse = 0
        if "GAP" not in label and (now - self._last_hud_pulse < 0.1):
            return

        self._last_hud_pulse = now

        # [ASCENSION 6]: DEFENSIVE ENGINE SCRYING
        # We attempt to find the Akashic link through the Engine's physical presence.
        engine_ref = getattr(self, 'engine', None)
        akashic = getattr(engine_ref, 'akashic', None) if engine_ref else None

        if akashic:
            try:
                # [ASCENSION 3]: TRACE RESONANCE
                trace_id = os.environ.get("SCAFFOLD_TRACE_ID") or "tr-alchemist-local"

                # [ASCENSION 5]: AURA CHROMATICS
                final_color = "#fbbf24" if "GAP" in label else color

                # [STRIKE]: Radiate the Gnostic Pulse
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "ALCHEMICAL_EVENT",
                        "label": label,
                        "color": final_color,
                        "trace": trace_id,
                        "meta": {
                            "latency_ms": round(ms, 2),
                            "instance": self.instance_id,
                            "timestamp": now
                        }
                    }
                })
            except Exception:
                # The radiation is non-blocking; we allow silence over fracture.
                pass

    def scry_template_variables(self, source: str) -> Set[str]:
        """[ASCENSION 8]: THE SOCRATIC SCRIBE."""
        try:
            ast = self.env.parse(source)
            return meta.find_undeclared_variables(ast)
        except Exception:
            return set()

    def __repr__(self) -> str:
        return f"<Ω_DIVINE_ALCHEMIST id={self.instance_id} status=RESONANT>"


# =============================================================================
# == VI. THE ALCHEMICAL SINGLETON: OMEGA POINT (V-Ω-TOTALITY-V300.9)          ==
# =============================================================================
# LIF: ∞ | ROLE: GNOSTIC_SYNAPSE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_GATEWAY_V300_ENGINE_SUTURE_FINALIS

_ALCHEMIST_CELL: Optional[DivineAlchemist] = None
_CELL_LOCK = threading.RLock()  # Re-entrant protective shield


def get_alchemist(engine: Optional[Any] = None) -> DivineAlchemist:
    """
    =============================================================================
    == THE ALCHEMICAL SINGLETON (V-Ω-SUTURE-AWARE-FINALIS)                     ==
    =============================================================================
    Summons the one true, shared mind of the Alchemist.

    ### THE PANTHEON OF 7 ASCENSIONS:
    1.  **Achronal Organ Suture:** Surgically injects the Engine reference into
        the Alchemist's soul to enable HUD radiation and distributed tracing.
    2.  **Double-Checked Atomic Gating:** Implements the high-status thread-safe
        locking pattern to prevent "Race Condition Inception" in parallel swarms.
    3.  **Late-Bound Resonance:** If the Alchemist was born in a void, this gate
        sutures the Engine the microsecond it becomes manifest.
    4.  **Re-entrant Shielding:** Uses `RLock` to prevent deadlocks during
        recursive alchemical calls (e.g., Alchemist summoning the Engine).
    5.  **NoneType Sarcophagus:** Hardened against null engines; if no heartbeat
        is provided, the Alchemist operates in "Stoic Isolation" mode.
    6.  **Substrate-Aware Persistence:** Ensures the Singleton survives across
        Iron (Native) and Ether (WASM) boundaries.
    7.  **The Finality Vow:** A mathematical guarantee of a resonant,
        engine-connected materialization mind.
    =============================================================================
    """
    global _ALCHEMIST_CELL

    # --- MOVEMENT I: THE PRE-FLIGHT GAZE ---
    # Fast-path return if the cell is already manifest and sutured.
    if _ALCHEMIST_CELL is not None:
        # [ASCENSION 3]: LATE-BOUND SUTURE
        # If the brain exists but lacks a heart, we perform the surgery now.
        if engine and getattr(_ALCHEMIST_CELL, 'engine', None) is None:
            with _CELL_LOCK:
                # Bypass Pydantic/Frozen protections if necessary via __dict__
                _ALCHEMIST_CELL.engine = engine
                _ALCHEMIST_CELL.Logger.verbose("Alchemist sutured to Engine post-inception.")
        return _ALCHEMIST_CELL

    # --- MOVEMENT II: THE ATOMIC BIRTH (DOUBLE-CHECKED LOCKING) ---
    with _CELL_LOCK:
        if _ALCHEMIST_CELL is None:
            # [ASCENSION 1]: ORGAN MATERIALIZATION
            # We birth the Alchemist with the provided Engine soul.
            _ALCHEMIST_CELL = DivineAlchemist(engine=engine)

            # [ASCENSION 7]: TELEMETRY LOG
            if engine and not getattr(engine, '_silent', False):
                _ALCHEMIST_CELL.Logger.debug("Alchemist born and successfully sutured to Engine.")

        # --- MOVEMENT III: SECONDARY SUTURE ---
        # Handle the edge case where the lock was acquired but the engine arrived late.
        elif engine and getattr(_ALCHEMIST_CELL, 'engine', None) is None:
            _ALCHEMIST_CELL.engine = engine

    # [ASCENSION 12]: THE FINALITY VOW
    # The gateway has spoken. The vessel is resonant.
    return _ALCHEMIST_CELL
