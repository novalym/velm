# path: scaffold/core/chaos_engine.py

import builtins
import http.client
import os
import random
import re
import socket
import threading
import time
from typing import Any, Dict, List, Optional, Callable

from ..logger import Scribe

Logger = Scribe("ChaosEngine")


class ChaosEngine:
    """
    =================================================================================
    == THE GOD-ENGINE OF ENTROPY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                   ==
    =================================================================================
    LIF: ∞ (THE HEART OF THE STORM)

    This divine artisan is the surgical hand of controlled chaos. It receives a
    declarative Gnostic scripture of calamities and performs the sacred and dangerous
    rite of monkey-patching the universe. It is the ultimate instrument for forging
    anti-fragile realities.
    =================================================================================
    """

    def __init__(self, settings: List[Dict[str, Any]]):
        """The Engine is born with its sacred scripture of chaos."""
        self.settings = settings
        self._originals: Dict[str, Any] = {}
        self.events_triggered: List[str] = []
        self._is_active = False
        self._resource_vampires: List[threading.Thread] = []

    def _get_setting(self, chaos_type: str) -> Optional[Dict[str, Any]]:
        """Finds the config for a specific type of chaos."""
        return next((s for s in self.settings if s.get("type") == chaos_type), None)

    def _should_inject(self, chaos_type: str, **kwargs: Any) -> bool:
        """
        [FACULTY 9] The Quantum Die. Adjudicates probability and targeting.
        """
        setting = self._get_setting(chaos_type)
        if not setting:
            return False

        # 1. Adjudicate Probability
        if random.random() >= setting.get("probability", 0.0):
            return False

        # 2. Adjudicate Target (Surgical Gaze)
        target = setting.get("target")
        if target:
            # Match against provided context (e.g., host, path)
            context_value = kwargs.get(setting.get("target_key", "default"))
            if not context_value or not re.search(target, str(context_value)):
                return False

        # If all checks pass, the chaos is willed.
        event_description = f"{chaos_type}"
        if target:
            event_description += f" (target: {target})"
        self.events_triggered.append(event_description)
        return True

    def inject(self):
        """The Rite of Injection: Replaces pure functions with chaotic ones."""
        if self._is_active: return
        Logger.warn(f"[CHAOS] The God-Engine of Entropy awakens. Warping the laws of this reality...")

        # --- The Pantheon of Chaos ---
        self._inject_network_chaos()
        self._inject_io_chaos()
        self._inject_time_chaos()
        self._inject_resource_chaos()

        self._is_active = True

    def retract(self):
        """[FACULTY 4] The Unbreakable Vow of Restoration."""
        if not self._is_active: return
        Logger.info("[CHAOS] The laws of physics are restored. Reality is pure again.")

        # Stop resource vampires
        for vampire in self._resource_vampires:
            vampire.do_run = False
            vampire.join(timeout=0.5)

        # Restore original functions
        for key, original_func in self._originals.items():
            module, func_name = key.split('.')
            if module == 'socket':
                setattr(socket.socket, func_name, original_func)
            elif module == 'builtins':
                setattr(builtins, func_name, original_func)
            elif module == 'time':
                setattr(time, func_name, original_func)

        self._originals.clear()
        self._is_active = False

    # =============================================================================
    # == THE PANTHEON OF CHAOTIC RITES                                           ==
    # =============================================================================

    def _inject_network_chaos(self):
        """Warps the fabric of the network."""
        if not (self._get_setting("network_latency") or self._get_setting("network_failure")):
            return

        if 'socket.connect' not in self._originals:
            original_connect = socket.socket.connect
            self._originals['socket.connect'] = original_connect

            def chaotic_connect_wrapper(sock_instance, address):
                is_local = isinstance(address, tuple) and address[0] in ('127.0.0.1', 'localhost')
                target_host = address[0] if isinstance(address, tuple) else "unknown"

                if self._should_inject("network_latency", host=target_host):
                    delay = random.uniform(0.1, 1.5)
                    Logger.warn(f"[CHAOS] Injecting {delay:.2f}s latency into connection to {address}...")
                    time.sleep(delay)

                if self._should_inject("network_failure", host=target_host):
                    Logger.error(f"[CHAOS] Injecting connection failure for {address}!")
                    raise ConnectionRefusedError(f"Chaos Engine: Connection to {address} forcefully refused.")

                return original_connect(sock_instance, address)

            socket.socket.connect = chaotic_connect_wrapper

    def _inject_io_chaos(self):
        """Warps the fabric of the filesystem."""
        if not (self._get_setting("io_latency") or self._get_setting("io_failure") or self._get_setting(
                "io_corruption")):
            return

        if 'builtins.open' not in self._originals:
            original_open = builtins.open
            self._originals['builtins.open'] = original_open

            def chaotic_open_wrapper(file, *args, **kwargs):
                file_path = str(file)

                if self._should_inject("io_latency", path=file_path):
                    time.sleep(random.uniform(0.05, 0.5))

                if self._should_inject("io_failure", path=file_path):
                    Logger.error(f"[CHAOS] Injecting I/O failure for path: {file_path}")
                    raise OSError(f"Chaos Engine: I/O operation on '{file_path}' failed.")

                file_obj = original_open(file, *args, **kwargs)

                if self._should_inject("io_corruption", path=file_path) and 'w' in file_obj.mode:
                    original_write = file_obj.write

                    def chaotic_write(data):
                        Logger.warn(f"[CHAOS] Corrupting write to {file_path}!")
                        # Flip some bits
                        if isinstance(data, str):
                            char_list = list(data)
                            idx = random.randint(0, len(char_list) - 1)
                            char_list[idx] = 'X'
                            data = "".join(char_list)
                        elif isinstance(data, bytes):
                            byte_list = bytearray(data)
                            idx = random.randint(0, len(byte_list) - 1)
                            byte_list[idx] = byte_list[idx] ^ 0xFF  # XOR flip
                            data = bytes(byte_list)
                        return original_write(data)

                    file_obj.write = chaotic_write

                return file_obj

            builtins.open = chaotic_open_wrapper

    def _inject_time_chaos(self):
        """[FACULTY 3] Warps the fabric of time."""
        if not self._get_setting("time_warp"):
            return

        if 'time.sleep' not in self._originals:
            original_sleep = time.sleep
            self._originals['time.sleep'] = original_sleep

            def chaotic_sleep(duration):
                if self._should_inject("time_warp"):
                    warp_factor = random.uniform(0.1, 5.0)  # Can be faster or slower
                    new_duration = duration * warp_factor
                    Logger.warn(f"[CHAOS] Time Warp! sleep({duration:.2f}s) became sleep({new_duration:.2f}s).")
                    return original_sleep(new_duration)
                return original_sleep(duration)

            time.sleep = chaotic_sleep

    def _inject_resource_chaos(self):
        """[FACULTY 5] Summons the Resource Vampires."""
        if self._should_inject("memory_spike"):
            Logger.error("[CHAOS] Summoning Memory Vampire...")

            def memory_vampire():
                # Allocate a large chunk of memory
                try:
                    _ = bytearray(int(random.uniform(256, 1024) * 1024 * 1024))  # 256MB to 1GB
                    Logger.warn("[CHAOS] Memory Vampire has feasted.")
                except MemoryError:
                    raise MemoryError("Chaos Engine: Simulated OOM Killer.")

            # This is a one-shot spike
            threading.Thread(target=memory_vampire).start()

        if self._should_inject("cpu_spike"):
            Logger.warn("[CHAOS] Summoning CPU Vampire...")

            def cpu_vampire(thread_ref):
                while getattr(thread_ref, "do_run", True):
                    _ = [i * i for i in range(1000)]  # Burn cycles
                    time.sleep(0.01)
                Logger.warn("[CHAOS] CPU Vampire returns to the void.")

            vampire_thread = threading.Thread(target=cpu_vampire, args=(threading.current_thread(),), daemon=True)
            vampire_thread.start()
            self._resource_vampires.append(vampire_thread)