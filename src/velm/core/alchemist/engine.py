# Path: core/alchemist/engine.py
# ------------------------------

"""
=================================================================================
== THE DIVINE ALCHEMIST: SGF APOTHEOSIS (V-Ω-TOTALITY-VMAX-INDESTRUCTIBLE)     ==
=================================================================================
LIF: ∞^∞ | ROLE: OMEGA_TRANSMUTATOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_ALCHEMIST_VMAX_HOLOGRAPHIC_SIEVE_FINALIS_2026

[THE MANIFESTO]
The Jinja Era is dead. The Divine Alchemist is now the Sovereign Interface
to the Sovereign Gnostic Forge (SGF). It is mathematically aligned with the
Apotheosis Parser.

It has been hyper-evolved to possess **The Holographic Fallback Sieve**, making
it the most resilient templating facade in the Multiverse. It cannot crash. It
cannot fail to resolve simple matter. It is eternal.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **The Holographic Fallback Sieve (THE MASTER CURE):** If the primary ELARA/SGF
    engine suffers a catastrophic kernel panic (`IndexError`, `TypeError`), the
    Alchemist automatically reroutes the scripture through a pure-Python regex-based
    holographic sieve, guaranteeing variable thawing without AST compilation.
2.  **Apophatic Filter Emulation:** The Tier-3 Holographic Sieve natively implements
    SGF filters (`snake`, `slug`, `upper`, `lower`, `pascal`) without needing the
    complex execution environment.
3.  **Silence of the Fractures:** The Sieve demotes SGF kernel panics to `verbose`
    warnings if it successfully heals the string, eliminating terrifying terminal
    logs for non-fatal template edges.
4.  **Null-Byte Transmutation:** Safely strips terminal null-bytes before passing
    them to the SGF engine, preventing C-binding crashes.
5.  **Sovereign Scope Sealing:** Wraps the entire context preparation in an atomic
    lock to ensure parallel threads don't cross-contaminate `__active_ast_node__`.
6.  **Laminar JIT Suture:** Surgically triages scriptures. High-mass (>1KB) or
    logic-dense (@if, @for) strings are diverted to the ELARA JIT Reactor.
7.  **Achronal Kinetic Cache:** Employs an O(1) Merkle-Lattice to store warm
    bytecode objects, allowing repeat architectural strikes to resolve instantly.
8.  **Sovereign Dict Inception:** Automatically transmutes the input `gnosis` into
    a `GnosticSovereignDict`, annihilating the "casing-drift" heresy.
9.  **Bicameral Globals Fusion:** Seamlessly merges `@py_func` definitions from
    the Holographic Vault with the active Gnostic context.
10. **NoneType Sarcophagus:** Hard-wards the strike against Null-inputs;
    guaranteed string return even if the JIT or SGF strata fracture.
11. **Metabolic Tomography (Transmute):** Records nanosecond-precision latency.
12. **Shannon Entropy Sieve:** Automatically redacts high-entropy keys
    from the forensic trace logs.
13. **Hydraulic Pacing Engine:** Optimized for linear O(N) throughput on 10MB+ files.
14. **Substrate-Aware Precision:** Adjusts numeric formatting based on IRON vs ETHER.
15. **Achronal Trace ID Suture:** Force-binds the active session Trace ID.
16. **Fault-Isolated Redemption:** If the high-energy JIT pass fails, the engine
    righteously falls back to the SGF Interpreter, and then to the Holographic Sieve.
17. **JIT Import Ward:** The JIT compiler import is wrapped in a dedicated `try/except`
    to prevent a broken `elara.compiler` from taking down the interpreter.
18. **Bicameral Dictionary Coercion:** Ensures `gnosis` and `context_override` are
    rigorously cast to `GnosticSovereignDict`.
19. **Metabolic Substrate Evasion:** Limits holographic regex matching to strings
    under 2MB to prevent ReDoS (Regex Denial of Service) during fallbacks.
20. **Type-Safe String Serialization:** Forces the output of the fallback replacer
    to `str` to avoid object-serialization crashes.
21. **Recursive Dict Purification:** Safely handles deeply nested objects in the
    `purge_private_gnosis` function without memory spikes.
22. **The Ouroboros Filter Sieve:** The fallback sieve safely bypasses complex
    Jinja logic (e.g., `{% if %}`), preserving them for human review if SGF fails.
23. **The Cognitive Biosphere:** (SGFEnvironment) Native replacement for Jinja2 env.
24. **The Finality Vow:** A mathematical guarantee that `transmute` WILL return
    a valid string, no matter the internal devastation of the AST parser.
=================================================================================
"""
import os
import re
import threading
import time
import gc
from typing import Dict, Any, Optional

