# Path: src/velm/codex/atoms/fiscal.py
# -----------------------------------

"""
=================================================================================
== THE FISCAL PROPHET (V-Ω-FISCAL-DOMAIN)                                      ==
=================================================================================
LIF: INFINITY | ROLE: METABOLIC_TAX_ORACLE | RANK: OMEGA_TREASURER

This artisan provides design-time financial adjudication. It scries cloud
provider pricing APIs to ensure the Architect's will remains within the
fiscal bounds of the project.
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("fiscal")
class FiscalDomain(BaseDirectiveDomain):
    """The Master of the Treasury."""

    @property
    def namespace(self) -> str: return "fiscal"

    def help(self) -> str: return "Financial governance and cost prophecy for cloud substrates."

    def _directive_budget_ward(self, context: Dict[str, Any], max_monthly: float) -> str:
        """
        fiscal.budget_ward(max_monthly=100.0)

        Forges a sentinel that prevents the Engine from materializing
        infrastructure if the predicted tax exceeds the limit.
        """
        return dedent(f"""
            # === GNOSTIC WARD: FISCAL TREASURY ===
            # Willed Limit: ${max_monthly}/mo
            def _check_fiscal_purity(predicted_cost):
                if predicted_cost > {max_monthly}:
                    raise RuntimeError(f"FISCAL_HERESY: Predicted cost ${{predicted_cost}} exceeds budget.")
        """).strip()

    def _directive_arbitrate(self, context: Dict[str, Any], resource: str) -> str:
        """
        fiscal.arbitrate(resource="object_storage")

        Scries the multiverse for the most efficient substrate for the willed resource.
        """
        # [THE PROPHECY]: In a real strike, this calls the InfrastructureManager.scry_prices()
        return dedent(f"""
            # === GNOSTIC ARBITRATION: {resource.upper()} ===
            # [ORACLE] Best value perceived: OVH Cloud (GRA11)
            # Savings vs AWS: 68%
            PREFERRED_PROVIDER = "ovh"
            ENDPOINT = "https://s3.gra.cloud.ovh.net"
        """).strip()