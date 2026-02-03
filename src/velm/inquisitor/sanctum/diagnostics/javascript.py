# Path: inquisitor/sanctum/diagnostics/javascript.py
# --------------------------------------------------
from ..engine import BaseInquisitor

class JavaScriptInquisitor(BaseInquisitor):
    """A divine artisan for perceiving the soul of JavaScript & TypeScript scriptures."""
    LANGUAGE_NAME = 'typescript'
    GRAMMAR_PACKAGE = 'tree_sitter_typescript'
    QUERIES = {
        # ★★★ PILLAR III ASCENSION ★★★
        'imports': """
            (import_statement source: (string) @import)
            (export_statement source: (string) @import)
            (call_expression
                function: (identifier) @_func
                arguments: (arguments (string) @import)
                (#match? @_func "^(require|import)$")
            )
        """,
        # ★★★ APOTHEOSIS COMPLETE ★★★
        'functions': """
            [
              (function_declaration name: (identifier) @name)
              (lexical_declaration (variable_declarator name: (identifier) @name value: (arrow_function)))
              (method_definition name: (property_identifier) @name)
            ] @function
        """,
        'function_args': '(formal_parameters . (required_parameter pattern: (identifier) @arg))',
        'classes': '(class_declaration name: (type_identifier) @name) @class',
        'methods': '(method_definition name: (property_identifier) @name) @method',
        'complexity_nodes': """
            [
              (if_statement)
              (for_statement)
              (for_in_statement)
              (while_statement)
              (do_statement)
              (switch_case)
              (catch_clause)
              (ternary_expression)
              (binary_expression operator: "&&")
              (binary_expression operator: "||")
            ] @complexity
        """
    }