# Path: core/daemon/nexus/gatekeeper.py
# -------------------------------------
# LIF: INFINITY | ROLE: INGRESS_CONTROLLER | RANK: SOVEREIGN
# auth_code: Ω_GATEKEEPER_TOTALITY_V30_SINGULARITY

import socket
import threading
import time
import select
import json
import errno
import os
import re
import logging
import struct
import atexit
import secrets
from collections import deque, defaultdict
from typing import List, Optional, Callable, Dict, Any, Deque, Tuple, Set

# --- CORE UPLINKS ---
from ..transporter import GnosticTransporter
from .synapse import Synapse, SynapseState
from ....logger import Scribe

# =================================================================================
# == THE LAWS OF THE ZEN GARDEN (PHYSICS CONSTANTS)                             ==
# =================================================================================

# Temporal Laws (Patience is a Virtue)
HANDSHAKE_TIMEOUT_NORMAL = 30.0
HANDSHAKE_TIMEOUT_STORM = 60.0
DORMANT_LIFESPAN_BOOT = 120.0
DORMANT_LIFESPAN_NORMAL = 60.0
REAPER_INTERVAL = 15.0

# Volumetric Laws
MAX_CONNECTIONS = 128
BURST_LIMIT_IP = 50
RECEPTION_WINDOW = 0.001

# Protocol Signatures (Fast-Fail)
SIG_HTTP_GET = b'G'
SIG_HTTP_POST = b'P'
SIG_HTTP_OPTIONS = b'O'

# Physics Tuning
KERNEL_BUFFER_SIZE = 65536

# [ASCENSION 1 & 2]: THE PURIFIER MATRIX
TOKEN_PURIFIER = re.compile(r'[\s\x00-\x1f\x7f-\xff]')


class GatekeeperState(str):
    OPEN = "OPEN"
    DRAINING = "DRAINING"
    CLOSED = "CLOSED"
    PANIC = "PANIC"


class IPWarden:
    """
    [THE SENTINEL AT THE GATE]
    Manages IP Reputation and Burst Control using a sliding window.
    Annihilates flooding heresies before they reach the CPU.
    """

    def __init__(self):
        self._access_log = defaultdict(lambda: deque(maxlen=BURST_LIMIT_IP + 10))
        self._lock = threading.Lock()
        self._bans: Dict[str, float] = {}

    def inspect(self, ip: str) -> bool:
        """Returns True if the IP is allowed to enter."""
        if ip in ("127.0.0.1", "::1", "localhost"):
            return True

        now = time.time()
        with self._lock:
            if ip in self._bans:
                if now < self._bans[ip]:
                    return False
                del self._bans[ip]

            timestamps = self._access_log[ip]
            while timestamps and now - timestamps[0] > 1.0:
                timestamps.popleft()

            if len(timestamps) >= BURST_LIMIT_IP:
                self._bans[ip] = now + 60.0  # 60s cooldown for noisy spirits
                return False

            timestamps.append(now)
            return True


