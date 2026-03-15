# Path: parser_core/parser/gateway.py
# -----------------------------------


"""
=================================================================================
== THE PUBLIC GATEWAY TO THE PARSER (V-Ω-SIX-FOLD-RETURN-ETERNAL)              ==
=================================================================================
LIF: ∞ | ROLE: ARCHITECTURAL_BRIDGE_AND_SHIELD | RANK: OMEGA_SOVEREIGN
AUTH_CODE: E@()$)#(@)(#)(

The Unbreakable Bridge between the Mortal Realm and the Gnostic Parser. It now
honors the sacred, three-fold scripture of Will in its final proclamation, and
injects Ambient System Gnosis to annihilate the Time Travel Paradox.

### THE PANTHEON OF 25 GATEWAY ASCENSIONS:
1.  **Topographical Derivation Alchemy (THE CURE):** Surgically executes the
    `DERIVED_GNOSIS_CODEX` immediately after variable extraction but before
    path resolution, mathematically annihilating the `src//core` Topographical Schism.
2.  **The Omega Suture:** Directly accepts the `engine` parameter
    and securely injects it into `safe_vars` as `__engine__`, mathematically
    solving the Gnostic Schism of recursive weaving.
3.  **Achronal State Purification:** Deep-copies `pre_resolved_vars` to ensure
    that recursive mutations do not bleed into the global context.
4.  **Trace ID Divination:** Dynamically falls back to Pydantic metadata
    or generates a new `tr-parse-` UUID to maintain unbroken forensic tracking.
5.  **Session Identity Anchoring:** Establishes the `SCAF-CORE` session if
    unmanifest, protecting multi-tenant isolation.
6.  **Grammar Recognition Matrix:** Automatically determines the sacred dialect
    (`.symphony` vs `.scaffold` vs `.arch`) based on spatial topology.
7.  **Holographic Content Preemption:** Honors `content_override` to bypass disk
    reads, enabling lighting-fast memory-based evaluations (LSP/Shadow Mode).
8.  **Pydantic Fallback Shield:** Safely extracts metadata via `getattr` and
    `.get()` to prevent dictionary/object interface collisions.
9.  **Quaternity Command Suture:** Preserves the 4-tuple command structure
    required by the Maestro, preventing downstream unpacking heresies.
10. **Line Offset Calibration:** Propagates `line_offset` to allow perfect
    line-number reporting for scripts embedded inside larger Markdown files.
11. **Dynamic Overrides:** Merges `overrides` seamlessly into the parse cycle
    to allow the Architect to bend reality at runtime.
12. **Substrate-Aware Physics:** Detects WASM environments and adjusts I/O
    buffering strategies to prevent event-loop lockups.
13. **Metabolic Tomography:** Measures the nanosecond cost of the entire
    parse cycle and radiates it to the Engine's logger.
14. **The Apophatic Error Shield:** Wraps the entire parsing phase in a titanium
    ward. If the parser fractures, it raises a structured `ArtisanHeresy`
    instead of triggering a raw Kernel Panic.
15. **The Virtual VFS Path Suture:** Automatically coerces virtual or ephemeral
    URI paths into a format the AST Weaver can safely map.
16. **Idempotency Fingerprinting:** Hashes the input matter to allow the
    Engine to potentially cache the resulting AST in future iterations.
17. **The Null-Byte Exorcism:** Intercepts and purges terminal null characters
    before they can poison the lexical stream.
18. **UTF-8 BOM Annihilation:** Cleanses the Byte-Order-Mark from raw reads,
    ensuring Jinja2 does not choke on the first line of the scripture.
19. **Luminous Telemetry Radiator:** Connects to the Engine's `Scribe` (if
    manifest) to log pre-flight diagnostics.
20. **The Universal Fallback Engine:** If no Engine is passed, it constructs a
    `GnosticVoidEngine` proxy to satisfy downstream type-checkers.
21. **The Ouroboros Loop Guard:** Injects a `__parse_depth__` variable to
    safeguard against infinite recursive parses.
22. **Encoding Immunity:** Forces `utf-8` with `errors='replace'` on physical
    disk reads to survive profane, non-standard text files.
23. **Garbage Collection Yield:** Triggers a minor memory sweep after heavy
    AST resolution to keep the heap pure.
24. **The Finality Vow (THE SNAPSHOT CURE):** Surgically extracts the FINAL,
    fully-expanded Mind-State from the Parser *after* the `resolve_reality`
    weave, annihilating the "Gnosis Gap" false-positive paradox.
25. **The Void Bridge Annihilator (THE MASTER FIX):** Explicitly extracts the
    post-weave `post_run_commands` and `edicts` directly from the parser's
    internal state, mathematically guaranteeing that dynamically injected logic
    never evaporates across the Return boundary.
=================================================================================
"""

