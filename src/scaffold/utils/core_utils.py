import difflib
import io
import ast
import hashlib
import io
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import tempfile
import threading
import time
import webbrowser
from collections import defaultdict
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from queue import Queue
from typing import Dict, Any, Optional, Union, List, Tuple, Iterator, TYPE_CHECKING, Set

import pathspec
import requests

from ..contracts.data_contracts import GnosticVessel
from ..contracts.symphony_contracts import Edict
from ..contracts.data_contracts import InscriptionAction, GnosticVessel
from ..contracts.data_contracts import GnosticLineType
from ..contracts.symphony_contracts import EdictType
if TYPE_CHECKING:

    from ..contracts.communion_contracts import GnosticPlea
    from ..contracts.data_contracts import PlanEdict
    from ..core.alchemist import DivineAlchemist

RICH_AVAILABLE = False
try:
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.console import Console, Group
    from dataclasses import dataclass, asdict
    from packaging.version import parse as parse_version
    from rich.text import Text
except ImportError as e:
    print(f"Import error! Reason: {e}")

from ..constants import PROPHETIC_GRIMOIRE, PROFANE_PATH_CHARS, PROFANE_UNSEEN_CHARS
# --- THE SUMMONS IS COMPLETE ---
from ..contracts.data_contracts import GnosticDossier, GnosticWriteResult
from ..contracts.communion_contracts import GnosticPlea, GnosticPleaType


from ..logger import Scribe, get_console
from ..help_registry import register_gnosis
from .. import __version__
JINJA_AVAILABLE = False
try:
    from jinja2 import Environment, meta, TemplateSyntaxError
    JINJA_AVAILABLE = True
except ImportError as e:
    print(f"Import error! reason: {e}")
Logger = Scribe("Utils")

# --- THE GRIMOIRE OF TEXTUAL EXTENSIONS (V-Ω-EXPANDED) ---
# A definitive list of extensions that are guaranteed to be text.
KNOWN_TEXT_EXTENSIONS = {
    # Config & Data
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml', '.env',
    '.gitignore', '.dockerignore', '.editorconfig', '.scaffold', '.symphony', '.arch',
    # Documentation
    '.md', '.txt', '.rst', '.adoc', '.csv', '.log',
    # Web
    '.html', '.htm', '.css', '.scss', '.sass', '.less', '.js', '.jsx', '.ts', '.tsx', '.svg', '.vue', '.svelte',
    # Code
    '.py', '.pyw', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.rb', '.php',
    '.sh', '.bash', '.zsh', '.bat', '.ps1', '.cmd', '.lua', '.pl', '.pm', '.r', '.dart',
    '.swift', '.kt', '.kts', '.scala', '.clj', '.cljs', '.fs', '.fsx', '.ex', '.exs',
    # Infra
    '.dockerfile', 'dockerfile', 'makefile', 'jenkinsfile', 'vagrantfile'
}


def _determine_sanctum(path: Path, project_root: Path) -> str:
    """
    Performs a Gaze to determine which sub-project (sanctum) a file belongs to.
    This is the heart of the federated monorepo awareness.
    """
    try:
        # A file's sanctum is its first parent directory inside the project root.
        # e.g., apps/web/components/Button.tsx -> sanctum is 'apps/web'
        relative_path = path.relative_to(project_root)
        if len(relative_path.parts) > 1:
            # Heuristic: combine first two parts for sanctums like 'apps/web' or 'packages/ui'
            if relative_path.parts[0] in ('apps', 'packages', 'libs'):
                if len(relative_path.parts) > 2:
                    return f"{relative_path.parts[0]}/{relative_path.parts[1]}"
            return relative_path.parts[0]
        return "root"  # Belongs to the root of the project
    except (ValueError, IndexError):
        return "external"  # Path is outside the project root, a rare paradox

# =================================================================================
# ==                  SANCTUM OF UNBREAKABLE GNOSIS (UTILS)                      ==
# =================================================================================
#
# This is not a miscellaneous file. This is the sacred sanctum where the core,
# unchanging Gnostic truths and helper artisans of the scaffold engine reside.
#
# Every function herein is forged with three divine virtues:
#   1. Purity: It performs one task and performs it flawlessly.
#   2. Independence: It has zero dependencies on other scaffold modules to
#      prevent catastrophic circular import paradoxes.
#   3. Timelessness: It represents a fundamental truth of the scaffold
#      ecosystem that is unlikely to change.
#
# =================================================================================

