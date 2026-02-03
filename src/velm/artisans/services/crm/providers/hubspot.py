import os
import httpx
from typing import Any, Dict, List
from .base import BaseCRMProvider
from .....contracts.heresy_contracts import ArtisanHeresy


class HubSpotSovereign(BaseCRMProvider):
    """
    [THE ORANGE GIANT]
    High-fidelity interaction with the HubSpot V3 API.
    """
    BASE_URL = "https://api.hubapi.com"

    def _get_headers(self) -> Dict[str, str]:
        token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
        if not token:
            raise ArtisanHeresy("HubSpot Access Token missing from environment.")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def create(self, entity: str, data: Dict) -> Any:
        url = f"{self.BASE_URL}/crm/v3/objects/{entity}"
        res = httpx.post(url, headers=self._get_headers(), json={"properties": data})
        if res.is_error: self._handle_error(res)
        return res.json()

    def update(self, entity: str, entity_id: str, data: Dict) -> Any:
        url = f"{self.BASE_URL}/crm/v3/objects/{entity}/{entity_id}"
        res = httpx.patch(url, headers=self._get_headers(), json={"properties": data})
        if res.is_error: self._handle_error(res)
        return res.json()

    def get(self, entity: str, entity_id: str, properties: List[str] = None) -> Any:
        url = f"{self.BASE_URL}/crm/v3/objects/{entity}/{entity_id}"
        params = {"properties": ",".join(properties)} if properties else {}
        res = httpx.get(url, headers=self._get_headers(), params=params)
        if res.is_error: self._handle_error(res)
        return res.json()

    def search(self, entity: str, field: str, value: str, properties: List[str] = None) -> Any:
        url = f"{self.BASE_URL}/crm/v3/objects/{entity}/search"
        payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": field,
                    "operator": "EQ",
                    "value": value
                }]
            }]
        }
        if properties: payload["properties"] = properties

        res = httpx.post(url, headers=self._get_headers(), json=payload)
        if res.is_error: self._handle_error(res)

        # Return list of results
        return res.json().get('results', [])

    def associate(self, from_entity: str, from_id: str, to_entity: str, to_id: str) -> Any:
        # HubSpot V4 Association API
        # We need the association Type ID. For simplicity, we use the default primary labels.
        # This mapping is complex in HubSpot, so we assume standard objects.

        # Standard Map: contact_to_company, deal_to_contact, etc.
        assoc_type = f"{from_entity}_to_{to_entity}"

        url = f"{self.BASE_URL}/crm/v3/objects/{from_entity}/{from_id}/associations/{to_entity}/{to_id}/{assoc_type}"
        res = httpx.put(url, headers=self._get_headers())
        if res.is_error: self._handle_error(res)
        return res.json()

    def _handle_error(self, res: httpx.Response):
        try:
            err = res.json()
            msg = err.get('message', res.text)
        except:
            msg = res.text
        raise ArtisanHeresy(f"HubSpot Rejection ({res.status_code}): {msg}")