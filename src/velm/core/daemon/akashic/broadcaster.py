# Path: core/daemon/akashic/broadcaster.py
# ----------------------------------------

import socket
import threading
import json
import select
import time
import uuid
import logging
from collections import deque
from typing import Set, List, Dict, Any, Optional, Tuple, NamedTuple, Deque

from ..transporter import GnosticTransporter

# --- PHYSICS CONSTANTS ---
MAX_SURGE_DEPTH = 5000  # Max logs before shedding
MUTINY_THRESHOLD_SEC = 15.0  # How long a client can be choked before exorcism
PUMP_PULSE_RATE = 0.001  # 1ms Sleep rhythm
LOCKED_SEND_TIMEOUT = 1.0  # Absolute limit for socket write attempt

# --- SEMANTIC PRIORITY ---
HIGH_PRIORITY_METHODS = {
    'textDocument/publishDiagnostics',
    'scaffold/jobComplete',
    'project/status',
    '$/heartbeat',
    'scaffold/progress',
    'window/showMessage'
}

class WitnessState:
    """
    [THE WITNESS VESSEL]
    Holds the mutable state of a single connected mind in the lattice.
    """
    __slots__ = [
        'transporter', 'socket', 'high_queue', 'low_queue',
        'last_drain_time', 'total_sent', 'id'
    ]

    def __init__(self, transporter: GnosticTransporter):
        self.transporter = transporter
        self.socket = transporter.sock
        self.id = transporter.id

        # [ASCENSION 3]: PRIORITY LANES
        self.high_queue: Deque[bytes] = deque()
        self.low_queue: Deque[bytes] = deque()

        # Vitality Tracking
        self.last_drain_time = time.time()
        self.total_sent = 0

    @property
    def is_choked(self) -> bool:
        return bool(self.high_queue or self.low_queue)

    @property
    def total_backlog(self) -> int:
        return len(self.high_queue) + len(self.low_queue)