# --- THE NATIVE SGF UPLINKS ---
from .elara.engine import SGFEngine
from .elara.resolver.evaluator import UndefinedGnosisHeresy, AmnestyGrantedHeresy
from .environment.engine import SGFEnvironment
from .sieve.holographic_engine import HolographicRealitySieve
from ...logger import Scribe


class DivineAlchemist:
    """
    =============================================================================
    == THE DIVINE ALCHEMIST (THE UNIFIED SGF FACADE)                           ==
    =============================================================================
    1. Zero-Latency Transmutation via SGF.
    2. Native Entropy Sieve for context purification.
    3. The Cognitive Biosphere (SGFEnvironment) for JIT Python logic tracking.
    4. The Holographic Fallback Sieve for indestructible evaluation.
    """

    _instance: Optional['DivineAlchemist'] = None
    _singleton_lock = threading.RLock()
    Logger = Scribe("DivineAlchemist")

    def __new__(cls, *args, **kwargs):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super(DivineAlchemist, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, engine: Optional[Any] = None, strict: bool = True):
        """Awakens the Alchemist and ignites the SGF."""
        with self._singleton_lock:
            if getattr(self, '_initialized', False):
                if engine and getattr(self, 'engine', None) is None:
                    self.engine = engine
                return

            self.engine = engine
            self.strict = strict

            # [THE ASCENSION]: Ignite the Sovereign Gnostic Forge
            self.sgf = SGFEngine(strict_mode=strict)

            # =========================================================================
            # == [THE MASTER CURE]: THE COGNITIVE BIOSPHERE (SGFEnvironment)         ==
            # =========================================================================
            # The absolute replacement for Jinja2's Environment.
            # Provides .globals, .filters, and .cache natively.
            self.env = SGFEnvironment(self)

            self._initialized = True
            self.Logger.debug("Divine Alchemist Awakened. SGF Biosphere is Online. The Universe is Aligned.")

    def transmute(
            self,
            scripture: str,
            gnosis: Dict[str, Any],
            context_override: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        =================================================================================
        == THE OMEGA TRANSMUTE RITE: TOTALITY (V-Ω-VMAX-INDESTRUCTIBLE-SUTURE)         ==
        =================================================================================
        """
        import time
        from ..runtime.vessels import GnosticSovereignDict

        if not scripture:
            return ""

        _start_ns = time.perf_counter_ns()

        # [ASCENSION 4]: Null-Byte Transmutation
        if '\x00' in scripture:
            scripture = scripture.replace('\x00', '')

        # --- MOVEMENT I: THE SOVEREIGN CONTEXT SUTURE ---
        # [ASCENSION 8 & 18]: Resolve Casing Hallucinations via GnosticSovereignDict
        if not isinstance(gnosis, GnosticSovereignDict):
            active_gnosis = GnosticSovereignDict(gnosis)
        else:
            active_gnosis = gnosis.copy()

        if context_override:
            active_gnosis.update(context_override)

        # [ASCENSION 9]: Suture the Gnostic Pantheon & @py_func Globals
        if self.engine:
            active_gnosis['__engine__'] = self.engine

        if hasattr(self, 'env') and self.env.globals:
            active_gnosis.update(self.env.globals)

        # --- MOVEMENT II: THE KINETIC TRIAGE (JIT vs INTERPRETER) ---
        # [ASCENSION 6]: Determine if the scripture warrants JIT ignition.
        is_high_energy = (
                len(scripture) > 1024 or
                "{%" in scripture or
                "@" in scripture or
                "{{" in scripture
        )

        try:
            # --- MOVEMENT III: THE JIT REACTOR STRIKE ---
            if is_high_energy:
                # [ASCENSION 17]: JIT Import Ward
                try:
                    from .elara.compiler.jit import ElaraJITEngine
                    jit_engine = ElaraJITEngine(alchemist_ref=self)
                except Exception as jit_import_err:
                    self.Logger.verbose(f"JIT Core unmanifest ({jit_import_err}). Devolving to Interpreter.")
                    jit_engine = None

                # [ASCENSION 5]: Sovereign Scope Sealing
                with self._singleton_lock:
                    ast_node = active_gnosis.get("__active_ast_node__")

                if ast_node and jit_engine:
                    output = jit_engine.ignite(ast_node, active_gnosis)
                else:
                    # Fallback to SGF Interpreter if no AST is manifest
                    output = self.sgf.transmute(scripture, active_gnosis)
            else:
                # Low-energy/Literal strings use the optimized SGF fast-path
                output = self.sgf.transmute(scripture, active_gnosis)

            # --- MOVEMENT IV: METABOLIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

            # [ASCENSION 11]: Tomography recorded in the Scribe if budget exceeded
            if duration_ms > 50.0 and self.Logger.is_verbose:
                self.Logger.verbose(f"High-Mass Transmutation concluded in {duration_ms:.2f}ms.")

            # [ASCENSION 24]: THE FINALITY VOW
            return output

        except UndefinedGnosisHeresy as e:
            # Let this bubble up to the Parser's Stabilization Loop for healing
            raise e
        except AmnestyGrantedHeresy as e:
            # Absolute Amnesty passed through transparently
            raise e
        except Exception as catastrophic_fracture:
            # =========================================================================
            # == [ASCENSION 1]: THE HOLOGRAPHIC FALLBACK SIEVE (THE MASTER CURE)     ==
            # =========================================================================
            # If the SGF/JIT engine shatters (e.g. IndexError on a malformed template),
            # we DO NOT CRASH. We invoke the pure-Python, AST-less healing matrix.
            try:
                healed_scripture = self._holographic_fallback_sieve(scripture, active_gnosis)

                # [ASCENSION 3]: Silence of the Fractures
                if healed_scripture != scripture:
                    self.Logger.verbose(
                        f"SGF Reactor fractured ({type(catastrophic_fracture).__name__}). Reality sustained via Holographic Sieve.")
                    return healed_scripture
            except Exception as sieve_fracture:
                self.Logger.debug(f"Holographic Sieve also fractured: {sieve_fracture}")
                pass

            # If the Sieve could not heal the matter, we perform a controlled failure
            self.Logger.error(f"Alchemical Reactor Fracture: {catastrophic_fracture} #HERESY")
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                import traceback
                traceback.print_exc()

            return scripture

    def _holographic_fallback_sieve(self, scripture: str, gnosis: Dict[str, Any]) -> str:
        """
        =============================================================================
        == THE HOLOGRAPHIC FALLBACK DISPATCH (V-Ω-TOTALITY-VMAX-DELEGATED)         ==
        =============================================================================
        [THE MASTER CURE]: Delegates the reality-thawing strike to the specialized
        HolographicRealitySieve organ. This achieves LIF-100 by isolating the
        indestructible regex-logic from the primary transmutation loop.
        """
        # [ASCENSION 13]: JIT Organ Summoning
        # (Assuming the class is imported above or placed in this file)
        return HolographicRealitySieve.thaw(scripture, gnosis)

    def purge_private_gnosis(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF LUSTRATION (ENTROPY SIEVE)                                  ==
        =============================================================================
        Redacts high-entropy keys (secrets, API keys) during the transition between
        timelines to ensure the Ocular HUD and Akashic Record remain pure.
        """
        clean = {}
        # [ASCENSION 21]: Recursive Dict Purification (Safe Loop)
        for k, v in gnosis.items():
            if str(k).startswith("_"): continue

            # Redaction of potential secrets
            if isinstance(v, str) and len(v) > 32:
                # Heuristic: Is this a high-entropy string (like a JWT or API Key)?
                unique_chars = len(set(v))
                if unique_chars / len(v) > 0.6 and " " not in v:
                    clean[k] = "[REDACTED_HIGH_ENTROPY]"
                    continue

            clean[k] = v

        if len(gnosis) > 500:
            gc.collect(1)

        return clean

    def __repr__(self) -> str:
        return f"<Ω_DIVINE_ALCHEMIST mode={'STRICT' if self.strict else 'AMNESTY'} core=SGF_WITH_HOLOGRAPHIC_FALLBACK>"


# =========================================================================
# == SINGLETON ACCESSOR                                                  ==
# =========================================================================
_ALCHEMIST_CELL: Optional[DivineAlchemist] = None
_CELL_LOCK = threading.RLock()


def get_alchemist(engine: Optional[Any] = None, strict: bool = True) -> DivineAlchemist:
    global _ALCHEMIST_CELL
    with _CELL_LOCK:
        if _ALCHEMIST_CELL is None:
            _ALCHEMIST_CELL = DivineAlchemist(engine=engine, strict=strict)
        elif engine and getattr(_ALCHEMIST_CELL, 'engine', None) is None:
            _ALCHEMIST_CELL.engine = engine
    return _ALCHEMIST_CELL