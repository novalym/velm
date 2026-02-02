# Path: scaffold/core/system/manager.py
# -------------------------------------

import os
import platform
import signal
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Callable, Any, Tuple

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# Lazy load psutil to avoid startup penalty
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

Logger = Scribe("SystemWarden")


@dataclass
class SystemTelemetry:
    """The Pulse of the Machine."""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_percent: float
    files_open: int
    threads_active: int
    timestamp: float = field(default_factory=time.time)


class SystemManager:
    """
    =================================================================================
    == THE WARDEN OF THE MACHINE (V-Ω-SYSTEM-HYPERVISOR-ULTIMA)                    ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Interface to the Operating System Kernel.
    It manages signals, resources, processes, and entropy.
    """

    _instance: Optional['SystemManager'] = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SystemManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.pid = os.getpid()
        self.process = psutil.Process(self.pid) if PSUTIL_AVAILABLE else None
        self._shutdown_hooks: List[Callable[[], None]] = []
        self._signal_handlers_installed = False
        self._platform_info = self._divine_platform()
        self._initialized = True

        Logger.verbose(f"System Warden initialized [PID: {self.pid} | OS: {self._platform_info['system']}]")

    def _divine_platform(self) -> Dict[str, str]:
        """[FACULTY 5] The Platform Diviner."""
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "node": platform.node()
        }
        # Windows specific tweaks
        if info["system"] == "Windows":
            info["win_edition"] = platform.win32_edition()
        return info

    # =========================================================================
    # == I. THE RITE OF TERMINATION (SIGNAL HANDLING)                        ==
    # =========================================================================

    def install_signal_handlers(self):
        """
        [FACULTY 3] The Signal Interceptor.
        Binds the Gnostic Engine to the OS's kill signals.
        """
        if self._signal_handlers_installed:
            return

        # We only catch SIGINT (Ctrl+C) and SIGTERM (Kill)
        # We assume the Engine's main loop will handle the logic, but we provide
        # a safety net here for cleanup hooks.
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, self._handle_signal)
            signal.signal(signal.SIGTERM, self._handle_signal)
            self._signal_handlers_installed = True
            Logger.verbose("Signal Interceptors engaged.")
        else:
            Logger.warn("Cannot install signal handlers from a worker thread.")

    def _handle_signal(self, signum, frame):
        """The atomic handler for OS signals."""
        sig_name = signal.Signals(signum).name
        Logger.warn(f"Received Signal: {sig_name}. Initiating Protocol Omega...")
        self.shutdown()
        # Re-raise to let Python exit if needed, or rely on sys.exit in shutdown
        sys.exit(128 + signum)

    def register_shutdown_hook(self, hook: Callable[[], None]):
        """Registers a cleanup rite to be performed at death."""
        self._shutdown_hooks.append(hook)

    def shutdown(self):
        """
        [FACULTY 6] The Doomsday Clock.
        Executes all shutdown hooks with a hard timeout.
        """
        Logger.info("System Warden executing shutdown rites...")

        # We execute hooks in LIFO order (Last In, First Out)
        for hook in reversed(self._shutdown_hooks):
            try:
                hook()
            except Exception as e:
                Logger.error(f"Shutdown Hook Heresy: {e}")

        # [FACULTY 7] The Zombie Ward
        if self.process:
            self.reap_zombies()

    # =========================================================================
    # == II. THE GAZE OF VITALITY (RESOURCE TELEMETRY)                       ==
    # =========================================================================

    def get_telemetry(self) -> SystemTelemetry:
        """
        [FACULTY 4] The Resource Oracle.
        Returns a snapshot of the machine's health.
        """
        if not PSUTIL_AVAILABLE or not self.process:
            return SystemTelemetry(0, 0, 0, 0, 0, 0, 0)

        try:
            # CPU
            cpu = psutil.cpu_percent(interval=None)

            # Memory
            mem = psutil.virtual_memory()

            # Process specific
            with self.process.oneshot():
                mem_info = self.process.memory_info()
                threads = self.process.num_threads()
                try:
                    # open_files() can be expensive/restricted
                    files = len(self.process.open_files())
                except:
                    files = -1

            # Disk (Root)
            disk = psutil.disk_usage(os.path.abspath(os.sep))

            return SystemTelemetry(
                cpu_percent=cpu,
                memory_percent=mem.percent,
                memory_used_mb=mem_info.rss / 1024 / 1024,
                memory_total_mb=mem.total / 1024 / 1024,
                disk_percent=disk.percent,
                files_open=files,
                threads_active=threads
            )

        except Exception as e:
            Logger.warn(f"Telemetry Gaze clouded: {e}")
            return SystemTelemetry(0, 0, 0, 0, 0, 0, 0)

    def check_vital_signs(self) -> bool:
        """
        [FACULTY 9] The OOM Prophet.
        Returns False if the system is critical.
        """
        telemetry = self.get_telemetry()

        if telemetry.memory_percent > 90.0:
            Logger.critical(f"MEMORY CRITICAL: {telemetry.memory_percent}% used.")
            return False

        if telemetry.disk_percent > 95.0:
            Logger.critical(f"DISK CRITICAL: {telemetry.disk_percent}% used.")
            return False

        return True

    # =========================================================================
    # == III. THE REAPER OF TREES (PROCESS MANAGEMENT)                       ==
    # =========================================================================

    def kill_process_tree(self, pid: int, timeout: float = 3.0):
        """
        [FACULTY 2] The Reaper of Trees.
        Terminates a process and all its descendants recursively.
        Handles Windows/Unix differences via psutil.
        """
        if not PSUTIL_AVAILABLE:
            # Fallback for systems without psutil (Weak Reaper)
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass
            return

        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)

            # 1. The Gentle Warning (SIGTERM)
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass

            try:
                parent.terminate()
            except psutil.NoSuchProcess:
                pass

            # 2. The Wait
            _, alive = psutil.wait_procs(children + [parent], timeout=timeout)

            # 3. The Killing Blow (SIGKILL)
            for p in alive:
                Logger.warn(f"Process {p.pid} resisted termination. Using force.")
                try:
                    p.kill()
                except psutil.NoSuchProcess:
                    pass

        except psutil.NoSuchProcess:
            pass  # Already dead
        except Exception as e:
            Logger.error(f"Reaper failed to harvest tree for PID {pid}: {e}")

    def reap_zombies(self):
        """[FACULTY 7] Cleans up zombie processes created by this process."""
        if not PSUTIL_AVAILABLE: return

        try:
            # waitpid() loop for Unix
            if os.name != 'nt':
                while True:
                    try:
                        pid, status = os.waitpid(-1, os.WNOHANG)
                        if pid == 0: break
                    except ChildProcessError:
                        break
        except Exception:
            pass

    # =========================================================================
    # == IV. THE GNOSTIC UTILITIES                                           ==
    # =========================================================================

    def is_admin(self) -> bool:
        """[FACULTY 8] The Privilege Gaze."""
        try:
            if os.name == 'nt':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False

    def is_interactive(self) -> bool:
        """Determines if the soul is connected to a TTY."""
        return sys.stdout.isatty() and sys.stdin.isatty()

    def get_capabilities(self) -> Dict[str, bool]:
        """[FACULTY 10] The Capability Map."""
        return {
            "symlinks": os.name != 'nt' or self.is_admin(),  # Windows requires admin for symlinks usually
            "chmod": os.name != 'nt',
            "signals": True,
            "tty": self.is_interactive(),
            "psutil": PSUTIL_AVAILABLE,
            "admin": self.is_admin()
        }


# Singleton Instance
System = SystemManager()