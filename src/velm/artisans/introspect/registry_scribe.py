# Path: artisans/introspect/registry_scribe.py
# --------------------------------------------

import inspect
from typing import Dict, Any, List

# --- THE DIVINE SUMMONS OF THE LAW ---
from ...core.cli.grimoire import RITE_GRIMOIRE
from ...logger import Scribe

Logger = Scribe("RegistryScribe")


class RegistryScribe:
    """
    =============================================================================
    == THE SCRIBE OF THE GRIMOIRE (V-Ω-UI-METADATA-INJECTOR)                   ==
    =============================================================================
    LIF: 10,000,000,000

    Transmutes the raw CLI `RITE_GRIMOIRE` into a rich, UI-ready manifest.
    It applies Gnostic Heuristics to assign Categories, Icons, and Tags
    dynamically, ensuring the Frontend receives a complete Soul.
    """

    # The Grimoire of Categories (Heuristic Mapping)
    CATEGORY_MAP = {
        "genesis": "Genesis", "init": "Genesis", "create": "Genesis",
        "transmute": "Evolution", "patch": "Evolution", "translocate": "Evolution",
        "conform": "Evolution", "refactor": "Evolution", "weave": "Evolution", "excise": "Evolution",
        "architect": "Intelligence", "manifest": "Intelligence", "resurrect": "Intelligence",
        "resonate": "Intelligence", "aether": "Intelligence", "ocular": "Intelligence",
        "distill": "Perception", "analyze": "Perception", "mri": "Perception",
        "graph": "Perception", "tree": "Perception", "read-soul": "Perception", "verify": "Perception",
        "audit": "Security", "isolate": "Security", "fortify": "Security", "deploy": "Infrastructure",
        "symphony": "Operations", "build": "Operations", "evolve": "Operations", "garden": "Operations",
        "history": "Temporal", "undo": "Temporal", "holographic": "Temporal", "akasha": "Temporal",
        "pad": "Interface", "studio": "Interface", "shell": "Interface", "gui": "Interface",
    }

    # The Grimoire of Icons (Lucide Names)
    ICON_MAP = {
        "genesis": "Zap", "init": "MessageSquare", "create": "PlusSquare",
        "transmute": "RefreshCw", "translocate": "Move", "conform": "AlignCenter",
        "patch": "Syringe", "refactor": "Hammer", "weave": "Cpu",
        "architect": "BrainCircuit", "manifest": "Sparkles", "resurrect": "Flame",
        "resonate": "Radio", "aether": "Wifi", "ocular": "Eye",
        "distill": "Microscope", "analyze": "Activity", "mri": "HeartPulse",
        "graph": "Map", "tree": "GitMerge", "verify": "ShieldCheck",
        "audit": "Lock", "isolate": "ShieldAlert", "deploy": "Cloud",
        "symphony": "Play", "build": "Hammer", "evolve": "Database",
        "garden": "Scissors", "history": "History", "undo": "RotateCcw",
        "holographic": "Camera", "akasha": "Library", "pad": "Layout",
        "studio": "Monitor", "shell": "Terminal", "gui": "Box"
    }

    @classmethod
    def proclaim_gnosis(cls) -> Dict[str, Any]:
        """
        The Rite of Reflection.
        Returns a dictionary mapping Command IDs to GnosticTool definitions.
        """
        Logger.verbose("The Registry Scribe reads the Grimoire...")

        registry_manifest = {}

        for cmd_name, config in RITE_GRIMOIRE.items():
            # 1. Divine Metadata
            category = cls.CATEGORY_MAP.get(cmd_name, "Utilities")
            icon = cls.ICON_MAP.get(cmd_name, "Box")

            # 2. Divine Complexity
            # If it has specific interaction flags or is a TUI, it is interactive.
            complexity = "instant"
            if "interactive" in str(config.get("flags", [])) or cmd_name in ["architect", "manifest", "pad", "studio",
                                                                             "gui", "repl"]:
                complexity = "interactive"
            elif "daemon" in cmd_name:
                complexity = "daemon"

            # 3. Forge Tags
            tags = [category]
            if "subparsers" in config:
                tags.append("Multi-Rite")
                tags.extend(config["subparsers"].keys())

            # 4. Construct the Gnostic Tool Object
            # This schema matches the TypeScript `GnosticTool` interface exactly.
            tool_definition = {
                "id": cmd_name,
                "name": cmd_name.replace("-", " ").title(),
                "description": config.get("help", "No gnosis provided."),
                "command": f"scaffold {cmd_name}",
                "category": category,
                "icon": icon,
                "complexity": complexity,
                "tags": tags,
                "isPlugin": False  # Native rites are false
            }

            registry_manifest[cmd_name] = tool_definition

        Logger.success(f"Registry Scribe has indexed {len(registry_manifest)} rites.")
        return registry_manifest


def proclaim_gnosis():
    """Public gateway for the Conductor."""
    return RegistryScribe.proclaim_gnosis()