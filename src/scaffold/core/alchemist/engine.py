# Path: scaffold/core/alchemist/engine.py
# ---------------------------------------

import os
from pathlib import Path
from typing import Set, Any, TYPE_CHECKING, Optional, Union, Dict

from .environment import ParanoidEnvironment, gnostic_validation_rite, gnostic_native_rite, paranoid_finalizer
from .library import (
    now_rite, forge_secret_rite, to_json_rite, to_yaml_rite, shell_rite,
    is_binary_test, include_file_rite
)
from ...utils import converters as conv
from ...logger import Scribe

if TYPE_CHECKING:
    from ...utils.gnosis_discovery import OmegaInquisitor

# Import Mixins
from .resolution import ResolutionMixin
from .inference import InferenceMixin


class DivineAlchemist(ResolutionMixin, InferenceMixin):
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC ALCHEMY (V-Ω-LEGENDARY-ULTIMA++. THE FACADE)      ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The Central Coordinator of the Alchemical Sanctum. It unifies the Environment,
    the Library, and the Logic Mixins into a single, sovereign entity.
    """
    Logger = Scribe("DivineAlchemist")
    _omega_inquisitor_instance = None

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        # 1. Forge Environment (Without Finalizer first)
        self.env = ParanoidEnvironment(
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            comment_start_string='<#',
            comment_end_string='#>',
        )

        # 2. Teach Rites (Standard Lib)
        self._teach_standard_rites()
        self._bestow_gnostic_bridge()
        self._bestow_sentient_scribe()

        # 3. Bind The Paranoid Finalizer (The Gnostic Bridge)
        # We bind it late so it can access the populated globals/filters.
        self.env.finalize = self._bound_finalizer

        # 4. Initialize State
        self._resolution_stack: Set[str] = set()
        self._initialized = True
        self.Logger.verbose("Divine Alchemist (Modular) Consecrated.")

    def _bound_finalizer(self, value: Any) -> Any:
        """
        [THE BRIDGE OF CONSCIENCE]
        Injects the environment's Gnosis into the stateless paranoid_finalizer.
        """
        return paranoid_finalizer(value, self.env.globals, self.env.filters, self.env.tests)

    def _get_inquisitor(self) -> 'OmegaInquisitor':
        """The Lazy Bridge to the OmegaInquisitor."""
        if self._omega_inquisitor_instance is None:
            from ...utils.gnosis_discovery import OmegaInquisitor
            self._omega_inquisitor_instance = OmegaInquisitor()
        return self._omega_inquisitor_instance

    # --- THE PROXIES OF COMPATIBILITY (THE HEALING) ---

    def _forge_secret_rite(self, length: int = 32, secret_type: str = 'hex') -> str:
        """
        [THE RESTORED LIMB]
        Proxies the library function to satisfy the GenesisProfiles contract.
        """
        return forge_secret_rite(length, secret_type)

    def render_string(self, source: str, context: Dict[str, Any]) -> str:
        """
        [THE RITE OF TRANSMUTATION]
        Compiles a raw string template and renders it with the provided Gnosis.
        This is the atomic unit of the Alchemist's power.
        """
        if not source:
            return ""

        try:
            # The Paranoid Environment handles the compilation and sandboxing
            template = self.env.from_string(source)
            return template.render(**context)
        except Exception as e:
            # We catch the fracture here to prevent a total system collapse
            # Raising ValueError allows the caller (render_file) to catch and contextualize it
            raise ValueError(f"Alchemical Transmutation Fracture: {e}")

    def render_file(self, template_path: Union[str, Path], context: Dict[str, Any]) -> str:
        """
        [THE RITE OF MATERIALIZATION]
        Reads a physical template scripture from disk and transmutes it with Gnosis.

        This bypasses the internal Jinja loader to allow rendering files
        from any location (e.g. user overrides, absolute paths).
        """
        path_obj = Path(template_path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Alchemical Template not found: {template_path}")

        try:
            # 1. Ingest the Scripture
            content = path_obj.read_text(encoding="utf-8")

            # 2. Transmute via the existing String Rite
            return self.render_string(content, context)

        except Exception as e:
            raise ValueError(f"Template Rendering Fracture ({template_path}): {e}")
    # --- THE TEACHING RITES ---

    def _teach_standard_rites(self):
        # Naming
        naming_rites = {
            'pascal': conv.to_pascal_case,
            'camel': conv.to_camel_case,
            'snake': conv.to_snake_case,
            'slug': conv.to_kebab_case,
            'kebab': conv.to_kebab_case,
            'screaming_snake': conv.to_screaming_snake_case,
        }
        for name, rite in naming_rites.items():
            self.env.filters[name] = rite
            self.env.filters[name.title()] = rite

        # Security
        import shlex
        self.env.filters['shell_escape'] = shlex.quote

        # Path
        self.env.filters['basename'] = lambda p: os.path.basename(str(p))
        self.env.filters['dirname'] = lambda p: os.path.dirname(str(p))
        self.env.filters['stem'] = lambda p: Path(str(p)).stem

        # Data
        self.env.filters['to_json'] = to_json_rite
        self.env.filters['to_yaml'] = to_yaml_rite
        self.env.filters['native'] = lambda v, c=None: gnostic_native_rite(v, c)  # wrapper to match sig

        # List
        self.env.filters['join'] = lambda l, sep=", ": str(sep).join(map(str, l))
        self.env.filters['sort'] = lambda l: sorted(l)
        self.env.filters['unique'] = lambda l: list(dict.fromkeys(l))

        # Validation
        self.env.filters['validate'] = gnostic_validation_rite

        # Tests
        self.env.tests['binary'] = is_binary_test
        self.env.tests['truthy'] = lambda v: str(v).lower() in ('true', '1', 'yes', 'y')

    def _bestow_gnostic_bridge(self):
        self.env.globals['now'] = now_rite
        self.env.globals['secret'] = forge_secret_rite
        self.env.globals['path_join'] = os.path.join
        self.env.globals['env'] = lambda key, default=None: os.getenv(key, default)
        self.env.globals['tag_start'] = '{%'
        self.env.globals['tag_end'] = '%}'
        self.env.globals['var_start'] = '{{'
        self.env.globals['var_end'] = '}}'

    def _bestow_sentient_scribe(self):
        self.env.globals['include_file'] = include_file_rite
        self.env.globals['shell'] = shell_rite

    # Dynamic Registration API
    def register_filter(self, name: str, rite: Any):
        self.env.filters[name] = rite

    def register_global(self, name: str, rite: Any):
        self.env.globals[name] = rite

    def register_test(self, name: str, rite: Any):
        self.env.tests[name] = rite


# The Singleton Factory
_alchemist_instance = None


def get_alchemist() -> DivineAlchemist:
    global _alchemist_instance
    if _alchemist_instance is None:
        _alchemist_instance = DivineAlchemist()
    return _alchemist_instance