# Path: scaffold/artisans/simulacrum/exceptions.py
from ...contracts.heresy_contracts import ArtisanHeresy


class VoidCollapseError(ArtisanHeresy):
    """The simulation failed to sustain itself."""
    pass


class SpectralLinkError(ArtisanHeresy):
    """Could not bridge dependencies from Reality to Void."""
    pass


class ContainmentBreach(ArtisanHeresy):
    """The simulation attempted to violate security protocols."""
    pass

