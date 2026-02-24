# Path: scaffold/grammar.py
# -------------------------

"""
=================================================================================
== THE SACRED GRAMMAR OF FORMS (V-Ω-PERCEPTION-LAYER)                          ==
=================================================================================
LIF: 10,000,000,000 (THE ATOMIC TRUTH)

This scripture defines the fundamental regular expressions (Regex) that the
Gnostic Lexer uses to deconstruct the Architect's Will into atomic units (Tokens).

It serves as the **eyes** of the God-Engine. If a pattern is not inscribed here,
the Engine cannot perceive it.

### THE HIERARCHY OF PERCEPTION:
1.  **Block Delimiters:** Multi-line structures must be perceived first to avoid
    fragmentation.
2.  **Operators & Sigils:** The verbs of the language (Create, Append, Link).
3.  **Modifiers:** Directives that alter the nature of a scripture (@hash, @inside).
4.  **Metadata:** Permissions, Variables, and Vows.
5.  **Values & Identifiers:** The raw material (Paths, Strings, Numbers).

### THE ASCENDED FACULTIES (V-Ω):
*   **The Sentinel of Links:** Added `->` for symbolic linking.
*   **The Gnostic Traits:** Added `%% trait` and `%% use` for mixin composition.
*   **The Integrity Anchor:** Added `@hash(...)` for SRI-style verification.
*   **The Permission Granularizer:** Expanded permission logic to accept keywords.
=================================================================================
"""

import re

