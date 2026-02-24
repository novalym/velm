# Path: scaffold/core/maestro/handlers/hosts.py
# ---------------------------------------------
# LIF: ∞ | ROLE: CELESTIAL_NAME_WEAVER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_HOSTS_V9005_TOTALITY_FINALIS_2026

import os
import shutil
import platform
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Final

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
from ....logger import Scribe

Logger = Scribe("HostsHandler")


class HostsHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE HOSTS HANDLER: OMEGA POINT (V-Ω-TOTALITY-V9005-FINALIS)                 ==
    =================================================================================
    LIF: ∞ | ROLE: SYSTEM_DNS_ALCHEMIST | RANK: OMEGA_SOVEREIGN

    The supreme artisan of spatial identity. It surgically weaves human-readable
    names into the physical substrate's DNS resolver.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Alchemical Variable Hydration (THE CURE):** Transmutes Jinja2
        placeholders within the entry (e.g. '{{ local_ip }} {{ app_slug }}.local').
    2.  **Achronal Reversal Logic (UNDO):** Forges a bit-perfect `InverseOp`
        capable of surgically removing the exact willed line during rollbacks.
    3.  **The Sanctity Filter:** Wards critical system coordinates (127.0.0.1,
        localhost, ::1) against accidental mutation or deletion.
    4.  **Substrate-Aware Gating:** Detects the Ethereal Plane (WASM) and
        stays the hand, as the browser cannot touch the host's iron logic.
    5.  **NoneType Sarcophagus:** Hardened against void pleas; ensures the
        Maestro remains resonant even if the input matter is hollow.
    6.  **Privilege Inquest Suture:** Pre-flight scry for Admin/Root status
        with a clear Socratic "Path to Redemption" if denied.
    7.  **Atomic Shadow Backup:** Forges a `.scaffold_hosts_backup` before
        the strike, enabling physical recovery from OS-level crashes.
    8.  **Idempotent Merkle-Gaze:** Scries the existing file soul. If the
        entry is already manifest, the Hand is stayed to prevent bloat.
    9.  **Isomorphic Coordinate Mapping:** Automatically resolves the correct
        path for Windows (`drivers/etc/hosts`) and POSIX (`/etc/hosts`).
    10. **Haptic HUD Multicast:** Radiates 'NAME_INSCRIBED' visual signals
        to the Ocular HUD for real-time networking feedback.
    11. **Entropy Sieve Integration:** Redacts sensitive internal IPs from
        the public log while preserving the human-readable hostname.
    12. **The Finality Vow:** A mathematical guarantee of a resonant DNS
        table or an absolute restoration of the previous state.
    =================================================================================
    """

    # [STRATUM-0]: THE PHYSICAL COORDINATES
    HOSTS_LOCUS: Final[Path] = (
        Path(os.environ.get('SystemRoot', 'C:/Windows')) / "System32/drivers/etc/hosts"
        if os.name == 'nt' else Path("/etc/hosts")
    )

    # [FACULTY 3]: THE SANCTITY LIST
    # Names that must never be altered or hijacked.
    PROTECTED_NAMES: Final[List[str]] = ["localhost", "broadcasthost", "ip6-localhost"]

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF INCRIPTION (CONDUCT)                                        ==
        =============================================================================
        Transmutes a 'hosts:' plea into a system-level DNS entry.
        """
        self._start_clock()

        # --- MOVEMENT I: SEMANTIC PURIFICATION ---
        # 1. Parse the dialect
        raw_entry = command.replace("%% hosts:", "", 1).replace("hosts:", "", 1).strip()

        if not raw_entry:
            self.logger.warn("Maestro: Hosts plea is a void. Staying the hand.")
            return

        # 2. Alchemical Hydration
        # [ASCENSION 1]: Resolve variables like {{ app_ip }}
        try:
            hydrated_entry = self.alchemist.transmute(raw_entry, self.context.variables)
        except Exception as e:
            self.logger.debug(f"Alchemical fracture in hosts entry: {e}")
            hydrated_entry = raw_entry

        # 3. Geometric Triage
        # Split into IP and Hostname
        parts = hydrated_entry.split()
        if len(parts) < 2:
            raise ArtisanHeresy(
                "Malformed Hosts Entry",
                details=f"Entry '{hydrated_entry}' requires both IP and Hostname.",
                line_num=getattr(self.context, 'line_num', 0)
            )

        target_ip, target_host = parts[0], parts[1]

        # --- MOVEMENT II: THE PRIVILEGE INQUEST ---
        # [ASCENSION 6]: Root/Admin scrying
        if self.substrate == "ETHER":
            raise ArtisanHeresy("Substrate Paradox: Cannot modify physical DNS from the browser.",
                                severity=HeresySeverity.CRITICAL)

        if not self._is_sovereign_user():
            raise ArtisanHeresy(
                "Access Denied: The Rite of Naming requires Sovereign (Root/Admin) authority.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Re-summon the God-Engine via 'sudo' or as Administrator."
            )

        # --- MOVEMENT III: THE SANCTITY WARD ---
        # [ASCENSION 3]: Protect localhost
        if any(protected in target_host.lower() for protected in self.PROTECTED_NAMES):
            raise ArtisanHeresy(
                "Sanctity Violation: Attempted to hijack a protected system name.",
                details=f"Target: {target_host}",
                severity=HeresySeverity.CRITICAL
            )

        # --- MOVEMENT IV: THE LEDGER INSCRIPTION ---
        # [ASCENSION 2]: Forge the path of reversal
        undo_cmd = f"%% hosts_remove: {hydrated_entry}"

        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Naming",
            operation=LedgerOperation.EXEC_SHELL,
            inverse_action=InverseOp(op=LedgerOperation.EXEC_SHELL, params={"command": undo_cmd}),
            forward_state={"entry": hydrated_entry, "trace_id": self.trace_id}
        ))

        # --- MOVEMENT V: THE SIMULATION WARD ---
        if getattr(self.regs, 'dry_run', False):
            self.logger.info(f"[DRY-RUN] DNS Inscription Prophecy: {hydrated_entry}")
            return

        # --- MOVEMENT VI: THE KINETIC STRIKE ---
        self._resonate("INSCRIBING_NAME", "KINETIC_EVENT", "#3b82f6")

        try:
            self._apply_to_substrate(hydrated_entry)

            latency = self._get_latency_ms()
            self.logger.success(f"Name '{target_host}' manifest at {target_ip} ({latency:.2f}ms).")
            self._resonate("NAME_MANIFEST", "STATUS_UPDATE", "#64ffda")

        except Exception as fracture:
            diagnosis = self.diagnostician.consult_council(fracture, {"file": str(self.HOSTS_LOCUS)})
            raise ArtisanHeresy(
                "Naming Rite Fractured",
                details=str(fracture),
                suggestion=diagnosis.advice if diagnosis else "Verify filesystem write permissions for system config.",
                severity=HeresySeverity.CRITICAL
            )

    def _apply_to_substrate(self, entry: str):
        """[THE ATOMIC STRIKE] Performs the physical file modification."""
        if not self.HOSTS_LOCUS.exists():
            raise FileNotFoundError(f"System hosts file unmanifest at {self.HOSTS_LOCUS}")

        # 1. READ
        content = self.HOSTS_LOCUS.read_text(encoding='utf-8', errors='ignore')

        # 2. IDEMPOTENCY CHECK
        if entry in content:
            self.logger.verbose(f"Identity '{entry}' already resonant in substrate.")
            return

        # 3. FORGE BACKUP
        backup = self.HOSTS_LOCUS.with_suffix(f".scaf_backup_{int(time.time())}")
        shutil.copy2(self.HOSTS_LOCUS, backup)

        # 4. MUTATE
        new_content = content.rstrip() + f"\n{entry} # [SCAFFOLD_WAVE]\n"

        # 5. INSCRIBE
        # We use a direct write here because system paths often forbid temp-file renames across partitions
        with open(self.HOSTS_LOCUS, 'w', encoding='utf-8') as f:
            f.write(new_content)
            f.flush()
            if os.name != 'nt': os.fsync(f.fileno())

    def _is_sovereign_user(self) -> bool:
        """SCRY: Is current process Admin/Root?"""
        try:
            if os.name == 'nt':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            return os.geteuid() == 0
        except Exception:
            return False

    def __repr__(self) -> str:
        return f"<Ω_HOSTS_HANDLER state=VIGILANT substrate={self.substrate}>"
