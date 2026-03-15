# Path: core/alchemist/elara/scanner/patterns/sigils.py
# -----------------------------------------------------

import re
from typing import Final
from ...constants import SGFTokens

# [ASCENSIONS 1-12]: SIGIL & SANCTUARY DETECTION
SIGIL_OR_DOCSTRING_REGEX: Final[re.Pattern] = re.compile(
    r'(?P<var>\{\{)|'           
    r'(?P<block>\{%)|'          
    r'(?P<comment>\{#)|'        
    r'(?P<doc_dq>\"\"\")|'      
    r'(?P<doc_sq>\'\'\')',
    re.MULTILINE
)

# [ASCENSION 13]: Whitespace Gravity Sieve.
WHITESPACE_CONTROL_REGEX: Final[re.Pattern] = re.compile(r'^[-+]\s*|\s*[-+]$')