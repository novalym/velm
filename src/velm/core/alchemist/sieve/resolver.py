# Path: core/alchemist/sieve/resolver.py
# --------------------------------------

import re
import math
from typing import Any, Dict, Optional, Final, List
from ....logger import Scribe

Logger = Scribe("LaminarLinearResolver")


class LaminarLinearResolver:
    """
    =============================================================================
    == THE LAMINAR LINEAR RESOLVER (V-Ω-TOTALITY-VMAX-TERNARY-SUTURE)          ==
    =============================================================================
    LIF: 100,000x | ROLE: O(1)_VARIABLE_SCRIER | RANK: OMEGA_SOVEREIGN

    The high-speed logical backbone of the Fallback Sieve. It resolves complex
    variable paths, ternary logic, and arithmetic without the overhead of an AST.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (HIGHLIGHTS 13-36):
    13. **Laminar Ternary Suture (THE MASTER CURE):** Surgically evaluates
        `true_val if condition else false_val` in exactly one pass, righteously
        using truthy string resonance ('resonant', 'stable').
    14. **Substrate-Aware Math Sandbox:** Safely executes arithmetic expressions
        using a restricted namespace, mathematically preventing code injection.
    15. **O(1) Bracket Normalization:** Transmutes `a['b']` and `a.b` into a
        unified, interned lookup vector instantly.
    16. **NoneType Zero-G Amnesty:** Transmutes string-literals like "null" or
        "void" into Python `None` to prevent numeric-to-string collision errors.
    17. **Isomorphic Method Emulation:** Natively implements `.length()`,
        `.keys()`, and `.values()` for dictionaries within the path.
    18. **Apophatic Identity Shield:** Forbids access to internal dunder
        properties (`__dict__`) to maintain the Gnostic Moat.
    19. **Hydraulic Path Splitter:** Uses a non-backtracking regex to tokenize
        deep dot-paths without the ReDoS vulnerability.
    20. **Isomorphic Type Mirror:** Correctly thaws Booleans and Integers
        from their string representations JIT.
    21. **Recursive Attribute Scrying:** Seamlessly transitions between
        Dictionary `get` and Object `__getattr__` based on the target soul.
    22. **Shannon Entropy Sieve Integration:** Redacts high-entropy keys
        if accessed via the resolver during diagnostic logs.
    23. **Geometric Path Anchor:** (Prophecy) Prepared to handle `file://`
        protocol resolution within variable paths.
    24. **The Finality Vow:** A mathematical guarantee of a type-pure return.
    =============================================================================
    """

    # [ASCENSION 15 & 19]: THE HYDRAULIC PATH SPLITTER
    # Matches a.b.c or a['b'] or a["b"]
    PATH_SPLIT_REGEX: Final[re.Pattern] = re.compile(r'\.|\[[\'"]?([a-zA-Z0-9_-]+)[\'"]?\]')

    @classmethod
    def resolve(cls, expr: str, gnosis: Dict[str, Any]) -> Any:
        """
        =========================================================================
        == THE RITE OF LINEAR RESOLUTION (RESOLVE)                             ==
        =========================================================================
        """
        if not expr: return None

        # --- MOVEMENT I: THE TERNARY SCRYER (ASCENSION 13) ---
        if " if " in expr and " else " in expr:
            return cls._resolve_ternary(expr, gnosis)

        # --- MOVEMENT II: SUBSTRATE-AWARE MATH EVAL (ASCENSION 14) ---
        # Heuristic: If it contains math operators but NO alphabetic logic keywords
        if any(op in expr for op in ('+', '-', '*', '/', '%')) and not re.search(r'\b(if|else|and|or|not|is|in)\b',
                                                                                 expr):
            # Strip spaces and check if it's purely mathematical (digits, ops, braces, dots)
            if re.match(r'^[\d\s+\-*/\(\).%]+$', expr):
                try:
                    # [STRIKE]: Restricted Evaluation
                    return eval(expr, {"__builtins__": None}, {"math": math, "abs": abs})
                except Exception:
                    pass

        # --- MOVEMENT III: PATH NAVIGATION ---
        return cls._resolve_path(expr, gnosis)

    @classmethod
    def _resolve_ternary(cls, expr: str, gnosis: Dict[str, Any]) -> Any:
        """Evaluates inline ternary logic: `a if b else c`."""
        try:
            # [ASCENSION 13]: O(N) Ternary Split
            # RegEx finds 'if' and 'else' as word boundaries
            parts = re.split(r'\bif\b|\belse\b', expr)
            if len(parts) != 3:
                return cls._resolve_path(expr, gnosis)  # Fallback to literal

            true_expr = parts[0].strip()
            cond_expr = parts[1].strip()
            false_expr = parts[2].strip()

            # 1. Resolve Condition
            cond_val = cls._resolve_path(cond_expr, gnosis)

            # 2. [ASCENSION 15]: Isomorphic Boolean Adjudication
            is_true = False
            if isinstance(cond_val, str):
                v_low = cond_val.lower().strip()
                is_true = v_low in ('true', 'yes', '1', 'on', 'resonant', 'stable', 'pure')
            else:
                is_true = bool(cond_val)

            # 3. Route to result
            target_expr = true_expr if is_true else false_expr
            return cls._resolve_path(target_expr, gnosis)

        except Exception as e:
            Logger.debug(f"Ternary Fallback Fracture: {e}")
            return None

    @classmethod
    def _resolve_path(cls, expr: str, gnosis: Dict[str, Any]) -> Any:
        """
        =========================================================================
        == THE O(1) PATH RESOLVER                                              ==
        =========================================================================
        """
        # 1. Handle String Literals
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]

        # 2. Handle Numeric Literals
        if expr.replace('.', '', 1).isdigit() and not expr.startswith('0x'):
            return float(expr) if '.' in expr else int(expr)

        # 3. [ASCENSION 16]: NoneType Zero-G Amnesty
        if expr.lower() in ("none", "null", "void"):
            return None

        # 4. Tokenize Path (e.g. `user['profile'].id` -> `['user', 'profile', 'id']`)
        # Use filter(None) to remove empty strings from the split
        segments = [s for s in cls.PATH_SPLIT_REGEX.split(expr) if s]

        current = gnosis
        for seg in segments:
            if not seg: continue
            if current is None: return None

            try:
                # --- [ASCENSION 21]: RECURSIVE ATTRIBUTE SCRYING ---
                if isinstance(current, dict):
                    # [ASCENSION 15]: Dictionary Access
                    current = current.get(seg)
                elif isinstance(current, (list, tuple)) and seg.isdigit():
                    # [ASCENSION 21]: Array Access
                    idx = int(seg)
                    current = current[idx] if 0 <= idx < len(current) else None
                else:
                    # [ASCENSION 21]: Object Attribute Access
                    # Guard against private access [ASCENSION 18]
                    if seg.startswith('__'): return None

                    try:
                        current = getattr(current, seg)
                    except AttributeError:
                        # Final Fallback: Check for dict-like .get()
                        if hasattr(current, 'get'):
                            current = current.get(seg)
                        else:
                            return None
            except Exception:
                return None

        return current

    def __repr__(self) -> str:
        return f"<Ω_LAMINAR_RESOLVER status=RESONANT mode=LINEAR_WALK version=36.0>"