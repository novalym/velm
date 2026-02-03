# Path: inquisitor/sanctum/diagnostics/rust.py
# ------------------------------------------

from ..engine import BaseInquisitor

class RustInquisitor(BaseInquisitor):
    """A divine artisan for perceiving the soul of Rust scriptures."""
    LANGUAGE_NAME = 'rust'
    GRAMMAR_PACKAGE = 'tree_sitter_rust'
    QUERIES = {
        'imports': """
            (use_declaration
              argument: [
                (scoped_identifier) @import
                (identifier) @import
              ]
            )
        """,
        'functions': '(function_item name: (identifier) @name) @function',
        'function_args': '(parameters . (identifier) @arg)',
        'classes': '[ (struct_item name: (type_identifier) @name) (enum_item name: (type_identifier) @name) ] @class',
        'methods': '(impl_item (function_item name: (identifier) @name)) @method',
        'complexity_nodes': """
            [
              (if_expression)
              (for_expression)
              (while_expression)
              (loop_expression)
              (match_expression)
              (binary_expression operator: "&&")
              (binary_expression operator: "||")
            ] @complexity
        """
    }