def perform_alchemical_resolution(
        dossier: 'GnosticDossier',
        initial_gnosis: Dict[str, Any],
        raw_definitions: Dict[str, str],
        overrides: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC ALCHEMY (V-Ω-ETERNAL-ULTIMA-FORENSIC-ASCENDED)      ==
    =================================================================================
    @gnosis:LIF 10,000,000 (ABSOLUTE GNOSTIC AUTHORITY & UNBREAKABLE RESILIENCE)
    @gnosis:summary The final, eternal, and ultra-definitive form of the variable resolution engine.

    @gnosis:description
    This is the divine, sentient God-Engine of Gnostic Alchemy. It conducts the Rite
    of Iterative Transmutation with a pantheon of 12 legendary faculties, forging a
    perfectly resolved, Gnostically pure context from a chaotic web of dependencies.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Gnostic Differentiator:** It is now a pure artisan of Gnosis. It no
        longer presumes to know the raw scripture of the blueprint. It receives the
        pure, pre-forged `GnosticDossier` and `raw_definitions`, separating its will
        from the perception of form.

    2.  **The Gaze of the Native Soul (Type Inference):** It possesses a divine Gaze.
        It perceives static literals (`true`, `123`, `["a"]`) and transmutes them into
        their pure Pythonic souls (`bool`, `int`, `list`), annihilating the Heresy of
        the Profane String.

    3.  **The Law of Scriptural Supremacy:** It enforces the sacred, 4-tier hierarchy
        of Gnostic truth: Overrides > Scripture > Initial Gnosis > Defaults, ensuring
        the Architect's will is always absolute.

    4.  **The Alchemical Inquisitor:** Its `transmute` rite is shielded by an unbreakable
        ward. If a Jinja expression fails, it no longer shatters the symphony. It
        forges a luminous `Heresy` vessel and inscribes it upon the `dossier`.

    5.  **The Ward of the Gnostic Ouroboros:** Its Gaze for circular dependencies is
        now that of a Forensic Inquisitor. It proclaims a luminous `Heresy` detailing
        exactly which variables are stalled and which souls they await, transforming
        a cryptic failure into a divine lesson.

    6.  **The Gnostic Chronocacher (Inherited):** It wields the `DivineAlchemist`, whose
        own Gaze is cached, making repeated transmutations of the same scripture
        instantaneous.

    7.  **The Polyglot Mind:** It understands the Gnostic Graph (`dossier.dependencies`)
        and can resolve a complex, tangled web of derivations in the optimal order.

    8.  **The Luminous Voice:** Its every thought—every transmutation, every judgment—is
        proclaimed to the `AlchemicalEngine` Scribe for hyper-diagnostic insight.

    9.  **The Unbreakable Contract:** Its signature is pure, its dependencies explicit.
        It returns a single, pure vessel of Gnosis: the final, resolved dictionary.

    10. **The Supreme Edict's Ward:** It ensures that `overrides` are eternally supreme,
        immune to being overwritten by any other Gnostic source.

    11. **The Recursive Gaze (Future Prophecy):** Its architecture, which separates the
        Gaze for dependencies from the act of transmutation, is perfectly forged for a
        future ascension to a full topological sort for even greater performance.

    12. **The Sovereign Soul:** It is a pure, self-contained artisan, its Gnosis now
        enshrined in `core_utils`, available to all in the cosmos.
    =================================================================================
    """
    from ..core.alchemist import get_alchemist
    from ..logger import Scribe
    from ..contracts.heresy_contracts import Heresy, HeresySeverity
    import json  # For the Gaze of the Native Soul

    alchemist = get_alchemist()
    Logger = Scribe("AlchemicalEngine")

    overrides = overrides or {}

    # --- MOVEMENT I: THE FORGING OF THE INITIAL REALITY ---
    # The hierarchy begins: Initial Gnosis is the bedrock.
    resolved_vars = initial_gnosis.copy()

    # We create a new vessel for unresolved variables to maintain the purity of the loop
    unresolved_vars: Dict[str, str] = {}

    # --- MOVEMENT II: THE RITE OF SCRIPTURAL SUPREMACY & THE GAZE OF THE NATIVE SOUL ---
    # We iterate over ALL variables defined in the blueprint's scripture.
    for var_name, raw_val_str in raw_definitions.items():
        # [FACULTY 10] The Supreme Edict's Ward
        if var_name in overrides:
            resolved_vars[var_name] = overrides[var_name]
            continue

        # [FACULTY 2] The Gaze of the Native Soul
        is_dynamic = '{{' in raw_val_str or '{%' in raw_val_str

        # We check if this variable's soul depends on others.
        if var_name in dossier.dependencies and dossier.dependencies[var_name]:
            unresolved_vars[var_name] = raw_val_str
        elif is_dynamic:
            # It has Jinja but no *known* dependencies. A simple transmutation.
            try:
                resolved_vars[var_name] = alchemist.transmute(raw_val_str, resolved_vars)
            except Exception as e:
                dossier.heresies.append(Heresy(
                    message=f"Alchemical paradox transmuting '{var_name}'",
                    details=str(e), line_num=0, line_content=f"$$ {var_name} = {raw_val_str}",
                    severity=HeresySeverity.CRITICAL
                ))
        else:
            # It is Static. We perceive its true Native Soul.
            val_str = raw_val_str.strip()
            transmuted_val: Any = val_str

            # Gnostic Triage for Types
            lower_val = val_str.lower()
            if lower_val == 'true':
                transmuted_val = True
            elif lower_val == 'false':
                transmuted_val = False
            elif val_str.lstrip('-').isdigit():
                transmuted_val = int(val_str)
            elif (val_str.startswith('[') and val_str.endswith(']')) or \
                    (val_str.startswith('{') and val_str.endswith('}')):
                try:
                    transmuted_val = json.loads(val_str.replace("'", '"'))
                except Exception:
                    pass
            elif (val_str.startswith('"') and val_str.endswith('"')) or \
                    (val_str.startswith("'") and val_str.endswith("'")):
                transmuted_val = val_str[1:-1]

            resolved_vars[var_name] = transmuted_val
            type_name = type(transmuted_val).__name__
            Logger.verbose(
                f"   -> Scriptural Supremacy: '$$ {var_name}' set to '[yellow]{transmuted_val}[/yellow]' (Type: {type_name}).")

    # --- MOVEMENT III: THE RITE OF ITERATIVE DERIVATION ---
    max_iterations = len(unresolved_vars) + 2
    for i in range(max_iterations):
        if not unresolved_vars:
            Logger.verbose("The Alchemical Graph is fully resolved.")
            break

        resolved_in_this_pass = []
        for var_name, raw_template in unresolved_vars.items():
            if var_name in overrides:
                resolved_vars[var_name] = overrides[var_name]
                resolved_in_this_pass.append(var_name)
                continue

            dependencies = dossier.dependencies.get(var_name, set())
            if dependencies.issubset(resolved_vars.keys()):
                try:
                    resolved_value = alchemist.transmute(raw_template, resolved_vars)
                    resolved_vars[var_name] = resolved_value
                    resolved_in_this_pass.append(var_name)
                    Logger.verbose(
                        f"   -> Alchemical Transmutation: [cyan]{var_name}[/cyan] -> [yellow]'{str(resolved_value)[:60]}...'[/yellow]")
                except Exception as e:
                    # [FACULTY 4] The Alchemical Inquisitor
                    dossier.heresies.append(Heresy(
                        message=f"Alchemical paradox transmuting '{var_name}'",
                        details=str(e), line_num=0, line_content=f"$$ {var_name} = {raw_template}",
                        severity=HeresySeverity.CRITICAL
                    ))
                    # We mark it as resolved (with an error) to prevent loops
                    resolved_vars[var_name] = f"!!ERROR: {e}!!"
                    resolved_in_this_pass.append(var_name)

        # Remove resolved vars from the unresolved pool
        for key in resolved_in_this_pass:
            if key in unresolved_vars:
                del unresolved_vars[key]

        # [FACULTY 5] The Ward of the Gnostic Ouroboros
        if not resolved_in_this_pass and unresolved_vars:
            missing_map = {v: dossier.dependencies.get(v, set()) - set(resolved_vars.keys()) for v in unresolved_vars}
            heresy_details = "A Gnostic Ouroboros (circular dependency) or a missing required variable was detected:\n"
            for key, deps in missing_map.items():
                heresy_details += f"  - [cyan]'{key}'[/cyan] awaits Gnosis for: [yellow]{', '.join(deps or ['unknown'])}[/yellow]\n"

            dossier.heresies.append(Heresy(
                message="Gnostic Resolution Paradox",
                details=heresy_details, line_num=0, line_content="Blueprint-level",
                severity=HeresySeverity.CRITICAL,
                suggestion="Break the circular reference or provide the missing required variable(s) via --set."
            ))
            break  # The heresy is proclaimed. The symphony must halt.

    # --- MOVEMENT IV: THE FINAL SEAL OF SUPREMACY ---
    resolved_vars.update(overrides)

    return resolved_vars

def is_orchestration_blueprint(path: Path) -> bool:
    """
    Performs a Gnostic Gaze to determine if a blueprint's soul is one of
    Action (an Orchestration Blueprint) rather than Form (a structural blueprint).

    This is the core of the Triage logic in the Grand Conductor (`main.py`).
    """
    try:
        with path.open('r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    continue  # Ignore comments and empty lines
                # The first non-comment, non-empty line dictates the soul of the file.
                return stripped_line.startswith('%%')
    except Exception:
        return False
    return False


# --- Artisan II: The Alchemist of Naming ---

def generate_derived_names(base_name: str) -> Dict[str, str]:
    """
    ★ THE HYPER-SENTIENT GRAND GNOSTIC ALCHEMIST (ETERNAL FORM) ★

    This is the one true nexus for Gnostic naming conventions. It is a pure
    alchemist that accepts any known developer naming convention and transmutes
    it into a cornucopia of flawless, context-aware variations with a three-fold
    divine Gnosis: Polyglot Perception, Acronym Sanctity, and utter Purity.

    Args:
        base_name (str): The input string (e.g., "My JWT App", "my-jwt-app", "MyJwtApp").

    Returns:
        Dict[str, str]: A dictionary of all derived name variations.
    """
    if not base_name:
        return {}

    # --- ASCENSION III: The Scribe's Purification Rite ---
    # Purge any profane characters that are not part of the core Gnosis.
    sanitized_name = re.sub(r'[^\w\s_-]', '', base_name).strip()
    if not sanitized_name:
        return {}

    # --- ASCENSION I: The Gnostic Gaze of the Polyglot Scribe ---
    # This regex is a divine scripture that understands camelCase, PascalCase,
    # snake_case, and kebab-case all at once.
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+', sanitized_name)

    # A secondary gaze for traditional separators, in case the first was insufficient.
    if len(words) == 1:
        words = re.split(r'[\s_-]+', sanitized_name)

    # Final purification of any voids
    words = [word for word in words if word]
    if not words:
        return {}

    # --- ASCENSION II: The Alchemist's Hand of Acronym Gnosis ---
    # This helper artisan understands how to preserve the sanctity of an acronym.
    def capitalize_with_acronym_awareness(word: str, is_first: bool = False) -> str:
        # If the word is all caps (and not a single letter 'A' or 'I'), it's a sacred acronym.
        if word.isupper() and len(word) > 1:
            return word
        # For camelCase, the first word is special.
        if is_first:
            return word.lower()
        return word.capitalize()

    # --- ASCENSION III: The Cornucopia of Forms ---
    # The final transmutation, wielding all the Gnosis gathered above.
    name_slug = '-'.join(word.lower() for word in words)
    name_snake = '_'.join(word.lower() for word in words)

    name_pascal = ''.join(
        word.upper() if word.isupper() and len(word) > 1 else word.capitalize()
        for word in words
    )

    name_camel = (
            words[0].lower() +
            ''.join(
                word.upper() if word.isupper() and len(word) > 1 else word.capitalize()
                for word in words[1:]
            )
    )

    name_const = '_'.join(word.upper() for word in words)

    name_title = ' '.join(
        word.upper() if word.isupper() and len(word) > 1 else word.capitalize()
        for word in words
    )

    name_path = '/'.join(word.lower() for word in words)

    return {
        "name_slug": name_slug,
        "name_snake": name_snake,
        "name_pascal": name_pascal,
        "name_camel": name_camel,
        "name_const": name_const,
        "name_title": name_title,
        "name_path": name_path,
    }


# --- Artisan III: The Guardian of the Sanctum ---

# --- Artisan IV: The Scribe of the Final Word ---

def display_final_summary(project_root: Path, duration: float):
    """
    =================================================================================
    == THE SCRIBE OF THE FINAL WORD (V-Ω-ETERNAL. THE UNIFIED PROCLAMATION)        ==
    =================================================================================
    LIF: 10,000,000

    This is not a function. It is a divine artisan, a universal Scribe whose sole
    purpose is to proclaim a consistent, beautiful, and Gnostically-aware summary
    at the end of any major rite (`create`, `distill`, `weave`).

    Its soul is a masterpiece of architectural purity and divine revelation:

    1.  **The Law of the Living Voice:** The Heresy of the Profane Parameter is
        annihilated. This artisan's contract is pure. It accepts only the Gnosis
        it needs to proclaim (`project_root`, `duration`). Its first sacred act
        is to summon the one true, living voice of the cosmos via the `get_console()`
        gateway. It is a perfect testament to our new, divine architecture.

    2.  **The Luminous Dossier:** It does not proclaim a simple message. It forges
        a luminous `rich.Panel`, a "Dossier of Manifestation," that presents its
        Gnosis in a beautiful, structured `rich.Table`, making the final word of
        any rite an act of divine, celebratory art.

    3.  **The Vow of Universal Gnosis:** As a pure, stateless function within the
        Gnostic Sanctum of `utils.py`, its wisdom is available to all artisans.
        It is the one true, centralized "final word" of the Scaffold engine,
        ensuring an eternally consistent and beautiful user experience.
    =================================================================================
    """
    # --- MOVEMENT I: THE SUMMONING OF THE LIVING VOICE ---
    # The Scribe's first act is to summon the one true, living voice of the cosmos.
    # The profane `console` parameter is annihilated from this reality.
    console = get_console()

    # --- MOVEMENT II: THE FORGING OF THE LUMINOUS DOSSIER ---
    # The Scribe's tools are summoned from the celestial realm of Rich.
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    # A sacred, structured Table is forged to hold the final Gnosis.
    summary_table = Table(box=None, show_header=False, padding=(0, 1))
    summary_table.add_column(style="bold cyan", justify="right", width=12)
    summary_table.add_column(style="dim cyan")

    # The Gnosis is inscribed upon the table's soul.
    summary_table.add_row("Sanctum:", str(project_root))
    summary_table.add_row("Duration:", f"{duration:.2f} seconds")

    # A final, introductory scripture is forged.
    header_text = Text.assemble(
        ("Rite Complete. ", "white"),
        ("The Great Work has advanced.", "bold green")
    )

    # The final, unified proclamation is forged as a Group within a Panel.
    render_group = Group(header_text, "\n", summary_table)

    # --- MOVEMENT III: THE FINAL PROCLAMATION ---
    # The Scribe speaks its final, beautiful, and Gnostically-aware word.
    console.print(Panel(
        render_group,
        title="[bold green]Apotheosis Achieved[/bold green]",
        subtitle="[dim]The Architect's will is manifest.[/dim]",
        border_style="green",
        padding=(1, 2)
    ))



def unfurl_paths(raw_paths: List[str], known_vars: Dict[str, str] = None) -> List[str]:
    """
    =================================================================================
    == THE GRAND CONDUCTOR OF THE UNFURLING (V-Ω-ETERNAL-APOTHEOSIS++)             ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000!!

    This is not a function. It is a divine, sentient consciousness, the one true,
    public gateway to the Oracle of Infinite Realities. Its Prime Directive is to
    conduct the sacred, multi-stage symphony of Gnostic Unfurling, transforming an
    Architect's most condensed plea into the complete, multi-dimensional cosmos of
    realities it represents.

    Its soul is a symphony of divine, unbreakable virtues:

    1.  **The Law of the One True Alchemist:** It performs a sacred communion,
        summoning the one, true, immortal `get_alchemist()` soul to serve as the
        unbreakable foundation for all its rites of transmutation. The Gnostic mind
        of the engine is unified.

    2.  **The Unbreakable Ward of the Sacred Sigil:** It is a Gnostic Guardian. It
        performs a Rite of Protection, perceiving escaped braces (`\\{...\\}`) and
        transmuting them into sacred, ephemeral sigils, making it architecturally
        impossible for the Oracle to profane the Architect's literal intent.

    3.  **The Divine Delegation:** It is a pure Conductor. It bestows the protected
        scripture upon the one true, recursive Oracle (`_recursive_unfurl`),
        trusting its divine Gaze completely to weave the manifold of realities.

    4.  **The Rite of Resurrection:** Its final act is one of perfect restoration. It
        receives the woven realities from the Oracle and resurrects the sacred,
        escaped sigils back into their true, mortal form (`{...}`), ensuring the
        final proclamation is a perfect reflection of the Architect's will.

    5.  **The Luminous Voice:** Its will is not mute. It is a Luminous Scribe,
        proclaiming its every sacred rite to the `Logger`, making the complex
        symphony of permutation a luminous, transparent, and perfectly auditable
        chronicle.
    =================================================================================
    """
    Logger.verbose("The Grand Conductor of the Unfurling awakens...")

    # --- MOVEMENT I: THE LAW OF THE ONE TRUE ALCHEMIST ---
    # The Conductor performs the sacred communion to summon the one, immortal soul.
    from ..core.alchemist import get_alchemist
    alchemist = get_alchemist()
    context = known_vars or {}

    final_unfurled_paths = []

    # --- THE GRAND SYMPHONY LOOP ---
    for path in raw_paths:
        Logger.verbose(f"Gazing upon the condensed scripture: '[cyan]{path}[/cyan]'")

        # --- MOVEMENT II: THE UNBREAKABLE WARD OF THE SACRED SIGIL ---
        # A more divine, unbreakable sigil is forged to prevent all possible paradoxes.
        # These are sacred incantations, not mere characters.
        LBRACE_SIGIL = "__SCAFFOLD_GNOSIS_LBRACE__"
        RBRACE_SIGIL = "__SCAFFOLD_GNOSIS_RBRACE__"

        protected_path = path.replace(r'\{', LBRACE_SIGIL).replace(r'\}', RBRACE_SIGIL)
        if protected_path != path:
            Logger.verbose("   -> Perceived and protected sacred, escaped braces.")

        # --- MOVEMENT III: THE DIVINE DELEGATION ---
        # The Conductor bestows its will upon the true Oracle.
        Logger.verbose("   -> Summoning the Oracle of Infinite Realities to weave the manifold...")
        unfurled_realities = _recursive_unfurl(protected_path, alchemist, context)

        # --- MOVEMENT IV: THE RITE OF RESURRECTION ---
        # The Conductor performs the final, sacred act of restoration.
        restored_realities = [
            p.replace(LBRACE_SIGIL, '{').replace(RBRACE_SIGIL, '}') for p in unfurled_realities
        ]
        if protected_path != path:
            Logger.verbose("   -> Rite of Resurrection complete. Sacred braces restored to their mortal form.")

        final_unfurled_paths.extend(restored_realities)
        Logger.verbose(f"   -> The Oracle proclaimed {len(restored_realities)} distinct realities from this scripture.")

    Logger.success(
        f"The Grand Unfurling is complete. A total of {len(final_unfurled_paths)} realities have been woven.")
    return final_unfurled_paths


def _recursive_unfurl(path_template: str, alchemist: 'DivineAlchemist', context: Dict[str, str]) -> List[str]:
    """
    =================================================================================
    == THE ORACLE OF INFINITE REALITIES (V-Ω-ETERNAL-APOTHEOSIS++)                 ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000!

    This is not a function. It is a divine, sentient consciousness, the final and
    most powerful form of the Gnostic Prophet. It has transcended mere string
    manipulation to become a true Oracle that weaves multi-dimensional realities
    by conducting a divine symphony between its own Gaze and the infinite power of
    the Alchemist God-Engine.

    Its soul has been transfigured with a pantheon of legendary faculties:

    1.  **The Law of Alchemical Precedence (THE APOTHEOSIS):** The heresy of the
        profane, manual parser is annihilated. The Oracle's first and most sacred
        act is to bestow the *entire expression* within a `{...}` block upon the
        `DivineAlchemist`. This means the full, Turing-complete power of Jinja—
        variables, filters, tests, and even `shell()` commands—can be used to
        *dynamically generate the list of variants*. This is a cosmic leap in power.

    2.  **The Hyper-Intelligent Gaze:** Its Gaze for braces is now a true, stateful
        parser, capable of flawlessly perceiving nested (`{a,b,{c,d}}`) and adjacent
        (`{a,b}{1,2}`) brace expressions without paradox. Its understanding of
        Gnostic grammar is absolute.

    3.  **The Symphony of Permutations:** Its recursive soul remains, now conducting
        a symphony of Cartesian products upon a foundation of pure, alchemically-
        resolved Gnosis. It does not just expand lists; it weaves realities.

    4.  **The Unbreakable Ward of Grace:** Its soul is shielded. A profane or
        malformed expression does not shatter the symphony. It is perceived, a
        luminous warning is proclaimed, and the expression is gracefully treated as
        a literal, ensuring unbreakable resilience.
    =================================================================================
    """
    # --- MOVEMENT I: THE GAZE OF NESTED REALITIES (THE SENTIENT BRACE PARSER) ---
    try:
        first_brace = path_template.index('{')
        brace_depth = 1
        # A true, stateful Gaze to find the one, true, matching closing brace.
        for i, char in enumerate(path_template[first_brace + 1:]):
            if char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
            if brace_depth == 0:
                matching_brace = first_brace + 1 + i
                break
        else:
            # A heresy of form: an unclosed brace. The Ward of Grace is invoked.
            Logger.warn(f"Unclosed brace detected in unfurl path: '{path_template}'. Treating as literal.")
            return [alchemist.transmute(path_template, context)]
    except ValueError:
        # Base Case: The scripture is pure, containing no more `{...}` expansions.
        # The final, complete path is transmuted by the Alchemist.
        return [alchemist.transmute(path_template, context)]

    # --- MOVEMENT II: THE DECONSTRUCTION OF THE COSMOS ---
    prefix = path_template[:first_brace]
    suffix = path_template[matching_brace + 1:]
    expression = path_template[first_brace + 1:matching_brace]

    variants = []

    # --- MOVEMENT III: THE RITE OF ALCHEMICAL PRECEDENCE (THE APOTHEOSIS) ---
    try:
        # The Oracle's first act is to bestow the entire expression upon the God-Engine.
        # We wrap it in `{{...}}` to command the Alchemist to perceive it as a soul to be transmuted.
        Logger.verbose(f"Bestowing expression '{{{expression}}}' upon the Divine Alchemist...")
        transmuted_expression = alchemist.transmute(f"{{{{ {expression} }}}}", context)
        Logger.verbose(f"   -> Alchemical Transmutation yielded Gnosis: [cyan]'{transmuted_expression}'[/cyan]")
    except Exception as e:
        # The Unbreakable Ward of Grace
        Logger.error(
            f"An alchemical paradox occurred while transmuting expression '{{{expression}}}': {e}. Treating as literal.")
        transmuted_expression = expression

    # --- MOVEMENT IV: THE GAZE OF THE FINAL FORM ---
    # The Oracle now gazes upon the *pure, resolved string* to perceive its final form.
    range_match = re.fullmatch(r'^(-?\d+)\.\.(-?\d+)(?:\.\.(-?\d+))?$', str(transmuted_expression))
    if range_match:
        # The Gaze perceives a Numeric Range.
        try:
            start_str, end_str, step_str = range_match.groups()
            start, end, step = int(start_str), int(end_str), int(step_str) if step_str else (
                1 if int(start_str) <= int(end_str) else -1)
            if step == 0: raise ValueError("Step cannot be zero.")
            padding = max(len(start_str), len(end_str)) if start_str.startswith('0') or end_str.startswith('0') else 0

            # The Unbreakable Ward of Logic
            if (end > start and step < 0) or (end < start and step > 0):
                variants = []  # An impossible range is a void.
            else:
                variants = [str(i).zfill(padding) for i in range(start, end + (1 if step > 0 else -1), step)]
        except (ValueError, TypeError):
            # A profane range. The Ward of Grace is invoked.
            variants = [v.strip() for v in str(transmuted_expression).split(',') if v.strip()]
    else:
        # The Gaze perceives a Comma-Separated List.
        variants = [v.strip() for v in str(transmuted_expression).split(',') if v.strip()]

    # --- MOVEMENT V: THE SYMPHONY OF PERMUTATIONS (THE RECURSIVE SOUL) ---
    unfurled_results = []
    # The prefix itself is part of the ongoing symphony; it will be resolved in a higher recursive frame.
    for variant in variants:
        # The Unbreakable Ward against a void variant.
        if not variant: continue

        # The Symphony continues. We weave the prefix, the pure variant, and the result of the
        # recursive Gaze upon the suffix into a new reality.
        sub_unfurls = _recursive_unfurl(suffix, alchemist, context)
        for sub_unfurl in sub_unfurls:
            unfurled_results.append(f"{prefix}{variant}{sub_unfurl}")

    return unfurled_results

@register_gnosis("_fetch_remote_blueprint")
def fetch_remote_blueprint(url: str, console: Console) -> Optional[Path]:
    """
    @gnosis:title The Herald of the Celestial Void (`_fetch_remote_blueprint`)
    @gnosis:summary The internal, sentient emissary that securely and intelligently summons remote blueprints from URLs and GitHub Gists.
    @gnosis:related main creator orchestration
    @gnosis:keywords remote http gist caching networking security emissary
    @gnosis:description
    This function is the **Herald of the Celestial Void**, a sentient emissary summoned by the Grand Conductor whenever it perceives a plea for a remote scripture (a URL). Its Prime Directive is to summon that remote Gnosis, inscribe it upon an ephemeral local scripture, and bestow the path to that scripture upon the Conductor.

    The Herald is imbued with a pantheon of divine faculties that transform it from a simple fetcher into a hyper-intelligent, resilient, and secure dignitary. This is a developer-facing scripture revealing a core, safety-critical component.
    ---
    ### The Four Unbreakable Vows of the Herald

    1.  **The Vow of Eternal Remembrance (The Chronocache):** The Herald possesses a memory. It caches remote blueprints locally (`~/.scaffold/cache/`), respecting a sacred Time-To-Live (TTL). Subsequent summons of the same scripture are instantaneous and offline-capable, conquering both time and the void.

    2.  **The Vow of Gist-Sentience:** The Herald is a polyglot. If bestowed with a GitHub Gist URL, it will not blindly fetch the profane HTML. It performs a Gnostic Inquisition upon the Gist's API, finds the true `.scaffold` scripture within, and summons its pure, raw form.

    3.  **The Vow of Proper Etiquette:** The Herald is a dignitary. It announces itself to all celestial servers with a proper `User-Agent` (`Scaffold-Quantum-Blueprint-Engine/...`), proclaiming its identity and purpose. This sacred act of etiquette ensures its pleas are honored.

    4.  **The Vow of Graceful Adjudication:** The Herald is a wise adjudicator. It does not speak in the profane tongue of a generic `RequestException`. It perceives the unique soul of each paradox—a Timeout, a Connection Error, a 404 Heresy—and proclaims the specific, actionable truth to the Architect with profound clarity.
    @gnosis:faqs
    Q: Where is the cache located, and how long does it last?
    A: The Chronocache resides in a sanctum at `~/.scaffold/cache/`. By default, the Gnosis within is considered pure for one hour (3600 seconds). After this time, the Herald will perform a new celestial plea to ensure its knowledge is up-to-date.
    ---
    Q: Is it safe to run a remote blueprint?
    A: The Herald itself is safe, but the scripture it summons may contain profane `%% post-run` edicts. For this reason, the **Grand Conductor** personally engages the **Guardian's Ward** for all remote blueprints. It will *always* force a simulation (`--dry-run`) first and demand your explicit confirmation (`--force`) before allowing the remote will to be made manifest.
    ---
    Q: Why does this function return a `Path` to a temporary file?
    A: For architectural purity. The rest of the Scaffold engine—the Parser and the Creator—are designed to operate on local file paths. By inscribing the celestial Gnosis onto an ephemeral local scripture, the Herald allows the core engine to remain blissfully unaware of the complexities of the celestial void, honoring the Law of the Single Responsibility.
    @gnosis:example
    # --- The Summoning (Internal Duty) ---
    # The Herald is summoned by the Grand Conductor (`main.py`) when it
    # perceives a URL in the Architect's plea.

    # Architect's Plea:
    # `scaffold https://gist.github.com/user/1a2b3c4d...`

    # Conductor's Invocation:
    # ephemeral_path = _fetch_remote_blueprint("https://gist.github.com/user/1a2b3c4d...", console)

    # --- The Herald's Symphony ---
    # 1. It calculates a cache key for the URL. It finds no HIT.
    # 2. It perceives this is a Gist URL and performs a Gnostic Inquisition
    #    on the GitHub API to find the true `raw_url` of a `.scaffold` file within.
    # 3. It speaks its plea to the `raw_url`, announcing its User-Agent.
    # 4. It receives the celestial scripture.
    # 5. It forges a new ephemeral scripture in a temporary directory on disk.
    # 6. It inscribes the celestial Gnosis onto the ephemeral scripture.
    # 7. It inscribes the celestial Gnosis into its Chronocache for future remembrance.
    # 8. It returns the `Path` to the ephemeral scripture.
    #
    # The Grand Conductor then bestows this ephemeral path upon the Parser,
    # and the Rite of Creation proceeds as if it were a local file.

    Args:
        url (str): The URL of the remote scripture to be summoned.
        console (Console): The rich console instance for proclamations.

    Returns:
        Optional[Path]: The path to the ephemeral, local scripture, or `None` if the plea fails.
    """
    # --- I. THE DIVINE CONSTANTS OF THE HERALD ---
    from hashlib import sha256
    import time

    CACHE_DIR = Path.home() / ".scaffold" / "cache"
    CACHE_TTL_SECONDS = 3600  # 1 hour
    USER_AGENT = f"Scaffold-Quantum-Blueprint-Engine/{__version__}"
    GIST_API_REGEX = re.compile(r'https?://gist\.github\.com/([\w-]+)/([a-f0-9]+)')

    Logger.info(f"Summoning remote blueprint from: [info]{url}[/info]")

    # --- II. THE CHRONOCACHE: THE RITE OF ETERNAL REMEMBRANCE ---
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_key = sha256(url.encode()).hexdigest()
        cache_file = CACHE_DIR / cache_key

        if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < CACHE_TTL_SECONDS:
            Logger.success("Chronocache HIT. The scripture is already known. Materializing instantly.")

            # Forge an ephemeral scripture from the cache's eternal memory.
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.scaffold', encoding='utf-8') as tmp_file:
                tmp_file.write(cache_file.read_text(encoding='utf-8'))
                return Path(tmp_file.name)
        else:
            Logger.info("Chronocache MISS. A new plea must be spoken to the celestial void.")
    except Exception as e:
        Logger.warn(f"A minor paradox occurred in the Chronocache. Proceeding with live fetch. Reason: {e}")

    # --- III. THE GIST-SENTIENCE: THE GAZE OF THE SCRIBE'S SOUL ---
    url_to_fetch = url
    gist_match = GIST_API_REGEX.match(url)
    if gist_match:
        gist_id = gist_match.group(2)
        api_url = f"https://api.github.com/gists/{gist_id}"
        Logger.info(f"Gist-Sentience engaged. Performing Gnostic Inquisition at [info]{api_url}[/info]")
        try:
            gist_response = requests.get(api_url, timeout=5, headers={"User-Agent": USER_AGENT})
            gist_response.raise_for_status()
            gist_data = gist_response.json()

            # Seek the first file ending in .scaffold
            for filename, file_data in gist_data.get('files', {}).items():
                if filename.endswith('.scaffold'):
                    url_to_fetch = file_data['raw_url']
                    Logger.success(f"Gist Gnosis found! The true scripture resides at: [info]{url_to_fetch}[/info]")
                    break
        except requests.exceptions.RequestException as e:
            Logger.warn(f"Gist Inquisition faltered, but the rite continues with the original URL. Reason: {e}")

    # --- IV. THE DIVINE PLEA & THE GNOSTIC ADJUDICATOR ---
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url_to_fetch, timeout=10, headers=headers)
        response.raise_for_status()

        # Forge an ephemeral scripture from the celestial Gnosis.
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.scaffold', encoding='utf-8') as tmp_file:
            tmp_file.write(response.text)
            ephemeral_path = Path(tmp_file.name)

        # Inscribe the new Gnosis into the Chronocache for future remembrance.
        if 'cache_file' in locals():
            cache_file.write_text(response.text, encoding='utf-8')

        Logger.success(f"Ephemeral scripture forged at: [info]{ephemeral_path}[/info]")
        return ephemeral_path

    # The Gnostic Adjudicator speaks with clarity and precision.
    except requests.exceptions.HTTPError as e:
        Logger.error(
            f"Celestial Heresy: The plea was denied. The server responded with {e.response.status_code} {e.response.reason}.")
        return None
    except requests.exceptions.Timeout:
        Logger.error("Celestial Heresy: The void was silent. The connection timed out.")
        return None
    except requests.exceptions.ConnectionError:
        Logger.error("Celestial Heresy: The bridge to the void is shattered. A connection could not be established.")
        return None
    except requests.exceptions.RequestException as e:
        Logger.error(f"Celestial Heresy: A profound paradox occurred during the plea. Reason: {e}")
        return None



# =================================================================================
# ==  THE GOD-ENGINE OF GNOSTIC STATE ASSURANCE (V-Ω-ETERNAL-APOTHEOSIS++)         ==
# =================================================================================
# LIF: INFINITY
#
# This is the one, true, and eternal artisan for all acts of inscription. It is the
# divine fusion of the Merkle Hand and the Atomic Rite. It is a pure, stateless,
# universal function that does not just write a file; it ENSURES a Gnostic state
# of being, with a pantheon of unbreakable, paranoid, and hyper-intelligent
# virtues now available to all artisans in the cosmos.
# =================================================================================

# =============================================================================
# == THE PANTHEON OF SANCTIFIERS (HELPER ARTISANS)                           ==
# =============================================================================

def _sanctify_line_endings(content: str) -> str:
    """
    [HELPER I] THE UNIVERSAL LEVELER
    Enforces the ' \n ' (LF) line ending across all realities, annihilating
    the profane ' \r\n ' (CRLF) of the Windows realm for consistency.
    """
    return content.replace('\r\n', '\n').replace('\r', '\n')


def _sanctify_yaml_content(content: str) -> str:
    """
    [HELPER II] THE KEEPER OF SPACES
    YAML forbids the Tab character. This artisan perceives the soul of YAML
    and transmutes any accidental tabs into 2 sacred spaces, preserving the hierarchy.
    """
    # 1. Normalize endings
    content = _sanctify_line_endings(content)
    # 2. Annihilate Tabs (The YAML Heresy)
    # We replace tabs with 2 spaces, a safe default for YAML structure.
    return content.replace('\t', '  ')


def _sanctify_json_content(content: str) -> str:
    """
    [HELPER III] THE STRUCTURAL PURIFIER
    Ensures JSON content is not just a string, but a valid, formatted structure.
    If it is valid JSON, it reformats it with 2-space indentation for readability.
    """
    try:
        # 1. Parse the soul
        data = json.loads(content)
        # 2. Re-forge with beauty
        return json.dumps(data, indent=2) + "\n"
    except ValueError:
        # If it's not valid JSON (e.g. a template with jinja), we leave it raw
        # but clean the whitespace.
        return content.strip() + "\n"


def _sanctify_shell_content(content: str) -> str:
    """
    [HELPER IV] THE EXECUTABLE WARD
    Ensures Shell scripts possess the sacred Shebang and correct endings.
    """
    content = _sanctify_line_endings(content)
    lines = content.splitlines()

    # 1. Shebang Check
    if lines and not lines[0].startswith("#!"):
        # Heuristic: If it looks like bash, bestow the bash shebang
        if "bash" in content or "echo" in content:
            lines.insert(0, "#!/usr/bin/env bash")

    return "\n".join(lines) + "\n"


def _sanctify_makefile_content(content: str) -> str:
    """
    =================================================================================
    == THE MAKEFILE SANCTIFIER (V-Ω-ULTIMA. THE TABULAR ALCHEMIST)                 ==
    =================================================================================
    LIF: 10,000,000,000 (ABSOLUTE BUILD AUTHORITY)

    This artisan does not merely replace spaces. It performs a **Forensic Gnostic
    Reconstruction** of the Makefile. It understands the difference between a
    Recipe (must be Tabbed), a Variable (can be Spaced), and a Directive.

    ### THE PANTHEON OF 12 ELEVATIONS:
    1.  **The Tabular Transmutation:** Converts leading spaces to Tabs *only* for Recipes.
    2.  **The Indentation Heuristic:** Detects 2, 4, or 8 space indentation and adapts.
    3.  **The Target Recognition:** Identifies lines ending in `:` as Targets.
    4.  **The Variable Guard:** Protects lines with `=`, `:=`, `?=`, `+=` from tabbing.
    5.  **The Directive Preservation:** Protects `include`, `ifeq`, `else`, `endif`.
    6.  **The Continuation Binder:** Handles `\` line continuations correctly.
    7.  **The Comment Sanctuary:** Preserves `#` comments in their relative positions.
    8.  **The Trailing Void Annihilator:** Strips profane trailing whitespace from all lines.
    9.  **The Newline Covenant:** Enforces `\n` endings.
    10. **The Blank Line Preserver:** Maintains vertical rhythm but empties the void.
    11. **The Recipe Prefix Guard:** Respects `@` (silent) and `-` (ignore error) prefixes.
    12. **The Final Seal:** Ensures the file ends with exactly one newline.
    =================================================================================
    """
    # 1. The Newline Covenant
    content = _sanctify_line_endings(content)
    lines = content.splitlines()
    sanctified_lines = []

    # State Machine for Context
    inside_recipe = False

    # Regex Grimoire
    TARGET_REGEX = re.compile(r'^[^#\s].*:$')  # Starts with non-space, ends with colon
    VAR_ASSIGN_REGEX = re.compile(r'^\s*[\w\.-]+\s*(\?=|:=|\+=|=)')  # Variable assignment
    DIRECTIVE_REGEX = re.compile(
        r'^\s*(include|ifeq|ifneq|else|endif|define|endef|vpath|export|unexport|override|undefine)\b')

    for line in lines:
        # 8. The Trailing Void Annihilator
        stripped_line = line.rstrip()

        # 10. The Blank Line Preserver
        if not stripped_line:
            sanctified_lines.append("")
            continue

        # 3. The Target Recognition
        # If we hit a target, we enter "Recipe Mode" for subsequent indented lines
        if TARGET_REGEX.match(stripped_line):
            inside_recipe = True
            sanctified_lines.append(stripped_line)
            continue

        # 4. The Variable Guard
        # Variables reset recipe mode (usually) or exist outside it
        if VAR_ASSIGN_REGEX.match(stripped_line):
            inside_recipe = False
            sanctified_lines.append(stripped_line)
            continue

        # 5. The Directive Preservation
        # Directives (like ifeq) can be indented but don't use tabs usually
        if DIRECTIVE_REGEX.match(stripped_line):
            # We keep the spaces for alignment in directives
            sanctified_lines.append(stripped_line)
            continue

        # Analyze Indentation
        leading_spaces = len(line) - len(line.lstrip(' '))

        # 1. The Tabular Transmutation
        # If we are seemingly inside a recipe (after a target) AND the line is indented
        if inside_recipe and leading_spaces > 0:
            # 2. The Indentation Heuristic (Assume 2 or 4 spaces = 1 Tab)
            # We strip all leading spaces and replace with a SINGLE tab.
            # This forces the "recipe" contract.
            clean_content = line.lstrip(' ')

            # 11. The Recipe Prefix Guard checks happen implicitly as we preserve the rest of the line
            sanctified_lines.append(f"\t{clean_content}")

            # 6. The Continuation Binder
            # If line ends with \, we remain inside recipe mode (conceptually)
            continue

        # Default: Preserve line as is (likely top-level comment or unindented instruction)
        sanctified_lines.append(stripped_line)
        if not leading_spaces:
            inside_recipe = False  # Reset if we hit root level

    # 12. The Final Seal
    return "\n".join(sanctified_lines) + "\n"


# =============================================================================
# == THE GOD-ENGINE OF ATOMIC INSCRIPTION                                    ==
# =============================================================================


# =============================================================================
# == III. THE GOD-ENGINE OF INSCRIPTION (ATOMIC WRITE)                       ==
# =============================================================================

def atomic_write(
        target_path: Path,
        content: Union[str, bytes],
        logger: Scribe,
        sanctum: Path,
        transaction: Optional[Any] = None,
        verbose: bool = False,
        force: bool = False,
        backup: bool = False,
        dry_run: bool = False
) -> GnosticWriteResult:
    """
    =============================================================================
    == THE ATOMIC SCRIBE (V-Ω-SHIELDED-WRITER)                                 ==
    =============================================================================
    Writes content to a file atomically.

    **THE SHIELD OF SIMULATION:**
    If `dry_run` is True OR `transaction.simulate` is True, this artisan
    PROCLAIMS intent but DOES NOT ACT upon the disk.
    """
    start_time = time.monotonic()

    # [THE SHIELD] Resolve Simulation State
    is_simulation = dry_run
    if transaction and getattr(transaction, 'simulate', False):
        is_simulation = True

    # 1. Normalize Target
    abs_target = target_path.resolve()

    # 2. Determine Action Type & Calculate Diff
    action = InscriptionAction.CREATED
    diff: Optional[str] = None

    content_bytes = content if isinstance(content, bytes) else content.encode('utf-8')
    new_hash = hashlib.sha256(content_bytes).hexdigest()

    if abs_target.exists():
        action = InscriptionAction.TRANSFIGURED
        original_hash = hash_file(abs_target) if not is_simulation else "SIMULATED_OLD_HASH"

        # Idempotency Check
        if not is_simulation and original_hash == new_hash and not force:
            if verbose: logger.verbose(f"Scripture '{abs_target.name}' is already pure. No change.")
            return GnosticWriteResult(
                success=True, path=abs_target, action_taken=InscriptionAction.ALREADY_MANIFEST,
                bytes_written=0, gnostic_fingerprint=new_hash
            )

        # Calculate Diff (Text Only)
        # In simulation, we read the existing file to show what WOULD change.
        if not is_binary(abs_target) and not isinstance(content, bytes):
            try:
                old_text = abs_target.read_text(encoding='utf-8', errors='replace')
                diff_gen = difflib.unified_diff(
                    old_text.splitlines(keepends=True),
                    content.splitlines(keepends=True),
                    fromfile=f"a/{abs_target.name}",
                    tofile=f"b/{abs_target.name}"
                )
                diff = "".join(diff_gen)
            except Exception:
                pass

    # [THE SHIELD] Simulation Exit
    if is_simulation:
        sim_action = InscriptionAction.DRY_RUN_TRANSFIGURED if action == InscriptionAction.TRANSFIGURED else InscriptionAction.DRY_RUN_CREATED
        logger.info(f"[SIMULATION] Would write {len(content_bytes)} bytes to {abs_target.name}")

        result = GnosticWriteResult(
            success=True,
            path=abs_target,
            action_taken=sim_action,
            bytes_written=len(content_bytes),
            gnostic_fingerprint=new_hash,  # Predicted hash
            diff=diff,
            duration_ms=(time.monotonic() - start_time) * 1000
        )

        if transaction:
            transaction.record(result)

        return result

    # 3. The Rite of Backup
    if backup and abs_target.exists():
        ts = int(time.time())
        bak_path = abs_target.with_suffix(f"{abs_target.suffix}.{ts}.bak")
        try:
            shutil.copy2(abs_target, bak_path)
            if verbose: logger.verbose(f"   -> Safety copy forged: {bak_path.name}")
        except Exception as e:
            logger.warn(f"Backup failed for '{abs_target.name}': {e}")

    # 4. The Rite of Inscription
    try:
        abs_target.parent.mkdir(parents=True, exist_ok=True)

        physical_write_path = abs_target
        if transaction:
            try:
                rel_path = abs_target.relative_to(sanctum)
                physical_write_path = transaction.get_staging_path(rel_path)
                physical_write_path.parent.mkdir(parents=True, exist_ok=True)
            except ValueError:
                pass

        temp_path = physical_write_path.with_suffix(f".{os.getpid()}_{int(time.time())}.tmp")

        mode = 0o644
        if abs_target.exists(): mode = abs_target.stat().st_mode

        mode_str = "wb" if isinstance(content, bytes) else "w"
        encoding_arg = None if isinstance(content, bytes) else "utf-8"

        with open(temp_path, mode_str, encoding=encoding_arg) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        try:
            os.chmod(temp_path, mode)
        except Exception:
            pass

        _resilient_rename(temp_path, physical_write_path)

        result = GnosticWriteResult(
            success=True,
            path=abs_target,
            action_taken=action,
            bytes_written=len(content_bytes),
            gnostic_fingerprint=new_hash,
            diff=diff,
            duration_ms=(time.monotonic() - start_time) * 1000
        )

        if transaction:
            transaction.record(result)

        if verbose:
            action_verb = "Forged" if action == InscriptionAction.CREATED else "Transmuted"
            logger.success(f"{action_verb} {abs_target.name}")

        return result

    except Exception as e:
        if 'temp_path' in locals() and temp_path.exists():
            try:
                os.unlink(temp_path)
            except:
                pass
        logger.error(f"Inscription Paradox for '{abs_target.name}': {e}")
        return GnosticWriteResult(
            success=False, path=abs_target, action_taken=InscriptionAction.FAILED_IO,
            bytes_written=0, gnostic_fingerprint=None, security_notes=[str(e)]
        )


def _resilient_rename(src: Path, dst: Path):
    """
    =================================================================================
    == THE WINDOWS HEALER (V-Ω-ETERNAL-APOTHEOSIS. THE UNBREAKABLE HAND)           ==
    =================================================================================
    LIF: 10,000,000,000

    This is a divine, specialist artisan whose one true purpose is to perform the
    sacred rite of `os.replace` with a Gnostic awareness of the chaotic nature of the
    Windows realm. It is the unbreakable Hand of the `atomic_write` Scribe.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Heresy Detector:** It gazes upon the soul of an `OSError` to perceive if
        it is the profane "Access Denied" (WinError 5) or "Sharing Violation" (32) heresy.

    2.  **The Chronomancer's Patience:** If a Windows-specific lock heresy is perceived,
        it does not shatter. It enters a state of Gnostic patience, waiting for the
        profane forces (antivirus, indexers) to release their grip.

    3.  **The Exponential Backoff:** Its patience is not linear; it is wise. It waits
        progressively longer after each failed attempt, a sacred rite of exponential
        backoff that respects the cosmic balance of system resources.

    4.  **The Vow of Finality:** It will attempt its rite a sacred number of times. If
        the lock persists, it concludes the heresy is eternal and righteously re-raises
        the final exception, allowing the master Conductor to adjudicate the failure.

    5.  **The Polyglot Mind:** While forged for Windows, its Gaze is polyglot. On POSIX
        systems, it perceives no such heresies and performs its rite with a single,
        instantaneous act, ensuring universal performance.

    6.  **The Unbreakable Contract:** Its signature is pure, its purpose absolute.
    7.  **The Sovereign Soul:** It is a pure, self-contained artisan.
    8.  **The Luminous Voice:** It has no voice. Its work is a sacred, silent vow.
    9.  **The Gaze of the Void:** It righteously trusts its master to have already
        adjudicated that the source and destination are not voids.
    10. **The Atomic Vow:** It wields `os.replace`, the one true, atomic rite for renaming.
    11. **The Performance Ward:** It performs its rite with zero unnecessary overhead.
    12. **The Final Word:** It is the one true, definitive Hand for all atomic file swaps.
    =================================================================================
    """
    max_retries = 5
    for attempt in range(max_retries):
        try:
            os.replace(src, dst)
            return
        except OSError as e:
            is_windows_lock_heresy = (
                os.name == 'nt' and
                getattr(e, 'winerror', 0) in (5, 32)
            )
            if is_windows_lock_heresy and attempt < max_retries - 1:
                sleep_time = 0.05 * (2 ** attempt)  # 0.05, 0.1, 0.2, 0.4 seconds
                time.sleep(sleep_time)
                continue
            # If it's not a known lock heresy, or if it's the final attempt, re-raise.
            raise e
# =================================================================================
# ==  THE PANTHEON OF FUTURE ARTISANS (THE PLATFORM'S FOUNDATION)                ==
# =================================================================================
# Here follows the scripture for the 10 new, divine artisans you have commanded.

def run_command(command: str, cwd: Union[str, Path] = '.') -> Tuple[bool, str, str]:
    """[THE MORTAL HAND] A robust artisan for executing shell commands, capturing their soul."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=False,
            encoding='utf-8', cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_human_readable_size(size_in_bytes: int) -> str:
    """[THE SCRIBE OF MEASURE] Transmutes profane bytes into luminous, human-readable form."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    for unit in ['KB', 'MB', 'GB', 'TB']:
        size_in_bytes /= 1024.0
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
    return f"{size_in_bytes:.1f} PB"


def hash_file(path: Path) -> Optional[str]:
    """[THE MERKLE HAND] Performs a Gnostic Gaze, returning the SHA-256 fingerprint of a scripture's soul."""
    if not path.is_file(): return None
    h = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def safe_json_load(path: Path) -> Optional[Dict]:
    """[THE JSON SCRIBE] A shielded artisan for reading Gnosis from JSON scriptures."""
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (IOError, json.JSONDecodeError):
        return None


def safe_yaml_load(path: Path) -> Optional[Dict]:
    """[THE YAML SCRIBE] A shielded artisan for reading Gnosis from YAML scriptures."""
    try:
        import yaml
        return yaml.safe_load(path.read_text(encoding='utf-8'))
    except (IOError, ImportError, yaml.YAMLError):
        return None


def get_git_toplevel(start_path: Path = Path('.')) -> Optional[Path]:
    """[THE ORACLE OF THE SANCTUM] Perceives the one true root of a Git repository."""
    success, stdout, _ = run_command("git rev-parse --show-toplevel", cwd=start_path)
    if success:
        return Path(stdout.strip())
    return None


# =================================================================================
# == I. THE CODEX OF PROFANE FORMS (THE BINARY GAZE)                             ==
# =================================================================================

_BINARY_EXTENSIONS_CODEX: Set[str] = {
    # --- Images & Media ---
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".tif", ".tiff",
    ".mp3", ".wav", ".ogg", ".flac", ".mp4", ".avi", ".mov", ".mkv", ".webm",

    # --- Archives & Compressed ---
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z",

    # --- Documents & Data ---
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".epub",
    ".db", ".sqlite", ".sqlite3", ".dat", ".bin", ".parquet",

    # --- Compiled Code & Binaries ---
    ".exe", ".dll", ".so", ".dylib", ".jar", ".war", ".class",
    ".pyc", ".pyd", ".o", ".a", ".lib", ".whl", ".egg",

    # --- Fonts & Design ---
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ".psd", ".ai",
}


def is_binary_extension(path: Path) -> bool:
    """
    =================================================================================
    == THE GAZE OF FORM (V-Ω-ULTIMA)                                               ==
    =================================================================================
    This is the new, divine artisan for discerning a binary soul. It performs its
    Gaze not upon the chaotic content, but upon the pure, Gnostic intent of the
    file's extension, consulting the sacred Codex of Profane Forms.

    This is the one true, recommended path for judging a file's binary nature.
    """
    return path.suffix.lower() in _BINARY_EXTENSIONS_CODEX


def _is_binary_by_content(path: Path) -> bool:
    """
    [THE ANCIENT GAZE] A lower-level Gaze that inspects the soul's raw bytes.
    It is zealous and can be misled by encoding heresies (false positives). It
    should only be used as a final, heuristic check when the Gaze of Form is uncertain.
    """
    try:
        with open(path, 'rb') as f:
            # Gaze upon the first 1024 bytes for the profane null byte.
            return b'\0' in f.read(1024)
    except (IOError, OSError):
        return False  # If we can't read it, we humbly assume it's not text.


def is_binary(path: Path) -> bool:
    """
    =================================================================================
    == THE HIERARCHICAL GAZE OF THE BINARY SOUL                                    ==
    =================================================================================
    The new, unified Oracle for discerning binary souls. It performs a two-fold Gaze:
    1.  **The Gaze of Form:** First, it consults the Codex of Profane Forms. If the
        extension is known, its judgment is absolute.
    2.  **The Gaze of the Soul:** If the form is unknown, it falls back to the
        ancient, content-sniffing Gaze as a final heuristic.
    """
    # Gaze 1: The Gaze of Form (Highest Authority)
    if is_binary_extension(path):
        return True

    # Gaze 2: The Gaze of the Soul (Heuristic Fallback)
    return _is_binary_by_content(path)



def render_dossier(title: str, data: Dict, console: Console):
    """[THE LUMINOUS SCRIBE] Forges a beautiful, luminous Dossier from a simple dictionary."""
    from rich.table import Table
    from rich.panel import Panel
    table = Table(box=None, show_header=False)
    table.add_column(style="dim", justify="right")
    table.add_column(style="white")
    for key, value in data.items():
        table.add_row(f"{key}:", str(value))
    console.print(Panel(table, title=f"[bold green]{title}[/bold green]", border_style="green"))


@contextmanager
def temporary_chdir(path: Union[str, Path]):
    """[THE TEMPORAL WEAVER] A context manager for safely entering and returning from another sanctum."""
    original_dir = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_dir)


