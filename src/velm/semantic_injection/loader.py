# Path: scaffold/semantic_injection/loader.py

"""
=================================================================================
== THE CORTEX LOADER (V-Ω-GOD-ENGINE. THE HYPER-DIAGNOSTIC ORACLE)             ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000!

This is the divine, sentient, and final form of the Semantic Cortex's soul. It is a
true God-Engine of Gnostic Revelation whose Prime Directive is to awaken every
domain and component in the Scaffold cosmos and, if its Gaze falters, to proclaim
a luminous, hyper-diagnostic Dossier of Heresy revealing the precise point of failure.

Its every faculty has been ascended. Its Gaze is absolute. Its voice is truth.
=================================================================================
"""
import difflib
import importlib
import importlib.util
import inspect
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, Any, Optional

from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe

Logger = Scribe("SemanticCortex")


class SemanticRegistry:
    """
    The Central Repository of Gnostic Domains, now a hyper-aware Oracle.
    """

    # The Sanctum of Knowledge (Name -> Handler)
    _domains: Dict[str, Any] = {}
    _is_loaded: bool = False
    _resolution_cache: Dict[str, str] = {}  # Faculty 4: Chronocache

    # Regex for the Robust Lexer (Faculty 3)
    PROP_REGEX = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^,\s()]+))')

    @classmethod
    def register_domain(cls, name: str, handler: Any, source: str = "Internal"):
        """
        [THE RITE OF REGISTRATION]
        Enshrines a domain handler with luminous, hyper-diagnostic proclamation.
        """
        # Faculty 7: Conflict Adjudicator & Faculty 12: Luminous Scribe
        if name in cls._domains:
            # We must proclaim the source of the old and new Gnosis for a perfect inquest.
            old_source = getattr(cls._domains[name], '__gnostic_source__', 'Unknown')
            Logger.warn(
                f"Domain Conflict: Overwriting Domain '@{name}' (from {old_source}) with new Gnosis from {source}.")
        else:
            # ★★★ THE LUMINOUS VOICE ★★★
            # This is the Gnosis you seek. It will proclaim the name of every
            # domain as it is consecrated.
            Logger.info(f"Domain consecrated: [bold cyan]@{name}[/bold cyan] (Source: {source})")

        # We bestow upon the handler a memory of its own origin.
        setattr(handler, '__gnostic_source__', source)
        cls._domains[name] = handler

        # Faculty 5: Dependency Sentinel
        if hasattr(handler, "__requires__"):
            reqs = getattr(handler, "__requires__")
            Logger.verbose(f"   -> Domain @{name} declares dependencies: {reqs}")

    @classmethod
    def get_domain(cls, name: str) -> Optional[Any]:
        """
        =================================================================================
        == THE GAZE OF HUMILITY (V-Ω-ETERNAL-APOTHEOSIS. THE SEVERED LINK)             ==
        =================================================================================
        This is the divine rite in its new, pure, and humble form. The profane, zealous
        plea to `awaken()` has been annihilated from its soul. It no longer presumes to
        know when the cosmos should awaken. Its one true purpose is now to gaze upon the
        Gnosis that is already manifest and proclaim its findings. The circular heresy is
        not just slain; it is made architecturally impossible.
        =================================================================================
        """
        # The profane call is annihilated. The Cortex must be awakened by the one true Conductor.
        # cls.awaken()
        return cls._domains.get(name)

    @classmethod
    def list_domains(cls) -> Dict[str, Any]:
        """Returns the complete map of known domains."""
        cls.awaken()
        return cls._domains

    @classmethod
    def awaken(cls, force_reload: bool = False):
        """
        =================================================================================
        == THE GOD-ENGINE OF DYNAMIC DISCOVERY (V-Ω-ETERNAL-APOTHEOSIS-ULTRA-DIAGNOSTIC) ==
        =================================================================================
        This rite now speaks with a Luminous Voice, proclaiming its every thought and
        action to the Gnostic Chronicle for a perfect, hyper-diagnostic inquest.
        =================================================================================
        """
        if cls._is_loaded and not force_reload:
            return

        if force_reload:
            Logger.warn("Architect has commanded a Force Awakening. The Cortex forgets all it knows...")
            cls._domains = {}
            cls._is_loaded = False

        Logger.info("Semantic Cortex awakens. Performing deep Gaze upon Internal Soul...")

        # --- MOVEMENT I: THE GAZE OF THE INTERNAL SOUL (ASCENDED & LUMINOUS) ---
        try:
            internal_directives_path_str = "velm.semantic_injection.directives"
            package = importlib.import_module(internal_directives_path_str)

            if not hasattr(package, '__path__') or not package.__path__:
                Logger.error("A catastrophic paradox occurred: The 'directives' package has no physical path.")
                return

            package_root_path = Path(package.__path__[0])
            Logger.verbose(f"   -> Gnostic Sanctum found at: [dim]{package_root_path}[/dim]")

            # We perform a recursive Gaze for all Python scriptures.
            all_py_files = list(package_root_path.rglob("*.py"))
            Logger.verbose(f"   -> Perceived {len(all_py_files)} potential Gnostic souls in the sanctum.")

            for py_file in all_py_files:
                if py_file.stem == "__init__":
                    continue

                relative_path = py_file.relative_to(package_root_path)
                module_suffix = '.'.join(relative_path.with_suffix('').parts)
                module_name = f"{internal_directives_path_str}.{module_suffix}"

                cls._try_import(module_name, "Internal (Deep Gaze)")

        except Exception as e:
            Logger.error(f"A catastrophic paradox shattered the Internal Gaze of the Cortex: {e}", exc_info=True)

        # --- MOVEMENT II: THE GAZE OF THE ARCHITECT'S WILL (UNCHANGED AND PURE) ---
        gaze_paths = [
            ("Project Forge", Path.cwd() / ".scaffold" / "generators"),
            ("Global Forge", Path.home() / ".scaffold" / "generators"),
        ]

        for source, path in gaze_paths:
            if path.is_dir():
                Logger.verbose(f"Performing Gaze upon the {source} at: {path}")
                for py_file in path.rglob("*.py"):
                    if py_file.stem.startswith("_"): continue
                    relative_path = py_file.relative_to(path)
                    module_name = f"user_forge.{relative_path.with_suffix('').as_posix().replace('/', '.')}"
                    cls._try_import_from_path(module_name, py_file, source)

        cls._is_loaded = True
        Logger.success(f"Cortex online. {len(cls._domains)} domains are now fully active and consecrated.")

    @staticmethod
    def _try_import(module_name: str, source: str) -> bool:
        """A divine, shielded artisan for summoning an internal module's soul."""
        try:
            importlib.import_module(module_name)
            # The verbose log remains, but the new `register_domain` INFO log will be clearer.
            Logger.verbose(f"   -> Awakened Gnostic soul: '{module_name}' ({source})")
            return True
        except Exception as e:
            Logger.error(
                f"A paradox occurred while awakening soul '{module_name}' from {source}: {e}\n{traceback.format_exc()}")
            return False

    @staticmethod
    def _try_import_from_path(module_name: str, file_path: Path, source: str) -> bool:
        """
        [THE JUST-IN-TIME ALCHEMIST]
        A divine, shielded artisan for summoning a user-forged module's soul from a raw path.
        """
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                Logger.warn(f"Could not forge a Gnostic soul for '{file_path}'. It may be a profane scripture.")
                return False
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            Logger.verbose(f"   -> Awakened user-forged soul: '{module_name}' ({source})")
            return True
        except Exception as e:
            Logger.error(
                f"A paradox occurred while awakening user-forged soul '{file_path.name}': {e}\n{traceback.format_exc()}")
            return False

    # The `resolve` and `manifest` methods remain pure and unchanged.
    @classmethod
    def resolve(cls, directive_string: str, context: Dict[str, Any]) -> str:
        """
        [THE GRAND ROUTER]
        Parses "@domain/rite(props...)" and dispatches to the correct handler with
        unbreakable, hyper-diagnostic grace.
        """
        # Faculty 4: Chronocache
        cache_key = f"{directive_string}:{hash(frozenset(context.items()))}"
        if cache_key in cls._resolution_cache:
            return cls._resolution_cache[cache_key]

        cls.awaken()

        # 1. Parse the Directive String
        match = re.match(r'^@([\w-]+)/([\w-]+)(?:\((.*)\))?$', directive_string.strip())
        if not match:
            raise ArtisanHeresy(f"Malformed directive syntax: '{directive_string}'")

        domain_name, rite_name, args_str = match.groups()

        # 2. Locate Domain Handler
        handler = cls.get_domain(domain_name)
        if not handler:
            # Faculty 2: The Fuzzy Oracle
            suggestions = difflib.get_close_matches(domain_name, cls._domains.keys(), n=1)
            hint = f" Did you mean '@{suggestions[0]}'?" if suggestions else f" Known domains are: {list(cls._domains.keys())}"
            raise ArtisanHeresy(f"Unknown Semantic Domain: '@{domain_name}'.{hint}")

        # 3. Locate Rite (The Generator Function/Method)
        # We must now perform a Gaze upon the handler to find a method that
        # has been consecrated for this rite. We look for `_directive_<rite_name>`.
        rite_method_name = f"_directive_{rite_name}"
        generator = getattr(handler, rite_method_name, None)

        if not callable(generator):
            # Faculty 2: Fuzzy Oracle for Rites
            known_rites = [r.replace('_directive_', '') for r in dir(handler) if r.startswith('_directive_')]
            suggestions = difflib.get_close_matches(rite_name, known_rites, n=1)
            hint = f" Did you mean '{suggestions[0]}'?" if suggestions else f" Known rites are: {known_rites}"
            raise ArtisanHeresy(f"Domain '@{domain_name}' has no consecrated rite named '{rite_name}'.{hint}")

        # 4. Parse Arguments (Faculty 3: Robust Lexer)
        props: Dict[str, Any] = {}
        if args_str:
            for match in cls.PROP_REGEX.finditer(args_str):
                key = match.group(1)
                val = match.group(2) or match.group(3) or match.group(4)

                # Faculty 11: Type Normalizer
                if isinstance(val, str):
                    if val.lower() == 'true':
                        val = True
                    elif val.lower() == 'false':
                        val = False
                    elif val.isdigit():
                        val = int(val)
                props[key] = val

        # 5. Invoke the Rite with the Unbreakable Ward
        try:
            # The sacred contract: The generator receives the full props dict and the context.
            result = generator(props, context)
            cls._resolution_cache[cache_key] = result  # Cache the pure result
            return result
        except Exception as e:
            # Faculty 10: The Safety Ward & Hyper-Diagnostic Heresy
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(f"A paradox occurred while conducting the '@{domain_name}/{rite_name}' rite: {e}",
                                child_heresy=e) from e

    @classmethod
    def manifest(cls) -> Dict[str, Any]:
        """
        [FACULTY 8: THE INTROSPECTIVE API]
        Returns a structured dossier of all domains and rites for the Studio UI.
        """
        cls.awaken()
        dossier: Dict[str, Dict[str, Any]] = {}
        for name, handler in cls._domains.items():
            # The Gaze of Gnostic Provenance
            source = getattr(handler, '__gnostic_source__', 'Unknown')
            # The Gaze of the Soul (Docstring)
            doc = inspect.getdoc(handler) or "No Gnosis provided."

            # The Gaze of the Rites
            rites = [
                r.replace('_directive_', '') for r in dir(handler) if r.startswith('_directive_')
            ]

            dossier[name] = {"source": source, "rites": rites, "doc": doc}
        return dossier


def domain(name: str):
    """A sacred decorator to register a class as a Semantic Domain handler."""

    def decorator(cls):
        # We instantiate the class to create the handler instance
        SemanticRegistry.register_domain(name, cls())
        return cls

    return decorator