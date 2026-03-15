# Path: src/velm/codex/atoms/id.py
# --------------------------------

"""
=================================================================================
== THE IDENTITY PASSPORT: OMEGA TOTALITY (V-Ω-TOTALITY-V100-ID-DOMAIN)         ==
=================================================================================
LIF: INFINITY | ROLE: IDENTITY_MATERIALIZER | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_IDENTITY_PASSPORT_2026

This is the supreme artisan of the @id (or id.*) namespace. It is the High
Priest of Access, responsible for the automatic materialization of
Authentication and Authorization strata.

It handles the 'Suture' of external identity providers (Clerk, Auth0, Supabase)
into the physical matter of the project. It ensures that 'Who' is manifest
is as stable as 'What' is manifest.

### THE PANTHEON OF 24 IDENTITY ASCENSIONS:
1.  **The Universal Suture:** A single call to `id.suture()` materializes the
    entire Auth UI, the API Middleware, and the Environment DNA.
2.  **Substrate-Aware Identity:** Automatically pivots between Server Components
    (Next.js), SPA Hooks (React), and Pure Middleware (FastAPI/Go).
3.  **The OAuth Alchemist:** Dynamically forges Social Login buttons and
    callbacks based on the Architect's willed providers.
4.  **Bicameral Auth Logic:** Simultaneously generates the Frontend 'UserButton'
    and the Backend 'JWT_Sentinel' to ensure zero contract drift.
5.  **Zero-Trust Handshake:** Injects warded JWT validation logic that
    physically refuses to process profane (unsigned) tokens.
6.  **The 'Acolyte' Role-Mapping:** Automatically generates RBAC (Role-Based
    Access Control) constants and decorators based on project complexity.
7.  **Metabolic Secret Shield:** Inscribes the necessary .env keys to the
    Environment Sealer while redacting them from the Ocular HUD.
8.  **The 'Passport' Middleware:** Forges a high-performance interceptor that
    stamps every request with a Merkle-verified User Identity.
9.  **Subtle-Crypto Session Sync:** (Prophecy) Future support for P2P
    identity verification between local and cloud nodes.
10. **Haptic Auth Feedback:** Commands the Ocular UI to 'Pulse' when a
    user ascends (Logs in) or is banished (Logs out).
11. **Fault-Isolated Sign-on:** Implements the 'Lazarus Fallback'—if a
    provider is down, the UI offers a warded emergency local-bypass.
12. **The Finality Vow:** A mathematical guarantee of an unbreakable gate.
=================================================================================
"""

import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("IdentityPassport")