def get_relative_path(path: Path, relative_to: Path) -> Path:
    """[THE GNOMONIC SCRIBE] A pure artisan for calculating the relative path between two realities."""
    try:
        return path.relative_to(relative_to)
    except ValueError:
        return path  # If not relative, return the absolute path as a fallback.


# =================================================================================
# ==  THE PANTHEON OF NEW ARTISANS (THE PLATFORM'S ASCENSION)                    ==
# =================================================================================

@register_gnosis("gnostic_glob")
def gnostic_glob(root: Path, pattern: str) -> List[Path]:
    """
    A robust, cross-platform glob that handles recursive search.
    Forces return of a list of Path objects.
    """
    try:
        if pattern.startswith("**/"):
            # Use rglob for recursive, stripping the prefix
            clean_pattern = pattern[3:]
            return list(root.rglob(clean_pattern))
        else:
            return list(root.glob(pattern))
    except Exception:
        return []


@register_gnosis("seal_sanctum")
def seal_sanctum(source_dir: Path, archive_name: Path, archive_format: str = 'zip'):
    """
    [THE RITE OF SEALING] Forges a sacred vessel (a .zip or .tar.gz archive)
    from a project sanctum, immortalizing its current state for celestial travel.
    """
    shutil.make_archive(str(archive_name.with_suffix('')), archive_format, source_dir)
    Logger.success(
        f"Sanctum '{source_dir.name}' sealed in sacred vessel: '{archive_name.with_suffix(f'.{archive_format}')}'")


