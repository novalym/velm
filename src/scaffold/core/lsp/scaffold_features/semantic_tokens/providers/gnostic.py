# Path: scaffold/core/lsp/scaffold_features/semantic_tokens/providers/gnostic.py
# ---------------------------------------------------------------------
# LIF: INFINITY | ROLE: SPECTRAL_TOKENIZER | RANK: SOVEREIGN
# auth_code: Ω_SPECTRAL_SEER_V100

import re
from typing import List
from ....base.features.semantic_tokens.contracts import TokenProvider
from ....base.features.semantic_tokens.encoder import RawToken
from ....base.features.semantic_tokens.legend import TokenType, TokenModifier
from ....base.document import TextDocument


class GnosticTokenProvider(TokenProvider):
    """
    =============================================================================
    == THE SPECTRAL SEER (V-Ω-REGEX-TOMOGRAPHY)                                ==
    =============================================================================
    Performs a single-pass regex scry to identify all Scaffold/Symphony particles
    and assign them their true semantic color.
    """

    # [ASCENSION 1]: THE MASTER REGEX (ULTRA-OPTIMIZED)
    # Priority ordered: Comments & Strings first to consume content.
    GNOSTIC_PATTERN = re.compile(
        r'(?P<comment>#.*)|'
        r'(?P<string>"(?:\\.|[^"\\])*"|\'\'\'.*?\'\'\')|'
        r'(?P<directive>@\w+)|'
        r'(?P<edict>>>|\?\?|!!|%%)|'
        r'(?P<polyglot>\b[a-z]+:)|'
        r'(?P<operator>::|<<|->|\+=|-=|~=|\^=|\|=)|'
        r'(?P<variable>\$\$[a-zA-Z_]\w*)|'
        r'(?P<jinja_open>\{\{)|'
        r'(?P<jinja_close>\}\})|'
        r'(?P<number>\b\d+\b)|'
        r'(?P<ident>[a-zA-Z_][\w\-]*)'
    )

    SYSTEM_VARS = {'project_root', 'scaffold_version', 'now', 'env', 'secret', 'cwd'}

    def scry_tokens(self, doc: TextDocument) -> List[RawToken]:
        tokens = []
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            # Track if we are inside a Jinja block for sub-token logic
            is_inside_jinja = False

            for match in self.GNOSTIC_PATTERN.finditer(line):
                kind = match.lastgroup
                start = match.start()
                length = match.end() - start

                t_type = TokenType.VARIABLE
                modifiers = 0

                if kind == "comment":
                    t_type = TokenType.COMMENT

                elif kind == "string":
                    t_type = TokenType.STRING

                elif kind == "directive":
                    t_type = TokenType.DECORATOR
                    modifiers |= TokenModifier.STATIC

                elif kind == "edict":
                    t_type = TokenType.KEYWORD
                    modifiers |= TokenModifier.DEFAULT_LIBRARY

                elif kind == "polyglot":
                    t_type = TokenType.NAMESPACE
                    modifiers |= TokenModifier.DEFINITION

                elif kind == "operator":
                    t_type = TokenType.OPERATOR

                elif kind == "variable":
                    # [ASCENSION 1]: Causal distinction
                    t_type = TokenType.VARIABLE
                    modifiers |= TokenModifier.DECLARATION

                elif kind == "jinja_open":
                    t_type = TokenType.OPERATOR
                    is_inside_jinja = True

                elif kind == "jinja_close":
                    t_type = TokenType.OPERATOR
                    is_inside_jinja = False

                elif kind == "number":
                    t_type = TokenType.NUMBER

                elif kind == "ident":
                    val = match.group()

                    # Jinja-specific sub-triage
                    if is_inside_jinja:
                        if val in self.SYSTEM_VARS:
                            t_type = TokenType.VARIABLE
                            modifiers |= TokenModifier.STATIC | TokenModifier.READONLY
                        elif line[match.end():match.end() + 1] == "(":
                            t_type = TokenType.FUNCTION
                        else:
                            t_type = TokenType.VARIABLE
                    else:
                        # Standard Identifiers
                        if val in ["true", "false", "null"]:
                            t_type = TokenType.KEYWORD
                        elif ":" in line[match.end():match.end() + 1]:
                            t_type = TokenType.PROPERTY
                        else:
                            t_type = TokenType.VARIABLE

                tokens.append(RawToken(i, start, length, int(t_type), modifiers))

        return tokens