# scaffold/semantic_injection/directives/mock_domain.py

"""
=================================================================================
== THE FABRICATOR OF ILLUSION (V-Ω-MOCK-DOMAIN)                                ==
=================================================================================
LIF: 75,000,000,000

This artisan implements the `@mock` namespace. It is a deterministic generator
of fake data. It does not require external heavy libraries (like faker) but uses
Gnostic heuristics to generate plausible realities.

Usage:
    seeds/users.json :: @mock/users_json(count=5)
    .env :: ADMIN_EMAIL=@mock/email
    tests/data.csv :: @mock/csv(cols="id,name,email", rows=10)
=================================================================================
"""
import json
import random
import uuid
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("mock")
class MockDomain(BaseDirectiveDomain):
    """
    The Forge of Counterfeit Reality.
    """

    @property
    def namespace(self) -> str:
        return "mock"

    def help(self) -> str:
        return "Generates fake data (json, csv, email, profiles) for testing/seeding."

    # --- Internal Datasets for Plausible Illusion ---
    FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Felix", "Grace", "Hector", "Iris", "Jack"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez"]
    DOMAINS = ["example.com", "test.org", "local.dev", "scaffold.io"]

    # =========================================================================
    # == THE RITES OF FABRICATION                                            ==
    # =========================================================================

    def _generate_person(self) -> Dict[str, str]:
        first = random.choice(self.FIRST_NAMES)
        last = random.choice(self.LAST_NAMES)
        return {
            "id": str(uuid.uuid4()),
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}@{random.choice(self.DOMAINS)}",
            "created_at": datetime_now_iso()
        }

    def _directive_email(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """@mock/email"""
        person = self._generate_person()
        return person["email"]

    def _directive_uuid(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """@mock/uuid"""
        return str(uuid.uuid4())

    def _directive_users_json(self, context: Dict[str, Any], count: int = 5, *args, **kwargs) -> str:
        """@mock/users_json(count=5)"""
        try:
            count = int(count)
        except:
            count = 5

        users = [self._generate_person() for _ in range(count)]
        return json.dumps(users, indent=2)

    def _directive_csv(self, context: Dict[str, Any], cols: str = "id,name,email", rows: int = 5, *args,
                       **kwargs) -> str:
        """
        @mock/csv(cols="id,name,status", rows=5)
        Generates a CSV string.
        Supported col types: id, name, email, date, status, int
        """
        headers = [c.strip() for c in cols.split(',')]
        lines = [",".join(headers)]

        for _ in range(rows):
            row_data = []
            for col in headers:
                col_lower = col.lower()
                if "id" in col_lower:
                    row_data.append(str(uuid.uuid4())[:8])
                elif "email" in col_lower:
                    row_data.append(self._directive_email(context))
                elif "name" in col_lower:
                    p = self._generate_person()
                    row_data.append(f"{p['first_name']} {p['last_name']}")
                elif "date" in col_lower or "at" in col_lower:
                    row_data.append(datetime_now_iso())
                elif "status" in col_lower:
                    row_data.append(random.choice(["active", "pending", "deleted"]))
                else:
                    row_data.append("value")
            lines.append(",".join(row_data))

        return "\n".join(lines)


def datetime_now_iso():
    # Helper to avoid importing datetime at module level if not needed
    import datetime
    return datetime.datetime.now().isoformat()