# Path: scaffold/artisans/hover/perception.py
# ------------------------------------------
# LIF: INFINITY | ROLE: OMNISCIENT_STATE_ENGINE | RANK: SOVEREIGN
# auth_code: Ω_PERCEPTION_TOTALITY_V9007_MAESTRO_ASCENDED

import re
from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict, Any, Tuple

# --- THE GEOMETRIC CONSTANTS ---
INDENT_SIZE = 4
SIGIL_COMMENT = '#'
SIGIL_JINJA_OPEN = '{{'
SIGIL_JINJA_CLOSE = '}}'
SIGIL_SOUL_OPS = {'::', '<<', '->', '+=', '-=', '~=', '^='}
SIGIL_HEADERS = {'$$', 'let', 'def', 'const'}

# [ASCENSION 2]: THE MAESTRO LIFECYCLE REGISTRY
MAESTRO_EDICTS = {'post-run', 'pre-run', 'on-undo', 'on-heresy', 'weave', 'trait', 'use', 'contract'}


@dataclass(frozen=True)
class AuraContext:
    """
    =============================================================================
    == THE VESSEL OF AURA (V-Ω-COGNITIVE-STATE-FINALIS)                        ==
    =============================================================================
    An immutable record of the logical spacetime surrounding a coordinate.
    """
    context_type: str  # 'form', 'will', 'logic', 'metadata', 'soul', 'void', 'polyglot'
    parent_block: Optional[str] = None
    ancestry: List[str] = field(default_factory=list)
    depth: int = 0

    # Flags of Essence
    is_inside_jinja: bool = False
    is_inside_string: bool = False
    is_inside_comment: bool = False
    is_inside_header: bool = False
    is_inside_soul: bool = False
    is_inside_vow: bool = False

    # [ASCENSION 2]: Lifecycle Markers
    maestro_edict: Optional[str] = None  # 'post-run', 'on-undo', etc.

    active_language: str = "scaffold"
    local_scope_vars: Set[str] = field(default_factory=set)
    line_idx: int = 0
    char_idx: int = 0