# =============================================================================
# == I. THE SCAFFOLD ATOMS (THE LANGUAGE OF FORM)                            ==
# =============================================================================
SCAFFOLD_ATOMS = [
    # -------------------------------------------------------------------------
    # 1. BLOCK DELIMITERS (The Containers of Soul)
    # -------------------------------------------------------------------------
    # These must be matched first. They represent the start of a multi-line content block.
    # We match the operator + the opening quote.
    ('SIGIL_MULTILINE_DQ', r'::\s*"""'),  # :: """ ... """
    ('SIGIL_MULTILINE_SQ', r"::\s*'''"),  # :: ''' ... '''
    ('SIGIL_APPEND_BLOCK_DQ', r'\+=\s*"""'),  # += """ ... """
    ('SIGIL_APPEND_BLOCK_SQ', r"\+=\s*'''"),  # += ''' ... '''
    ('SIGIL_TRANSFIGURE_BLOCK_DQ', r'~=\s*"""'),  # ~= """ ... """
    ('SIGIL_TRANSFIGURE_BLOCK_SQ', r"~=\s*'''"),  # ~= ''' ... '''
    ('SIGIL_PREPEND_BLOCK_DQ', r'\^=\s*"""'),  # ^= """ ... """
    ('SIGIL_PREPEND_BLOCK_SQ', r"\^=\s*'''"),  # ^= ''' ... '''

    # -------------------------------------------------------------------------
    # 2. INLINE OPERATORS (The Verbs of Creation)
    # -------------------------------------------------------------------------
    # These define the relationship between the Path (Form) and the Content (Soul).
    ('SIGIL_APPEND', r'\+='),  # Append content
    ('SIGIL_SUBTRACT', r'-='),  # Remove content (Regex)
    ('SIGIL_TRANSFIGURE', r'~='),  # Regex substitution
    ('SIGIL_PREPEND', r'\^='),  # Prepend content
    ('SIGIL_INLINE', r'::'),  # Define content inline
    ('SIGIL_SEED', r'<<'),  # Seed content from external file
    ('SIGIL_SYMLINK', r'->'),  # [NEW] Establish a symbolic link

    # -------------------------------------------------------------------------
    # 3. SEMANTIC MODIFIERS (The Adjectives of Intent)
    # -------------------------------------------------------------------------
    # These modify the behavior of the operation (e.g., @inside a class, @hash integrity).

    # [NEW] The Hash Anchor: file.py @hash(sha256:abc...)
    # Matches the full directive to capture the algorithm and digest.
    ('HASH_ANCHOR', r'@hash\([a-zA-Z0-9]+:[a-fA-F0-9]+\)'),

    # -----------------------------------------------------------------------------------------
    # [1] SIGIL_DIRECTIVE: THE HIGH RITUALS OF GOVERNANCE
    # -----------------------------------------------------------------------------------------
    # These are the "Sovereign Verbs". They represent standalone actions of the Engine.
    # They control Composition (@import, @include), Logic (@if), and Reusability (@macro).
    # STRATEGY: We explicitly list these to ensure they receive "Naked Ward" priority.
    # To add a new command to the language, simply append the verb here and wire its
    # Scribe in the SCRIBE_PANTHEON.
    # -----------------------------------------------------------------------------------------
    ('SIGIL_DIRECTIVE', r'@(import|from|include|macro|call|session|manifested|if|elif|else|endif|for|endfor|task|endtask|try|catch|finally|endtry|scry|audit|herald|proclaim)\b'),
    # -----------------------------------------------------------------------------------------
    # [2] SIGIL_MODIFIER: THE LAWS OF PROPERTY & AD-HOC ASCENSION
    # -----------------------------------------------------------------------------------------
    # These are the "Spectral Adjectives". Unlike Directives, they attach to Matter (Paths).
    # e.g., "src/auth.py @encrypt @readonly".
    #
    # ### THE AD-HOC STRATEGY (WHAT THIS OPENS UP):
    # 1. ATOMIC EXPANSION: This architecture allows us to add new "Middleware Traits" to
    #    files without refactoring. By adding '@hidden' here, we instantly enable the
    #    VFS to scry that property and hide the file from the Ocular UI.
    # 2. ASPECT-ORIENTED ARCHITECTURE:
    #    - @inside(sanctum): Forces a file to exist only within a specific virtual container.
    #    - @after(rite): Delays manifestation until a specific kinetic strike concludes.
    #    - @patch(path): Flags a file as a surgical mutation rather than a creation.
    #    - @warded(auth): Enforces Identity Handshakes before the file can be read.
    # 3. FUTURE-PROOFING: To add a new property (e.g. '@distributed'), you only add the
    #    word to this regex. The DeconstructionScribe automatically extracts it into the
    #    'semantic_selector' dict on the ScaffoldItem, where any Artisan can scry it.
    # -----------------------------------------------------------------------------------------
    ('SIGIL_MODIFIER', r'@(inside|after|before|patch|warded|hidden|volatile|ephemeral|readonly|executable|signature|encrypt|trace|audit)\b'),

    # -----------------------------------------------------------------------------------------
    # [3] OPERATOR_KEYWORD: THE LOGICAL SUTURE (CONJUNCTIONS)
    # -----------------------------------------------------------------------------------------
    # These are the "Particles of Resonance". They provide the glue for complex directives.
    # Essential for the '@from <path> import <item> as <alias>' Python-parity syntax.
    # STRATEGY: By defining these as keywords, we prevent the Lexer from misidentifying
    # the word "import" as a "file path" when it appears inside a @directive line.
    # -----------------------------------------------------------------------------------------
    ('OPERATOR_KEYWORD', r'\b(import|as|in|from|where|using|trait|use|of|by|with|on|to)\b'),
    
    # Arguments for directives: (key="value", ...)
    ('SIGIL_LPAREN', r'\('),
    ('SIGIL_RPAREN', r'\)'),
    ('KEY_VALUE_PAIR', r'\w+\s*=\s*(?:"[^"]*"|\'[^\']*\')'),
    ('OPERATOR_COMMA', r','),

    # -------------------------------------------------------------------------
    # 4. METADATA & TRAITS (The Laws of the File)
    # -------------------------------------------------------------------------

    # [NEW] Gnostic Traits: Reusable architectural DNA
    ('SIGIL_TRAIT_DEF', r'%%\s*trait\b'),  # %% trait Auth = ...
    ('SIGIL_TRAIT_USE', r'%%\s*use\b'),  # %% use Auth
    ('SIGIL_ON_UNDO', r'%%\s*on-undo\b'), # [NEW] The Maestro's Counter-Edict
    # =====================
    ('SIGIL_PERMS', r'%%'),  # Permissions marker
    ('SIGIL_VAR_DEF', r'\$\$'),  # Variable definition
    ('SIGIL_VOW', r'\?\?'),  # Gnostic Vow (Assertion)
    ('SIGIL_INDENTED', r':\s*$'),  # Start of an indented block

    # -------------------------------------------------------------------------
    # 5. VALUES (The Raw Gnosis)
    # -------------------------------------------------------------------------

    # Permissions: Octal (755) or Named (executable, readonly, secret)
    # Note: We rely on the DeconstructionScribe to bind this to the %% sigil.
    ('PERMISSIONS', r'(?<=%%\s)(?:[0-7]{3}|executable|readonly|secret)'),

    # Seed Paths: The source of a << operation
    ('SEED_PATH', r'(?<=\<\<\s)[\S]+'),

    # Jinja2 Constructs: {{ var }} or {% if %}
    ('JINJA_CONSTRUCT', r'\{[%#].*?[%#]\}'),
    ('PLACEHOLDER', r'\{\{.*?\}\}'),

    # Strings: Double or Single quoted, handling escaped quotes.
    ('QUOTED_STRING', r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),

    # -------------------------------------------------------------------------
    # 6. THE PATH (The Locus of Manifestation)
    # -------------------------------------------------------------------------
    # A path is any sequence of characters that is NOT a sigil or operator.
    # We explicitly exclude the new `->` sigil from being consumed as part of a filename.
    ('PATH', r'(?:(?!\+=|-=|~=|\^=|::|<<|%%|\?\?|@|#|->)[^"\':\s])+'),

    # -------------------------------------------------------------------------
    # 7. THE VOID (Comments & Whitespace)
    # -------------------------------------------------------------------------
    ('COMMENT', r'#.*'),
]

