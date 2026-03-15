# Path: parser_core/logic_weaver/traversal/evaluator.py
# -----------------------------------------------------

import time
import os
import sys
import threading
import traceback
from typing import Optional, Any, Dict, List, Final
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .context import SpacetimeContext
from ..contracts import LogicScope, ChainStatus
from ....contracts.data_contracts import _GnosticNode, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....logger import Scribe

# =========================================================================
# == [THE OMEGA SUTURE]: ELARA CORE INTEGRATION                          ==
# =========================================================================
from ....core.alchemist.elara.resolver.evaluator import (
    GnosticASTEvaluator,
    AmnestyGrantedHeresy,
    UndefinedGnosisHeresy,
    MetabolicFeverHeresy
)
from ....core.alchemist.elara.resolver.context import LexicalScope
from ....core.alchemist.elara.contracts.state import ForgeContext, SubstratePlane

Logger = Scribe("LogicAdjudicator")


class LogicAdjudicator:
    """
    =============================================================================
    == THE OMEGA LOGIC ADJUDICATOR (V-Ω-TOTALITY-VMAX-INDESTRUCTIBLE)          ==
    =============================================================================
    LIF: ∞^∞ | ROLE: JURISPRUDENCE_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

    The Supreme High Court of the God-Engine. It adjudicates the existence of
    reality by bridging the Scaffold Topography and the ELARA Mind.

    [AXIOM]: Logic is not a guess; it is a spatiotemporal proof.
    """

    __slots__ = ('ctx', '_lock', '_is_wasm', '_instruction_limit')

    def __init__(self, ctx: SpacetimeContext):
        """[THE RITE OF INCEPTION]"""
        self.ctx = ctx
        self._lock = threading.RLock()

        # [ASCENSION 6]: Substrate DNA Recognition
        self._is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten"
        )
        self._instruction_limit = 5000  # [ASCENSION 11]

    def evaluate_gate(self, node: _GnosticNode, scope: LogicScope) -> bool:
        """
        =============================================================================
        == THE RITE OF ADJUDICATION (V-Ω-TOTALITY-VMAX)                            ==
        =============================================================================
        LIF: 1,000,000x | ROLE: REALITY_GOVERNOR

        Evaluates the structural logic gate (@if, @elif, @else) and updates the
        dimensional chain state.
        """
        if not node.item:
            return True

        # [ASCENSION 18]: Linguistic Purity Suture
        raw_ctype = node.item.condition_type or ""
        ctype = str(raw_ctype).lower().split('.')[-1]

        # Normalize 'elseif' to 'elif' for universal resonance
        if ctype == "elseif": ctype = "elif"

        # [ASCENSION 21]: NoneType Zero-G Amnesty for inline constructs
        if not ctype:
            return True

        should_enter = False
        trace_id = self.ctx.gnostic_context.raw.get('trace_id', 'tr-void')

        # --- THE CONSTITUTIONAL CHAIN MACHINE ---
        with self._lock:
            if ctype == 'if':
                scope.start_chain()
                if self._test_condition(node):
                    should_enter = True
                    scope.mark_entered()

            elif ctype == 'elif':
                # [ASCENSION 9]: Branch Mutual Exclusivity Enforced
                if scope.chain_status == ChainStatus.PENDING and self._test_condition(node):
                    should_enter = True
                    scope.mark_entered()

            elif ctype == 'else':
                if scope.chain_status == ChainStatus.PENDING:
                    should_enter = True
                    scope.mark_entered()

            elif ctype in ('endif', 'endfor', 'endtry'):
                scope.end_chain()

        # [ASCENSION 5]: Ocular HUD Multicast
        self._radiate_logic_pulse(node, ctype, should_enter, trace_id)

        node.logic_result = should_enter
        return should_enter

    def _test_condition(self, node: _GnosticNode) -> bool:
        """
        =============================================================================
        == THE OMEGA TEST: TOTALITY (V-Ω-ELARA-STRIKE-VMAX)                       ==
        =============================================================================
        [THE MASTER CURE]: Executes the high-energy ELARA strike.
        """
        condition = node.item.condition
        if not condition:
            return True

        line_num = node.item.line_num
        start_ts = time.perf_counter_ns()

        try:
            # 1. FORGE THE GNOSTIC SANDBOX
            # [ASCENSION 1]: Achronal State Purification
            # We wrap the global mind in a new ForgeContext
            forge_ctx = ForgeContext(
                variables=self.ctx.gnostic_context.raw,
                strict_mode=False,  # [ASCENSION 3]: Absolute Amnesty
                trace_id=self.ctx.gnostic_context.raw.get('trace_id', 'tr-gate'),
                substrate=SubstratePlane.ETHER if self._is_wasm else SubstratePlane.IRON
            )
            lex_scope = LexicalScope(forge_ctx)

            # 2. THE KINETIC STRIKE (ELARA EVALUATION)
            # [STRIKE]: Calling the ELARA/SGF Meta-Compiler Evaluator
            result = GnosticASTEvaluator.evaluate(condition, lex_scope)

            # 3. [ASCENSION 7]: ISOMORPHIC TRUTH THAWING
            # Normalizes "resonant", "manifest", etc., into Python Bits.
            return self._thaw_gnostic_truth(result)

        except UndefinedGnosisHeresy as ugh:
            # [ASCENSION 3]: Amnesty Hand-off
            Logger.verbose(f"L{line_num}: Gnosis Void in Gate '{condition}'. Granting Amnesty (False).")
            return False

        except MetabolicFeverHeresy as mfh:
            # [ASCENSION 4]: Thermodynamic Pacing Error
            self._proclaim_fracture("METABOLIC_FEVER_HERESY", node, mfh)
            return False

        except Exception as catastrophic_paradox:
            # [ASCENSION 15]: Haptic Failure Signaling
            self._proclaim_fracture("LOGIC_ADJUDICATION_FRACTURE", node, catastrophic_paradox)
            return False

    def _thaw_gnostic_truth(self, value: Any) -> bool:
        """[ASCENSION 7 & 12]: Transmutes diverse scalar inputs into absolute logical bits."""
        if value is None: return False
        if isinstance(value, bool): return value

        v_str = str(value).lower().strip()
        # The Trinity of Gnostic Resonance
        if v_str in ('true', 'yes', 'on', '1', 'resonant', 'pure', 'manifest', 'stable'):
            return True
        if v_str in ('false', 'no', 'off', '0', 'fractured', 'void', 'null', 'none'):
            return False

        # [ASCENSION 11]: Weight-Based Truth
        try:
            return bool(float(value))
        except:
            return bool(value)

    def _radiate_logic_pulse(self, node: _GnosticNode, gate: str, result: bool, trace: str):
        """[ASCENSION 5 & 21]: High-frequency HUD pulse with haptic aura."""
        if self.ctx.gnostic_context.raw.get('silent'): return

        engine = self.ctx.gnostic_context.raw.get('__engine__')
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                aura = "#64ffda" if result else "#94a3b8"  # Teal for Taken, Slate for Skipped
                if gate == "else": aura = "#3b82f6"  # Blue for Fallback

                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LOGIC_ADJUDICATED",
                        "label": f"GATE_{gate.upper()}",
                        "message": f"'{node.item.condition or 'True'}' -> {str(result).upper()}",
                        "color": aura,
                        "trace": trace,
                        "line": node.item.line_num
                    }
                })
            except:
                pass

    def _proclaim_fracture(self, code: str, node: _GnosticNode, error: Exception):
        """[ASCENSION 12 & 21]: Inscribes a logical heresy into the forensic ledger."""
        tb = traceback.format_exc()
        Logger.error(f"L{node.item.line_num}: Logic Fracture ({code}): {error}")

        # [ASCENSION 16]: Achronal Temporal Anchoring
        timestamp = time.strftime("%H:%M:%S")

        self.ctx.heresies.append(Heresy(
            code=code,
            message=f"Logical Adjudication failed for structural gate: {type(error).__name__}",
            line_num=node.item.line_num,
            line_content=node.item.raw_scripture,
            details=f"[{timestamp}] ELARA Reactor Exception: {str(error)}\n{tb}",
            severity=HeresySeverity.CRITICAL,
            suggestion="Verify the expression syntax and ensure all willed variables are manifest in the altar."
        ))

    def __repr__(self) -> str:
        return f"<Ω_LOGIC_ADJUDICATOR status=RESONANT substrate={'WASM' if self._is_wasm else 'IRON'} lif=INFINITY>"
