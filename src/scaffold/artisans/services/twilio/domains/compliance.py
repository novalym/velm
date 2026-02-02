# Path: scaffold/artisans/services/twilio/domains/compliance.py
# -------------------------------------------------------------

import os
from twilio.base.exceptions import TwilioRestException
from .base import BaseTwilioDomain
from .....interfaces.base import ScaffoldResult
from .....interfaces.requests import TwilioRequest


class ComplianceDomain(BaseTwilioDomain):
    """[THE HIGH SCRIBE] A2P 10DLC & Regulatory."""

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        if request.action == "register_brand": return self._brand(request)
        if request.action == "register_campaign": return self._campaign(request)
        if request.action == "link_number": return self._link(request)
        return self.engine.failure(f"Unknown Compliance Rite: {request.action}")

    def _brand(self, req: TwilioRequest) -> ScaffoldResult:
        try:
            # 1. Customer Profile
            profile = self.client.trusthub.v1.customer_profiles.create(
                friendly_name=req.legal_name,
                email=req.email,
                policy_sid=req.policy_sid or "RN00000000000000000000000000000000"
            )
            # 2. A2P Brand
            brand = self.client.messaging.v1.brand_registrations.create(
                customer_profile_bundle_sid=profile.sid,
                brand_type="STANDARD"
            )
            return self.engine.success("Brand Created", data={"brand_sid": brand.sid, "profile_sid": profile.sid})
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Brand"))

    def _campaign(self, req: TwilioRequest) -> ScaffoldResult:
        if not req.brand_sid: return self.engine.failure("Campaign requires brand_sid.")
        try:
            # 1. Service
            service = self.client.messaging.v1.services.create(friendly_name=f"Cmp: {req.friendly_name}")
            # 2. Campaign
            campaign = self.client.messaging.v1.services(service.sid).us_app_to_person.create(
                brand_registration_sid=req.brand_sid,
                description=req.description or "Notifications",
                sample_msg_1=req.sample_msgs[0] if req.sample_msgs else "Sample Message",
                us_app_to_person_usecase=req.use_case,
                has_embedded_links=True,
                has_embedded_phone=True
            )
            return self.engine.success("Campaign Submitted",
                                       data={"campaign_sid": campaign.sid, "service_sid": service.sid})
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Campaign"))

    def _link(self, req: TwilioRequest) -> ScaffoldResult:
        """Links a Phone Number SID to a Messaging Service SID."""
        if not req.sid and not req.phone_number: return self.engine.failure("Link requires Phone SID/Number.")
        if not req.messaging_service_sid: return self.engine.failure("Link requires Messaging Service SID.")

        try:
            # Resolve SID
            phone_sid = req.sid
            if not phone_sid:
                existing = self.client.incoming_phone_numbers.list(phone_number=req.phone_number, limit=1)
                if existing: phone_sid = existing[0].sid

            if not phone_sid: return self.engine.failure("Phone Number not found.")

            # Add to Service
            self.client.messaging.v1.services(req.messaging_service_sid).phone_numbers.create(
                phone_number_sid=phone_sid
            )
            return self.engine.success(f"Number {phone_sid} linked to Service {req.messaging_service_sid}")
        except TwilioRestException as e:
            return self.engine.failure(self.alchemist.transmute_error(e, "Link"))