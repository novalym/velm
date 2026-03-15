# Path: src/velm/codex/loader/registry.py
# ---------------------------------------

"""
=================================================================================
== THE OMNISCIENT CODEX REGISTRY (V-Ω-TOTALITY-V50-LEGENDARY)                  ==
=================================================================================
LIF: INFINITY | ROLE: UNIVERSAL_KNOWLEDGE_LATTICE | RANK: OMEGA_SOVEREIGN

This is the divine, sentient memory of the God-Engine. It acts as the Central
Switchboard for all Gnostic Rites.

### THE PANTHEON OF ASCENSIONS:
1.  **The Global Resolver:** Intelligently routes `@Dockerfile` to `@cloud/dockerfile`
    via the `_global_rites` index.
2.  **Fuzzy Resonance:** If a user types `@dockrfile`, the Registry suggests
    `@Dockerfile` using Jaro-Winkler distance analysis.
3.  **Conflict Adjudication:** Detects if two domains claim the same global rite
    and forces the Architect to use explicit namespacing.
4.  **Schema Radiator:** Transmutes all registered skills into a JSON Schema
    for the React UI Flow editor.
5.  **Thread-Safe Mutex:** Protects the memory lattice during hot-reloads.
=================================================================================
"""

import difflib
import importlib
import inspect
import sys
import os
import time
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("CodexRegistry")

# [ASCENSION]: WASM Compatibility Check
_IS_WASM = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"


