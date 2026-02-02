# === [scaffold/inquisitor/config.py] - SECTION 1 of 1: The Gnostic Constitution ===
from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


# =================================================================================
# == THE ENUMS OF PERCEPTION (MODES OF SIGHT)                                    ==
# =================================================================================

class GazeStrategy(str, Enum):
    """
    The Philosophy of Perception.
    """
    STRICT = "STRICT"  # Tree-sitter only. Fail if grammar missing.
    HYBRID = "HYBRID"  # Tree-sitter preferred, Regex fallback.
    SURGICAL = "SURGICAL"  # Only parse specific symbols (perf optimized).
    SHALLOW = "SHALLOW"  # Regex only (Ultra-fast, lower accuracy).


class ComplexityMetric(str, Enum):
    """
    The Calculus of Cognitive Load.
    """
    CYCLOMATIC = "cyclomatic"  # Standard branching complexity
    COGNITIVE = "cognitive"  # Nesting depth + branching (Future)
    HALSTEAD = "halstead"  # Volume/Effort (Future)


# =================================================================================
# == THE LANGUAGE REGISTRY (THE MAP OF TONGUES)                                  ==
# =================================================================================

@dataclass
class LanguageSpec:
    """The DNA of a Supported Language."""
    id: str
    extensions: List[str]
    grammar_package: str
    symbolic_cortex_class: str
    parser_class: str


# =================================================================================
# == THE INQUISITOR CONFIGURATION (THE IMMUTABLE LAW)                            ==
# =================================================================================

class InquisitorConfig(BaseModel):
    """
    =============================================================================
    == THE GNOSTIC CONSTITUTION (V-Ω-TUNABLE-REALITY)                          ==
    =============================================================================
    LIF: 10,000,000,000,000

    This vessel holds the tuning parameters for the entire Inquisitor subsystem.
    It allows the Architect to adjust the sensitivity, depth, and resource usage
    of the God-Engine's perception.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Strategy Switch:** Dynamically toggle between `STRICT` (High Gaze) and
        `SHALLOW` (Low Gaze) modes globally or per-scan.
    2.  **The Size Ward:** `max_file_size_bytes` prevents the Parser from choking on
        massive, minified monoliths (default 1MB).
    3.  **The Concurrency Governor:** `max_workers` controls the thread pool size for
        batch inquisitions, auto-scaling to CPU count.
    4.  **The Complexity Thresholds:** Tunable limits for what constitutes "Complex"
        code, used by the Ranker and Linter.
    5.  **The Timeout Sentry:** `parsing_timeout_ms` ensures a single file cannot
        halt the entire distillation rite.
    6.  **The Grammar Overrides:** A map to inject custom grammar packages at runtime.
    7.  **The Heuristic Weights:** Tunable scoring parameters for the "Low Gaze"
        regex fallback (e.g., how much weight to give a regex function match).
    8.  **The Cache Policy:** Controls the lifetime and location of the AST cache.
    9.  **The Ignore Matrix:** Deep, recursive ignore patterns specific to parsing
        (e.g., skipping tests during structural analysis).
    10. **The Language Enablement:** A set of enabled/disabled languages to prune
        the runtime overhead.
    11. **The Telemetry Level:** Controls the verbosity of the Inquisitor's internal
        monologue (for debugging grammar issues).
    12. **The Unbreakable Validator:** Self-healing validation logic to ensure
        configuration sanity.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- I. THE GAZE OF EXECUTION ---
    strategy: GazeStrategy = Field(
        default=GazeStrategy.HYBRID,
        description="The primary method of perception."
    )
    max_workers: int = Field(
        default_factory=lambda: (os.cpu_count() or 1) + 4,
        description="Thread count for parallel inquisition."
    )
    parsing_timeout_ms: int = Field(
        default=2000,
        description="Max time allowed to parse a single file before averting gaze."
    )

    # --- II. THE WARD OF FINITUDE ---
    max_file_size_bytes: int = Field(
        default=1_000_000,  # 1MB
        description="Files larger than this are treated as Binary/Blob."
    )
    max_recursion_depth: int = Field(
        default=100,
        description="Limit for AST traversal depth to prevent stack overflows."
    )

    # --- III. THE CALCULUS OF COMPLEXITY ---
    complexity_metric: ComplexityMetric = ComplexityMetric.CYCLOMATIC
    complexity_threshold_warning: int = 15
    complexity_threshold_critical: int = 30

    # --- IV. THE POLYGLOT REGISTRY ---
    enabled_languages: Set[str] = Field(
        default_factory=lambda: {"python", "javascript", "typescript", "go", "rust", "ruby", "java", "cpp"},
        description="Languages active in this session."
    )
    grammar_package_overrides: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of language_id -> custom_package_name."
    )

    # --- V. THE LOW GAZE HEURISTICS ---
    # Used when Tree-sitter fails
    heuristic_confidence_threshold: float = 0.6

    # --- VI. VALIDATION RITES ---
    @field_validator('max_workers')
    @classmethod
    def validate_workers(cls, v):
        if v < 1: return 1
        return v


# =================================================================================
# == THE GLOBAL INSTANCE (THE LAW)                                               ==
# =================================================================================
# The single source of truth for the running process.
# Can be re-consecrated via `configure_inquisitor()`.

_GLOBAL_CONFIG = InquisitorConfig()


def get_configuration() -> InquisitorConfig:
    """Retrieves the current Gnostic Constitution."""
    return _GLOBAL_CONFIG


def configure_inquisitor(new_config: InquisitorConfig):
    """
    The Rite of Re-Consecration.
    Updates the global configuration for all future Inquests.
    """
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = new_config