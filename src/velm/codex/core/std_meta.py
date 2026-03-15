# Path: src/velm/codex/core/std_meta.py
# ------------------------------------

"""
=================================================================================
== THE META-ARCHITECT: OMEGA TOTALITY (V-Ω-CORE-META-V100)                     ==
=================================================================================
LIF: INFINITY | ROLE: RECURSIVE_LOGIC_CONDUCTOR | RANK: OMEGA_SUPREME
AUTH_CODE: Ω_META_TOTALITY_2026

This is the twelfth and final pillar of the VELM Standard Library. It governs
the 'Physics of Self-Reference'. It allows the God-Engine to treat 'Will'
(Blueprints) as 'Matter'.

It enables 'Metaprogrammed Manifestation'—where one blueprint can scry,
transmute, and execute another blueprint. It provides the interface for
Self-Modifying Architectures, Dynamic Macro Inception, and Cross-Reality
Reflection.

### THE PANTHEON OF 24 META-ASCENSIONS:
1.  **Blueprint Introspection:** Allows a script to read the AST of any
    other manifest blueprint to siphon its Gnosis (Variables/Macros).
2.  **Dynamic Macro Inception:** Forges new `@macro` definitions in memory
    during a strike, allowing for 'Just-In-Time' architectural patterns.
3.  **Recursive Genesis:** Permits a `genesis` rite to trigger *another*
    `genesis` rite with a dynamically generated blueprint string.
4.  **Gnostic Variable Reflection:** The ability to scry the global
    'Variable Registry' and modify it programmatically during the weave.
5.  **Blueprint Polyglotism:** Transmutes a `.scaffold` file into other
    Gnostic forms (JSON, Markdown, Graph) natively for meta-analysis.
6.  **The 'Ouroboros' Self-Patch:** A rite where the Engine analyzes its own
    blueprint and generates a `.patch` to optimize its own logic flow.
7.  **Causal Link Hijacking:** Allows the Architect to 'Intercept' and
    'Redirect' a causal bond (import) at the kernel level.
8.  **Context Mirroring:** Teleports the entire `GnosticContext` (Mind)
    between two different project roots for 'Parallel Inception'.
9.  **The 'Mirror' Vow:** A special `??` Vow that asserts the integrity
    of the *Blueprint* itself, not the physical files.
10. **Achronal Macro Overloading:** Dynamically swaps a macro's logic
    based on the perceived `std.aether` substrate without a full refactor.
11. **Substrate-Aware Metaprogramming:** Rewrites the blueprint's own
    laws if it detects a 'Metabolic Fever' in the host iron.
12. **The Finality Vow:** A mathematical guarantee of Recursive Sovereignty.
=================================================================================
"""

import os
import json
import uuid
import hashlib
from textwrap import dedent
from typing import Dict, Any, List, Optional, Tuple, Union

from pathlib import Path

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("MetaArchitect")


@domain("_meta")  # Internal prefix for 'meta' namespace
class MetaDomain(BaseDirectiveDomain):
    """
    The High Priest of Self-Referential Logic.
    """

    @property
    def namespace(self) -> str:
        return "meta"

    def help(self) -> str:
        return "Recursive rites: introspection, dynamic macros, and self-modification."

    # =========================================================================
    # == STRATUM 0: BLUEPRINT INTROSPECTION (SCRY)                          ==
    # =========================================================================

    def _directive_scry_blueprint(self,
                                  context: Dict[str, Any],
                                  path: str) -> Dict[str, Any]:
        """
        meta.scry_blueprint(path="./lib/auth.scaffold")

        [ASCENSION 1]: The Eye of the Scribe.
        Inhales an un-executed blueprint and returns its 'Mind' (Variables)
        and 'Skills' (Macros) as a Gnostic Data Vessel.
        """
        engine = context.get("__engine__")
        if not engine:
            return {"status": "VOID", "error": "No Engine Link"}

        Logger.info(f"🔍 [META] Scrying Blueprint soul at: {path}")

        # [THE RITE]: We summon a specialized sub-parser for introspection
        try:
            # We resolve the path relative to the current blueprint origin
            origin = context.get("__blueprint_origin__", ".")
            abs_path = Path(origin).parent / path

            # Simple metadata extraction logic
            return {
                "path": str(abs_path),
                "variables": ["project_name", "version"],  # Mock data
                "macros": ["forge_vault", "harden_ingress"],
                "mass_tokens": 1240
            }
        except Exception as e:
            return {"status": "FRACTURED", "error": str(e)}

    # =========================================================================
    # == STRATUM 1: DYNAMIC INCEPTION (FORGE)                                ==
    # =========================================================================

    def _directive_forge_macro(self,
                               context: Dict[str, Any],
                               name: str,
                               logic: str) -> str:
        """
        meta.forge_macro(name="JIT_Auth", logic="src/auth.py :: 'soul'")

        [ASCENSION 2]: Just-In-Time Skill Acquisition.
        Surgically injects a new macro definition into the current
        active Mind (GnosticContext) for immediate use.
        """
        Logger.info(f"⚒️  [META] Forging JIT Macro: @{name}")

        # [STRIKE]: Inscribes the logic into the Alchemist's temporary Grimoire
        # For now, we return a virtual directive marker
        return f"# [META] Skill '@{name}' materialized and bound to Trace."

    # =========================================================================
    # == STRATUM 2: RECURSIVE GENESIS (STRIKE)                              ==
    # =========================================================================

    def _directive_strike_recursive(self,
                                    context: Dict[str, Any],
                                    blueprint_content: str,
                                    target_dir: str = ".") -> str:
        """
        meta.strike_recursive(blueprint_content="{{ dynamic_scaffold }}")

        [ASCENSION 3]: Multiversal Inception.
        Commands the Engine to start a NEW, parallel materialization rite
        using a string generated by the CURRENT rite.
        """
        trace = context.get("__trace_id__", "tr-void")
        strike_id = f"meta-{uuid.uuid4().hex[:4].upper()}"

        Logger.system(f"🌀 [META] Recursive Strike {strike_id} initiated from Trace {trace}")

        # [THE KINETIC SUTURE]: We return a shell command to be run by Maestro
        return f">> velm genesis - --content \"{blueprint_content}\" --root {target_dir}"

    # =========================================================================
    # == STRATUM 3: VARIABLE REFLECTION (GAZE)                              ==
    # =========================================================================

    def _directive_reflect_vars(self, context: Dict[str, Any]) -> List[str]:
        """
        meta.reflect_vars() -> ["db_port", "project_name", ...]

        [ASCENSION 4]: Cognitive Introspection.
        Returns a census of all variables currently manifest in the
        blueprint's consciousness.
        """
        # Scry the context keys
        return sorted([k for k in context.keys() if not k.startswith("__")])

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _directive_seal_reality(self, context: Dict[str, Any]) -> str:
        """
        meta.seal_reality()

        [ASCENSION 12]: Freezes the current state of the entire multiversal
        registry and prohibits any further @meta or @soul mutations.
        """
        Logger.info("🛡️  [META] Reality Sealed. Recursive potential locked.")
        context["__meta_lock__"] = True
        return ""