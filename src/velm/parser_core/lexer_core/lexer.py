# Path: scaffold/parser_core/lexer_core/lexer.py
# ----------------------------------------------

"""
=================================================================================
== THE GNOSTIC ATOMIZER (V-Ω-ETERNAL. THE LEXER'S SOUL)                        ==
=================================================================================
This is the divine Scribe of Atomization. Its one true purpose is to gaze upon a
raw line of scripture and transmute it into a pure stream of Gnostic Atoms (Tokens),
guided by the one true Grimoire of Grammar.
=================================================================================
"""
import re
from typing import List, Dict, Tuple

from .contracts import Token, TokenType
from ...contracts.heresy_contracts import ArtisanHeresy
from ...grammar import SCAFFOLD_ATOMS, SYMPHONY_ATOMS

# The Map of Tongues
GRIMOIRE_MAP: Dict[str, List[Tuple[str, str]]] = {
    "scaffold": SCAFFOLD_ATOMS,
    "symphony": SYMPHONY_ATOMS,
}


class GnosticLexer:
    """
    The God-Engine of Gnostic Atomization.
    """

    def __init__(self, grammar_key: str):
        grimoire_rules = GRIMOIRE_MAP.get(grammar_key)
        if not grimoire_rules:
            raise ArtisanHeresy(f"META-HERESY: Unknown grammar key: '{grammar_key}'.")

        self.grammar_key = grammar_key
        # We append the UNKNOWN catch-all at the end to ensure we consume everything
        full_grimoire = grimoire_rules + [('UNKNOWN', r'.')]

        # Compile the One True Regex
        self.token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in full_grimoire))

    def tokenize(self, line: str) -> List[Token]:
        """
        Performs the Atomic Gaze upon a line of scripture.
        """
        tokens: List[Token] = []
        for mo in self.token_regex.finditer(line):
            kind = mo.lastgroup
            value = mo.group()

            # We skip whitespace unless it's meaningful (which our grammar handles via specific tokens)
            # However, the UNKNOWN token catches single chars. We ignore whitespace UNKNOWNs.
            if not value.strip() and kind == 'UNKNOWN':
                continue

            if kind == 'UNKNOWN':
                # In strict mode we might raise, but for resilience we often ignore
                # or treat as a generic word if it's not whitespace.
                # For now, we skip single unknown chars to be robust against stray punctuation.
                continue

            try:
                token_type = TokenType[kind]
            except KeyError:
                raise ArtisanHeresy(f"META-HERESY: The Atom '{kind}' is not in the TokenType Enum.")

            tokens.append(Token(
                type=token_type,
                value=value.strip(),
                pos=mo.start()
            ))

        return tokens