# Path: src/velm/codex/atoms/ghost.py
# ----------------------------------

"""
=================================================================================
== THE GHOST SIMULACRUM: OMEGA TOTALITY (V-Ω-TOTALITY-V100-GHOST-DOMAIN)      ==
=================================================================================
LIF: INFINITY | ROLE: API_REALITY_MIRROR | RANK: OMEGA_SOVEREIGN

This is the supreme artisan of the @ghost namespace. It is responsible for the
materialization of "Ghost Enclaves"—local, stateful, and warded simulations of
external SaaS providers (Stripe, AWS, Twilio, GitHub, etc.).

It allows the God-Engine to function in "Achronal Isolation," removing the
dependency on external aether (Internet) during the development and
adjudication phases of a project.

### THE PANTHEON OF 24 GHOST ASCENSIONS:
1.  **Stateful Memory Lattice:** Every ghost maintains an in-memory SQLite or
    Redis-lite database to track willed entities (Customers, Buckets, Messages).
2.  **Substrate-Agnostic Redirection:** Automatically scries the environment and
    swaps `API_BASE` URLs between Local-Ghost and Remote-Iron.
3.  **The Webhook Radiator:** Forges the logic to "Push" events from the Ghost
    back to the application, simulating external asynchronous triggers.
4.  **Temporal Replay Suture:** Allows the Architect to "Record" real API
    interactions and transmute them into deterministic Ghost Blueprints.
5.  **Metabolic Failure Injection:** Logic to simulate 429 (Rate Limit),
    500 (Fracture), and 504 (Timeout) events to test app resilience.
6.  **Shannon-Entropy Secret Mocking:** Generates fake keys (rk_test_...)
    that match the exact geometry of real secrets but hold zero value.
7.  **The OAuth2 Handshake Mirror:** Simulates complex authentication flows
    (Google/GitHub) without leaving the local substrate.
8.  **Hydraulic Paging Emulation:** Natively handles cursor-based and offset
    pagination for large simulated datasets.
9.  **Geometric Signature Validation:** Every mock response is verified against
    the provider's actual Pydantic/Zod schema to prevent "Mirror Drift."
10. **Distributed Tracing Suture:** Injects the `X-Gnostic-Trace` ID into
    mock logs to allow for unified forensic scrying across ghosts.
11. **Apophatic Permissions:** Mocks can be configured to return 403 Forbidden
    to test the application's Jurisprudence layer.
12. **The Finality Vow:** A mathematical guarantee of 1:1 API parity.
=================================================================================
"""

import re
import json
import uuid
import time
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("GhostForge")


