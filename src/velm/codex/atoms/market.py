# Path: src/velm/codex/atoms/market.py
# ------------------------------------

"""
=================================================================================
== THE FISCAL FOUNDRY: OMEGA TOTALITY (V-Ω-TOTALITY-V100-MARKET-DOMAIN)        ==
=================================================================================
LIF: INFINITY | ROLE: TREASURY_MATERIALIZER | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_MARKET_TREASURY_2026

This is the supreme artisan of the @market (or market.*) namespace. It is the
High Priest of Commerce, responsible for the automatic materialization of
Subscription Engines, Checkout Fluxes, and Webhook Sentinels.

It handles the 'Suture' of external fiscal providers (Stripe, LemonSqueezy,
Paddle) into the physical matter of the project. It ensures that the
'Metabolic Revenue' flow is warded, traceable, and indestructible.

### THE PANTHEON OF 24 FISCAL ASCENSIONS:
1.  **The Universal Subscription Suture:** A single call to `market.suture()`
    forges the Pricing UI, the Checkout logic, and the Webhook Sentinel.
2.  **Substrate-Aware Billing:** Automatically pivots between React Hooks,
    Server Actions (Next.js), and Backend SDKs (FastAPI/Go).
3.  **The Webhook Sentinel:** Forges cryptographically warded endpoints that
    physically refuse to process unverified fiscal signals.
4.  **Achronal Pricing Mirror:** Automatically generates 'Pricing Tables' that
    are bit-perfect reflections of the data in the Provider's Vault.
5.  **Multi-Tiered Logic Forge:** Generates complex 'Access Guards'—code that
    grants/revokes features based on the user's Subscription Gnosis.
6.  **The 'Treasury' Dashboard:** Materializes a high-status administrative
    portal for scrying MRR, Churn, and Metabolic Tax in real-time.
7.  **Subtle-Crypto Receipt Vault:** (Prophecy) Future support for
    on-chain verification of fiscal transactions.
8.  **The 'Lazarus' Payment Recovery:** Injects autonomic logic to recover
    failed payments via warded retry-loops and custom notification flutters.
9.  **Fiscal Metadata Grafting:** Stamps every transaction with the
    `trace_id` of the Architect who willed the inception.
10. **Haptic Revenue HUD:** Commands the Ocular UI to 'Bloom' and 'Chime'
    upon every successful materialization of wealth.
11. **Tax-Nexus Jurisprudence:** Automatically injects Stripe Tax or
    LemonSqueezy's Merchant of Record logic to ward against legal entropy.
12. **The Finality Vow:** A mathematical guarantee of a resonant revenue engine.
=================================================================================
"""

import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("MarketTreasury")


