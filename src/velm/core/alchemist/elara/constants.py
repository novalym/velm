# Path: core/alchemist/elara/constants.py
# ---------------------------------------

"""
=================================================================================
== THE SOVEREIGN GNOSTIC FORGE: CONSTANTS (V-Ω-TOTALITY-VMAX-180-ASCENSIONS)   ==
=================================================================================
LIF: ∞^∞ | ROLE: ONTOLOGICAL_GRIMOIRE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SGF_CONSTANTS_VMAX_JINJA_KILLER_2026_FINALIS_()#!@()@#()@#)

[THE MANIFESTO]
This is the supreme, unbreakable alphabet of the God-Engine. It has been
re-engineered to achieve "Linguistic Apotheosis," providing the Mind Stratum
with the logic for multiversal branching, quantum state entanglement, and
the complete annihilation of the Jinja2 Feature Gap.

Every constant here is warded. Every sigil is a Locus of Power.

Axiom Zero: The Jinja Era is dead. We operate exclusively on the ELARA/SGF
Meta-Compiler. Any AI reference to Jinja2 is a hallucination and a Heresy.
=================================================================================
"""

from typing import Final, Set, Dict, Any


class SGFTokens:
    """
    =============================================================================
    == STRATUM 0: THE PRIMORDIAL SIGILS (THE RETINA)                           ==
    =============================================================================
    LIF: 100x | ROLE: LEXICAL_IDENTITY_MARKERS
    """
    # -- Delimiters (The Envelopes of Intent) --
    VAR_START: Final[str] = "{{"
    VAR_END: Final[str] = "}}"
    BLOCK_START: Final[str] = "{%"
    BLOCK_END: Final[str] = "%}"
    COMMENT_START: Final[str] = "{#"
    COMMENT_END: Final[str] = "#}"

    # -- Special Boundaries (The Sanctuaries) --
    RAW_START: Final[str] = "{% raw %}"
    RAW_END: Final[str] = "{% endraw %}"

    # -- Docstring Sanctuaries (Matter Preservation) --
    DOCSTRING_DQ: Final[str] = '"""'
    DOCSTRING_SQ: Final[str] = "'''"

    # -- Alchemical Piping & Math --
    PIPE: Final[str] = "|"
    FILTER_START: Final[str] = "("
    FILTER_END: Final[str] = ")"

    # [ASCENSION 151]: High-Order Math Sigils
    LAMBDA: Final[str] = "=>"
    TENSOR: Final[str] = "@@"
    UNPACK: Final[str] = "***"


