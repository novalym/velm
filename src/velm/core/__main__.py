# Path: core/__main__.py
# ----------------------
import sys
import os

# [ASCENSION 1]: PATH INJECTION
# Ensure the package root is in sys.path so we can import 'core'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.cli.cli_conductor import conduct_local_rite

if __name__ == "__main__":
    conduct_local_rite(sys.argv)