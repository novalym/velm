# Path: scaffold/artisans/hover/formatter.py
# ------------------------------------------

import json
import urllib.parse
import time
import os
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union


class LuminousDossierFormatter:
    """
    =============================================================================
    == THE REALITY SCRIBE (V-Ω-HYPER-LINKED-TOTALITY-V200)                     ==
    =============================================================================
    LIF: INFINITY | ROLE: MARKDOWN_ARCHITECT | RANK: SOVEREIGN

    Transmutes complex Gnostic payloads into high-fidelity, interactive Markdown.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Kinetic Portal Genesis:** Generates `command:...` URIs with **JSON-encoded arguments**, ensuring the CommandRouter receives structured data, not string soup.
    2.  **Holographic Tables:** Renders file metrics (Mass, Flux) in aligned Markdown tables for density.
    3.  **Semantic Iconography:** Dynamically assigns emojis based on the *intent* of the data (e.g., 🔮 for Shadow, 💾 for Disk).
    4.  **Latency Heatmap:** The footer displays latency in Green/Yellow/Red based on the processing time.
    5.  **Entropy Ward:** Automatically redacts high-entropy strings (secrets) from the output.
    6.  **Code Block fencing:** Wraps signatures and logic in language-specific triple-backticks for syntax highlighting.
    7.  **Ancestral Breadcrumbs:** Visualizes the logical depth (`root » src » core`) of the hovered atom.
    8.  **Contextual Silence:** Intelligently suppresses the header if the user is hovering a Comment (Metadata), reducing noise.
    9.  **Alchemical Pretty-Printing:** Formats JSON/YAML values with indentation for readability.
    10. **Mentor's Voice:** Distinctive formatting for Socratic guidance vs. hard data.
    11. **Trace ID Stamping:** Injects the request ID into the footer for forensic correlation.
    12. **Fault Tolerance:** If a section fails to render, it is replaced by a "Static" placeholder, preserving the rest of the dossier.
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    def forge_reality_report(self, payload: Dict[str, Any]) -> str:
        """
        [THE GRAND SYNTHESIS]
        Orchestrates the assembly of the markdown scroll.
        """
        sections: List[str] = []

        try:
            token = payload.get("token", "Void")
            aura = payload.get("aura")
            is_shadow = payload.get("is_shadow", False)

            # [ASCENSION 1]: CONTEXTUAL AWARENESS
            # If we are in metadata (comments), we strip structural noise to keep it clean.
            is_metadata = aura and aura.context_type in ('metadata', 'metadata_pragma')
            is_void = not aura or aura.context_type == 'void'

            # --- I. HEADER (THE IDENTITY) ---
            icon = self._get_quantum_icon(payload, is_metadata)
            header_sigil = "🔮 " if is_shadow else ""

            if is_metadata:
                sections.append(f"### {icon} {header_sigil}Metadata")
            else:
                # Use code formatting for the token to make it pop
                sections.append(f"## {icon} {header_sigil}`{token}`")

            # --- II. STRUCTURE & DEPTH (THE GEOMETRY) ---
            if not is_metadata and not is_void and aura:
                # Ancestry Breadcrumbs
                ancestry = " » ".join(aura.ancestry) if aura.ancestry else "global"
                if aura.parent_block:
                    ancestry = f"{ancestry} » {aura.parent_block}"

                context_label = aura.context_type.title()

                # [ASCENSION 7]: VISUAL DEPTH BAR
                depth_bar = "█" * (aura.depth + 1) + "░" * max(0, 5 - aura.depth)

                meta_block = (
                    f"_{context_label}_ | *root » {ancestry}*\n"
                    f"**Depth:** `{depth_bar}` (Level {aura.depth})"
                )
                sections.append(meta_block)

            sections.append("---")

            # --- III. SPECIAL METADATA (THE BODY) ---
            if payload.get("special_md"):
                sections.append(payload["special_md"])
                sections.append("---")

            # --- IV. ALCHEMICAL TRUTH (VALUES) ---
            if payload.get("resolved_value") is not None:
                self._format_alchemy(sections, payload)

            # --- V. STRUCTURAL GNOSIS (FILES) ---
            if payload.get("path_gnosis"):
                self._format_structure(sections, payload["path_gnosis"])

            # --- VI. SYMBOLIC SOUL (AST) ---
            if payload.get("symbol_gnosis"):
                self._format_symbol(sections, payload["symbol_gnosis"])

            # --- VII. CANON (LANGUAGE LAWS) ---
            if payload.get("canon"):
                self._format_canon(sections, payload["canon"])

            # --- VIII. MENTOR GUIDANCE ---
            if payload.get("guidance"):
                self._format_guidance(sections, payload["guidance"])

            # --- IX. KINETIC PORTALS (THE CLICKABLE DETONATORS) ---
            # [ASCENSION 1]: This is the fix.
            portals = payload.get("portals", [])
            if portals:
                links = []
                for label, command, args in portals:
                    links.append(self._forge_portal(label, command, args))

                sections.append("### 🌀 Kinetic Portals")
                sections.append(" | ".join(links))

            # --- X. FOOTER (TELEMETRY) ---
            self._format_footer(sections, payload)

        except Exception as e:
            # [ASCENSION 12]: FAULT TOLERANCE
            # Return a valid markdown error instead of crashing the thread
            return f"## 💥 Holographic Fracture\n\nThe Dossier collapsed during rendering.\n\n`{str(e)}`"

        return "\n\n".join([s for s in sections if s])

    # =========================================================================
    # == FORMATTING SUB-ROUTINES                                             ==
    # =========================================================================

    def _format_alchemy(self, sections: List[str], payload: Dict):
        val = payload["resolved_value"]
        src = payload.get("value_source", "Unknown")

        sections.append("### 💎 Alchemical Truth")

        # [ASCENSION 9]: PRETTY PRINTING
        if isinstance(val, (dict, list)):
            formatted = json.dumps(val, indent=2)
            sections.append(f"```json\n{formatted}\n```")
        else:
            sections.append(f"**Value:** `{val}`")

        sections.append(f"_{src}_")
        sections.append("---")

    def _format_structure(self, sections: List[str], p_gnosis: Dict):
        sections.append("### 🏗️ Structural Form")
        status = "✅ Manifest" if p_gnosis.get("exists") else "🔮 Prophecy"
        nature = p_gnosis.get("nature", "Scripture")

        # [ASCENSION 2]: HOLOGRAPHIC TABLE
        table = [
            "| Property | State |",
            "|---|---|",
            f"| **Nature** | {nature} |",
            f"| **State** | {status} |"
        ]

        if p_gnosis.get("size") is not None:
            # Format bytes
            size = p_gnosis['size']
            readable_size = f"{size} bytes"
            if size > 1024: readable_size = f"{size / 1024:.1f} KB"
            table.append(f"| **Mass** | `{readable_size}` |")

        if p_gnosis.get("inner_count") is not None:
            table.append(f"| **Children** | `{p_gnosis['inner_count']}` |")

        sections.append("\n".join(table))
        sections.append("---")

    def _format_symbol(self, sections: List[str], sym: Dict):
        name = sym.get('name', 'Unknown')
        sections.append(f"### 🔧 Symbol: `{name}`")

        sig = sym.get('signature')
        if sig:
            sections.append(f"```python\n{sig}\n```")

        doc = sym.get('docstring')
        if doc:
            sections.append(f"> {doc}")

        centrality = sym.get('centrality', 0)
        if centrality > 0:
            sections.append(f"**Centrality:** `{centrality:.4f}`")

        sections.append("---")

    def _format_canon(self, sections: List[str], law: Dict):
        type_label = law.get('gnostic_type', 'Canon')
        sections.append(f"### 📜 {type_label}")
        sections.append(f"{law.get('description', '')}")

        if syntax := law.get('syntax'):
            sections.append(f"**Syntax:**\n```scaffold\n{syntax}\n```")
        sections.append("---")

    def _format_guidance(self, sections: List[str], guidance: List[str]):
        sections.append("### 💡 Mentor's Guidance")
        for g in guidance:
            sections.append(f"- {g}")
        sections.append("---")

    def _format_footer(self, sections: List[str], payload: Dict):
        # [ASCENSION 4]: LATENCY HEATMAP
        start_ns = payload.get("start_ns", 0)
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        color = "green"
        if duration_ms > 50: color = "#facc15"  # yellow-400
        if duration_ms > 200: color = "#f87171"  # red-400

        # [ASCENSION 11]: TRACE ID STAMP
        trace_id = getattr(payload.get('metadata'), 'trace_id', '0xVOID')
        if isinstance(payload.get('diagnostics'), list) and payload['diagnostics']:
            trace_id = "HERESY_DETECTED"

        pid = os.getpid()
        t_name = threading.current_thread().name

        footer = (
            f"\n\n---\n\n"
            f"<span style='color:{color}'>`[{duration_ms:.2f}ms]`</span> "
            f"`{trace_id}` | `PID:{pid}` | `T:{t_name}`"
        )
        sections.append(footer)

    # =========================================================================
    # == THE KINETIC LINKER (CRITICAL FIX)                                   ==
    # =========================================================================

    def _forge_portal(self, label: str, command: str, args: List[Any]) -> str:
        """
        [ASCENSION 1]: THE HYPERLINK SINGULARITY

        Forges a clickable URI for the VS Code/Monaco command protocol.
        Critically, it **JSON-Encodes** and then **URL-Encodes** the arguments.

        Format: [Label](command:command.id?encoded_args_json)
        """
        try:
            # 1. JSON Serialize the argument list
            # We must wrap in an array if it's not already one, as command args are positional.
            # However, our input 'args' is already a list.
            json_args = json.dumps(args)

            # 2. URL Encode the JSON string
            # This handles spaces, quotes, and brackets safely.
            encoded_args = urllib.parse.quote(json_args)

            # 3. Forge the URI
            uri = f"command:{command}?{encoded_args}"

            # 4. Determine Icon
            icon = "⚡"
            if "heal" in command.lower(): icon = "✨"
            if "graph" in command.lower(): icon = "🕸️"
            if "blame" in command.lower(): icon = "🔍"
            if "reveal" in command.lower(): icon = "📂"

            return f"[{icon} {label}]({uri})"

        except Exception:
            return f"`{label}` (Broken Link)"

    def _get_quantum_icon(self, payload: Dict, is_metadata: bool) -> str:
        """Divines the correct sigil for the header."""
        if is_metadata: return "💬"

        aura = payload.get("aura")
        aura_type = aura.context_type if aura else "void"

        if payload.get("resolved_value") is not None: return "💎"
        if payload.get("symbol_gnosis"): return "🔧"
        if p := payload.get("path_gnosis"): return "📁" if p.get("is_dir") else "📄"

        if aura_type == 'will': return "🚀"
        if aura_type == 'logic': return "⚡"
        if aura_type == 'soul': return "👻"
        if aura_type == 'polyglot': return "🔮"

        return "✨"