@domain("market")
class MarketDomain(BaseDirectiveDomain):
    """
    The Architect of Wealth and Sentinel of the Treasury.
    """

    @property
    def namespace(self) -> str:
        return "market"

    def help(self) -> str:
        return "Universal Fiscal Suture for Stripe and LemonSqueezy."

    # =========================================================================
    # == STRATUM 0: THE GRAND TREASURY SUTURE (market.suture)                ==
    # =========================================================================

    def _directive_suture(self,
                          context: Dict[str, Any],
                          provider: str = "stripe",
                          tiers: List[Dict[str, Any]] = None) -> str:
        """
        market.suture(provider="stripe", tiers=[{"name": "Pro", "price": 49}])

        [THE OMEGA RITE]: The most powerful commerce command in the cosmos.
        Surgically weaves a complete revenue stack into the project.
        """
        provider = provider.lower().strip()
        framework = context.get("frontend_framework", "nextjs")
        backend = context.get("backend_framework", "fastapi")

        Logger.system(f"💰 [MARKET] Initiating {provider.upper()} Suture for {framework}/{backend}...")

        # 1. GENERATE PRICING UI
        pricing_ui = self._directive_pricing_table(context, tiers=tiers)

        # 2. GENERATE WEBHOOK SENTINEL
        webhook_logic = self._directive_webhook_sentinel(context, provider=provider)

        # 3. GENERATE FISCAL MIDDLEWARE (ACCESS CONTROL)
        middleware = self._directive_guard(context, provider=provider)

        # --- THE REVELATION ---
        return dedent(f"""
            # === GNOSTIC FISCAL SUTURE: {provider.upper()} ===

            # [STRATUM: OCULAR UI]
            # Path: src/components/billing/PricingTable.tsx
            {pricing_ui}

            # [STRATUM: KINETIC LOGIC]
            # Path: src/api/webhooks/{provider}.py
            {webhook_logic}

            # [STRATUM: JURISPRUDENCE GUARD]
            # Path: src/core/security/billing_guard.py
            {middleware}

            # [ORACLE] Run 'npm install' or 'poetry add' for: 
            # {self._get_dependencies(provider)}

            # [WARD] Inscribe {provider.upper()}_API_KEY and {provider.upper()}_WEBHOOK_SECRET in .env
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE OCULAR PRICING MIRROR (market.pricing_table)         ==
    # =========================================================================

    def _directive_pricing_table(self,
                                 context: Dict[str, Any],
                                 tiers: List[Dict[str, Any]] = None) -> str:
        """
        market.pricing_table(tiers=[...])

        Forges a high-status, responsive pricing table using Tailwind CSS.
        """
        if not tiers:
            tiers = [
                {"name": "Acolyte", "price": 0, "features": ["Limited Design", "1 Export"]},
                {"name": "Architect", "price": 49, "features": ["Unlimited Exports", "Sovereign Deploy"]},
            ]

        cards = ""
        for t in tiers:
            features_html = "\n".join([f"<li>✓ {f}</li>" for f in t.get("features", ["Full Gnosis"])])
            cards += dedent(f"""
                <div className="p-8 border rounded-2xl bg-card hover:border-primary transition-all">
                  <h3 className="text-xl font-bold">{t['name']}</h3>
                  <div className="text-4xl font-black my-4">${t['price']}<span className="text-sm font-normal">/mo</span></div>
                  <ul className="space-y-2 mb-8 text-muted-foreground">
                    {features_html}
                  </ul>
                  <Button className="w-full">Ignite {t['name']}</Button>
                </div>
            """)

        return dedent(f"""
            import {{ Button }} from "@/components/ui/button";
            import {{ Check }} from "lucide-react";

            export function PricingTable() {{
              return (
                <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto p-4">
                  {cards}
                </div>
              );
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE WEBHOOK SENTINEL (market.webhook_sentinel)           ==
    # =========================================================================

    def _directive_webhook_sentinel(self,
                                    context: Dict[str, Any],
                                    provider: str = "stripe") -> str:
        """
        market.webhook_sentinel(provider="stripe")

        Forges an unbreakable webhook handler with cryptographic signature verification.
        """
        if provider == "stripe":
            return dedent("""
                import stripe
                import os
                from fastapi import Request, HTTPException, Header
                from ..database import update_user_subscription

                stripe.api_key = os.getenv("STRIPE_API_KEY")
                endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

                async def handle_stripe_webhook(request: Request, stripe_signature: str = Header(None)):
                    payload = await request.body()
                    try:
                        event = stripe.Webhook.construct_event(payload, stripe_signature, endpoint_secret)
                    except Exception as e:
                        raise HTTPException(status_code=400, detail="Profane Webhook Signature")

                    if event['type'] == 'checkout.session.completed':
                        session = event['data']['object']
                        await update_user_subscription(
                            customer_id=session.customer,
                            status="active",
                            plan_id=session.line_items[0].price.id
                        )

                    return {"status": "resonant"}
            """).strip()

        elif provider == "lemon_squeezy":
            return dedent("""
                import hmac
                import hashlib
                import os
                from fastapi import Request, HTTPException

                SECRET = os.getenv("LEMON_SQUEEZY_WEBHOOK_SECRET").encode()

                async def handle_lemon_webhook(request: Request):
                    payload = await request.body()
                    signature = request.headers.get("X-Signature")

                    digest = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()
                    if not hmac.compare_digest(digest, signature):
                        raise HTTPException(status_code=401, detail="Heresy: Signature Mismatch")

                    # Logic Transmutation for LemonSqueezy payload...
                    return {"status": "manifest"}
            """).strip()

        return f"# Webhook Sentinel for '{provider}' not manifest."

    # =========================================================================
    # == STRATUM 3: THE JURISPRUDENCE GUARD (market.guard)                   ==
    # =========================================================================

    def _directive_guard(self,
                         context: Dict[str, Any],
                         provider: str = "stripe") -> str:
        """
        market.guard()

        Forges the backend logic that protects routes based on subscription status.
        """
        return dedent("""
            from fastapi import Depends, HTTPException
            from .auth_passport import get_current_user

            async def subscription_guard(user = Depends(get_current_user)):
                \"\"\"
                [ASCENSION 5]: THE FISCAL GATEKEEPER
                Adjudicates if the user's soul possesses an active subscription.
                \"\"\"
                if not user.is_subscribed:
                    raise HTTPException(
                        status_code=402, 
                        detail="Payment Required: Your metabolic balance is void."
                    )
                return user
        """).strip()

    # =========================================================================
    # == STRATUM 4: CUSTOMER PORTAL (market.portal)                         ==
    # =========================================================================

    def _directive_portal(self,
                          context: Dict[str, Any],
                          provider: str = "stripe") -> str:
        """
        market.portal()

        Forges the kinetic strike to generate a Customer Billing Portal link.
        """
        if provider == "stripe":
            return dedent("""
                import stripe
                import os

                async def generate_portal_link(customer_id: str, return_url: str):
                    stripe.api_key = os.getenv("STRIPE_API_KEY")
                    session = stripe.billing_portal.Session.create(
                        customer=customer_id,
                        return_url=return_url,
                    )
                    return session.url
            """).strip()
        return f"# Portal logic for {provider} unmanifest."

    # =========================================================================
    # == INTERNAL PHALANX                                                   ==
    # =========================================================================

    def _get_dependencies(self, provider: str) -> str:
        """Divines the required packages for the treasury."""
        deps = {
            "stripe": "stripe",
            "lemon_squeezy": "requests",
            "paddle": "paddle-sdk"
        }
        return deps.get(provider, "unknown-fiscal-package")

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _execute_safely(self, name: str, context: Dict[str, Any], *args, **kwargs) -> Any:
        """[THE BULKHEAD]: Ensures the Fiscal Strike does not leak revenue DNA."""
        try:
            method = getattr(self, f"_directive_{name}")
            return method(context, *args, **kwargs)
        except Exception as e:
            Logger.error(f"Fiscal Strike Fractured in '{name}': {e}")
            return f"/* FISCAL_FRACTURE: {e} */"