class Congregation:
    """
    =================================================================================
    == THE HYDRODYNAMIC ENGINE (V-Ω-SURGE-PROTECTED-FINAL)                         ==
    =================================================================================
    The Supreme Broadcast Engine. It manages the physics of the Neural Link.
    """

    def __init__(self):
        # Registry: Map[socket, WitnessState]
        self._registry: Dict[socket.socket, WitnessState] = {}
        # ID Map: Map[id, WitnessState]
        self._id_map: Dict[str, WitnessState] = {}

        self._lock = threading.RLock()
        self._stop_event = threading.Event()

        # Telemetry
        self.total_broadcasts = 0
        self.surge_events = 0
        self.shed_events = 0

        # [THE CURE]: SUBSTRATE DETECTION
        # We determine if we are in the Ethereal Plane (WASM/Pyodide)
        import sys
        import os
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # [ASCENSION 1]: CONDITIONAL PUMP IGNITION
        # Background threads are a heresy in standard WASM runtimes.
        self._pump_thread = threading.Thread(
            target=self._hydrodynamic_pump,
            name="AkashicPump",
            daemon=True
        )

        if not self._is_wasm:
            self._pump_thread.start()
        else:
            logging.getLogger("Congregation").debug("WASM Substrate perceived. Congregation operating in Passive Mode.")

        self.logger = logging.getLogger("Congregation")

    # =========================================================================
    # == THE RITE OF DISSOLUTION (THE FIX)                                   ==
    # =========================================================================

    def close_all(self):
        """
        [ASCENSION 1]: THE ATOMIC SHUTDOWN
        Gracefully severs all links and collapses the background engine.
        """
        self.logger.info("Initiating Congregation Dissolution...")

        # 1. Stop the Pump
        self._stop_event.set()

        # [THE FIX]: Only join the pump if it was actually started (Non-WASM)
        if not self._is_wasm and self._pump_thread.is_alive():
            try:
                self._pump_thread.join(timeout=2.0)
            except:
                pass

        # 2. Banish the Witnesses
        with self._lock:
            sockets = list(self._registry.keys())
            for sock in sockets:
                try:
                    self.remove_witness(sock)
                except:
                    pass

            self._registry.clear()
            self._id_map.clear()

        self.logger.info("Congregation Dissolved. Sockets Returned to Void.")

    # =========================================================================
    # == THE RITE OF CONSECRATION                                            ==
    # =========================================================================

    def add_witness(self, transporter: GnosticTransporter):
        """Consecrates a new listener in the registry."""
        with self._lock:
            state = WitnessState(transporter)
            self._registry[transporter.sock] = state
            self._id_map[transporter.id] = state
            self.logger.debug(f"Witness Consecrated: {transporter.id}")

    def remove_witness(self, sock: socket.socket) -> Dict[str, List[bytes]]:
        """
        [ASCENSION 6]: WIDOW RECLAMATION
        Removes a mind and returns its undelivered thoughts.
        """
        with self._lock:
            if sock not in self._registry:
                return {}

            state = self._registry.pop(sock)
            if state.id in self._id_map:
                del self._id_map[state.id]

            # Reclaim undelivered frames
            widowed = {
                'high': list(state.high_queue),
                'low': list(state.low_queue)
            }

            try:
                state.transporter.close()
            except:
                pass

            return widowed

    # =========================================================================
    # == THE RITE OF PROJECTION (MULTICAST)                                  ==
    # =========================================================================

    def multicast(self, packet: Dict[str, Any]):
        """
        [ASCENSION 2 & 3]: PRE-SERIALIZED PROJECTION
        Transmutes a thought-form into a binary frame and injects it into
        the queues of all connected witnesses.
        """
        if not packet: return

        # 1. TRACE INJECTION
        if 'trace_id' not in packet:
            packet['trace_id'] = f"bc-{uuid.uuid4().hex[:6]}"

        method = packet.get('method', '')
        is_high_priority = method in HIGH_PRIORITY_METHODS

        # [ASCENSION 2]: ATOMIC SERIALIZATION
        # We serialize exactly once to bytes before touching the registry.
        try:
            body = json.dumps(packet, default=str).encode('utf-8')
            # Forge standard LSP frame: Content-Length: n\r\n\r\n{...}
            header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
            binary_frame = header + body
        except Exception as e:
            self.logger.error(f"Serialization Fracture: {e}")
            return

        with self._lock:
            targets = list(self._registry.values())
            if not targets: return

            self.total_broadcasts += 1

            for witness in targets:
                # [ASCENSION 2]: SURGE CHECK
                # If the witness is already backlogged, enqueue immediately to preserve order.
                if witness.is_choked:
                    self._enqueue(witness, binary_frame, is_high_priority)
                    continue

                # Attempt Direct Projection
                # priority=False in send_raw allows a non-blocking attempt
                success = witness.transporter.send_raw(binary_frame, priority=False)

                if success:
                    witness.total_sent += 1
                else:
                    # [SURGE DETECTED]: Buffer into the memory tanks
                    self._enqueue(witness, binary_frame, is_high_priority)

    def _enqueue(self, witness: WitnessState, frame: bytes, is_high: bool):
        """Buffers binary frames into the appropriate lane."""
        self.surge_events += 1
        if is_high:
            witness.high_queue.append(frame)
        else:
            # [ASCENSION 11]: ENTROPY SHEDDING
            if len(witness.low_queue) >= MAX_SURGE_DEPTH:
                witness.low_queue.popleft()
                self.shed_events += 1
            witness.low_queue.append(frame)

    # =========================================================================
    # == THE HYDRODYNAMIC PUMP (BACKGROUND LOOP)                             ==
    # =========================================================================

    def _hydrodynamic_pump(self):
        """
        [ASCENSION 5]: THE PUMP LOOP
        Background thread that monitors choked sockets and drains them.
        """
        while not self._stop_event.is_set():
            try:
                # 1. Filter the Choked
                with self._lock:
                    choked = [w for w in self._registry.values() if w.is_choked]

                if not choked:
                    time.sleep(PUMP_PULSE_RATE * 10)
                    continue

                # 2. Matrix Mapping for Select
                sock_map = {w.socket: w for w in choked}
                sockets = list(sock_map.keys())

                # 3. OS Level Poll
                # timeout=0.01 keeps the loop responsive to shutdown signals
                try:
                    _, writable, errors = select.select([], sockets, sockets, 0.01)
                except (ValueError, OSError):
                    # Handle bad file descriptors (WinError 10038/10053)
                    time.sleep(0.01)
                    continue

                # 4. Drain the Writable
                for sock in writable:
                    witness = sock_map.get(sock)
                    if witness:
                        self._drain_witness(witness)

                # 5. [ASCENSION 6]: ZOMBIE EXORCISM
                now = time.time()
                for sock in errors:
                    self.remove_witness(sock)

                for witness in choked:
                    if now - witness.last_drain_time > MUTINY_THRESHOLD_SEC:
                        self.logger.warning(f"Exorcising Witness {witness.id}: Socket Unresponsive.")
                        self.remove_witness(witness.socket)

                time.sleep(PUMP_PULSE_RATE)

            except Exception as e:
                if not self._stop_event.is_set():
                    # self.logger.error(f"Pump Fracture: {e}")
                    time.sleep(0.1)

    def _drain_witness(self, witness: WitnessState):
        """Drains the High queue then the Low queue until blocked again."""
        witness.last_drain_time = time.time()

        # 1. High Priority First
        while witness.high_queue:
            frame = witness.high_queue[0]
            if witness.transporter.send_raw(frame, priority=True):
                witness.high_queue.popleft()
                witness.total_sent += 1
            else:
                return  # Blocked again

        # 2. Low Priority Second
        while witness.low_queue:
            frame = witness.low_queue[0]
            if witness.transporter.send_raw(frame, priority=True):
                witness.low_queue.popleft()
                witness.total_sent += 1
            else:
                return  # Blocked again

    def get_witness_by_id(self, transporter_id: str) -> Optional[GnosticTransporter]:
        with self._lock:
            state = self._id_map.get(transporter_id)
            return state.transporter if state else None

    def get_census(self) -> Dict[str, Any]:
        """[ASCENSION 12]: THE CENSUS ORACLE"""
        with self._lock:
            snap = [
                {
                    "id": w.id,
                    "hq_depth": len(w.high_queue),
                    "lq_depth": len(w.low_queue),
                    "sent": w.total_sent
                }
                for w in self._registry.values()
            ]
            return {
                "active_witnesses": len(self._registry),
                "total_broadcasts": self.total_broadcasts,
                "surge_events": self.surge_events,
                "shed_events": self.shed_events,
                "census": snap
            }

# == CONGREGATION_ASCENSION: COMPLETE ==