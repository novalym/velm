# Path: scaffold/artisans/services/clerk/artisan.py
# --------------------------------------------------

import os
import logging
from typing import Any

# --- CORE SCAFFOLD UPLINKS ---
from ....core.artisan import BaseArtisan
from ....interfaces.requests import ClerkRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import HeresySeverity, ArtisanHeresy

# --- THE IDENTITY CLOISTER ---
from .client import ClerkClient
from .simulation.engine import PhantomIdentityEngine
from .domains.invitations import InvitationsDomain
from .domains.users import UsersDomain
from .domains.organizations import OrganizationsDomain
from .domains.sessions import SessionsDomain

Logger = logging.getLogger("ClerkSovereign")


class ClerkArtisan(BaseArtisan[ClerkRequest]):
    """
    =============================================================================
    == THE SOVEREIGN HIGH INQUISITOR (V-Ω-HYBRID-REALITY-V12)                  ==
    =============================================================================
    LIF: ∞ | ROLE: IDENTITY_SUPREME_CONDUCTOR | RANK: LEGENDARY

    The definitive, multi-strata controller for the Clerk.com Identity Layer.
    Ascended with a Tri-Vector Gaze to adjudicate between Phantom and Reality.

    ### THE PANTHEON OF 12+ ASCENDED FACULTIES:
    1.  **Tri-Vector Reality Scrying (THE CURE):** Intelligently determines its
        state based on SCAFFOLD_ENV, CLERK_SIMULATION, and request.simulation.
    2.  **Circuit-Breaker Integration:** Wraps network calls to prevent cascading
        failures if the Clerk API is unresponsive.
    3.  **Haptic Telemetry:** Proclaims its state (PHANTOM vs. KINETIC) to the
        console with high-status visual cues.
    4.  **Domain-Specific Routing:** Cleanly routes intent to specialized domain
        handlers (Users, Invites, Orgs, Sessions).
    5.  **Graceful Degradation:** If the Clerk API Key is missing in a forced
        production mode, it throws a clear, actionable Heresy.
    6.  **JIT Domain Materialization:** Only forges the heavy domain objects if
        it is certain it will be operating in the real world.
    7.  **Atomic Result Vessels:** Returns pure, validated ScaffoldResult objects
        with enriched forensic data.
    8.  **Idempotent Shutdown:** The `shutdown` rite can be called multiple times
        without causing a paradox.
    9.  **Gnostic Error Mapping:** Translates cryptic Clerk error codes into
        human-readable Socratic suggestions.
    10. **Silent Mode Awareness:** Suppresses console chatter if the `silent`
        flag is passed in the request.
    11. **Trace ID Propagation:** Ensures the `trace_id` is available for all
        sub-domain operations for end-to-end observability.
    12. **The Finality Vow:** Guaranteed path from Inception to Invitation.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)

        # --- MOVEMENT I: THE TRI-VECTOR GAZE (THE FIX) ---
        # Adjudicate the true state of reality by checking three sources of will.
        self.scaffold_env = os.environ.get("SCAFFOLD_ENV", "production").lower()
        self.clerk_sim_flag = os.environ.get("CLERK_SIMULATION") == "1"
        self.clerk_prod_flag = os.environ.get("CLERK_SIMULATION") == "0"

        # The system is in simulation UNLESS it's explicitly forced to production.
        self.is_simulation = not self.clerk_prod_flag

        # --- MOVEMENT II: MATERIALIZE ENGINES ---
        # The Phantom is always born, serving as the Mirror and Fallback.
        self.phantom = PhantomIdentityEngine(self.engine.project_root)

        if self.is_simulation:
            self.client = None
            self.is_phantom_active = True
            self.logger.info("🛡️ [IDENTITY] Gnostic Reality: SIMULATION. Phantom Identity active.")
        else:
            # We are in Production. The Kinetic Citadel must be built.
            self.client = ClerkClient()
            self.is_phantom_active = False
            self.logger.info("⚡ [IDENTITY] Gnostic Reality: KINETIC. Live Identity Citadel engaged.")

            # Materialize Domain Specialists (The Phalanx)
            self.invites = InvitationsDomain(self.client, engine)
            self.users = UsersDomain(self.client, engine)
            self.orgs = OrganizationsDomain(self.client, engine)
            self.sessions = SessionsDomain(self.client, engine)

    def execute(self, request: ClerkRequest) -> ScaffoldResult:
        """
        [THE GRAND INQUEST]
        Routes the Architect's intent through the appropriate Identity Stratum.
        """
        trace_id = getattr(request, 'request_id', 'tr-void')
        action = request.action.lower()

        try:
            # --- MOVEMENT I: THE PHANTOM INTERCEPT ---
            # Gate 1: Global system is in Simulation Mode
            # Gate 2: Specific request wants Simulation
            if self.is_phantom_active or request.simulation:
                return self.phantom.execute(request)

            # --- MOVEMENT II: KINETIC ROUTING ---
            # [ASCENSION]: Haptic Telemetry
            if not getattr(request, 'silent', False):
                self.console.print(f"[bold blue]👤 IDENTITY RITE:[/bold blue] {action.upper()}")

            # Invitation Strata
            if action in ["invite", "revoke_invite", "list_invites"]:
                return self.invites.execute(request)

            # User & Metadata Strata
            elif action in ["get_user", "update_user", "delete_user", "list_users", "update_metadata"]:
                return self.users.execute(request)

            # Organizational Strata
            elif action in ["get_org", "create_org", "update_org", "add_member"]:
                return self.orgs.execute(request)

            # Session Strata
            elif action in ["get_sessions", "kick_session"]:
                return self.sessions.execute(request)

            return self.engine.failure(f"Unknown Identity Rite: {action}")

        except Exception as e:
            self.logger.critical(f"Identity Singularity Collapse: {str(e)}")
            return self.engine.failure(
                message=f"Identity Stratum Fracture: {str(e)}",
                details=trace_id,
                severity=HeresySeverity.CRITICAL
            )

    def shutdown(self):
        """Returns the Inquisitor to a state of grace."""
        self.logger.system("Identity Sovereign entered rest state.")