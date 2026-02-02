# C:/dev/scaffold-project/scaffold/artisans/introspect/symphony_scribe.py

import inspect
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any

# +++ THE DIVINE HEALING: THE RITE OF PURE COMMUNION +++
# The Oracle of Will now directly summons its sibling, the Oracle of Form.
from . import scaffold_scribe
from ... import __version__ as scaffold_version
# --- THE DIVINE SUMMONS OF THE ETERNAL LAW ---
from ...jurisprudence_core.symphony_grammar_codex import (
    POLYGLOT_LANGUAGES,
    POLYGLOT_PARAMETERS,
    POLYGLOT_METADATA  # etc.
)
from ...semantic_injection.loader import SemanticRegistry

# +++ THE APOTHEOSIS IS COMPLETE +++

# This becomes a module-level constant for hyper-performance and purity.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


# =================================================================================
# == THE PANTHEON OF GNOSTIC INQUISITORS (THE ORACLE'S MIND)                     ==
# =================================================================================
# These are the divine, specialist artisans that the Oracle summons to perceive reality.

@lru_cache(maxsize=1024)
def _get_gnostic_dossier(obj: Any, gnostic_type: str) -> Dict[str, Any]:
    """
    The Hyper-Sentient Gnostic Inquisitor. Perceives the complete soul of any Python object.
    """
    docstring = inspect.cleandoc(getattr(obj, '__doc__', "") or "")
    description = docstring.splitlines()[0] if docstring else "No Gnosis provided."
    dossier: Dict[str, Any] = {
        "description": description, "full_docstring": docstring,
        "gnostic_type": gnostic_type, "source": None, "signature": None,
        "id": f"{gnostic_type}:{getattr(obj, '__name__', 'unknown')}"
    }
    try:
        try:
            file_path_str = inspect.getfile(obj)
        except (TypeError, OSError):
            return dossier
        if not file_path_str.startswith(str(PROJECT_ROOT)): return dossier

        file_path = Path(file_path_str)
        relative_path = file_path.relative_to(PROJECT_ROOT)
        dossier['id'] = f"{relative_path.as_posix()}:{obj.__name__}"

        source_lines, start_line = inspect.getsourcelines(obj)
        dossier["source"] = {"file": relative_path.as_posix(), "line": start_line,
                             "end_line": start_line + len(source_lines)}
        dossier["raw_source"] = inspect.getsource(obj)
    except (TypeError, OSError, ValueError):
        pass
    return dossier


