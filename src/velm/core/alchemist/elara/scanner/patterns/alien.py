# Path: core/alchemist/elara/scanner/patterns/alien.py
# ----------------------------------------------------

import re
from typing import Final

GNOSTIC_DOMAINS: Final[str] = (
    r'(?:logic|math|os|time|str|sec|cloud|ui|ai|auth|id|infra|'
    r'integration|iris|mock|monitor|neuron|ops|policy|pulse|'
    r'shadow|sim|soul|stack|struct|test|topo|veritas|path|default|coalesce)'
)

GNOSTIC_PREFIX: Final[str] = rf'(?:\s*{GNOSTIC_DOMAINS})(?:\.|\b)'

ALIEN_JS_REGEX: Final[re.Pattern] = re.compile(
    rf'^(?!(?:{GNOSTIC_PREFIX}))'  
    r'(?:[\w-]+\s*:\s+[{"\'])'
)

ALIEN_ARROW_REGEX: Final[re.Pattern] = re.compile(
    rf'^(?!(?:{GNOSTIC_PREFIX}))'
    r'\(?.*?\)?\s*=>\s*'
)

ALIEN_NESTING_REGEX: Final[re.Pattern] = re.compile(
    rf'^(?!(?:{GNOSTIC_PREFIX}))'
    r'\{[^{}]*:[^{}]*\}'
)

ALIEN_RUST_REGEX: Final[re.Pattern] = re.compile(r'[\w]+::[\w]+')
ALIEN_GO_REGEX: Final[re.Pattern] = re.compile(r'[\w]+\s*:=\s*')

# The Multi-Dimensional Amnesty Phalanx
AMNESTY_VETO_REGEX: Final[re.Pattern] = re.compile(
    r'(' + ALIEN_JS_REGEX.pattern + r')|(' +
    ALIEN_ARROW_REGEX.pattern + r')|(' +
    ALIEN_NESTING_REGEX.pattern + r')|(' +
    ALIEN_RUST_REGEX.pattern + r')|(' +
    ALIEN_GO_REGEX.pattern + r')'
)