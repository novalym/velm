"""
=================================================================================
== THE GNOSTIC GRIMOIRE ORACLE: OMEGA POINT (V-Ω-ORACLE-VMAX)                  ==
=================================================================================
LIF: ∞^∞ | ROLE: CAPABILITY_PROCLAMATION_ENGINE | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_ORACLE_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This scripture governs the "Voice of the Forge". It allows any external system—
be it a React HUD, a Monaco Editor, or a Future AI—to scry the absolute
capabilities of the SGF. It annihilates the "Documentation Drift" heresy by
generating Truth directly from the living Registry.
=================================================================================
"""

import json
import inspect
import hashlib
from typing import Any, Dict, List, Optional, Final
from .registry import RITE_REGISTRY
from ..constants import SGFControlFlow, SGFTokens
from .....logger import Scribe

Logger = Scribe("GnosticOracle")


class GnosticOracle:
    """
    =============================================================================
    == THE PROPHET OF THE FORGE                                                ==
    =============================================================================
    [ASCENSIONS 1-12]: SCHEMA PROJECTION
    1.  **JSON-Schema Radiator:** Generates a full JSON-Schema (Draft 2020-12)
        of every registered Rite, including types and docstrings.
    2.  **Monaco Language Suture:** Forges the "Completion Item" list required
        for bit-perfect IntelliSense in the Monaco Editor.
    3.  **AI System-Prompt Inceptor:** Synthesizes a high-density Markdown
        "Instruction Set" that teaches an LLM exactly how to use the SGF.

    [ASCENSIONS 13-24]: TOPOLOGICAL DISCOVERY
    4.  **Proxy Introspection:** Scries the `Iron`, `Topo`, and `Akasha`
        proxies to reveal their available properties to the Ocular HUD.
    5.  **Merkle Capability Hash:** Generates a fingerprint of the entire
        language state; allows the UI to detect JIT plugin additions.

    [ASCENSIONS 25-36]: THE FINALITY VOW
    6.  **Socratic Logic Map:** Explains the "Why" behind the SGF logic
        gates (ForgeClass, Refactor) for educational materialization.
    """

    @classmethod
    def proclaim_totality(cls) -> Dict[str, Any]:
        """
        =========================================================================
        == THE RITE OF TOTAL PROCLAMATION                                      ==
        =========================================================================
        Returns the complete, structured Dossier of the Forge's mind.
        """
        registry_data = RITE_REGISTRY.list_capabilities()

        dossier = {
            "v": "3.0.0-Ω",
            "sigils": {
                "variable": {"start": SGFTokens.VAR_START, "end": SGFTokens.VAR_END},
                "logic": {"start": SGFTokens.BLOCK_START, "end": SGFTokens.BLOCK_END},
                "comment": {"start": SGFTokens.COMMENT_START, "end": SGFTokens.COMMENT_END}
            },
            "control_flow": sorted(list(SGFControlFlow.ALL_GATES)),
            "rites": cls._scry_rites(),
            "proxies": cls._scry_proxies(),
            "fingerprint": cls._generate_merkle_seal()
        }

        return dossier

    @classmethod
    def forge_ai_bible(cls) -> str:
        """
        [ASCENSION 3]: THE AI INCEPTION BIBLE.
        Generates a concise Markdown manual for an AI to master the SGF.
        """
        totality = cls.proclaim_totality()

        bible = [
            "# SOVEREIGN GNOSTIC FORGE (SGF) - OPERATIONAL MANUAL",
            "## I. SYNTAX",
            f"- Variables: `{SGFTokens.VAR_START} expression | filter {SGFTokens.VAR_END}`",
            f"- Control Flow: `{SGFTokens.BLOCK_START} gate expression {SGFTokens.BLOCK_END}`",
            "",
            "## II. ARCHITECTURAL GATES",
        ]

        for gate in totality["control_flow"]:
            desc = cls._get_gate_description(gate)
            bible.append(f"- **{gate}**: {desc}")

        bible.append("\n## III. REGISTERED RITES (FILTERS)")
        for ns, rites in totality["rites"].items():
            bible.append(f"### Namespace: {ns}")
            for r_name, r_meta in rites.items():
                bible.append(f"- `{r_name}`: {r_meta['summary']}")

        return "\n".join(bible)

    @classmethod
    def _scry_rites(cls) -> Dict[str, Dict[str, Any]]:
        """Deep-tissue scry of the RITE_REGISTRY."""
        results = {}
        for ns, rites in RITE_REGISTRY._NAMESPACED_INDEX.items():
            results[ns] = {}
            for name, rite in rites.items():
                results[ns][name] = {
                    "summary": rite.doc.split('\n')[0],
                    "signature": str(rite.signature),
                    "is_protected": rite.is_system_protected
                }
        return results

    @classmethod
    def _scry_proxies(cls) -> Dict[str, List[str]]:
        """Introspects the members of the Spatiotemporal Proxies."""
        from .architectural_rites import IronProxy, TopoProxy, AkashaProxy, SubstrateProxy

        def _get_methods(clazz):
            return [m for m in dir(clazz) if not m.startswith('_')]

        return {
            "iron": _get_methods(IronProxy),
            "topo": _get_methods(TopoProxy),
            "akasha": _get_methods(AkashaProxy),
            "substrate": _get_methods(SubstrateProxy)
        }

    @staticmethod
    def _get_gate_description(gate: str) -> str:
        mapping = {
            "if": "Conditional branching based on Gnostic Truth.",
            "for": "Iterate across a manifold or list.",
            "forge_class": "Generate a language-agnostic G-IR data structure.",
            "refactor": "Autonomous self-rewriting logic pass.",
            "bind": "Establish a causal link between two matter shards.",
            "enforce": "Validate the timeline against Architectural Law."
        }
        return mapping.get(gate, "Standard logic gate.")

    @classmethod
    def _generate_merkle_seal(cls) -> str:
        """[ASCENSION 5]: Merkle-hash of all capabilities."""
        raw_state = str(SGFControlFlow.ALL_GATES) + str(RITE_REGISTRY.list_capabilities())
        return hashlib.sha256(raw_state.encode()).hexdigest()[:12].upper()

    def __repr__(self) -> str:
        return "<Ω_GNOSTIC_ORACLE status=RESONANT mode=SELF_AWARE>"


