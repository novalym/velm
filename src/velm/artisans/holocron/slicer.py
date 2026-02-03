# Path: artisans/holocron/slicer.py
# ---------------------------------

from pathlib import Path
import re
from typing import Dict, List, Set, Optional, Any

# --- THE DIVINE SUMMONS OF THE INQUISITOR'S SOUL ---
# The Slicer now possesses its own, direct Gaze.
from ...inquisitor import get_treesitter_gnosis
from ...logger import Scribe

Logger = Scribe("SurgicalSlicer")


class SurgicalSlicer:
    """
    =============================================================================
    == THE GNOSTIC SURGEON (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-SOVEREIGN)             ==
    =============================================================================
    @gnosis:title The Gnostic Surgeon (`SurgicalSlicer`)
    @gnosis:summary A divine, intent-aware artisan that performs surgical code
                     extraction with either skeletal or full-body fidelity.
    @gnosis:LIF INFINITY
    @gnosis:auth_code:)(#@()@#()!

    This is the final, eternal form of the Surgical Slicer. It is a true Gnostic
    Surgeon, its profane bond to the Skeletonizer annihilated. It now wields its
    own Gaze via the Tree-sitter Inquisitor, allowing it to perform a full
    soul-transplant (full fidelity) or a delicate extraction (skeletal) with
    byte-perfect precision. It is the indispensable hand of the Holocron
    Forensic Engine.
    """

    def __init__(self, root: Path, keywords: List[str]):
        self.root = root
        self.keywords = set(k.lower() for k in keywords)

    def slice(self, file_paths: List[str], fidelity: str = 'full') -> Dict[str, str]:
        """
        The Grand Rite of Surgical Slicing.

        Args:
            file_paths: A list of project-relative paths to slice.
            fidelity: The desired level of detail ('skeleton' or 'full').

        Returns:
            A dictionary mapping file paths to their sliced content.
        """
        results: Dict[str, str] = {}
        Logger.verbose(f"Surgical Gaze initiated with '{fidelity}' fidelity on {len(file_paths)} scriptures.")

        for path_str in file_paths:
            results[path_str] = self._slice_single_file(path_str, fidelity)

        return results

    def _slice_single_file(self, path_str: str, fidelity: str) -> str:
        """Performs the surgical operation on a single file."""
        path = self.root / path_str
        if not path.is_file():
            Logger.warn(f"Slicer's Gaze averted: The scripture '{path_str}' is a void.")
            return f"// Heresy: Scripture '{path_str}' is a void."

        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()

            # --- THE GAZE OF THE INQUISITOR ---
            dossier = get_treesitter_gnosis(path, content)
            if "error" in dossier:
                return f"// Gnostic Syntax Heresy: Could not parse '{path_str}'.\n{content}"

            output_fragments = []
            all_nodes = dossier.get("functions", []) + dossier.get("classes", [])
            all_nodes.sort(key=lambda n: n.get("start_point", [0, 0])[0])

            # --- THE RITE OF SURGICAL SELECTION ---
            for node in all_nodes:
                node_name = node.get("name", "").lower()

                # A symbol is relevant if its name contains any of the intent keywords.
                is_relevant = any(keyword in node_name for keyword in self.keywords)

                start_line_idx, end_line_idx = node['start_point'][0], node['end_point'][0]

                # Forge the Gnostic Anchor
                anchor = f"<!-- GNOSTIC_ANCHOR: {path_str}::{node.get('name')} -->"
                output_fragments.append(anchor)

                if is_relevant and fidelity == 'full':
                    # [FACULTY 1] Full Body Preservation
                    # Extract the entire, untransmuted soul of the node.
                    node_content = self._extract_node_content(content, node)
                    output_fragments.append(node_content)
                else:
                    # [FIDELITY 'skeleton'] Skeletal Extraction
                    # Extract only the signature.
                    # Heuristic: Find the line with ':' or '{'.
                    signature_end_line = start_line_idx
                    for i in range(start_line_idx, min(end_line_idx + 1, len(lines))):
                        if lines[i].strip().endswith((':', '{')):
                            signature_end_line = i
                            break

                    signature = "\n".join(lines[start_line_idx: signature_end_line + 1])
                    indentation = " " * (len(lines[start_line_idx]) - len(lines[start_line_idx].lstrip()))

                    output_fragments.append(signature)
                    output_fragments.append(f"{indentation}    ...")  # Add ellipsis to signify stub

            # --- THE FINAL SCRIPTURE FORGING ---
            # We add a header to proclaim the nature of this scripture.
            header = f"// == GNOSTIC SLICE: {path.name} | Fidelity: {fidelity.upper()} =="
            return f"{header}\n\n" + "\n\n".join(output_fragments)

        except Exception as e:
            # [FACULTY 10] The Unbreakable Gaze
            Logger.error(f"A paradox shattered the slicer's hand for '{path_str}': {e}")
            return f"// A Gnostic paradox occurred during slicing: {e}"

    def _extract_node_content(self, full_content: str, node: Dict[str, Any]) -> str:
        """Extracts the raw source code for a node using its byte offsets."""
        start_byte = node.get("start_byte")
        end_byte = node.get("end_byte")

        if start_byte is not None and end_byte is not None:
            # Encode the full content to utf-8 to work with bytes, then slice.
            return full_content.encode('utf-8')[start_byte:end_byte].decode('utf-8', 'ignore')

        # Fallback to line numbers if byte offsets are missing
        lines = full_content.splitlines()
        start_line = node.get("start_point", [0, 0])[0]
        end_line = node.get("end_point", [0, 0])[0] + 1
        return "\n".join(lines[start_line:end_line])