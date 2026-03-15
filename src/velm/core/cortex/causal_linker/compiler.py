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

    def compile(
            self,
            ordered_shards: List[ShardNode],
            primary_intent: str,
            existing_vars: Dict[str, Any],
            shard_manifests: Dict[str, ShardHeader]
    ) -> str:
        """
        =================================================================================
        == THE OMEGA COMPILATION: TOTALITY (V-Ω-TOTALITY-VMAX-PURE-WILL)               ==
        =================================================================================
        """
        start_ts = time.time()

        # --- MOVEMENT 0: IDENTITY ANCHORING ---
        trace_id = existing_vars.get("trace_id", f"tr-{uuid.uuid4().hex[:8].upper()}")
        project_name = existing_vars.get("project_name", "Dreamed_Reality")

        manifest_lines =[]

        # --- MOVEMENT I: THE CONSTITUTIONAL HEADER ---
        manifest_lines.extend([
            f"# ============================================================================",
            f"# == GNOSTIC MANIFEST: {project_name.upper()} ",
            f"# == TRACE_ID: {trace_id} ",
            f"# == FORGED_BY: {self._architect} @ {self._machine_id} ",
            f"# == INTENT: {primary_intent[:100]}...",
            f"# == GENESIS_EPOCH: {int(time.time())} ",
            f"# ============================================================================",
            ""
        ])

        # --- MOVEMENT II: THE ALCHEMICAL REASONER ---
        manifest_lines.append("# --- I. ARCHITECTURAL RATIONALE ---")
        for shard in ordered_shards:
            origin = "[EXPLICIT]" if shard.is_explicitly_willed else "[AUTONOMIC]"
            manifest_lines.append(f"# - {shard.id.ljust(30)} {origin} via {shard.match_reason}")
        manifest_lines.append("")

        # --- MOVEMENT III: THE ALTAR OF VARIABLES ($$) ---
        manifest_lines.append("# --- II. THE ALTAR OF VARIABLES ($$) ---")

        all_requirements = self._harvest_all_requirements(ordered_shards)
        final_vars = self._resolve_variable_matrix(all_requirements, existing_vars)

        for k in sorted(final_vars.keys()):
            # [ASCENSION 7]: Apophatic Variable Sieve
            if k.startswith('__') or k in self.SUBSTRATE_GHOST_VARS:
                continue

            if k in self.prophet.RESERVED_NAMES and k not in existing_vars:
                continue

            v = final_vars[k]

            # [ASCENSION 9]: Linguistic Purity Suture
            safe_key = re.sub(r'[^a-zA-Z0-9_]', '_', k.lower())
            if safe_key and safe_key[0].isdigit():
                safe_key = f"_{safe_key}"

            # [ASCENSION 3]: THE OBJECT EXORCIST V3
            val_str = self._serialize_gnosis(v)
            if val_str is None:
                continue

            # [ASCENSION 5]: Recursive Type-Hint Suture
            type_hint = ""
            if isinstance(v, bool):
                type_hint = ": bool"
            elif isinstance(v, int):
                type_hint = ": int"
            elif isinstance(v, float):
                type_hint = ": float"
            elif isinstance(v, str) and not val_str.startswith('@'):
                type_hint = ": str"

            manifest_lines.append(f"$$ {safe_key}{type_hint}".ljust(30) + f"= {val_str}")

        manifest_lines.append("")

        # --- MOVEMENT IV: THE CAUSAL WEB (TOPOLOGY) ---
        manifest_lines.append("# --- III. THE CAUSAL WEB (TOPOLOGY) ---")
        manifest_lines.append("# ```mermaid")
        manifest_lines.append("# graph TD")
        for shard in ordered_shards:
            safe_shard_id = shard.id.replace('/', '_').replace('-', '_')
            for req in shard.requires:
                if "/" in req:
                    safe_req = req.replace('/', '_').replace('-', '_')
                    manifest_lines.append(f"#   {safe_req} --> {safe_shard_id}")
        manifest_lines.append("# ```")
        manifest_lines.append("")

        # --- MOVEMENT V: THE MANIFESTATION (WEAVING) ---
        manifest_lines.append("# --- IV. THE MANIFESTATION ---")

        # =========================================================================
        # ==[ASCENSION 1048]: THE GEOMETRIC SANCTUM ANCHOR (THE MASTER CURE)    ==
        # =========================================================================
        # We righteously force all woven shards to manifest inside the willed project
        # directory. This annihilates the "Root Drift" heresy and ensures 'package.json'
        # resolves natively for the Maestro shell strikes.
        manifest_lines.append(f"{{{{ project_slug }}}}/")

        #[ASCENSION 4]: Topographical Tier Stratification
        # Sort by foundations first (Iron -> Body -> Mind -> Soul -> Ocular)
        tier_order =["iron", "body", "mind", "soul", "ocular", "void"]
        shards_by_tier = {t:[] for t in tier_order}

        for shard in ordered_shards:
            tier = shard.tier.lower() if hasattr(shard, 'tier') and shard.tier else "mind"
            if tier not in shards_by_tier: tier = "mind"
            shards_by_tier[tier].append(shard)

        for tier in tier_order:
            tier_shards = shards_by_tier[tier]
            if not tier_shards: continue

            # We apply the 4-space Isomorphic Indentation to adhere to the Project Root anchor
            manifest_lines.append(f"\n    # === STRATUM: {tier.upper()} ===")

            for shard in tier_shards:
                # =====================================================================
                # ==[ASCENSION 1]: BICAMERAL SUMMARY SUTURE (THE MASTER CURE)       ==
                # =====================================================================
                header = shard_manifests.get(shard.id)
                role = "file"
                summary = "No summary provided."

                if header:
                    role = header.suture.role if header.suture else "file"
                    # Prioritize v3.0 Header Summary
                    if header.summary and "Architectural shard:" not in header.summary:
                        summary = header.summary
                    # Fallback to description
                    elif hasattr(header, 'description') and header.description:
                        summary = header.description

                # Secondary Fallback to ShardNode data
                if summary == "No summary provided.":
                    if hasattr(shard, 'summary') and shard.summary:
                        summary = shard.summary
                    elif hasattr(shard, 'description') and shard.description:
                        summary = shard.description

                # Clean summary mass
                summary = str(summary).replace('\n', ' ').strip()

                manifest_lines.append(f"    # [SHARD]: {shard.id} | ROLE: {role}")
                manifest_lines.append(f"    # {summary}")

                # =====================================================================
                # == [ASCENSION 2]: ISOMORPHIC TYPE THAW (THE SPACING CURE)          ==
                # =====================================================================
                vibe_list =[]
                if hasattr(shard, 'vibe') and shard.vibe:
                    if isinstance(shard.vibe, str):
                        # The Suture: Convert comma-string to list
                        vibe_list =[v.strip() for v in shard.vibe.strip('[]').split(',')]
                    elif isinstance(shard.vibe, (list, tuple, set)):
                        vibe_list = list(shard.vibe)

                if vibe_list:
                    manifest_lines.append(f"    # Tags: {', '.join(vibe_list)}")

                # [ASCENSION 10]: Achronal Trace ID Suture w/ 4-space Indent
                manifest_lines.append(f"    {{{{ logic.weave('{shard.id}', variables={{'trace_id': '{trace_id}'}}) }}}}")
                manifest_lines.append("")

        # --- MOVEMENT VI: THE MAESTRO'S FINALITY ---
        manifest_lines.append("%% post-run")
        manifest_lines.append(f'    proclaim: "✨[SINGULARITY] Realities converged for project \'{project_name}\'."')
        manifest_lines.append(f'    proclaim: "Trace ID: {trace_id}"')
        manifest_lines.append(f'    proclaim: "To ignite the citadel: [bold cyan]make up[/bold cyan]"')

        # --- MOVEMENT VII: THE INTEGRITY SEAL ---
        full_blueprint = "\n".join(manifest_lines)
        # [ASCENSION 11]: Merkle-Lattice Sealing
        merkle_seal = hashlib.sha256(full_blueprint.encode()).hexdigest()[:12].upper()
        full_blueprint += f"\n# == INTEGRITY_SEAL: 0x{merkle_seal} =="

        duration_ms = (time.time() - start_ts) * 1000
        Logger.success(f"Gnostic Scripture forged in {duration_ms:.2f}ms. Seal: 0x{merkle_seal}")

        #[ASCENSION 24]: THE FINALITY VOW
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