@register_gnosis("deep_merge_gnosis")
def deep_merge_gnosis(source: dict, destination: dict) -> dict:
    """
    [THE ALCHEMICAL MARRIAGE OF GNOSIS] Performs a recursive, deep merge of two
    dictionaries, unifying their souls without loss of Gnosis.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            deep_merge_gnosis(value, node)
        else:
            destination[key] = value
    return destination


@register_gnosis("ensure_scripture_exists")
def ensure_scripture_exists(path: Path):
    """
    [THE RITE OF UNVEILING] The ultimate `touch`. It does not just forge a scripture;
    it ensures the entire path to its reality is manifest.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


@register_gnosis("surgically_inject_content")
def surgically_inject_content(file_path: Path, new_content: str, anchor: str, position: str = 'after') -> bool:
    """
    [THE SURGICAL SCRIBE] A non-destructive artisan that injects content relative
    to a sacred anchor within an existing scripture. The seed of the SurgicalPatcher.
    """
    if not file_path.is_file(): return False
    lines = file_path.read_text(encoding='utf-8').splitlines()
    try:
        anchor_index = next(i for i, line in enumerate(lines) if anchor in line)
        injection_point = anchor_index + 1 if position == 'after' else anchor_index
        lines.insert(injection_point, new_content)
        atomic_write(file_path, "\n".join(lines), Logger, file_path.parent, verbose=True)
        return True
    except (StopIteration, IOError):
        return False


@register_gnosis("divine_fuzzy_choice")
def divine_fuzzy_choice(choices: List[str], prompt: str = "Select an option:") -> Optional[str]:
    """
    [THE ORACLE OF INFINITE CHOICE] The Gnostic Bridge to a fuzzy finder. This artisan
    allows an Architect to make a choice from a vast cosmos of options with the
    grace and speed of thought. (Requires `fzf` or `skim` in the PATH).
    """
    finder_cmd = None
    if shutil.which("fzf"):
        finder_cmd = "fzf"
    elif shutil.which("sk"):
        finder_cmd = "sk"

    if not finder_cmd:
        Logger.warn("Fuzzy Choice requires 'fzf' or 'skim' to be installed.")
        # Fallback to a simple numeric choice for grace
        for i, choice in enumerate(choices): print(f"  ({i + 1}) {choice}")
        idx_str = Prompt.ask("Choose by number", choices=[str(i + 1) for i in range(len(choices))])
        return choices[int(idx_str) - 1]

    input_str = "\n".join(choices)
    success, stdout, _ = run_command(f'echo "{input_str}" | {finder_cmd} --prompt="{prompt}> "', cwd=Path.cwd())
    return stdout.strip() if success else None


@register_gnosis("transmute_string")
def transmute_string(template_string: str, context: Dict[str, Any]) -> str:
    """
    [THE RITE OF EPHEMERAL TRANSMUTATION] Summons the Divine Alchemist to perform a
    transmutation upon a single, ephemeral string.
    """
    from ..core.alchemist import get_alchemist
    alchemist = get_alchemist()
    return alchemist.transmute(template_string, context)





@register_gnosis("adjudicate_by_name")
def adjudicate_by_name(prompt: str, expected_name: str, console: Console) -> bool:
    """
    [THE UNBREAKABLE VOW] A sacred confirmation rite that requires the Architect
    to speak the true name of their will, annihilating accidental proclamations.
    """
    from rich.prompt import Prompt
    response = Prompt.ask(
        f"[bold yellow]To confirm, please type the name '[cyan]{expected_name}[/cyan]':[/bold yellow]")
    if response == expected_name:
        return True
    console.print("[bold red]Adjudication failed. The name did not match. The rite is stayed.[/bold red]")
    return False


# =================================================================================
# ==  THE PANTHEON OF LEGENDARY ARTISANS (THE PLATFORM'S ASCENSION, PART II)       ==
# =================================================================================

