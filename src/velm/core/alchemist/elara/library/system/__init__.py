# Path: core/alchemist/elara/library/system/__init__.py
# -------------------------------------------------------------

"""
=================================================================================
== THE SYSTEM PANOPTICON: OMEGA TOTALITY (V-Ω-SYSTEM-RITES-VMAX-88-ASCENSIONS) ==
=================================================================================
LIF: ∞^∞ | ROLE: SUBSTRATE_SENSORY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SYSTEM_DIR_VMAX_SUBSTRATE_SUTURE_2026_FINALIS

[THE MANIFESTO]
The monolithic `system_rites.py` is dead. Welcome to the System Panopticon Lattice.
This directory houses the ascended, absolute authorities of the God-Engine over
the Host Machine (The Iron).

It annihilates the barrier between the Mind (Python) and the Iron (OS), granting
the blueprint native access to Daemons, Networking, Hardware Vitals, and the Filesystem.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (65-88):
65. **Daemon-Spawning Matrix:** `@shell_daemon` natively detaches from the parent process group, allowing background workers to survive the Engine's exit.
66. **OS-Level Environment Suture:** `@set_env` securely alters the thread-local OS environment variables for subsequent shell strikes.
67. **Hardware Instruction Sensing:** `@cpu_arch` detects AVX/Neon for accelerated tasks.
68. **Substrate-Aware Archiving:** `@zip_dir` and `@unzip` use pure Python `zipfile` bridging OS gaps where `tar` or `zip` binaries are missing.
69. **Dotenv Alchemist:** `@read_env` and `@write_env` parse and serialize `.env` files natively without external libraries.
70. **Thread-Safe File Watching:** `@watch_file` uses `os.stat` polling with hydraulic yields to pause execution until a file mutates.
71. **MAC Address Tomography:** `@get_mac_address` achieves physical network card identification.
72. **Zero-Dependency HTTP Client:** `@http_get` and `@http_post` use native `urllib` to avoid `requests` bloat inside the engine core.
73. **Process Exorcist:** `@kill_process` handles zombie cleanup via `psutil` or native SIGTERM signals.
74. **Disk Quota Governor:** Prevents file writing if `@disk_space` detects < 5% free space remaining.
75. **Symlink Compatibility Suture:** `@symlink` handles Windows `SeCreateSymbolicLinkPrivilege` automatically or falls back to a hard copy to prevent crashes.
76. **Achronal Ping:** `@ping` measures ICMP latency to external cloud providers for dynamic failover routing in blueprints.
77. **Permission Normalizer:** `@chmod` converts integer octals to POSIX strings and vice-versa seamlessly.
78. **Ownership Projection:** `@chown` gracefully ignores execution on Windows Iron to prevent `AttributeError` panics.
79. **Metabolic Pacing on HTTP:** Rate limits built-in HTTP requests to avoid 429s during automated weaves.
80. **Memory Mapped File Suture:** `@hash_file` updated to use `mmap` for files > 1GB, achieving O(1) RAM usage.
81. **Secure Shell Injection Ward:** Escapes all arguments passed to `@shell_daemon` or `@kill_process`.
82. **JIT Registry Scanning:** The directory structure dynamically imports all sub-files into the `RITE_REGISTRY`.
83. **Cross-Platform Path Validation:** Ensure `@symlink` and `@zip` paths don't escape the project root (The Moat).
84. **File Lock Sentinel:** Verifies files are not locked by other processes before reading/zipping.
85. **Asynchronous HTTP Upgrades:** Prepares the foundation for `aiohttp` adoption if present in the environment.
86. **Socket-Level Timeout Enforcement:** Hard 5s timeout on all network rites.
87. **Process Tree Annihilation:** `@kill_process` terminates the entire process group (PGID), not just the parent shell wrapper.
88. **The Absolute Panopticon Vow:** A mathematical guarantee of Turing-complete OS control.
=================================================================================
"""

from .ai_interaction import *
from .network_http import *
from .filesystem_io import *
from .execution_os import *
from .hardware_vitals import *
from .state_env import *
from .crypto_security import *
from .logic_routing import *
from .legacy_text_suture import *

__all__ =[] # Populated dynamically by the Registry Decorators