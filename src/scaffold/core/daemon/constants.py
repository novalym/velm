# Path: core/daemon/constants.py
# ------------------------------
# LIF: INFINITY | ROLE: IMMUTABLE_LAW_TABLE | AUTH_CODE: Ω_CONSTANTS_V99
# =================================================================================
# == THE TABLE OF CONSTANTS (V-Ω-IMMUTABLE-LAW)                                  ==
# =================================================================================
# [PURPOSE]: The single source of truth for all hardcoded physics within the
#            Gnostic Daemon. Changing a value here alters the fundamental
#            behavior of the system.
#
# [SECTIONS]:
# 1. PROTOCOL IDENTITY
# 2. NETWORK PHYSICS
# 3. TEMPORAL GOVERNANCE (TIMEOUTS)
# 4. MEMORY & BUFFER LIMITS
# 5. CONCURRENCY STRATA
# 6. FILESYSTEM ANCHORS
# 7. TELEMETRY CONFIGURATION

import os

# =================================================================================
# == 1. PROTOCOL IDENTITY                                                        ==
# =================================================================================
# The handshake version string sent to the Electron client.
# Bump this when changing the JSON-RPC schema to force client-side re-validation.
PROTOCOL_VERSION = "2.3.0-HEALED"

# The internal name of the service, used for process tagging and logging headers.
DAEMON_IDENTITY = "GnosticNexus"

# =================================================================================
# == 2. NETWORK PHYSICS                                                          ==
# =================================================================================
# The default localhost binding.
# [ASCENSION]: We use 127.0.0.1 to avoid IPv6 '::1' resolution lags on Windows/Node.
DEFAULT_HOST = "127.0.0.1"

# The default TCP port. If occupied, the Nexus will hunt for the next available one
# (e.g. 5556, 5557...).
DEFAULT_PORT = 5555

# The maximum number of pending connections in the OS backlog.
# 50 is sufficient for a local dev tool; protects against SYN flood instability.
MAX_CONNECTIONS = 50

# TCP Socket Options
# Enable TCP_NODELAY (Nagle's Algorithm disabled) for lower latency RPC calls.
ENABLE_TCP_NODELAY = True

# Enable SO_KEEPALIVE to detect severed links from crashed clients immediately.
ENABLE_KEEP_ALIVE = True

# =================================================================================
# == 3. TEMPORAL GOVERNANCE (TIMEOUTS)                                           ==
# =================================================================================
# [CORTEX TIER]: Time limit for high-frequency intelligence (LSP, Hover, Completion).
# These operations must be near-instant. If they hang, we cut them loose to free threads.
TIMEOUT_CORTEX = 30.0  # Seconds

# [FOUNDRY TIER]: Time limit for heavy kinetic rites (Genesis, Distill, Install, Docker).
# These operations involve Disk I/O, Network calls, and massive computation.
TIMEOUT_FOUNDRY = 300.0  # 5 Minutes

# The default timeout if no specific tier is assigned by the Dispatcher.
DEFAULT_TIMEOUT = 60.0

# The interval at which the Daemon checks for the Parent PID or Pulse File updates.
HEARTBEAT_INTERVAL = 2.0  # Seconds

# =================================================================================
# == 4. MEMORY & BUFFER LIMITS                                                   ==
# =================================================================================
# [AKASHIC RECORD]: The number of past logs to keep in the ring buffer.
# Used for the "Temporal Replay" when a new client connects (e.g., page refresh).
MAX_LOG_HISTORY = 2000

# [TRANSPORTER]: The size of the read chunk from the kernel socket.
# 65536 bytes (64KB) aligns with L1 CPU cache pages on many modern architectures.
DEFAULT_CHUNK_SIZE = 65536

# [TRANSPORTER]: The maximum allowed size for a single JSON-RPC message body.
# 64MB prevents memory exhaustion attacks (DoS) from rogue clients sending infinite streams.
MAX_PAYLOAD_SIZE = 64 * 1024 * 1024

# =================================================================================
# == 5. CONCURRENCY STRATA                                                       ==
# =================================================================================
# [CORTEX POOL]: Threads reserved for fast, CPU-bound intelligence tasks.
# Higher count to handle bursty autocomplete/hover requests without blocking.
POOL_SIZE_CORTEX = 12

