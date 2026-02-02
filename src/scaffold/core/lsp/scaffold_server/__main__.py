# Path: core/lsp/scaffold_server/__main__.py
# ------------------------------------------

import sys
import os

# [ASCENSION 1]: PATH ANCHORING
# Ensure the package root is in sys.path so relative imports within the module work
# when executed directly.
current_dir = os.path.dirname(os.path.abspath(__file__))
package_root = os.path.abspath(os.path.join(current_dir, "../../../.."))
if package_root not in sys.path:
    sys.path.insert(0, package_root)

from scaffold.core.lsp.scaffold_server.bootstrap import main

if __name__ == "__main__":
    """
    [THE SPARK]
    Ignites the Gnostic Oracle via the Bootstrap sequence.
    """
    sys.exit(main())