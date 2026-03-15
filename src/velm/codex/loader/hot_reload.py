# Path: src/velm/codex/loader/hot_reload.py
# -----------------------------------------

import threading
import time
import os
import sys
from pathlib import Path
from ...logger import Scribe

Logger = Scribe("CodexWatchdog")


class CodexWatchdog:
    """
    =============================================================================
    == THE ACHRONAL HOT-RELOADER (V-Ω-BACKGROUND-SENTINEL)                     ==
    =============================================================================
    Monitors user plugins in `.scaffold/codex/atoms`. If a file changes,
    it triggers `CodexRegistry.awaken(force_reload=True)` seamlessly.
    """
    _active = False

    @classmethod
    def ignite(cls):
        # [ASCENSION 12]: WASM Ether Degradation
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        if is_wasm or cls._active:
            return

        def _watch():
            from .discovery import _FILE_LEDGER, PluginScrier
            from .registry import CodexRegistry

            while True:
                time.sleep(2.0)
                try:
                    mutations = False
                    for file_str, data in list(_FILE_LEDGER.items()):
                        p = Path(file_str)
                        if p.exists() and p.stat().st_mtime > data["mtime"]:
                            Logger.info(f"🌀 Mutation detected in {p.name}. Transmuting AST...")
                            PluginScrier.import_user_plugin(data["mod_name"], p, "Hot-Reload")
                            mutations = True

                    if mutations:
                        # Force a full registry reconstruction
                        CodexRegistry.awaken(force_reload=True)
                except Exception:
                    pass

        t = threading.Thread(target=_watch, daemon=True, name="CodexWatchdogThread")
        t.start()
        cls._active = True