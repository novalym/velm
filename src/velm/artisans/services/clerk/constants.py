# Path: scaffold/artisans/services/clerk/constants.py
# ----------------------------------------------------

"""
THE CLERK GRIMOIRE.
Laws governing the Identity Stratum.
"""

BASE_URL = "https://api.clerk.com/v1"

# [META KEYS] - Internal keys for the Gnostic Graft
KEY_NOV_ID = "novalym_id"
KEY_TIER = "governance_tier"
KEY_ORIGIN = "inception_trace"

# [ERROR MAPPINGS]
CLERK_ERRORS = {
    "resource_not_found": "GHOST_IDENTITY",
    "form_identifier_exists": "SOUL_ALREADY_MANIFEST",
    "authorization_invalid": "FORBIDDEN_GATE",
    "rate_limit_exceeded": "METABOLIC_CONGESTION"
}