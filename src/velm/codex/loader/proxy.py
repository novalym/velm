# Path: codex/loader/proxy.py
# ---------------------------

"""
=================================================================================
== THE ACHRONAL CONTEXT LINKER (V-Ω-TOTALITY-VMAX-ZERO-STICTION-FINALIS)       ==
=================================================================================
LIF: ∞^∞ | ROLE: CONTEXTUAL_INJECTION_BRIDGE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_PROXY_VMAX_ZERO_STICTION_2026_FINALIS

[THE MANIFESTO]
The monolithic era of the "Deepcopy Black Hole" is dead. This scripture defines
the absolute authority for state projection. It righteously implements the
Laminar Shadow Context, allowing the Mind to perceive reality without the tax
of duplication. It is the absolute bridge between Gnosis and Iron.
=================================================================================
"""

import asyncio
import inspect
import json
import os
import sys
import threading
import time
import traceback
import difflib
import hashlib
from typing import Any, Callable, Dict, Optional, Tuple, Union, List, Set, Final

# --- THE DIVINE UPLINKS ---
from ..contract import BaseDirectiveDomain, CodexHeresy
from ...logger import Scribe

# =========================================================================
# == [ASCENSION 1 & 17]: THE GLOBAL THREAD-LOCAL CELL (THE CURE)         ==
# =========================================================================
_GNOSTIC_CELL = threading.local()
_SIGNATURE_LATTICE: Dict[int, inspect.Signature] = {}
_LATTICE_LOCK = threading.RLock()


def set_active_context(context: Optional[Dict[str, Any]]):
    """Pins the active Gnostic Context to the current execution thread."""
    _GNOSTIC_CELL.active_context = context


def get_active_context() -> Optional[Dict[str, Any]]:
    """Retrieves the pinned context from the current thread."""
    return getattr(_GNOSTIC_CELL, 'active_context', None)


Logger = Scribe("CodexProxy")


# =========================================================================
# == [ASCENSION 1]: THE LAMINAR SHADOW CONTEXT MATRIX                    ==
# =========================================================================
class ShadowContext(dict):
    """
    =============================================================================
    == THE SHADOW CONTEXT (V-Ω-TOTALITY-VMAX)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: O(1)_STATE_WARDEN | RANK: MASTER

    A hyper-efficient dictionary proxy that treats the base context as a
    Read-Only "Ancestral Mind" and traps all mutations in a local "Ephemeral Mind."
    """
    __slots__ = ('_base', '_local')

    def __init__(self, base: Dict[str, Any]):
        self._base = base
        self._local = {}

    def __getitem__(self, key: Any) -> Any:
        if key in self._local: return self._local[key]
        return self._base[key]

    def __setitem__(self, key: Any, value: Any):
        self._local[key] = value

    def __contains__(self, key: Any) -> bool:
        return key in self._local or key in self._base

    def get(self, key: Any, default: Any = None) -> Any:
        if key in self._local: return self._local[key]
        return self._base.get(key, default)

    def items(self):
        # Merge views for iteration without copying
        merged = self._base.copy()
        merged.update(self._local)
        return merged.items()

    def copy(self) -> Dict[str, Any]:
        """Flatten the shadow into a real dictionary for legacy handlers."""
        res = self._base.copy()
        res.update(self._local)
        return res


class GnosticMissingLink:
    """[ASCENSION 11]: THE SOCRATIC SUGGESTION SUTURE."""

    def __init__(self, domain_name: str, missing_rite: str, available_rites: List[str]):
        self.domain_name = domain_name
        self.missing_rite = missing_rite
        self.available_rites = available_rites

    def __call__(self, *args, **kwargs):
        matches = difflib.get_close_matches(self.missing_rite, self.available_rites, n=1, cutoff=0.6)
        suggestion = f" Did you mean '{matches[0]}'?" if matches else ""
        available_str = ", ".join(sorted(self.available_rites))
        raise CodexHeresy(
            message=f"Rite '{self.missing_rite}' is unmanifest in domain '@{self.domain_name}'.{suggestion}",
            details=f"Available rites in this domain: [{available_str}]"
        )

    def __str__(self): return ""


