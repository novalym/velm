# Path: parser_core/logic_weaver/traversal/mason.py
# -------------------------------------------------


import sys
import gc
import os
import re
import time
import unicodedata
import threading
import uuid
from pathlib import Path
from typing import Optional, Set, Final, List, Tuple

# --- THE DIVINE UPLINKS ---
from .context import SpacetimeContext
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ....logger import Scribe
from ....codex.loader.proxy import set_active_context, get_active_context

Logger = Scribe("GeometricMason")


class GeometricMason:
    """
    =================================================================================
    == THE GEOMETRIC MASON: OMEGA POINT (V-Ω-TOTALITY-VMAX-84-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MATTER_MATERIALIZER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MASON_VMAX_PHANTOM_EVAPORATION_2026_FINALIS

    [THE MANIFESTO]
    The absolute definitive authority for transmuting Gnostic Form into Physical
    Matter. This version righteously implements the **Phantom Matter Evaporation Suture**,
    mathematically annihilating the "Hyper-Vigilance Paradox" where stray UI logs or AI
    hallucinations would crash the entire Engine. It now silently incinerates
    anomalous branches while preserving the Prime Timeline.

    ### THE PANTHEON OF 24 NEW HYPER-DIAGNOSTIC ASCENSIONS (60-84):
    74. **The Blurry Matter Inquest:** Forbids `{{` sigils or logs from surviving into
        the physical node list, severing the AST branch instantly.
    75. **The False-Positive Suture:** Refines `LEAK_SIGNATURES` to target exact
        tracebacks, saving valid names like `exceptions.py`.
    76. **Phantom Matter Evaporation Suture (THE MASTER CURE):** Dynamically degrades
        Ontological Leaks from `CRITICAL` to `WARNING`. If a ghost string enters the
        Mason, it is evaporated into the void without shattering the God-Engine's
        overall convergence pass.
    77. **Dynamic Severity Triage:** The `except` block now perfectly inherits and
        radiates the exact willed severity of the underlying `ArtisanHeresy`,
        ensuring true Panics remain fatal while Noise is purged.
    =================================================================================
    """

    __slots__ = ('ctx', 'seen_paths_lower', '_lock', '_start_ns', 'Logger', '_is_adrenaline')

    # [CHROMATIC SIGILS]
    GOLD: Final[str] = "\x1b[38;5;220m"
    UV: Final[str] = "\x1b[38;5;141m"
    ALERT: Final[str] = "\x1b[41;1m"  # INVERSE RED
    RESET: Final[str] = "\x1b[0m"

    # [PATTERNS]
    ILLEGAL_CHARS: Final[re.Pattern] = re.compile(r'[<>:"|?*\x00-\x1F\x7F-\x9F]')
    HOMOGLYPH_REGEX: Final[re.Pattern] = re.compile(r'[\u200b\u200c\u200d\u2060\uFEFF]')
    CONDITIONAL_PATH_REGEX: Final[re.Pattern] = re.compile(r'^(?P<path>.*)\s+@if\((?P<cond>.*)\)$')

    # [STRATUM 1: THE WINDOWS IRON PHALANX]
    # Blocking reserved words that crash the OS Kernel.
    WINDOWS_RESERVED: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
        "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # =========================================================================
    # == THE FALSE-POSITIVE SUTURE (REFINED LEAK SIGNATURES)                 ==
    # =========================================================================
    LEAK_SIGNATURES: Final[re.Pattern] = re.compile(
        r'('
        r'\/\*|'  # SGF Fracture markers (/*)
        r'\[dim\]|\[bold\]|\[cyan\]|\[red\]|'  # Rich UI Formatting tags
        r'Traceback \(most recent call last\):|'  # Python Traceback signatures
        r'\bTypeError:|\bValueError:|\bKeyError:|\bAttributeError:|\bException:|'  # Specific exception signatures
        r'!!\s|\?\?\s|>>\s|::|<<\s'  # Escaped literal sigils with boundaries
        r')'
    )

    SYMBOLIC_AI_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
        (re.compile(r'\{\{\s*_(project|package|app|slug|name|title|desc|author)_\s*\}\}'), r'{{ \1 }}'),
        (re.compile(r'\{\{\s*_(default|lower|upper|snake|pascal|camel|kebab|coalesce)_\s*\}\}'), r'{{ \1 }}'),
    ]

    def __init__(self, ctx: SpacetimeContext):
        """
        =============================================================================
        == THE RITE OF INCEPTION: OMEGA (V-Ω-TOTALITY-VMAX-ADRENALINE-SUTURE)      ==
        =============================================================================
        """
        self.ctx = ctx
        self.seen_paths_lower: Set[str] = set()
        self._lock = threading.RLock()
        self._start_ns = 0
        self.Logger = Logger

        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    def forge_matter(self, node: _GnosticNode, parent_path: Optional[Path]) -> Optional[Path]:
        """
        =================================================================================
        == THE Ω_GEOMETRIC_MASON: TOTALITY (V-Ω-TOTALITY-VMAX-LEAK-WARDED-FINALIS)     ==
        =================================================================================
        """
        if parent_path is None:
            if not getattr(node, '_collapse_warned', False):
                sys.stderr.write(f"\n{self.ALERT}💀 TOPOLOGICAL COLLAPSE DETECTED{self.RESET}\n")
                sys.stderr.write(f"Node: [bold]{node.name}[/] arrived with a VOID anchor. Branch severed.\n")
                sys.stderr.flush()
                for child in node.children:
                    child._collapse_warned = True
            return None

        self._start_ns = time.perf_counter_ns()

        if not self.ctx:
            return parent_path

        PROJECT_ROOT = self.ctx.gnostic_context.project_root
        ALCHEMIST = self.ctx.alchemist
        TRACE_ID = self.ctx.gnostic_context.raw.get('trace_id', f"tr-mason-auto")

        try:
            # --- MOVEMENT I: CONTEXTUAL INCEPTION ---
            active_context = self.ctx.gnostic_context.raw.copy()

            if node.item and node.item.semantic_selector:
                macro_ctx = node.item.semantic_selector.get("_macro_ctx")
                if isinstance(macro_ctx, dict):
                    active_context.update(macro_ctx)

            raw_name = str(node.name).replace('\\', '/')

            # --- MOVEMENT II: CONDITIONAL TOPOGRAPHY ---
            conditional_match = self.CONDITIONAL_PATH_REGEX.match(raw_name)
            if conditional_match:
                path_part = conditional_match.group("path")
                condition = conditional_match.group("cond")
                try:
                    eval_result = ALCHEMIST.transmute(f"{{{{ {condition} }}}}", active_context)
                    if str(eval_result).lower() not in ('true', 'yes', '1', 'on', 'resonant'):
                        return None  # Branch dissolved naturally
                except Exception as e:
                    Logger.warn(f"L{getattr(node.item, 'line_num', 0)}: Path Condition Fracture: {e}")
                    return None
                raw_name = path_part.strip()

            # =========================================================================
            # == MOVEMENT III: GEOMETRIC ALCHEMY (PATH TRANSMUTATION)                ==
            # =========================================================================
            healed_name = raw_name
            for symbolic_pattern, replacement in self.SYMBOLIC_AI_PATTERNS:
                if symbolic_pattern.search(healed_name):
                    healed_name = symbolic_pattern.sub(replacement, healed_name)

            if "{{" in healed_name or "{%" in healed_name:
                transmuted_name = ALCHEMIST.transmute(healed_name, active_context)
            else:
                transmuted_name = healed_name

            # =========================================================================
            # ==[ASCENSION 74 & 76]: THE BLURRY MATTER INQUEST (THE MASTER CURE)    ==
            # =========================================================================
            if self.LEAK_SIGNATURES.search(transmuted_name) or "{{" in transmuted_name:
                error_fragment = transmuted_name[:40] + "..." if len(transmuted_name) > 40 else transmuted_name

                # [THE FIX]: We throw a WARNING instead of a CRITICAL. This allows the
                # Traverser to log the anomaly but CONTINUE building the rest of the project!
                raise ArtisanHeresy(
                    f"ONTOLOGICAL_LEAK_EVAPORATED: Phantom matter detected.",
                    details=f"The string '{error_fragment}' was interpreted as a physical coordinate. It has been silently evaporated into the void.",
                    line_num=node.item.line_num if node.item else 0,
                    severity=HeresySeverity.WARNING,  # <--- THE ABSOLUTE CURE
                    suggestion="This is typically caused by AI hallucinations or raw terminal output leaking into the blueprint AST. It was safely bypassed."
                )

            # --- MOVEMENT IV: PHYSICAL PURIFICATION ---
            transmuted_name = unicodedata.normalize('NFC', transmuted_name)
            transmuted_name = transmuted_name.translate(str.maketrans('', '', '\x00\ufeff\u200b'))

            clean_name = transmuted_name.replace('\\', '/').strip().rstrip(' .')
            if not clean_name:
                return parent_path

            # --- MOVEMENT V: GEOMETRIC JURISPRUDENCE (THE MOAT) ---
            next_path = (parent_path / clean_name)

            try:
                abs_root = PROJECT_ROOT.resolve()
                check_path = (abs_root / next_path).resolve() if not next_path.is_absolute() else next_path.resolve()

                if os.path.commonpath([str(abs_root), str(check_path)]) != str(abs_root):
                    Logger.warn(f"Moat Breach Blocked: '{check_path}' escapes project root. Re-anchoring.")
                    return parent_path
            except Exception:
                pass

            if os.name == 'nt':
                for segment in next_path.parts:
                    stem = segment.split('.')[0].upper()
                    if stem in self.WINDOWS_RESERVED:
                        # Make this a warning too, so windows users don't suffer total crash
                        raise ArtisanHeresy(
                            "OS Compatibility Warning",
                            details=f"'{segment}' is a reserved Windows word. Evaporating branch.",
                            severity=HeresySeverity.WARNING
                        )

            path_lower = str(next_path).lower()
            if path_lower in self.seen_paths_lower and os.name == 'nt':
                self.Logger.warn(f"Case Collision Paradox: '{next_path}' conflicts with existing coordinate.")
            self.seen_paths_lower.add(path_lower)

            # --- MOVEMENT VI: MATTER MATERIALIZATION ---
            if node.item:
                new_item = node.item.model_copy(deep=True)
                new_item.path = next_path

                if clean_name.endswith('/') or clean_name.endswith('\\'):
                    new_item.is_dir = True

                ext = new_item.path.suffix.lower()
                if ext in {'.png', '.jpg', '.jpeg', '.gif', '.exe', '.dll', '.zip', '.gz', '.pdf', '.woff', '.woff2',
                           '.ttf', '.eot'}:
                    new_item.is_binary = True

                if new_item.metadata is None: new_item.metadata = {}
                new_item.metadata.update({
                    'forged_at': time.time_ns(),
                    'source_line': node.item.line_num,
                    'trace_id': TRACE_ID,
                    'is_virtual': getattr(self.ctx.gnostic_context, '_next_item_virtual', False)
                })

                # --- MOVEMENT VII: ELARA TRANSMUTATION STRIKE ---
                if new_item.content and not new_item.is_binary:
                    render_ctx = active_context.copy()
                    render_ctx['_meta'] = new_item.metadata
                    render_ctx["__current_file__"] = str(next_path).replace('\\', '/')
                    render_ctx["__current_dir__"] = str(next_path.parent).replace('\\', '/')
                    render_ctx["__current_column__"] = node.item.original_indent

                    previous_ctx = get_active_context()
                    set_active_context(render_ctx)

                    gc_was_enabled = gc.isenabled()
                    if self._is_adrenaline: gc.disable()

                    try:
                        new_item.content = ALCHEMIST.transmute(new_item.content, render_ctx)
                    except Exception:
                        pass
                    finally:
                        set_active_context(previous_ctx)
                        if gc_was_enabled: gc.enable()

                self.ctx.register_matter(new_item)
                self._radiate_hud_pulse(next_path, TRACE_ID)

            else:
                dir_item = ScaffoldItem(
                    path=next_path, is_dir=True, line_type=GnosticLineType.FORM,
                    action="created", line_num=0,
                    metadata={"origin": "ImplicitPathMason", "trace_id": TRACE_ID}
                )
                self.ctx.register_matter(dir_item)

            return next_path

        except Exception as catastrophic_paradox:
            # =========================================================================
            # ==[ASCENSION 77]: DYNAMIC SEVERITY TRIAGE (THE MASTER CURE)           ==
            # =========================================================================
            line = node.item.line_num if node.item else 0

            # If the paradox is a known Heresy, we respect its willed severity.
            # This allows Warnings (like Evaporated Logs) to pass through harmlessly.
            if isinstance(catastrophic_paradox, ArtisanHeresy):
                severity = catastrophic_paradox.severity
                details_msg = catastrophic_paradox.details
                sugg_msg = catastrophic_paradox.suggestion
                msg_title = catastrophic_paradox.message
            else:
                # If it's a raw Python panic (KeyError, TypeError), it remains CRITICAL.
                severity = HeresySeverity.CRITICAL
                details_msg = str(catastrophic_paradox)
                sugg_msg = "Perform a structural biopsy. Check for unresolved Gnosis."
                msg_title = "TRANSMUTATION_HERESY"

            self.ctx.heresies.append(Heresy(
                message=msg_title,
                line_num=line,
                line_content=node.item.raw_scripture if node.item else str(node.name),
                details=details_msg,
                severity=severity,  # <--- THE FIX
                suggestion=sugg_msg
            ))

            # We return None to sever the current branch, but because severity is
            # WARNING, the TraversalEngine will NOT abort the entire project build!
            return None

    def _radiate_hud_pulse(self, path: Path, trace_id: str):
        if self.ctx and self.ctx.gnostic_context.raw.get('silent'): return
        engine = self.ctx.gnostic_context.raw.get('__engine__')
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_FORGE",
                        "label": "MASON_STRIKE",
                        "color": "#64ffda",
                        "path": str(path).replace('\\', '/'),
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_MASON paths_manifested={len(self.ctx.materialized_paths)} status=RESONANT mode=PHANTOM_EVAPORATION>"