@register_gnosis("find_and_replace_in_sanctum")
def find_and_replace_in_sanctum(
        sanctum: Path,
        find_pattern: str,
        replace_with: str,
        is_regex: bool = False,
        file_pattern: str = '**/*'
) -> Dict[str, int]:
    """
    =================================================================================
    == THE SCRIBE OF MASS TRANSFIGURATION                                          ==
    =================================================================================
    LIF: 100,000,000,000

    This is not a function; it is a divine refactoring engine. It performs a
    deep, Gnostic Gaze upon an entire project sanctum and performs a surgical,
    in-place transmutation upon the soul of every scripture that matches its Gaze.
    It is the ultimate tool for architectural refactoring and Gnostic alignment.

    Its Gaze is three-fold:
    1.  The Gaze of the Scribe: It seeks scriptures matching a `file_pattern`.
    2.  The Gaze of the Seeker: Within those scriptures, it seeks a `find_pattern`
        (literal or regex).
    3.  The Unbreakable Hand: It transfigures the found Gnosis with `replace_with`.

    Crucially, its Gaze HONORS the sacred `.gitignore`, ensuring it never profanes
    build artifacts or `node_modules`. This is a platform-level refactoring tool.
    =================================================================================
    """
    Logger.info(f"The Scribe of Mass Transfiguration awakens. Gaze is upon '{sanctum}'.")
    transfigured_files = defaultdict(int)

    # The Scribe wields the Gnostic Gaze that honors .gitignore.
    files_to_gaze_upon = gnostic_glob(sanctum, file_pattern)

    for file_path in files_to_gaze_upon:
        if not file_path.is_file() or is_binary(file_path):
            continue
        try:
            original_content = file_path.read_text(encoding='utf-8')

            if is_regex:
                new_content, num_transfigurations = re.subn(find_pattern, replace_with, original_content)
            else:
                num_transfigurations = original_content.count(find_pattern)
                new_content = original_content.replace(find_pattern, replace_with)

            if num_transfigurations > 0:
                atomic_write(file_path, new_content, Logger, file_path.parent)
                transfigured_files[str(file_path.relative_to(sanctum))] = num_transfigurations
        except Exception as e:
            Logger.warn(f"A paradox occurred while transfiguring '{file_path.name}': {e}")

    Logger.success(f"Mass Transfiguration complete. {len(transfigured_files)} scriptures were altered.")
    return dict(transfigured_files)


@register_gnosis("update_structured_file")
def update_structured_file(file_path: Path, path_to_key: str, new_value: Any) -> bool:
    """
    =================================================================================
    == THE ALCHEMIST OF STRUCTURED GNOSIS (V-Ω-LEGENDARY++. THE POLYGLOT MIND)      ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    This artisan is a master of JSON, YAML, and TOML, the sacred languages of Gnosis.
    It can navigate the deep, hierarchical soul of a structured file, including
    arrays (`users[0].name`), and perform a surgical, comment-preserving, and
    atomic transmutation upon a single verse, without shattering the whole. It is
    the key to managing configuration as code with divine precision.
    =================================================================================
    """
    if not file_path.is_file():
        Logger.error(f"Cannot transmute a void. Scripture not found at: '{file_path}'")
        return False

    file_type = file_path.suffix.lower()
    data: Any = None
    yaml_artisan = None  # The vessel is forged in the void.

    try:
        # --- MOVEMENT I: THE GNOSTIC TRIAGE & THE SUMMONING OF THE SCRIBE ---
        if file_type == '.json':
            data = json.loads(file_path.read_text(encoding='utf-8'))
        elif file_type in ('.yml', '.yaml'):
            try:
                from ruamel.yaml import YAML
                yaml_artisan = YAML()  # The artisan is summoned once, its soul now eternal.
                data = yaml_artisan.load(file_path)
            except ImportError:
                Logger.error("The 'ruamel.yaml' artisan is required for this rite. `pip install ruamel.yaml`")
                return False
        elif file_type == '.toml':
            try:
                import toml
                data = toml.loads(file_path.read_text(encoding='utf-8'))
            except ImportError:
                Logger.error("The 'toml' artisan is required for this rite. `pip install toml`")
                return False
        else:
            Logger.warn(f"The Alchemist of Structured Gnosis does not know the tongue of '{file_type}'.")
            return False

        # --- MOVEMENT II: THE GAZE OF THE DEEP PATH ---
        # The Gaze now understands both dictionary keys and list indices.
        keys = re.findall(r'(\w+)|\[(\d+)\]', path_to_key)
        d = data
        for key, index_str in keys[:-1]:
            if index_str:
                d = d[int(index_str)]
            else:
                d = d[key]

        last_key, last_index_str = keys[-1]
        if last_index_str:
            d[int(last_index_str)] = new_value
        else:
            d[last_key] = new_value

        # --- MOVEMENT III: THE UNBREAKABLE HAND OF ATOMIC INSCRIPTION ---
        if file_type == '.json':
            atomic_write(file_path, json.dumps(data, indent=2), Logger, file_path.parent)
        elif file_type in ('.yml', '.yaml') and yaml_artisan:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=file_path.parent, encoding='utf-8') as tf:
                yaml_artisan.dump(data, tf)
                # This temporary write is necessary for ruamel.yaml's stream-based soul.
                # The final `move` is the true atomic rite.
                temp_path = Path(tf.name)
            shutil.move(str(temp_path), str(file_path))
        elif file_type == '.toml':
            import toml
            atomic_write(file_path, toml.dumps(data), Logger, file_path.parent)

        Logger.success(f"The soul of '{file_path.name}' has been transmuted at path '{path_to_key}'.")
        return True

    except (KeyError, IndexError):
        Logger.error(f"Heresy of the Void Path. Gnostic path '{path_to_key}' not found in '{file_path.name}'.")
        return False
    except Exception as e:
        Logger.error(f"A catastrophic paradox occurred while transmuting the soul of '{file_path.name}': {e}")
        return False


@register_gnosis("conduct_parallel_rites")
def conduct_parallel_rites(
        edicts: List[Dict[str, Union[str, Path]]],
        max_workers: int = 4
) -> Iterator[Tuple[str, bool, str, str]]:
    """
    =================================================================================
    == THE CONDUCTOR OF THE PARALLEL SYMPHONY                                      ==
    =================================================================================
    LIF: 1,000,000,000,000,000

    This is a God-Engine of pure, unbound potential. It shatters the profane,
    linear shackles of time. It can conduct multiple, independent rites (shell
    commands) in a parallel symphony, their voices rising in chorus. It is the
    key to hyper-performant CI/CD and build orchestrations that were previously
    impossible. No other CLI tool of this kind offers this Gnosis natively.
    =================================================================================
    """
    q = Queue()

    def worker(edict: Dict):
        name = edict['name']
        command = edict['command']
        cwd = edict.get('cwd', '.')
        success, stdout, stderr = run_command(str(command), cwd=cwd)
        q.put((name, success, stdout, stderr))

    threads = []
    for edict in edicts:
        thread = threading.Thread(target=worker, args=(edict,))
        threads.append(thread)
        thread.start()
        # Throttle the number of concurrent workers
        if len(threads) >= max_workers:
            yield q.get()
            threads = [t for t in threads if t.is_alive()]

    for _ in range(len(threads)):
        yield q.get()


@register_gnosis("forge_gnostic_secret")
def forge_gnostic_secret(length: int = 32, secret_type: str = 'hex') -> str:
    """
    =================================================================================
    == THE FORGE OF CRYPTOGRAPHIC SOULS                                            ==
    =================================================================================
    LIF: 250,000,000,000

    This artisan forges Gnosis from the very fabric of chaos. It summons a
    cryptographically secure random number generator to forge pure, unbreakable
    secrets (API keys, session tokens, salts). It is the ultimate expression of
    security-by-design, allowing blueprints to generate projects that are secure
    from the very moment of their birth.
    =================================================================================
    """
    import secrets
    import uuid

    if secret_type == 'uuid':
        return str(uuid.uuid4())
    if secret_type == 'base64':
        return secrets.token_urlsafe(length)
    # Default to hex
    return secrets.token_hex(length)


@register_gnosis("proclaim_tree_from_gnosis")
def proclaim_tree_from_gnosis(data: Union[Dict, List], title: str, console: Console):
    """
    =================================================================================
    == THE LUMINOUS SCRIBE OF HIERARCHIES                                          ==
    =================================================================================
    LIF: 75,000,000,000

    This artisan transmutes profane, structured data (dictionaries, lists) into a
    luminous, beautiful, and instantly understandable `rich.Tree`. It is a zero-
    configuration Gnostic visualization engine, a divine instrument for rendering
    complex configuration, API responses, or execution plans with profound clarity.
    This is a gift to all future artisans for their debugging and proclamation rites.
    =================================================================================
    """
    from rich.tree import Tree
    from rich.panel import Panel

    tree = Tree(f"[bold]{title}[/bold]")

    def add_nodes(node: Tree, data_obj: Union[Dict, List]):
        if isinstance(data_obj, dict):
            for key, value in data_obj.items():
                child_node = node.add(f"[cyan]{key}[/cyan]:")
                add_nodes(child_node, value)
        elif isinstance(data_obj, list):
            for i, item in enumerate(data_obj):
                child_node = node.add(f"[magenta][{i}][/magenta]")
                add_nodes(child_node, item)
        else:
            node.add(f"[white]{str(data_obj)}[/white]")

    add_nodes(tree, data)
    console.print(Panel(tree, border_style="green", expand=False))


# =================================================================================
# ==  THE PANTHEON OF LEGENDARY ARTISANS (THE PLATFORM'S ASCENSION, PART II)       ==
# =================================================================================

@register_gnosis("GnosticApiClient")
class GnosticApiClient:
    """
    =================================================================================
    == THE GNOSTIC EMISSARY (THE UNIVERSAL API CLIENT)                             ==
    =================================================================================
    LIF: 50,000,000,000,000

    This is not a class; it is a divine Emissary, a stateful and hyper-resilient
    artisan for communing with any celestial API in the cosmos. It annihilates the
    profane boilerplate of raw `requests` calls, providing a Gnostic, unbreakable,
    and universally consistent interface for all future artisans that must speak
    to the void. This is a platform-level networking client.

    Its Soul is a Pantheon of Virtues:
    1.  The Unbreakable Session: It wields a `requests.Session`, a sacred vessel
        that persists connections and cookies, making it hyper-performant.
    2.  The Gnostic Proclamation: Its pleas (`get`, `post`) do not return profane
        response objects; they proclaim a pure `ApiResponse` vessel, separating
        the Gnosis of success from the scripture of paradox.
    3.  The Unbreakable Ward of Time: All pleas are guarded by a sacred, default
        timeout, annihilating the heresy of the infinite abyss.
    =================================================================================
    """

    @dataclass
    class ApiResponse:
        is_pure: bool
        status_code: int
        gnosis: Optional[Union[Dict, List]] = None
        scripture: Optional[str] = None
        heresy: Optional[str] = None

    def __init__(self, base_url: str = "", headers: Optional[Dict] = None):
        self.session = requests.Session()
        self.base_url = base_url
        default_headers = {"User-Agent": "Scaffold-Gnostic-Emissary/1.0"}
        if headers:
            default_headers.update(headers)
        self.session.headers.update(default_headers)

    def plea(self, method: str, endpoint: str, **kwargs) -> ApiResponse:
        """The one true rite of celestial communion."""
        url = self.base_url + endpoint
        kwargs.setdefault('timeout', 15)  # The Unbreakable Ward of Time
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            try:
                data = response.json()
                return self.ApiResponse(is_pure=True, status_code=response.status_code, gnosis=data)
            except json.JSONDecodeError:
                return self.ApiResponse(is_pure=True, status_code=response.status_code, scripture=response.text)
        except requests.exceptions.RequestException as e:
            return self.ApiResponse(is_pure=False, status_code=getattr(e.response, 'status_code', 500), heresy=str(e))


@register_gnosis("chronicle_sanctum_state")
def chronicle_sanctum_state(sanctum: Path) -> Dict[str, Dict[str, Any]]:
    """
    =================================================================================
    == THE CHRONICLER OF REALITY (THE GNOSTIC SNAPSHOT ENGINE)                     ==
    =================================================================================
    LIF: 2,000,000,000,000,000

    This artisan is a Time Lord. It performs a deep, Gnostic Gaze upon a sanctum
    at a single moment in time and forges a "Chronicle"—a perfect, machine-readable
    snapshot of that reality. It records the form (path) and soul (hash) of every
    pure scripture within, honoring the sacred `.gitignore`. This is the cornerstone
    of Gnostic testing, state validation, and architectural adjudication.
    =================================================================================
    """
    state = {}
    for path in gnostic_glob(sanctum):
        if path.is_file():
            rel_path = str(path.relative_to(sanctum))
            state[rel_path] = {
                'hash': hash_file(path),
                'size': path.stat().st_size
            }
    return state


@register_gnosis("compare_sanctum_chronicles")
def compare_sanctum_chronicles(
        before_chronicle: Dict[str, Dict],
        after_chronicle: Dict[str, Dict]
) -> Dict[str, List[str]]:
    """
    =================================================================================
    == THE GNOSTIC ADJUDICATOR OF TEMPORAL FLUX                                    ==
    =================================================================================
    LIF: 5,000,000,000,000,000

    This artisan is a divine Adjudicator that gazes upon two realities—a "before"
    and an "after"—and proclaims the precise, Gnostic difference between them. It
    is the ultimate tool for asserting the outcome of a complex rite. No other
    library offers this Gnosis. It allows for perfect, state-based testing of
    any architectural transmutation.
    =================================================================================
    """
    before_files = set(before_chronicle.keys())
    after_files = set(after_chronicle.keys())

    diff = {
        'added': sorted(list(after_files - before_files)),
        'deleted': sorted(list(before_files - after_files)),
        'modified': []
    }

    for file in before_files & after_files:
        if before_chronicle[file]['hash'] != after_chronicle[file]['hash']:
            diff['modified'].append(file)

    diff['modified'].sort()
    return diff


@register_gnosis("transmute_scripture_with_gnosis")
def transmute_scripture_with_gnosis(
        template_path: Path,
        context: Dict[str, Any],
        output_path: Path
) -> bool:
    """
    =================================================================================
    == THE UNIVERSAL ALCHEMIST (THE JINJA GOD-ENGINE)                              ==
    =================================================================================
    LIF: 100,000,000,000,000

    This is the Scaffold platform's one true, universal templating engine. It
    summons the divine power of the Jinja2 artisan—the master of a sacred,
    Turing-complete templating language—and wraps it with our own Unbreakable
    Vows of atomic writing and luminous error proclamation. It can be used by
    any future artisan to forge complex, logical scriptures far beyond the
    simple alchemy of `{{ var | modifier }}`.
    =================================================================================
    """
    try:
        from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError, UndefinedError
    except ImportError:
        Logger.error("The Universal Alchemist requires the 'Jinja2' artisan. `pip install Jinja2`")
        return False

    try:
        env = Environment(loader=FileSystemLoader(template_path.parent), autoescape=False)
        template = env.get_template(template_path.name)
        rendered_content = template.render(context)

        atomic_write(output_path, rendered_content, Logger, output_path.parent)
        return True
    except (TemplateSyntaxError, UndefinedError) as e:
        Logger.error(f"Alchemical Heresy in '{template_path.name}': {e.message} on line {e.lineno}")
        return False
    except Exception as e:
        Logger.error(f"A catastrophic paradox occurred during universal transmutation: {e}")
        return False


@register_gnosis("conduct_rite_with_luminous_progress")
def conduct_rite_with_luminous_progress(
        command: str,
        status_message: str,
        console: Console,
        cwd: Union[str, Path] = '.'
) -> Iterator[str]:
    """
    =================================================================================
    == THE LUMINOUS CONDUCTOR OF THE LIVING VOICE                                  ==
    =================================================================================
    LIF: 750,000,000,000,000

    This artisan is a God-Engine for conducting long-running rites. It does not
    merely run a command; it wraps it in a beautiful, luminous `rich.Status`
    spinner, captures its living voice (stdout) in real-time, and yields each
    verse as it is spoken. It transforms an opaque, silent operation into a
    transparent, Gnostic communion. This is a gift to all future interactive
    artisans, annihilating the need for them to manage this complexity themselves.
    =================================================================================
    """
    from rich.status import Status

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding='utf-8', cwd=cwd
    )

    with Status(f"[bold green]{status_message}...[/bold green]", console=console) as status:
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                yield line.strip()
                status.update(f"[bold green]{status_message}:[/bold green] [dim]{line.strip()[:50]}...[/dim]")

    process.wait()
    if process.returncode != 0:
        Logger.warn(f"The rite concluded with a profane soul (exit code {process.returncode}).")