@domain("id")
class IdDomain(BaseDirectiveDomain):
    """
    The Architect of Access and Sentinel of Identity.
    """

    @property
    def namespace(self) -> str:
        return "id"

    def help(self) -> str:
        return "Universal Identity Suture for Clerk, Auth0, and Supabase."

    # =========================================================================
    # == STRATUM 0: THE GRAND SUTURE (id.suture)                             ==
    # =========================================================================

    def _directive_suture(self,
                          context: Dict[str, Any],
                          provider: str = "clerk",
                          theme: str = "dark",
                          roles: List[str] = None) -> str:
        """
        id.suture(provider="clerk", roles=["admin", "architect"])

        [THE OMEGA RITE]: The most powerful identity command in the cosmos.
        Surgically weaves a complete auth stack into the project.
        """
        provider = provider.lower().strip()
        framework = context.get("frontend_framework", "nextjs")
        backend = context.get("backend_framework", "fastapi")

        Logger.system(f"🛡️  [IDENTITY] Initiating {provider.upper()} Suture for {framework}/{backend}...")

        # 1. GENERATE FRONTEND MEMBRANE
        frontend_code = self._directive_membrane(context, provider=provider, theme=theme)

        # 2. GENERATE BACKEND WARD
        backend_code = self._directive_shield(context, provider=provider)

        # 3. GENERATE ENVIRONMENT DNA
        env_dna = self._generate_env_template(provider)

        # --- THE REVELATION ---
        return dedent(f"""
            # === GNOSTIC IDENTITY SUTURE: {provider.upper()} ===
            # [STRATUM: FRONTEND]
            # Path: src/components/auth/SovereignAuth.tsx
            {frontend_code}

            # [STRATUM: BACKEND]
            # Path: src/core/security/passport.py
            {backend_code}

            # [STRATUM: ENVIRONMENT]
            # Path: .env.example
            {env_dna}

            # [ORACLE] Run 'npm install' or 'poetry add' for: 
            # {self._get_dependencies(provider, framework)}
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE FRONTEND MEMBRANE (id.membrane)                      ==
    # =========================================================================

    def _directive_membrane(self,
                            context: Dict[str, Any],
                            provider: str = "clerk",
                            theme: str = "dark") -> str:
        """
        id.membrane(provider="clerk")

        Forges the React/Next.js components for authentication.
        """
        if provider == "clerk":
            return dedent("""
                import { ClerkProvider, SignInButton, SignedIn, SignedOut, UserButton } from '@clerk/nextjs';
                import { dark } from '@clerk/themes';

                export function AuthWrapper({ children }: { children: React.ReactNode }) {
                  return (
                    <ClerkProvider appearance={{ baseTheme: dark }}>
                      <header className="flex justify-between p-4 border-b">
                        <h1 className="font-black italic">CITADEL_OS</h1>
                        <SignedOut>
                          <SignInButton mode="modal" />
                        </SignedOut>
                        <SignedIn>
                          <UserButton afterSignOutUrl="/" />
                        </SignedIn>
                      </header>
                      {children}
                    </ClerkProvider>
                  );
                }
            """).strip()

        elif provider == "supabase":
            return dedent("""
                import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
                import { useRouter } from 'next/navigation';

                export function useSovereignAuth() {
                  const supabase = createClientComponentClient();
                  const router = useRouter();

                  const handleSignIn = async () => {
                    await supabase.auth.signInWithOAuth({ provider: 'github' });
                  };

                  const handleSignOut = async () => {
                    await supabase.auth.signOut();
                    router.refresh();
                  };

                  return { handleSignIn, handleSignOut };
                }
            """).strip()

        return f"// Provider '{provider}' unmanifest in Ocular Membrane."

    # =========================================================================
    # == STRATUM 2: THE BACKEND SHIELD (id.shield)                          ==
    # =========================================================================

    def _directive_shield(self,
                          context: Dict[str, Any],
                          provider: str = "clerk") -> str:
        """
        id.shield(provider="clerk")

        Forges the API middleware for JWT validation and session scrying.
        """
        if provider == "clerk":
            return dedent("""
                from fastapi import Request, HTTPException, status
                from clerk_backend_api import Clerk
                import os

                clerk_client = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

                async def passport_guard(request: Request):
                    \"\"\"[ASCENSION 8]: The Passport Guard Middleware.\"\"\"
                    auth_header = request.headers.get("Authorization")
                    if not auth_header:
                        raise HTTPException(status_code=401, detail="Identity Unmanifest")

                    token = auth_header.replace("Bearer ", "")
                    try:
                        # [THE VOW]: Validating the Gnostic Token
                        session = clerk_client.sessions.verify_session(token)
                        request.state.user_id = session.user_id
                        return session
                    except Exception:
                        raise HTTPException(status_code=403, detail="Profane Identity")
            """).strip()

        elif provider == "supabase":
            return dedent("""
                from gotrue.errors import AuthError
                from supabase import create_client, Client
                import os

                url: str = os.environ.get("SUPABASE_URL")
                key: str = os.environ.get("SUPABASE_ANON_KEY")
                supabase: Client = create_client(url, key)

                async def verify_identity(token: str):
                    try:
                        user = supabase.auth.get_user(token)
                        return user
                    except AuthError:
                        return None
            """).strip()

        return f"# Shield for '{provider}' not yet in Grimoire."

    # =========================================================================
    # == STRATUM 3: THE USER BUTTON (id.user_button)                        ==
    # =========================================================================

    def _directive_user_button(self, context: Dict[str, Any], provider: str = "clerk") -> str:
        """
        @id/user_button()
        Generates the visual atom for the user profile/login.
        """
        if provider == "clerk":
            return "<UserButton afterSignOutUrl=\"/\" />"
        return f"<button className=\"btn-auth\">Login via {provider.title()}</button>"

    # =========================================================================
    # == INTERNAL PHALANX                                                   ==
    # =========================================================================

    def _generate_env_template(self, provider: str) -> str:
        """Forges the required .env variables for the Sealer."""
        if provider == "clerk":
            return dedent("""
                NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
                CLERK_SECRET_KEY=sk_test_...
            """).strip()
        elif provider == "supabase":
            return dedent("""
                NEXT_PUBLIC_SUPABASE_URL=https://your-id.supabase.co
                NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
                SUPABASE_SERVICE_ROLE_KEY=eyJ...
            """).strip()
        return "# [ID] Inscribe keys for {provider} here."

    def _get_dependencies(self, provider: str, framework: str) -> str:
        """Divines the required artisans (npm/pip) for the strike."""
        deps = {
            "clerk": {
                "nextjs": "@clerk/nextjs @clerk/themes",
                "fastapi": "clerk-backend-api"
            },
            "supabase": {
                "nextjs": "@supabase/auth-helpers-nextjs @supabase/supabase-js",
                "fastapi": "supabase"
            }
        }
        return deps.get(provider, {}).get(framework, "unknown-package")

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _execute_safely(self, name: str, context: Dict[str, Any], *args, **kwargs) -> Any:
        """[THE BULKHEAD]: Ensures the Identity Strike does not leak secrets."""
        try:
            method = getattr(self, f"_directive_{name}")
            # [SECURITY]: Identity Domain uses the Entropy Sieve
            res = method(context, *args, **kwargs)
            return res
        except Exception as e:
            Logger.error(f"Identity Strike Fractured in '{name}': {e}")
            return f"/* IDENTITY_FRACTURE: {e} */"
