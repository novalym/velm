# Path: src/scaffold/artisans/services/communication/channels/social.py
# ---------------------------------------------------------------------

from __future__ import annotations
import os
import time
import uuid
import json
import logging
import hashlib
import base64
import httpx
from typing import Any, Dict, Optional, Tuple, Union, List

# --- CORE SCAFFOLD UPLINKS ---
from .base import BaseCourier
from ..contracts import MessageEnvelope
from .....interfaces.base import ScaffoldResult
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = logging.getLogger("SocialCourier")


class SocialPhysics:
    """
    [THE LAWS OF THE SOCIAL ETHER]
    Immutable constants governing the platform giants.
    """
    # Character Limits
    LIMIT_META_TEXT = 2000
    LIMIT_WHATSAPP_TEXT = 4096
    LIMIT_GOOGLE_TEXT = 4096

    # API Endpoints
    URL_GRAPH_BASE = "https://graph.facebook.com/v19.0"
    URL_GBM_BASE = "https://businessmessages.googleapis.com/v1"

    # Cost Basis (Estimates)
    COST_WHATSAPP_CONVO = 0.08  # Blended avg for marketing/utility
    COST_META_MSG = 0.00  # Currently free for standard replies


class GoogleTokenForge:
    """
    [THE OAUTH SMITH]
    A minimal JWT signer for Google Service Accounts.
    Used if 'google-auth' library is missing or for raw control.
    """

    @staticmethod
    def mint(service_account_json: Dict) -> str:
        # In a full implementation, this uses google.oauth2.service_account
        # For this file, we assume the token is passed in or we use a library if present.
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request

            creds = service_account.Credentials.from_service_account_info(
                service_account_json,
                scopes=['https://www.googleapis.com/auth/businessmessages']
            )
            creds.refresh(Request())
            return creds.token
        except ImportError:
            Logger.warning("Google Auth library missing. Cannot mint tokens locally.")
            return "VOID_TOKEN"