# [FOUNDRY POOL]: Threads reserved for slow, I/O-bound kinetic tasks.
# Lower count to prevent disk thrashing or network saturation during heavy loads.
POOL_SIZE_FOUNDRY = 8

# [CONCLAVE POOL]: Threads for general system management and socket accepting.
POOL_SIZE_WORKERS = 20

# The maximum depth of the work queue before the Dispatcher applies Backpressure
# and rejects new requests with "HERESY_CONGESTION".
MAX_QUEUE_DEPTH = 64

# =================================================================================
# == 6. FILESYSTEM ANCHORS                                                       ==
# =================================================================================
# The hidden directory where the Daemon stores its state, logs, and locks.
SCAFFOLD_DIR = ".scaffold"

# [ASCENSION 1]: THE SESSION SANCTUM
# The root folder for all unique execution lifecycles.
SESSIONS_DIR = os.path.join(SCAFFOLD_DIR, "sessions")

# [ASCENSION 2]: THE GNOSTIC POINTER
# A text-based reference to the most recent session folder.
# Enables O(1) discovery for the Time Machine without scanning the disk.
LATEST_SESSION_REF = os.path.join(SCAFFOLD_DIR, "latest_session.txt")

# [ASCENSION 3]: DYNAMIC LOG PATTERNS
# The name of the traffic log scripture within each session vault.
TRAFFIC_LOG_NAME = "traffic.jsonl"

# [ASCENSION 4]: FORENSIC MANIFESTS
# The scrolls that describe the beginning and end of a session's reality.
SESSION_MANIFEST = "manifest.json"
SESSION_SNAPSHOT = "snapshot.json"

# [ASCENSION 9]: LEGACY BRIDGE
# Maintained for backward compatibility with un-ascended artisans.
# New logic in AkashicRecord now prioritizes the PID-scoped Vault structure.
TRAFFIC_LOG_FILE = os.path.join(SCAFFOLD_DIR, "daemon_traffic.jsonl")

# =================================================================================
# == SECTION 8: TEMPORAL GOVERNANCE & RETENTION                                  ==
# =================================================================================
# [ASCENSION 5]: THE EVENT HORIZON
# The maximum mass (bytes) a single session can reach before cauterization.
MAX_SESSION_MASS = 100 * 1024 * 1024  # 100MB

# [ASCENSION 6]: THE RETENTION LIMIT
# The maximum number of historical timelines to preserve in the Vault.
MAX_SESSION_COUNT = 5

# [ASCENSION 7]: THE ABYSSAL TTL
# The time (hours) after which a session is considered ancient and reclaimable.
SESSION_TTL_HOURS = 24

# [ASCENSION 10]: ATOMIC BUFFER TUNING
# The chunk size for disk I/O, optimized for modern NVMe and CPU cache lines.
LOG_BUFFER_SIZE = 65536  # 64KB

# [ASCENSION 8]: ARCHIVE SIGNATURE
# The sigil used for compressed historical logs.
COMPRESSION_SIGIL = ".gz"

# The file where catastrophic stack traces are dumped before death.
CRASH_DUMP_FILE = os.path.join(SCAFFOLD_DIR, "daemon_crash.json")

# The file used for the "Pulse" heartbeat mechanism (Lifecycle Manager).
PULSE_FILE_NAME = "daemon.pulse"

# =================================================================================
# == 7. TELEMETRY CONFIGURATION                                                  ==
# =================================================================================
# Whether to emit "kinetic" level logs (verbose movement data) by default.
LOG_KINETICS = True

# Whether to scrub ANSI color codes from logs before broadcasting (UI safety).
# The Daemon logs raw ANSI to stdout/file for terminals, but strips it for JSON-RPC.
SCRUB_ANSI_FOR_RPC = True

# The semantic keys used to tag log entries for routing in the Akashic Record.
TAG_HERESY = "HERESY"
TAG_KINETIC = "KINETIC"
TAG_INTERNAL = "INTERNAL_BRIDGE"

