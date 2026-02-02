import shutil
import os
from typing import Tuple
from .base import BaseVowHandler

# Lazy load psutil to avoid hard dependency crash
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class ResourceVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE WARDEN OF RESOURCES (V-Ω-SYSTEM-VITALITY)                           ==
    =============================================================================
    Judges the capacity of the Host Machine.
    """

    def _vow_disk_space_gt(self, path: str, gb_str: str) -> Tuple[bool, str]:
        """Asserts free disk space is greater than X Gigabytes."""
        target = self._resolve(path)
        try:
            usage = shutil.disk_usage(target.parent if target.exists() else self.root)
            free_gb = usage.free / (1024 ** 3)
            needed_gb = float(gb_str)
            return free_gb > needed_gb, f"Free space {free_gb:.2f}GB > {needed_gb}GB."
        except Exception as e:
            return False, f"Disk check error: {e}"

    def _vow_memory_available_gt(self, mb_str: str) -> Tuple[bool, str]:
        """Asserts available RAM is greater than X Megabytes."""
        if not PSUTIL_AVAILABLE: return False, "psutil artisan missing."
        try:
            mem = psutil.virtual_memory()
            avail_mb = mem.available / (1024 ** 2)
            needed_mb = float(mb_str)
            return avail_mb > needed_mb, f"Available RAM {avail_mb:.0f}MB > {needed_mb}MB."
        except Exception:
            return False, "Memory check failed."

    def _vow_cpu_load_lt(self, percent_str: str) -> Tuple[bool, str]:
        """Asserts CPU usage is less than X percent."""
        if not PSUTIL_AVAILABLE: return False, "psutil artisan missing."
        try:
            # Interval=0.1 blocks slightly to get an accurate reading
            load = psutil.cpu_percent(interval=0.1)
            limit = float(percent_str)
            return load < limit, f"CPU Load {load}% < {limit}%."
        except Exception:
            return False, "CPU check failed."

    def _vow_battery_gt(self, percent_str: str) -> Tuple[bool, str]:
        """
        [THE MOBILE SENTINEL]
        Asserts battery is sufficient. Useful for local dev tasks that drain power.
        """
        if not PSUTIL_AVAILABLE: return False, "psutil artisan missing."
        try:
            battery = psutil.sensors_battery()
            if not battery: return True, "No battery detected (AC Power)."
            limit = float(percent_str)
            return battery.percent > limit, f"Battery {battery.percent}% > {limit}%."
        except Exception:
            return False, "Battery check failed."