class CodexRegistry:
    """The Unbreakable Memory Lattice of the Velm Codex."""

    # --- THE TRINITY OF STORAGE ---
    _domains: Dict[str, Any] = {}
    _global_rites: Dict[str, List[Any]] = {}

    # State flags
    _is_loaded: bool = False
    _lock = threading.RLock()
    _watchdog_active: bool = False

    @classmethod
    def register_domain(cls, name: str, handler: Any, source: str = "Internal"):
        """
        [THE RITE OF CONSECRATION]
        Enshrines a new domain. Handles hierarchical overrides safely.
        """
        with cls._lock:
            # [ASCENSION]: Type Safety Duck-Typing
            # We check for the 'namespace' attribute to ensure it's a valid Domain.
            if not hasattr(handler, 'namespace'):
                Logger.error(f"Heresy: '{name}' attempted to register without valid Domain Contract.")
                return

            if name in cls._domains:
                old_source = getattr(cls._domains[name], '__gnostic_source__', 'Unknown')
                if source == "Project Forge":
                    Logger.info(f"Domain Override: Project atom [cyan]@{name}[/cyan] supersedes {old_source}.")
                elif source == "Internal" and old_source != "Internal":
                    # User overrides Internal; do not overwrite.
                    return
                else:
                    Logger.warn(
                        f"Domain Collision: Overwriting [cyan]@{name}[/cyan] (from {old_source}) with {source}.")
            else:
                # [ASCENSION]: Shadow Domain Stealth (Don't log internal utilities)
                if not name.startswith("_"):
                    Logger.info(f"Codex Domain consecrated:[bold cyan]@{name}[/bold cyan] (Source: {source})")

            # Stamp Biometric Provenance
            setattr(handler, '__gnostic_source__', source)
            setattr(handler, '__consecration_time__', time.time())

            cls._domains[name] = handler
            cls._index_global_rites(handler)

    @classmethod
    def _index_global_rites(cls, handler: Any):
        """
        [ASCENSION]: Global Alias Trie Builder.
        Extracts all `_directive_x` methods for namespace-less invocation.
        """
        for method_name in dir(handler):
            if method_name.startswith("_directive_") and not method_name.startswith("_directive___"):
                rite_name = method_name.replace("_directive_", "")

                if rite_name not in cls._global_rites:
                    cls._global_rites[rite_name] = []

                # Prevent duplicates from re-registration
                if handler not in cls._global_rites[rite_name]:
                    cls._global_rites[rite_name].append(handler)

    @classmethod
    def get_domain(cls, name: str) -> Optional[Any]:
        """Retrieves a specific domain by namespace."""
        cls.awaken()
        return cls._domains.get(name)

    @classmethod
    def list_domains(cls) -> Dict[str, Any]:
        """
        [THE CENSUS]
        Returns the complete map of known domains for CLI introspection.
        """
        cls.awaken()
        return cls._domains

    @classmethod
    def get_domain_and_rite(cls, namespace: Optional[str], rite_name: str) -> Tuple[Any, str]:
        """
        [THE GLOBAL RESOLVER] (Crucial for Injector)
        Finds the correct Domain Handler for a rite.
        If namespace is None (e.g. @Dockerfile), it scries ALL domains.
        """
        cls.awaken()
        rite_target = rite_name.lower().strip()

        with cls._lock:
            # --- PATH A: EXPLICIT NAMESPACE (@cloud/dockerfile) ---
            if namespace:
                domain = cls._domains.get(namespace.lower().strip())
                if not domain:
                    # [ASCENSION]: Fuzzy Resonance
                    suggestions = difflib.get_close_matches(namespace, cls._domains.keys(), n=1)
                    hint = f" Did you mean '@{suggestions[0]}'?" if suggestions else ""
                    raise ArtisanHeresy(f"Unknown Codex Domain: '@{namespace}'.{hint}")

                # Verify rite exists on domain
                if not hasattr(domain, f"_directive_{rite_target}"):
                    # Fuzzy Resonance for Rites
                    known = [r.replace('_directive_', '') for r in dir(domain) if r.startswith('_directive_')]
                    sug = difflib.get_close_matches(rite_target, known, n=1)
                    h = f" Did you mean '{sug[0]}'?" if sug else ""
                    raise ArtisanHeresy(f"Domain '@{namespace}' lacks the rite '{rite_target}'.{h}")

                return domain, rite_target

            # --- PATH B: IMPLICIT GLOBAL RITE (@Dockerfile) ---
            if rite_target not in cls._global_rites:
                # Deep Fuzzy Search
                all_rites = list(cls._global_rites.keys())
                sug = difflib.get_close_matches(rite_target, all_rites, n=1, cutoff=0.7)
                h = f" Did you mean '@{sug[0]}'?" if sug else ""
                raise ArtisanHeresy(f"Unknown Global Rite: '@{rite_name}'.{h}")

            matches = cls._global_rites[rite_target]

            if len(matches) == 1:
                return matches[0], rite_target

            # --- [ASCENSION]: CONFLICT ADJUDICATION ---
            # If multiple domains have @Dockerfile, we rank them.
            # 1. Project Forge wins.
            # 2. 'cloud' namespace wins for infra terms.
            ranked_matches = sorted(
                matches,
                key=lambda m: (
                    getattr(m, '__gnostic_source__', '') == 'Project Forge',
                    m.namespace == 'cloud'
                ),
                reverse=True
            )

            # Ambiguity Check
            top = ranked_matches[0]
            runner_up = ranked_matches[1]

            # If the sources are identical (e.g. both Internal), we have a true ambiguity.
            if getattr(top, '__gnostic_source__', '') == getattr(runner_up, '__gnostic_source__', ''):
                names = [m.namespace for m in matches]
                raise ArtisanHeresy(
                    f"Ambiguous Global Rite: '@{rite_name}'. The Engine perceived this rite in: {names}. "
                    f"You must use explicit syntax: '@namespace/{rite_name}'."
                )

            return top, rite_target

    @classmethod
    def awaken(cls, force_reload: bool = False):
        """The Master Boot Sequence. Delegates to the Scrier and Watchdog."""
        with cls._lock:
            if cls._is_loaded and not force_reload:
                return

            if force_reload:
                Logger.warn("Force Awakening. The Codex is wiped.")
                cls._domains.clear()
                cls._global_rites.clear()
                cls._is_loaded = False

            # Delegate to the Discovery Module (Lazy imported to prevent circularity)
            try:
                from .discovery import PluginScrier
                PluginScrier.scry_all_realms()
            except ImportError:
                # Fallback for bootstrap
                Logger.debug("PluginScrier not yet manifest. Proceeding with core.")

            cls._is_loaded = True
            Logger.success(f"Codex Resonant. {len(cls._domains)} domains manifest.")

            # Delegate to Watchdog (Iron Only)
            if not _IS_WASM and not cls._watchdog_active:
                try:
                    from .hot_reload import CodexWatchdog
                    CodexWatchdog.ignite()
                    cls._watchdog_active = True
                except ImportError:
                    pass

    @classmethod
    def export_context(cls) -> Dict[str, Any]:
        """
        =============================================================================
        == THE UNIVERSAL CONTEXT EXPORTER (V-Ω-DOT-NOTATION-BRIDGE)                ==
        =============================================================================
        Extracts all domains into a dictionary of `DomainProxy` objects.
        This is injected into the Alchemist and the Weaver.

        Usage in Blueprint: `{{ cloud.dockerfile(lang="node") }}`
        """
        cls.awaken()
        from .proxy import DomainProxy

        context_dict = {}
        with cls._lock:
            # 1. Map namespaces (e.g. "cloud" -> DomainProxy)
            for d_name, d_handler in cls._domains.items():
                context_dict[d_name] = DomainProxy(d_handler)

            # 2. Hoist Global Aliases to root level
            if "crypto" in cls._domains:
                context_dict["uuid"] = DomainProxy(cls._domains["crypto"]).uuid
            if "time" in cls._domains:
                context_dict["now"] = DomainProxy(cls._domains["time"]).now

        return context_dict

    @classmethod
    def generate_schema(cls) -> Dict[str, Any]:
        """
        [ASCENSION]: Schema Radiator.
        Generates the JSON Schema for the React Flow UI.
        """
        cls.awaken()
        schema = {"type": "object", "properties": {}}

        for d_name, d_handler in cls._domains.items():
            if hasattr(d_handler, 'get_manifest'):
                manifests = d_handler.get_manifest()
                domain_schema = {
                    "type": "object",
                    "description": d_handler.help(),
                    "rites": {}
                }
                for rite_name, manifest in manifests.items():
                    domain_schema["rites"][rite_name] = manifest.to_json_schema()

                schema["properties"][d_name] = domain_schema

        return schema