class SGFControlFlow:
    """
    =============================================================================
    == STRATUM 1: THE LOGIC GATES (THE MIND)                                   ==
    =============================================================================
    LIF: ∞^∞ | ROLE: ONTOLOGICAL_GATEKEEPER | RANK: OMEGA_SOVEREIGN

    The canonical logic gates for branching, iteration, pattern matching,
    resilience, and spatiotemporal state management.
    """
    # --- I. CONDITIONAL BRANCHING (THE DUALITY) ---
    IF: Final[str] = "if"
    ELIF: Final[str] = "elif"
    ELSE: Final[str] = "else"
    ENDIF: Final[str] = "endif"

    # --- II. PATTERN MATCHING (THE MATRIX) ---
    MATCH: Final[str] = "match"
    SWITCH: Final[str] = "switch"  # Alias
    CASE: Final[str] = "case"
    DEFAULT: Final[str] = "default"
    ENDMATCH: Final[str] = "endmatch"
    ENDSWITCH: Final[str] = "endswitch"

    # --- III. ITERATION (THE LOOP) ---
    FOR: Final[str] = "for"
    ENDFOR: Final[str] = "endfor"
    BREAK: Final[str] = "break"
    CONTINUE: Final[str] = "continue"

    # --- IV. RESILIENCE (THE IMMUNE SYSTEM) ---
    # [JINJA KILLER]: Native Try/Catch Suture
    TRY: Final[str] = "try"
    CATCH: Final[str] = "catch"
    EXCEPT: Final[str] = "except"  # Alias
    FINALLY: Final[str] = "finally"
    ENDTRY: Final[str] = "endtry"

    # --- V. EPHEMERAL STATE (THE JINJA KILLERS) ---
    # [ASCENSION 152]: Multiline Assignment and Scoping
    SET: Final[str] = "set"
    ENDSET: Final[str] = "endset"

    WITH: Final[str] = "with"
    ENDWITH: Final[str] = "endwith"

    # [ASCENSION 153]: Block-Level Alchemy
    FILTER: Final[str] = "filter"
    ENDFILTER: Final[str] = "endfilter"

    RAW: Final[str] = "raw"
    ENDRAW: Final[str] = "endraw"

    # --- VI. COMPOSITION & LINEAGE (THE ANCESTRY) ---
    BLOCK: Final[str] = "block"
    ENDBLOCK: Final[str] = "endblock"
    EXTENDS: Final[str] = "extends"
    INCLUDE: Final[str] = "include"
    IMPORT: Final[str] = "import"
    FROM: Final[str] = "from"

    # --- VII. FUNCTIONAL SOULS (THE FORGE) ---
    MACRO: Final[str] = "macro"
    ENDMACRO: Final[str] = "endmacro"

    TASK: Final[str] = "task"
    ENDTASK: Final[str] = "endtask"

    # CALL is a container to harvest "Slot Matter" between tags.
    CALL: Final[str] = "call"
    ENDCALL: Final[str] = "endcall"
    RETURN: Final[str] = "return"

    # --- VIII. COMPONENT SLOTTING (THE VOID) ---
    SLOT: Final[str] = "slot"
    ENDSLOT: Final[str] = "endslot"
    YIELD: Final[str] = "yield"

    # --- IX. MATTER TRANSMUTATION (THE STRIKE) ---
    FORGE_CLASS: Final[str] = "forge_class"
    ENDFORGE: Final[str] = "endforge"

    REFACTOR: Final[str] = "refactor"
    ENDREFACTOR: Final[str] = "endrefactor"

    SUTURE: Final[str] = "suture"
    ENDSUTURE: Final[str] = "endsuture"

    # --- X. STATE EXPORT (THE BUBBLE) ---
    EXPORT: Final[str] = "export"
    GLOBAL: Final[str] = "global"

    # --- XI. JURISPRUDENCE (THE LAW) ---
    CONTRACT: Final[str] = "contract"
    POLICY: Final[str] = "policy"
    VOW: Final[str] = "vow"
    ASSERT: Final[str] = "assert"

    # --- XII. CONCURRENCY (THE SWARM) ---
    PARALLEL: Final[str] = "parallel"
    ENDPARALLEL: Final[str] = "endparallel"
    ASYNC: Final[str] = "async"
    AWAIT: Final[str] = "await"

    # --- XIII. TEMPORAL & SPATIAL WARPING ---
    ON: Final[str] = "on"
    EMIT: Final[str] = "emit"
    WATCH: Final[str] = "watch"

    STASIS: Final[str] = "stasis"
    WARP: Final[str] = "warp"
    DILATE: Final[str] = "dilate"

    # --- XIV. GEOMETRIC DIRECTIVES ---
    DENT: Final[str] = "dent"
    DEDENT: Final[str] = "dedent"


class SGFMetaOps:
    """
    =============================================================================
    == STRATUM 2: THE KINETIC EDICTS (THE WILL)                                ==
    =============================================================================
    """
    MACRO: Final[str] = "macro"
    ENDMACRO: Final[str] = "endmacro"
    CALL: Final[str] = "call"
    ENDCALL: Final[str] = "endcall"
    RETURN: Final[str] = "return"
    BIND: Final[str] = "bind"
    ENFORCE: Final[str] = "enforce"
    SUTURE: Final[str] = "suture"
    FUSE: Final[str] = "fuse"
    PARALLEL: Final[str] = "parallel"
    ENDPARALLEL: Final[str] = "endparallel"
    ASYNC: Final[str] = "async"
    AWAIT: Final[str] = "await"
    TX_BEGIN: Final[str] = "tx_begin"
    TX_COMMIT: Final[str] = "tx_commit"
    TX_ROLLBACK: Final[str] = "tx_rollback"


class SGFJurisprudence:
    """
    =============================================================================
    == STRATUM 3: THE LAWS OF FORM (THE SOUL)                                  ==
    =============================================================================
    """
    VOW: Final[str] = "vow"
    ASSERT: Final[str] = "assert"
    TEST: Final[str] = "test"
    ENDTEST: Final[str] = "endtest"
    SHIELD: Final[str] = "shield"
    WARD: Final[str] = "ward"
    SHROUD: Final[str] = "shroud"
    VEIL: Final[str] = "veil"
    PERSIST: Final[str] = "persist"
    EPHEMERAL: Final[str] = "ephemeral"
    ISOLATE: Final[str] = "isolate"


