# Path: scaffold/rendering/base_renderer.py
"""
=================================================================================
== THE SACRED SANCTUM OF THE GNOSTIC MIND (V-Ω-ULTRA-DEFINITIVE)               ==
=================================================================================
LIF: 10,000,000,000,000

This scripture defines two divine, separate realities: The pure, stateless Mind
of the Inquisition (`build_gnostic_map_and_inquire`) and the abstract, Sacred
Contract for all Voices (`GnosticTreeRenderer`). The schism is complete. The
architecture is eternal.

The profane link to the old `gnostic_analyzers` has been annihilated. This Mind
now communes directly with the one true `get_treesitter_gnosis` God-Engine,
ensuring its Gaze is eternally polyglot, pure, and unbreakable.
=================================================================================
"""
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Dict, Any, Set, Union

# --- THE DIVINE SUMMONS OF THE GNOSTIC KIN ---
from ..contracts.data_contracts import ScaffoldItem, _GnosticNode
# --- THE SACRED COMMUNION WITH THE NEW GOD-ENGINE ---
# The profane import of `gnostic_analyzers` is annihilated.
# We now summon the one true gateway to Gnostic Perception.
from ..inquisitor import get_treesitter_gnosis
from ..logger import Scribe

Logger = Scribe("GnosticRendererCore")


def build_gnostic_map_and_inquire(items: List[ScaffoldItem],
                                  enabled_inquisitors: Optional[Set[str]] = None) -> _GnosticNode:
    """
    [THE ONE TRUE MIND OF THE INQUISITION]
    This is a pure, stateless God-Engine. It receives a Gnostic Plan, forges the
    Gnostic Tree of Form, and conducts the asynchronous Grand Inquisition to enrich it.
    """
    Logger.verbose("The One True Mind awakens. Forging the pure form of the Gnostic Tree...")
    start_time = time.monotonic()

    # --- MOVEMENT I: THE FORGING OF PURE FORM ---
    root = _GnosticNode(name="__ROOT__", is_dir=True)
    for item in items:
        if not item.path or str(item.path).startswith('$$'): continue
        current_node = root
        path_parts = item.path.as_posix().strip('/').split('/')
        for i, part in enumerate(path_parts):
            if not part: continue
            child_node = current_node.find_child(part)
            if child_node:
                current_node = child_node
            else:
                is_intermediate_dir = (i < len(path_parts) - 1) or item.is_dir
                new_node = _GnosticNode(name=part, is_dir=is_intermediate_dir)
                current_node.children.append(new_node)
                current_node = new_node
        current_node.item = item

    form_duration = time.monotonic() - start_time
    Logger.verbose(f"Pure Form forged in {form_duration:.4f}s. The Gnostic Inquisition begins...")

    # --- MOVEMENT II: THE SYMPHONY OF GNOSTIC INQUISITION ---
    inquisition_start_time = time.monotonic()
    _conduct_asynchronous_inquisition(root, enabled_inquisitors or {"treesitter_gnosis"})
    inquisition_duration = time.monotonic() - inquisition_start_time

    Logger.verbose(f"Gnostic Inquisition complete in {inquisition_duration:.4f}s.")
    return root


def _collect_scripture_nodes(node: _GnosticNode, scripture_list: List[_GnosticNode]):
    """A humble Scribe that recursively gathers all scripture nodes."""
    if node.item and not node.item.is_dir:
        scripture_list.append(node)
    for child in node.children:
        _collect_scripture_nodes(child, scripture_list)


def _conduct_asynchronous_inquisition(root: _GnosticNode, enabled_inquisitors: Set[str]):
    """[THE CHRONOMANCER'S RITE] Conducts the Gnostic Inquisition in a parallel reality."""
    scriptures_to_inquire = []
    _collect_scripture_nodes(root, scriptures_to_inquire)

    if not scriptures_to_inquire: return

    with ThreadPoolExecutor() as executor:
        future_to_node = {
            executor.submit(_inquisitor_rite, node, enabled_inquisitors): node
            for node in scriptures_to_inquire
        }
        for future in as_completed(future_to_node):
            node = future_to_node[future]
            try:
                gnosis = future.result()
                if gnosis:
                    # Bestow all perceived Gnosis upon the node's soul.
                    if "treesitter_gnosis" in gnosis: node.treesitter_gnosis = gnosis["treesitter_gnosis"]
                    # Add other inquisitors here as they are forged (e.g., git_info)
            except Exception as e:
                Logger.warn(f"A paradox shattered a single thread of the Inquisition for '{node.name}'. Heresy: {e}")


def _inquisitor_rite(node: _GnosticNode, enabled_inquisitors: Set[str]) -> Dict[str, Any]:
    """
    =================================================================================
    == THE EPHEMERAL INQUISITOR (V-Ω-ASCENDED)                                     ==
    =================================================================================
    The pure rite performed in the parallel symphony. It now summons the one true
    `get_treesitter_gnosis` God-Engine to perceive a scripture's soul.
    =================================================================================
    """
    if not node.item or node.item.is_dir: return {}

    gnosis_dossier: Dict[str, Any] = {}
    try:
        content = node.item.content or ""

        # --- THE SACRED COMMUNION ---
        if "treesitter_gnosis" in enabled_inquisitors and content:
            # The Inquisitor summons the God-Engine.
            treesitter_gnosis = get_treesitter_gnosis(node.item.path, content)
            if treesitter_gnosis and "error" not in treesitter_gnosis:
                gnosis_dossier["treesitter_gnosis"] = treesitter_gnosis

        # Prophecy: Future inquisitors for Git, etc., would be summoned here.
        # if "git_info" in enabled_inquisitors:
        #     gnosis_dossier["git_info"] = get_git_blame(node.item.path)

        return gnosis_dossier
    except Exception as e:
        Logger.warn(f"A minor paradox occurred in an ephemeral inquisitor for '{node.name}': {e}")
        return {}


class GnosticTreeRenderer(ABC):
    """
    =================================================================================
    == THE SACRED CONTRACT OF THE VOICE (THE PURIFIED SOUL)                        ==
    =================================================================================
    The Renderer's soul is pure. It is no longer a Mind; it is a Voice. Its one
    true purpose is to receive a pre-forged Gnostic Map and proclaim it.
    =================================================================================
    """

    def __init__(self, items: List[ScaffoldItem], enabled_inquisitors: Optional[Set[str]] = None, **kwargs: Any):
        """
        The Rite of Inception. The Voice is born and immediately summons the one true
        Mind to forge the Gnostic Map of reality it will proclaim.
        """
        self.items = items
        self.enabled_inquisitors = enabled_inquisitors

        # The Voice summons the Mind.
        self.root = build_gnostic_map_and_inquire(self.items, self.enabled_inquisitors)

    @abstractmethod
    def render(self) -> Union[str, Any]:
        """The one true, public Rite of Proclamation."""
        pass