# Path: scaffold/artisans/seed/fabricator.py
# ------------------------------------------
import random
from typing import Any, Dict

try:
    from faker import Faker

    FAKE = Faker()
except ImportError:
    FAKE = None


class DataFabricator:
    """
    =============================================================================
    == THE FABRICATOR (V-Ω-SEMANTIC-GENERATOR)                                 ==
    =============================================================================
    Transmutes Type Hints and Variable Names into Mock Data.
    """

    def forge(self, field_name: str, field_type: str) -> Any:
        if not FAKE: return "Install 'faker' for gnosis."

        name = field_name.lower()

        # Semantic Heuristics
        if "email" in name: return FAKE.email()
        if "name" in name: return FAKE.name()
        if "phone" in name: return FAKE.phone_number()
        if "address" in name: return FAKE.address()
        if "url" in name: return FAKE.url()
        if "uuid" in name or "id" == name: return FAKE.uuid4()
        if "created_at" in name: return FAKE.iso8601()

        # Type Heuristics
        if field_type == "int": return random.randint(1, 100)
        if field_type == "bool": return random.choice([True, False])
        if field_type == "float": return random.uniform(0.0, 100.0)

        return FAKE.word()

    def generate_row(self, schema: Dict[str, str]) -> Dict[str, Any]:
        return {k: self.forge(k, v) for k, v in schema.items()}