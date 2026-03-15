# Path: core/alchemist/elara/library/system_rites/hardware_vitals.py
# ------------------------------------------------------------------

import os
import sys
import time
import hashlib
import platform
import multiprocessing
import uuid
from typing import Any, Dict
from ..registry import register_rite

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

@register_rite("vitals")
def get_metabolic_vitals(value: Any = None, **kwargs) -> Dict[str, Any]:
    """[ASCENSION 15]: Full-Spectrum Hardware Biopsy."""
    vitals = {
        "cores": multiprocessing.cpu_count(),
        "status": "RESONANT",
        "timestamp": time.time(),
        "substrate": "IRON" if not os.environ.get("SCAFFOLD_ENV") == "WASM" else "ETHER"
    }
    if HAS_PSUTIL and not os.environ.get("SCAFFOLD_ENV") == "WASM":
        vitals.update({
            "cpu_load": psutil.cpu_percent(interval=None),
            "ram_usage": psutil.virtual_memory().percent,
            "fever": psutil.cpu_percent() > 90,
            "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
        })
    return vitals

@register_rite("os_info")
def get_os_dna(value: Any = None) -> Dict[str, str]:
    """Platform Fingerprinting."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "arch": platform.machine(),
        "node": platform.node(),
        "is_windows": platform.system() == "Windows",
        "python_v": sys.version.split()[0],
        "machine_id": hashlib.sha256(platform.node().encode()).hexdigest()[:12].upper()
    }

@register_rite("cpu_arch")
def get_cpu_arch(value: Any = None) -> str:
    """[ASCENSION 67]: Hardware Instruction Sensing."""
    arch = platform.machine().lower()
    if 'arm' in arch or 'aarch64' in arch: return "arm64"
    if 'x86_64' in arch or 'amd64' in arch: return "x86_64"
    return arch

@register_rite("mem_usage")
def get_mem_usage(value: Any = None) -> float:
    """Returns Process RAM usage in MB."""
    if HAS_PSUTIL:
        process = psutil.Process(os.getpid())
        return round(process.memory_info().rss / 1024 / 1024, 2)
    return 0.0

@register_rite("disk_space")
def get_disk_space(value: Any) -> Dict[str, float]:
    """[ASCENSION 74]: Disk Quota Governor."""
    path = str(value) if value else "/"
    if HAS_PSUTIL:
        try:
            usage = psutil.disk_usage(path)
            return {
                "total_gb": round(usage.total / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent_used": usage.percent
            }
        except: pass
    return {"total_gb": 0.0, "free_gb": 0.0, "percent_used": 0.0}

@register_rite("get_mac_address")
def get_mac_address_rite(value: Any = None) -> str:
    """[ASCENSION 71]: MAC Address Tomography."""
    return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])