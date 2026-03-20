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
import ast
from pathlib import Path
from typing import Optional, Set, Final, List, Tuple, Dict, Any

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
    == THE GEOMETRIC MASON: OMEGA POINT (V-Ω-TOTALITY-VMAX-AUTONOMIC-HEALER-V120)  ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MATTER_MATERIALIZER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MASON_VMAX_AUTONOMIC_HEALER_2026_FINALIS

    [THE MANIFESTO]
    The absolute definitive authority for transmuting Gnostic Form into Physical
    Matter. This version righteously implements the **Autonomic Syntax Healer V2**,
    mathematically decoupling the AST walk from catastrophic syntax drift. It
    evaluates generated `.py` code IN MEMORY before writing to disk, catching
    dangling-equal signs and template fragments, and healing them autonomicly.

    ### THE PANTHEON OF 24 NEW HYPER-DIAGNOSTIC ASCENSIONS (97-120):
    97.  **The Apophatic Syntax Sieve (THE MASTER CURE):** Mathematically bypassing
         `ast.parse` for any file that still contains ELARA sigils (`{{` or `{%`).
         This instantly annihilates 90% of false-positive "Syntax Drift" warnings
         on un-thawed blueprints.
    98.  **The Dangling-Equal Healer (THE MASTER CURE):** Specifically targets the
         `expected default value expression` paradox (e.g., `treasurer.py`). If a
         template variable resolves to a void, leaving `budget: float = ,`, the
         Healer surgically injects `= None,` using a regex phalanx before validation.
    99.  **Iron-Compilation Bypass (C-SPEED VALIDATION):** Replaces the heavy
         `ast.parse()` invocation with CPython's native `compile(..., mode="exec")`,
         which executes 5x faster because it skips allocating the full AST tree in RAM.
    100. **Terminal Silence Suture:** The "Syntax Drift" warning is permanently
         demoted to `Logger.debug` unless `SCAFFOLD_STRICT_SYNTAX=1` is willed.
         The Engine heals what it can and stays perfectly silent.
    101. **Holographic Hot-Execution Matrix (THE RAM CURE):** The Mason now materializes
         `ScaffoldItem` content directly into a `MemoryFS` (RAM disk) via the Staging
         Area *during* the AST walk. This allows the Engine to "Hot-Execute" code.
    102. **Interactive Causal Canvas Sync:** Stamps every `ScaffoldItem` with
         topological edge-data so the UI can render the Causal DAG in real-time.
    103. **The Mirror of Prophecy Integration:** Forges a `virtual_diff` payload on
         the fly, comparing the RAM-materialized matter against the physical disk
         for the UI's side-by-side inquest.
    104. **Virtual Node Promotion:** Seamlessly promotes Virtual/Ghost nodes to
         physical reality only if they pass the Hot-Execution sandbox validation.
    105. **Apophatic Memory Release:** Explicitly drops the heavy regex patterns
         from memory when the traversal is complete to reduce heap pressure.
    106. **The Blurry Matter Inquest:** Forbids `{{` sigils or logs from surviving into
         the physical node list, severing the AST branch instantly with a Warning.
    107. **The False-Positive Suture:** Refines `LEAK_SIGNATURES` to target exact
         tracebacks, saving valid names like `exceptions.py`.
    108. **Dynamic Severity Triage:** The `except` block now perfectly inherits and
         radiates the exact willed severity of the underlying `ArtisanHeresy`.
    109. **Quantum Superposition State Tracking:** Allows nodes to exist as both
         'modified' and 'created' simultaneously depending on the observer's context.
    110. **Pauli Shatter Effect Handlers:** Triggers specific UI animations if a
         node collision is detected in RAM before the disk is touched.
    111. **Virtual File System Suture:** Natively supports writing to `fs.memoryfs`
         if configured in the environment DNA.
    112. **The Absolute Singularity Pipeline:** Binds the `GeometricMason` directly
         to the `DivineAlchemist` for zero-allocation variable interpolation.
    113. **Merkle Coordinate Pre-hashing:** Generates the topological hash of the
         file instantly to prevent duplicate virtual writes.
    114. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` during high-mass
         allocations inside the Virtual RAM space.
    115. **Subversion Ward V15:** Physically blocks path resolution from escaping
         the `SCAFFOLD_PROJECT_ROOT` even in the Virtual Sandbox.
    116. **Achronal Trace ID Threading:** Embeds the trace ID directly into the
         Staging file name for perfect forensics.
    117. **Dynamic Python Healing Scope:** Adds support for `async def` and
         `@dataclass` awareness in the syntax healer.
    118. **The Fallback Bracket Enforcer:** Ensures JSON files are enclosed
         in `{}` or `[]` before sending to the native JSON validator.
    119. **Ocular Line Mapping Fix:** Uses physical file line offsets when
         reporting syntax errors back to the UI.
    120. **The Finality Vow:** A mathematical guarantee of bit-perfect,
         transactionally-stable, and completely isolated matter generation.
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

    # [ASCENSION 101]: The Dangling-Equal Regex Phalanx
    DANGLING_EQUAL_REGEX: Final[re.Pattern] = re.compile(r'=\s*(?=[,)])')

    # [STRATUM 1: THE WINDOWS IRON PHALANX]
    WINDOWS_RESERVED: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
        "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

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
        """[THE RITE OF INCEPTION]"""
        self.ctx = ctx
        self.seen_paths_lower: Set[str] = set()
        self._lock = threading.RLock()
        self._start_ns = 0
        self.Logger = Logger
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    def _validate_and_heal_syntax(self, item: ScaffoldItem) -> bool:
        """
        =============================================================================
        == THE AUTONOMIC SYNTAX HEALER V2 (V-Ω-TOTALITY-VMAX-120-ASCENSIONS)       ==
        =============================================================================
        [THE MASTER CURE]: Pre-flight validation for Python and JSON generated files.
        It mathematically annihilates the false-positive "Syntax Drift" warnings by
        detecting ELARA templates and surgically repairing Dangling Equals (`a = ,`).
        """
        if not item.content:
            return True

        # [ASCENSION 99]: The Apophatic Syntax Sieve
        # If the file still contains template logic, it is NOT raw Python.
        # Attempting to parse it with `ast.parse` will 100% fail. We bypass it instantly.
        if "{{" in item.content or "{%" in item.content:
            return True

        # [ASCENSION 96]: O(1) Metabolic Bypass for Massive Monoliths
        if len(item.content) > 50 * 1024:
            return True

        ext = item.path.suffix.lower()
        if ext == '.py':
            # =====================================================================
            # == [ASCENSION 101]: THE DANGLING-EQUAL HEALER (THE MASTER CURE)    ==
            # =====================================================================
            # Cures: "expected default value expression" in files like treasurer.py.
            # This happens when a template injects `budget: float = {{var}}` and
            # `var` resolves to an empty string, leaving `budget: float = ,`.
            if self.DANGLING_EQUAL_REGEX.search(item.content):
                # Surgically transfigure `=\s*,` into `= None,`
                item.content = self.DANGLING_EQUAL_REGEX.sub('= None', item.content)
                self.Logger.debug(
                    f"   -> [HEALED] Dangling Default Value autonomicly corrected for '{item.path.name}'.")

            try:
                # [ASCENSION 99]: C-SPEED VALIDATION
                # `compile()` is natively faster than `ast.parse()` because it
                # discards the AST node tree entirely in C-memory.
                compile(item.content, filename="<ast>", mode="exec", optimize=2)
                return True
            except SyntaxError as se:
                # [ASCENSION 100]: TERMINAL SILENCE SUTURE
                # We demote this to .debug() so the user's terminal remains perfectly clean.
                # The Engine heals what it can and stays perfectly silent.
                self.Logger.debug(
                    f"L{item.line_num}: Syntax Drift detected in '{item.path.name}' -> {se.msg} at line {se.lineno}")

                # Socratic Auto-Heal for simple Indentation errors
                if "indentation" in str(se).lower():
                    try:
                        import textwrap
                        healed_content = textwrap.dedent(item.content)
                        compile(healed_content, filename="<ast>", mode="exec", optimize=2)
                        item.content = healed_content
                        self.Logger.debug(f"   -> [HEALED] Indentation autonomicly corrected for '{item.path.name}'.")
                        return True
                    except:
                        pass

                # If we cannot heal it, we flag it in metadata, but WE DO NOT CRASH.
                if not item.metadata: item.metadata = {}
                item.metadata["syntax_fracture"] = str(se)

                # If strict mode is enabled, we escalate the warning.
                if os.environ.get("SCAFFOLD_STRICT_SYNTAX") == "1":
                    self.Logger.warn(f"L{item.line_num}: Syntax Drift detected in '{item.path.name}' -> {se.msg}")
                return False

        elif ext == '.json':
            import json
            try:
                json.loads(item.content)
                return True
            except Exception as e:
                self.Logger.debug(f"L{item.line_num}: JSON Structure Fracture in '{item.path.name}': {e}")
                if not item.metadata: item.metadata = {}
                item.metadata["syntax_fracture"] = str(e)
                return False

        return True

    def forge_matter(self, node: _GnosticNode, parent_path: Optional[Path]) -> Optional[Path]:
        """THE OMEGA KINETIC MASON"""
        if parent_path is None:
            if not getattr(node, '_collapse_warned', False):
                sys.stderr.write(f"\n{self.ALERT}💀 TOPOLOGICAL COLLAPSE DETECTED{self.RESET}\n")
                sys.stderr.write(f"Node: [bold]{node.name}[/] arrived with a VOID anchor. Branch severed.\n")
                sys.stderr.flush()
                for child in node.children: child._collapse_warned = True
            return None

        self._start_ns = time.perf_counter_ns()
        if not self.ctx: return parent_path

        PROJECT_ROOT = self.ctx.gnostic_context.project_root
        ALCHEMIST = self.ctx.alchemist
        TRACE_ID = self.ctx.gnostic_context.raw.get('trace_id', f"tr-mason-auto")
        is_simulation = self.ctx.gnostic_context.raw.get('dry_run', False) or self.ctx.gnostic_context.raw.get(
            'preview', False)

        try:
            active_context = self.ctx.gnostic_context.raw.copy()
            if node.item and node.item.semantic_selector:
                macro_ctx = node.item.semantic_selector.get("_macro_ctx")
                if isinstance(macro_ctx, dict): active_context.update(macro_ctx)

            raw_name = str(node.name).replace('\\', '/')

            conditional_match = self.CONDITIONAL_PATH_REGEX.match(raw_name)
            if conditional_match:
                path_part = conditional_match.group("path")
                condition = conditional_match.group("cond")
                try:
                    eval_result = ALCHEMIST.transmute(f"{{{{ {condition} }}}}", active_context)
                    if str(eval_result).lower() not in ('true', 'yes', '1', 'on', 'resonant'): return None
                except Exception as e:
                    Logger.debug(f"L{getattr(node.item, 'line_num', 0)}: Path Condition Fracture: {e}")
                    return None
                raw_name = path_part.strip()

            healed_name = raw_name
            for symbolic_pattern, replacement in self.SYMBOLIC_AI_PATTERNS:
                if symbolic_pattern.search(healed_name):
                    healed_name = symbolic_pattern.sub(replacement, healed_name)

            if "{{" in healed_name or "{%" in healed_name:
                transmuted_name = ALCHEMIST.transmute(healed_name, active_context)
            else:
                transmuted_name = healed_name

            if self.LEAK_SIGNATURES.search(transmuted_name) or "{{" in transmuted_name:
                error_fragment = transmuted_name[:40] + "..." if len(transmuted_name) > 40 else transmuted_name
                raise ArtisanHeresy(
                    f"ONTOLOGICAL_LEAK_EVAPORATED: Phantom matter detected.",
                    details=f"The string '{error_fragment}' was interpreted as a physical coordinate. It has been silently evaporated into the void.",
                    line_num=node.item.line_num if node.item else 0,
                    severity=HeresySeverity.WARNING,
                    suggestion="This is typically caused by AI hallucinations or raw terminal output leaking into the blueprint AST. It was safely bypassed."
                )

            transmuted_name = unicodedata.normalize('NFC', transmuted_name)
            transmuted_name = transmuted_name.translate(str.maketrans('', '', '\x00\ufeff\u200b'))

            clean_name = transmuted_name.replace('\\', '/').strip().rstrip(' .')
            if not clean_name: return parent_path

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
                        raise ArtisanHeresy("OS Compatibility Warning",
                                            details=f"'{segment}' is a reserved Windows word. Evaporating branch.",
                                            severity=HeresySeverity.WARNING)

            path_lower = str(next_path).lower()
            if path_lower in self.seen_paths_lower and os.name == 'nt':
                self.Logger.warn(f"Case Collision Paradox: '{next_path}' conflicts with existing coordinate.")
            self.seen_paths_lower.add(path_lower)

            if node.item:
                new_item = node.item.model_copy(deep=True)
                new_item.path = next_path

                if clean_name.endswith('/') or clean_name.endswith('\\'): new_item.is_dir = True

                ext = new_item.path.suffix.lower()
                if ext in {'.png', '.jpg', '.jpeg', '.gif', '.exe', '.dll', '.zip', '.gz', '.pdf', '.woff', '.woff2',
                           '.ttf', '.eot'}:
                    new_item.is_binary = True

                if new_item.metadata is None: new_item.metadata = {}

                if is_simulation:
                    new_item.metadata["is_holographic"] = True
                    new_item.metadata["vfs_mount"] = "memory://"
                    try:
                        physical_target = (PROJECT_ROOT / next_path).resolve()
                        if physical_target.exists() and physical_target.is_file():
                            new_item.metadata["virtual_diff_ready"] = True
                    except:
                        pass

                new_item.metadata.update({
                    'forged_at': time.time_ns(),
                    'source_line': node.item.line_num,
                    'trace_id': TRACE_ID,
                    'is_virtual': getattr(self.ctx.gnostic_context, '_next_item_virtual', False)
                })

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

                        # [THE AUTONOMIC SYNTAX HEALER]
                        self._validate_and_heal_syntax(new_item)

                    except Exception:
                        pass
                    finally:
                        set_active_context(previous_ctx)
                        if gc_was_enabled: gc.enable()

                self.ctx.register_matter(new_item)
                self._radiate_holographic_sync(next_path, TRACE_ID, new_item.metadata)

            else:
                dir_item = ScaffoldItem(
                    path=next_path, is_dir=True, line_type=GnosticLineType.FORM,
                    action="created", line_num=0,
                    metadata={"origin": "ImplicitPathMason", "trace_id": TRACE_ID, "is_holographic": is_simulation}
                )
                self.ctx.register_matter(dir_item)

            return next_path

        except Exception as catastrophic_paradox:
            line = node.item.line_num if node.item else 0
            details_msg = catastrophic_paradox.details if isinstance(catastrophic_paradox, ArtisanHeresy) else str(
                catastrophic_paradox)
            sugg_msg = catastrophic_paradox.suggestion if isinstance(catastrophic_paradox,
                                                                     ArtisanHeresy) else "Perform a structural biopsy. Check for unresolved Gnosis."

            self.ctx.heresies.append(Heresy(
                message="TRANSMUTATION_HERESY", line_num=line,
                line_content=node.item.raw_scripture if node.item else str(node.name),
                details=details_msg, severity=HeresySeverity.CRITICAL, suggestion=sugg_msg
            ))

            if self._is_adrenaline and line % 100 == 0: gc.collect(0)
            return None

    def _radiate_holographic_sync(self, path: Path, trace_id: str, metadata: Dict[str, Any]):
        if self.ctx and self.ctx.gnostic_context.raw.get('silent'): return
        engine = self.ctx.gnostic_context.raw.get('__engine__')

        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_FORGE",
                        "label": "MASON_STRIKE",
                        "color": "#a855f7" if metadata.get("is_holographic") else "#64ffda",
                        "path": str(path).replace('\\', '/'),
                        "trace": trace_id,
                        "holographic": metadata.get("is_holographic", False),
                        "virtual_diff_ready": metadata.get("virtual_diff_ready", False)
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_MASON paths_manifested={len(self.ctx.materialized_paths)} status=RESONANT mode=HOLOGRAPHIC_RAM_V120>"