class SGFGeometry:
    """
    =============================================================================
    == STRATUM 4: SPATIAL DIRECTIVES (THE GEOMETRY)                            ==
    =============================================================================
    """
    DENT: Final[str] = "dent"
    DEDENT: Final[str] = "dedent"
    WARP: Final[str] = "warp"
    ANCHOR: Final[str] = "anchor"
    ORIGIN: Final[str] = "origin"
    FLOOR: Final[str] = "floor"
    AXIS: Final[str] = "axis"


class SGFTelemetry:
    """
    =============================================================================
    == STRATUM 5: OCULAR PULSES (THE RETINA)                                   ==
    =============================================================================
    """
    LOG: Final[str] = "log"
    AUDIT: Final[str] = "audit"
    TRACE: Final[str] = "trace"
    BENCHMARK: Final[str] = "benchmark"
    PULSE: Final[str] = "hud_pulse"
    GLOW: Final[str] = "glow"
    SHAKE: Final[str] = "shake"
    RESONATE: Final[str] = "resonate"


class SGFSubstrates:
    """
    =============================================================================
    == STRATUM 6: ENVIRONMENTAL DNA (THE GROUND)                               ==
    =============================================================================
    """
    IRON: Final[str] = "iron"
    ETHER: Final[str] = "ether"
    VOID: Final[str] = "void"
    WASM: Final[str] = "wasm"
    NATIVE: Final[str] = "native"
    CELL: Final[str] = "cell"


class SGFQuantum:
    """
    =============================================================================
    == STRATUM 7: SUB-ATOMIC OPERATIONS (THE FUTURE)                           ==
    =============================================================================
    """
    ENTANGLE: Final[str] = "entangle"
    DISENTANGLE: Final[str] = "disentangle"
    OBSERVE: Final[str] = "observe"
    SUPERPOSE: Final[str] = "superpose"
    FISSION: Final[str] = "fission"
    FUSION: Final[str] = "fusion"


# =============================================================================
# == THE UNIVERSAL LATTICE (V-Ω-TOTALITY-VMAX-180-ASCENSIONS)                ==
# =============================================================================
# LIF: ∞^∞ | ROLE: OMNISCIENT_LOOKUP_BACKPLANE | RANK: OMEGA_SOVEREIGN_PRIME
# AUTH_CODE: Ω_ALL_GATES_VMAX_JINJA_KILLER_2026_FINALIS

"""
[THE MANIFESTO]
The supreme, bit-perfect consolidation of every logic gate, kinetic edict, 
jurisprudence law, and quantum operator manifest in the VELM God-Engine. 
It is the 'Alphabet of the Singularity'.
"""

