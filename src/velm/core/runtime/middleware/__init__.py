# Path: scaffold/core/runtime/middleware/__init__.py
# --------------------------------------------------

"""
=================================================================================
== THE MIDDLEWARE PANTHEON (V-Ω-ETERNAL-REGISTRY)                              ==
=================================================================================
This sanctum holds the 21 Guardians of the Gnostic Pipeline.
"""

from .contract import Middleware, NextHandler
from .pipeline import MiddlewarePipeline

# --- The Guardians of the Flow (Identity & Metaphysics) ---
from .tracing import DistributedTracingMiddleware
from .singularity import SingularityMiddleware
from .telemetry import TelemetryMiddleware

# --- The Guardians of Input (Purity) ---
from .harmonizer import PathNormalizationMiddleware
from .veil import SecretScrubberMiddleware
from .auth import AuthMiddleware
from .constitution import ConstitutionMiddleware  # <--- KEYSTONE
from .policy import PolicyMiddleware  # <--- NEW

# --- The Guardians of Context (Wisdom) ---
from .enrichment import EnrichmentMiddleware
from .librarian import SemanticInjectorMiddleware

# --- The Guardians of Performance (Speed) ---
from .caching import CachingMiddleware
from .resonance import ResonanceMiddleware

# --- The Guardians of Stability (Resilience) ---
from .entropy_shield import EntropyShieldMiddleware
from .governor import RateLimitMiddleware
from .circuit import CircuitBreakerMiddleware
from .healing import SelfHealingMiddleware
from .persona_warden import PersonaWardenMiddleware
# --- The Guardians of Execution (Safety & Feedback) ---
from .prerequisites import PrerequisiteMiddleware
from .safety import SafetyMiddleware
from .budget import BudgetMiddleware
from .forensics import ForensicMiddleware
from .notification import NotificationMiddleware  # <--- NEW
from .output_veil import OutputRedactionMiddleware # <--- NEW

from .flags import FeatureFlagMiddleware  # <--- NEW

from .chaos import ChaosMiddleware        # <--- NEW
from .compliance import ComplianceMiddleware
from .optimization import OptimizationMiddleware
from .reflective import ReflectiveCritiqueMiddleware
from .adaptive import AdaptiveResourceMiddleware

__all__ = [
    "Middleware",
    "MiddlewarePipeline",

    "DistributedTracingMiddleware",
    "SingularityMiddleware",
    "TelemetryMiddleware",

    "PathNormalizationMiddleware",
    "SecretScrubberMiddleware",
    "AuthMiddleware",
    "ConstitutionMiddleware",
    "PolicyMiddleware",

    "EnrichmentMiddleware",
    "SemanticInjectorMiddleware",

    "CachingMiddleware",
    "ResonanceMiddleware",

    "EntropyShieldMiddleware",
    "RateLimitMiddleware",
    "CircuitBreakerMiddleware",
    "SelfHealingMiddleware",

    "PrerequisiteMiddleware",
    "SafetyMiddleware",
    "BudgetMiddleware",
    "ForensicMiddleware",
    "NotificationMiddleware",
    "FeatureFlagMiddleware",
    "ChaosMiddleware",
    "OutputRedactionMiddleware",
    "ComplianceMiddleware",
    "OptimizationMiddleware",
    "ReflectiveCritiqueMiddleware",
    "AdaptiveResourceMiddleware",
    "NextHandler",
    "PersonaWardenMiddleware",

]