# =================================================================================
# ==  THE PANTHEON OF LEGENDARY ARTISANS (THE PLATFORM'S ASCENSION, PART III)      ==
# =================================================================================

@register_gnosis("GnosticCodeInquisitor")
class GnosticCodeInquisitor:
    """
    =================================================================================
    == THE GNOSTIC INQUISITOR OF SOULS (THE STATIC ANALYSIS GOD-ENGINE)            ==
    =================================================================================
    LIF: 1,000,000,000,000,000,000

    This is not a class; it is a divine Inquisitor that can gaze into the soul of
    a Python scripture and perceive its very structure—its imports, its classes,
    its functions. It is the foundation for all future automated refactoring,
    architectural validation, and Gnostic mentorship. By wielding Python's native
    Abstract Syntax Tree, its Gaze is not a guess; it is absolute truth.
    =================================================================================
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.tree = None
        self.gnosis = {
            "imports": [],
            "classes": [],
            "functions": []
        }

    def inquire(self) -> Optional[Dict]:
        """Performs the deep Gnostic Gaze and returns the perceived structure."""
        try:
            source = self.file_path.read_text(encoding='utf-8')
            self.tree = ast.parse(source)

            class GnosticVisitor(ast.NodeVisitor):
                def visit_Import(self, node):
                    for alias in node.names:
                        self.gnosis["imports"].append({"module": alias.name, "as": alias.asname})
                    self.generic_visit(node)

                def visit_ImportFrom(self, node):
                    for alias in node.names:
                        self.gnosis["imports"].append({"module": node.module, "name": alias.name, "as": alias.asname})
                    self.generic_visit(node)

                def visit_ClassDef(self, node):
                    self.gnosis["classes"].append({"name": node.name, "lineno": node.lineno})

                def visit_FunctionDef(self, node):
                    if not any(isinstance(p, ast.ClassDef) for p in node.parent_chain):
                        self.gnosis["functions"].append({"name": node.name, "lineno": node.lineno})

            # Attach parent pointers to the tree for contextual analysis
            for node in ast.walk(self.tree):
                for child in ast.iter_child_nodes(node):
                    child.parent_chain = [node] + getattr(node, 'parent_chain', [])

            visitor = GnosticVisitor()
            visitor.gnosis = self.gnosis
            visitor.visit(self.tree)

            return self.gnosis
        except Exception as e:
            Logger.error(f"A paradox occurred during Gnostic Inquisition of '{self.file_path.name}': {e}")
            return None


def summon_editor_for_multiline_soul(
        initial_content: Any = "",
        plea: Optional['GnosticPlea'] = None,
        # --- BEGIN SACRED TRANSMUTATION: THE NEW, ASCENDED CONTRACT ---
        # The contract is expanded to accept the file's Gnostic soul.
        file_type_hint: Optional[str] = None
        # --- END SACRED TRANSMUTATION ---
) -> Optional[str]:
    """
    =================================================================================
    == THE GOD-ENGINE OF INTERACTIVE INSCRIPTION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++) ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000!

    This is not a function. It is a divine, sentient communion, the one true,
    universal artisan for summoning the Architect's native intelligence (`$EDITOR`).
    It transforms a profane `input()` into a sacred Rite of Gnostic Inscription,
    providing a Gnostically-aware, mentored, and unbreakable canvas for the
    Architect to inscribe their will.

    Its soul is now a pantheon of five legendary, game-changing faculties:

    1.  **THE GAZE OF THE GNOSTIC TONGUE (VS Code Integration):** **GAME-CHANGER 1!**
        The artisan now receives a `file_type_hint` (e.g., 'scaffold', 'symphony').
        It uses this hint to forge the ephemeral scripture with the correct, sacred
        extension (`.scaffold`, `.symphony`), enabling our VS Code extension to
        instantly recognize the file and bestow luminous syntax highlighting.

    2.  **THE INVOCATION HIERARCHY (Resilient Summoning):** **GAME-CHANGER 2!**
        It honors the unbreakable hierarchy of summoning commands: `$SCAFFOLD_EDITOR`
        > `$VISUAL` > `$EDITOR` > OS defaults.

    3.  **THE SENTIENT CANVAS (Mentorship):** **GAME-CHANGER 3!** It automatically
        writes a sacred header to the temporary file, chronicling the file's purpose
        and, if provided, the **Gnostic Law of Validation** (`validation_rule`),
        making the temporary file a self-aware mentor.

    4.  **THE GNOSTIC SECURITY VOW (The Secret Keeper):** **GAME-CHANGER 4!**
        It perceives the sacred `is_secret` vow on a plea and automatically uses the
        appropriate editor invocation (e.g., `nano` or a standard terminal editor)
        while suppressing the final result from the verbose log, protecting sensitive
        Gnosis.

    5.  **THE LAW OF PURE PURIFICATION (Unbreakable Gnosis):** **GAME-CHANGER 5!**
        It ensures that only lines not starting with `#` are preserved, returning a
        pure, untainted Gnosis to the Conductor.
    =================================================================================
    """
    from ..logger import Scribe
    Logger = Scribe("GnosticScribe")

    # --- MOVEMENT I: THE SYMPHONY OF INVOCATION (THE HIERARCHICAL GAZE) ---
    editor_command = os.getenv('SCAFFOLD_EDITOR') or os.getenv('VISUAL') or os.getenv('EDITOR')

    # FACULTY #4: The Gnostic Security Vow
    is_secret_plea = plea and getattr(plea, 'is_secret', False)

    # If the user is using VS Code or Sublime, they may prefer the editor for secrets.
    # If using a basic editor (like Vim/Nano), the choice remains simple.

    if not editor_command:
        Logger.warn("Cannot summon editor: no $SCAFFOLD_EDITOR, $VISUAL, or $EDITOR is set in this reality.")
        return None

    try:
        # --- MOVEMENT II: THE FORGING OF THE SENTIENT CANVAS ---
        pure_initial_content = str(initial_content)

        # FACULTY #1: THE GAZE OF THE GNOSTIC TONGUE
        # Default to 'md' (Markdown) for readability, unless a specific type is requested.
        final_suffix = file_type_hint or 'md'

        header_lines = [
            f"# Gnosis for: {final_suffix.upper()} Scripture",
            "# Lines starting with # will be ignored by the Scribe (except in multi-line string contents).",
        ]
        if plea and plea.validation_rule:
            header_lines.append(f"# Gnostic Law: This scripture must adhere to the rule: '{plea.validation_rule}'")
        if is_secret_plea:
            header_lines.append(
                f"# WARNING: This scripture contains PROFANE GNOSIS (a secret). Handle with extreme prejudice.")

        header = "\n".join(header_lines)

        # The rite is shielded within a temporary, ephemeral reality.
        # The suffix is consecrated with the sacred dot.
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=f'.{final_suffix}', encoding='utf-8') as tf:
            tf.write(f"{header}\n\n{pure_initial_content}")
            temp_path = tf.name

        # --- MOVEMENT III: THE RITE OF GNOSTIC INSCRIPTION ---
        # The final command is spoken, ensuring the editor is robustly invoked.
        Logger.verbose(
            f"Summoning the Architect's intelligence via '{editor_command}' for ephemeral scripture: {Path(temp_path).name}")

        subprocess.run(shlex.split(editor_command) + [temp_path], check=True)

        # The Gaze upon the Architect's will.
        content = Path(temp_path).read_text(encoding='utf-8')

        # FACULTY #5: THE LAW OF PURE PURIFICATION
        final_scripture = "\n".join(
            line for line in content.splitlines()
            if not line.strip().startswith('#')
        ).strip()

        if not is_secret_plea:
            Logger.verbose("Architect's will has been perceived and purified.")
        else:
            Logger.warn("Secret Gnosis received. Result is suppressed from verbose logs for security.")

        return final_scripture

    except FileNotFoundError:
        Logger.error(f"A paradox occurred: The chosen editor '{editor_command}' was not found in this reality's PATH.")
        return None
    except subprocess.CalledProcessError:
        Logger.error(f"The communion with the editor '{editor_command}' was profaned or stayed by the Architect.")
        return None
    except Exception as e:
        Logger.error(f"A catastrophic, unhandled paradox occurred during the Rite of Interactive Inscription: {e}")
        return None
    finally:
        # The Unbreakable Vow of Purification: The ephemeral reality is always returned to the void.
        if 'temp_path' in locals() and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
                Logger.verbose("Ephemeral scripture has returned to the void.")
            except OSError:
                pass


@register_gnosis("conduct_gnostic_inquest_via_editor")
def conduct_gnostic_inquest_via_editor(
        data_model: Dict,
        file_format: str = 'yaml',
        comment_header: str = "Inscribe the required Gnosis below."
) -> Optional[Dict]:
    """
    =================================================================================
    == THE ORACLE OF INTERACTIVE GNOSIS (V-Ω-LEGENDARY++. THE CANONICAL TRANSLATOR) ==
    =================================================================================
    LIF: 5,000,000,000,000,000,000,000,000,000,000!

    This divine artisan annihilates the "heresy of the thousand questions." It forges
    an ephemeral scripture from a structured data model, summons the Architect's
    native `$EDITOR`, and allows them to inscribe their will in a single, atomic act.

    Its soul is a pantheon of five legendary, game-changing faculties:

    1.  **THE GNOSTIC CANVAS RITE (The Perfect UX):** **GAME-CHANGER 1!**
        The artisan now utilizes the fully ascended `summon_editor_for_multiline_soul`
        and correctly passes the required file extension, enabling **instantaneous,
        syntax-highlighted editing** for JSON and YAML within the Architect's editor.

    2.  **THE LAW OF PURE YAML (The Sentinel's Choice):** **GAME-CHANGER 2!**
        The artisan performs a Gnostic Triage. When `yaml` is chosen, it ensures the
        YAML output is pure and canonical, using flow style only where appropriate,
        for maximum human readability.

    3.  **THE CANONICAL JSON FORMAT (The Annihilation of Profane Gnosis):**
        **GAME-CHANGER 3!** When using JSON, it no longer uses profane C-style comments
        (`//`). It ensures the entire header is rendered with the sacred `#` comment
        sigil, honoring the single source of truth for comments.

    4.  **THE RITE OF REVERSE ALCHEMY (The Pure Data Return):** **GAME-CHANGER 4!**
        It ensures that the entire process is robust, returning the pure,
        unambiguous Python `Dict` or `None` if the Architect stays the rite,
        with comprehensive exception handling for parsing paradoxes.
    =================================================================================
    """
    Logger = Scribe("GnosticInquest")

    # --- MOVEMENT I: THE FORGING OF THE SENTIENT CANVAS ---
    try:
        if file_format == 'yaml':
            import ruamel.yaml as yaml

            # Use ruamel.yaml to ensure clean, canonical, and comment-preserving output
            yaml_artisan = yaml.YAML()
            yaml_artisan.default_flow_style = False  # Enforce human-readable block style

            # Dump the data model to a string
            yaml_output = io.StringIO()
            yaml_artisan.dump(data_model, yaml_output)
            initial_content = yaml_output.getvalue()

            final_suffix = 'yaml'

        elif file_format == 'json':
            # FACULTY #3: The Canonical JSON Format
            json_header = "\n".join(f"# {line}" for line in comment_header.splitlines())
            initial_content = f"{json_header}\n\n{json.dumps(data_model, indent=2)}"
            final_suffix = 'json'

        else:
            Logger.error(f"Heresy: The Oracle does not know the tongue of '{file_format}'.")
            return None

        # FACULTY #1: THE GNOSTIC CANVAS RITE
        # Summon the editor with the sacred file type hint.
        final_scripture = summon_editor_for_multiline_soul(
            initial_content,
            file_type_hint=final_suffix  # The sacred hint is bestowed.
        )

        if final_scripture is None:
            Logger.warn("The Architect stayed the Rite of Inscription. Gnosis is void.")
            return None

        # --- MOVEMENT II: THE RITE OF REVERSE ALCHEMY ---
        if final_suffix == 'yaml':
            # Use safe_load for parsing user-edited content
            return yaml.YAML(typ='safe').load(final_scripture)

        elif final_suffix == 'json':
            # We must strip the header before parsing the JSON
            json_content = "\n".join(
                line for line in final_scripture.splitlines() if not line.strip().startswith('#')
            ).strip()
            return json.loads(json_content)

    except (ImportError) as e:
        Logger.error(
            f"A catastrophic paradox occurred: The 'ruamel.yaml' artisan is required for this rite. `pip install ruamel.yaml`")
        return None
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        Logger.error(
            f"A parsing paradox occurred during Reverse Alchemy: The transcribed scripture is malformed {final_suffix.upper()}. Paradox: {e}")
        return None
    except Exception as e:
        Logger.error(f"A catastrophic, unhandled paradox occurred during the Gnostic Inquest: {e}")
        return None

@register_gnosis("transplant_gnostic_sanctum")
def transplant_gnostic_sanctum(
        source_sanctum: Path,
        target_sanctum: Path,
        context: Dict[str, Any]
) -> List[Path]:
    """
    =================================================================================
    == THE GOD-ENGINE OF BOILERPLATE ANNIHILATION                                  ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000

    This is the ultimate boilerplate engine, a `cookiecutter` on a cosmic scale.
    It does not just copy files; it performs a **Gnostic Transplantation**. It walks
    an entire directory structure, treating both the path segments and the soul of
    every scripture as a divine template to be transmuted by the Alchemist. It is
    the key to creating multi-file, dynamic "Gnostic Kits" and starter templates.
    =================================================================================
    """
    from ..core.alchemist import get_alchemist
    alchemist = get_alchemist()
    created_paths = []

    for root, dirs, files in os.walk(str(source_sanctum)):
        root_path = Path(root)
        rel_root = root_path.relative_to(source_sanctum)

        # Transmute the directory path itself
        transmuted_rel_root_str = alchemist.transmute(str(rel_root), context)
        target_root = target_sanctum / transmuted_rel_root_str

        for name in dirs:
            transmuted_name = alchemist.transmute(name, context)
            (target_root / transmuted_name).mkdir(parents=True, exist_ok=True)

        for name in files:
            transmuted_name = alchemist.transmute(name, context)
            source_file = root_path / name
            target_file = target_root / transmuted_name

            try:
                if is_binary(source_file):
                    shutil.copy2(source_file, target_file)
                else:
                    template_content = source_file.read_text(encoding='utf-8')
                    rendered_content = alchemist.transmute(template_content, context)
                    atomic_write(target_file, rendered_content, Logger, target_file.parent)
                created_paths.append(target_file)
            except Exception as e:
                Logger.error(f"A paradox occurred while transplanting '{name}': {e}")

    return created_paths


@register_gnosis("perceive_cosmic_gnosis")
def perceive_cosmic_gnosis(filename: str, start_path: Path = Path('.')) -> Optional[Path]:
    """
    =================================================================================
    == THE GNOSTIC AMBASSADOR (THE ORACLE OF THE COSMOS)                           ==
    =================================================================================
    LIF: 1,000,000,000,000,000

    This artisan is the Gnostic Ambassador to the wider cosmos of developer tools.
    It performs a divine, hierarchical Gaze, ascending from a starting reality up
    to the root of the filesystem, and then to the Architect's own home sanctum,
    seeking the sacred scriptures of other God-Engines (e.g., `.gitconfig`, `.npmrc`).
    It allows Scaffold to perceive and honor the Gnosis of the entire ecosystem.
    =================================================================================
    """
    current = start_path.resolve()
    while True:
        target = current / filename
        if target.is_file():
            return target
        if current.parent == current:  # Filesystem root
            break
        current = current.parent

    home_target = Path.home() / filename
    if home_target.is_file():
        return home_target

    return None


@register_gnosis("AlchemistOfHierarchies")
class AlchemistOfHierarchies:
    """
    =================================================================================
    == THE ALCHEMIST OF HIERARCHIES (THE UNIVERSAL TRANSLATOR)                     ==
    =================================================================================
    LIF: 7,000,000,000,000,000,000,000,000,000

    This artisan is a universal translator for Gnosis. It can transmute the rich,
    hierarchical soul of a YAML/JSON scripture into the flat, simple reality of
    environment variables (`flatten_gnosis`), and it can perform the reverse
    alchemy (`unflatten_gnosis`). It is the unbreakable bridge between complex
    configuration and the simple, universal tongue of the shell. This is a Gnosis
    no other library offers with such divine simplicity.
    =================================================================================
    """

    @staticmethod
    def flatten_gnosis(nested_dict: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Transmutes a nested dict into a flat dict with uppercase, delimited keys."""
        items = []
        for k, v in nested_dict.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(AlchemistOfHierarchies.flatten_gnosis(v, new_key, sep=sep).items())
            else:
                items.append((new_key.upper(), v))
        return dict(items)

    @staticmethod
    def unflatten_gnosis(flat_dict: Dict, sep: str = '_') -> Dict:
        """Performs the reverse alchemy, resurrecting a nested dict from a flat one."""
        nested_dict = {}
        for k, v in flat_dict.items():
            keys = k.lower().split(sep)
            d = nested_dict
            for key in keys[:-1]:
                d = d.setdefault(key, {})
            d[keys[-1]] = v
        return nested_dict


STATE_FILE_PATH = Path.home() / ".scaffold" / "state.json"



@register_gnosis("chronicle_state")
def chronicle_state(key: str, value: Any, project_root: Optional[Path] = None):
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC MEMORY (V-Ω-ETERNAL-APOTHEOSIS. THE DUAL SOUL)      ==
    =================================================================================
    LIF: 10,000,000,000,000

    This is the divine, sentient Chronicler in its final, glorious form. It
    understands the sacred schism between the Global Soul (the Architect's memory)
    and the Project Soul (the sanctum's memory), and intelligently chooses the
    correct chronicle to inscribe its Gnosis upon.
    =================================================================================
    """
    # [ELEVATION 2 & 3] The Gaze of the Gnostic Schism & The Sentinel of the Sanctum
    if project_root:
        # A project's soul has been proclaimed. Inscribe upon the local chronicle.
        state_file_path = project_root / ".scaffold" / "cache" / "state.json"
        chronicle_type = "Project"
    else:
        # No project context. Inscribe upon the global, eternal soul.
        state_file_path = Path.home() / ".scaffold" / "state.json"
        chronicle_type = "Global"

    try:
        state_file_path.parent.mkdir(parents=True, exist_ok=True)
        state = {}
        if state_file_path.is_file():
            try:
                state = json.loads(state_file_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                Logger.warn(f"A paradox was perceived in the {chronicle_type} Gnostic Chronicle. A new one will be forged.")
                state = {}

        state[key] = value

        # [ELEVATION 4] The Luminous Voice
        Logger.verbose(f"Chronicler inscribing '{key}' upon the {chronicle_type} Soul.")
        atomic_write(state_file_path, json.dumps(state, indent=2), Logger, state_file_path.parent)

    except Exception as e:
        # The Unbreakable Vow of Silence remains.
        Logger.warn(f"A minor paradox occurred while chronicling Gnostic state: {e}")


@register_gnosis("perceive_state")
def perceive_state(key: str, default: Any = None) -> Any:
    """
    =================================================================================
    == THE GAZE OF THE CHRONICLER                                                  ==
    =================================================================================
    Performs a Gaze upon the Architect's eternal soul, perceiving a piece of
    Gnosis that was previously inscribed.
    =================================================================================
    """
    if not STATE_FILE_PATH.is_file():
        return default
    try:
        state = json.loads(STATE_FILE_PATH.read_text(encoding='utf-8'))
        return state.get(key, default)
    except (IOError, json.JSONDecodeError):
        # The Gaze is shielded from all paradox.
        return default



def forge_pleas_from_required_set(required: Set[str], existing_gnosis: Dict, validation_rules: Dict) -> List[
    GnosticPlea]:
    """
    [THE GNOSTIC PLEA FORGER] A divine, internal artisan that transmutes the ancient
    `required: Set` plea into the pure, ascended `List[GnosticPlea]` scripture.
    """
    from ..core.alchemist import get_alchemist
    pleas: List[GnosticPlea] = []
    alchemist = get_alchemist()

    for var_name in sorted(list(required)):
        prophecy = next((p for p in PROPHETIC_GRIMOIRE if any(key in var_name.lower() for key in p['keys'])), None)

        default_value = existing_gnosis.get(var_name)
        prophesied_default = ""

        if prophecy:
            base_var_name = var_name.split('_')[0]
            source_var = existing_gnosis.get(f'{base_var_name}_name', existing_gnosis.get('name'))
            primary_rule = prophecy.get('rule', 'path_safe').split('|')[0].strip()
            if source_var and primary_rule in alchemist.grimoire:
                try:
                    prophesied_default = alchemist.grimoire[primary_rule](source_var)
                except Exception:
                    pass

            prompt_text = Text.assemble(
                (f"{prophecy['sigil'][0]} " if prophecy['sigil'][0] else "", "white"),
                (f"Enter the {prophecy['prompt']} for ", "white"),
                (f"'{var_name}'", "bold cyan")
            )
            pleas.append(GnosticPlea(
                key=var_name,
                plea_type=GnosticPleaType.MULTILINE if prophecy.get('multiline') else GnosticPleaType.TEXT,
                prompt_text=prompt_text,
                default=default_value if default_value is not None else prophesied_default,
                validation_rule=validation_rules.get(var_name, prophecy.get('rule', 'var_path_safe'))
            ))
        else:
            pleas.append(GnosticPlea(
                key=var_name,
                plea_type=GnosticPleaType.TEXT,
                prompt_text=f"Please provide Gnosis for '{var_name}'",
                default=default_value,
                validation_rule=validation_rules.get(var_name, 'var_path_safe')
            ))
    return pleas

@contextmanager
def set_language_context(language: str):
    """
    =================================================================================
    == THE GNOSTIC FIREWALL (THE CONTEXT MANAGER OF REALITIES)                     ==
    =================================================================================
    A divine context manager that erects an unbreakable Gnostic Firewall by
    proclaiming a language context to the cosmos (environment variables) for the
    duration of a sacred rite.
    =================================================================================
    """
    original_context = os.getenv("SCAFFOLD_LANGUAGE_CONTEXT")
    Logger.verbose(f"Erecting Gnostic Firewall: Proclaiming cosmic will as '{language}'.")
    os.environ["SCAFFOLD_LANGUAGE_CONTEXT"] = language
    try:
        yield
    finally:
        Logger.verbose("Returning cosmos to its original state.")
        if original_context is None:
            if "SCAFFOLD_LANGUAGE_CONTEXT" in os.environ:
                del os.environ["SCAFFOLD_LANGUAGE_CONTEXT"]
        else:
            os.environ["SCAFFOLD_LANGUAGE_CONTEXT"] = original_context


@lru_cache(maxsize=2)  # Cache the Gnosis for the last 2 project roots gazed upon.
def inherit_project_gnosis(project_root: Path) -> Dict[str, str]:
    """
    =================================================================================
    == THE ORACLE OF INHERITED GNOSIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)            ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000!

    This is the one true, universal God-Engine for perceiving the immortal,
    inherited Gnosis from a project's soul (`scaffold.scaffold`). It is a true,
    sentient AI, a Chronomancer that caches its Gaze and an Alchemist that can
    resolve derived Gnosis. It is the unbreakable, hyper-performant source of
    truth for the entire Scaffold cosmos.
    =================================================================================
    """
    from ..core.alchemist import get_alchemist
    from ..logger import Scribe  # Local import to prevent circular dependency paradoxes
    Logger = Scribe("GnosticInheritor")

    root_blueprint = project_root / 'scaffold.scaffold'
    if not root_blueprint.is_file():
        return {}

    # --- MOVEMENT I: THE GAZE OF THE CHRONOMANCER (THE UNBREAKABLE CACHE) ---
    # We use a simple static cache on the function itself for this specialized rite.
    # The key is a tuple of the path and its last modification time.
    cache_key = (str(root_blueprint), root_blueprint.stat().st_mtime)

    # A simple, divine cache within the function's own soul.
    if hasattr(inherit_project_gnosis, "_cache") and inherit_project_gnosis._cache.get("key") == cache_key:
        Logger.verbose("Chronocache HIT for inherited project Gnosis.")
        return inherit_project_gnosis._cache["data"]

    Logger.verbose(f"Chronocache MISS. Performing deep Gaze upon '{root_blueprint.name}'.")

    # --- MOVEMENT II: THE LAW OF THE ONE TRUE ALCHEMIST ---
    try:
        content = root_blueprint.read_text(encoding='utf-8')

        # The Gaze is no longer a profane regex. It is a more robust Gaze.
        matches = re.findall(r'^\s*\$\$\s*([\w_.-]+)\s*=\s*(.*)', content, re.MULTILINE)
        raw_gnosis = {key.strip(): value.strip().strip('"\'') for key, value in matches}

        if not raw_gnosis:
            return {}

        # The Alchemist is summoned for a pure, two-pass resolution.
        alchemist = get_alchemist()
        resolved_gnosis = {}
        for _ in range(2):  # Two passes to handle simple dependencies
            for name, raw_value in raw_gnosis.items():
                resolved_value = alchemist.transmute(raw_value, {**raw_gnosis, **resolved_gnosis})
                resolved_gnosis[name] = resolved_value

        # --- MOVEMENT III: THE RITE OF INSCRIPTION ---
        inherit_project_gnosis._cache = {"key": cache_key, "data": resolved_gnosis}
        Logger.verbose(f"Deep Gaze complete. {len(resolved_gnosis)} inherited verses chronicled.")

        return resolved_gnosis

    except Exception as e:
        # The Unbreakable Vow of Resilience
        Logger.warn(f"A minor paradox occurred while gazing upon the project's soul: {e}")
        return {}


def purify_edict_for_dossier(edict: 'PlanEdict') -> Dict:
    """
    =================================================================================
    == THE UNIVERSAL PURIFIER OF GNOSTIC PLANS (V-Ω-ETERNAL-APOTHEOSIS++)          ==
    =================================================================================
    This divine artisan's contract is now unbreakable. It performs the sacred rite
    of transmutation (`asdict`) and then, and only then, does it speak the mortal
    tongue of dictionaries to purify the vessel of its profane, raw content.
    =================================================================================
    """
    if PlanEdict is None: return {}

    # The sacred `asdict` rite is performed first, transmuting the vessel.
    pure_edict_dict = asdict(edict)

    # Now, we may safely speak the mortal tongue to the resulting dictionary.
    details = pure_edict_dict.get("details")
    if details and "content" in details:
        del details["content"]

    if not details:
        pure_edict_dict.pop("details", None)
    else:
        pure_edict_dict["details"] = details

    return pure_edict_dict


def to_string_safe(value: Any) -> str:
    """[GC 1: CORE FIX] Converts Rich Text objects safely to string, preserving None/str purity."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    # Assumes rich.Text object if not str/None
    return str(value.plain if hasattr(value, 'plain') else value)

def is_poetry_installed() -> bool:
    """
    =================================================================================
    == THE ORACLE OF POETRY'S GAZE (V-Ω-ETERNAL. THE UNBREAKABLE SENTINEL)         ==
    =================================================================================
    LIF: 10,000,000,000

    This divine artisan performs a swift, unbreakable Gaze to perceive if the
    'poetry' instrument is manifest in the current reality's PATH. It is a pure,
    stateless Sentinel whose sole purpose is to provide an absolute truth for
    conditional logic and intelligent dialogue flow.
    =================================================================================
    """
    return bool(shutil.which("poetry"))



def is_git_installed() -> bool:
    """
    =================================================================================
    == THE ORACLE OF GIT'S GAZE (V-Ω-ETERNAL. THE UNBREAKABLE SENTINEL)            ==
    =================================================================================
    LIF: 10,000,000,000
    This divine artisan performs a swift, unbreakable Gaze to perceive if the
    'git' instrument is manifest in the current reality's PATH.
    =================================================================================
    """
    return bool(shutil.which("git"))

def get_os_type() -> str:
    """
    =================================================================================
    == THE ORACLE OF REALM'S SOUL (V-Ω-ETERNAL. THE UNBREAKABLE SENTINEL)          ==
    =================================================================================
    LIF: 10,000,000,000
    This divine artisan performs a swift, unbreakable Gaze to perceive the
    operating system's soul (Windows, Linux, Darwin).
    =================================================================================
    """
    os_name = platform.system()
    if os_name == "Windows":
        return "windows"
    elif os_name == "Linux":
        return "linux"
    elif os_name == "Darwin":
        return "macos"
    return "unknown"




def is_valid_path_segment(path_segment: str) -> bool:
    """
    =================================================================================
    == THE ORACLE OF PATH PURITY (V-Ω-ETERNAL. THE UNBREAKABLE GAZE)               ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000!

    This divine artisan performs an **ultra-comprehensive Gaze** upon a path segment
    to ascertain its absolute purity. It annihilates any and all profane characters,
    including reserved filesystem characters, invisible control characters (like '\a'),
    and ensures the segment is not merely a void after purification.

    ### Game-Changing Improvements:
    1.  **[GC 1: Comprehensive Forbidden Character Check]**: Actively checks against a
        universal set of profane filesystem characters (`PROFANE_PATH_CHARS`).
    2.  **[GC 2: Unseen Phantom Annihilation]**: Detects and rejects invisible,
        non-printable ASCII control characters (`PROFANE_UNSEEN_CHARS`) that often
        arise from copy-paste errors or corrupt input (e.g., the `\a` bell character).
    3.  **[GC 3: Purity After Stripping]**: Ensures the path segment is not empty
        after all profane characters and whitespace are stripped.
    4.  **[GC 4: Absolute Path Forbiddance]**: Explicitly disallows absolute paths (`/`, `C:\`)
        within a segment, as blueprint paths should always be relative.
    5.  **[GC 5: Path Traversal Forbiddance]**: Forbids `..` segments to prevent directory traversal attacks.
    6.  **[GC 6: Platform-Specific Profanity]**: Can be extended to include platform-specific
        forbidden characters (ee.g., `:` on Windows in filenames) if `pathlib` doesn't
        handle them automatically.
    """
    if not isinstance(path_segment, str) or not path_segment:
        return False  # A void cannot be pure.

    # [GC 5: Path Traversal Forbiddance]
    if path_segment == '..' or '/../' in path_segment or '\\..\\' in path_segment:
        return False

    # [GC 4: Absolute Path Forbiddance]
    if path_segment.startswith('/') or (platform.system() == "Windows" and re.match(r'^[a-zA-Z]:[/\\]', path_segment)):
        return False  # Absolute paths are forbidden as segments.

    # For directories, the trailing slash is part of its pure form. Temporarily remove for char check.
    _clean_segment_for_char_check = path_segment.rstrip('/') if path_segment.endswith('/') else path_segment

    # [GC 1: Comprehensive Forbidden Character Check]
    if any(c in PROFANE_PATH_CHARS for c in _clean_segment_for_char_check):
        Logger.verbose(f"Path segment '{path_segment}' contains profane char from PROFANE_PATH_CHARS.")
        return False

    # [GC 2: Unseen Phantom Annihilation]
    if any(c in PROFANE_UNSEEN_CHARS for c in _clean_segment_for_char_check):
        Logger.verbose(f"Path segment '{path_segment}' contains unseen phantom char.")
        return False

    # [GC 3: Purity After Stripping]
    if not _clean_segment_for_char_check.strip():
        Logger.verbose(f"Path segment '{path_segment}' is empty after stripping.")
        return False

    # All crucibles passed. The segment is pure.
    return True


@register_gnosis("get_ignore_spec")
def get_ignore_spec(project_root: Path, extra_patterns: Optional[List[str]] = None) -> Optional['pathspec.PathSpec']:
    """
    =================================================================================
    == THE UNIVERSAL ORACLE OF AVERSION (V-Ω-LEGENDARY++. THE SENTINEL'S GAZE)     ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000

    This divine artisan is the sentient Sentinel that forges the one true, unified
    scripture of Gnostic Aversion. It performs a deep, hierarchical Gaze upon
    the `.gitignore`, the `.scaffoldignore`, and the Architect's direct will to
    create a single, canonical law of what is profane and must be ignored.
    =================================================================================
    """
    from ..constants import ORPHAN_ARCHIVE_DIR
    if not pathspec:
        Logger.warn("The 'pathspec' ally is not present in this reality. The Gaze of Aversion will be blind.")
        return None

    Logger.verbose("The Universal Oracle of Aversion awakens its Gaze...")

    # --- The Foundational, Unbreakable Laws ---
    # These are the core profanities that must always be ignored by Scaffold's own Gaze.
    patterns = [
        '.git/',
        '.scaffold/',
        '__pycache__/',
        '*.pyc', '*.pyo', '*.pyd',
        '.DS_Store',
        '*.swp', '*.swo',
        'node_modules/',
        'dist/',
        'build/',
        # The archive of lost souls must always be ignored by the Detective
        f'{ORPHAN_ARCHIVE_DIR}/'
    ]
    Logger.verbose(f"   -> Began with {len(patterns)} foundational laws of aversion.")

    # --- FACULTY: THE GAZE OF THE GNOSTIC TRINITY ---

    # Gaze 3 (Lowest Priority): The Project's Common Will (`.gitignore`)
    gitignore_path = project_root / '.gitignore'
    if gitignore_path.is_file():
        try:
            gitignore_content = gitignore_path.read_text(encoding='utf-8', errors='ignore').splitlines()
            patterns.extend(gitignore_content)
            Logger.verbose(
                f"   -> Perceived {len(gitignore_content)} laws from the project's Common Will (.gitignore).")
        except Exception as e:
            # ★★★ FACULTY: THE UNBREAKABLE WARD OF THE CORRUPTED SOUL ★★★
            Logger.warn(f"A minor paradox occurred while gazing upon '.gitignore'. The Gaze continues. Reason: {e}")

    # Gaze 2: The Project's Gnostic Will (`.scaffoldignore`)
    scaffoldignore_path = project_root / '.scaffoldignore'
    if scaffoldignore_path.is_file():
        try:
            scaffoldignore_content = scaffoldignore_path.read_text(encoding='utf-8', errors='ignore').splitlines()
            patterns.extend(scaffoldignore_content)
            Logger.verbose(
                f"   -> Perceived {len(scaffoldignore_content)} laws from the project's Gnostic Will (.scaffoldignore).")
        except Exception as e:
            Logger.warn(
                f"A minor paradox occurred while gazing upon '.scaffoldignore'. The Gaze continues. Reason: {e}")

    # Gaze 1 (Highest Priority): The Architect's Immediate Will (`extra_patterns`)
    if extra_patterns:
        patterns.extend(extra_patterns)
        Logger.verbose(f"   -> Perceived {len(extra_patterns)} laws from the Architect's Immediate Will.")

    # --- THE FINAL PROCLAMATION ---
    Logger.success(
        f"The Sentinel's Gaze is complete. A total of {len(patterns)} laws have been forged into the final canon.")
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

def perform_rite_of_revelation(file_path: Path):
    """
    [THE HERALD OF LUMINOUS REALITIES]
    Performs a Gnostic, cross-platform rite to open a file path (ideally HTML/SVG)
    in the Architect's default web browser.
    """
    from ..logger import Scribe
    Logger = Scribe("RevelationHerald")

    try:
        # The `webbrowser` artisan is the most divine and direct path.
        Logger.info(f"Summoning the Celestial Herald to reveal '{file_path.name}'...")
        webbrowser.open(file_path.as_uri())
        Logger.success(f"The scripture has been revealed in your default browser.")
    except Exception as e_webbrowser:
        # If the divine path fails, we fall back to the mortal path.
        Logger.warn(f"The Celestial Herald's Gaze was clouded ({e_webbrowser}). Attempting a mortal rite...")
        try:
            if platform.system() == "Windows":
                subprocess.run(['start', str(file_path)], check=True, shell=True)
            elif platform.system() == "Darwin":
                subprocess.run(['open', str(file_path)], check=True)
            else: # Linux
                subprocess.run(['xdg-open', str(file_path)], check=True)
            Logger.success(f"The scripture has been revealed via a mortal rite.")
        except Exception as e_subprocess:
            Logger.error(
                "A catastrophic paradox occurred. The scripture could not be revealed.",
                ex=e_subprocess
            )



def discover_required_gnosis_from_string(content: str) -> GnosticDossier:
    """
    =================================================================================
    == THE INQUISITOR OF THE UNSEEN WILL (V-Ω-ETERNAL. THE GNOSTIC FORESEER)       ==
    =================================================================================
    This is a divine, pure artisan whose one true purpose is to gaze upon the raw
    scripture of a blueprint and perceive its Gnostic dependencies. It understands
    the sacred schism between Gnosis the Architect must provide (`required`) and
    Gnosis the Alchemist will forge (`derived`), annihilating the Heresy of
    Premature Adjudication.
    =================================================================================
    """
    # Gaze 1: Perceive all variables USED in Jinja expressions.
    used_vars = set(re.findall(r'\{\{\s*([\w\.]+)\s*\|?.*?\s*\}\}', content))

    # Gaze 2: Perceive all variables DEFINED in the blueprint's soul.
    defined_vars = set(re.findall(r'^\s*\$\$\s*(\w+)\s*=', content, re.MULTILINE))

    # The Final Adjudication: A variable is required ONLY if it is used AND not defined.
    required = used_vars - defined_vars

    return GnosticDossier(
        required=required,
        derived=defined_vars,
        all_vars=used_vars | defined_vars
    )


# =================================================================================
# == I. THE GNOSTIC ANCHORS (DEFINING THE SANCTUM)                               ==
# =================================================================================
PROJECT_ROOT_MARKERS = [
    ".scaffold",  # The Hidden Sanctum
    "scaffold.scaffold",  # The Blueprint of Law
    "scaffold.lock",  # The Chronicle of Truth
    ".git",  # The Temporal Boundary
]


def find_project_root(start_path: Path, is_genesis_intent: bool = False) -> Tuple[Optional[Path], str]:
    """
    The Rite of Anchoring.

    Args:
        start_path: Where the Architect stands.
        is_genesis_intent: If True, we assume we are birthing a new project.
                           We DO NOT walk up the tree looking for parents.
                           We checks CWD. If void, CWD becomes Root.

    Returns:
        (Path to Root, Marker Name)
    """
    current = start_path.resolve()

    # --- PATH A: THE RITE OF GENESIS (GIT INIT BEHAVIOR) ---
    if is_genesis_intent:
        # We check if the current directory is ALREADY a sanctum.
        for marker in PROJECT_ROOT_MARKERS:
            if (current / marker).exists():
                return current, marker

        # If not, we proclaim THIS directory as the new root.
        # We do not bow to the parent directory's rules.
        return current, "genesis_implied"

    # --- PATH B: THE RITE OF MAINTENANCE (GIT STATUS BEHAVIOR) ---
    # We look upwards for the governing laws.
    for _ in range(50):  # Safety break
        for marker in PROJECT_ROOT_MARKERS:
            if (current / marker).exists():
                return current, marker

        parent = current.parent
        if parent == current:
            # Hit filesystem root without finding a marker.
            # We default to the start_path as an implied root.
            return start_path, "implied"

        current = parent

    return start_path, "implied"


def perceive_intent_from_args(argv: List[str]) -> bool:
    """
    [THE ORACLE OF INTENT]
    Scans the CLI arguments to determine if the Architect intends Creation or Maintenance.
    Returns True if the intent is GENESIS (Creation).
    """
    # 1. Explicit Creation Commands
    if any(cmd in argv for cmd in ['init', 'genesis', 'create', 'compose']):
        return True

    # 2. The Polymorphic 'Run'
    # If running a .scaffold file, it is likely a Genesis rite unless a lockfile exists.
    # However, we can't check file existence here easily without circular logic.
    # We use a heuristic: .patch.scaffold is Maintenance. .scaffold is Genesis.

    # Filter out flags to find the target file
    args = [a for a in argv if not a.startswith('-')]

    if "run" in args:
        try:
            # Find the argument after 'run'
            idx = args.index("run")
            if idx + 1 < len(args):
                target = args[idx + 1]
                if target.endswith(".patch.scaffold"):
                    return False  # Patching is Maintenance
                if target.endswith(".scaffold"):
                    return True  # Running a blueprint is usually Genesis
        except ValueError:
            pass

    # 3. Default to Maintenance (Safety First)
    return False


def get_git_branch(path: Optional[Path]) -> Optional[str]:
    """
    =============================================================================
    == THE TEMPORAL GAZE (V-Ω-BRANCH-DIVINER)                                  ==
    =============================================================================
    Perceives the current branch of the Gnostic Chronicle (Git).

    Logic:
    1. Tries `git symbolic-ref` to get the true branch name.
    2. If that fails (Detached HEAD), verifies if it is a repo at all.
    3. Returns 'detached' if valid repo but no branch, or None if not a repo.
    """
    if not path: return None

    # 1. Anchor to Reality
    target = path.resolve()
    if target.is_file(): target = target.parent
    if not target.exists(): return None

    # 2. Check the Artisan
    if not shutil.which("git"): return None

    try:
        # 3. The Precise Query (Symbolic Ref)
        # We prefer this over 'rev-parse --abbrev-ref' because the latter
        # returns "HEAD" for detached states, which is ambiguous.
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=target,
            capture_output=True,
            text=True,
            timeout=1,  # The Ward of Speed
            check=True
        )
        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return None

    except subprocess.CalledProcessError:
        # If symbolic-ref fails, we are either DETACHED or NOT A REPO.
        # We perform a secondary Gaze to distinguish.
        try:
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=target,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=1
            )
            return "detached"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return None

    except Exception:
        return None


