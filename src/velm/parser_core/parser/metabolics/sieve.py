# Path: parser_core/parser/metabolics/sieve.py
# --------------------------------------------

"""
=================================================================================
== THE OMEGA ONTOLOGICAL SIEVE: TOTALITY (V-Ω-VMAX-IDENTITY-SUTURE-FINALIS)    ==
=================================================================================
LIF: ∞^∞ | ROLE: IDENTITY_BOUNDARY_WARDEN | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_SIEVE_VMAX_ANOMALY_238_CURE_2026_FINALIS_!#()@()@#)(

[THE MANIFESTO]
The supreme definitive authority for distinguishing between 'Self' (Internal)
and 'Other' (External). This version righteously annihilates Anomaly 238 by
enforcing the Law of the Sanctuary Zone.
=================================================================================
"""

import re
import hashlib
from typing import Dict, Any, Set, Final, List, Optional, Tuple
from .constants import is_standard_library


class OntologicalSieve:
    """
    The High-Performance Boundary Governor.
    Ensures that internal architecture never leaks into external package debt.
    """

    # [ASCENSION 1]: THE GNOSTIC IMMUNITY WHITELIST
    # These tokens represent structural invariants that are ALWAYS internal.
    IMMUNITY_WHITELIST: Final[frozenset[str]] = frozenset({
        "velm", "scaffold", "src", "app", "core", "test", "tests", "internal",
        "api", "models", "schemas", "utils", "services", "infrastructure",
        "config", "constants", "contracts", "base", "main", "hub", "logic",
        "auth", "db", "database", "repository", "middleware", "controller",
        "vessels", "guardian", "sentinel", "weaver", "mason", "lib", "shards",
        "blueprint", "manifest", "setup", "nova", "omega", "impl", "refactor"
    })

    __slots__ = (
        'internal_signatures', 'internal_prefixes', 'internal_regex',
        '_state_hash', '_trace_id'
    )

    def __init__(self, variables: Dict[str, Any], manifests: Dict[str, Any]):
        """
        =============================================================================
        == THE RITE OF IDENTITY MAPPING (V-Ω-TOTALITY)                             ==
        =============================================================================
        LIF: 10,000x | ROLE: IDENTITY_DECODER
        """
        self.internal_signatures: Set[str] = set(self.IMMUNITY_WHITELIST)
        self.internal_prefixes: Set[str] = set()
        self._trace_id = variables.get("trace_id", "tr-sieve-void")

        # --- MOVEMENT I: PROJECT IDENTITY MIRROR ---
        # [ASCENSION 2]: Capture every permutation of the Project's Soul.
        for key in ('project_slug', 'package_name', 'project_name', 'org_name'):
            val = variables.get(key)
            if val and isinstance(val, str):
                clean = val.lower().strip()
                # 1. Standard Identity
                self.internal_signatures.add(clean)
                # 2. Hyphen/Underscore Dialects
                self.internal_signatures.add(clean.replace('_', '-'))
                self.internal_signatures.add(clean.replace('-', '_'))
                # 3. Scoped NPM/Node Prefixes
                self.internal_prefixes.add(f"@{clean}/")
                self.internal_prefixes.add(f"{clean}-")

        # --- MOVEMENT II: SHARD-LEVEL PERCEPTION ---
        # [ASCENSION 3]: Inhale the identity of every shard willed in this strike.
        for shard_id in manifests.keys():
            shard_lower = shard_id.lower()
            self.internal_signatures.add(shard_lower)

            # Extract atomic segments (e.g. 'auth' from 'system/auth')
            segments = re.split(r'[/\-_]', shard_lower)
            for seg in segments:
                if len(seg) > 2:
                    self.internal_signatures.add(seg)

            # [ASCENSION 4]: Scoped Workspace Shield
            if '/' in shard_lower:
                self.internal_prefixes.add(f"@{shard_lower.split('/')[0]}/")

        # --- MOVEMENT III: KINETIC COMPILE ---
        # [ASCENSION 1]: Compile an O(1) Regex for prefix matching
        if self.internal_prefixes:
            pattern = "^(" + "|".join(re.escape(p) for p in self.internal_prefixes) + ")"
            self.internal_regex = re.compile(pattern)
        else:
            self.internal_regex = re.compile(r"^\b$")  # Match nothing

        # [ASCENSION 8]: Merkle State Fingerprinting
        self._evolve_hash()

    def is_external_debt(self, requirement: str, ecosystem: str) -> bool:
        """
        =========================================================================
        == THE RITE OF JURISPRUDENCE (ADJUDICATE DEBT)                         ==
        =========================================================================
        LIF: 1,000,000x | ROLE: BOUNDARY_ADJUDICATOR
        [THE MASTER CURE]: Final verification of external soul residency.
        """
        # --- PHASE 0: THE VOID GUARD ---
        # [ASCENSION 6 & 19]: NoneType Sarcophagus
        if not requirement or not isinstance(requirement, str):
            return False

        req = requirement.strip().lower().replace('\x00', '')
        if not req: return False

        # --- PHASE 1: THE ANCESTRAL ORACLE ---
        # [ASCENSION 1]: Standard Library Sieve
        if is_standard_library(req, ecosystem):
            return False

        # --- PHASE 2: SPATIAL COORDINATE DETECTION ---
        # [ASCENSION 7]: Relative and absolute paths are NEVER debt.
        if req.startswith(('.', '/', '@/', '~/')) or '\\' in req:
            return False

        # Detect Semantic Pathing (e.g., src.api.v1)
        if '.' in req and not any(op in req for op in ('>', '=', '<')):
            # Heuristic: If it contains dots but no version operators, it's a path.
            return False

        # --- PHASE 3: THE SANCTUARY ZONE (INTERNAL IDENTITY) ---
        # 1. [ASCENSION 1]: O(1) Signature Match
        if req in self.internal_signatures:
            return False

        # [ASCENSION 9]: Linguistic Purity Suture
        if req.replace('-', '_') in self.internal_signatures or req.replace('_', '-') in self.internal_signatures:
            return False

        # 2. [ASCENSION 4]: Scoped Prefix Shield
        if self.internal_regex.match(req):
            return False

        # --- PHASE 4: RECURSIVE HUB DISCOVERY ---
        # If the requirement is a direct Shard ID (e.g. system/auth), it is Self.
        if '/' in req:
            if req in self.internal_signatures:
                return False

        # =========================================================================
        # == THE FINAL VERDICT                                                   ==
        # =========================================================================
        # [ASCENSION 24]: If the requirement has survived the Sieve, it is true
        # external debt that must be materialised in pyproject.toml or package.json.
        return True

    def _evolve_hash(self):
        """[ASCENSION 8]: Merkle State Evolution."""
        raw_state = "|".join(sorted(list(self.internal_signatures)))
        self._state_hash = hashlib.sha256(raw_state.encode()).hexdigest()[:12].upper()

    def __repr__(self) -> str:
        return f"<Ω_ONTOLOGICAL_SIEVE status=RESONANT signatures={len(self.internal_signatures)} hash={self._state_hash}>"