# =============================================================================
# == II. THE SYMPHONY ATOMS (THE LANGUAGE OF WILL)                           ==
# =============================================================================
# Used for parsing .symphony files.
SYMPHONY_ATOMS = [
    ('SIGIL_BLOCK_START', r'^[a-zA-Z0-9_]+\s*(?:\(.*\))?:\s*$'),  # Task/Macro definitions
    ('SIGIL_HEREDOC', r'<<\s*(\w+)'),  # Legacy heredoc support
    ('SIGIL_SIMPLE', r'>>|\?\?|%%'),  # Action, Vow, State
    ('SIGIL_BREAKPOINT', r'!!'),  # Debug breakpoint
    ('SIGIL_PARALLEL', r'&&'),  # Parallel execution
    ('SIGIL_IF', r'@if\b'),
    ('SIGIL_ELIF', r'@elif\b'),
    ('SIGIL_ELSE', r'@else\b'),
    ('SIGIL_ENDIF', r'@endif\b'),
    ('SIGIL_FOR', r'@for\b'),
    ('SIGIL_ENDFOR', r'@endfor\b'),
    ('SIGIL_TRY', r'@try\b'),
    ('SIGIL_CATCH', r'@catch\b'),
    ('SIGIL_FINALLY', r'@finally\b'),
    ('SIGIL_ENDTRY', r'@endtry\b'),
    ('SIGIL_TASK_DEF', r'@task\b'),
    ('SIGIL_TASK_END', r'@endtask\b'),
    ('SIGIL_MACRO_DEF', r'@macro\b'),
    ('SIGIL_MACRO_END', r'@endmacro\b'),
    ('SIGIL_CALL', r'@call\b'),
    ('SIGIL_IMPORT', r'@import\b'),
    ('SIGIL_DIRECTIVE', r'@\w+'),
    ('OPERATOR_COLON', r':'),
    ('OPERATOR_COMMA', r','),
    ('OPERATOR_KEYWORD', r'\b(as|using|in)\b'),
    ('QUOTED_STRING', r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
    ('COMMENT', r'#.*'),
    ('WORD', r'[^"\':,\s#]+'),
]