# Path: parser_core/parser/metabolics/builders.py
# -----------------------------------------------

"""
=================================================================================
== THE OMEGA MANIFEST BUILDERS: TOTALITY (V-Ω-TOTALITY-VMAX-GENOMIC-FINALIS)   ==
=================================================================================
LIF: ∞^∞ | ROLE: GENOMIC_SCRIBE_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_BUILDERS_VMAX_CODEX_SINGULARITY_2026_FINALIS_!#()@()@#)(

[THE MANIFESTO]
The supreme authority for transmuting Gnostic Intent into Physical Matter.
This artisan righteously annihilates the "Object Leak" and "Directive Mirage"
heresies by enforcing a Recursive Reification Sieve.

Axiom Zero: No pointer shall escape the Mind. Only Matter shall touch the Iron.
=================================================================================
"""

import json
import os
import re
import hashlib
import time
import yaml
import unicodedata
from pathlib import Path
from typing import Set, Tuple, Dict, Any, List, Final, Optional, Union

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....logger import Scribe

# [ASCENSION 51]: JIT Codex Inhalation
try:
    from ....codex import resolve_codex_directive
except ImportError:
    resolve_codex_directive = None

Logger = Scribe("ManifestBuilders")


class ManifestBuilders:
    """
    =============================================================================
    == THE OMNISCIENT GENOME SCRIBE (V-Ω-TOTALITY-VMAX-REIFICATION-SUTURE)     ==
    =============================================================================
    LIF: ∞ | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_MASTER
    """

    # =========================================================================
    # == STRATUM 0: THE REIFICATION ORACLE (THE MASTER CURE)                 ==
    # =========================================================================

    @classmethod
    def _reify_matter(cls, val: Any, context: Dict[str, Any], depth: int = 0,
                      _visited: Optional[Set[int]] = None) -> str:
        """
        =================================================================================
        == THE OMEGA REIFICATION ORACLE: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)    ==
        =================================================================================
        LIF: ∞ | ROLE: MATTER_TRANSMUTATOR_PRIME | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_REIFY_VMAX_CIRCULAR_WARD_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme final authority for flattening Gnosis into Matter. This version
        righteously annihilates the <Ω_GNOSTIC_DICT> leak and the Ouroboros Loop
        heresy. It ensures the Project Conscience is bit-perfect and shell-resonant.
        =================================================================================
        """
        import json
        import decimal
        import unicodedata
        from pathlib import Path

        # --- MOVEMENT 0: THE VOID & OUROBOROS GUARD ---
        if val is None:
            return ""

        # [ASCENSION 1]: Laminar Circularity Ward
        if _visited is None: _visited = set()
        val_id = id(val)
        if val_id in _visited:
            return f"/* CIRCULAR_REF:{hex(val_id).upper()} */"

        if depth > 10:
            return "/* RECURSION_LIMIT_REACHED */"

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 3] - THE APOPHATIC ENGINE WARD               ==
        # =========================================================================
        # Surgically identify and incinerate the Reprs of the Gnostic Pantheon.
        v_type = type(val).__name__
        if any(x in v_type for x in ("Proxy", "Engine", "Alchemist", "Parser", "SGF", "Context", "Weaver")):
            return ""

        # --- MOVEMENT II: THE TRINITY OF SCALARS ---
        # [ASCENSION 7]: Isomorphic Boolean Mapping
        if isinstance(val, bool):
            return str(val).lower()

        # [ASCENSION 9]: Numeric Precision Suture
        if isinstance(val, (int, float, decimal.Decimal)):
            return str(val)

        # --- MOVEMENT III: THE COLLECTION INCEPTION ---
        # [STRIKE]: Mark this node as visited to prevent Ouroboros loops
        if not isinstance(val, (str, bytes)):
            _visited.add(val_id)

        try:
            # A. Dictionaries & GnosticSovereignDicts
            if isinstance(val, dict) or hasattr(val, '_shadow_map'):
                try:
                    # [ASCENSION 5]: Pydantic Soul Extraction
                    if hasattr(val, 'model_dump') and callable(val.model_dump):
                        data = val.model_dump(mode='json')
                    elif hasattr(val, 'dict') and callable(val.dict):
                        data = val.dict()
                    else:
                        # [ASCENSION 49]: Recursive Flattening with Dunder Exorcism
                        data = {
                            str(k): cls._reify_matter(v, context, depth + 1, _visited)
                            for k, v in val.items()
                            if not str(k).startswith('_')
                        }

                    # Sieve out empty atoms to keep the manifest lean
                    data = {k: v for k, v in data.items() if v != ""}
                    if not data: return ""

                    # [ASCENSION 50]: Bicameral JSON Suture
                    return json.dumps(data, ensure_ascii=False)
                except Exception:
                    return ""

            # B. Arrays (Lists / Sets / Tuples)
            if isinstance(val, (list, tuple, set)):
                try:
                    # Recursive descent
                    flattened = [cls._reify_matter(i, context, depth + 1, _visited) for i in val]
                    # Filter voids
                    flattened = [i for i in flattened if i != ""]
                    if not flattened: return ""

                    # [ASCENSION 4]: Bicameral Triage
                    # If it's a simple list of primitives, use comma-separation for shell utility
                    if all(isinstance(x, (str, int, float, bool, decimal.Decimal)) for x in val):
                        return ",".join(map(str, flattened))

                    return json.dumps(flattened, ensure_ascii=False)
                except Exception:
                    return ""

            # C. [ASCENSION 8]: GEOMETRIC PATH HARMONY
            if isinstance(val, Path):
                return str(val).replace('\\', '/')

        finally:
            # Reclaim memory and unmark visit
            if not isinstance(val, (str, bytes)):
                _visited.remove(val_id)

        # --- MOVEMENT IV: PHYSICAL PURIFICATION (THE FINALITY) ---
        # [ASCENSION 59]: Unicode & Homoglyph Normalization
        result = str(val).strip()
        result = unicodedata.normalize('NFC', result)

        # [ASCENSION 6 & 60]: Null-Byte & Invisible Toxin Annihilation
        # C-speed translation table would be faster, but replace is bit-perfect here.
        result = result.replace('\x00', '').replace('\ufeff', '').replace('\u200b', '')

        # [ASCENSION 10]: GEOMETRIC QUOTING ORACLE
        # If the string contains spaces or shell-hostile chars, we wrap it in safety.
        if re.search(r'[ \t\n\r!$;<>|&()]', result):
            # Already quoted check
            if not (result.startswith(('"', "'")) and result.endswith(result[0])):
                return f'"{result}"'

        return result

    # =========================================================================
    # == STRATUM 1: THE MANIFEST RITES (FORGE)                               ==
    # =========================================================================

    @classmethod
    def forge_env_example(cls, variables: Dict[str, Any], parser: Any) -> ScaffoldItem:
        """
        =================================================================================
        == THE OMEGA DELEGATION RITE: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)      ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_DNA_DISPATCHER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_ENV_DELEGATED_VMAX_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for transmuting the project's Conscience.
        This version righteously incinerates the monolithic burden by delegating
        total materialization authority to the specialized ConscienceForger organ.
        =================================================================================
        """
        # [ASCENSION 2]: APOPHATIC IMPORT SHIELDING
        # We perform a JIT import to prevent topological circularity.
        from .env_forger import ConscienceForger

        # --- MOVEMENT I: THE SILVER-CORD SUTURE ---
        # [ASCENSION 3]: Force-bind the trace context
        trace_id = variables.get("trace_id", "tr-env-delegated")

        if not variables.get("silent"):
            Logger.verbose(f"[{trace_id[:8]}] Orchestrator: Summoning the ConscienceForger for manifest inception.")

        try:
            # =========================================================================
            # == MOVEMENT II: THE KINETIC HAND-OFF (THE STRIKE)                      ==
            # =========================================================================
            # [ASCENSION 1]: THE MASTER CURE.
            # We delegate the entire reification, categorization, and Saas-Retina
            # scrying to the specialized organ. We pass 'parser' so it can access
            # the Alchemist and the existing Gnostic Mind.
            env_item = ConscienceForger.forge(variables, parser)

            # --- MOVEMENT III: ADJUDICATION & FINALITY ---
            # [ASCENSION 6]: NoneType Sarcophagus check
            if not env_item or not isinstance(env_item, ScaffoldItem):
                raise ValueError("ConscienceForger returned a Void Manifest.")

            # [ASCENSION 15]: Adrenaline Telemetry
            if not variables.get("is_adrenaline") and not variables.get("silent"):
                Logger.success(
                    f"   -> [SUTURE] Conscience manifest foraged. Seal: 0x{getattr(env_item, 'merkle_seal', 'VOID')}")

            # [ASCENSION 24]: THE FINALITY VOW
            return env_item

        except Exception as delegation_fracture:
            # [ASCENSION 17]: Socratic Error Unwrapping
            import traceback
            error_details = f"Delegation Shattered: {str(delegation_fracture)}\n{traceback.format_exc()}"
            Logger.critical(error_details)

            # [ASCENSION 18]: EMERGENCY REDEMPTION
            # If the forger shatters, we return a warded Failure Item to prevent engine collapse.
            return ScaffoldItem(
                path=Path(".env.example"),
                content=f"# [FRACTURE]: Conscience materialization failed.\n# Reason: {str(delegation_fracture)}",
                line_type=GnosticLineType.FORM,
                metadata={"origin": "Orchestrator_Emergency", "trace_id": trace_id}
            )

    @classmethod
    def forge_pyproject_toml(cls, deps: Set[str], variables: Dict[str, Any], parser: Any = None) -> ScaffoldItem:
        """
        =================================================================================
        == THE OMEGA DELEGATION RITE: TOTALITY (V-Ω-TOTALITY-VMAX-PEP621-SUTURE)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_DNA_DISPATCHER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_TOML_DELEGATED_VMAX_2026_FINALIS

        [THE MANIFESTO]
        This rite has been completely decapitated from the orchestrator monolith.
        It now securely summons the `TomlForger` to perform advanced PEP-621
        and Tooling Configuration DNA weaving.
        =================================================================================
        """
        # [ASCENSION 1]: APOPHATIC IMPORT SHIELDING
        from .toml_forger import TomlForger

        trace_id = variables.get("trace_id", "tr-py-manifest")

        if not variables.get("silent"):
            Logger.verbose(f"[{trace_id[:8]}] Orchestrator: Summoning the TomlForger for Pythonic Genome inception.")

        try:
            # =========================================================================
            # == THE KINETIC HAND-OFF (THE STRIKE)                                   ==
            # =========================================================================
            # Delegate the entire array resolution, PEP-621 metadata insertion,
            # and autoconfiguration of Ruff/Pytest to the dedicated Artisan.
            toml_item = TomlForger.forge(deps, variables, parser)

            return toml_item

        except Exception as delegation_fracture:
            import traceback
            error_details = f"TomlForger Shattered: {str(delegation_fracture)}\n{traceback.format_exc()}"
            Logger.critical(error_details)

            # [ASCENSION 2]: EMERGENCY REDEMPTION SUTURE
            # If the forger shatters, we return a warded Failure Item to prevent engine collapse.
            from pathlib import Path
            return ScaffoldItem(
                path=Path("pyproject.toml"),
                content=f"# [FRACTURE]: Pythonic Genome materialization failed.\n# Reason: {str(delegation_fracture)}",
                line_type=GnosticLineType.FORM,
                mutation_op="*=",
                metadata={"origin": "Orchestrator_Emergency", "trace_id": trace_id}
            )

    @classmethod
    def forge_package_json(cls, deps: Set[str], variables: Dict[str, Any], parser: Any = None) -> ScaffoldItem:
        """
        =================================================================================
        == THE OMEGA DELEGATION RITE: TOTALITY (V-Ω-TOTALITY-VMAX-NODE-SUTURE)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_DNA_DISPATCHER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_JSON_DELEGATED_VMAX_2026_FINALIS

        [THE MANIFESTO]
        This rite has been completely decapitated from the orchestrator monolith.
        It now securely summons the `NodeForger` to perform advanced bicameral
        NPM segregation and script auto-generation.
        =================================================================================
        """
        # [ASCENSION 1]: APOPHATIC IMPORT SHIELDING
        from .node_forger import NodeForger

        trace_id = variables.get("trace_id", "tr-node-manifest")

        if not variables.get("silent"):
            Logger.verbose(f"[{trace_id[:8]}] Orchestrator: Summoning the NodeForger for JS Genome inception.")

        try:
            # =========================================================================
            # == THE KINETIC HAND-OFF (THE STRIKE)                                   ==
            # =========================================================================
            # Delegate the entire array resolution, scripts injection, and module
            # typology enforcement to the dedicated Artisan.
            json_item = NodeForger.forge(deps, variables, parser)

            return json_item

        except Exception as delegation_fracture:
            import traceback
            error_details = f"NodeForger Shattered: {str(delegation_fracture)}\n{traceback.format_exc()}"
            Logger.critical(error_details)

            # [ASCENSION 2]: EMERGENCY REDEMPTION SUTURE
            # If the forger shatters, we return a warded Failure Item to prevent engine collapse.
            from pathlib import Path
            return ScaffoldItem(
                path=Path("package.json"),
                content=json.dumps(
                    {"error": f"Node.js Genome materialization failed. Reason: {str(delegation_fracture)}"}),
                line_type=GnosticLineType.FORM,
                mutation_op="*=",
                metadata={"origin": "Orchestrator_Emergency", "trace_id": trace_id}
            )

    @classmethod
    def forge_docker_compose(cls, services: Dict[str, Any], variables: Dict[str, Any],
                             parser: Any = None) -> ScaffoldItem:
        """
        =================================================================================
        == THE OMEGA DELEGATION RITE: TOTALITY (V-Ω-TOTALITY-VMAX-IRON-SUTURE)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_DNA_DISPATCHER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_DOCKER_DELEGATED_VMAX_2026_FINALIS

        [THE MANIFESTO]
        This rite has been completely decapitated from the orchestrator monolith.
        It now securely summons the `DockerForger` to perform advanced health checks,
        topological depends_on sorting, and Ghost-Dockerfile inception.
        =================================================================================
        """
        # [ASCENSION 1]: APOPHATIC IMPORT SHIELDING
        from .docker_forger import DockerForger

        trace_id = variables.get("trace_id", "tr-docker-manifest")

        if not variables.get("silent"):
            Logger.verbose(f"[{trace_id[:8]}] Orchestrator: Summoning the DockerForger for Iron Genome inception.")

        try:
            # =========================================================================
            # == THE KINETIC HAND-OFF (THE STRIKE)                                   ==
            # =========================================================================
            # Delegate the entire array resolution, dependency graph injection, and
            # autonomic Ghost-file inception to the dedicated Artisan.
            docker_item = DockerForger.forge(services, variables, parser)

            return docker_item

        except Exception as delegation_fracture:
            import traceback
            error_details = f"DockerForger Shattered: {str(delegation_fracture)}\n{traceback.format_exc()}"
            Logger.critical(error_details)

            # [ASCENSION 2]: EMERGENCY REDEMPTION SUTURE
            # If the forger shatters, we return a warded Failure Item to prevent engine collapse.
            from pathlib import Path
            return ScaffoldItem(
                path=Path("docker-compose.yml"),
                content=f"# [FRACTURE]: Iron Genome materialization failed.\n# Reason: {str(delegation_fracture)}\n",
                line_type=GnosticLineType.FORM,
                mutation_op="*=",
                metadata={"origin": "Orchestrator_Emergency", "trace_id": trace_id}
            )

    # =========================================================================
    # == INTERNAL OCULAR RADIATION                                           ==
    # =========================================================================

    @staticmethod
    def _radiate_hud_pulse(type_label: str, target: str, trace_id: str, variables: Dict[str, Any]):
        """[ASCENSION 62]: Radiates reification progress to the Ocular HUD."""
        engine = variables.get("__engine__")
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "METABOLIC_REIFICATION",
                        "label": type_label,
                        "message": f"Inscribing Genome into {target}",
                        "color": "#64ffda",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_MANIFEST_BUILDERS mode=TOTAL_REIFICATION status=RESONANT version=VMAX_2026>"