# Path: inquisitor/sanctum/diagnostics/ruby.py
# --------------------------------------------
from ..engine import BaseInquisitor

class RubyInquisitor(BaseInquisitor):
    """A divine artisan for perceiving the soul of Ruby scriptures."""
    LANGUAGE_NAME = 'ruby'
    GRAMMAR_PACKAGE = 'tree_sitter_ruby'
    QUERIES = {
        # ★★★ PILLAR III ASCENSION ★★★
        'imports': """
            (call
                method: (identifier) @_func
                arguments: (argument_list (string (string_content) @import))
                (#match? @_func "^(require|require_relative)$")
            )
        """,
        # ★★★ APOTHEOSIS COMPLETE ★★★
        'functions': '(method name: (identifier) @name) @function',
        'methods': '(method name: (identifier) @name) @method',
        'function_args': '(method_parameters . (identifier) @arg)',
        'classes': '(class name: (constant) @name) @class',
        'complexity_nodes': """
            [
              (if)
              (unless)
              (for)
              (while)
              (until)
              (case)
              (rescue)
              (binary operator: "&&")
              (binary operator: "||")
            ] @complexity
        """
    }