class BlockAuraPerceiver:
    """
    =============================================================================
    == THE AURA SEER (V-Ω-RECURSIVE-CONTEXT-ENGINE-ULTIMA)                     ==
    =============================================================================
    LIF: 10,000,000,000,000 | ROLE: OMNISCIENT_PERCEIVER
    """

    RE_BLOCK_START = re.compile(r'^\s*(@if|@for|@macro|@try|@task|%%|py:|rs:|go:|js:|sh:)\b')
    RE_MAESTRO_FULL = re.compile(r'^\s*%%\s+([\w\-]+)')
    RE_LOOP_VAR = re.compile(r'@for\s+([a-zA-Z_]\w*)\s+in')

    @staticmethod
    def scan(content: str, line_idx: int, char_idx: int = 0) -> AuraContext:
        lines = content.splitlines()
        if not lines or line_idx < 0 or line_idx >= len(lines):
            return AuraContext(context_type='void')

        raw_line = lines[line_idx]
        stripped = raw_line.strip()

        # =========================================================================
        # == MOVEMENT I: COMMENT ABSOLUTISM (THE CURE)                           ==
        # =========================================================================
        # We perform a character-by-character scan to find the TRUE comment horizon.

        in_string_char: Optional[str] = None
        in_comment: bool = False
        comment_start_idx = -1
        jinja_depth = 0

        cursor_in_string = False
        cursor_in_comment = False
        cursor_in_jinja = False

        soul_op_idx = -1
        vow_op_idx = -1

        for i, char in enumerate(raw_line):
            # 1. State Capture at Cursor
            if i == char_idx:
                cursor_in_string = (in_string_char is not None)
                cursor_in_comment = in_comment
                cursor_in_jinja = (jinja_depth > 0)

            # 2. Comment Absolutism Gating
            if in_comment: continue

            # 3. String Physics
            if in_string_char:
                if char == in_string_char and (i == 0 or raw_line[i - 1] != '\\'):
                    in_string_char = None
            else:
                if char in ('"', "'"):
                    # Check for Triple Quotes
                    if i + 2 < len(raw_line) and raw_line[i:i + 3] in ('"""', "'''"):
                        # Simplified for line-perception, treat as standard string start
                        in_string_char = char
                    else:
                        in_string_char = char

                # 4. The Comment Horizon [ASCENSION 1]
                elif char == SIGIL_COMMENT:
                    in_comment = True
                    comment_start_idx = i
                    if char_idx >= i: cursor_in_comment = True

                # 5. Jinja & Operators
                elif char == '{' and i + 1 < len(raw_line) and raw_line[i + 1] == '{':
                    jinja_depth += 1
                elif char == '}' and i + 1 < len(raw_line) and raw_line[i + 1] == '}':
                    jinja_depth = max(0, jinja_depth - 1)

                if i + 1 < len(raw_line):
                    chunk = raw_line[i:i + 2]
                    if chunk in SIGIL_SOUL_OPS:
                        if soul_op_idx == -1: soul_op_idx = i
                    if chunk == '??':
                        if vow_op_idx == -1: vow_op_idx = i

        # Handle EOL Cursor
        if char_idx >= len(raw_line):
            cursor_in_comment = in_comment
            cursor_in_string = (in_string_char is not None)

        # [THE CURE]: If cursor is in comment, we RETURN IMMEDIATELY.
        if cursor_in_comment:
            is_pragma = raw_line[comment_start_idx:].strip().startswith('# @')
            return AuraContext(
                context_type='metadata_pragma' if is_pragma else 'metadata',
                is_inside_comment=True,
                line_idx=line_idx,
                char_idx=char_idx
            )

        # =========================================================================
        # == MOVEMENT II: CONTEXT TRIAGE                                         ==
        # =========================================================================
        is_inside_soul = (soul_op_idx != -1 and char_idx > soul_op_idx)
        is_inside_vow = (vow_op_idx != -1 and char_idx > vow_op_idx)

        context_type = 'form'
        maestro_edict = None

        # 1. MAESTRO AWARENESS [ASCENSION 2]
        maestro_match = BlockAuraPerceiver.RE_MAESTRO_FULL.match(raw_line)
        if maestro_match:
            context_type = 'will'
            maestro_edict = maestro_match.group(1) if maestro_match.group(1) in MAESTRO_EDICTS else None

        elif is_inside_soul:
            context_type = 'soul'
        elif is_inside_vow or stripped.startswith(('>>', '!!')):
            context_type = 'will'
        elif stripped.startswith('@'):
            context_type = 'logic'

        is_definition = any(stripped.startswith(s) for s in SIGIL_HEADERS)

        # =========================================================================
        # == MOVEMENT III: ANCESTRAL DNA THREADING                               ==
        # =========================================================================
        raw_indent = len(raw_line) - len(raw_line.lstrip())
        current_depth = raw_indent // INDENT_SIZE

        parent_block = None
        ancestry = []
        active_language = "scaffold"
        local_vars = set()

        scan_indent = raw_indent
        for i in range(line_idx - 1, -1, -1):
            line = lines[i]
            s_line = line.strip()
            if not s_line or s_line.startswith(SIGIL_COMMENT): continue

            l_indent = len(line) - len(s_line)

            if l_indent < scan_indent:
                scan_indent = l_indent

                # Detect Maestro Parent
                m_parent = BlockAuraPerceiver.RE_MAESTRO_FULL.match(s_line)
                if m_parent:
                    edict_name = m_parent.group(1)
                    ancestry.insert(0, f"%% {edict_name}")
                    if not parent_block: parent_block = f"%% {edict_name}"
                    if not maestro_edict: maestro_edict = edict_name
                    context_type = 'will'

                # Detect Logic Parent
                match = BlockAuraPerceiver.RE_BLOCK_START.match(s_line)
                if match:
                    b_type = match.group(1)
                    ancestry.insert(0, b_type)
                    if not parent_block: parent_block = b_type
                    if b_type == "@for":
                        lm = BlockAuraPerceiver.RE_LOOP_VAR.search(s_line)
                        if lm: local_vars.add(lm.group(1))
                    if b_type.endswith(':'): active_language = b_type.rstrip(':')

                if any(m in s_line for m in ('>>', '??', '%% symphony')):
                    if context_type == 'form': context_type = 'will'

                if l_indent == 0: break

        return AuraContext(
            context_type=context_type,
            parent_block=parent_block,
            ancestry=ancestry,
            depth=current_depth,
            is_inside_jinja=cursor_in_jinja,
            is_inside_string=cursor_in_string,
            is_inside_comment=False,
            is_inside_header=is_definition,
            is_inside_soul=is_inside_soul,
            is_inside_vow=is_inside_vow,
            maestro_edict=maestro_edict,  # [WIRED]
            active_language=active_language,
            local_scope_vars=local_vars,
            line_idx=line_idx,
            char_idx=char_idx
        )

# === SCRIPTURE SEALED: THE MAESTRO IS MANIFEST ===