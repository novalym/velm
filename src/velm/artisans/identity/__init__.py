# Path: src/velm/artisans/identity/__init__.py
# --------------------------------------------
"""
=================================================================================
== THE IDENTITY SANCTUM (V-Ω-GLOBAL-AUTH)                                      ==
=================================================================================
LIF: ∞ | ROLE: AUTHENTICATION_GATEWAY | RANK: OMEGA

The sovereign domain for managing Global Identity and Cloud Handshakes.
It exists outside the scope of a specific project, anchoring directly to the
Architect's session or machine.
"""
from .artisan import IdentityArtisan
# Note: IdentityRequest is imported from interfaces/requests.py

__all__ = ["IdentityArtisan"]