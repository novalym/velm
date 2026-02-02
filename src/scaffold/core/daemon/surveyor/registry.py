# Path: core/daemon/surveyor/registry.py
# --------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_REGISTRY_COMPOSITE_V99

from typing import Dict, List, Type
from .sentinels.base import BaseSentinel

# --- THE MORTAL PHALANX (Static/Fast) ---
from .sentinels.python import PythonSentinel
from .sentinels.scaffold import ScaffoldSentinel
from .sentinels.javascript import JavaScriptSentinel
from .sentinels.typescript import TypeScriptSentinel
from .sentinels.rust import RustSentinel
from .sentinels.golang import GolangSentinel
from .sentinels.java import JavaSentinel
from .sentinels.infra import InfraSentinel

# --- THE DEEP BRIDGE (Advanced/Slow) ---
from .sentinels.adapter import DeepSentinelAdapter


# [PLACEHOLDER]: Import your existing advanced analysis logic here
# from ....artisans.analyze.logic import deep_scan_python, deep_scan_generic

class SentinelRegistry:
    """
    =================================================================================
    == THE SENTINEL REGISTRY (V-Ω-COMPOSITE-FACTORY)                               ==
    =================================================================================
    The central authority for assigning Guardians to Scriptures.

    [CAPABILITIES]:
    1. EXTENSION MAPPING: Resolves file types to Sentinel Keys.
    2. COMPOSITE STRATEGY: Can assign MULTIPLE Sentinels (Fast + Deep) to one file.
    3. LAZY LOADING: Instantiates logic only when summoned.
    """

    # 1. THE MAP OF TONGUES
    # Maps file extensions to internal capability keys.
    _EXTENSION_MAP = {
        # Core Gnosis
        '.scaffold': ['SCAFFOLD'],
        '.arch': ['SCAFFOLD'],
        '.symphony': ['SYMPHONY'],

        # High-Level Tongues
        '.py': ['PYTHON', 'DEEP_PYTHON'],
        '.js': ['JAVASCRIPT'],
        '.jsx': ['JAVASCRIPT'],
        '.ts': ['TYPESCRIPT'],
        '.tsx': ['TYPESCRIPT'],

        # System Tongues
        '.rs': ['RUST'],
        '.go': ['GOLANG'],
        '.java': ['JAVA'],

        # Infrastructure
        'Dockerfile': ['INFRA'],
        'docker-compose.yml': ['INFRA'],
        '.env.example': ['INFRA']
    }

    # 2. THE HALL OF GUARDIANS
    # Maps capability keys to Sentinel Classes (or Factories).
    _SENTINEL_CLASSES = {
        'SCAFFOLD': ScaffoldSentinel,
        'SYMPHONY': ScaffoldSentinel,  # Reusing structure logic for now
        'PYTHON': PythonSentinel,
        'JAVASCRIPT': JavaScriptSentinel,
        'TYPESCRIPT': TypeScriptSentinel,
        'RUST': RustSentinel,
        'GOLANG': GolangSentinel,
        'JAVA': JavaSentinel,
        'INFRA': InfraSentinel,
    }

    def __init__(self):
        # Cache instantiated sentinels to reduce overhead
        self._cache: Dict[str, BaseSentinel] = {}

        # Initialize Deep Adapters (Wiring the Advanced System)
        self._init_deep_logic()

    def _init_deep_logic(self):
        """
        [THE RITE OF BINDING]
        Wraps your existing advanced heresy detectors into the Sentinel system.
        This ensures the Grand Surveyor leverages the FULL power of the God Engine.
        """

        # Example: Wrapping a hypothetical existing Python analyzer
        # In a real scenario, you import `deep_scan_python` from your codebase.
        def mock_deep_python(content, path):
            # This is where your actual advanced logic goes
            return []

        self._cache['DEEP_PYTHON'] = DeepSentinelAdapter(
            analyzer_func=mock_deep_python,
            context="Neural Astrolabe"
        )

        # Example: Wrapping a generic security scan
        self._cache['DEEP_GENERIC'] = DeepSentinelAdapter(
            analyzer_func=lambda c, p: [],
            context="Security Omniscience"
        )

    def summon(self, filename: str) -> List[BaseSentinel]:
        """
        [THE SUMMONING RITE]
        Returns a PHALANX (List) of Sentinels for a given file.
        This allows us to run Fast checks first, then Deep checks.
        """
        sentinels = []

        # 1. Divine Keys by Extension/Filename
        keys = self._divine_keys(filename)

        # 2. Materialize Sentinels
        for key in keys:
            if key in self._cache:
                # Use cached instance (Deep Adapters are pre-cached)
                sentinels.append(self._cache[key])
            elif key in self._SENTINEL_CLASSES:
                # Instantiate Mortal Sentinel and cache it
                instance = self._SENTINEL_CLASSES[key]()
                self._cache[key] = instance
                sentinels.append(instance)

        return sentinels

    def _divine_keys(self, filename: str) -> List[str]:
        """
        Resolves the list of capabilities required for a file.
        """
        # Exact Match (Dockerfiles, Configs)
        if filename in self._EXTENSION_MAP:
            return self._EXTENSION_MAP[filename]

        # Extension Match
        # Handle compound extensions? (e.g. .test.ts) - Future
        import os
        _, ext = os.path.splitext(filename)

        return self._EXTENSION_MAP.get(ext.lower(), [])

    @classmethod
    def summon_phalanx(cls):
        """Static factory for the Engine."""
        return cls()