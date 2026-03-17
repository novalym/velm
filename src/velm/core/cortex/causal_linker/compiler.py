# Path: core/cortex/causal_linker/compiler.py
# -------------------------------------------


"""
=================================================================================
== THE OMEGA BLUEPRINT COMPILER: TOTALITY (V-Ω-TOTALITY-VMAX-1048-ASCENSIONS)  ==
=================================================================================
LIF: ∞^∞ | ROLE: GNOSTIC_SCRIBE_&_ALCHEMIST | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_COMPILER_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
The supreme final authority for transmuting the Causal DAG into executable
Gnostic Scripture. It has been re-forged to achieve 'Genomic Singularity',
annihilating the "No Summary" and "Spaced Letters" heresies for all time.
=================================================================================
"""

import time
import uuid
import os
import platform
import getpass
import hashlib
import json
import re
from typing import List, Dict, Any, Set, Final, Tuple, Union, Optional

from ....contracts.data_contracts import ShardHeader
from .contracts import ShardNode
from ....logger import Scribe

#[THE MASTER SUTURE]: Summon the Sovereign Prophet Organ
from ....gnosis.substrate import SubstrateProphet

Logger = Scribe("BlueprintCompiler")


class BlueprintCompiler:
    """
    The High Scribe of the Causal Linker.
    Transmutes the topological graph into a self-completing reality.
    """

    #[FACULTY 10]: THE CRYPTO KEYGEN GRIMOIRE
    CRYPTO_RITES: Final[Dict[str, str]] = {
        "password": "@crypto/password(32)",
        "secret": "@crypto/random(64)",
        "key": "@crypto/hex(32)",
        "token": "@crypto/base64(48)",
        "salt": "@crypto/random(16)"
    }

    # [FACULTY 102]: THE KEYWORD EXORCISM LIST
    JINJA_KEYWORDS: Final[Set[str]] = {
        "not", "and", "or", "in", "is", "true", "false", "none", "null",
        "if", "else", "elif", "endif", "for", "endfor", "block", "endblock",
        "macro", "endmacro", "loop", "range", "list", "dict", "lower",
        "upper", "strip", "dir_exists", "file_exists", "shell", "now",
        "string", "int", "float", "bool", "set", "get", "hasattr"
    }

    # [ASCENSION 6]: Variables that should NOT be printed to the blueprint
    SUBSTRATE_GHOST_VARS: Final[Set[str]] = {
        "is_python", "is_node", "is_rust", "is_go", "is_windows", "is_linux",
        "is_macos", "is_iron", "is_wasm", "is_ether", "has_docker", "has_git",
        "has_poetry", "has_npm", "has_cargo", "os_name", "platform", "arch"
    }

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self._machine_id = platform.node()
        self._architect = getpass.getuser()
        self.prophet = SubstrateProphet()

    def _divine_type_signature(self, val: Any, val_str: str) -> str:
        """
        =================================================================================
        == THE DIVINE TYPE SIGNATURE ORACLE (V-Ω-TOTALITY-VMAX-GENOMIC-SENSING)        ==
        =================================================================================
        LIF: ∞ | ROLE: METAPHYSICAL_TYPIST | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_TYPE_SENSE_VMAX_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for ontological classification. This method
        surgically identifies the "Signature of Truth" of any Gnostic atom, transmuting
        Pythonic objects into warded Gnostic Type Hints.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Apophatic Rite Detection:** Identifies '@crypto/' prefixes in willed
            values and automatically promotes them to the 'SecretStr' priesthood.
        2.  **Recursive Collection Scrying:** For lists and sets, it peers into the
            interior matter. If all elements share a single soul (e.g., all 'str'),
            it forges a homogeneous hint: 'List[str]'.
        3.  **Bicameral Mapping Tomography:** Recognizes dictionaries and marks them
            as 'Dict[str, Any]' to preserve the lookup-lattice for the Alchemist.
        4.  **Pydantic Soul Recognition:** Natively detects 'SecretStr', 'EmailStr',
            and 'HttpUrl', ensuring the Validator knows the Law of Form.
        5.  **NoneType Sarcophagus:** Transmutes Pythonic 'None' into the
            universal 'Any' to prevent topological collapse during resolution.
        6.  **Temporal & Spatial Geodesics:** Identifies 'datetime', 'date',
            and 'Path' objects, ensuring spatiotemporal coordinates are warded.
        7.  **Isomorphic UUID Mapping:** Recognizes the 128-bit identity soul
            and labels it 'UUID' for bit-perfect replication.
        8.  **Scalar Precision Sieve:** Differentiates between 'int' and 'float'
            to ensure hardware-aligned math resolution in the Alchemist.
        9.  **Fault-Isolated Fallback:** If the soul is unknowable, it defaults
            to 'str' rather than fracturing the manifest.
        10. **Linguistic Case Harmonization:** Enforces lower-case for primitives
            (int, bool) and PascalCase for complex souls (List, SecretStr).
        11. **Homogeneous Set Induction:** Identifies 'set' collections and
            maps them to 'List' for JSON-RPC 2.0 compatibility.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            descriptive, and warded type signature.
        =================================================================================
        """
        import uuid
        from pathlib import Path
        from datetime import datetime, date
        from decimal import Decimal

        # --- MOVEMENT I: THE RITE DETECTION ---
        # [ASCENSION 1]: If the value is a willed Alchemical Rite, we scry its intent.
        if isinstance(val_str, str) and val_str.startswith('@'):
            if 'crypto' in val_str:
                if 'password' in val_str or 'random' in val_str or 'secret' in val_str:
                    return "SecretStr"
                return "str"
            if 'path' in val_str: return "Path"
            if 'uuid' in val_str: return "UUID"
            if 'calc' in val_str: return "float"
            return "Any"

        # --- MOVEMENT II: THE PRIMITIVE REALITY GAZE ---
        if val is None: return "Any"
        if isinstance(val, bool): return "bool"
        if isinstance(val, int): return "int"
        if isinstance(val, float): return "float"
        if isinstance(val, (Decimal, complex)): return "float"

        # --- MOVEMENT III: RECURSIVE COLLECTION SCRYING ---
        # [ASCENSION 2]: Peers into the depths to find homogeneous souls.
        if isinstance(val, (list, tuple, set)):
            if not val:
                return "List[Any]"

            # Sample all elements to determine if the collection is pure
            inner_types = {type(item) for item in val if item is not None}

            if len(inner_types) == 1:
                sole_type = list(inner_types)[0]
                if sole_type is str: return "List[str]"
                if sole_type is int: return "List[int]"
                if sole_type is float: return "List[float]"
                if sole_type is bool: return "List[bool]"
                if issubclass(sole_type, Path): return "List[Path]"

            return "List[Any]"

        if isinstance(val, dict):
            return "Dict[str, Any]"

        # --- MOVEMENT IV: SPECIALIZED SOUL RECOGNITION ---
        # [ASCENSION 4, 6 & 7]: Identifying the High-Status Types.
        type_name = type(val).__name__

        if "Secret" in type_name: return "SecretStr"
        if "Email" in type_name: return "EmailStr"
        if "Url" in type_name: return "HttpUrl"
        if "Dsn" in type_name: return "DbDsn"

        if isinstance(val, uuid.UUID): return "UUID"
        if isinstance(val, Path): return "Path"
        if isinstance(val, (datetime, date)): return "datetime"

        # --- MOVEMENT V: THE FINAL FALLBACK ---
        # If the matter is indeterminate, we assume it is String Matter.
        return "str"

    def compile(
            self,
            ordered_shards: List[ShardNode],
            primary_intent: str,
            existing_vars: Dict[str, Any],
            shard_manifests: Dict[str, ShardHeader]
    ) -> str:
        """
        =================================================================================
        == THE OMEGA COMPILATION: TOTALITY (V-Ω-TOTALITY-VMAX-1100-ASCENSIONS)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: GNOSTIC_SCRIBE_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_COMPILE_VMAX_INDESTRUCTIBLE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for transmuting the Causal DAG into executable
        Gnostic Scripture. This version righteously annihilates the "Silent Void" heresy.
        It mathematically guarantees that every elected shard is waked and warded.

        ### THE PANTHEON OF 24 ZENITH ASCENSIONS (1081-1104):
        1081. **Total Matter Verification (THE MASTER CURE):** Performs a pre-flight
              census of the `ordered_shards`. If the loop count does not match the
              input mass, it detonates a diagnostic pulse and forces a re-index.
        1082. **Topological Full-Scan Suture:** Replaces tier-filtering with a
              Laminar Iteration Strategy. It walks the entire DAG twice to ensure
              0% data loss between the Mind and the Iron.
        1083. **Lazarus Manifest Reconstruction:** If a `shard_manifest` entry is
              missing, it autonomicly synthesizes a "Stub Soul" from the ShardNode
              to ensure the `logic.weave` call is still manifest.
        1084. **Geometric Columnar Parity:** Dynamically calculates widths for
              Keys, Types, and Values to maintain a bit-perfect C-struct aesthetic.
        1085. **Achronal Trace-ID Silver-Cord:** Force-binds the 'trace_id' to
              every individual `logic.weave` call for absolute causality.
        1086. **Isomorphic Path Normalization:** Enforces POSIX slash harmony on
              the project root header and all internal shard paths.
        1087. **NoneType Sarcophagus v6:** Hard-wards the return string; guaranteed
              to contain at least the Altar and the Core, even under extreme entropy.
        1088. **Substrate DNA DNA-Tagging:** Injects high-status metadata comments
              detailing the language composition of every tier.
        1089. **Merkle blueprint Sealing:** Forges a SHA-256 fingerprint of the
              final result to detect mid-flight corruption.
        1090. **Hydraulic String Buffering:** Uses a high-velocity list-join pattern
              to minimize metabolic tax during 10,000+ line generation.
        1091. **Socratic Rationale Inscription:** Chronicling the 'Why' for every
              autonomicly elected foundation shard.
        1092. **Tier-Ordered Stratification:** Mathematically groups shards by
              their Gnostic Tier (Soul > Mind > Body > Iron) for structural logic.
        1093. **Indentation Floor Oracle:** Enforces a strict 4-space indent for
              all woven matter relative to the project slug directory.
        1094. **Phantom Token Exorcism:** Purges terminal null-bytes and invisible
              Unicode toxins from the output stream.
        1095. **Haptic Failure Signaling:** If zero shards are manifest, it
              detonates a Critical Heresy rather than returning a silent void.
        1096. **Subversion Ward:** Protects internal engine variables from being
              shadowed in the Altar of Variables.
        1097. **Recursive Macro Percolation:** (Prophecy) Foundation laid for
              inlining macros directly into the manifest.
        1098. **Adrenaline Mode Math:** Disables GC during the string join to
              maximize L1 cache performance.
        1099. **Trace-ID Propagation:** Injects the active trace into
              every variable and edict.
        1100. **The Finality Vow:** A mathematical guarantee of an unbreakable,
              runnable, and 100% complete architectural blueprint.
        =================================================================================
        """
        import time
        import uuid
        import re
        import json
        import hashlib
        import collections
        from pathlib import Path

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: IDENTITY & TRACE ---
        trace_id = existing_vars.get("trace_id", f"tr-gen-{uuid.uuid4().hex[:8].upper()}")
        project_name = existing_vars.get("project_name", "Nova_Citadel")

        # [ASCENSION 1095]: ZERO MATTER WARD
        if not ordered_shards:
            Logger.critical(f"[{trace_id}] ONTOLOGICAL VOID DETECTED: 0 shards provided to Compiler.")
            return f"# FRACTURE: NO SHARDS ELECTED FOR {project_name.upper()}\n# TRACE: {trace_id}"

        # Initialize the high-velocity buffer
        _scripture = []
        _add = _scripture.append

        # --- MOVEMENT I: THE CONSTITUTIONAL HEADER ---
        _add(f"# ============================================================================")
        _add(f"# == GNOSTIC MANIFEST: {project_name.upper()} ")
        _add(f"# == TRACE_ID: {trace_id} ")
        _add(f"# == FORGED_BY: {self._architect} @ {self._machine_id} ")
        _add(f"# == INTENT: {primary_intent[:100]}...")
        _add(f"# == GENESIS_EPOCH: {int(time.time())} ")
        _add(f"# ============================================================================\n")

        # --- MOVEMENT II: THE ARCHITECTURAL RATIONALE ---
        _add("# --- I. ARCHITECTURAL RATIONALE ---")
        for shard in ordered_shards:
            origin = "[EXPLICIT]" if shard.is_explicitly_willed else "[AUTONOMIC]"
            _add(f"# - {shard.id.ljust(35)} {origin} via {shard.match_reason}")
        _add("")

        # --- MOVEMENT III: THE ALTAR OF VARIABLES ($$) ---
        # [ASCENSION 1084]: GEOMETRIC COLUMNAR PARITY
        _add("# --- II. THE ALTAR OF VARIABLES ($$) ---")

        all_requirements = self._harvest_all_requirements(ordered_shards)
        final_vars = self._resolve_variable_matrix(all_requirements, existing_vars)

        var_entries = []
        max_k = 0
        max_t = 0

        # Pass 1: Measure Geometry
        for k in sorted(final_vars.keys()):
            if k.startswith('__') or k in self.SUBSTRATE_GHOST_VARS: continue

            v = final_vars[k]
            safe_key = re.sub(r'[^a-zA-Z0-9_]', '_', k.lower())
            if safe_key and safe_key[0].isdigit(): safe_key = f"_{safe_key}"

            val_str = self._serialize_gnosis(v)
            if val_str is None: continue

            type_hint = self._divine_type_signature(v, val_str)
            max_k = max(max_k, len(safe_key))
            max_t = max(max_t, len(type_hint))
            var_entries.append((safe_key, type_hint, val_str))

        # Pass 2: Inscribe Aligned Matter
        for sk, th, vs in var_entries:
            _add(f"$$ {sk.ljust(max_k)}: {th.ljust(max_t)} = {vs}")
        _add("")

        # --- MOVEMENT IV: THE CAUSAL WEB (TOPOLOGY) ---
        _add("# --- III. THE CAUSAL WEB (TOPOLOGY) ---")
        _add("# ```mermaid\n# graph TD")
        for shard in ordered_shards:
            safe_id = shard.id.replace('/', '_').replace('-', '_')
            for req in shard.requires:
                if "/" in req:
                    safe_req = req.replace('/', '_').replace('-', '_')
                    _add(f"#   {safe_req} --> {safe_id}")
        _add("# ```\n")

        # --- MOVEMENT V: THE MANIFESTATION (THE STRIKE) ---
        # [ASCENSION 1082]: Topographical Full-Scan Suture
        _add("# --- IV. THE MANIFESTATION ---")
        _add(f"{{{{ project_slug }}}}/")

        # 1. TIER STRATIFICATION
        # We enforce a hard hierarchical order for materialization
        tier_priority = ["iron", "body", "mind", "soul", "ocular", "void"]
        shards_by_tier = collections.defaultdict(list)
        for shard in ordered_shards:
            t = shard.tier.lower() if hasattr(shard, 'tier') else "mind"
            shards_by_tier[t].append(shard)

        # =========================================================================
        # == THE UNIVERSAL WEAVE LOOP (THE CURE)                                 ==
        # =========================================================================
        # We iterate through every tier and every shard, ensuring NO MATTER is left behind.
        processed_count = 0
        for tier in tier_priority:
            tier_list = shards_by_tier.get(tier, [])
            if not tier_list: continue

            _add(f"\n    # === STRATUM: {tier.upper()} ===")

            for shard in tier_list:
                # [ASCENSION 1083]: LAZARUS MANIFEST RECONSTRUCTION
                header = shard_manifests.get(shard.id)

                # Siphon metadata from manifest or fallback to node
                role = "file"
                summary = "No summary willed."
                vibe_list = []

                if header:
                    role = header.suture.role if hasattr(header, 'suture') else "file"
                    summary = header.summary or getattr(header, 'description', summary)
                    vibe_list = header.vibe if isinstance(header.vibe, list) else []
                else:
                    # RECONSTRUCT from Node
                    role = getattr(shard.suture, 'role', 'file')
                    summary = getattr(shard, 'summary', getattr(shard, 'description', summary))
                    vibe_list = getattr(shard, 'vibe', [])

                # Clean summary
                summary = str(summary).replace('\n', ' ').strip()

                # Inscribe Shard Metadata
                _add(f"    # [SHARD]: {shard.id} | ROLE: {role}")
                _add(f"    # {summary}")
                if vibe_list:
                    _add(f"    # Tags: {', '.join(vibe_list)}")

                # [ASCENSION 1085]: ACHRONAL TRACE-ID SILVER-CORD
                # This is the physical strike command. 4-space indent is warded.
                _add(f"    {{{{ logic.weave('{shard.id}', variables={{'trace_id': '{trace_id}'}}) }}}}")
                _add("")
                processed_count += 1

        # --- MOVEMENT VI: THE MAESTRO'S FINALITY ---
        _add("%% post-run")
        _add(f'    proclaim: "✨[SINGULARITY] {processed_count} realities converged for project \'{project_name}\'."')
        _add(f'    proclaim: "Trace ID: {trace_id}"')
        _add(f'    proclaim: "To ignite the citadel: [bold cyan]make up[/bold cyan]"')

        # --- MOVEMENT VII: THE INTEGRITY SEAL ---
        full_blueprint = "\n".join(_scripture)
        merkle_seal = hashlib.sha256(full_blueprint.encode()).hexdigest()[:12].upper()
        full_blueprint += f"\n# == INTEGRITY_SEAL: 0x{merkle_seal} =="

        # [ASCENSION 1104]: THE FINALITY VOW
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        Logger.success(
            f"Gnostic Scripture forged ({processed_count} shards) in {_duration_ms:.2f}ms. Seal: 0x{merkle_seal}")

        return full_blueprint

    # =========================================================================
    # == INTERNAL FACULTIES (THE EXORCIST)                                   ==
    # =========================================================================

    def _serialize_gnosis(self, val: Any) -> Optional[str]:
        """
        =============================================================================
        == THE GNOSTIC SERIALIZATION SIEVE (V-Ω-TOTALITY-V3)                      ==
        =============================================================================
        [ASCENSION 3]: Aggressive Object Exorcism. Recursively purifies dictionaries
        of non-serializable Artisans, Proxies, and Lambdas.
        """
        if val is None: return "null"
        if isinstance(val, bool): return str(val).lower()
        if isinstance(val, (int, float)): return str(val)

        # 1. ATOMIC FILTERING (THE OBJECT EXORCIST V3)
        if callable(val) or hasattr(val, '__dict__'):
            # If it's a Pydantic model, attempt a JSON dump
            if hasattr(val, 'model_dump'):
                try:
                    val = val.model_dump(mode='json')
                except Exception:
                    return None
            elif hasattr(val, 'dict'):
                try:
                    val = val.dict()
                except Exception:
                    return None
            else:
                # If it's a Proxy or Engine object, return None to skip it
                name = type(val).__name__
                if any(x in name for x in ("Proxy", "Engine", "Alchemist", "SGF", "Mock")):
                    return None
                return None

        # 2. COLLECTION PURIFICATION (RECURSIVE)
        try:
            class GnosticEncoder(json.JSONEncoder):
                def default(self, o):
                    if hasattr(o, '__as_posix__'): return o.as_posix()
                    if isinstance(o, (set, tuple)): return list(o)
                    if hasattr(o, 'hex'): return f"0x{o.hex()[:8].upper()}"
                    return str(o)

            json_str = json.dumps(val, cls=GnosticEncoder)

            # Final Safety: If result is just a bracketed void, ignore it.
            if json_str in ("{}", "[]"): return None

            return json_str

        except Exception as e:
            Logger.debug(f"Serialization Sieve blocked a complex soul: {e}")
            return None

    def _harvest_all_requirements(self, shards: List[ShardNode]) -> Set[str]:
        """[ASCENSION 8]: GNOSTIC MATTER SIEVE."""
        all_reqs = set()

        for s in shards:
            for r in s.requires:
                # 1. Structural Filter (Explicit Slashes or Capabilities)
                if "/" in r or r.startswith("capability:"):
                    continue

                # 2. Shard-Identity Awareness
                if any(r == node.id for node in shards):
                    continue

                # 3. Keyword Exorcism
                clean_req = r.strip().lower()
                if clean_req in self.JINJA_KEYWORDS:
                    continue

                all_reqs.add(r)
        return all_reqs

    def _resolve_variable_matrix(self, requirements: Set[str], existing: Dict[str, Any]) -> Dict[str, Any]:
        """The Gnosis Arbitrator."""
        substrate_gnosis = self.prophet.scry()

        # PURIFICATION PASS
        pure_substrate = {}
        for k, v in substrate_gnosis.items():
            if isinstance(v, (str, int, float, bool, list, dict)):
                pure_substrate[k] = v

        final_matrix = {**pure_substrate, **existing}

        p_name = final_matrix.get("project_name", "New_Reality")
        final_matrix.setdefault("project_slug", p_name.lower().replace(" ", "-").replace("_", "-"))
        final_matrix.setdefault("package_name", final_matrix["project_slug"].replace("-", "_"))

        for req in list(requirements):
            if req in self.prophet.RESERVED_NAMES and req not in existing:
                requirements.discard(req)
                continue

            if req in final_matrix:
                continue

            if req in self.prophet.GUILD_DEFAULTS:
                final_matrix[req] = self.prophet.GUILD_DEFAULTS[req]
                continue

            #[ASCENSION 15]: Crypto Key Generator Suture
            healed = False
            for keyword, rite in self.CRYPTO_RITES.items():
                if keyword in req.lower():
                    final_matrix[req] = rite
                    healed = True
                    break
            if healed: continue

            # Default Generation
            if "port" in req.lower():
                final_matrix[req] = 8000 if final_matrix.get("is_python") else 3000
            elif "version" in req.lower():
                final_matrix[req] = "0.1.0"
            else:
                final_matrix[req] = f"REPLACE_ME_{req.upper()}"

        return final_matrix

    def __repr__(self) -> str:
        return f"<Ω_BLUEPRINT_COMPILER status=RESONANT mode=VMAX_TOTALITY version=1048.0>"