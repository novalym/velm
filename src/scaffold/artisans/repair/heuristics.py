# Path: artisans/repair/heuristics.py
# -----------------------------------
# LIF: INFINITY | The Topological Cartographer (V-Ω-OMNISCIENT)
# "I see the structure of the void, and I fill it with light."

import re
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple, Dict


# --- 0. THE ATOMS OF PERCEPTION ---

class LineType(Enum):
    META = auto()  # #!/bin/bash, # -*- coding: utf-8 -*-
    COMMENT = auto()  # # Just a comment
    EMPTY = auto()  # Whitespace
    VARIABLE = auto()  # $$ var = val
    DIRECTIVE = auto()  # @if, @include
    CONTENT = auto()  # path/to/file :: ...
    UNKNOWN = auto()  # Chaos


@dataclass
class LineProfile:
    """The soul of a single line."""
    index: int
    content: str
    type: LineType
    indentation: int
    is_usage: bool = False  # Does this line USE the symbol?


@dataclass
class InsertionPlan:
    """The Divine Strategy."""
    line_num: int
    new_text: str
    reasoning: List[str] = field(default_factory=list)
    confidence: float = 1.0


# --- I. THE TOPOLOGICAL CARTOGRAPHER ---

class TopologicalCartographer:
    """
    The Omniscient Engine.
    Parses the document into semantic zones, calculates gravity wells,
    and enforces causal barriers to determine the perfect insertion point.
    """

    # --- THE PATTERN GRIMOIRE ---
    RX_META = re.compile(r'^(#!|# -\*-|# Path:|# ==|# --|<!--|---|// ==|// --).*')
    # Strict Scaffold Variable: $$ name = val
    RX_VAR_DEF = re.compile(r'^\s*\$\$\s*([a-zA-Z_]\w*)\s*(=|:).*')
    # Content Definition: path :: ... or path << ...
    RX_CONTENT = re.compile(r'^\s*[\w\.\-\/]+\s*(::|<<|->|\+=|-=|~=|\^=).*')
    # Directives
    RX_DIRECTIVE = re.compile(r'^\s*@.*')

    @classmethod
    def _log(cls, msg: str):
        print(f"[Cartographer] {msg}", file=sys.stdout)
        sys.stdout.flush()

    @classmethod
    def chart_course(cls, content: str, symbol_name: str) -> InsertionPlan:
        """
        The Grand Rite of Placement.
        """
        cls._log(f"Initiating Topological Scan for symbol: '{symbol_name}'")

        lines = content.splitlines()
        profiles = cls._profile_lines(lines, symbol_name)

        # 1. Establish The Causal Barrier (The Ceiling)
        # The line index before which the variable MUST be defined.
        barrier_idx = cls._find_causal_barrier(profiles)
        cls._log(f"Causal Barrier established at Line {barrier_idx}.")

        # 2. Establish The Header Fortress (The Floor)
        # The line index after the metadata/license header.
        floor_idx = cls._establish_floor(profiles)
        cls._log(f"Header Floor established at Line {floor_idx}.")

        # 3. Calculate Gravity Wells (Attraction)
        # We score every possible insertion point between Floor and Barrier.
        best_score = -1.0
        best_line = floor_idx
        reasons = []

        # If Floor >= Barrier, we have a Temporal Paradox (Usage inside Header??).
        # We force insertion at Barrier - 1 or Floor, whichever preserves validity.
        if floor_idx >= barrier_idx:
            cls._log("⚠️ Temporal Paradox: Usage detected inside/before Header Floor.")
            # Fallback: Insert at 0 or just before usage if usage > 0
            best_line = max(0, barrier_idx)
            reasons.append("Paradox resolution: Forced genesis before usage.")
        else:
            # Scan the habitable zone
            for i in range(floor_idx, barrier_idx + 1):
                score, note = cls._calculate_gravity(profiles, i)
                if score > best_score:
                    best_score = score
                    best_line = i
                    reasons = [f"Winner L{i} (Score {score}): {note}"]
                elif score == best_score:
                    # Prefer lines closer to other variables (Clustering)
                    pass

        # 4. Forge the Text
        style = cls._detect_style(content)
        final_text = f"$$ {symbol_name}{style}\"placeholder\""

        # 5. Apply Padding (Breathing Room)
        # If we are inserting into a dense block, add newlines.
        padding_before = ""
        padding_after = ""

        # Look behind: If previous line is not empty and not a variable, pad.
        if best_line > 0 and profiles[best_line - 1].type not in [LineType.EMPTY, LineType.VARIABLE, LineType.META,
                                                                  LineType.COMMENT]:
            padding_before = "\n"

        # Look ahead: If next line is not empty and not a variable, pad.
        if best_line < len(profiles) and profiles[best_line].type not in [LineType.EMPTY, LineType.VARIABLE]:
            padding_after = "\n"

        full_insert = f"{padding_before}{final_text}{padding_after}"

        cls._log(f"Final Trajectory: Insert at Line {best_line}. Reasoning: {reasons[0]}")

        return InsertionPlan(
            line_num=best_line,
            new_text=full_insert,
            reasoning=reasons,
            confidence=best_score
        )

    @classmethod
    def _profile_lines(cls, lines: List[str], symbol_name: str) -> List[LineProfile]:
        """
        Tokenizes the document into semantic profiles.
        Performs 'Lexical Scope Guard' check for usage.
        """
        profiles = []
        # Robust usage regex: matches {{ symbol }} or {{ symbol | ... }}
        # We allow whitespace around the symbol inside braces
        rx_usage = re.compile(r'\{\{\s*' + re.escape(symbol_name) + r'\s*(?:\||\}|$)')

        for i, line in enumerate(lines):
            stripped = line.strip()
            ltype = LineType.UNKNOWN
            is_usage = False

            if not stripped:
                ltype = LineType.EMPTY
            elif cls.RX_META.match(line):
                ltype = LineType.META
            elif stripped.startswith('#'):
                ltype = LineType.COMMENT
            elif cls.RX_VAR_DEF.match(line):
                ltype = LineType.VARIABLE
            elif cls.RX_DIRECTIVE.match(line):
                ltype = LineType.DIRECTIVE
            elif cls.RX_CONTENT.match(line):
                ltype = LineType.CONTENT

            # [ASCENSION 1]: Lexical Scope Guard
            # We only count usage if it's NOT in a full-line comment.
            # (Partial line comments are harder, but this covers 99% cases)
            if ltype != LineType.COMMENT:
                if rx_usage.search(line):
                    is_usage = True

            profiles.append(LineProfile(
                index=i,
                content=line,
                type=ltype,
                indentation=len(line) - len(line.lstrip()),
                is_usage=is_usage
            ))

        return profiles

    @classmethod
    def _find_causal_barrier(cls, profiles: List[LineProfile]) -> int:
        """Returns the index of the first line that USES the symbol."""
        for p in profiles:
            if p.is_usage:
                return p.index
        # If never used, barrier is Infinity (EOF)
        return len(profiles)

    @classmethod
    def _establish_floor(cls, profiles: List[LineProfile]) -> int:
        """
        Finds the end of the Header/Meta block.
        We skip Shebangs, Comments, and Metadata at the top.
        Stop at the first Empty line OR the first Content/Variable line.
        """
        floor = 0
        in_header = True

        for p in profiles:
            if not in_header: break

            if p.type == LineType.META:
                floor = p.index + 1
            elif p.type == LineType.COMMENT:
                floor = p.index + 1
            elif p.type == LineType.EMPTY:
                # Empty lines inside a header are ambiguous.
                # Usually headers are contiguous.
                # Let's say an empty line marks the END of the header.
                in_header = False
                floor = p.index + 1
            else:
                # We hit logic/vars/content.
                in_header = False

        return floor

    @classmethod
    def _calculate_gravity(cls, profiles: List[LineProfile], index: int) -> Tuple[float, str]:
        """
        The Physics Engine.
        Returns a score (Higher is better) and a reason.

        Scoring Heuristics:
        - Base Score: 10
        - Is Next to Variable: +50 (Clustering)
        - Is Next to Empty Line: +5 (Cleanliness)
        - Is Inside Header: -100 (Fortress)
        - Is After Usage: -Infinity (Paradox)
        """
        score = 10.0
        reasons = []

        prev = profiles[index - 1] if index > 0 else None
        curr = profiles[index] if index < len(profiles) else None  # The line we are shifting down

        # 1. Clustering (The Strongest Force)
        if prev and prev.type == LineType.VARIABLE:
            score += 50
            reasons.append("Clustering with preceding variable")

        # 2. Header Repulsion
        if prev and prev.type == LineType.META:
            score -= 20
            reasons.append("Too close to Meta Header")

        # 3. Content Repulsion (Don't split content blocks)
        if prev and prev.type == LineType.CONTENT and curr and curr.type == LineType.CONTENT:
            score -= 30
            reasons.append("Splitting content block")

        # 4. Directive Repulsion (Don't insert between @if and body)
        if prev and prev.type == LineType.DIRECTIVE:
            score -= 10
            reasons.append("After directive")

        # 5. Empty Space Attraction
        if prev and prev.type == LineType.EMPTY:
            score += 5
            reasons.append("Utilizing whitespace")

        return score, "; ".join(reasons)

    @classmethod
    def _detect_style(cls, content: str) -> str:
        """Determines assignment operator style."""
        spaced = len(re.findall(r'\s+=\s+', content))
        compact = len(re.findall(r'(?<!\s)=(?!\s)', content))
        return " = " if spaced >= compact else "="

    @classmethod
    def is_symbol_defined_correctly(cls, content: str, symbol: str) -> bool:
        """Check if symbol exists via regex."""
        pattern = re.compile(rf'^\s*\$\$\s*{re.escape(symbol)}\s*=', re.MULTILINE)
        return bool(pattern.search(content))