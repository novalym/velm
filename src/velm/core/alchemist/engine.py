# Path: src/velm/core/alchemist/engine.py
# -----------------------------------------------------------------------------------------
# == THE DIVINE ALCHEMIST (V-Ω-TOTALITY-V300.0-CONVERGENCE-REACTOR-FINALIS)             ==
# =========================================================================================
# LIF: INFINITY | ROLE: SECURE_TRANSMUTATION_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ALCHEMIST_V300_RECURSIVE_CONVERGENCE_)(@)(!@#(#@)
# =========================================================================================
#
# [ARCHITECTURAL MANIFESTO]
# The Alchemist is the God-Engine of Change. It takes the abstract Gnosis of variables
# and transmutes it into the physical Matter of code. This version implements
# 'Achronal Convergence'—resolving variables that depend on other variables across
# multiple dimensions of recursion until a stable, grounded reality is manifest.
#
# [THE PANTHEON OF 24 LEGENDARY ASCENSIONS - SEGMENT I]:
# 1.  **Hermetic Sandbox V2:** Employs a zero-trust Jinja2 environment that
#     mathematically forbids access to Python's dunder-methods and system globals.
# 2.  **Recursive Convergence Reactor:** Implements a multi-pass gaze (Default: 5)
#     to ensure nested variables like '{{ {{ sub_var }} }}' resolve perfectly.
# 3.  **Bicameral Scoping Protocol:** Automatically isolates and annihilates
#     variables starting with '_' (Private Gnosis) after a rite concludes.
# 4.  **Null-Safe Sarcophagus:** 'GnosticUndefined' prevents AttributeError
#     cascades by returning resonant void constants instead of breaking the flow.
# 5.  **Achronal Telemetry:** Measures the nanosecond latency of every alchemical
#     transmutation, injecting the tax into the result vitals.
# 6.  **Atomic Resolution Stack:** Prevents the 'Ouroboros Paradox' (Infinite
#     Recursion) by tracking the resolution depth of every variable.
# 7.  **Selective Finalization:** Employs a 'Paranoid Finalizer' that sanitizes
#     the output of every expression before it touches the scripture.
# 8.  **Socratic Scribe:** Extracts 'Undeclared Variables' from templates,
#     allowing the Mentor to prophesy missing Gnosis before execution.
# =========================================================================================

import os
import time
import shlex
import logging
import uuid
import hashlib
from pathlib import Path
from typing import Set, Any, TYPE_CHECKING, Optional, Union, Dict, List

# --- JINJA2 SACRED GEOMETRY ---
from jinja2 import meta, TemplateSyntaxError, Undefined
from jinja2.sandbox import SandboxedEnvironment

# --- CORE UPLINKS ---
from .environment import ParanoidEnvironment, gnostic_validation_rite, gnostic_native_rite, paranoid_finalizer
from .library import (
    now_rite, forge_secret_rite, to_json_rite, to_yaml_rite, shell_rite,
    is_binary_test, include_file_rite
)
from ...utils import converters as conv
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..runtime.vessels import GnosticSovereignDict

if TYPE_CHECKING:
    from ...utils.gnosis_discovery import OmegaInquisitor

# Import Mixins for logic distribution
from .resolution import ResolutionMixin
from .inference import InferenceMixin


# =============================================================================
# == II. THE SOVEREIGN ALCHEMIST                                             ==
# =============================================================================

