from typing import Any
from .providers.base import BaseCRMProvider
from .providers.hubspot import HubSpotSovereign


# from .providers.salesforce import SalesforceSovereign (Future Prophecy)

class CRMFactory:
    """[THE PROVIDER FORGE] Instantiates the correct Diplomat."""

    @staticmethod
    def get_provider(name: str, engine: Any) -> BaseCRMProvider:
        if name == "hubspot":
            return HubSpotSovereign(engine)
        elif name == "salesforce":
            # return SalesforceSovereign(engine)
            raise NotImplementedError("Salesforce Diplomat not yet consecrated.")
        else:
            raise ValueError(f"Unknown CRM Provider: {name}")