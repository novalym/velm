# Path: core/lsp/scaffold_server/__init__.py
# -----------------------------------------
# LIF: INFINITY | ROLE: GATEWAY_TO_THE_ORACLE | RANK: SOVEREIGN
# =================================================================================
# == THE GNOSTIC ORACLE GATEWAY (V-Ω-TOTALITY-V300)                              ==
# =================================================================================
"""
The unified export gateway for the Scaffold Language Server domain.
It exposes the ScaffoldLSPServer totality and provides the entry point for the
Ocular Mind to commune with the physical world.
"""

import sys
import os
import platform

# [ASCENSION 1]: BINARY SOVEREIGNTY (THE KERNEL WARD)
# This rite must be conducted at the absolute dawn of the package's existence.
if platform.system() == "win32":
    try:
        import msvcrt
        # Force raw binary mode on standard handles to prevent CRLF mangling.
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    except Exception as e:
        sys.stderr.write(f"[Oracle:Kernel] 💥 Binary Mode Shift failed: {e}\n")
        sys.stderr.flush()

from .engine import ScaffoldLSPServer
from .bootstrap import main as ignite_oracle

__version__ = "3.2.0-SINGULARITY"
__all__ = ["ScaffoldLSPServer", "ignite_oracle"]

# [ASCENSION 12]: METABOLIC PROCLAMATION
# If the SCAFFOLD_DEBUG_BOOT flag is manifest, we scream the arrival of the Oracle.
if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
    sys.stderr.write(f"[Oracle] 🕯️  Gnostic Oracle Stratum v{__version__} manifest.\n")
    sys.stderr.flush()