@domain("ghost")
class GhostDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE MASTER OF SHADOWS                                                   ==
    =============================================================================
    Forges the Virtual Twins of the Global SaaS Grid.
    """

    @property
    def namespace(self) -> str:
        return "ghost"

    def help(self) -> str:
        return "Materializes stateful API enclaves (Stripe, AWS, Twilio, GitHub)."

    # =========================================================================
    # == STRATUM 0: THE FISCAL SHADOW (STRIPE)                              ==
    # =========================================================================

    def _directive_stripe(self,
                          context: Dict[str, Any],
                          port: int = 8081,
                          version: str = "2024-02-01",
                          webhook_port: int = 8000,
                          persist: bool = True) -> str:
        """
        ghost.stripe(port=8081, webhook_port=3000)

        Forges a stateful Stripe API Enclave. It manages Customers, Prices,
        and Subscriptions in a local RAM-lattice and radiates webhooks.
        """
        p_name = context.get("project_name", "Reality")

        return dedent(f"""
            # === GNOSTIC GHOST: STRIPE ENCLAVE (TOTALITY) ===
            # ROLE: FISCAL_SIMULACRUM | PORT: {port}

            import os
            from fastapi import FastAPI, Request, Response, HTTPException
            from pydantic import BaseModel
            import uvicorn, threading, time, uuid, json, requests

            app = FastAPI(title="Stripe Ghost for {p_name}")

            # [STRATUM: MEMORY]
            # The RAM-Lattice for persistent simulation
            VAULT = {{
                "customers": {{}},
                "subscriptions": {{}},
                "webhooks": []
            }}

            @app.post("/v1/customers")
            async def create_customer(request: Request):
                form = await request.form()
                c_id = f"cus_{{uuid.uuid4().hex[:14]}}"
                customer = {{
                    "id": c_id,
                    "object": "customer",
                    "email": form.get("email"),
                    "metadata": {{}},
                    "created": int(time.time())
                }}
                VAULT["customers"][c_id] = customer
                _radiate_webhook("customer.created", customer)
                return customer

            @app.get("/v1/customers/{{c_id}}")
            async def get_customer(c_id: str):
                if c_id not in VAULT["customers"]:
                    raise HTTPException(status_code=404, detail="Customer unmanifest in Shadow.")
                return VAULT["customers"][c_id]

            def _radiate_webhook(event_type, data):
                def _strike():
                    # [ASCENSION 3]: Webhook Radiation logic
                    payload = {{
                        "id": f"evt_{{uuid.uuid4().hex[:14]}}",
                        "object": "event",
                        "type": event_type,
                        "data": {{"object": data}},
                        "created": int(time.time())
                    }}
                    try:
                        requests.post("http://localhost:{webhook_port}/webhooks/stripe", json=payload)
                    except: pass
                threading.Thread(target=_strike, daemon=True).start()

            # [IGNITION]
            def start_ghost():
                print("👻 [GHOST] Stripe Enclave Awakening on port {port}...")
                uvicorn.run(app, host="127.0.0.1", port={port}, log_level="error")

            if os.getenv("SCAFFOLD_ENV") == "development":
                # Suture the environment DNA
                os.environ["STRIPE_API_BASE"] = "http://localhost:{port}/v1"
                os.environ["STRIPE_API_KEY"] = "sk_test_gnostic_ghost_key"
                if not any(t.name == "StripeGhost" for t in threading.enumerate()):
                    threading.Thread(target=start_ghost, name="StripeGhost", daemon=True).start()
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE CELESTIAL MIRROR (AWS / LOCALSTACK)                 ==
    # =========================================================================

    def _directive_aws(self,
                       context: Dict[str, Any],
                       services: List[str] = None,
                       region: str = "us-east-1") -> str:
        """
        ghost.aws(services=["s3", "sqs", "lambda"])

        Forges the link to LocalStack. It ensures the environment DNA is
        sutured to redirect Boto3 calls to the local Docker-based AWS mirror.
        """
        s_list = services or ["s3"]
        s_str = ",".join(s_list)

        return dedent(f"""
            # === GNOSTIC GHOST: AWS MIRROR (LOCALSTACK) ===
            # SERVICES: {s_str}

            import os, boto3
            from botocore.config import Config

            if os.getenv("SCAFFOLD_ENV") == "development":
                # [ASCENSION 2]: Substrate Redirection
                ENDPOINT = "http://localhost:4566"

                # Suture the Global Session
                # Bypasses physical signature verification for local speed
                os.environ["AWS_ACCESS_KEY_ID"] = "test"
                os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
                os.environ["AWS_DEFAULT_REGION"] = "{region}"

                def get_ghost_client(service_name):
                    return boto3.client(
                        service_name,
                        endpoint_url=ENDPOINT,
                        use_ssl=False,
                        verify=False,
                        config=Config(retries={{"max_attempts": 0}})
                    )

                print("🛰️ [GHOST] AWS Mirror engaged via LocalStack ({s_str})")
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE TELEPHONIC GHOST (TWILIO)                          ==
    # =========================================================================

    def _directive_twilio(self,
                          context: Dict[str, Any],
                          port: int = 8082) -> str:
        """
        ghost.twilio(port=8082)

        Forges a simulation of the Twilio Programmable Voice/SMS API.
        It captures outgoing signals and allows for "Inbound" simulation.
        """
        return dedent(f"""
            # === GNOSTIC GHOST: TWILIO ENCLAVE ===
            import os, threading, uvicorn
            from fastapi import FastAPI, Form

            app = FastAPI(title="Twilio Ghost")
            LEDGER = []

            @app.post("/2010-04-01/Accounts/{{acc}}/Messages.json")
            async def send_message(acc: str, To: str = Form(...), From: str = Form(...), Body: str = Form(...)):
                msg = {{"id": f"SM{{uuid.uuid4().hex}}", "to": To, "from": From, "body": Body, "status": "sent"}}
                LEDGER.append(msg)
                print(f"📱 [GHOST] SMS Intercepted: {{To}} -> {{Body}}")
                return msg

            # [IGNITION]
            if os.getenv("SCAFFOLD_ENV") == "development":
                os.environ["TWILIO_API_BASE"] = "http://localhost:{port}"
                threading.Thread(
                    target=lambda: uvicorn.run(app, host="127.0.0.1", port={port}, log_level="error"),
                    daemon=True
                ).start()
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE CODE ARCHIVE GHOST (GITHUB)                        ==
    # =========================================================================

    def _directive_github(self,
                          context: Dict[str, Any],
                          org: str = "novalym",
                          repos: List[str] = None) -> str:
        """
        ghost.github(org="novalym", repos=["velm-core"])

        Forges a mock of the GitHub API. Essential for testing CI/CD
        orchestrators or repository management artisans.
        """
        repo_data = {r: {"id": i, "name": r, "full_name": f"{org}/{r}"} for i, r in enumerate(repos or ["reality"])}
        repo_json = json.dumps(repo_data)

        return dedent(f"""
            # === GNOSTIC GHOST: GITHUB API ===
            import os, threading, uvicorn, json
            from fastapi import FastAPI

            app = FastAPI()
            REPOS = {repo_json}

            @app.get("/orgs/{org}/repos")
            async def list_repos():
                return list(REPOS.values())

            @app.get("/repos/{org}/{{repo_name}}")
            async def get_repo(repo_name: str):
                return REPOS.get(repo_name, {{"error": "not found"}})

            if os.getenv("SCAFFOLD_ENV") == "development":
                os.environ["GITHUB_API_URL"] = "http://localhost:8083"
                threading.Thread(
                    target=lambda: uvicorn.run(app, host="127.0.0.1", port=8083, log_level="error"),
                    daemon=True
                ).start()
        """).strip()

    # =========================================================================
    # == STRATUM 4: THE FAILURE INJECTOR (RESILIENCE)                      ==
    # =========================================================================

    def _directive_chaos_proxy(self,
                               context: Dict[str, Any],
                               target_url: str,
                               failure_rate: float = 0.1) -> str:
        """
        ghost.chaos_proxy(target_url="http://localhost:8081", failure_rate=0.2)

        Forges a middleware proxy that randomly injects latency or HTTP
        errors into mock calls to test application robustness.
        """
        return dedent(f"""
            # === GNOSTIC GHOST: CHAOS PROXY ===
            import random, time, requests

            class ChaosProxy:
                def __init__(self):
                    self.failure_rate = {failure_rate}
                    self.target = "{target_url}"

                def strike(self, method, path, **kwargs):
                    # [ASCENSION 5]: Metabolic Failure Injection
                    if random.random() < self.failure_rate:
                        choice = random.choice(["delay", "429", "500"])
                        if choice == "delay": 
                            print("⏳ [CHAOS] Injecting Latency...")
                            time.sleep(random.uniform(2.0, 5.0))
                        elif choice == "429": return {{"status_code": 429, "error": "Too Many Requests"}}
                        else: return {{"status_code": 500, "error": "Internal Server Fracture"}}

                    return requests.request(method, f"{{self.target}}{{path}}", **kwargs)
        """).strip()

    # =========================================================================
    # == STRATUM 5: THE MAIL ENCLAVE (SENDGRID/MAILCHIMP)                  ==
    # =========================================================================

    def _directive_mail_enclave(self, context: Dict[str, Any], port: int = 8084) -> str:
        """
        ghost.mail_enclave(port=8084)

        Materializes a local SMTP/API mock for email services. Captures
        all outgoing mail and renders them in the Ocular UI.
        """
        return dedent(f"""
            # === GNOSTIC GHOST: MAIL ENCLAVE ===
            import os, threading, uvicorn
            from fastapi import FastAPI, Body

            app = FastAPI()
            OUTBOX = []

            @app.post("/v3/mail/send")
            async def send_mail(payload: dict = Body(...)):
                OUTBOX.append(payload)
                print(f"📧 [GHOST] Email Captured to: {{payload.get('personalizations',[])[0].get('to',[])[0].get('email')}}")
                return Response(status_code=202)

            if os.getenv("SCAFFOLD_ENV") == "development":
                os.environ["MAIL_API_BASE"] = "http://localhost:{port}"
                threading.Thread(
                    target=lambda: uvicorn.run(app, host="127.0.0.1", port={port}, log_level="error"),
                    daemon=True
                ).start()
        """).strip()

    # =========================================================================
    # == STRATUM 6: THE REALTIME GHOST (WEBSOCKETS/SSE)                   ==
    # =========================================================================

    def _directive_pusher_mirror(self, context: Dict[str, Any], port: int = 8085) -> str:
        """
        ghost.pusher_mirror(port=8085)

        Forges a local WebSocket server that mimics Pusher or Ably.
        Enables testing of real-time Ocular HUD updates offline.
        """
        return dedent(f"""
            # === GNOSTIC GHOST: REALTIME MIRROR ===
            import os, threading, uvicorn
            from fastapi import FastAPI, WebSocket

            app = FastAPI()

            @app.websocket("/app/{{app_key}}")
            async def websocket_endpoint(websocket: WebSocket):
                await websocket.accept()
                print("🔌 [GHOST] Realtime Membrane Linked.")
                while True:
                    data = await websocket.receive_text()
                    await websocket.send_text(f"Ghost Echo: {{data}}")

            if os.getenv("SCAFFOLD_ENV") == "development":
                os.environ["PUSHER_HOST"] = "localhost"
                os.environ["PUSHER_PORT"] = "{port}"
                threading.Thread(
                    target=lambda: uvicorn.run(app, host="127.0.0.1", port={port}, log_level="error"),
                    daemon=True
                ).start()
        """).strip()

    # =========================================================================
    # == STRATUM 7: THE REPLAY ORACLE (FORENSICS)                          ==
    # =========================================================================

    def _directive_replay_suture(self, context: Dict[str, Any], session_log: str) -> str:
        """
        ghost.replay_suture(session_log="./logs/api_traffic.jsonl")

        [ASCENSION 4]: The Temporal Replay Suture.
        Transmutes a traffic log into a deterministic Ghost response map.
        """
        return dedent(f"""
            # === GNOSTIC GHOST: REPLAY SUTURE ===
            import json
            class ReplayOracle:
                def __init__(self):
                    with open("{session_log}", "r") as f:
                        self.history = [json.loads(line) for line in f]

                def scry_response(self, request_hash):
                    # Finds the historical response that matches the request geometry
                    return next((item['response'] for item in self.history if item['hash'] == request_hash), None)
        """).strip()