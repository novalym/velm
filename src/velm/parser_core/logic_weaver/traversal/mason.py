# Path: src/velm/parser_core/logic_weaver/traversal/mason.py
# ----------------------------------------------------------


import os
import re
import time
import unicodedata
from pathlib import Path
from typing import Optional, Dict, Any, List, Set, Final

from .context import SpacetimeContext
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....logger import Scribe
from ....utils import to_snake_case

Logger = Scribe("GeometricMason")


class GeometricMason:
    """
    =================================================================================
    == THE GEOMETRIC MASON (V-Ω-TOTALITY-V25000-OMNISCIENT-ARCHITECT)              ==
    =================================================================================
    LIF: ∞ | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MASON_V25000_DYNAMIC_TOPOLOGY_FINALIS_2026

    The Sovereign Artisan of Form. It transmutes abstract AST nodes into concrete
    Reality Paths. It understands that a path is not just a string; it is a
    Logic Gate, a Variable Container, and a Security Boundary.
    """

    # [ASCENSION 7]: THE SANITIZER
    ILLEGAL_CHARS: Final[re.Pattern] = re.compile(r'[<>:"|?*]')

    # [ASCENSION 2]: CONDITIONAL EXISTENCE
    # Matches "path/to/file @if(condition)"
    CONDITIONAL_PATH_REGEX: Final[re.Pattern] = re.compile(r'^(?P<path>.*)\s+@if\((?P<cond>.*)\)$')

    def __init__(self, ctx: SpacetimeContext):
        self.ctx = ctx
        self.seen_paths_lower: Set[str] = set()

    def forge_matter(self, node: _GnosticNode, parent_path: Path) -> Optional[Path]:
        """
        [THE RITE OF FORM]
        Transmutes the node name, checks for collisions, resolves conditions,
        and harvests the item into the Spacetime Context.
        """
        start_ns = time.perf_counter_ns()

        try:
            # =========================================================================
            # == [ASCENSION 1]: THE MACRO CONTEXT SUTURE                             ==
            # =========================================================================
            # We must forge a specialized context for this specific atom.
            # We start with the Global Truth.
            active_context = self.ctx.gnostic_context.raw.copy()

            # If the item carries the DNA of a Macro, we inject its local variables.
            if node.item and node.item.semantic_selector:
                macro_ctx = node.item.semantic_selector.get("_macro_ctx")
                if macro_ctx:
                    active_context.update(macro_ctx)

            # [ASCENSION 22]: ENVIRONMENT BRIDGE
            active_context['env'] = os.environ

            # =========================================================================
            # == [ASCENSION 2]: CONDITIONAL EXISTENCE CHECK                          ==
            # =========================================================================
            raw_name = node.name
            conditional_match = self.CONDITIONAL_PATH_REGEX.match(raw_name)

            if conditional_match:
                path_part = conditional_match.group("path")
                condition = conditional_match.group("cond")

                # Evaluate condition
                # We use the Alchemist to render it as a boolean string first
                # (Simple check: "true" or "false" or "1" or "0")
                # For complex logic, we rely on the Jinja engine returning "True" string.
                try:
                    eval_result = self.ctx.alchemist.transmute(f"{{{{ {condition} }}}}", active_context)
                    if eval_result.lower() not in ('true', 'yes', '1', 'on'):
                        Logger.verbose(
                            f"   -> Conditional Skip: '{path_part}' (Condition: {condition} -> {eval_result})")
                        return None  # Skip this node and its children
                except Exception as e:
                    Logger.warn(f"Conditional Path Error: {e}. Skipping.")
                    return None

                raw_name = path_part.strip()

            # =========================================================================
            # == PHASE I: ALCHEMICAL TRANSMUTATION                                   ==
            # =========================================================================

            # 1. Transmute the Name
            transmuted_name = self.ctx.alchemist.transmute(raw_name, active_context)

            # [ASCENSION 21]: UNICODE NORMALIZATION
            transmuted_name = unicodedata.normalize('NFC', transmuted_name)

            # [ASCENSION 7]: SANITIZATION
            if self.ILLEGAL_CHARS.search(transmuted_name) and os.name == 'nt':
                # Only warn on Windows, allow on Linux/Mac if valid there
                Logger.warn(f"Path '{transmuted_name}' contains characters illegal on Windows.")

            # [ASCENSION 13]: NULL-BYTE PHALANX
            if '\0' in transmuted_name:
                raise ValueError("Null byte detected in path.")

            clean_name = transmuted_name.strip().strip('/').strip('\\')

            # [ASCENSION 23]: FALLBACK STRATEGIST
            if not clean_name:
                return parent_path

            # [ASCENSION 5]: SYMLINK RESOLVER
            # Check if name contains "->" which implies a link
            # But wait, symlinks are usually defined as `link -> target`.
            # If the resolved name has it, we handle it?
            # Or is that handled by the Lexer? Lexer handles `->` token.
            # Here we just construct the path.

            next_path = parent_path / clean_name

            # =========================================================================
            # == PHASE II: MATERIALIZATION & CLONING                                 ==
            # =========================================================================
            if node.item:
                full_path_str = str(next_path).replace('\\', '/')
                current_line = node.item.line_num

                # [ASCENSION 6 & 17]: ATOMIC DEDUPLICATION & IDEMPOTENCY
                # We check for exact string matches AND case-insensitive collisions
                path_lower = full_path_str.lower()

                if full_path_str in self.ctx.materialized_paths:
                    original_line = self.ctx.materialized_paths[full_path_str]
                    Logger.warn(
                        f"Collision Detected: '{full_path_str}' (L{current_line}) "
                        f"overwrites previous definition from L{original_line}."
                    )
                elif path_lower in self.seen_paths_lower and os.name == 'nt':
                    Logger.warn(f"Case Collision Warning: '{full_path_str}' conflicts with existing path on Windows.")

                self.ctx.materialized_paths[full_path_str] = current_line
                self.seen_paths_lower.add(path_lower)

                # [ASCENSION 19]: DEEP COPY SHIELD
                # Deep copy to prevent contaminating the original AST during multi-pass weaving
                new_item = node.item.model_copy(deep=True)
                new_item.path = next_path

                # [ASCENSION 14]: TRAILING SLASH DECREE
                if transmuted_name.endswith(('/', '\\')):
                    new_item.is_dir = True

                # [ASCENSION 10]: BINARY DIVINER
                if new_item.path.suffix.lower() in ('.png', '.jpg', '.exe', '.dll', '.so', '.zip', '.gz'):
                    new_item.is_binary = True

                # [ASCENSION 18]: METADATA GRAFT
                if new_item.metadata is None: new_item.metadata = {}
                new_item.metadata['forged_at'] = time.time()
                new_item.metadata['source_line'] = current_line

                # =========================================================================
                # == PHASE III: CONTENT ALCHEMY                                          ==
                # =========================================================================

                # 3. Alchemical Transmutation of the File Content
                if new_item.content:
                    # [ASCENSION 9]: CONTENT INJECTION SUTURE
                    # We inject the item's own metadata (like permissions) into the context
                    # so the template can reference `{{ _meta.permissions }}` if needed.
                    render_ctx = active_context.copy()
                    render_ctx['_meta'] = new_item.metadata

                    new_item.content = self.ctx.alchemist.transmute(new_item.content, render_ctx)

                # [ASCENSION 11]: SEED RESOLUTION
                if new_item.seed_path:
                    # Resolve variables in the seed path itself
                    seed_str = str(new_item.seed_path)
                    if "{{" in seed_str:
                        new_item.seed_path = Path(self.ctx.alchemist.transmute(seed_str, active_context))

                # 4. Harvest the Item
                self.ctx.visibility_map[node.item.line_num] = True
                self.ctx.items.append(new_item)

                # Register in the shared context for the `ensure_structure` validators
                self.ctx.gnostic_context.register_virtual_file(next_path)

            # [ASCENSION 12]: FORENSIC LOGGING
            if Logger.is_verbose:
                duration = (time.perf_counter_ns() - start_ns) / 1_000_000
                Logger.debug(f"   -> Forged: {next_path} ({duration:.2f}ms)")

            return next_path

        except Exception as e:
            Logger.error(f"Form Paradox on '{node.name}': {e}")

            line = node.item.line_num if node.item else 0
            content = node.item.raw_scripture if node.item else node.name

            self.ctx.heresies.append(Heresy(
                message="TRANSMUTATION_HERESY",
                line_num=line,
                line_content=content,
                details=str(e),
                severity=HeresySeverity.CRITICAL
            ))

            return parent_path

    def __repr__(self) -> str:
        return f"<Ω_GEOMETRIC_MASON paths_forged={len(self.ctx.materialized_paths)}>"