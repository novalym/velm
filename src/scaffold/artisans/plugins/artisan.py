# Path: artisans/plugins/artisan.py
# ---------------------------------
import hashlib
import json
import math
from functools import lru_cache
from typing import Dict, Any, List, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import PluginsRequest
from ...help_registry import register_artisan
from ...core.cli.grimoire import RITE_GRIMOIRE


@register_artisan("plugins")
class PluginsArtisan(BaseArtisan[PluginsRequest]):
    """
    =============================================================================
    == THE PLUGINS CENSUS (V-Ω-HYDRODYNAMIC-ASCENDED-V2)                       ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: CAPABILITY_ORACLE

    The Sovereign Cataloger. It reads the Laws (Grimoire), applies the
    Light-Matter Protocol to compress the payload, and serves the UI
    with zero-latency Gnosis.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Lean Protocol:** Aggressively truncates heavy text (descriptions > 60 chars) and limits tags to prevent JSON bloat.
    2.  **Immutable Chronocache:** The heavy parsing of the Grimoire is performed ONCE and cached in RAM. Subsequent calls are O(1).
    3.  **Categorical Sieve:** Applies server-side filtering before serialization to minimize data transfer.
    4.  **Pagination Forensics:** Supports `limit` and `offset` for chunked loading (Future-Proofing).
    5.  **Complexity Divination:** Scans flags (`--interactive`) to determine if a tool requires a modal.
    6.  **Safety Rating System:** Auto-detects destructive verbs (`delete`, `prune`) and marks them `CRITICAL`.
    7.  **Visual Cortex (Icon Map):** A complete Lucide mapping for every known tool.
    8.  **Search Vector Injection:** Pre-computes a lowercase search string for instant client-side filtering.
    9.  **UI Component Bridge:** Links tools to their specific React implementation (`uiComponent`).
    10. **Merkle Pulse:** Generates a hash of the current plugin set for cache invalidation.
    11. **Shortcut Prophecy:** Injects standard keybindings (e.g. `Ctrl+S` for Save).
    12. **The Void Guard:** Robust handling of missing metadata or malformed Grimoire entries.
    """

    # [ASCENSION 7]: THE ICONOGRAPHY CODEX (Visual Soul)
    ICON_MAP = {
        "genesis": "Zap", "init": "MessageSquare", "create": "PlusSquare",
        "arch": "Layers", "manifest": "Sparkles", "mock": "Box", "dream": "Cloud",
        "transmute": "RefreshCw", "patch": "Syringe", "translocate": "Move",
        "conform": "AlignCenter", "refactor": "Hammer", "weave": "Cpu",
        "excise": "Trash2", "remove": "Eraser", "compose": "Network",
        "upgrade": "Flame", "schema": "Database", "evolve": "Database",
        "fuse": "Zap", "distill": "Microscope", "analyze": "Activity",
        "mri": "HeartPulse", "graph": "Map", "tree": "GitMerge",
        "verify": "ShieldCheck", "inspect": "Eye", "blame": "Fingerprint",
        "lint": "FileWarning", "hunt": "Ghost", "read-soul": "Eye",
        "sgrep": "FileSearch", "semdiff": "ArrowRightLeft", "summarize": "BookOpen",
        "matrix": "Grid", "risk": "AlertTriangle", "architect": "BrainCircuit",
        "agent": "Bot", "holocron": "Search", "scribe": "PenTool",
        "muse": "Sparkles", "query": "Search", "debate": "Users",
        "train": "Brain", "translate": "Languages", "resonate": "Radio",
        "ocular": "Eye", "mimic": "Copy", "introspect": "Search",
        "resurrect": "Flame", "vector": "Database", "telepathy": "Wifi",
        "neural": "Brain", "aether": "Wifi", "symphony": "Play",
        "run": "Play", "daemon": "Server", "watch": "Activity",
        "settings": "Settings2", "runtimes": "Server", "templates": "Archive",
        "alias": "Keyboard", "install": "Package", "ci-optimize": "Dna",
        "self-test": "ShieldCheck", "save": "Save", "snippet": "Braces",
        "repl": "Terminal", "qr": "QrCode", "workspace": "Orbit",
        "observatory": "Orbit", "studio": "Monitor", "shell": "Terminal",
        "pad": "Tablet", "gui": "Command", "tool": "Wrench",
        "beautify": "Wand2", "garden": "Scissors", "build": "Hammer",
        "isolate": "ShieldAlert", "audit": "Lock", "signature": "Fingerprint",
        "with": "Lock", "deploy": "Cloud", "expose": "Globe",
        "prophesy": "DollarSign", "fortify": "Shield", "canon": "Scale",
        "freeze": "Snowflake", "ignore": "EyeOff", "history": "History",
        "undo": "RotateCcw", "time-branch": "GitBranch", "time-machine": "History",
        "replay": "Timer", "akasha": "Library", "holographic": "Camera",
        "shadow": "Copy", "plugins": "Grid", "preview": "Monitor",
        "help": "BookOpen"
    }

    # [ASCENSION 1]: THE TAXONOMY MAP
    CATEGORY_MAP = {
        "genesis": "Genesis", "init": "Genesis", "create": "Genesis", "arch": "Genesis",
        "mock": "Genesis", "dream": "Genesis",
        "transmute": "Evolution", "patch": "Evolution", "translocate": "Evolution",
        "conform": "Evolution", "refactor": "Evolution", "weave": "Evolution",
        "excise": "Evolution", "upgrade": "Evolution", "remove": "Evolution",
        "schema": "Evolution", "compose": "Evolution",
        "architect": "Intelligence", "manifest": "Intelligence", "resurrect": "Intelligence",
        "resonate": "Intelligence", "aether": "Intelligence", "ocular": "Intelligence",
        "train": "Intelligence", "agent": "Intelligence", "holocron": "Intelligence",
        "scribe": "Intelligence", "muse": "Intelligence", "query": "Intelligence",
        "debate": "Intelligence", "translate": "Intelligence", "mimic": "Intelligence",
        "introspect": "Intelligence", "vector": "Intelligence", "telepathy": "Intelligence",
        "neural": "Intelligence",
        "distill": "Perception", "analyze": "Perception", "mri": "Perception",
        "graph": "Perception", "tree": "Perception", "read-soul": "Perception",
        "verify": "Perception", "risk": "Perception", "inspect": "Perception",
        "blame": "Perception", "lint": "Perception", "hunt": "Perception",
        "sgrep": "Perception", "semdiff": "Perception", "summarize": "Perception",
        "matrix": "Perception", "preview": "Perception",
        "audit": "Security", "isolate": "Security", "fortify": "Security",
        "signature": "Security", "with": "Security", "canon": "Security",
        "freeze": "Security", "ignore": "Security",
        "deploy": "Infrastructure", "prophesy": "Infrastructure",
        "symphony": "Operations", "build": "Operations", "evolve": "Operations",
        "garden": "Operations", "tool": "Operations", "settings": "Operations",
        "runtimes": "Operations", "templates": "Operations", "alias": "Operations",
        "install": "Operations", "ci-optimize": "Operations", "self-test": "Operations",
        "save": "Operations", "snippet": "Operations", "repl": "Operations",
        "qr": "Operations", "workspace": "Operations", "observatory": "Operations",
        "fuse": "Operations", "beautify": "Operations",
        "history": "Temporal", "undo": "Temporal", "holographic": "Temporal",
        "akasha": "Temporal", "time-machine": "Temporal", "time-branch": "Temporal",
        "replay": "Temporal", "shadow": "Temporal",
        "pad": "Interface", "studio": "Interface", "shell": "Interface",
        "gui": "Interface", "help": "Interface",
        "plugins": "System"
    }

    # [ASCENSION 9]: UI COMPONENT MAP
    UI_COMPONENT_MAP = {
        "studio": "StudioInstrument",
        "manifest": "ManifestInstrument",
        "resurrect": "ResurrectInstrument",
        "deploy": "DeployInstrument",
        "observe": "ObserveRite",
        "train": "TrainInstrument",
        "run": "RunRite",
        "workspace": "WorkspaceInstrument",
        "with": "WithInstrument",
        "watch": "WatchInstrument",
        "inspect": "InspectInstrument",
        "evolve": "SchemaInstrument",
        "save": "SaveRite",
        "teach": "TeachInstrument",
        "read-soul": "ReadSoulInstrument",
        "mock": "MockInstrument",
        "ignore": "IgnoreInstrument",
        "freeze": "FreezeInstrument",
        "canon": "CanonInstrument",
        "build": "BuildInstrument",
        "mri": "MRIInstrument"
    }

    # [ASCENSION 11]: SHORTCUT PROPHECY
    SHORTCUT_MAP = {
        "save": "Ctrl+S",
        "run": "Ctrl+Enter",
        "genesis": "Alt+G",
        "distill": "Alt+D",
        "transmute": "Alt+T",
        "refactor": "Alt+R",
        "inspect": "Alt+I"
    }

    def execute(self, request: PluginsRequest) -> ScaffoldResult:
        """
        [THE RITE OF CENSUS]
        Retrieves, filters, and compresses the tool registry.
        """
        # 1. FETCH FROM CHRONOCACHE (O(1))
        all_tools = self._get_cached_tools()

        # 2. CATEGORICAL SIEVE (Filter)
        filtered_tools = all_tools
        if request.category:
            target_cat = request.category.lower()
            filtered_tools = [t for t in all_tools if t['category'].lower() == target_cat]

        # 3. PAGINATION FORENSICS (Chunking)
        # Allows the UI to request "Page 1" of tools if needed.
        # Defaults to ALL if not specified (legacy behavior).
        limit = getattr(request, 'limit', None) or len(filtered_tools)
        offset = getattr(request, 'offset', 0)

        paginated_tools = filtered_tools[offset: offset + limit]

        # 4. LIGHT-MATTER PROTOCOL (Compression)
        # If 'detail' is not requested, we strip heavy fields.
        is_detailed = getattr(request, 'detail', False)

        final_payload = []
        for tool in paginated_tools:
            tool_lite = {
                "id": tool['id'],
                "name": tool['name'],
                "category": tool['category'],
                "icon": tool['icon'],
                "command": tool['command'],
                "complexity": tool['complexity'],
                "safety": tool['safety'],
                "uiComponent": tool['uiComponent'],
                # [ASCENSION 11]: Inject Shortcut
                "shortcut": self.SHORTCUT_MAP.get(tool['id']),
                # [ASCENSION 1]: Truncate Description
                "description": tool['description'][:60] + "..." if len(tool['description']) > 60 else tool[
                    'description']
            }

            if is_detailed:
                # Add heavy fields only if requested
                tool_lite["tags"] = tool['tags']
                tool_lite["search_vector"] = tool['search_vector']
                tool_lite["description"] = tool['description']  # Full description
            else:
                # Lean tags (Max 2)
                tool_lite["tags"] = tool['tags'][:2]

            final_payload.append(tool_lite)

        # 5. MERKLE PULSE (Hash)
        # Generate a hash of the result so the client knows if it's stale.
        payload_str = json.dumps(final_payload, sort_keys=True)
        merkle_hash = hashlib.md5(payload_str.encode()).hexdigest()[:8]

        return self.success(
            f"Census: {len(final_payload)} Rites.",
            data={
                "plugins": final_payload,
                "meta": {
                    "total": len(filtered_tools),
                    "count": len(final_payload),
                    "offset": offset,
                    "hash": merkle_hash,
                    "mode": "detailed" if is_detailed else "lite"
                }
            }
        )

    @lru_cache(maxsize=1)
    def _get_cached_tools(self) -> List[Dict[str, Any]]:
        """
        [THE IMMUTABLE CHRONOCACHE]
        Parses the Grimoire once and holds the truth in RAM.
        """
        tools = []
        for cmd_name, config in RITE_GRIMOIRE.items():

            # [ASCENSION 5]: COMPLEXITY DIVINATION
            flags_str = str(config.get("flags", []))
            is_interactive = (
                    "interactive" in flags_str or
                    cmd_name in ["architect", "manifest", "pad", "studio", "gui", "repl", "symphony"]
            )
            complexity = "interactive" if is_interactive else "instant"
            if "daemon" in cmd_name: complexity = "daemon"

            # [ASCENSION 6]: SAFETY RATING
            desc = config.get("help", "").lower()
            safety = "SAFE"
            if "delete" in desc or "remove" in desc or "prune" in desc or "annihilate" in desc:
                safety = "CRITICAL"
            elif "update" in desc or "modify" in desc or "write" in desc:
                safety = "CAUTIOUS"

            category = self.CATEGORY_MAP.get(cmd_name, "Utilities")
            icon = self.ICON_MAP.get(cmd_name, "Box")

            # [ASCENSION 8]: SEARCH VECTOR
            tags = [category]
            if "subparsers" in config:
                tags.append("Multi-Rite")
                tags.extend(list(config["subparsers"].keys()))

            search_vector = f"{cmd_name} {' '.join(tags)} {config.get('help', '')}".lower()

            tool = {
                "id": cmd_name,
                "name": cmd_name.replace("-", " ").title(),
                "description": config.get("help", "Gnostic capability."),
                "command": f"scaffold {cmd_name}",
                "category": category,
                "icon": icon,
                "complexity": complexity,
                "tags": tags,
                "isPlugin": False,
                "safety": safety,
                "search_vector": search_vector,
                "uiComponent": self.UI_COMPONENT_MAP.get(cmd_name)
            }
            tools.append(tool)

        # Sort by Category then Name
        tools.sort(key=lambda x: (x['category'], x['name']))
        return tools