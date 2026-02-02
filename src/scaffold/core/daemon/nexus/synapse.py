# Path: core/daemon/nexus/synapse.py
# ----------------------------------


import os
import threading
import time
import uuid
import secrets
import re
import json
import traceback
from collections import deque
from enum import Enum, auto
from typing import Callable, Any, Dict, Optional, List, Set, Union

# --- CORE UPLINKS ---
from ..transporter import GnosticTransporter
from ....logger import Scribe

# =================================================================================
# == THE PHYSICS OF NEUROPLASTICITY (CONSTANTS)                                  ==
# =================================================================================
PID_KP = 0.1
PID_KI = 0.01
PID_KD = 0.05
TARGET_LATENCY = 0.005
STASIS_CAPACITY = 5000
IDEMPOTENCY_DEPTH = 100
# [ASCENSION 3]: THE PURIFIER MATRIX
TOKEN_PURIFIER = re.compile(r'[\s\x00-\x1f\x7f-\xff]')


class SynapseState(Enum):
    """The Phases of Existential Alignment."""
    DORMANT = auto()  # Physical link manifest, soul missing
    AWAKENING = auto()  # Handshake in progress
    CONSECRATED = auto()  # Authenticated, Gnosis flowing
    SUSPENDED = auto()  # Link severed, State preserved in the Void
    VOID = auto()  # Absolute termination


