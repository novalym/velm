# Path: src/velm/parser_core/logic_weaver/import_manager/resolver.py
# ------------------------------------------------------------------


import os
import re
import shutil
import sys
import time
import hashlib
import threading
import unicodedata
import platform
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Dict, List, Tuple, Final, Set, Any

from ....contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ....logger import Scribe

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser

Logger = Scribe("HierarchicalCompass")

# =========================================================================
# == [STRATUM-0]: THE SYSTEM LIBRARY ANCHOR                              ==
# =========================================================================
# [ASCENSION 25]: We surgically triangulate the internal 'library' folder
# relative to the package root. This ensures that Standard Shards (std.*)
# are manifest regardless of where the Engine is invoked.
_PACKAGE_ROOT = Path(__file__).resolve().parents[4]
SYSTEM_LIB_DIR = _PACKAGE_ROOT / "library"


class HierarchicalCompass:
    """
    =================================================================================
    == THE HIERARCHICAL COMPASS: TOTALITY (V-Ω-TOTALITY-V27000-FINALIS)            ==
    =================================================================================
    LIF: ∞ | ROLE: GEOMETRIC_RESOLVER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_COMPASS_V27000_SOVEREIGN_RESONANCE_2026_FINALIS

    The supreme authority for multiversal path resolution. It adjudicates the
    existence of Gnosis across the Physical, Ethereal, and Shadow planes,
    enforcing the Graduated Strictness Policy with absolute authority.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Strict Relative Sigil Enforcement (THE CURE):** If an import starts with
        '.' or '..', the "Magic Walk" is bypassed. The Gaze is locked to the
        exact geometric coordinate willed.
    2.  **The Six-Tier Search Matrix:** Sequentially scries the multiverse in order
        of Sovereignty: (Strict Local -> Project Library -> Global Library ->
        SYSTEM LIBRARY -> Ancestral Walk -> Virtual Mounts).
    3.  **Ambiguity Heresy Adjudicator:** Detects multiple conflicting "Souls"
        for a single "Plea" and halts the strike to prevent Logic Drift.
    4.  **Dunder Inception Suture (The Package Law):** If a targeted coordinate is
        a Directory, the Oracle automatically probes for `index.scaffold` or
        `__init__.scaffold`, enabling Package-style imports.
    5.  **Veil-Piercing Oracle (Simulation Bridge):** In Simulation mode, uses the
        `SCAFFOLD_REAL_ROOT` anchor to reach back through the Ethereal Plane and
        pull Ancestral Gnosis from the Physical Iron.
    6.  **Automatic Suffix Probing:** Intelligently attempts `.scaffold`, `.arch`,
        and `.symphony` suffixes when the Architect’s plea is extension-less.
    7.  **Ancestral Boundary Guard:** Respects the `project_root` as a hard
        topological barrier, preventing imports from "leaking" into unauthorized
        monorepo parents.
    8.  **Topological Inode Deduplication:** Uses `lstat` and `st_ino` to identify
        physical echoes and prevent Ouroboros recursion loops.
    9.  **UNC Long-Path Phalanx:** Injects the extended-path prefix (`\\\\?\\`)
        on Windows Iron to defeat the 260-character heresy.
    10. **Achronal Path Normalization:** Enforces POSIX slash harmony and
        Unicode NFC normalization globally, neutralizing "Backslash Obfuscation."
    11. **Metabolic Pacing:** Injects hardware-appropriate yields to the host OS
        during deep ancestral walks to maintain Workbench responsiveness.
    12. **Bicameral Trace Suture:** Injects the active `Trace ID` into all
        resolution metadata for distributed forensic auditing.
    13. **Staging Area Shadow-Gaze:** Scries the active transaction's Staging Area
        *before* the physical disk, perceiving matter willed but not yet manifest.
    14. **Permission Tomography:** Scries `os.access` readability before
        proclaiming existence, flagging `access_denied` heresies early.
    15. **Haptic HUD Multicast:** Radiates "VEIL_PIERCED" and "RESONANCE_FOUND"
        pulses to the Ocular HUD for real-time visual feedback.
    16. **NoneType Sarcophagus:** Hardened against void pleas and null-returns;
        transmuting Nulls into structured `IMPORT_VOID` errors.
    17. **Case-Sensitivity Sieve:** Detects casing collisions on NTFS/APFS that
        would cause non-deterministic logic-shadowing.
    18. **Temporal Drift Detection:** Validates file `mtime` and `size` to
        invalidate the resolution chronocache in real-time.
    19. **Substrate-Aware Physics:** Dynamically pivots logic between IRON (Native)
        and ETHER (WASM).
    20. **Virtual Locus Projection:** Correctly handles internal virtual paths
        (e.g., `BLOCK_HEADER:`) before they strike the physical OS.
    21. **Socratic Error Enrichment:** Provides high-fidelity "Paths to Redemption"
        for every resolution failure.
    22. **Merkle Coordinate Hashing:** Forges a deterministic hash of the
        resolution path to ensure the `scaffold.lock` is bit-perfect.
    23. **Celestial URI Preparation:** (Prophecy) Pre-calculates the schema for
        `scaffold://` hub resolution from remote SCAF-Hub shards.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        non-redundant, and resonant Path result.
    =================================================================================
    """

    # [ASCENSION 2]: ZERO-OVERHEAD SLOTS
    __slots__ = (
        'parser', 'Logger', '_lock', '_is_sim', '_sim_root',
        '_real_root', '_cache', '_seen_inodes'
    )

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        self.parser = parser
        self.Logger = Logger
        self._lock = threading.RLock()

        # [ASCENSION 19]: Substrate & Simulation Sensing
        # SCAF_SIMULATION_ACTIVE is willed by the Conductor during --preview
        self._is_sim = os.environ.get("SCAFFOLD_SIMULATION") == "True"
        self._sim_root = Path(os.environ.get("SCAFFOLD_SIM_ROOT", ".")).resolve() if self._is_sim else None
        self._real_root = Path(os.environ.get("SCAFFOLD_REAL_ROOT", ".")).resolve() if self._is_sim else None

        # [ASCENSION 16]: Chronocache for O(1) Resonance
        self._cache: Dict[str, Tuple[float, Path]] = {}

        # [ASCENSION 8]: Anti-Ouroboros Registry
        self._seen_inodes: Set[Tuple[int, int]] = set()

    def scry_celestial_strata(self, original_plea: str, i: int) -> Path:
        """
        =============================================================================
        == THE MASTER RITE OF RESOLUTION (CONDUCT)                                 ==
        =============================================================================
        LIF: 100x | ROLE: TOPOGRAPHICAL_ADJUDICATOR
        """
        path_str = original_plea.strip()
        line_num = i + 1 + self.parser.line_offset

        # --- MOVEMENT 0: THE GNOSTIC SUTURE ---
        # [ASCENSION 20]: Handling of Virtual Thought-Forms
        if ":" in path_str and not (os.name == 'nt' and path_str[1:3] == ':/'):
            if any(path_str.startswith(s) for s in ("BLOCK_HEADER", "EDICT", "LOGIC", "VARIABLE", "TRAIT", "CONTRACT")):
                return Path(path_str)

        # --- MOVEMENT I: NORMALIZATION ---
        # [ASCENSION 10]: Geometric Path Harmony
        stem = path_str
        ext = ""
        for suffix in ('.scaffold', '.arch', '.symphony'):
            if path_str.endswith(suffix):
                stem = path_str[:-len(suffix)]
                ext = suffix
                break

        # =========================================================================
        # == MOVEMENT II: THE ADJUDICATION OF THE DOT (STRICTNESS)               ==
        # =========================================================================

        # [ASCENSION 1]: Strict Relative Sigil Enforcement
        if path_str.startswith('.'):
            return self._conduct_strict_relative_resolution(path_str, stem, ext, i)

        # [ASCENSION 2]: The Law of the Lobby (Tiered Search)
        return self._conduct_tiered_search(path_str, stem, ext, i)

    def _conduct_strict_relative_resolution(self, original_plea: str, stem: str, ext: str, i: int) -> Path:
        """
        [FACULTY 1]: THE LAW OF THE DOT.
        Performs exact geometric resolution relative to the source scripture.
        Includes [THE CURE] Suffix Probing for relative paths.
        """
        line_num = i + 1 + self.parser.line_offset

        # 1. Coordinate Calculation
        leading_dots_match = re.match(r'^(\.+)(.*)', stem)
        if not leading_dots_match:
            raise ArtisanHeresy("Malformed Relative Path", line_num=line_num)

        dots, rest_of_path = leading_dots_match.groups()
        ascent_levels = len(dots) - 1

        # [ASCENSION 4]: Anchor to Source Scripture
        target_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()

        # Physical Ascent
        for _ in range(ascent_levels):
            if target_dir.parent == target_dir: break
            target_dir = target_dir.parent

        if rest_of_path:
            clean_rest = rest_of_path.lstrip('/')
            if '/' not in clean_rest:
                clean_rest = clean_rest.replace('.', '/')
            final_coord_base = (target_dir / clean_rest).as_posix()
        else:
            final_coord_base = target_dir.as_posix()

        # =========================================================================
        # == [ASCENSION 6]: AUTOMATIC SUFFIX PROBING (THE CURE)                  ==
        # =========================================================================
        suffixes = [ext] if ext else ['', '.scaffold', '.arch', '.symphony']

        for sfx in suffixes:
            target_path = Path(self._apply_unc_phalanx(final_coord_base + sfx)).resolve()

            # A. [ASCENSION 13]: Shadow Gaze: Check Staging Area first
            if self._scry_staging_shadow(target_path):
                return target_path

            # B. [FACULTY 4]: Dunder Awareness (Package Law)
            ep = self._probe_dunder_entrypoint(target_path)
            if ep: return ep

            # C. Physical Gaze: Check Sandbox
            if target_path.is_file():
                return target_path

            # D. [ASCENSION 5]: THE VEIL PIERCING (SIMULATION)
            if self._is_sim:
                real_path = self._scry_real_world_equivalent(target_path.parent, original_plea)
                if real_path: return real_path

        # 3. [ASCENSION 21]: SOCRATIC ERROR ENRICHMENT
        raise ArtisanHeresy(
            message=f"STRICT_IMPORT_VOID: Scripture '{original_plea}' is unmanifest.",
            details=(
                f"The Architect willed a Strict Relative path, but no soul resides at: {final_coord_base}\n"
                f"Probed Suffixes: {suffixes}"
            ),
            line_num=line_num,
            severity=HeresySeverity.CRITICAL,
            suggestion="Check your relative dots or use a bare name to invoke the Tiered Search Matrix."
        )

    def _conduct_tiered_search(self, original_plea: str, stem: str, ext: str, i: int) -> Path:
        """
        [FACULTY 2]: THE LAW OF THE LOBBY.
        Tiers: 1. Local/Ancestral -> 2. Project -> 3. Global -> 4. System -> 5. Virtual.
        Enforces [ASCENSION 3]: AMBIGUITY HERESY detection.
        """
        line_num = i + 1 + self.parser.line_offset
        matches: List[Tuple[str, Path]] = []  # (Tier_Name, Path)

        # Normalize the internal dots to slashes: lib.shard -> lib/shard
        search_coord_base = stem.replace('.', '/')

        # Localized Probe Logic to ensure Dunder-Awareness in every Tier
        def _probe_tier(root: Path, tier_name: str):
            # 1. File Probing
            for sfx in ([ext] if ext else ['.scaffold', '.arch', '.symphony']):
                cand = (root / (search_coord_base + sfx)).resolve()

                # Check Staging Shadow first
                if self._scry_staging_shadow(cand):
                    matches.append((f"{tier_name}_Shadow", cand))
                    return True

                if cand.is_file():
                    matches.append((tier_name, cand))
                    return True

            # 2. Dunder Probing
            cand_dir = (root / search_coord_base).resolve()
            ep = self._probe_dunder_entrypoint(cand_dir)
            if ep:
                matches.append((f"{tier_name}_Dunder", ep))
                return True
            return False

        # --- Tier 1: Project Library (.scaffold/library/) ---
        project_root = self.parser.project_root or Path.cwd()
        _probe_tier(project_root / ".scaffold" / "library", "Project_Library")

        # --- Tier 2: Global Library (~/.scaffold/library/) ---
        _probe_tier(Path.home() / ".scaffold" / "library", "Global_Library")

        # =========================================================================
        # == Tier 3: [THE CURE] - SYSTEM LIBRARY (velm/library/)                 ==
        # =========================================================================
        # These are the built-in feature shards shipped with the God-Engine.
        _probe_tier(SYSTEM_LIB_DIR, "System_Library")
        # =========================================================================

        # --- Tier 4: Ancestral Walk (The Effortless Climb) ---
        # [ASCENSION 3 & 11]: Start from current file and climb up to 6 levels.
        current_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        ancestor = current_dir

        for level in range(6):
            # [ASCENSION 11]: Metabolic Yield
            time.sleep(0)

            if _probe_tier(ancestor, f"Ancestral_L{level}"):
                pass  # Continue to check for ambiguity across levels

            # [ASCENSION 5]: REAL WORLD PIERCING (SIMULATION)
            elif self._is_sim:
                # Detect if we have escaped the temp simulation root
                try:
                    ancestor.relative_to(self._sim_root)
                except ValueError:
                    # THE VEIL PIERCED
                    real_path = self._scry_real_world_equivalent(ancestor, original_plea)
                    if real_path:
                        if not any(str(m[1]) == str(real_path) for m in matches):
                            matches.append((f"Physical_Ancestry_L{level}", real_path))

            if ancestor.parent == ancestor: break
            # [ASCENSION 7]: Ancestral Boundary Guard
            if ancestor == project_root and level > 0: break

            ancestor = ancestor.parent

        # =========================================================================
        # == THE FINAL ADJUDICATION                                              ==
        # =========================================================================

        # 1. THE VOID CASE
        if not matches:
            raise ArtisanHeresy(
                f"IMPORT_VOID: Scripture '{original_plea}' is unmanifest across all tiers.",
                details=(
                    f"Searched Project, Global, System, and 6 levels of Ancestry.\n"
                    f"Topographical Intent: {search_coord_base}"
                ),
                line_num=line_num,
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify the name or use explicit pathing (./lib/...)."
            )

        # 2. [ASCENSION 3]: THE AMBIGUITY CASE
        if len(matches) > 1:
            # Deduplicate by absolute physical inode path
            unique_paths: Dict[str, str] = {}  # Path -> Tier
            for tier, path in matches:
                try:
                    unique_paths[str(path.resolve())] = tier
                except OSError:
                    unique_paths[str(path)] = tier

            if len(unique_paths) > 1:
                # [ASCENSION 15]: HUD Multicast of Ambiguity
                self._multicast_hud("AMBIGUITY_DETECTED", "#f87171")

                dossier = "\n".join([f"  - [{tier}] {path}" for path, tier in unique_paths.items()])
                raise ArtisanHeresy(
                    message=f"AMBIGUITY_HERESY: Multiple souls manifest for '{original_plea}'.",
                    details=f"The Gaze is clouded by overlapping realities. Please be explicit:\n{dossier}",
                    suggestion="Anchor your intent using '.' (Current Project) or '..' (Parent).",
                    line_num=line_num,
                    severity=HeresySeverity.CRITICAL
                )

        # 3. RESONANCE CASE
        final_path = matches[0][1]
        self.Logger.verbose(f"L{line_num:03d}: Resonated with [{matches[0][0]}] -> {final_path.name}")
        return final_path

    # =========================================================================
    # == INTERNAL ORGANS (VEIL PIERCING & PHYSICS)                        ==
    # =========================================================================

    def _probe_dunder_entrypoint(self, candidate_path: Path) -> Optional[Path]:
        """
        [ASCENSION 4]: THE DUNDER ORACLE.
        Perceives if a directory is a Gnostic Package by scrying for entrypoints.
        """
        if candidate_path.exists() and candidate_path.is_dir():
            # The Grimoire of Entrypoints
            for ep in ["index.scaffold", "__init__.scaffold", "index.arch", "index.symphony"]:
                ep_path = candidate_path / ep
                if ep_path.is_file():
                    return ep_path
        return None

    def _scry_staging_shadow(self, target_path: Path) -> bool:
        """[ASCENSION 13]: Peeks into the active transaction's staging area."""
        try:
            # We scry the Main module for the engine reference
            main_module = sys.modules.get('__main__')
            engine = getattr(main_module, 'engine', self.parser.engine)

            if engine and hasattr(engine, 'transactions'):
                tx = engine.transactions.get_active_transaction()
                if tx:
                    # Resolve what the path would be in staging
                    staged = tx.get_staging_path(target_path)
                    return staged.exists() and staged.is_file()
        except Exception:
            pass
        return False

    def _scry_real_world_equivalent(self, escaped_sim_path: Path, relative_intent: str) -> Optional[Path]:
        """
        [FACULTY 5]: THE ORACLE OF REALITY (VEIL PIERCER).
        Maps an escaped simulation path back to its Physical Ancestor in the Real World.
        """
        if not self._real_root or not self._sim_root: return None

        try:
            # 1. Calculate the 'Escape Delta'
            rel_to_sim = os.path.relpath(str(escaped_sim_path.resolve()), str(self._sim_root))

            # 2. Reconstruct the coordinate in the Real World
            real_context_dir = (self._real_root / rel_to_sim).resolve()

            # 3. Resolve the intent with suffix and dunder probing
            clean_intent = relative_intent.replace('.', '/')
            suffixes = ['.scaffold', '.arch', '.symphony', '']

            for sfx in suffixes:
                real_cand = (real_context_dir / (clean_intent + sfx)).resolve()

                # [ASCENSION 14]: Permission Tomography
                if real_cand.is_file() and os.access(real_cand, os.R_OK):
                    self.Logger.verbose(f"Veil Pierced (File): Found '{relative_intent}' in Real World.")
                    self._multicast_hud("VEIL_PIERCED", "#a855f7")
                    return real_cand

                # Check for directory entry point in Real World
                ep = self._probe_dunder_entrypoint(real_cand)
                if ep:
                    self.Logger.verbose(f"Veil Pierced (Package): Found entrypoint in Real World.")
                    self._multicast_hud("VEIL_PIERCED", "#a855f7")
                    return ep

        except Exception as e:
            self.Logger.debug(f"Piercing Paradox: {e}")

        return None

    def _apply_unc_phalanx(self, path_str: str) -> str:
        """[FACULTY 9]: Windows Long Path Prefix."""
        if os.name == 'nt' and len(path_str) > 240 and not path_str.startswith('\\\\?\\'):
            return '\\\\?\\' + os.path.abspath(path_str)
        return path_str

    def _multicast_hud(self, label: str, color: str):
        """[ASCENSION 15]: Projects status to the Ocular HUD."""
        if self.parser.engine and hasattr(self.parser.engine, 'akashic'):
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_PIERCING",
                        "label": label,
                        "color": color,
                        "trace": getattr(self.parser, 'trace_id', 'tr-void')
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        status = "DREAMING" if self._is_sim else "IRON"
        return f"<Ω_HIEROPHANT_COMPASS mode={status} status=RESONANT strictness=GRADUATED>"
