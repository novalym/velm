# Path: parser_core/parser/ast_weaver/weaver/path_mason.py
# --------------------------------------------------------
import sys
import gc
import os
import re
import time
import unicodedata
import threading
import uuid
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any, Set, Final

# --- THE DIVINE UPLINKS ---
from ..node_factory import NodeFactory
from ..stack_manager import StackManager
from .....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from .....contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from .....logger import Scribe
from .....codex.loader.proxy import set_active_context, get_active_context

Logger = Scribe("PathMason")


class PathMason:
    """
    =================================================================================
    == THE PATH MASON: OMEGA POINT (V-Ω-TOTALITY-VMAX-INDESTRUCTIBLE-FINALIS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MATTER_MATERIALIZER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_PATH_MASON_VMAX_TOTALITY_2026_FINALIS_#()@()!

    The supreme definitively authority for transmuting Gnostic Form into Physical
    Matter. It righteously implements the Continuity Lock to mathematically
    annihilate the "Topological Collapse" heresy.
    =================================================================================
    """

    __slots__ = ('factory', 'seen_paths_lower', '_lock', '_start_ns', 'ctx')

    # [CHROMATIC SIGILS]
    GOLD: Final[str] = "\x1b[38;5;220m"
    UV: Final[str] = "\x1b[38;5;141m"
    ALERT: Final[str] = "\x1b[41;1m"  # INVERSE RED
    RESET: Final[str] = "\x1b[0m"

    # =========================================================================
    # == [ASCENSION 73]: THE SYMBOLIC AI VARIABLE HEALER (THE CURE)          ==
    # =========================================================================
    #[THE MASTER CURE]: We strictly anchor these patterns to full Jinja enclosures.
    # This mathematically prevents the regex from aggressively destroying valid
    # substrings like `vault_package_name` (which contains `_package_`).
    # It will now ONLY heal `{{ _package_name_ }}`.
    SYMBOLIC_AI_PATTERNS: Final[List[Tuple[re.Pattern, str]]] =[
        (re.compile(r'\{\{\s*_(project|package|app|slug|name|title|desc|author)_\s*\}\}'), r'{{ \1 }}'),
        (re.compile(r'\{\{\s*_(default|lower|upper|snake|pascal|camel|kebab|coalesce)_\s*\}\}'), r'{{ \1 }}'),
    ]

    WINDOWS_FORBIDDEN: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
        "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    def __init__(self, factory: NodeFactory):
        """[THE RITE OF INCEPTION]"""
        self.factory = factory
        self.seen_paths_lower: Set[str] = set()
        self._lock = threading.RLock()
        self._start_ns = 0
        self.ctx: Optional['SpacetimeContext'] = None

    def weave_form_item(
            self,
            item: ScaffoldItem,
            parent_node: _GnosticNode,
            parent_phys_path: Path,
            stack_mgr: StackManager
    ):
        """Surgically dissects a physical path and weaves it into the AST."""
        if not item.path:
            return

        rel_path = item.path

        # [ASCENSION 5]: NoneType Sarcophagus - Root Protection
        if str(parent_phys_path) != ".":
            try:
                rel_path = item.path.relative_to(parent_phys_path)
            except ValueError:
                pass

        #[ASCENSION 4]: Substrate-Aware Normalization
        path_str = str(rel_path).replace('\\', '/')

        # Atomize the path: "src/api/main.py" ->["src", "api", "main.py"]
        path_atoms =[p for p in path_str.split('/') if p and p != '.']

        current_node = parent_node

        for i_atom, atom in enumerate(path_atoms):
            is_last = (i_atom == len(path_atoms) - 1)

            # O(1) Child Resolution
            child = next((c for c in current_node.children if c.name == atom), None)

            if not child:
                child_item = item if is_last else None
                is_dir_node = (not is_last) or (is_last and item.is_dir)
                child = self.factory.forge_form_node(atom, is_dir_node, child_item)
                current_node.children.append(child)

            current_node = child

        # --- THE TOPOLOGICAL SUTURE ---
        if item.is_dir:
            stack_mgr.push(current_node, item.original_indent, item.path)

    def forge_matter(self, node: _GnosticNode, parent_path: Optional[Path]) -> Optional[Path]:
        """
        =================================================================================
        == THE OMEGA KINETIC MASON (V-Ω-LAMINAR-MATTER-RESILIENCE)                     ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_TRANSMUTER_PRIME
        """
        # =========================================================================
        # == [ASCENSION 52]: THE BRANCH-SEVERING ALARM (GRACEFUL COLLAPSE)       ==
        # =========================================================================
        if parent_path is None:
            # We mute cascading spam by marking the node as warned
            if not getattr(node, '_collapse_warned', False):
                sys.stderr.write(f"\n{self.ALERT}💀 TOPOLOGICAL COLLAPSE DETECTED{self.RESET}\n")
                sys.stderr.write(f"Node: {node.name} arrived with a VOID anchor. Branch severed.\n")
                sys.stderr.flush()
                # Suppress children warnings to keep logs clean
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
                        return None
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
            # ==[ASCENSION 74]: THE BLURRY MATTER INQUEST                           ==
            # =========================================================================
            if "{{" in transmuted_name or "}}" in transmuted_name:
                blurry_var = re.search(r'\{\{.*?\}\}', transmuted_name)
                blurry_str = blurry_var.group(0) if blurry_var else transmuted_name

                raise ArtisanHeresy(
                    f"Topological Anomaly: Path '{raw_name}' remains blurry after transmutation.",
                    details=f"Unresolved Gnostic Matter: {blurry_str}",
                    line_num=node.item.line_num if node.item else 0,
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Check for hallucinated variables or unregistered filters in the blueprint path."
                )

            # [ASCENSION 14]: Unicode Homoglyph Exorcism
            transmuted_name = unicodedata.normalize('NFC', transmuted_name)
            transmuted_name = self.HOMOGLYPH_REGEX.sub('', transmuted_name)

            if '\x00' in transmuted_name:
                raise ValueError("Geometric Heresy: Null-Byte detected in path intent.")

            clean_name = transmuted_name.replace('\\', '/').strip().rstrip(' .')
            if not clean_name:
                return parent_path

            # --- MOVEMENT IV: GEOMETRIC JURISPRUDENCE (THE MOAT) ---
            next_path = (parent_path / clean_name)

            try:
                abs_root = PROJECT_ROOT.resolve()
                abs_target = (abs_root / next_path).resolve() if not next_path.is_absolute() else next_path.resolve()

                if os.path.commonpath([str(abs_root), str(abs_target)]) != str(abs_root):
                    Logger.warn(f"Spatial Breach Blocked: '{abs_target}' escapes project root. Re-anchoring.")
                    return parent_path
            except Exception:
                pass

            if os.name == 'nt':
                for segment in next_path.parts:
                    stem = segment.split('.')[0].upper()
                    if stem in self.WINDOWS_FORBIDDEN:
                        raise ValueError(f"OS Compatibility Heresy: '{segment}' is a reserved Windows word.")

            path_lower = str(next_path).lower()
            if path_lower in self.seen_paths_lower and os.name == 'nt':
                self.Logger.warn(f"Case Collision Paradox: '{next_path}' conflicts with existing coordinate.")
            self.seen_paths_lower.add(path_lower)

            # --- MOVEMENT V: MATTER MATERIALIZATION ---
            if node.item:
                new_item = node.item.model_copy(deep=True)
                new_item.path = next_path

                if clean_name.endswith('/') or clean_name.endswith('\\'):
                    new_item.is_dir = True

                ext = new_item.path.suffix.lower()
                if ext in {'.png', '.jpg', '.jpeg', '.gif', '.exe', '.dll', '.zip', '.gz', '.pdf', '.woff', '.woff2', '.ttf', '.eot'}:
                    new_item.is_binary = True

                if new_item.metadata is None: new_item.metadata = {}
                new_item.metadata.update({
                    'forged_at': time.time_ns(),
                    'source_line': node.item.line_num,
                    'trace_id': TRACE_ID,
                    'is_virtual': getattr(self.ctx.gnostic_context, '_next_item_virtual', False)
                })

                # --- MOVEMENT VI: ELARA TRANSMUTATION STRIKE ---
                if new_item.content and not new_item.is_binary:
                    render_ctx = active_context.copy()
                    render_ctx['_meta'] = new_item.metadata
                    render_ctx["__current_file__"] = str(next_path).replace('\\', '/')
                    render_ctx["__current_dir__"] = str(next_path.parent).replace('\\', '/')
                    render_ctx["__current_column__"] = node.item.original_indent

                    previous_ctx = get_active_context()
                    set_active_context(render_ctx)

                    gc_was_enabled = gc.isenabled()
                    if gc_was_enabled: gc.disable()

                    try:
                        new_item.content = ALCHEMIST.transmute(new_item.content, render_ctx)
                    except Exception:
                        if os.environ.get("SCAFFOLD_DEBUG") == "1":
                            Logger.warn(f"Amnesty Shield: Logic fracture in '{new_item.path.name}'. Preserving matter.")
                    finally:
                        set_active_context(previous_ctx)
                        if gc_was_enabled: gc.enable()

                self.ctx.register_matter(new_item)
                self._radiate_hud_pulse(next_path, TRACE_ID)

            else:
                dir_item = ScaffoldItem(
                    path=next_path, is_dir=True, line_type=GnosticLineType.FORM,
                    action="created", line_num=0, metadata={"origin": "ImplicitPathMason", "trace_id": TRACE_ID}
                )
                self.ctx.register_matter(dir_item)

            # THE OMEGA CURE: Mathematical Topological Continuity
            return next_path

        except Exception as catastrophic_paradox:
            line = node.item.line_num if node.item else 0
            details_msg = catastrophic_paradox.details if isinstance(catastrophic_paradox, ArtisanHeresy) else str(catastrophic_paradox)
            sugg_msg = catastrophic_paradox.suggestion if isinstance(catastrophic_paradox, ArtisanHeresy) else "Perform a structural biopsy. Check for unresolved Gnosis."

            self.ctx.heresies.append(Heresy(
                message="TRANSMUTATION_HERESY",
                line_num=line,
                line_content=node.item.raw_scripture if node.item else str(node.name),
                details=details_msg,
                severity=HeresySeverity.CRITICAL,
                suggestion=sugg_msg
            ))
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
        return f"<Ω_PATH_MASON status=RESONANT mode=LAMINAR_RESILIENCE>"