# Path: scaffold/artisans/watchman/engine.py
# ------------------------------------------
import os
import subprocess
import threading
import time
import signal
from pathlib import Path
from typing import Optional, List
from fnmatch import fnmatch

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    Observer = object
    FileSystemEventHandler = object


class KineticEngine:
    """
    Manages the physical execution of commands.
    Handles process killing (restarts) and environment injection.
    """

    def __init__(self, command: str, root: Path, restart: bool = True):
        self.command = command
        self.root = root
        self.restart = restart
        self._process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()

    def trigger(self, changed_file: Path):
        """
        Executes the command.
        If 'restart' is True, kills the previous process first.
        """
        with self._lock:
            if self.restart and self._process and self._process.poll() is None:
                # Kill previous
                self._kill_process_tree(self._process)
                self._process = None

            # Inject Gnostic Context
            env = os.environ.copy()
            env["SCAFFOLD_CHANGED_FILE"] = str(changed_file)
            env["SCAFFOLD_CHANGED_REL"] = str(changed_file.relative_to(self.root))

            try:
                # We use a shell to allow complex pipes and logic in the command string
                self._process = subprocess.Popen(
                    self.command,
                    shell=True,
                    cwd=self.root,
                    env=env
                )
                self._process.wait()
                return self._process.returncode
            except Exception as e:
                print(f"[Sentinel Error] Execution failed: {e}")
                return 1

    def _kill_process_tree(self, proc: subprocess.Popen):
        """Recursively kills a process tree."""
        try:
            if os.name == 'nt':
                # Windows needs force
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)])
            else:
                # Unix: Kill the process group
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except:
            pass  # Already dead


class GnosticHandler(FileSystemEventHandler):
    """
    Filters events based on glob patterns and ignore lists.
    Debounces bursts of events (e.g. "Save All").
    """

    def __init__(self, engine: KineticEngine, glob: str, ignore: List[str], debounce: float, callback):
        self.engine = engine
        self.glob = glob
        self.ignore = ignore or []
        # Add standard ignores
        self.ignore.extend([".git*", ".scaffold*", "__pycache__*", "*.swp", "*.tmp"])
        self.debounce = debounce
        self.callback = callback  # UI Callback
        self._timer: Optional[threading.Timer] = None

    def on_any_event(self, event):
        if event.is_directory: return

        path = Path(event.src_path)
        try:
            rel_path = path.relative_to(self.engine.root)
        except ValueError:
            return  # Outside root

        # 1. Check Ignores
        for pattern in self.ignore:
            if fnmatch(str(rel_path), pattern) or fnmatch(path.name, pattern):
                return

        # 2. Check Match
        if not fnmatch(str(rel_path), self.glob):
            return

        # 3. Debounce
        if self._timer:
            self._timer.cancel()

        self._timer = threading.Timer(self.debounce, lambda: self._fire(path))
        self._timer.start()

    def _fire(self, path: Path):
        self.callback(path)
        start = time.time()
        code = self.engine.trigger(path)
        duration = time.time() - start
        # We rely on the Artisan to handle the result UI,
        # but the handler triggers the engine directly for speed.