class SocialCourier(BaseCourier):
    """
    =============================================================================
    == THE SOCIAL COURIER (V-Ω-OMNICHANNEL-EGRESS-TITANIUM)                    ==
    =============================================================================
    LIF: ∞ | ROLE: EXTERNAL_DIPLOMAT | RANK: SOVEREIGN

    The unified gateway for Meta (FB/IG), WhatsApp, and Google Business Messages.
    It manages the complex rituals of OAuth, Token Rotation, and Media Uploads
    so the Logic Kernel remains pure.
    """

    def deliver(self, envelope: MessageEnvelope) -> ScaffoldResult:
        """
        [THE RITE OF DISPATCH]
        Routes the envelope to the correct digital kingdom.
        """
        start_ts = time.perf_counter()

        # 1. DIVINE THE CHANNEL
        raw_channel = str(envelope.metadata.get("channel", "UNKNOWN")).upper()

        # [ASCENSION 21]: CHANNEL ALIASING
        channel_map = {
            "FACEBOOK": "META", "FB": "META", "FB_MESSENGER": "META", "META": "META",
            "INSTAGRAM": "META_IG", "IG": "META_IG",
            "WHATSAPP": "WHATSAPP", "WA": "WHATSAPP",
            "GOOGLE": "GOOGLE", "GBM": "GOOGLE", "GOOGLE_BIZ": "GOOGLE"
        }

        target_platform = channel_map.get(raw_channel, "UNKNOWN")
        trace_id = envelope.metadata.get("trace_id", f"soc-{uuid.uuid4().hex[:6]}")

        # 2. SIMULATION GATE
        is_sim = envelope.metadata.get("simulation", False) or os.environ.get("SCAFFOLD_ENV") == "development"

        try:
            if target_platform == "UNKNOWN":
                return self.engine.failure(f"Social Protocol Unknown: {raw_channel}")

            # 3. ROUTE TO SPECIALIST
            result = None
            if target_platform in ["META", "META_IG"]:
                result = self._dispatch_meta(envelope, target_platform, is_sim)
            elif target_platform == "WHATSAPP":
                result = self._dispatch_whatsapp(envelope, is_sim)
            elif target_platform == "GOOGLE":
                result = self._dispatch_google(envelope, is_sim)

            # 4. ENRICH RESULT
            duration_ms = (time.perf_counter() - start_ts) * 1000
            if result.success:
                result.vitals["latency_ms"] = duration_ms
                result.vitals["channel"] = target_platform

            return result

        except Exception as e:
            Logger.error(f"[{trace_id}] Social Egress Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Omnichannel Link Severed: {str(e)}")

    # =========================================================================
    # == HEMISPHERE I: THE META CITADEL (FB / INSTAGRAM)                     ==
    # =========================================================================

    def _dispatch_meta(self, envelope: MessageEnvelope, platform: str, is_sim: bool) -> ScaffoldResult:
        """
        Handles Graph API v19.0 calls for Page and IG conversations.
        """
        # 1. EXTRACT KEYS
        recipient_id = envelope.to[0]
        # [ASCENSION 14]: Env Fallback
        page_token = envelope.metadata.get("page_access_token") or os.environ.get("META_PAGE_TOKEN")

        if not page_token and not is_sim:
            return self.engine.failure("Meta Dispatch Failed: Page Access Token void.")

        # 2. FORGE URL
        # For FB: me/messages. For IG: me/messages (unified in v19 if page-linked)
        url = f"{SocialPhysics.URL_GRAPH_BASE}/me/messages?access_token={page_token}"

        # 3. CONSTRUCT PAYLOAD
        # [ASCENSION 5]: Truncation Physics
        safe_text = envelope.body_text[:SocialPhysics.LIMIT_META_TEXT]

        payload = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            # [ASCENSION 2]: WINDOW MANAGER
            # "HUMAN_AGENT" tag allows responding > 24h. Requires permission.
            "tag": "HUMAN_AGENT",
            "message": {"text": safe_text}
        }

        # [ASCENSION 4]: MEDIA HANDLING
        if envelope.attachments:
            # Meta requires an attachment ID or URL.
            # Assuming 'attachments' list contains URLs or local paths.
            media_item = envelope.attachments[0]
            # Simple logic: If it looks like a URL, use it.
            if str(media_item).startswith("http"):
                payload["message"] = {
                    "attachment": {
                        "type": "image",
                        "payload": {"url": str(media_item), "is_reusable": True}
                    }
                }
                # Note: Text + Image requires separate messages in standard API,
                # or complex multipart. This implementation prioritizes the image if present.

        if is_sim:
            return self._mock_success("Meta", recipient_id, payload)

        # 4. KINETIC STRIKE
        try:
            res = httpx.post(url, json=payload, timeout=10.0)

            if res.is_error:
                # [ASCENSION 8]: ERROR TRANSLATION
                return self._transmute_meta_error(res)

            data = res.json()
            return self.engine.success(
                f"Meta Signal Dispatched to {recipient_id}",
                data={
                    "message_id": data.get("message_id"),
                    "recipient_id": data.get("recipient_id"),
                    "platform": platform
                },
                vitals={"metabolic_cost_usd": 0.00}
            )

        except httpx.RequestError as e:
            return self.engine.failure(f"Meta Network Fracture: {e}")

    def _transmute_meta_error(self, res: httpx.Response) -> ScaffoldResult:
        try:
            err_body = res.json().get("error", {})
            code = err_body.get("code")
            msg = err_body.get("message")

            if code == 10:
                suggestion = "Permission Denied. Check Page Access Token scope."
            elif code == 100:
                suggestion = "Param Error. Check recipient ID validity."
            else:
                suggestion = "Consult Meta Graph API docs."

            return self.engine.failure(
                f"Meta API Rejection ({code}): {msg}",
                suggestion=suggestion,
                details=json.dumps(err_body)
            )
        except:
            return self.engine.failure(f"Meta HTTP {res.status_code}: {res.text}")

    # =========================================================================
    # == HEMISPHERE II: THE WHATSAPP CLOUD                                   ==
    # =========================================================================

    def _dispatch_whatsapp(self, envelope: MessageEnvelope, is_sim: bool) -> ScaffoldResult:
        """
        Handles WhatsApp Cloud API calls.
        """
        # 1. EXTRACT KEYS
        recipient_phone = envelope.to[0].replace("+", "")  # WA uses clean digits
        phone_id = envelope.metadata.get("phone_number_id") or os.environ.get("WHATSAPP_PHONE_ID")
        token = envelope.metadata.get("access_token") or os.environ.get("META_PAGE_TOKEN")  # Uses same system token

        if not (phone_id and token) and not is_sim:
            return self.engine.failure("WhatsApp Dispatch Failed: Phone ID or Token void.")

        url = f"{SocialPhysics.URL_GRAPH_BASE}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 2. CONSTRUCT PAYLOAD
        # [ASCENSION 11]: TEMPLATE VS TEXT
        template_name = envelope.metadata.get("template_name")

        if template_name:
            payload = {
                "messaging_product": "whatsapp",
                "to": recipient_phone,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": envelope.metadata.get("lang", "en_US")}
                }
            }
        else:
            safe_text = envelope.body_text[:SocialPhysics.LIMIT_WHATSAPP_TEXT]
            payload = {
                "messaging_product": "whatsapp",
                "to": recipient_phone,
                "type": "text",
                "text": {"body": safe_text}  # Preview URL defaults to false
            }

        if is_sim:
            return self._mock_success("WhatsApp", recipient_phone, payload)

        # 3. KINETIC STRIKE
        try:
            res = httpx.post(url, headers=headers, json=payload, timeout=10.0)

            if res.is_error:
                return self.engine.failure(f"WhatsApp Rejection: {res.text}")

            data = res.json()
            return self.engine.success(
                f"WhatsApp Signal Dispatched to {recipient_phone}",
                data={"messages": data.get("messages", [])},
                vitals={"metabolic_cost_usd": SocialPhysics.COST_WHATSAPP_CONVO}  # [ASCENSION 7]
            )

        except Exception as e:
            return self.engine.failure(f"WhatsApp Link Severed: {e}")

    # =========================================================================
    # == HEMISPHERE III: THE GOOGLE SENTINEL (GBM)                           ==
    # =========================================================================

    def _dispatch_google(self, envelope: MessageEnvelope, is_sim: bool) -> ScaffoldResult:
        """
        Handles Google Business Messages (GBM) API.
        Requires ConversationID and AgentID.
        """
        # 1. EXTRACT COORDINATES
        # For GBM, 'to' contains the conversationId
        conversation_id = envelope.to[0]

        # 2. MINT TOKEN
        # [ASCENSION 3]: Dynamic Token Minting
        # We check for a pre-minted token or raw creds
        access_token = envelope.metadata.get("access_token")
        if not access_token and not is_sim:
            creds = envelope.metadata.get("service_account") or os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
            if creds:
                if isinstance(creds, str): creds = json.loads(creds)
                access_token = GoogleTokenForge.mint(creds)

        if not access_token and not is_sim:
            # Fallback: Maybe we are running in an environment with default creds?
            # For now, strict check.
            return self.engine.failure("Google Dispatch Failed: No Credentials Manifest.")

        url = f"{SocialPhysics.URL_GBM_BASE}/conversations/{conversation_id}/messages"
        headers = {"Authorization": f"Bearer {access_token}"}

        # 3. CONSTRUCT PAYLOAD
        # [ASCENSION 6]: Idempotency
        msg_id = f"gbm-{uuid.uuid4().hex}"

        payload = {
            "messageId": msg_id,
            "representative": {
                "representativeType": "HUMAN"  # Or BOT
            },
            "text": envelope.body_text[:SocialPhysics.LIMIT_GOOGLE_TEXT]
        }

        # [ASCENSION 12]: Rich Card Stub
        if envelope.metadata.get("rich_card"):
            # If the artisan passed a structured card, use it.
            payload["richCard"] = envelope.metadata["rich_card"]
            del payload["text"]  # Rich card replaces text

        if is_sim:
            return self._mock_success("Google", conversation_id, payload)

        # 4. KINETIC STRIKE
        try:
            res = httpx.post(url, headers=headers, json=payload, timeout=10.0)

            if res.is_error:
                return self.engine.failure(f"Google Rejection: {res.text}")

            data = res.json()
            return self.engine.success(
                f"Google Signal Dispatched to {conversation_id}",
                data=data
            )
        except Exception as e:
            return self.engine.failure(f"Google Link Severed: {e}")

    # =========================================================================
    # == INTERNAL UTILITIES                                                  ==
    # =========================================================================

    def _mock_success(self, platform: str, target: str, payload: Dict) -> ScaffoldResult:
        """
        [ASCENSION 9]: HIGH-FIDELITY SIMULATION
        """
        Logger.info(f"[{platform}] SIMULATED_EGRESS -> {target}")
        Logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        return self.engine.success(
            f"Simulated {platform} Strike Successful.",
            data={
                "message_id": f"sim-{uuid.uuid4()}",
                "recipient_id": target,
                "platform": platform,
                "mode": "SIMULATION"
            },
            vitals={"metabolic_cost_usd": 0.00}
        )

# == SCRIPTURE SEALED: THE DIPLOMAT IS OMNIPRESENT ==