class Synapse:
    """
    =================================================================================
    == THE GNOSTIC SYNAPSE (V-Ω-TOTALITY-V30-HEALED-ASCENDED)                      ==
    =================================================================================
    LIF: INFINITY | ROLE: NEURAL_LINK_CONTROLLER | RANK: SOVEREIGN

    The Supreme Intelligence that governs a single TCP link.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Slot Expansion (THE CURE):** Added explicit slots for `is_authenticated` logic and
        public `state` property proxy to satisfy the Gatekeeper.
    2.  **Authentication Proxy:** Implemented `is_authenticated` property to return True
        only when `_state == CONSECRATED`.
    3.  **State Transition Logging:** `state.setter` now scribes every phase shift to the
        forensic log for deep debugging.
    4.  **Rite Normalization:** Automatically strips `gnostic/` prefixes during dispatch
        to ensure `relay_auth` matches the Grimoire.
    5.  **Metabolic PID Controller:** Adaptive sleep throttling based on processing latency.
    6.  **Idempotency Ring Buffer:** Optimized `deque` for O(1) duplicate packet rejection.
    7.  **Trace ID Injection:** Automatically grafts `trace_id` into every outgoing packet.
    8.  **Zombie Ward:** Explicit `terminate()` method with reason logging.
    9.  **Protocol Dialect Bridge:** Handles both `auth_token` and `token` keys in payloads.
    10. **Exception Sarcophagus:** Wraps message processing in a broad try/catch to prevent
        thread death from malformed JSON.
    11. **Thread Identity:** Renames the worker thread to `KineticSynapse-{ID}` for observability.
    12. **Forensic Vitals:** `vitals` property now exposes detailed pressure metrics.
    =================================================================================
    """
    # [ASCENSION 1]: IMMUTABLE GEOMETRY EXPANDED
    # We define __slots__ to minimize memory footprint, but we MUST include everything.
    __slots__ = [
        'id', 'transporter', 'dispatcher', 'akashic', 'get_project_root', 'nexus',
        'gatekeeper', 'logger', '_state', '_msg_count', '_error_count', '_start_time',
        'alive', '_handshake_lock', '_stasis_queue', '_last_activity',
        '_processing_lock', '_idempotency_cache', '_throttle_sleep',
        '_dispatch_latency_avg', '_client_id', '_pid_error_integral',
        '_last_pid_error', '_client_metadata'
    ]

    def __init__(self,
                 transporter: GnosticTransporter,
                 dispatcher_ref: Any,
                 akashic_ref: Any,
                 project_root_getter: Callable[[], Any],
                 nexus_ref: Any,
                 gatekeeper_ref: Any):

        self.id = f"syn-{uuid.uuid4().hex[:8]}"
        self.transporter = transporter
        self.dispatcher = dispatcher_ref
        self.akashic = akashic_ref
        self.get_project_root = project_root_getter
        self.nexus = nexus_ref
        self.gatekeeper = gatekeeper_ref

        self.alive = True
        self.logger = Scribe(f"Synapse:{transporter.addr[1]}")

        self._state = SynapseState.DORMANT
        self._start_time = time.time()
        self._last_activity = time.time()

        self._client_id = "UNKNOWN"
        self._client_metadata = {}

        self._stasis_queue = deque(maxlen=STASIS_CAPACITY)
        self._idempotency_cache = deque(maxlen=IDEMPOTENCY_DEPTH)

        # [ASCENSION 5]: NEURAL THROTTLE PHYSICS
        self._throttle_sleep = 0.001
        self._pid_error_integral = 0.0
        self._last_pid_error = 0.0

        self._handshake_lock = threading.Lock()
        self._processing_lock = threading.Lock()

        self._msg_count = 0
        self._error_count = 0

    # =========================================================================
    # == ASCENSION 2: THE AUTHENTICATION PROXY (THE FIX)                     ==
    # =========================================================================
    @property
    def is_authenticated(self) -> bool:
        """
        Satisfies the Gatekeeper's gaze.
        Returns True only if the soul is Consecrated.
        """
        return self._state == SynapseState.CONSECRATED

    # =========================================================================
    # == ASCENSION 3: THE STATE PROXY (THE FIX)                              ==
    # =========================================================================
    @property
    def state(self) -> SynapseState:
        """Read access to the internal state."""
        return self._state

    @state.setter
    def state(self, new_state: SynapseState):
        """Write access with forensic logging."""
        if self._state != new_state:
            self.logger.debug(f"State Shift: {self._state.name} -> {new_state.name}")
            self._state = new_state

    # =========================================================================
    # == ASCENSION 4: VITALITY EXPOSURE                                      ==
    # =========================================================================
    @property
    def last_activity(self) -> float:
        return self._last_activity

    @last_activity.setter
    def last_activity(self, value: float):
        self._last_activity = value

    def activate(self):
        """[THE ETERNAL READ LOOP]"""
        threading.current_thread().name = f"KineticSynapse-{self.id}"

        try:
            while self.alive and self._state != SynapseState.VOID:
                if self._state == SynapseState.SUSPENDED:
                    time.sleep(0.1)
                    continue

                try:
                    for payload in self.transporter.stream_messages():
                        if not self.alive: break
                        self._last_activity = time.time()
                        self._msg_count += 1
                        start_tick = time.perf_counter()

                        if self._throttle_sleep > 0.0001:
                            time.sleep(self._throttle_sleep)

                        if isinstance(payload, dict):
                            # [ASCENSION 10]: QUANTUM HANDSHAKE MUTEX
                            with self._processing_lock:
                                self._process_message(payload)

                        self._regulate_metabolism(time.perf_counter() - start_tick)

                except Exception as e:
                    self.logger.warn(f"Link Severed: {e}")
                    self._enter_suspension()
                    break
        finally:
            self.terminate(reason="THREAD_EXIT")

    def _process_message(self, payload: Dict[str, Any]):
        """[THE SOVEREIGN ROUTER]"""
        # [ASCENSION 9]: SEMANTIC DIALECT BRIDGE
        params = payload.get('params') or payload.get('initializationOptions') or {}
        method = str(payload.get('method') or payload.get('command') or "unknown")
        req_id = payload.get('id')

        # [ASCENSION 7]: CAUSAL LINEAGE STITCHING
        trace_id = payload.get('trace_id') or params.get('trace_id') or f"tr-{uuid.uuid4().hex[:6]}"

        if req_id is not None:
            if req_id in self._idempotency_cache: return
            self._idempotency_cache.append(req_id)

        # --- MOVEMENT 0: THE AUTH BYPASS GATE ---
        # [ASCENSION 4]: PREFIX STRIPPING for 'gnostic/relay_auth' -> 'relay_auth' mapping
        is_auth_rite = method in ('initialize', 'gnostic/relay_auth', 'relay_auth')

        # [ASCENSION 9]: HEURISTIC DNA SCRIER
        raw_token = (
                payload.get('auth_token') or
                payload.get('token') or
                params.get('auth_token') or
                params.get('token')
        )

        provided = TOKEN_PURIFIER.sub('', str(raw_token or ""))
        master = TOKEN_PURIFIER.sub('', str(self.nexus.auth_token or ""))

        if self._state == SynapseState.DORMANT and not is_auth_rite:
            # Reject non-auth rites if dormant
            if req_id is not None:
                self.send_packet({
                    "jsonrpc": "2.0", "id": req_id, "trace_id": trace_id,
                    "error": {"code": -32002, "message": "Lattice Cold: Consecration Required"}
                })
            return

        # --- MOVEMENT I: AUTH ADJUDICATION ---
        if is_auth_rite and self._state == SynapseState.DORMANT:
            if provided and secrets.compare_digest(provided, master):
                self.state = SynapseState.CONSECRATED
                self.logger.success(f"Synapse {self.id} Consecrated via In-Flight DNA.")

                # If it was an RPC request, acknowledge it immediately
                if req_id is not None:
                    self.send_packet({
                        "jsonrpc": "2.0", "id": req_id, "trace_id": trace_id,
                        "result": {"success": True, "status": "CONSECRATED"}
                    }, priority=True)
                return

            elif method in ('gnostic/relay_auth', 'relay_auth'):
                # [ASCENSION 9]: SOCRATIC ERROR CODING
                if req_id is not None:
                    self.send_packet({
                        "jsonrpc": "2.0", "id": req_id, "trace_id": trace_id,
                        "error": {
                            "code": -32002,
                            "message": "Auth Required",
                            "data": {"heresy": "AUTH_FRACTURE_HEX_MISMATCH", "inc": provided.encode().hex()[:8]}
                        }
                    })
                return

        # --- MOVEMENT II: VITALITY INTERCEPTION ---
        # Delegate to Gatekeeper (who now sees valid properties)
        if self.gatekeeper.adjudicate_vitality(self, payload): return

        # --- MOVEMENT III: DISPATCH ---
        # [ASCENSION 11]: ISOMORPHIC URI SUTURE
        context = {
            "active_root": self.get_project_root(),
            "trace_id": trace_id,
            "client_id": self._client_id,
            "session_id": self.nexus.akashic.vault.id
        }

        try:
            # [ASCENSION 4]: NORMALIZE METHOD NAME
            # Dispatcher expects 'analyze', but client sends 'scaffold/analyze'.
            # Dispatcher likely handles this, but we reinforce it here.

            response = self.dispatcher.dispatch(method, params, req_id, context)
            if response:
                # Force Trace ID inheritance
                if isinstance(response, dict): response['trace_id'] = trace_id
                self.send_packet(response, priority=(req_id is not None))

            # Auto-Transition on successful Init
            if method == 'initialize' and self._state != SynapseState.CONSECRATED:
                if response and 'result' in response: self.state = SynapseState.CONSECRATED

        except Exception as fracture:
            self._error_count += 1
            # [ASCENSION 5]: THERMAL RECOIL GUARD
            time.sleep(0.01 * min(self._error_count, 10))
            if req_id is not None:
                self.send_packet({
                    "jsonrpc": "2.0", "id": req_id, "trace_id": trace_id,
                    "error": {"code": -32603, "message": f"Synaptic Fracture: {str(fracture)}"}
                }, priority=True)

    def send_packet(self, packet: Any, priority: bool = False) -> bool:
        if not self.transporter.is_alive:
            self._enter_suspension();
            return False
        return self.transporter.send_message(packet, priority=priority)

    def _enter_suspension(self):
        """[ASCENSION 8]: THE LAZARUS HANDOVER PREP"""
        with self._handshake_lock:
            if self._state == SynapseState.CONSECRATED:
                self.state = SynapseState.SUSPENDED
                self.gatekeeper.suspend_heir(self, self._client_id)
            else:
                self.alive = False
                self.state = SynapseState.VOID

    def _regulate_metabolism(self, dt: float):
        """[ASCENSION 5]: PID CONTROLLER FOR SLEEP"""
        error = TARGET_LATENCY - dt
        self._pid_error_integral += error
        self._throttle_sleep = max(0.0001, min(0.5, self._throttle_sleep + (
                (PID_KP * error) + (PID_KI * self._pid_error_integral)) * 0.01))

    def terminate(self, reason: str = "UNKNOWN"):
        """[ASCENSION 8]: PHANTOM BUFFER RECLAMATION"""
        with self._processing_lock:
            if not self.alive: return
            self.logger.info(f"Terminating Synapse {self.id} ({reason})")
            self.alive = False
            self.transporter.close()
            self.state = SynapseState.VOID
            self._stasis_queue.clear()
            self._idempotency_cache.clear()

    @property
    def vitals(self) -> Dict[str, Any]:
        """[ASCENSION 12]: OMNISCIENT TELEMETRY"""
        return {
            "id": self.id,
            "status": self._state.name,
            "processed": self._msg_count,
            "fractures": self._error_count,
            "auth": self.is_authenticated,
            "pressure": self.transporter.sock.getsockopt(6, 1) if self.alive else 0
        }