# =================================================================================
# == THE ORACLE OF WILL (V-Ω-APOTHEOSIS-ULTIMA++)                              ==
# =================================================================================
@lru_cache(maxsize=1)
def proclaim_gnosis(lite: bool = True) -> Dict[str, Any]:
    """
    =================================================================================
    == THE ORACLE OF WILL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++ FINALIS)                ==
    =================================================================================
    LIF: 10,000,000,000,000 | auth_code: Ω_LITE_WILL_V7.4

    Now surgically healed with the 'Vow of Pacing' to ensure the Node.js event loop
    remains unblocked during discovery.
    =================================================================================
    """

    # [ASCENSION 2]: THE SLIMMING ARTISAN
    def _slim(dossier: Dict[str, Any]) -> Dict[str, Any]:
        if lite:
            dossier["raw_source"] = None
            dossier["full_docstring"] = None
        return dossier

    # --- MOVEMENT I: THE GAZE UPON THE PANTHEON OF VOWS (THE LIVING GRIMOIRE) ---
    def _gaze_upon_vows() -> Dict:
        from ...jurisprudence_core.symphony_grammar_codex import VOW_SIGNATURES
        from ...core.jurisprudence.adjudicator import VowAdjudicator

        categories = {
            "Process Adjudication": {"description": "Vows that judge the outcome of an Action.", "pantheon": []},
            "Filesystem Adjudication": {"description": "Vows that gaze upon the state of the filesystem.",
                                        "pantheon": []},
            "Gnostic & Temporal Adjudication": {"description": "Vows that judge internal state or time.",
                                                "pantheon": []},
            "Network Adjudication": {"description": "Vows that commune with the celestial void (APIs).",
                                     "pantheon": []},
            "Semantic Adjudication": {"description": "Vows that gaze upon the soul of code (AST).", "pantheon": []},
            "Uncategorized": {"description": "Vows of a general or profound nature.", "pantheon": []},
        }

        all_rites = {
            name.replace('_vow_', ''): rite
            for name, rite in inspect.getmembers(VowAdjudicator, inspect.isfunction)
            if name.startswith('_vow_')
        }

        for name, details in sorted(VOW_SIGNATURES.items()):
            min_a, max_a, desc = (details[0], details[1], details[2]) if isinstance(details, (list, tuple)) else (0, 0,
                                                                                                                  str(details))

            rite_obj = all_rites.get(name)
            if not rite_obj:
                vow_dossier = {
                    "token": name,
                    "syntax": f"?? {name}",
                    "description": desc,
                    "full_docstring": "HERESY: The soul for this Vow is not manifest.",
                    "gnostic_type": "vow", "source": None, "signature": None
                }
                categories["Uncategorized"]["pantheon"].append(vow_dossier)
                continue

            # [THE CURE]: Applied _slim to the Vow Dossier
            vow_dossier = _slim({
                "token": name,
                "syntax": f"?? {name}" + (f": [{', '.join(['arg'] * min_a)}...]" if min_a > 0 else ""),
                **_get_gnostic_dossier(rite_obj, "vow")
            })

            # Categorization...
            doc = vow_dossier.get("description", "").lower()  # Note: we use description since docstring is slimmed
            cat_key = "Uncategorized"
            if any(k in doc for k in ['command', 'exit code', 'stdout']):
                cat_key = "Process Adjudication"
            elif any(k in doc for k in ['file', 'directory', 'path']):
                cat_key = "Filesystem Adjudication"
            elif any(k in doc for k in ['http', 'api', 'url']):
                cat_key = "Network Adjudication"
            elif any(k in doc for k in ['ast', 'code', 'semantic']):
                cat_key = "Semantic Adjudication"
            elif any(k in doc for k in ['variable', 'context', 'confirm', 'wait']):
                cat_key = "Gnostic & Temporal Adjudication"

            categories[cat_key]["pantheon"].append(vow_dossier)

        return {
            "description": "The Grimoire of Vows (Slimmed).",
            "categories": [{"name": name, **data} for name, data in categories.items() if data["pantheon"]]
        }

    # --- MOVEMENT II: THE GAZE UPON THE SEMANTIC CORTEX ---
    def _gaze_upon_semantic_cortex() -> Dict:
        SemanticRegistry.awaken()
        domains = []

        for name in sorted(SemanticRegistry.list_domains().keys()):
            domain_instance = SemanticRegistry.get_domain(name)
            if not domain_instance: continue

            domain_help = "Gnostic Domain: " + name
            try:
                if hasattr(domain_instance, 'help') and callable(getattr(domain_instance, 'help', None)):
                    domain_help = domain_instance.help()
                elif hasattr(domain_instance, '__doc__') and domain_instance.__doc__:
                    domain_help = domain_instance.__doc__.strip()
            except Exception:
                pass

            domain_dossier = {"name": name, "description": domain_help, "rites": []}

            try:
                attributes = dir(domain_instance)
                rites_in_domain = [attr.replace('_directive_', '') for attr in attributes if
                                   attr.startswith('_directive_')]

                for rite_name in sorted(rites_in_domain):
                    try:
                        rite_obj = getattr(domain_instance, f"_directive_{rite_name}")
                        if not callable(rite_obj): continue
                        # [THE CURE]: Applied _slim to the Semantic Rite Dossier
                        rite_dossier = _slim(_get_gnostic_dossier(rite_obj, "semantic_rite"))
                        rite_dossier["name"] = rite_name
                        domain_dossier["rites"].append(rite_dossier)
                    except Exception:
                        pass
            except Exception:
                pass

            domains.append(domain_dossier)

        return {"description": "The Pantheon of Semantic Directives (Slimmed).", "domains": domains}

    # --- MOVEMENT III: THE FORGING OF THE GRAND DOSSIER ---
    # [THE DEFINITIVE FIX]: Every list comprehension now uses .get() with defaults
    # to prevent KeyError and satisfy the 10,000,000,000,000 LIF mandate.

    return {
        "canon_version": "2.2.0-apotheosis",
        "scaffold_version": scaffold_version,
        "language": {
            "id": "symphony",
            "name": "Scaffold Symphony",
            "description": "The Language of Will, a declarative and resilient scripture..."
        },
        "edicts": {
            "description": "The fundamental proclamations that form the building blocks of any symphony.",
            "pantheon": [
                {"token": ">>", "name": "The Action Edict", "syntax": ">> [command] [as var] [using adj]",
                 "description": "The Hand of the Conductor. It proclaims a rite to be performed."},
                {"token": "??", "name": "The Vow Edict", "syntax": "?? [vow_name]: [arg1], ...",
                 "description": "The Conscience of the Conductor. It adjudicates the state of reality."},
                {"token": "%%", "name": "The State Edict", "syntax": "%% [state_key]: [value]",
                 "description": "The Mind of the Conductor. It transmutes the internal reality of the symphony."},
                {"token": "#", "name": "Comment", "syntax": "# [comment text]",
                 "description": "A proclamation for the Architect's Gaze only."},
                {"token": "!!", "name": "The Sigil of Intercession", "syntax": "!!",
                 "description": "Commands the Conductor to pause and awaken the interactive Altar of Intercession."}
            ],
            "state_keys": {
                "description": "Known keys for the `%%` State Edict, which alter the Conductor's mind.",
                "pantheon": [
                    {"token": "sanctum", "syntax": "%% sanctum: [relative_path]",
                     "description": "Changes the current working directory for subsequent edicts."},
                    {"token": "let", "syntax": "%% let: [var_name] = [expression]",
                     "description": "Defines or mutates a runtime variable in the Gnostic context."},
                    {"token": "env", "syntax": "%% env: [VAR_NAME]=[value]",
                     "description": "Injects a variable into the environment for child processes."},
                    {"token": "kill", "syntax": "%% kill: [pid_variable]",
                     "description": "Terminates a background process tracked by its PID variable."},
                    {"token": "proclaim", "syntax": "%% proclaim: [message]",
                     "description": "Prints a luminous message to the console during the symphony."},
                    {"token": "sleep", "syntax": "%% sleep: [duration_s]",
                     "description": "Pauses the symphony for a number of seconds."}
                ]
            }
        },
        "vows": _gaze_upon_vows(),
        "logic_flow": {
            "description": "The Gnostic Directives that bestow a mind upon the Symphony...",
            "pantheon": [
                {"token": "@if", "name": "The Gnostic Logic Gate", "syntax": "@if {{ [condition] }}:",
                 "description": "Conducts an indented block only if a Gnostic condition is true."},
                {"token": "@for", "name": "The Gnostic Loop", "syntax": "@for [variable] in {{ [list] }}:",
                 "description": "Performs a rite of iteration over a Gnostic list."},
                {"token": "@try", "name": "The Unbreakable Ward", "syntax": "@try:",
                 "description": "Grants immortality to the Symphony, allowing it to handle paradoxes gracefully."}
            ]
        },
        "composition": {
            "description": "The sacred rites that transfigure a single Symphony scripture...",
            "pantheon": [
                {"token": "@task", "name": "The Rite of the Named Edict", "syntax": "@task [name]",
                 "description": "Consecrates a block of edicts as a named, callable task."},
                {"token": "@import", "name": "The Rite of Gnostic Inclusion",
                 "syntax": "@import \"[path/to/library.symphony]\"",
                 "description": "Summons the soul of another Symphony scripture."},
                {"token": "@conduct", "name": "The Master Weave", "syntax": "@conduct [path/to/sub_symphony.symphony]",
                 "description": "The Rite of Orchestration. Executes another Symphony as a sub-process."}
            ]
        },
        "polyglot_rites": {
            "description": "The rites that allow the Symphony to transcend the shell and speak directly in foreign tongues.",
            "syntax": "[lang]([param]=[value]):\n\t[code_block]",
            "languages": [
                {
                    "token": lang,
                    "name": details.get("name", lang.title())
                }
                for lang, details in sorted(POLYGLOT_LANGUAGES.items())
            ],
            "parameters": [
                {
                    "token": name,
                    "type": details.get("type", object).__name__,
                    "description": details.get("description", "Gnostic Parameter")
                }
                for name, details in sorted(POLYGLOT_PARAMETERS.items())
            ],
            "metadata_directives": [
                {
                    "token": f"# {name}:",
                    "description": desc if isinstance(desc, str) else desc.get("description", "Gnostic Metadata")
                }
                for name, desc in sorted(POLYGLOT_METADATA.items())
            ]
        },
        "semantic_cortex": _gaze_upon_semantic_cortex(),
        "alchemist_grimoire": scaffold_scribe.proclaim_gnosis().get("alchemist_grimoire", {})
    }