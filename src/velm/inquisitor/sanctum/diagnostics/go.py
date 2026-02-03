# Path: inquisitor/sanctum/diagnostics/go.py
# ------------------------------------------
from ..engine import BaseInquisitor

class GoInquisitor(BaseInquisitor):
    """A divine artisan for perceiving the soul of Go scriptures."""
    LANGUAGE_NAME = 'go'
    GRAMMAR_PACKAGE = 'tree_sitter_go'
    QUERIES = {
        # ★★★ PILLAR III ASCENSION ★★★
        'imports': """
            (import_spec path: (interpreted_string_literal) @import)
        """,
        # ★★★ APOTHEOSIS COMPLETE ★★★
        'functions': '(function_declaration name: (identifier) @name) @function',
        'function_args': '(parameter_list . (parameter_declaration name: (identifier) @arg))',
        'classes': '(type_declaration (type_spec name: (type_identifier) @name (struct_type))) @class',
        'methods': '(method_declaration receiver: (_) name: (field_identifier) @name) @method',
        'complexity_nodes': """
            [
              (if_statement)
              (for_statement)
              (expression_switch_statement)
              (type_switch_statement)
              (binary_expression operator: "&&")
              (binary_expression operator: "||")
            ] @complexity
        """
    }