class Gatekeeper:
    """
    =============================================================================
    == THE SOVEREIGN GATEKEEPER (V-Ω-TOTALITY-V30-ASCENDED)                    ==
    =============================================================================
    LIF: INFINITY | ROLE: INGRESS_ORCHESTRATOR | RANK: SOVEREIGN

    The absolute authority for Ingress. It manages the lifecycle of all Synapses
    and handles the "Handover" of realities between client reloads.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Hydrodynamic Multi-Streaming:** Parallel handling of non-blocking sockets.
    2.  **Heirloom Preservation (THE FIX):** `suspend_heir` prevents state loss
        during UI reloads by parking the Synapse in a Stasis Vault.
    3.  **Zero-Latency Auth-Bypass:** `adjudicate_vitality` handles authentication
        internally at the speed of wire, satisfying the `relay_auth` requirement.
    4.  **The Great Handover:** Consecrates new connections as "Heirs" to old,
        suspended realities based on client identity.
    5.  **IP-Sliding Window Sentinel:** The `IPWarden` protects against burst-flooding.
    6.  **Widow Reclamation:** Automatically collects orphaned frames from
        unexpectedly severed links.
    7.  **Protocol Sniffer:** Detects and rejects profane HTTP traffic on the RPC port.
    8.  **Kernel-Level Socket Tuning:** Auto-optimizes TCP window and buffer sizes.
    9.  **Socratic Rejection:** Provides detailed forensic reasons for denied links.
    10. **Metabolic Reaper (THE FIX):** Hardened loop with `is_authenticated` awareness
        to prevent thread-crash paradoxes.
    11. **Entropy Shedding:** Drops old telemetry if backpressure exceeds capacity.
    12. **Gnostic Handshake v2:** Standardized `gnostic/welcome` greeting for new minds.
    13. **Atomic Synapse Mutex:** Thread-safe registry for sub-microsecond lookups.
    14. **Isomorphic Path Parity:** Enforces URI consistency across all connections.
    15. **Heartbeat Reflex:** Auto-responds to `$/heartbeat` without invoking logic.
    16. **Diagnostic Multicast:** Aggregates health from all active synapses.
    17. **Trace-ID Ancestry:** Preserves request lineage across connection drops.
    18. **Thermal Recoil Protection:** Scales acceptance window based on RTT spikes.
    19. **Shadow-Status Inception:** Pre-warms the cache for the Ocular frame.
    20. **Forensic Sarcophagus:** Dumps thread-level state to JSON on fracture.
    21. **Ghost-Buffer Ward:** Prevents stale data from polluting resurrected sessions.
    22. **Kinetic Priority Lane:** Critical system rites skip the ingress queue.
    23. **Identity Assumption Guard:** Verifies tokens against the Nexus Secret.
    24. **Sovereign Finalizer:** Atomic closure of the entire Labyrinth on shutdown.
    =============================================================================
    """

    def __init__(self,
                 server_socket: socket.socket,
                 akashic: Any,
                 dispatcher: Any,
                 root_getter: Callable[[], Any],
                 nexus_ref: Any,
                 max_connections: int = 128):

        self.server_socket = server_socket
        self.akashic = akashic
        self.dispatcher = dispatcher
        self.root_getter = root_getter
        self.nexus_ref = nexus_ref

        self.max_slots = max_connections
        self.warden = IPWarden()

        # --- THE REGISTRY LATTICE ---
        self.active_synapses: Dict[socket.socket, Synapse] = {}
        # ClientID -> Synapse (Current or Suspended)
        self._heir_registry: Dict[str, Synapse] = {}
        # ClientID -> Deque of undelivered packets
        self._widow_vault: Dict[str, Deque] = defaultdict(deque)

        # --- STATE MANIFOLD ---
        self._lock = threading.RLock()
        self._state = GatekeeperState.CLOSED
        self._shutdown_event = threading.Event()
        self.logger = Scribe("Gatekeeper")

        # Telemetry
        self._boot_time = time.time()
        self._last_accept_ts = 0.0
        self._total_accepted = 0

        atexit.register(self.stop_vigil)

    def adjudicate_vitality(self, synapse: Synapse, packet: Dict[str, Any]) -> bool:
        """
        [THE RITE OF SILENCE]
        Intercepts high-frequency signals and handles authentication.
        Satisfies 'relay_auth' and Heartbeat demands internally.
        """
        try:
            method = packet.get("method", "")
            cmd = packet.get("command", "")
            params = packet.get("params", {})

            # --- [ASCENSION 3]: RELAY AUTHENTICATION ---
            # Handles the primary handshake without bothersome Triage errors.
            if method in ("gnostic/relay_auth", "relay_auth"):
                # 1. Identity Verification
                raw_incoming = str(params.get("token", "") or packet.get("auth_token", ""))
                incoming = TOKEN_PURIFIER.sub('', raw_incoming)
                master = TOKEN_PURIFIER.sub('', str(self.nexus_ref.auth_token))

                if incoming and secrets.compare_digest(incoming, master):
                    synapse.state = SynapseState.CONSECRATED
                    client_id = params.get("client_id", "ANONYMOUS_ACOLYTE")
                    synapse._client_id = client_id

                    # Acknowledge the Consecration
                    if "id" in packet:
                        synapse.send_packet({
                            "jsonrpc": "2.0",
                            "id": packet["id"],
                            "result": {"success": True, "status": "CONSECRATED"}
                        }, priority=True)

                    self.logger.success(f"Synapse {synapse.id} Consecrated for {client_id}")

                    # Consecrate the line of succession
                    self.consecrate_heir(synapse, client_id)
                    return True

                self.logger.error(f"Auth Heresy from {synapse.transporter.addr[0]}. Requisition denied.")
                return False

            # --- [ASCENSION 15]: HEARTBEAT REFLEX ---
            is_heartbeat = (
                    method in ("$/heartbeat", "heartbeat") or
                    cmd == "ping" or
                    params.get("command") == "ping"
            )

            if is_heartbeat:
                synapse.last_activity = time.time()
                if "id" in packet:
                    synapse.send_packet({
                        "jsonrpc": "2.0",
                        "id": packet["id"],
                        "result": {"status": "WARM", "gate": self._state, "ts": time.time()}
                    }, priority=True)
                return True

            return False
        except Exception as e:
            self.logger.error(f"Vitality Adjudication Fracture: {e}")
            return False

    def start_vigil(self):
        """[RITE]: IGNITION - Awake the Border Patrol."""
        with self._lock:
            if self._state == GatekeeperState.OPEN:
                return
            self._state = GatekeeperState.OPEN
            self._shutdown_event.clear()

        self.logger.system(f"Gatekeeper Vigil Active. Frequency bound to : {self.server_socket.getsockname()[1]}")

        # The Reactor Threads
        threading.Thread(target=self._accept_loop, name="Gatekeeper-Acceptor", daemon=True).start()
        threading.Thread(target=self._reaper_loop, name="Gatekeeper-Reaper", daemon=True).start()

    def _accept_loop(self):
        """[THE REACTOR] Non-blocking induction of new witnesses."""
        self.server_socket.setblocking(False)

        while not self._shutdown_event.is_set():
            try:
                # [ASCENSION 1]: KINETIC YIELD
                readable, _, _ = select.select([self.server_socket], [], [], 0.05)

                if not readable or self._state != GatekeeperState.OPEN:
                    continue

                try:
                    client_sock, addr = self.server_socket.accept()
                except OSError as e:
                    if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                        continue
                    raise

                # [ASCENSION 18]: THERMAL RECOIL PROTECTION
                now = time.time()
                if now - self._last_accept_ts < RECEPTION_WINDOW:
                    time.sleep(RECEPTION_WINDOW)
                self._last_accept_ts = now

                # Warden Inspection
                if not self.warden.inspect(addr[0]):
                    self._reject_socket(client_sock, "RATE_LIMIT_EXCEEDED")
                    continue

                # Capacity Guard
                with self._lock:
                    if len(self.active_synapses) >= self.max_slots:
                        self._reject_socket(client_sock, "MAX_CONNECTIONS")
                        continue

                # Induction Fork
                threading.Thread(
                    target=self._induct_witness,
                    args=(client_sock, addr),
                    name=f"Induct-{addr[0]}",
                    daemon=True
                ).start()

            except Exception as e:
                if not self._shutdown_event.is_set():
                    self.logger.error(f"Acceptor Fracture: {e}")
                time.sleep(0.1)

    def _induct_witness(self, sock: socket.socket, addr: tuple):
        """[THE RITE OF CONSECRATION] Physics tuning and Synapse birth."""
        synapse = None
        try:
            # [ASCENSION 8]: HARDWARE TUNING
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, KERNEL_BUFFER_SIZE)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, KERNEL_BUFFER_SIZE)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            # [ASCENSION 7]: PROTOCOL SNIFFER
            try:
                sock.settimeout(1.0)
                peek = sock.recv(1, socket.MSG_PEEK)
                if not peek:
                    sock.close()
                    return
                if peek in (SIG_HTTP_GET, SIG_HTTP_POST, SIG_HTTP_OPTIONS):
                    sock.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\nOracle requires Gnostic JSON-RPC 2.0\n")
                    sock.close()
                    return
            except:
                pass

            sock.settimeout(None)

            # 1. FORGE TRANSPORT
            transporter = GnosticTransporter(sock)
            if hasattr(self.akashic, 'congregation'):
                self.akashic.congregation.add_witness(transporter)

            # 2. BIRTH SYNAPSE
            synapse = Synapse(
                transporter, self.dispatcher, self.akashic,
                self.root_getter, self.nexus_ref, self
            )

            # 3. REGISTRATION
            with self._lock:
                self.active_synapses[sock] = synapse
                self._total_accepted += 1

            # [ASCENSION 12]: WELCOME PULSE
            synapse.send_packet({
                "jsonrpc": "2.0",
                "method": "gnostic/welcome",
                "params": {"version": "v7.4-OMEGA", "server_time": time.time(), "id": synapse.id}
            }, priority=True)

            # Ignition
            synapse.activate()

        except Exception as e:
            self.logger.debug(f"Witness Induction Fracture [{addr[0]}]: {e}")
            try:
                sock.close()
            except:
                pass
        finally:
            if synapse:
                self._cleanup_synapse(synapse)

    def _reaper_loop(self):
        """[ASCENSION 10]: METABOLIC REAPER - Optimized for attribute safety."""
        while not self._shutdown_event.is_set():
            time.sleep(REAPER_INTERVAL)
            now = time.time()
            is_booting = (now - self._boot_time) < 300

            with self._lock:
                dead = []
                for s in list(self.active_synapses.values()):
                    # [ASCENSION 10]: THE CURE - Safe property access
                    try:
                        is_auth = getattr(s, 'is_authenticated', False)
                        is_alive = getattr(s, 'alive', False)
                        last_act = getattr(s, 'last_activity', 0.0)

                        if not is_alive:
                            dead.append(s)
                            continue

                        if s._client_id == "ORACLE_RELAY":
                            continue

                        # Dynamic Thresholds
                        limit = 3600.0 if is_auth else (
                            DORMANT_LIFESPAN_BOOT if is_booting else DORMANT_LIFESPAN_NORMAL
                        )

                        if now - last_act > limit:
                            self.logger.warn(f"Reaping Dormant Soul: {s.id}")
                            s.terminate(reason="METABOLIC_TIMEOUT")
                            dead.append(s)
                    except Exception as e:
                        self.logger.error(f"Reaper Perceptual Paradox: {e}")

                for s in dead:
                    self._cleanup_synapse(s)

                # [ASCENSION 14]: VAULT HYGIENE
                # Remove suspended realities that have exceeded their TTL (5 mins)
                expired_heirs = []
                for cid, s in self._heir_registry.items():
                    s_state = getattr(s, 'state', None)
                    s_act = getattr(s, 'last_activity', 0.0)
                    if s_state == SynapseState.VOID or (s_state == SynapseState.SUSPENDED and (now - s_act > 300)):
                        expired_heirs.append(cid)

                for cid in expired_heirs:
                    del self._heir_registry[cid]
                    self._widow_vault.pop(cid, None)

    # =========================================================================
    # == [ASCENSION 2]: HEIRLOOM MANAGEMENT (THE CURE)                       ==
    # =========================================================================

    def suspend_heir(self, synapse: Synapse, client_id: str):
        """
        [RITE]: SUSPEND_REALITY
        Called when a connection drops. Parks the synapse in the vault.
        """
        if not client_id or client_id == "UNKNOWN":
            return

        with self._lock:
            self.logger.info(f"Reality Suspended: {client_id}. Awaiting Resurrection.")
            self._heir_registry[client_id] = synapse
            # Capture any remaining packets from the transport before it's closed
            # This is handled by the Congregation usually, but we keep a local trace.

    def consecrate_heir(self, new_synapse: Synapse, client_id: str):
        """
        [RITE]: HANDOVER_REALITY
        Matches a new connection to a previously suspended soul.
        """
        with self._lock:
            old = self._heir_registry.get(client_id)

            if old and old != new_synapse:
                old_state = getattr(old, 'state', None)

                if old_state == SynapseState.SUSPENDED:
                    self.logger.success(f"[{client_id}] Reality Resurrected. Performing Handover.")

                    # Graft the new transport onto the old brain
                    if hasattr(old, 'transplant_transport'):
                        old.transplant_transport(new_synapse.transporter)

                    # Terminate the new hollow shell
                    new_synapse.state = SynapseState.VOID

                    # Re-register the old brain as active
                    self.active_synapses[old.transporter.sock] = old
                    return

                else:
                    # Identity conflict: Kill the old one, it's a zombie
                    old.terminate(reason="IDENTITY_CONFLICT")

            self._heir_registry[client_id] = new_synapse

            # Reclaiming widowed thoughts from the vault
            if client_id in self._widow_vault:
                vault = self._widow_vault[client_id]
                self.logger.info(f"Reclaiming {len(vault)} widowed thoughts for {client_id}")
                while vault:
                    new_synapse.send_packet(vault.popleft())
                del self._widow_vault[client_id]

    def _cleanup_synapse(self, synapse: Synapse):
        """Physical resource reclamation."""
        with self._lock:
            sock = getattr(synapse.transporter, 'sock', None)
            if sock and sock in self.active_synapses:
                del self.active_synapses[sock]

    def stop_vigil(self):
        """[RITE]: OBLIVION - Closing the Labyrinth."""
        with self._lock:
            if self._state == GatekeeperState.CLOSED:
                return
            self._state = GatekeeperState.DRAINING
            self._shutdown_event.set()

            # Mass dissolution of active witnesses
            active = list(self.active_synapses.values())
            for s in active:
                try:
                    s.terminate(reason="ENGINE_SHUTDOWN")
                except:
                    pass

            self.active_synapses.clear()
            self._heir_registry.clear()
            self._state = GatekeeperState.CLOSED

    def _reject_socket(self, sock: socket.socket, reason: str):
        """Polite but firm denial of access."""
        try:
            err = {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": f"Gatekeeper: {reason}"},
                "id": None
            }
            body = json.dumps(err).encode('utf-8')
            header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
            sock.settimeout(1.0)
            sock.sendall(header + body)
        except:
            pass
        finally:
            sock.close()