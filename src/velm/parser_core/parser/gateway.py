# Path: scaffold/parser_core/parser/gateway.py
# --------------------------------------------
"""
=================================================================================
== THE PUBLIC GATEWAY TO THE PARSER (V-Ω-SIX-FOLD-RETURN-ETERNAL)              ==
=================================================================================
LIF: 10,000,000,000

The Unbreakable Bridge between the Mortal Realm and the Gnostic Parser. It now
honors the sacred, three-fold scripture of Will in its final proclamation.
=================================================================================
"""
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
) -> Tuple['ApotheosisParser', List[ScaffoldItem], List[Tuple[str, int, Optional[List[str]]]], List[Edict], Dict[str, Any], GnosticDossier]:
    """The Unbreakable Bridge, its soul now eternally pure."""
    # 1. The Divination of Grammar
    grammar_key = 'symphony' if file_path.suffix in ('.symphony', '.arch') else 'scaffold'

    parser = ApotheosisParser(grammar_key=grammar_key)
    if args: 
        parser.args = args

    content = content_override if content_override is not None else file_path.read_text(encoding='utf-8')

    # 2. The Sacred Plea to the Engine
    parser_instance, raw_items, raw_commands, edicts, variables, dossier = parser.parse_string(
        content,
        file_path_context=file_path,
        pre_resolved_vars=pre_resolved_vars,
        overrides=overrides,
        line_offset=line_offset
    )

    # 3. The Resolution of Reality (The Logic Weave)
    resolved_items = parser.resolve_reality()

    # 4. === THE DIVINE HEALING: THE RITE OF GNOSTIC PRESERVATION ===
    # The profane unpacking is annihilated. The parser's `post_run_commands` is
    # already a pure list of three-fold tuples. We pass it directly, preserving
    # its complete Gnostic soul for all downstream artisans.
    commands = parser.post_run_commands
    # === THE APOTHEOSIS IS COMPLETE. THE CONTRACT IS ETERNAL. ===

    # 5. The Six-Fold Truth is Proclaimed (with the new contract)
    return parser_instance, resolved_items, commands, edicts, variables, dossier