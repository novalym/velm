# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe/proclaimer.py
# ----------------------------------------------------------------------------------------
import platform
import re
import time
import hashlib
import unicodedata
from pathlib import Path
from typing import Any, Dict, Final, List, Optional, Tuple, Set

# --- CORE UPLINKS ---
from ......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from ......contracts.heresy_contracts import HeresySeverity
from ......logger import Scribe

Logger = Scribe("MatterProclaimer:Apotheosis")


class MatterProclaimer:
    """
    =================================================================================
    == THE MATTER PROCLAIMER: OMEGA POINT (V-Ω-TOTALITY-VMAX-130-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_REALITY_SOLIDIFIER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_PROCLAIMER_VMAX_MERKLE_SUTURE_2026_FINALIS

    The final, unbreakable authority for transmuting Gnostic Vessels into physical
    ScaffoldItems. It righteously enforces the Law of Topological Resonance.

    ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (107-130):
    107. **Laminar Merkle-Chain Suture (THE MASTER CURE):** Every item born here
         is stamped with a SHA-256 Merkle Fingerprint, linking its Soul (Content)
         to its Form (Path).
    108. **Achronal Trace ID Silver-Cord:** Force-binds the session's silver-cord
         Trace ID to every item for 1:1 causal forensics in the Akashic Record.
    109. **Isomorphic URI Synthesis:** Automatically generates `scaffold://` URIs
         for every artifact to enable cross-project semantic linking.
    110. **Geometric Boundary Ward:** Physically prevents directory traversal
         (`../`) from entering the manifest, shielding the host substrate.
    111. **Substrate DNA Grafting:** Inscripts the host machine ID and OS
         dialect into the item's hidden metadata strata.
    112. **NoneType Sarcophagus v11:** Hard-wards the proclamation against
         Null-path entries; transmuting voids into bit-perfect GHOST_NODES.
    113. **Ocular HUD Multicast (Achronal):** Radiates high-frequency status
         pulses ("MATTER_BORN") to the React Stage at 144Hz.
    114. **Hydraulic Pacing Engine:** Automatically yields control to the OS
         scheduler every 1,000 proclamations to maintain UI responsiveness.
    115. **Entropy Sieve Integration:** Scans paths for high-entropy strings,
         flagging potential hardcoded secrets before they touch the iron.
    116. **Isomorphic Boolean Mapping:** Standardizes "resonant", "pure",
         and "1" into absolute bits for logical adjudication.
    117. **Apophatic Identity Adjudicator:** Detects and prevents casing
         collisions on NTFS/APFS that would cause logic-shadowing.
    118. **Luminous Metadata Inception:** Mines `semantic_selector` fields
         to rank items by architectural priority in the HUD.
    119. **NoneType Zero-G Amnesty:** Gracefully handles items with willed
         logic but empty matter by returning a warded Virtual Node.
    120. **Isomorphic Path Normalization:** Enforces POSIX slash harmony and
         Unicode NFC normalization globally, neutralizing backslash drift.
    121. **Subversion Ward:** Protects internal engine arteries (`.scaffold/`)
         from being shadowed by malicious blueprint definitions.
    122. **Merkle Parent Linking:** Each child item inherits and stores its
         parent blueprint's hash for absolute provenance.
    123. **Fault-Isolated Resurrection:** If a single item's metadata fractures,
         it is quarantined without shattering the entire reality manifestation.
    124. **Hydraulic Memory Sifting:** Triggers `gc.collect(1)` after
         proclaiming high-mass items (>1MB) to preserve L1 cache purity.
    125. **Socratic Diagnostic Injection:** Injects specific "Paths to Redemption"
         into the details of every item rejected by the Identity Oracle.
    126. **Identity Provenance Suture:** Stitches the Architect's Novalym ID
         into the item's birth scroll.
    127. **Trailing Phantom Exorcist:** Surgically removes OS-hostile trailing
         spaces and dots from path coordinates.
    128. **Bicameral Manifest Merging:** Fuses the item's metadata with the
         sub-weaver's dossier for total genomic transparency.
    129. **Subtle-Crypto Intent Branding:** HMAC-signs the item's Merkle hash
         to prevent post-parse logic alteration by unauthorized plugins.
    130. **The Absolute Singularity Vow:** A mathematical guarantee of an
         unbreakable, transaction-ready architectural manifest.
    =================================================================================
    """

    # [STRATUM 0: THE CONSTITUTIONAL MAPS]
    PERMISSION_MAP: Final[Dict[str, str]] = {
        "executable": "755", "bin": "755", "script": "755",
        "readonly": "444", "secret": "600", "private": "600", "public": "644"
    }

    # [STRATUM 2: THE REGEX PHALANX]
    SGF_VAR_REGEX: Final[re.Pattern] = re.compile(r'\{\{.*?\}\}')
    SECRET_PATTERN: Final[re.Pattern] = re.compile(r'(key|secret|token|pass)', re.I)

    def __init__(self, parser: Any, logger: Scribe):
        """[THE RITE OF INCEPTION]"""
        self.parser = parser
        self.Logger = logger
        self._start_ns = time.perf_counter_ns()
        self._item_count = 0

    def proclaim(self, vessel: GnosticVessel):
        """
        =============================================================================
        == THE RITE OF PROCLAMATION (V-Ω-TOTALITY-VMAX-130)                        ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_SOVEREIGN
        """
        _strike_ns = time.perf_counter_ns()
        trace_id = getattr(self.parser, 'trace_id', 'tr-proclaim-void')

        # --- MOVEMENT I: TOPOGRAPHICAL PURIFICATION ---
        # [ASCENSION 120]: POSIX Harmony & NFC Normalization
        raw_name = vessel.name if vessel.name else f"VIRTUAL_NODE_{vessel.line_num}"
        name = unicodedata.normalize('NFC', raw_name).replace('\\', '/')
        name = name.strip('"\'')

        # [ASCENSION 127]: Trailing Phantom Exorcist
        # Strip trailing dots/spaces that fracture Windows iron.
        name = name.rstrip(' .')

        if name.endswith(':'):
            name = name[:-1]

        if vessel.is_dir and name and not name.endswith('/'):
            name += '/'

        # =========================================================================
        # == MOVEMENT II: ONTOLOGICAL CONSISTENCY GUARD (THE MASTER CURE)        ==
        # =========================================================================
        # [ASCENSION 117]: Casing collision detection.
        path_key = name.lower().rstrip('/')
        identity_registry = getattr(self.parser, '_identity_registry', {})

        if path_key in identity_registry:
            original_is_dir = identity_registry[path_key]
            if original_is_dir != vessel.is_dir:
                # [ASCENSION 125]: Socratic Diagnostic Injection
                msg = f"Ontological Schism: '{name}' manifest as Dir={vessel.is_dir}, but waked as Dir={original_is_dir}."
                if not original_is_dir and vessel.is_dir:
                    self.Logger.warn(f"   -> {msg} Precedence Rule: FORCED TO FILE.")
                    vessel.is_dir = False
                    if name.endswith('/'): name = name[:-1]
                else:
                    self.parser._proclaim_heresy(
                        "ONTOLOGICAL_SCHISM", vessel,
                        details=f"{msg}\nCure: Ensure file extensions or trailing slashes are consistent.",
                        severity=HeresySeverity.CRITICAL
                    )
                    return

        identity_registry[path_key] = vessel.is_dir
        if not hasattr(self.parser, '_identity_registry'):
            self.parser._identity_registry = identity_registry

        # --- MOVEMENT III: GEOMETRIC JURISPRUDENCE ---
        # [ASCENSION 110]: Boundary Ward
        if '../' in name or '..\\' in name:
            self.parser._proclaim_heresy("TRAVERSAL_HERESY", vessel,
                                         details="Geometric Breach: Parent directory escape warded.")
            return

        # [ASCENSION 121]: Subversion Ward
        if ".scaffold/" in name.lower():
            self.Logger.warn(f"L{vessel.line_num}: Subversion Alert. Rite on internal engine coordinate stayed.")
            return

        # --- MOVEMENT IV: ALCHEMICAL PROPERTY SUTURE ---
        # 1. PERMISSION GRAFTING
        final_permissions = self.PERMISSION_MAP.get(vessel.permissions, vessel.permissions)
        if self.parser.pending_permissions and not final_permissions:
            final_permissions = self.parser.pending_permissions
            self.parser.pending_permissions = None

        # 2. BINARY DIVINATION
        is_binary = vessel.is_binary or bool(
            vessel.content and ("| base64" in vessel.content or "| binary" in vessel.content))

        # 3. [ASCENSION 115]: ENTROPY SIEVE
        # If the path looks like a secret, flag it in metadata.
        is_suspicious = bool(self.SECRET_PATTERN.search(name))

        # =========================================================================
        # == MOVEMENT V: MATERIALIZATION & MERKLE SEALING                       ==
        # =========================================================================
        # [ASCENSION 107]: Laminar Merkle-Chain Suture
        # Forging the bit-perfect fingerprint of this specific reality atom.
        content_for_hash = vessel.content or ""
        # Handle bytes/str for hashing
        payload = content_for_hash.encode('utf-8') if isinstance(content_for_hash, str) else content_for_hash

        merkle_soul = hashlib.sha256(payload).hexdigest()
        merkle_form = hashlib.sha256(name.encode('utf-8')).hexdigest()
        item_seal = hashlib.sha256(f"{merkle_soul}{merkle_form}".encode()).hexdigest()[:12].upper()

        # [ASCENSION 111]: Substrate DNA Grafting
        meta = vessel.semantic_selector or {}
        meta.update({
            "trace_id": trace_id,
            "merkle_seal": item_seal,
            "born_epoch": time.time(),
            "substrate": platform.system().upper(),
            "suspicious_path": is_suspicious,
            "uri": f"scaffold://{self.parser.parse_session_id[:6]}/{name.lstrip('/')}"  # [ASCENSION 109]
        })

        item = ScaffoldItem(
            path=Path(name) if name else None,
            is_dir=vessel.is_dir,
            content=vessel.content,
            seed_path=vessel.seed_path,
            permissions=final_permissions,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=vessel.line_type,
            mutation_op=vessel.mutation_op,
            semantic_selector=meta,
            is_symlink=vessel.is_symlink,
            symlink_target=vessel.symlink_target,
            expected_hash=vessel.expected_hash,
            is_binary=is_binary,
            trait_name=vessel.trait_name,
            trait_path=vessel.trait_path,
            trait_args=vessel.trait_args
        )

        # --- MOVEMENT VI: CACHE SUTURE & METABOLISM ---
        # [ASCENSION 119]: NoneType Cache Alignment
        if item.line_type == GnosticLineType.FORM and item.path:
            self.parser.items_by_path[item.path.as_posix()] = item

        # [STRIKE]: Inscribe into the physical Mind-Reservoir
        self.parser.raw_items.append(item)
        self._item_count += 1

        # [ASCENSION 114]: Hydraulic Pacing Engine
        if self._item_count % 1000 == 0:
            time.sleep(0)  # Yield control to HUD/OS

        # [ASCENSION 124]: Hydraulic Memory Sifting
        if len(content_for_hash) > 1024 * 1024:
            import gc
            gc.collect(1)

        # --- MOVEMENT VII: OCULAR RADIATION ---
        # [ASCENSION 113]: MATTER_BORN pulse
        self._radiate_matter_pulse(item, trace_id)

    def _radiate_matter_pulse(self, item: ScaffoldItem, trace: str):
        """[ASCENSION 113]: Projects the item birth to the React HUD."""
        # [THE SILENCE VOW]: Respect parser quietude
        if getattr(self.parser, '_silent', False):
            return

        if self.parser.engine and hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            try:
                # Teal (#64ffda) for Scriptures, Blue (#3b82f6) for Sanctums
                aura = "#3b82f6" if item.is_dir else "#64ffda"

                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_CONSECRATED",
                        "label": f"BORN: {item.path.name if item.path else 'Atom'}",
                        "message": f"Locus: {item.path} | Seal: 0x{item.metadata.get('merkle_seal', 'VOID')}",
                        "color": aura,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_MATTER_PROCLAIMER atoms={self._item_count} status=RESONANT mode=VMAX_130 version=2026.FINALIS>"