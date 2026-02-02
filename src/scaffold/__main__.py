# Path: scaffold/__main__.py
# --------------------------
# LIF: INFINITY | ROLE: MODULE_PROXY
# ==============================================================================

import sys
import os

# Ensure we can import the sibling 'main.py' even if run as a script
if __name__ == "__main__":
    # Add the parent directory to sys.path so "from scaffold.main import main" works
    # regardless of how python was invoked.
    current_path = os.path.abspath(os.path.dirname(__file__))
    parent_path = os.path.dirname(current_path)
    if parent_path not in sys.path:
        sys.path.insert(0, parent_path)

    try:
        from scaffold.main import main
        main()
    except ImportError:
        # Fallback for direct execution inside the folder
        from main import main
        main()