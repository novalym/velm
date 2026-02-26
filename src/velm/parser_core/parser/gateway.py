# Path: src/velm/parser_core/parser/gateway.py
# --------------------------------------------

"""
=================================================================================
== THE PUBLIC GATEWAY TO THE PARSER (V-Ω-SIX-FOLD-RETURN-ETERNAL)              ==
=================================================================================
LIF: 10,000,000,000

The Unbreakable Bridge between the Mortal Realm and the Gnostic Parser. It now
honors the sacred, three-fold scripture of Will in its final proclamation, and
injects Ambient System Gnosis to annihilate the Time Travel Paradox.
=================================================================================
"""
import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from .engine import ApotheosisParser
from ...contracts.data_contracts import ScaffoldItem, GnosticDossier
from ...contracts.symphony_contracts import Edict


def parse_structure(
        file_path: Path,
        args: Optional[Any] = None,
        pre_resolved_vars: Optional[Dict[str, Any]] = None,
        content_override: Optional[str] = None,
        line_offset: int = 0,
        overrides: Optional[Dict[str, Any]] = None
) -> Tuple[
    'ApotheosisParser', List[ScaffoldItem], List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]], List[
        Edict], Dict[str, Any], GnosticDossier]:
    """The Unbreakable Bridge, its soul now eternally pure."""

    # =========================================================================
    # == THE CURE: AMBIENT GNOSIS SUTURE                                     ==
    # =========================================================================
    # We must ensure trace_id and session_id exist before the parser awakens,
    # otherwise early Jinja renders in the AST Weaver will yield voids.
    safe_vars = pre_resolved_vars.copy() if pre_resolved_vars else {}

    trace_id = None
    session_id = "SCAF-CORE"

    if args:
        trace_id = getattr(args, 'trace_id', None)
        session_id = getattr(args, 'session_id', session_id)

        # Pydantic dict fallback for complex Request vessels
        if not trace_id and hasattr(args, 'metadata') and isinstance(args.metadata, dict):
            trace_id = args.metadata.get('trace_id')

    if not trace_id:
        trace_id = os.environ.get("SCAFFOLD_TRACE_ID") or f"tr-parse-{uuid.uuid4().hex[:6].upper()}"

    safe_vars['trace_id'] = trace_id
    safe_vars['session_id'] = session_id
    # =========================================================================

    # 1. The Divination of Grammar
    grammar_key = 'symphony' if file_path.suffix in ('.symphony', '.arch') else 'scaffold'

    parser = ApotheosisParser(grammar_key=grammar_key)
    if args:
        parser.args = args

    content = content_override if content_override is not None else file_path.read_text(encoding='utf-8')

    # 2. The Sacred Plea to the Engine
    # We pass the newly enriched `safe_vars` here, guaranteeing Nanosecond Zero awareness.
    parser_instance, raw_items, raw_commands, edicts, variables, dossier = parser.parse_string(
        content,
        file_path_context=file_path,
        pre_resolved_vars=safe_vars,
        overrides=overrides,
        line_offset=line_offset
    )

    # 3. The Resolution of Reality (The Logic Weave)
    resolved_items = parser.resolve_reality()

    # 4. === THE DIVINE HEALING: THE RITE OF GNOSTIC PRESERVATION ===
    # The profane unpacking is annihilated. The parser's `post_run_commands` is
    # already a pure list of four-fold Quaternities. We pass it directly, preserving
    # its complete Gnostic soul for all downstream artisans.
    commands = parser.post_run_commands
    # === THE APOTHEOSIS IS COMPLETE. THE CONTRACT IS ETERNAL. ===

    # 5. The Six-Fold Truth is Proclaimed (with the new contract)
    return parser_instance, resolved_items, commands, edicts, variables, dossier