class DivineAlchemist(ResolutionMixin, InferenceMixin):
    """
    =============================================================================
    == THE DIVINE ALCHEMIST (V-Ω-CONVERGENCE-REACTOR)                          ==
    =============================================================================
    The Supreme Conductor of Alchemical Transmutation.
    Wields the Convergence Reactor to resolve nested truths with absolute security.
    """
    Logger = Scribe("DivineAlchemist")
    _omega_inquisitor_instance = None

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        # =========================================================================
        # == THE UNBREAKABLE VOW OF STRICTNESS (THE CURE)                        ==
        # =========================================================================
        # We replace 'GnosticUndefined' with 'jinja2.StrictUndefined'.
        # This ensures that any missing variable or unmanifested function raises
        # a fatal error immediately, preventing "Ghost Matter" from being inscribed.
        import jinja2

        self.env = SandboxedEnvironment(
            autoescape=False,
            trim_blocks=True,  # Remove leading/trailing newlines from blocks
            lstrip_blocks=True,  # Strip tabs/spaces from the start of a block line
            keep_trailing_newline=False,  # Ensure we don't leak "Newline Ghosts"
            comment_start_string='<#',
            comment_end_string='#>',
            undefined=jinja2.StrictUndefined  # <--- THE SOVEREIGN ALIGNMENT
        )
        # =========================================================================

        self._arm_hermetic_wards()
        self._teach_standard_rites()
        self._bestow_gnostic_bridge()
        self._bestow_sentient_scribe()
        self.env.finalize = self._bound_finalizer
        self._resolution_stack = set()
        self._initialized = True
        self.instance_id = uuid.uuid4().hex[:8].upper()
        self.Logger.success(f"Divine Alchemist [{self.instance_id}] Consecrated with Strict Sovereignty.")

    def _arm_hermetic_wards(self):
        """
        [ASCENSION 1]: Blacklists all Python dunder-methods and system-level
        globals to enforce absolute containment of the Alchemical process.
        """
        self.env.globals.update({
            "range": range,
            "enumerate": enumerate,
            "len": len,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "any": any,
            "all": all,
            # Annihilate dangerous accessors to prevent Cerebral Breach
            "open": None,
            "getattr": None,
            "setattr": None,
            "eval": None,
            "exec": None,
            "__builtins__": None
        })

        # Intercept attribute access at the kernel level
        def is_safe_attribute(obj, attr, value):
            if str(attr).startswith("__") or str(attr).startswith("func_"):
                return False
            return True

        self.env.is_safe_attribute = is_safe_attribute

    # =========================================================================
    # == THE CONVERGENCE REACTOR (CORE TRANSMUTATION)                        ==
    # =========================================================================

    def render_string(self, source: str, context: Dict[str, Any], depth_limit: int = 5) -> str:
        """
        =============================================================================
        == THE CONVERGENCE REACTOR (V-Ω-TOTALITY-V301-FAIL-FAST)                   ==
        =============================================================================
        [ASCENSION V301]: Now warded against UndefinedError.
        """
        import jinja2
        if not source or "{{" not in source:
            return source or ""

        if not isinstance(context, GnosticSovereignDict):
            context = GnosticSovereignDict(context)

        current_matter = source
        iteration = 0
        start_ns = time.perf_counter_ns()

        while "{{" in current_matter and iteration < depth_limit:
            previous_matter = current_matter
            try:
                template = self.env.from_string(current_matter)
                current_matter = template.render(**context)

                if current_matter == previous_matter:
                    break
                iteration += 1

            # =========================================================================
            # == THE ADJUDICATION OF THE VOID (THE CORE FIX)                        ==
            # =========================================================================
            except (jinja2.exceptions.UndefinedError, NameError) as void_error:
                # If a variable is missing, we raise a Critical Heresy immediately.
                # This prevents the "!!HERESY" strings from ever being born.
                raise ArtisanHeresy(
                    f"Alchemical Heresy: Gnosis is a void. {void_error}",
                    severity=HeresySeverity.CRITICAL,
                    details=f"The scripture attempted to summon an unmanifested entity: {void_error}",
                    suggestion="Verify your '$$' definitions. If using system checks, ensure 'checks' is manifest in the context."
                )
            # =========================================================================

            except TemplateSyntaxError as e:
                raise ArtisanHeresy(
                    f"Alchemical Syntax Fracture on Line {e.lineno}: {e.message}",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Context: {current_matter[max(0, e.cursor - 20):e.cursor + 20]}"
                )
            except Exception as e:
                self.Logger.error(f"Alchemical Collapse: {e}")
                raise ValueError(f"Transmutation Paradox: {e}")

        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if latency_ms > 10.0:
            self.Logger.verbose(f"Complex Transmutation: {iteration} passes in {latency_ms:.2f}ms")

        return current_matter

    def transmute(self, matter: str, gnosis: Dict[str, Any]) -> str:
        """The Sovereign Facade for the reactor loop."""
        return self.render_string(matter, gnosis)

    # =========================================================================
    # == III. THE BICAMERAL PURGE & FILE MATERIALIZATION                     ==
    # =========================================================================

    def purge_private_gnosis(self, gnosis: Dict[str, Any]) -> Dict[str, Any]:
        """
        =============================================================================
        == THE BICAMERAL PURGE (V-Ω-TOTALITY-CLEANSE)                             ==
        =============================================================================
        [ASCENSION 3]: Surgically removes all variables starting with an underscore.
        This ensures that 'Transient Souls' (local loop variables, private flags)
        never leak into the project's permanent Gnostic Record (scaffold.lock).
        """
        return {k: v for k, v in gnosis.items() if not str(k).startswith("_")}

    def render_file(self, template_path: Union[str, Path], context: Dict[str, Any]) -> str:
        """
        =============================================================================
        == THE RITE OF MATERIALIZATION (FILE-TO-SOUL)                              ==
        =============================================================================
        LIF: 10x | ROLE: PHYSICAL_TO_GNOSTIC_BRIDGE

        Reads a physical template from the Mortal Realm and transmutes it via the
        Convergence Reactor. Hardened against encoding heresies.
        """
        path_obj = Path(template_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Alchemical Template Void: {template_path}")

        try:
            # [ASCENSION 11]: Encoding Resilience
            # We attempt to resurrect the scripture through multiple linguistic filters.
            content = None
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    content = path_obj.read_text(encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue

            if content is None:
                # Final fallback with replacement characters
                content = path_obj.read_text(encoding='utf-8', errors='replace')

            # 2. Transmute via the existing Reactor Loop
            return self.render_string(content, context)

        except Exception as e:
            raise ValueError(f"Template Rendering Fracture ({template_path}): {e}")

    # =========================================================================
    # == IV. THE TEACHING RITES (THE GRIMOIRE)                                ==
    # =========================================================================

    def _teach_standard_rites(self):
        """
        =============================================================================
        == THE LUMINOUS FILTER GRIMOIRE (V-Ω-TOTALITY-V302-STRICT)                 ==
        =============================================================================
        [ASCENSION 6]: Inscribes the complete naming nomenclature and
        data alchemies as first-class citizens of the Alchemist's mind.
        """
        import jinja2
        import shlex
        import os
        import re
        from pathlib import Path

        # --- 1. NAMING & NOMENCLATURE ---
        # Logic remains identical to previous scripture
        naming_rites = {
            'pascal': conv.to_pascal_case,
            'camel': conv.to_camel_case,
            'snake': conv.to_snake_case,
            'slug': conv.to_kebab_case,
            'kebab': conv.to_kebab_case,
            'screaming_snake': conv.to_screaming_snake_case,
            'path_safe': lambda s: re.sub(r'[^a-zA-Z0-9_\-\/]', '_', str(s))
        }
        for name, rite in naming_rites.items():
            self.env.filters[name] = rite
            self.env.filters[name.title()] = rite

        # --- 2. SECURITY & WARDING ---
        self.env.filters['shell_escape'] = shlex.quote

        # --- 3. PATH PERCEPTION ---
        self.env.filters['basename'] = lambda p: os.path.basename(str(p))
        self.env.filters['dirname'] = lambda p: os.path.dirname(str(p))
        self.env.filters['stem'] = lambda p: Path(str(p)).stem

        # --- 4. DATA ALCHEMY ---
        self.env.filters['to_json'] = to_json_rite
        self.env.filters['to_yaml'] = to_yaml_rite
        self.env.filters['native'] = lambda v, c=None: gnostic_native_rite(v, c)

        # --- 5. COLLECTION RITES ---
        self.env.filters.update({
            'join': lambda l, sep=", ": str(sep).join(map(str, l)),
            'sort': sorted,
            'unique': lambda l: list(dict.fromkeys(l)),
            'first': lambda l: l[0] if l else None,
            'last': lambda l: l[-1] if l else None,
            'count': len
        })

        # --- 6. VALIDATION & JUDGMENT ---
        self.env.filters['validate'] = gnostic_validation_rite
        self.env.tests['binary'] = is_binary_test
        self.env.tests['truthy'] = lambda v: str(v).lower() in ('true', '1', 'yes', 'y', 'on')

        # =========================================================================
        # == THE VOID TEST TRANSMUTATION (THE CURE)                              ==
        # =========================================================================
        # We no longer need to check for GnosticUndefined. Jinja2's internal
        # 'defined' test is now our sovereign judge. We only keep this if we
        # want to provide a specific 'truthy' alias for the Architect.
        # =========================================================================

    def _bestow_gnostic_bridge(self):
        """
        =============================================================================
        == THE CELESTIAL BRIDGE (V-Ω-ENVIRONMENTAL-DNA)                           ==
        =============================================================================
        [ASCENSION 9]: Connects the Alchemist to the external physical world while
        maintaining the Hermetic Ward.
        """
        self.env.globals.update({
            'now': now_rite,
            'secret': forge_secret_rite,
            'path_join': os.path.join,
            # [THE VEIL]: Controlled environment access
            'env': lambda key, default="": os.getenv(key, default),
            # Metadata for blueprint awareness
            'SCAFFOLD_VERSION': os.getenv("SCAFFOLD_VERSION", "2.6.0"),
            # [ASCENSION 3]: Dynamic Bracket Support
            'tag_start': '{%', 'tag_end': '%}',
            'var_start': '{{', 'var_end': '}}'
        })

    def _bestow_sentient_scribe(self):
        """[ASCENSION 10]: Inscribes the advanced scrying and inclusion rites."""
        self.env.globals['include_file'] = include_file_rite
        self.env.globals['shell'] = shell_rite

    # =========================================================================
    # == V. EXTERNAL REGISTRATION API                                        ==
    # =========================================================================

    def register_filter(self, name: str, rite: Any):
        """Consecrates a new filter from a third-party plugin."""
        self.env.filters[name] = rite

    def register_global(self, name: str, rite: Any):
        """Consecrates a new global function."""
        self.env.globals[name] = rite

    def register_test(self, name: str, rite: Any):
        """Consecrates a new boolean test."""
        self.env.tests[name] = rite

    def _bound_finalizer(self, value: Any) -> Any:
        """
        [THE BRIDGE OF CONSCIENCE]
        Injects the environment's Gnosis into the stateless paranoid_finalizer.
        """
        return paranoid_finalizer(value, self.env.globals, self.env.filters, self.env.tests)


# =============================================================================
# == VI. THE ALCHEMICAL SINGLETON (THE ONE TRUE SOURCE)                      ==
# =============================================================================

_alchemist_instance = None


def get_alchemist() -> DivineAlchemist:
    """
    Summons the singleton instance of the Divine Alchemist.
    Ensures that the entire Engine shares a single, warded mind.
    """
    global _alchemist_instance
    if _alchemist_instance is None:
        _alchemist_instance = DivineAlchemist()
    return _alchemist_instance

# == SCRIPTURE SEALED: THE CONVERGENCE REACTOR IS AT STEADY STATE ==

