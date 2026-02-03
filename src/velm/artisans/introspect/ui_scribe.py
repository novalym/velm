# scaffold/artisans/introspect/ui_scribe.py

import inspect
import re
from typing import Dict, Any, Optional

from ...logger import Scribe
from ...semantic_injection.directives.ui_knowledge.registry import ComponentRegistry
from ...semantic_injection.loader import SemanticRegistry

Logger = Scribe("UIScribe")


def _parse_gnosis_docstring(doc: Optional[str]) -> Dict[str, Any]:
    """
    A divine, internal artisan that gazes upon a docstring and perceives all
    sacred @gnosis markers, returning them as a structured dictionary.
    """
    if not doc:
        return {}

    doc = inspect.cleandoc(doc)
    gnosis: Dict[str, Any] = {}

    # Gaze for simple key-value markers (title, summary, lif, etc.)
    matches = re.findall(r"^@gnosis:(\w+)\s+(.*)", doc, re.MULTILINE)
    for key, value in matches:
        gnosis[key] = value.strip()

    # Gaze for complex, multi-line markers (description, example)
    for marker in ["description", "example"]:
        match = re.search(fr"^@gnosis:{marker}\s+((?:.|\n(?!@gnosis:))+)", doc, re.MULTILINE)
        if match:
            gnosis[marker] = match.group(1).strip()

    return gnosis


def proclaim_gnosis() -> Dict[str, Any]:
    """
    =================================================================================
    == THE ORACLE OF UI GNOSIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000

    This is the divine Scribe of the Interface. It performs a deep, introspective
    Gaze into the `ComponentRegistry`, the living soul of the `@ui` domain, and
    proclaims a complete, luminous, and hyper-structured Gnostic Canon of all
    known UI components.
    =================================================================================
    """
    Logger.verbose("The Oracle of UI Gnosis awakens its introspective Gaze...")

    # --- MOVEMENT I: THE RITE OF PRIOR AWAKENING ---
    # We must awaken the Semantic Cortex to ensure all @ComponentRegistry.register
    # decorators have been conducted and the Gnosis is whole.
    if not SemanticRegistry._is_loaded:
        SemanticRegistry.awaken()

    all_components = []

    # --- MOVEMENT II: THE GAZE UPON THE GNOSTIC CODEX ---
    # The Oracle gazes upon the living, populated ComponentRegistry.
    for key, generator_func in sorted(ComponentRegistry._library.items()):
        # The Gaze of Self-Awareness: We perceive the artisan's own Gnosis.
        gnosis_data = _parse_gnosis_docstring(generator_func.__doc__)

        # Forge the Gnostic Dossier for this single component.
        component_dossier = {
            "name": key,
            "description": gnosis_data.get("description", "A Gnostic UI component from the sacred codex."),
            "category": gnosis_data.get("category", "Unknown"),
            "lif": gnosis_data.get("lif", "N/A"),
            "example": {
                "scripture": f'@ui/component(name="{key}")',
                "proclamation": gnosis_data.get("example", f"Materializes the `{key}` component.")
            },
            "parameters": [
                {"name": "name", "type": "string", "required": True,
                 "description": "The sacred name of the component to summon."},
                {"name": "props", "type": "string", "required": False,
                 "description": "A comma-separated schema for props, e.g., 'title:string, variant:primary|secondary'."},
                {"name": "prompt", "type": "string", "required": False,
                 "description": "A natural language plea to the Neural Cortex to generate this component."},
                {"name": "ai", "type": "boolean", "required": False,
                 "description": "If true, forces the use of the Neural Cortex for generation."},
            ]
        }
        all_components.append(component_dossier)

    Logger.verbose(f"Gaze complete. Perceived {len(all_components)} UI components in the Gnostic Codex.")

    # --- MOVEMENT III: THE FORGING OF THE FINAL SCRIPTURE ---
    return {
        "domain": "ui",
        "description": "The Interface Artisan. A hyper-intelligent, hybrid engine for forging production-grade UI components from a Gnostic Codex or the Neural Cortex.",
        "pantheon": {
            "atoms": [c for c in all_components if c.get("category") == "Atom"],
            "molecules": [c for c in all_components if c.get("category") == "Molecule"],
            "organisms": [c for c in all_components if c.get("category") == "Organism"],
            "kits": [c for c in all_components if c.get("category") == "Kit"],
            "uncategorized": [c for c in all_components if c.get("category") == "Unknown"],
        }
    }