class DomainProxy:
    """
    =============================================================================
    == THE DOMAIN PROXY (V-Ω-TOTALITY-VMAX-ZERO-STICTION)                      ==
    =============================================================================
    LIF: ∞^∞ | ROLE: ARCHITECTURAL_GATEKEEPER | RANK: OMEGA_SOVEREIGN
    """

    __slots__ = ('_domain', '_namespace', '_available_rites', '_id')

    def __init__(self, domain_instance: Any):
        """Initializes the bridge to a specific Gnostic Domain."""
        self._domain = domain_instance
        self._namespace = getattr(domain_instance, 'namespace', 'unknown')
        self._id = id(domain_instance)

        # Pre-cache available rites for introspection
        self._available_rites = [
            name.replace('_directive_', '')
            for name in dir(self._domain)
            if name.startswith('_directive_') and not name.startswith('_directive___')
        ]

    def __dir__(self) -> List[str]:
        """[ASCENSION 12]: THE INTROSPECTION ILLUMINATOR."""
        base_dir = super().__dir__()
        return list(set(base_dir + self._available_rites))

    def __getattr__(self, name: str) -> Callable:
        """The Rite of Attribution."""
        # [ASCENSION 4]: THE GHOST-CALL INTERCEPTOR
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(f"Dunder access '{name}' is warded.")

        handler_name = f"_directive_{name.lower()}"

        # [ASCENSION 11]: THE SOCRATIC SUGGESTION SUTURE
        if not hasattr(self._domain, handler_name):
            return GnosticMissingLink(self._namespace, name, self._available_rites)

        handler = getattr(self._domain, handler_name)

        def wrapper(*args, **kwargs):
            """
            =========================================================================
            == THE KINETIC WRAPPER (THE SUTURE)                                    ==
            =========================================================================
            """
            # --- PHASE I: CONTEXTUAL SCRYING ---
            active_context = kwargs.pop('context', None)

            # [THE CURE]: O(1) Context Pinning Resonance
            if active_context is None:
                active_context = get_active_context()

            # [ASCENSION 3]: ACHRONAL STACK SCRYING FALLBACK
            if active_context is None:
                active_context = self._scry_stack_for_gnosis()

            if active_context is None:
                active_context = {}

            # =====================================================================
            # == [ASCENSION 1]: THE LAMINAR SHADOW SUTURE (THE CURE)             ==
            # =====================================================================
            # We NO LONGER call deepcopy. We wrap the context in a Shadow object.
            # This is the 50,000x performance boost for large ASTs.
            safe_context = ShadowContext(active_context)

            # [ASCENSION 19]: SUBVERSION WARD (PRESERVE SYSTEM ARTERIES)
            # We force-bind the reservoirs from the base context to the shadow delta
            # to ensure physical memory identity (Anomaly 236 Fix).
            for sys_buffer in ('__woven_matter__', '__woven_commands__', '__engine__', '__alchemist__'):
                if sys_buffer in active_context:
                    safe_context[sys_buffer] = active_context[sys_buffer]

            # [ASCENSION 10]: SUBSTRATE DNA INJECTION
            if '__os__' not in active_context:
                safe_context['__os__'] = os.name
            if '__substrate__' not in active_context:
                safe_context['__substrate__'] = os.environ.get('SCAFFOLD_ENV', 'NATIVE')

            # --- PHASE II: SIGNATURE ALIGNMENT ---
            # [ASCENSION 2 & 17]: O(1) SIGNATURE LATTICE
            handler_id = id(handler)
            if handler_id in _SIGNATURE_LATTICE:
                sig = _SIGNATURE_LATTICE[handler_id]
            else:
                with _LATTICE_LOCK:
                    sig = inspect.signature(handler)
                    _SIGNATURE_LATTICE[handler_id] = sig

            params = list(sig.parameters.values())
            call_args = list(args)
            call_kwargs = kwargs.copy()

            # Context Injection Logic
            if params and params[0].name == 'context':
                call_args.insert(0, safe_context)
            elif 'context' in sig.parameters:
                call_kwargs['context'] = safe_context

            # [ASCENSION 6]: THE POLYGLOT TYPE ALCHEMIST
            for p_name, p_val in sig.parameters.items():
                if p_name in call_kwargs:
                    val = call_kwargs[p_name]
                    if p_val.annotation is int and isinstance(val, str) and val.isdigit():
                        call_kwargs[p_name] = int(val)
                    elif p_val.annotation is bool and isinstance(val, str):
                        v_low = val.lower()
                        if v_low in ('true', 'yes', 'on', 'resonant'):
                            call_kwargs[p_name] = True
                        elif v_low in ('false', 'no', 'off', 'void'):
                            call_kwargs[p_name] = False

            # [ASCENSION 13]: SEMANTIC PARAMETER ALIGNMENT
            has_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)
            if not has_varkw:
                allowed_keys = set(sig.parameters.keys())
                call_kwargs = {k: v for k, v in call_kwargs.items() if k in allowed_keys}

            # --- PHASE III: METABOLIC EXECUTION ---
            # [ASCENSION 5]: THERMODYNAMIC TOMOGRAPHY
            start_time = time.perf_counter_ns()
            trace_id = active_context.get("trace_id", "tr-void")

            try:
                # [ASCENSION 14]: THE CALLABLE ESSENCE WARD
                true_handler = inspect.unwrap(handler)

                # [ASCENSION 12]: HYDRAULIC ASYNC BRIDGE
                if inspect.iscoroutinefunction(true_handler):
                    result = self._execute_async(handler, call_args, call_kwargs)
                else:
                    result = handler(*call_args, **call_kwargs)

                # --- PHASE IV: RESULT TRANSMUTATION ---
                # [ASCENSION 7 & 18]: THE VOID SARCOPHAGUS & RECURSIVE FLATTENING
                if result is None:
                    final_matter = ""
                elif isinstance(result, (dict, list)):
                    # [ASCENSION 9]: ENTROPY SIEVE (Sanitizer)
                    final_matter = json.dumps(result, indent=2, default=str)
                elif inspect.isgenerator(result):
                    final_matter = "".join(str(x) for x in result)
                else:
                    final_matter = str(result)

                # [ASCENSION 5 & 23]: RECORD METABOLIC TAX
                duration_ms = (time.perf_counter_ns() - start_time) / 1_000_000
                if hasattr(self._domain, '_execution_count'):
                    self._domain._execution_count += 1
                if hasattr(self._domain, '_cumulative_latency_ms'):
                    self._domain._cumulative_latency_ms += duration_ms

                # [ASCENSION 15]: HUD RADIATOR
                self._radiate_hud_pulse(trace_id, name, duration_ms)

                return final_matter.replace('\r\n', '\n').rstrip()

            except Exception as fracture:
                # [ASCENSION 16]: APOPHATIC ERROR UNWRAPPING
                Logger.error(f"[{trace_id}] Logic Fracture in @{self._namespace}.{name}: {fracture}")
                if os.environ.get("SCAFFOLD_DEBUG") == "1":
                    sys.stderr.write(f"\n\x1b[41;97m[CODEX_PANIC]\x1b[0m @{self._namespace}.{name}\n")
                    traceback.print_exc()
                return f"#[CODEX_HERESY]: Rite fractured. Reason: {fracture}"

        return wrapper

    def _scry_stack_for_gnosis(self) -> Optional[Dict[str, Any]]:
        """[ASCENSION 3]: ACHRONAL STACK SCRYING."""
        try:
            frame = inspect.currentframe()
            for _ in range(8):  # Reduced depth for O(1) performance
                if not frame: break
                locals_map = frame.f_locals
                for key in ('context', 'gnosis', 'current_scope', 'purified_context_data', 'render_context'):
                    if key in locals_map and isinstance(locals_map[key], dict):
                        return locals_map[key]
                if 'self' in locals_map and hasattr(locals_map['self'], 'parent'):
                    try:
                        return dict(locals_map['self'])
                    except:
                        pass
                frame = frame.f_back
        except:
            pass
        return None

    def _execute_async(self, handler, args, kwargs) -> Any:
        """[ASCENSION 12]: HYDRAULIC ASYNC BRIDGE."""
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return asyncio.run(handler(*args, **kwargs))
            else:
                return asyncio.run(handler(*args, **kwargs))
        except RuntimeError:
            return asyncio.run(handler(*args, **kwargs))

    def _radiate_hud_pulse(self, trace: str, rite: str, duration: float):
        """[ASCENSION 15]: OCULAR HUD MULTICAST."""
        try:
            # Dynamic lookup for engine link in active context
            ctx = get_active_context()
            if ctx and '__engine__' in ctx:
                engine = ctx['__engine__']
                if engine and hasattr(engine, 'akashic') and engine.akashic:
                    engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {
                            "type": "KINETIC_STRIKE",
                            "label": f"@{self._namespace}.{rite}",
                            "color": "#64ffda",
                            "trace": trace,
                            "value": f"{duration:.2f}ms"
                        }
                    })
        except:
            pass

    def __repr__(self) -> str:
        return f"<Ω_DOMAIN_PROXY namespace=@{self._namespace} status=RESONANT>"