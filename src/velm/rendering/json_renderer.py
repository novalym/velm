# Path: scaffold/rendering/json_renderer.py

"""
=================================================================================
== THE UNIVERSAL SCRIBE OF GNOSTIC TRUTH (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)       ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000

This divine artisan speaks the one true, universal language of machines: JSON. It
has been transfigured from a simple scribe into the God-Engine of Gnostic Synthesis.
It gazes upon the complete, Gnostically-enriched tree and proclaims not just its
form, but its entire soul as a pure, structured, and self-aware Gnostic Dossier.

Its scripture is the unbreakable contract for all future tools that would seek to
commune with the Scaffold cosmos.
=================================================================================
"""
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

from .base_renderer import GnosticTreeRenderer, _GnosticNode
from .. import __version__ as scaffold_version
from ..constants import SECRET_FILENAMES
from ..contracts.data_contracts import ScaffoldItem


class JSONRenderer(GnosticTreeRenderer):
    """Proclaims a Gnostic Tree as a pure, machine-readable, and complete JSON Dossier."""

    def __init__(self, items: List[ScaffoldItem], pretty: bool = True):
        """
        =================================================================================
        == THE RITE OF PURE INCEPTION                                                  ==
        =================================================================================
        The Scribe is born. It is bestowed with the Architect's will for aesthetic
        purity (`pretty`) and immediately conducts the Gnostic Inquisition to forge
        its understanding of the reality it must proclaim.
        =================================================================================
        """
        self.pretty = pretty
        self._node_id_counter = 0  # The ephemeral soul for forging unique IDs.
        super().__init__(items)

    def render(self) -> str:
        """
        The one true Rite of Proclamation. It conducts a recursive symphony to
        transmute the Gnostic Node tree into a pure Python dictionary, wraps it in a
        divine Dossier of Provenance, and proclaims it as a JSON scripture.
        """
        # --- The Forging of the Vessels ---
        transmuted_tree: List[Dict[str, Any]] = []
        errors: List[str] = []
        file_count = 0
        dir_count = 0

        # --- The Symphony of Synthesis ---
        # We start the recursive transmutation from the children of the root.
        if self.root.children:
            for child in sorted(self.root.children, key=lambda n: (0 if n.is_dir else 1, n.name.lower())):
                try:
                    child_dict, stats = self._transmute_node_to_dict(child)
                    transmuted_tree.append(child_dict)
                    file_count += stats['files']
                    dir_count += stats['dirs']
                except Exception as e:
                    errors.append(f"A paradox occurred while transmuting node '{child.name}': {str(e)}")

        # --- The Forging of the Gnostic Dossier ---
        dossier = {
            "provenance": {
                "scribe": "Scaffold Gnostic JSONRenderer",
                "version": scaffold_version,
                "timestamp_utc": datetime.now(timezone.utc).isoformat()
            },
            "telemetry": {
                "total_nodes": file_count + dir_count,
                "file_count": file_count,
                "directory_count": dir_count,
            },
            "architectural_tree": transmuted_tree
        }
        if errors:
            dossier["errors"] = errors

        # --- The Final Proclamation ---
        indent = 2 if self.pretty else None
        return json.dumps(dossier, indent=indent)

    def _transmute_node_to_dict(self, node: _GnosticNode) -> Tuple[Dict[str, Any], Dict[str, int]]:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC SYNTHESIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)       ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000

        This artisan has been ascended to become the **Universal Herald of Deep Gnosis**.
        It gazes upon the `_GnosticNode`'s now-complete soul and proclaims every
        facet of the Gnostic Inquisition's findings—from Git Forensics to AST
        Analysis—into a pure, structured, and luminous JSON scripture. Its
        proclamation is the one true, machine-readable soul of the project.
        =================================================================================
        """
        self._node_id_counter += 1
        node_id = f"gnostic-node-{self._node_id_counter}"

        file_count = 1 if not node.is_dir else 0
        dir_count = 1 if node.is_dir else 0

        node_dict = {
            "id": node_id,
            "name": node.name,
            "type": "directory" if node.is_dir else "file",
        }

        if node.item:
            item = node.item

            item_gnosis = {
                "path": item.path.as_posix(),
                "permissions": item.permissions,
            }

            # --- Proclamation of the Soul's Origin (Unchanged and Pure) ---
            source_gnosis = {"type": "forge"}
            if item.seed_path:
                source_gnosis = {"type": "seed", "path": item.seed_path.as_posix()}
            elif item.content is not None:
                source_gnosis = {"type": "inline", "content_hash": item.content_hash}
            elif item.name in SECRET_FILENAMES:
                source_gnosis = {"type": "secret"}
            elif item.content_hash is None and item.last_modified is None:
                source_gnosis = {"type": "binary"}
            item_gnosis["source"] = source_gnosis

            # =================================================================================
            # ==         BEGIN SACRED TRANSMUTATION: THE PROCLAMATION OF DEEP GNOSIS         ==
            # =================================================================================
            # The Scribe now gazes upon every vessel of the ascended _GnosticNode and
            # proclaims all Gnosis that is manifest.
            inquisitor_gnosis = {}
            if node.complexity:
                inquisitor_gnosis['complexity'] = node.complexity
            if node.git_info:
                inquisitor_gnosis['git_info'] = node.git_info
            if node.dependency_gnosis:
                inquisitor_gnosis['dependencies'] = node.dependency_gnosis
            if node.git_forensics:
                inquisitor_gnosis['git_forensics'] = node.git_forensics
            if node.ast_gnosis:
                inquisitor_gnosis['ast_analysis'] = node.ast_gnosis
            if node.treesitter_gnosis:
                inquisitor_gnosis['treesitter_analysis'] = node.treesitter_gnosis
            if node.sentinel_gnosis:
                inquisitor_gnosis['sentinel_analysis'] = node.sentinel_gnosis

            if inquisitor_gnosis:
                item_gnosis['inquisitor_gnosis'] = inquisitor_gnosis
            # =================================================================================
            # ==                          THE APOTHEOSIS IS COMPLETE                         ==
            # =================================================================================

            node_dict["architectural_gnosis"] = item_gnosis

        if node.children:
            children_list = []
            for child in sorted(node.children, key=lambda n: (0 if n.is_dir else 1, n.name.lower())):
                child_dict, stats = self._transmute_node_to_dict(child)
                children_list.append(child_dict)
                file_count += stats['files']
                dir_count += stats['dirs']
            node_dict['children'] = children_list

        stats = {'files': file_count, 'dirs': dir_count}
        return node_dict, stats