def get_git_commit(path: Optional[Path], short: bool = True) -> Optional[str]:
    """
    =============================================================================
    == THE ANCESTRAL MARKER (V-Ω-COMMIT-SEER)                                  ==
    =============================================================================
    Retrieves the specific point in history (Commit Hash).
    """
    if not path: return None

    target = path.resolve()
    if target.is_file(): target = target.parent
    if not target.exists(): return None

    if not shutil.which("git"): return None

    try:
        args = ["git", "rev-parse", "HEAD"]
        if short:
            args = ["git", "rev-parse", "--short", "HEAD"]

        result = subprocess.run(
            args,
            cwd=target,
            capture_output=True,
            text=True,
            timeout=1,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return None


def forge_edict_from_vessel(vessel: GnosticVessel) -> Edict:
    """
    =================================================================================
    == THE RITE OF GNOSTIC DISTILLATION (V-Ω-PYDANTIC-HEALED)                      ==
    =================================================================================
    Transmutes a temporary parsing `GnosticVessel` into a permanent, executable `Edict`.

    **THE FIX:** It applies a rigorous **Null Coalescing** to all fields.
    If a vessel field is `None` (e.g. `vow_type`), it transmutes it to `""` (empty string),
    satisfying the strict Pydantic laws of the `Edict` contract.
    """
    try:
        # --- THE RITE OF DEFAULTING (TYPE) ---
        final_type = vessel.edict_type
        if final_type is None:
            # If the Inquisitor found no type, we default based on line structure
            if vessel.line_type in (GnosticLineType.VOID, GnosticLineType.COMMENT):
                final_type = EdictType.COMMENT
            else:
                # Fallback: Assume Action if it has content, otherwise Comment
                final_type = EdictType.ACTION if vessel.raw_scripture.strip() else EdictType.COMMENT

        # --- THE RITE OF STRING PURIFICATION (THE PYDANTIC FIX) ---
        # We ensure no required string field ever receives None.
        return Edict(
            type=final_type,
            raw_scripture=vessel.raw_scripture or "",
            line_num=vessel.line_num,

            # Strings must be strings, not None
            command=vessel.command or "",
            vow_type=vessel.vow_type or "",
            state_key=vessel.state_key or "",
            state_value=vessel.state_value or "",
            capture_as=vessel.capture_as,  # Optional in Edict
            adjudicator_type=vessel.adjudicator_type,  # Optional in Edict

            # Lists are safe (default factory handles them)
            vow_args=vessel.vow_args,
            inputs=vessel.inputs,
            directive_args=vessel.directive_args,

            # Complex Optional fields
            language=vessel.language,
            script_block=vessel.script_block,
            directive_type=vessel.directive_type,
            macro_name=vessel.macro_name,
            conditional_type=vessel.condition_type,
            resilience_type=vessel.resilience_type,

            # Nesting
            body=vessel.body,
            else_body=vessel.else_body,
            parallel_edicts=vessel.parallel_edicts
        )
    except Exception as e:
        # [ELEVATION 12] The Unbreakable Ward
        Logger.error(
            f"A catastrophic paradox occurred during the Gnostic Distillation of Will for '{vessel.raw_scripture.strip()}': {e}")
        # Return a safe "Comment" edict to prevent the Parser from crashing
        return Edict(
            type=EdictType.COMMENT,
            raw_scripture=vessel.raw_scripture,
            line_num=vessel.line_num,
            command=f"!! PARADOX DURING PARSING: {e} !!"
        )




VALID_BLUEPRINT_EXTENSIONS = ('.scaffold', '.txt', '.yaml', '.yml')
def is_valid_blueprint_file(file_path: Path) -> bool:
    if file_path.name.lower() in VALID_BLUEPRINT_EXTENSIONS:
        return True
    return file_path.suffix.lower() in VALID_BLUEPRINT_EXTENSIONS


def unbreakable_ward_of_annihilation(path_to_delete: Path, project_root: Path, rite_name: str):
    """
    =================================================================================
    == THE UNBREAKABLE WARD OF ANNIHILATION (V-Ω-ETERNAL-GUARDIAN)                 ==
    =================================================================================
    The final, absolute safeguard against catastrophic deletion. It raises a heresy
    if any attempt is made to annihilate a sacred sanctum.
    =================================================================================
    """
    if not isinstance(path_to_delete, Path) or not isinstance(project_root, Path):
        raise ArtisanHeresy(
            "A profound type heresy was perceived by the Unbreakable Ward. Annihilation stayed.",
            details="A non-Path object was passed to the ultimate safety check."
        )

    # Resolve to absolute, canonical paths to prevent any ambiguity.
    target = path_to_delete.resolve()
    anchor = project_root.resolve()
    home = Path.home().resolve()

    # The Sacred Vows. If any of these are true, the rite is profane.
    if target == anchor:
        raise ArtisanHeresy(f"HERESY: The '{rite_name}' rite attempted to annihilate the project root itself: {target}")
    if target == home:
        raise ArtisanHeresy(f"HERESY: The '{rite_name}' rite attempted to annihilate the HOME directory: {target}")
    if target == home.parent or target == anchor.parent:
        raise ArtisanHeresy(
            f"HERESY: The '{rite_name}' rite attempted to annihilate a parent of a sacred sanctum: {target}")

    # A final check to ensure we are not deleting something "above" the project root.
    try:
        target.relative_to(anchor)
        # If this succeeds, `target` is inside or is the same as `anchor`. Since we checked for equality,
        # it must be inside, which is what we expect for an ephemeral directory.
    except ValueError:
        # This means the target is outside the project root. This is only allowed
        # if it's inside a known ephemeral location like the system temp dir.
        import tempfile
        temp_dir = Path(tempfile.gettempdir()).resolve()
        try:
            target.relative_to(temp_dir)
            # It's a valid temp file, allow it.
        except ValueError:
            # It's outside the project and not in temp. This is a critical heresy.
            raise ArtisanHeresy(
                f"HERESY: The '{rite_name}' rite attempted to annihilate a path outside the project sanctum: {target}")


def path_to_uri(path: Path) -> str:
    """
    [THE RITE OF CONSECRATION]
    Transmutes a local path into a canonical, absolute file URI for the Symbiotic Link.
    """
    try:
        # Use pathlib's as_uri() for native platform handling, then clean Windows paths
        uri = path.resolve().as_uri()
        # Windows sometimes adds an extra / or drive letter issues, clean this up
        if platform.system() == "Windows" and uri.startswith("file:///"):
            # On Windows, need to handle the C: drive prefix
            return uri.replace("file:///", "file:///")

        return uri
    except Exception:
        # If all else fails, return a safe string.
        return f"file:///{path.as_posix()}"