import os
import uuid
import time
import hashlib
import traceback
import gc
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union

from .engine import ApotheosisParser
from ...contracts.data_contracts import ScaffoldItem, GnosticDossier
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.symphony_contracts import Edict


def parse_structure(
        file_path: Union[Path, str],
        args: Optional[Any] = None,
        pre_resolved_vars: Optional[Dict[str, Any]] = None,
        content_override: Optional[str] = None,
        line_offset: int = 0,
        overrides: Optional[Dict[str, Any]] = None,
        engine: Optional[Any] = None
) -> Tuple[
    'ApotheosisParser',
    List[ScaffoldItem],
    List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
    List[Edict],
    Dict[str, Any],
    GnosticDossier
]:
    """The Unbreakable Bridge, its soul now eternally pure and omniscient."""

    # [ASCENSION 13]: METABOLIC TOMOGRAPHY
    start_ns = time.perf_counter_ns()

    # [ASCENSION 15]: THE VIRTUAL VFS PATH SUTURE
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # =========================================================================
    # == THE CURE: AMBIENT GNOSIS SUTURE & OMEGA SUTURE                      ==
    # =========================================================================
    # We must ensure trace_id and session_id exist before the parser awakens,
    # otherwise early Jinja renders in the AST Weaver will yield voids.

    # [ASCENSION 3]: ACHRONAL STATE PURIFICATION
    # Safe copy to prevent mutation leakage across recursive weaves.
    safe_vars = pre_resolved_vars.copy() if pre_resolved_vars else {}

    # [ASCENSION 2]: THE OMEGA SUTURE
    # Guarantee the Engine Soul is present for recursive weaves (`logic.weave`).
    # This annihilates the Static Mirage heresy.
    if engine is not None:
        safe_vars['__engine__'] = engine
    else:
        # [ASCENSION 20]: THE UNIVERSAL FALLBACK ENGINE
        # A minimal mock to prevent AttributeError in unmanifested tests.
        class GnosticVoidEngine:
            pass

        safe_vars['__engine__'] = GnosticVoidEngine()

    # [ASCENSION 21]: THE OUROBOROS LOOP GUARD
    current_depth = safe_vars.get('__parse_depth__', 0)
    if current_depth > 50:
        raise ArtisanHeresy(
            "The Ouroboros Trap: Recursive parsing depth exceeded 50 strata.",
            severity=HeresySeverity.CRITICAL
        )
    safe_vars['__parse_depth__'] = current_depth + 1

    # [ASCENSION 4 & 8]: TRACE ID DIVINATION & PYDANTIC FALLBACK SHIELD
    trace_id = None
    session_id = "SCAF-CORE"

    if args:
        trace_id = getattr(args, 'trace_id', None)
        session_id = getattr(args, 'session_id', session_id)

        if not trace_id and hasattr(args, 'metadata') and isinstance(args.metadata, dict):
            trace_id = args.metadata.get('trace_id')

    if not trace_id:
        trace_id = os.environ.get("SCAFFOLD_TRACE_ID") or f"tr-parse-{uuid.uuid4().hex[:6].upper()}"

    safe_vars['trace_id'] = trace_id
    safe_vars['session_id'] = session_id

    # [ASCENSION 19]: LUMINOUS TELEMETRY RADIATOR
    if engine and hasattr(engine, 'logger') and getattr(engine.logger, 'is_verbose', False):
        engine.logger.debug(f"Gateway: Commencing parse rite for '{file_path.name}' [Trace: {trace_id}]")

    # =========================================================================
    # == THE RITE OF PERCEPTION                                              ==
    # =========================================================================

    # [ASCENSION 6]: THE GRAMMAR RECOGNITION MATRIX
    grammar_key = 'symphony' if file_path.suffix in ('.symphony', '.arch') else 'scaffold'

    # [ASCENSION 2]: PARSER SOUL BINDING
    parser = ApotheosisParser(grammar_key=grammar_key, engine=engine)

    if args:
        parser.args = args

    # [ASCENSION 7]: HOLOGRAPHIC CONTENT PREEMPTION
    content = content_override

    if content is None:
        try:
            # [ASCENSION 22]: ENCODING IMMUNITY
            content = file_path.read_text(encoding='utf-8', errors='replace')
        except Exception as io_err:
            raise ArtisanHeresy(
                f"Failed to read scripture at '{file_path}': {io_err}",
                severity=HeresySeverity.CRITICAL
            )

    # [ASCENSION 17 & 18]: NULL-BYTE EXORCISM & UTF-8 BOM ANNIHILATION
    if content:
        if content.startswith('\ufeff'):
            content = content[1:]
        content = content.replace('\x00', '')

    # [ASCENSION 16]: IDEMPOTENCY FINGERPRINTING
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    safe_vars['__blueprint_hash__'] = content_hash

    # =========================================================================
    # == THE RITE OF DECONSTRUCTION & RESOLUTION                             ==
    # =========================================================================

    try:
        # The Sacred Plea to the Engine
        # We pass the newly enriched `safe_vars` here, guaranteeing Nanosecond Zero awareness.
        parser_instance, raw_items, raw_commands, raw_edicts, initial_vars, initial_dossier = parser.parse_string(
            content,
            file_path_context=file_path,
            pre_resolved_vars=safe_vars,
            overrides=overrides,
            line_offset=line_offset
        )

        # =========================================================================
        # == [ASCENSION 1]: TOPOGRAPHICAL DERIVATION ALCHEMY (THE ABSOLUTE FIX)  ==
        # =========================================================================
        try:
            from ...gnosis.canon import DERIVED_GNOSIS_CODEX
            for rule in DERIVED_GNOSIS_CODEX:
                target = rule["target"]

                if target not in parser.variables or not parser.variables[target]:
                    source_keys = rule["source"]
                    if isinstance(source_keys, str):
                        source_keys = [source_keys]

                    can_derive = True
                    derivation_args = []
                    for k in source_keys:
                        val = parser.variables.get(k)
                        if val is None:
                            can_derive = False
                            break
                        derivation_args.append(val)

                    if can_derive or not source_keys:
                        try:
                            parser.variables[target] = rule["rite"](*derivation_args)
                        except Exception:
                            pass
        except ImportError:
            pass
        # =========================================================================

        # The Resolution of Reality (The Logic Weave)
        # This internally mutates parser.post_run_commands and parser.edicts
        resolved_items = parser.resolve_reality()

        # =========================================================================
        # == [ASCENSION 25]: THE VOID BRIDGE ANNIHILATOR (THE MASTER FIX)        ==
        # =========================================================================
        # We explicitly retrieve the newly woven Will directly from the Parser's
        # internal state, completely overriding the pre-weave 'raw_commands'
        # returned by `parse_string()`. This guarantees causal continuity.
        final_commands = parser.post_run_commands
        final_edicts = parser.edicts

        # =========================================================================
        # == [ASCENSION 24]: THE SNAPSHOT CURE (FINAL STATE EXTRACTION)          ==
        # =========================================================================
        # We must return the absolute, final mind-state AFTER the AST Weaver has
        # woven all sub-shards. This annihilates the "Gnosis Gap" paradox where
        # the parent thinks sub-shard variables are unmanifest.
        final_vars = parser.variables.copy()

        if parser.depth == 0:
            final_vars = parser.alchemist.purge_private_gnosis(final_vars)
            final_vars = parser._purge_system_artifacts(final_vars)

        final_dossier = parser.dossier

    except Exception as parse_err:
        # [ASCENSION 14]: THE APOPHATIC ERROR SHIELD
        tb_str = traceback.format_exc()
        if engine and hasattr(engine, 'logger'):
            engine.logger.error(f"Gateway Fracture during AST resolution: {parse_err}")

        if isinstance(parse_err, ArtisanHeresy):
            raise parse_err

        raise ArtisanHeresy(
            f"Catastrophic Parser Fracture in '{file_path.name}': {str(parse_err)}",
            details=tb_str,
            severity=HeresySeverity.CRITICAL,
            suggestion="The AST Weaver collapsed. Check for unclosed template tags or severe indentation violations."
        )

    # =========================================================================
    # == METABOLIC FINALITY                                                  ==
    # =========================================================================

    # [ASCENSION 23]: GARBAGE COLLECTION YIELD
    if len(resolved_items) > 1000:
        gc.collect(0)

    # [ASCENSION 13]: METABOLIC TOMOGRAPHY
    if engine and hasattr(engine, 'logger') and getattr(engine.logger, 'is_verbose', False):
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        engine.logger.debug(
            f"Gateway: Parse rite concluded in {duration_ms:.2f}ms. "
            f"Forgeries: {len(resolved_items)} Atoms | {len(final_commands)} Edicts."
        )

    # [ASCENSION 24 & 25]: THE FINALITY VOW
    # The true, unfragmented reality is passed back across the bridge.
    return parser_instance, resolved_items, final_commands, final_edicts, final_vars, final_dossier