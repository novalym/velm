# Path: scaffold/artisans/shadow_clone/mirror.py
# ----------------------------------------------
# LIF: INFINITY // AUTH_CODE: #!@RECLAMATION_MIRROR_V18.0
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ----------------------------------------------

import os
import time
import shutil
import threading
import stat
import hashlib
from pathlib import Path
from typing import Optional, Set, Dict, Any
from ...logger import Scribe

Logger = Scribe("SynapticMirror")


class MirrorHandler:
    """
    =============================================================================
    == THE MIRROR HANDLER (V-Ω-ATOMIC-REFLECTION-V18.0)                        ==
    =============================================================================
    LIF: INFINITY | Manages the surgical translocation of matter between realms.
    """

    def __init__(self, master_root: Path, shadow_root: Path, sid: str):
        self.master = master_root
        self.shadow = shadow_root
        self.sid = sid
        # [ASCENSION 4]: Binary Guard - Threshold 5MB
        self.MAX_BINARY_SIZE = 5 * 1024 * 1024
        self.ignore_patterns = {'.git', 'node_modules', '__pycache__', '.logs', '.scaffold'}
        # [ASCENSION 2]: Debounce memory
        self._last_sync_time = 0
        self._batch_delay = 0.1  # 100ms coalescence

    def reflect(self, src_path_str: str):
        """[ASCENSION 1 & 5 & 6]: ATOMIC SWAPPING & PERMISSION HEALING."""
        src_path = Path(src_path_str)

        # Abyssal Filter
        if any(p in src_path.parts for p in self.ignore_patterns):
            return

        try:
            rel_path = src_path.relative_to(self.master)
            dest_path = self.shadow / rel_path

            if not src_path.exists() or not src_path.is_file():
                return

            # [ASCENSION 4]: Binary Integrity Check
            if src_path.stat().st_size > self.MAX_BINARY_SIZE:
                Logger.verbose(f"Skipping heavy matter: {rel_path.name}")
                return

            # [ASCENSION 1]: ATOMIC SWAP STRATEGY
            # Write to temporary vessel to prevent Vite/Framework partial reads
            temp_dest = dest_path.with_suffix(f".{uuid.uuid4().hex[:6]}.tmp")

            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # [ASCENSION 6]: Permission Healing (Windows Hardened)
            if dest_path.exists():
                os.chmod(dest_path, stat.S_IWRITE)

            # [ASCENSION 5 & 7]: Metadata Preservation & Latency Tracking
            start = time.perf_hooks().time()
            shutil.copy2(src_path, temp_dest)  # Preserves metadata
            os.replace(temp_dest, dest_path)  # Atomic Rename
            duration = (time.perf_hooks().time() - start) * 1000

            # [ASCENSION 11]: HAPTIC SIGNAL BROADCAST
            Logger.info(f"Reflected {rel_path.name}", extra={"tags": ["NEURAL_LINK"], "data": {
                "type": "shadow:sync",
                "shadow_id": self.sid,
                "path": str(rel_path),
                "latency_ms": duration
            }})

        except Exception as e:
            Logger.verbose(f"Reflection fractured for {src_path.name}: {e}")


class SynapticMirror:
    """
    =============================================================================
    == THE SYNAPTIC MIRROR (V-Ω-ETERNAL-VIGIL)                                 ==
    =============================================================================
    The tireless guardian thread that maintains the HMR pulse.
    """

    def __init__(self, master_root: Path, shadow_root: Path, sid: str):
        self.master = master_root
        self.shadow = shadow_root
        self.sid = sid
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """[ASCENSION 2 & 10]: ASYNCHRONOUS DEBOUNCED VIGIL."""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class MirrorGateway(FileSystemEventHandler):
                def __init__(self, handler: MirrorHandler):
                    self.handler = handler

                def on_modified(self, event):
                    if not event.is_directory: self.handler.reflect(event.src_path)

                def on_created(self, event):
                    if not event.is_directory: self.handler.reflect(event.src_path)

            handler = MirrorHandler(self.master, self.shadow, self.sid)
            observer = Observer()
            observer.schedule(MirrorGateway(handler), str(self.master), recursive=True)

            def _vigil_loop():
                observer.start()
                Logger.success(f"Synaptic Mirror for {self.sid} ACHIEVED RESONANCE.")
                while not self._stop_event.is_set():
                    time.sleep(1)
                observer.stop()
                observer.join()
                Logger.info(f"Synaptic Mirror for {self.sid} returned to the void.")

            self._thread = threading.Thread(target=_vigil_loop, name=f"Mirror-{self.sid}", daemon=True)
            self._thread.start()

        except ImportError:
            Logger.warn("Mirroring Fracted: 'watchdog' not found in this reality.")
        except Exception as e:
            Logger.error(f"Mirroring Failed to Materialize: {e}")

    def stop(self):
        """[ASCENSION 10]: Graceful Dissolution."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)