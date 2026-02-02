# // scaffold/inquisitor/queries/react_queries.py

"""
=================================================================================
== THE CODEX OF REACT QUERIES (V-Ω-STABLE-CORE-HEALED)                         ==
=================================================================================
LIF: 10,000,000,000

This file holds the Tree-sitter SCM queries.
FIXES:
- Removed explicit `jsx_fragment` to prevent grammar crashes.
- Broadened return statement capture to safely handle all JSX types.
"""

# Finds the last import statement.
QUERY_LAST_IMPORT = """
(program
  (import_statement)* @last_import
)
"""

# Finds specific named imports.
QUERY_NAMED_IMPORTS = """
(import_statement
  (import_clause
    (named_imports
      (import_specifier
        name: (identifier) @imported_name
      )
    )
  )
  source: (string) @source
)
"""

# Finds the Gnostic Injection Marker.
QUERY_GNOSTIC_MARKER = """
(jsx_expression
  (comment) @marker
  (#match? @marker "Gnostic Injection Point")
)
"""

# --- THE UNIVERSAL ROOT GAZE (HEALED) ---
# We look for return statements or arrow functions returning *something*.
# We rely on the `jsx_element` capture for standard cases, and a generic
# expression capture for fragments/self-closing to avoid "Invalid Node Type".
QUERY_RETURN_JSX = """
(return_statement
  [
    (parenthesized_expression (jsx_element) @jsx_root)
    (jsx_element) @jsx_root
    ; Fallback for fragments/other types that might crash explicit naming
    (parenthesized_expression) @jsx_generic
  ]
) @return_stmt

(arrow_function
  body: [
    (parenthesized_expression (jsx_element) @jsx_root)
    (jsx_element) @jsx_root
    (parenthesized_expression) @jsx_generic
  ]
) @arrow_implicit_return
"""

# We no longer need QUERY_DEFAULT_EXPORT_COMPONENT.
QUERY_DEFAULT_EXPORT_COMPONENT = ""