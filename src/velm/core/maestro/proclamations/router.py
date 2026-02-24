# Path: core/maestro/proclamations/router.py
# ------------------------------------------

import re
import shlex
import sys
import os
import time
import hashlib
from typing import Any, Dict, Optional, Type, List, Final, Union

# --- THE DIVINE UPLINKS ---
from .base import ProclamationScribe
from .terminal_scribe import TerminalScribe
from .panel_scribe import PanelScribe
from .table_scribe import TableScribe
from .slack_scribe import SlackScribe
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("ProclamationRouter")


def _divine_gnosis(obj: Any) -> Dict[str, Any]:
    """
    =============================================================================
    == THE POLYMORPHIC CONTEXT SCRYER (THE CURE)                               ==
    =============================================================================
    LIF: 100x | ROLE: IDENTITY_RESOLVER

    [THE MANIFESTO]: This helper annihilates the 'dict has no attribute' heresy.
    It scries the object to find 'gnosis' or 'variables', regardless of its form.
    """
    if obj is None: return {}

    # 1. DICTIONARY REALITY
    if isinstance(obj, dict):
        return obj.get('gnosis', obj.get('variables', obj.get('context', {})))

    # 2. OBJECT REALITY
    # Check common Gnostic anchors in order of precedence
    for anchor in ['gnosis', 'variables', 'context']:
        if hasattr(obj, anchor):
            val = getattr(obj, anchor)
            if val is not None: return val

    return {}


class GnosticProxyContext:
    """[ASCENSION]: A minimal, unbreakable wrapper to satisfy Attribute accessors."""
    def __init__(self, gnosis_dict: Dict[str, Any]):
        self.variables = gnosis_dict


class GnosticProxyEngine:
    """[ASCENSION]: A fail-safe shell representing the Engine in a void."""
    def __init__(self, c: Any, r: Any):
        self.console = c
        self.logger = Scribe("ProxyEngine")
        # [THE CURE]: Wraps the dict in a proper Context object
        self.context = GnosticProxyContext(_divine_gnosis(r))
        self.akashic = None  # Prevents 'NoneType has no attribute akashic'


def dispatch_proclamation(
        raw_plea: str,
        alchemist: Any,
        console: Any,
        engine: Any,
        regs: Any
):
    """
    =============================================================================
    == THE OMNISCIENT DISPATCH RITE (V-Ω-TOTALITY-V2000-HEALED)                ==
    =============================================================================
    LIF: ∞ | ROLE: SEMANTIC_VOICE_CONDUCTOR
    """
    start_ns = time.perf_counter_ns()

    # --- MOVEMENT 0: THE GNOSTIC PROXY SUTURE (THE CORE FIX) ---
    # [ASCENSION 1]: We ensure that the 'engine' object passed to Scribes is resonant.
    if engine is None:
        engine = GnosticProxyEngine(console or get_console(), regs)

    # [ASCENSION 2]: Double-checked console suture
    if not hasattr(engine, 'console') or engine.console is None:
        safe_console = console or get_console()
        try:
            object.__setattr__(engine, 'console', safe_console)
        except (AttributeError, TypeError):
            engine.console = safe_console

    # --- MOVEMENT I: ATOMIC TRIAGE & LEXICAL ANALYSIS ---
    # Matches 'key: message' or 'key(args)'
    match = re.match(r'^\s*(\w+)\s*[:\(]', raw_plea)

    scribe_map: Dict[str, Type[ProclamationScribe]] = {
        "panel": PanelScribe,
        "table": TableScribe,
        "slack": SlackScribe,
        "terminal": TerminalScribe
    }

    selected_key = "terminal"
    payload = raw_plea
    metadata = {}

    active_gnosis = _divine_gnosis(regs)

    if match:
        key = match.group(1).lower()
        if key in scribe_map:
            selected_key = key
            # [ASCENSION 3]: Advanced Arg-Weaving
            if "(" in raw_plea and ")" in raw_plea:
                # Handle function style: table(rows={{list}}, title="Manifest")
                inner = raw_plea[raw_plea.find("(") + 1: raw_plea.rfind(")")]
                try:
                    # [ASCENSION 4]: Alchemical Variable Thawing
                    hydrated_inner = alchemist.transmute(inner, active_gnosis)
                    # shlex handles complex quoting in arguments
                    for pair in shlex.split(hydrated_inner):
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            metadata[k.strip()] = v.strip().strip('"\'')
                    payload = ""
                except Exception as e:
                    Logger.debug(f"Arg-Weaving fracture: {e}. Falling back to raw payload.")
                    payload = raw_plea
            else:
                # Handle colon style: panel: My Message
                payload = raw_plea.split(":", 1)[1].strip()

    # --- MOVEMENT II: SUBSTRATE-AWARE ADAPTATION ---
    # [ASCENSION 5 & 11]: If Adrenaline is high or TTY is void, we downgrade to Terminal
    is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
    is_headless = not sys.stderr.isatty()

    if (is_adrenaline or is_headless) and selected_key not in ("terminal", "slack"):
        Logger.verbose(f"Substrate Shift: Downgrading '{selected_key}' to 'terminal' for velocity.")
        selected_key = "terminal"
        if not payload and "msg" in metadata:
            payload = metadata["msg"]
        elif not payload:
            payload = str(metadata)

    # --- MOVEMENT III: KINETIC MATERIALIZATION (SUMMONS) ---
    try:
        # [ASCENSION 9]: Fault-Isolated Inception
        ScribeClass = scribe_map[selected_key]
        artisan = ScribeClass(engine, alchemist)

        # [ASCENSION 8]: Trace Identity Suture
        if isinstance(regs, dict):
            trace_id = regs.get('trace_id', 'tr-unbound')
        else:
            trace_id = getattr(regs, 'trace_id', 'tr-unbound')

        # [STRIKE]: THE PROCLAMATION
        artisan.proclaim(payload, metadata)

        # [ASCENSION 7]: HUD Multicast
        if hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "PROCLAMATION",
                        "label": selected_key.upper(),
                        "color": "#64ffda",
                        "trace": trace_id,
                        "meta": {
                            "latency_ns": time.perf_counter_ns() - start_ns,
                            "dialect": selected_key
                        }
                    }
                })
            except Exception:
                pass

    except Exception as fracture:
        # [ASCENSION 9]: RESILIENT FALLBACK (THE CURE)
        # If the willed scribe fails, we log it purely to DEBUG and invoke the terminal.
        error_msg = f"Proclamation Router Fracture: {str(fracture)}"
        Logger.debug(error_msg)

        # [STRIKE]: The Ultimate Fallback
        fallback = TerminalScribe(engine, alchemist)
        # Wrap fallback proclaim in try/except to prevent recursive explosion
        try:
            fallback.proclaim(f"[dim red]![/] {payload or raw_plea}", {"error": error_msg})
        except Exception as deep_fracture:
            Logger.debug(f"TerminalScribe Fallback Failed: {deep_fracture}")