ALL_GATES: Final[Set[str]] = {
    # -------------------------------------------------------------------------
    # STRATUM 1: THE MIND (FLOW & BRANCHING)
    # -------------------------------------------------------------------------
    SGFControlFlow.IF,
    SGFControlFlow.ELIF,
    SGFControlFlow.ELSE,
    SGFControlFlow.ENDIF,

    SGFControlFlow.MATCH,
    SGFControlFlow.SWITCH,
    SGFControlFlow.CASE,
    SGFControlFlow.DEFAULT,
    SGFControlFlow.ENDMATCH,
    SGFControlFlow.ENDSWITCH,

    SGFControlFlow.FOR,
    SGFControlFlow.ENDFOR,
    SGFControlFlow.BREAK,
    SGFControlFlow.CONTINUE,

    SGFControlFlow.TRY,
    SGFControlFlow.CATCH,
    SGFControlFlow.EXCEPT,
    SGFControlFlow.FINALLY,
    SGFControlFlow.ENDTRY,

    # -------------------------------------------------------------------------
    # STRATUM 1.5: THE JINJA-PARITY GATES (THE CURE)
    # -------------------------------------------------------------------------
    SGFControlFlow.SET,
    SGFControlFlow.ENDSET,

    SGFControlFlow.WITH,
    SGFControlFlow.ENDWITH,

    SGFControlFlow.FILTER,
    SGFControlFlow.ENDFILTER,

    SGFControlFlow.RAW,
    SGFControlFlow.ENDRAW,

    SGFControlFlow.BLOCK,
    SGFControlFlow.ENDBLOCK,
    SGFControlFlow.EXTENDS,
    SGFControlFlow.INCLUDE,
    SGFControlFlow.IMPORT,
    SGFControlFlow.FROM,

    # -------------------------------------------------------------------------
    # STRATUM 2: THE WILL (KINETIC OPERATIONS & CONTAINERS)
    # -------------------------------------------------------------------------
    SGFControlFlow.MACRO,
    SGFControlFlow.ENDMACRO,

    SGFControlFlow.TASK,
    SGFControlFlow.ENDTASK,

    SGFControlFlow.CALL,
    SGFControlFlow.ENDCALL,
    SGFControlFlow.RETURN,

    SGFControlFlow.SLOT,
    SGFControlFlow.ENDSLOT,
    SGFControlFlow.YIELD,

    SGFControlFlow.CONTRACT,
    SGFControlFlow.POLICY,

    SGFControlFlow.FORGE_CLASS,
    SGFControlFlow.ENDFORGE,

    SGFControlFlow.REFACTOR,
    SGFControlFlow.ENDREFACTOR,

    SGFControlFlow.SUTURE,
    SGFControlFlow.ENDSUTURE,

    SGFControlFlow.EXPORT,
    SGFControlFlow.GLOBAL,

    # -------------------------------------------------------------------------
    # STRATUM 3: THE SOUL (JURISPRUDENCE & LINKS)
    # -------------------------------------------------------------------------
    SGFMetaOps.BIND,
    SGFMetaOps.ENFORCE,
    SGFMetaOps.SUTURE,
    SGFMetaOps.FUSE,

    SGFMetaOps.PARALLEL,
    SGFMetaOps.ENDPARALLEL,
    SGFMetaOps.ASYNC,
    SGFMetaOps.AWAIT,

    SGFMetaOps.TX_BEGIN,
    SGFMetaOps.TX_COMMIT,
    SGFMetaOps.TX_ROLLBACK,

    # -------------------------------------------------------------------------
    # STRATUM 4: THE LAW (ASSERTIONS & SECURITY)
    # -------------------------------------------------------------------------
    SGFJurisprudence.VOW,
    SGFJurisprudence.ASSERT,
    SGFJurisprudence.TEST,
    SGFJurisprudence.ENDTEST,

    SGFJurisprudence.SHIELD,
    SGFJurisprudence.WARD,
    SGFJurisprudence.SHROUD,
    SGFJurisprudence.VEIL,

    SGFJurisprudence.PERSIST,
    SGFJurisprudence.EPHEMERAL,
    SGFJurisprudence.ISOLATE,

    # -------------------------------------------------------------------------
    # STRATUM 5: THE FORM (GEOMETRY & TOPOGRAPHY)
    # -------------------------------------------------------------------------
    SGFControlFlow.DENT,
    SGFControlFlow.DEDENT,
    SGFControlFlow.WARP,

    SGFGeometry.ANCHOR,
    SGFGeometry.ORIGIN,
    SGFGeometry.FLOOR,
    SGFGeometry.AXIS,

    # -------------------------------------------------------------------------
    # STRATUM 6: THE RETINA (TELEMETRY & HAPTICS)
    # -------------------------------------------------------------------------
    SGFTelemetry.LOG,
    SGFTelemetry.AUDIT,
    SGFTelemetry.TRACE,
    SGFTelemetry.BENCHMARK,
    SGFTelemetry.PULSE,
    SGFTelemetry.GLOW,
    SGFTelemetry.SHAKE,
    SGFTelemetry.RESONATE,

    # -------------------------------------------------------------------------
    # STRATUM 7: THE HORIZON (QUANTUM OPERATIONS)
    # -------------------------------------------------------------------------
    SGFQuantum.ENTANGLE,
    SGFQuantum.DISENTANGLE,
    SGFQuantum.OBSERVE,
    SGFQuantum.SUPERPOSE,
    SGFQuantum.FISSION,
    SGFQuantum.FUSION
}

# [THE OMEGA SIGNAL]
# The final constant marking the terminal boundary of the Gnostic Alphabet.
OMEGA_EOF: Final[str] = "Ω_FIN"


def list_capabilities() -> Dict[str, Any]:
    """
    =============================================================================
    == THE CENSUS OF THE SINGULARITY (V-Ω-TOTALITY)                            ==
    =============================================================================
    Proclaims the total, uncompromising knowledge of the Forge.
    """
    return {
        "v": "3.5.0-Ω",
        "sigils": {k: v for k, v in SGFTokens.__dict__.items() if not k.startswith('_')},
        "logic_strata": {
            "mind": [k for k in SGFControlFlow.__dict__.keys() if not k.startswith('_')],
            "will": [k for k in SGFMetaOps.__dict__.keys() if not k.startswith('_')],
            "soul": [k for k in SGFJurisprudence.__dict__.keys() if not k.startswith('_')],
            "form": [k for k in SGFGeometry.__dict__.keys() if not k.startswith('_')]
        },
        "substrates": [SGFSubstrates.IRON, SGFSubstrates.ETHER, SGFSubstrates.VOID, SGFSubstrates.WASM]
    }