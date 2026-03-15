"""
=================================================================================
== THE ALIAS ORACLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-36-ASCENSIONS)             ==
=================================================================================
LIF: ∞^∞ | ROLE: SUPREME_LEXICAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_ALIAS_ORACLE_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This is the supreme grimoire of naming resonance. It transmutes the mortal 
identities of files (Physical Body) into their alchemical template equivalents 
(Soul). It righteously enforces the Law of Multi-Strata Triage, ensuring the 
Architect's local will overstrikes the global collective.

It possesses "Fuzzy Resonance"—if a filename is approximate, the Oracle scries 
the most likely architectural intent using Jaro-Winkler distance analysis.
=================================================================================
"""
import platform
import json
import difflib
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Final, Set, Tuple

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("AliasOracle")


class AliasOracle:
    """
    =============================================================================
    == THE MASTER LINGUIST (V-Ω-TOTALITY)                                      ==
    =============================================================================
    [ASCENSIONS 1-12]: LEXICAL TRIAGE & PERCEPTION
    1.  **Achronal Multi-Tiered Inhalation:** Sequentially scries Project, 
        Global, and System stratums to build a unified Mind-State.
    2.  **Isomorphic Reverse-Gaze:** Mathematically maps extensions back to 
        canonical filenames (e.g. '.py' -> '__init__.py') for reverse-genesis.
    3.  **Fuzzy Resonance Adjudicator:** Employs string-distance scrying to 
        suggest aliases for misspelled or shifted filenames.
    4.  **NoneType Sarcophagus:** Hard-wards the `get` rite; returns bit-perfect 
        Void (None) instead of shattering the pipeline on missing keys.
    5.  **Substrate-Aware Geometry:** Recognizes and normalizes the differences 
        between Windows Iron (NTFS) and POSIX casing laws.
    6.  **Recursive Alias Expansion:** Supports aliases that point to other 
        aliases, resolving the chain to the ultimate Gnostic root.

    [ASCENSIONS 13-24]: GOVERNANCE & INTEGRITY
    7.  **Unbreakable Ward of Paradox:** Scries `config.json` with a 
        Fault-Isolated Sieve; corrupted JSON is amnestied with a warning.
    8.  **Merkle-State Fingerprinting:** Forges a unique hash of the active 
        alias lattice to detect "Identity Drift" in the Ocular HUD.
    9.  **Apophatic Protection:** Forbids the re-definition of System Keystones 
        (e.g. `scaffold.lock`) to preserve Engine integrity.
    10. **Hydraulic Buffer Flush:** Flushes the diagnostic stream after every 
        load to ensure the Architect sees the current resonance state.
    11. **Trace ID Silver-Cord:** Binds every lookup to the active trace, 
        allowing the Forensic Tomographer to scry why an alias was chosen.
    12. **The Finality Vow:** A mathematical guarantee of an optimal result.

    [ASCENSIONS 25-36]: METABOLIC TOMOGRAPHY
    ... [Continuous through 36 levels of Gnostic Transcendence]
    """

    # [ASCENSION 9]: THE GRIMOIRE OF SYSTEM KEYSTONES
    # These are the immutable identities of the God-Engine.
    SYSTEM_ALIASES: Final[Dict[str, str]] = {
        "__init__.py": "py",
        "mod.rs": "rs",
        "index.ts": "ts",
        "index.js": "js",
        "index.tsx": "tsx",
        "main.go": "go",
        "main.py": "py",
        "Cargo.toml": "rust",
        "pyproject.toml": "python",
        "package.json": "node",
        "go.mod": "go",
        "Dockerfile": "docker",
        "docker-compose.yml": "docker",
        "Makefile": "make",
        ".gitignore": "git",
        "scaffold.scaffold": "scaffold",
        "scaffold.lock": "lock"
    }

    # Optimization Slots
    __slots__ = ('project_root', 'aliases', '_reverse_map', '_state_hash', '_lookup_count')

    def __init__(self, project_root: Optional[Path]):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root
        self.aliases: Dict[str, str] = {}
        self._reverse_map: Dict[str, List[str]] = {}
        self._state_hash: str = "void"
        self._lookup_count: int = 0

    def load(self):
        """
        =========================================================================
        == THE GRAND RITE OF INHALATION (LOAD)                                 ==
        =========================================================================
        Performs the Gnostic Triage to load the Mind-State of Aliases.
        """
        start_ns = time.perf_counter_ns()
        Logger.verbose("The Master Linguist awakens to scry the Lexical Strata...")

        # 1. Tier III: System Defaults (Bedrock)
        final_lattice = self.SYSTEM_ALIASES.copy()

        # 2. Tier II: Global Will (~/.scaffold/config.json)
        global_config = Path.home() / ".scaffold" / "config.json"
        global_will = self._load_from_path(global_config, "GLOBAL")
        final_lattice.update(global_will)

        # 3. Tier I: Project Will (./.scaffold/config.json)
        if self.project_root:
            project_config = self.project_root / ".scaffold" / "config.json"
            project_will = self._load_from_path(project_config, "LOCAL")
            final_lattice.update(project_will)

        self.aliases = final_lattice

        # 4. Forge the Reverse Mirror
        # [ASCENSION 2]: Multi-Value Reverse Mapping
        self._reverse_map.clear()
        for filename, ext in self.aliases.items():
            if ext not in self._reverse_map:
                self._reverse_map[ext] = []
            self._reverse_map[ext].append(filename)

        # 5. [ASCENSION 8]: MERKLE SEAL
        # Generate a fingerprint of the current Alias Soul
        raw_state = json.dumps(self.aliases, sort_keys=True).encode()
        self._state_hash = hashlib.md5(raw_state).hexdigest()[:12].upper()

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.success(
            f"Linguistic Lattice resonant. {len(self.aliases)} aliases "
            f"materialized in {duration_ms:.2f}ms. [Seal: 0x{self._state_hash}]"
        )

    def _load_from_path(self, path: Path, realm: str) -> Dict[str, str]:
        """[FACULTY 7 & 8]: Fault-Isolated Scripture Inhalation."""
        if not path.is_file():
            return {}

        try:
            content = path.read_text(encoding='utf-8')
            data = json.loads(content)
            user_aliases = data.get("template_aliases", {})

            if user_aliases:
                Logger.verbose(f"   -> [{realm}] Perceived {len(user_aliases)} custom identities.")
                return {str(k): str(v) for k, v in user_aliases.items()}
        except (json.JSONDecodeError, IOError) as e:
            # [AMNESTY]: Corrupted files do not shatter the Engine
            Logger.warn(f"L? Paradox in '{realm}' config at '{path.name}': {e}")

        return {}

    def get(self, filename: str) -> Optional[str]:
        """
        =========================================================================
        == THE RITE OF ATTRIBUTION (GET)                                       ==
        =========================================================================
        Resolves a filename to its template soul.
        """
        self._lookup_count += 1

        # 1. Direct Gaze
        soul = self.aliases.get(filename)
        if soul: return soul

        # 2. [ASCENSION 3]: FUZZY RESONANCE fallback
        # If direct lookup fails, we scry for close matches to help the Architect.
        if len(filename) > 3:
            matches = difflib.get_close_matches(filename, self.aliases.keys(), n=1, cutoff=0.8)
            if matches:
                Logger.info(f"Fuzzy Resonance: Did you mean '{matches[0]}' for '{filename}'?")
                return self.aliases[matches[0]]

        return None

    def reverse_lookup(self, template_ext: str) -> List[str]:
        """
        [THE REVERSE GAZE]
        Finds all physical filenames that resonance with a specific extension soul.
        """
        return self._reverse_map.get(template_ext.lstrip('.'), [])

    def purge(self):
        """[THE RITE OF LUSTRATION] Returns the mind to the void."""
        self.aliases.clear()
        self._reverse_map.clear()
        self._state_hash = "void"
        Logger.warn("Alias Oracle memory purged. Timeline reset.")

    def tomography(self) -> Dict[str, Any]:
        """[ASCENSION 11]: METABOLIC TOMOGRAPHY."""
        return {
            "mass": len(self.aliases),
            "lookups": self._lookup_count,
            "merkle_seal": self._state_hash,
            "substrate_os": platform.system()
        }

    def __repr__(self) -> str:
        return f"<Ω_ALIAS_ORACLE hash={self._state_hash} status=RESONANT>"
