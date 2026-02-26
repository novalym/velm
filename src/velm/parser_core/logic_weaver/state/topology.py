# Path: parser_core/logic_weaver/state/topology.py
# ------------------------------------------------

from pathlib import Path
from typing import TYPE_CHECKING, List, Optional
from ....utils import find_project_root
from ....logger import Scribe

if TYPE_CHECKING:
    from .engine import GnosticContext

Logger = Scribe("GeometricAnchor")


class GeometricAnchor:
    """
    =============================================================================
    == THE GEOMETRIC ANCHOR (V-Ω-SPATIAL-WARDEN)                               ==
    =============================================================================
    Governs the spatial reality of the Context. It defines the absolute origin
    point of the Universe (Project Root) and tracks ephemeral matter created
    during simulation.
    """

    __slots__ = ('ctx',)

    def __init__(self, ctx: 'GnosticContext'):
        self.ctx = ctx

    def establish_root(self):
        """
        [ASCENSION 6 & 10]: ABSOLUTE GEOMETRIC ANCHORING.
        Calculates the one true Project Root, inheriting from the Ancestor
        or divining it from the physical disk.
        """
        if 'project_root' not in self.ctx._context:
            if self.ctx.parent:
                self.ctx._context['project_root'] = self.ctx.parent.project_root
            else:
                found_root, _ = find_project_root(Path.cwd())
                self.ctx._context['project_root'] = found_root or Path.cwd()

        # Enforce Path Integrity
        if isinstance(self.ctx._context['project_root'], str):
            self.ctx._context['project_root'] = Path(self.ctx._context['project_root'])

    def establish_manifest(self):
        """Links the virtual filesystem manifest across the multiverse."""
        if 'generated_manifest' not in self.ctx._context:
            if self.ctx.parent:
                # Share the manifest reference with the parent (Shared Pointer)
                self.ctx._context['generated_manifest'] = self.ctx.parent.raw.get('generated_manifest', [])
            else:
                self.ctx._context['generated_manifest'] = []

    def register_virtual_file(self, path: Path):
        """
        [ASCENSION 10]: THE VOID PATH EXORCIST.
        Inscribes a path into the shared Virtual Reality manifest, guaranteeing
        POSIX forward-slash normalization instantly.
        """
        clean_path = str(path).replace('\\', '/')
        manifest: List[str] = self.ctx._context['generated_manifest']

        if clean_path not in manifest:
            manifest.append(clean_path)
            if self.ctx.depth == 0:
                Logger.verbose(f"Lattice: Inscribed virtual atom: [dim]{clean_path}[/dim]")