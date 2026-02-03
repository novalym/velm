# C:/dev/scaffold-project/scaffold/artisans/introspect/scaffold_scribe.py

import inspect
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any

from ... import __version__ as scaffold_version
from ...core.alchemist import get_alchemist
from ...jurisprudence_core.scaffold_grammar_codex import ALLOWED_VAR_TYPES
from ...semantic_injection.loader import SemanticRegistry

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@lru_cache(maxsize=1024)
def _get_gnostic_dossier(obj: Any, gnostic_type: str) -> Dict[str, Any]:
    """
    =================================================================================
    == THE HYPER-SENTIENT GNOSTIC INQUISITOR (V-Ω-ETERNAL-APOTHEOSIS-FINALIS)      ==
    =================================================================================
    @gnosis:title The Gnostic Inquisitor
    @gnosis:summary The final, ultra-definitive rite of object introspection.
    @gnosis:LIF INFINITY
    @gnosis:auth_code: )#(@()#@()#

    This divine artisan performs the Grand Inquest upon a Python soul. It has been
    bestowed with the 'Ward of Prudence', preventing it from attempting to
    materialize the source of built-ins or foreign scriptures which causes
    temporal stasis (hangs) in the Windows/Miniconda realm.
    =================================================================================
    """
    # --- MOVEMENT I: THE PRE-FLIGHT GAZE (THE WARD OF PRUDENCE) ---
    # Fast exit for souls that have no physical manifestation or belong to the C-Void.
    if inspect.isbuiltin(obj) or not hasattr(obj, '__module__'):
        return {
            "description": "Built-in or C-Extension soul.",
            "full_docstring": "Gnosis is encapsulated in the binary void.",
            "gnostic_type": gnostic_type,
            "source": None, "signature": None, "raw_source": None,
            "id": f"{gnostic_type}:{getattr(obj, '__name__', 'built-in')}"
        }

    docstring = inspect.cleandoc(getattr(obj, '__doc__', "") or "")
    description = docstring.splitlines()[0] if docstring else "No Gnosis provided."

    dossier: Dict[str, Any] = {
        "description": description,
        "full_docstring": docstring,
        "gnostic_type": gnostic_type,
        "source": None,
        "signature": None,
        "raw_source": None,
        "id": f"{gnostic_type}:{getattr(obj, '__name__', 'unknown')}"
    }

    try:
        # --- MOVEMENT II: THE GAZE OF JURISDICTIONAL PURITY ---
        # We determine the scripture's home before attempting to read its soul.
        try:
            file_path_str = inspect.getfile(obj)
        except (TypeError, OSError):
            return dossier  # Soul is ephemeral or dynamic

        # [FACULTY: THE SINGULARITY ANCHOR]
        # If the scripture dwells outside our project root, we do not attempt
        # to extract its raw source, as it belongs to another god (3rd party lib).
        if not file_path_str.startswith(str(PROJECT_ROOT)):
            return dossier

        file_path = Path(file_path_str)
        relative_path = file_path.relative_to(PROJECT_ROOT)
        dossier['id'] = f"{relative_path.as_posix()}:{obj.__name__}"

        # --- MOVEMENT III: THE SURGICAL EXTRACTION ---
        # We use the lines we've already found to forge the raw_source,
        # avoiding a redundant and potentially hanging 'inspect.getsource' call.
        source_lines, start_line = inspect.getsourcelines(obj)

        dossier["source"] = {
            "file": relative_path.as_posix(),
            "line": start_line,
            "end_line": start_line + len(source_lines)
        }

        # Transmute the list of lines back into a single, pure scripture.
        dossier["raw_source"] = "".join(source_lines)

    except (TypeError, OSError, ValueError, RecursionError):
        # The Gaze is gracefully averted if a paradox is encountered.
        pass

    # --- MOVEMENT IV: THE SIGNATURE ALCHEMIST ---
    try:
        sig = inspect.signature(obj)

        def _format_annotation(anno: Any) -> str:
            if anno is inspect.Parameter.empty: return "Any"
            # Support complex types like Union, Optional, etc.
            return str(anno).replace("typing.", "")

        def _format_default(val: Any) -> Any:
            # We must not allow the default value to trigger its own introspection.
            if val is inspect.Parameter.empty: return None
            try:
                return str(val) if not isinstance(val, (int, float, bool, str)) else val
            except:
                return "<Complex Value>"

        dossier["signature"] = {
            "return_annotation": _format_annotation(sig.return_annotation),
            "parameters": [
                {
                    "name": param.name,
                    "annotation": _format_annotation(param.annotation),
                    "default": _format_default(param.default),
                    "kind": str(param.kind)
                }
                for param in sig.parameters.values()
            ]
        }
    except (ValueError, TypeError):
        # A ward for souls whose signature is too complex for the mortal mind.
        pass

    return dossier


def proclaim_gnosis(lite: bool = True) -> Dict[str, Any]:
    """
    [ASCENSION]: Restores the registry list with SMART-FULL logic.
    """
    if not SemanticRegistry._is_loaded:
        SemanticRegistry.awaken()

    semantic_domains = SemanticRegistry.list_domains()
    semantic_directives = []
    for domain, handler in SemanticRegistry._domains.items():
        directives = [f"@{domain}/{d.replace('_directive_', '')}" for d in dir(handler) if d.startswith('_directive_')]
        semantic_directives.extend(directives)

    alchemist = get_alchemist()

    # [THE CURE]: Metadata is Full, Source is Lazy.
    # This allows the 105 Rites to be manifest without bloating the JSON.
    def _dossier_stub(name: str, obj: Any, gtype: str) -> Dict:
        doc = inspect.getdoc(obj) or "No Gnosis provided."
        return {
            "name": name,
            "description": doc.splitlines()[0],
            "full_docstring": doc if not lite else None,  # Include full docs but not source
            "gnostic_type": gtype,
            "signature_string": f"{name}()",
            "raw_source": None  # Always lazy-load source via a separate 'resolveSource' rite
        }

    filters = [_dossier_stub(n, f, "filter") for n, f in sorted(alchemist.env.filters.items())]
    functions = [_dossier_stub(n, f, "function") for n, f in sorted(alchemist.env.globals.items()) if
                 callable(f) and not n.startswith('_')]


    return {
        "canon_version": "2.1.0",
        "scaffold_version": scaffold_version,
        "language": {
            "id": "scaffold",
            "name": "Scaffold Blueprint",
            "description": "The Language of Form, a declarative scripture for defining the static structure and soul of a new reality."
        },
        "sigils": [
            {
                "token": "::",
                "name": "Inline Content",
                "description": "Inscribes a single-line or multi-line soul (content) directly into a scripture. This is the highest Gnostic precedence for content.",
                "usage": "[path] :: \"...\" or [path] :: \"\"\"...\"\"\"",
                "example": {
                    "scripture": 'config.yml :: "version: 1.0.0"',
                    "proclamation": "Forges a `config.yml` file containing the string `version: 1.0.0`."
                }
            },
            {
                "token": "<<",
                "name": "External Seed",
                "description": "Seeds a scripture's soul from an external file. The content of the seed file is subject to Alchemical Transmutation (variable injection).",
                "usage": "[path] << [path/to/seed_file]",
                "example": {
                    "scripture": 'Dockerfile << ./seeds/python.dockerfile',
                    "proclamation": "Forges a `Dockerfile` whose content is a copy of the `./seeds/python.dockerfile` file."
                }
            },
            {
                "token": "%%",
                "name": "Permissions / Maestro's Will",
                "description": "A dual-souled sigil. When used on a scripture line, it bestows executable permissions (e.g., `%% 755`). When used as a block header, it begins the Maestro's Edicts (`%% post-run`), an automation block executed after creation.",
                "usage": "[path] :: \"...\" %% 755  OR  %% post-run",
                "example": {
                    "scripture": 'scripts/deploy.sh %% 755',
                    "proclamation": "Makes the `deploy.sh` scripture executable."
                }
            },
            {
                "token": "$$",
                "name": "Variable Definition",
                "description": "Defines a Gnostic variable, the foundational Gnosis for the Divine Alchemist to perform its transmutations. This is the primary method for making blueprints dynamic.",
                "usage": "$$ [name]: [type] = [value]",
                "example": {
                    "scripture": '$$ project_name: str = "sentinel-api"',
                    "proclamation": "Defines a variable named `project_name` with the value `sentinel-api`."
                }
            },
            {
                "token": "#",
                "name": "Comment / Gnostic Meta-Tag",
                "description": "A proclamation for the Architect's Gaze only. It can also be used for Gnostic Meta-Tags (e.g., `# @description: ...`) which are perceived by other artisans like the `weave` Altar.",
                "usage": "# [comment text]",
                "example": {
                    "scripture": '# This is a sacred scripture.',
                    "proclamation": "The line is ignored by the Creator but perceived by the Oracle."
                }
            }
        ],
        "variables": {
            "description": "The system for injecting dynamic Gnosis into the blueprint, allowing for reusable and context-aware architectural patterns.",
            "definition": {
                "token": "$$",
                "syntax": "$$ [variable_name]: [type] = [value]",
                "notes": "The type hint is optional but recommended for clarity and future tooling.",
                "allowed_types": sorted(list(ALLOWED_VAR_TYPES))
            },
            "usage": {
                "token": "{{ ... }}",
                "syntax": "{{ [variable_name] | [filter] }}",
                "description": "The sacred vessel for Alchemical Transmutation. Used in paths, filenames, and content to inject the resolved value of a variable."
            },
            "dynamic_sources": [
                {
                    "token": "${...}",
                    "name": "Environment Gnosis",
                    "syntax": "${[ENV_VAR_NAME]:[default_value]}",
                    "description": "Summons a variable from the system environment at the moment of creation. The default value is used if the environment variable is a void. This is the sacred rite for injecting secrets.",
                    "example": {
                        "scripture": '$$ db_password = ${DB_PASS:"default_secret"}',
                        "proclamation": "The `db_password` variable will be filled by the `DB_PASS` environment variable, or `default_secret` if it's not set."
                    }
                },
                {
                    "token": "$(...)",
                    "name": "Command Gnosis",
                    "syntax": "$([shell_command])",
                    "description": "Summons Gnosis from the living voice of the mortal realm. The standard output of the shell command is captured and used as the variable's value. This is a rite of profound power and must be conducted with care.",
                    "example": {
                        "scripture": '$$ git_branch = $(git rev-parse --abbrev-ref HEAD)',
                        "proclamation": "The `git_branch` variable will be filled with the name of the current Git branch."
                    }
                }
            ]
        },
        "directives": {
            "description": "Sacred edicts beginning with the `@` sigil that bestow Gnostic logic, modularity, and validation upon a blueprint, transforming it into an intelligent architectural program.",
            "pantheon": [
                {
                    "token": "@include",
                    "name": "The Gnostic Includer",
                    "syntax": "@include \"[relative/path/to/fragment.scaffold]\"",
                    "description": "Performs a rite of Gnostic Composition. The scripture and soul of another blueprint are summoned and woven into the current reality at the point of invocation. This is the key to creating a modular, reusable library of architectural patterns.",
                    "example": {
                        "scripture": 'src/api/ ::\n    @include "./api_v1.scaffold"',
                        "proclamation": "The entire structure defined in `api_v1.scaffold` will be materialized inside the `src/api/` directory."
                    }
                },
                {
                    "token": "@if / @elif / @else / @endif",
                    "name": "The Logic Gate",
                    "syntax": "@if {{ [condition] }}\n\t...\n@elif {{ [condition] }}\n\t...\n@else\n\t...\n@endif",
                    "description": "A sacred Logic Gate that forges an entire sub-tree of reality only if a Gnostic condition is true. The condition is a pure Jinja2 expression. This is the primary rite for creating adaptive, multi-purpose blueprints.",
                    "example": {
                        "scripture": '@if {{ use_docker }}\n    Dockerfile\n@endif',
                        "proclamation": "The `Dockerfile` will only be created if the `use_docker` variable is true."
                    }
                },
                {
                    "token": "if ... ->",
                    "name": "The Single-Line Guard",
                    "syntax": "@if {{ [condition] }} -> [path/to/item]",
                    "description": "A concise form of the Logic Gate for a single scripture or sanctum. It is a vow that a reality should exist only if a condition is met, without the need for a closing `@endif`.",
                    "example": {
                        "scripture": '@if {{ create_env_file }} -> .env.example',
                        "proclamation": "The `.env.example` file will be created only if `create_env_file` is true."
                    }
                },
                {
                    "token": "@def",
                    "name": "Variable Definition (Alias)",
                    "syntax": "@def [name] = [value]",
                    "description": "A stylistic alias for the `$$` sigil, preferred by some Architects for its aesthetic harmony with other `@` directives. Its Gnostic function is identical.",
                    "example": {
                        "scripture": '@def api_version = "v2"',
                        "proclamation": "Defines a variable named `api_version`."
                    }
                },
                {
                    "token": "@error / @warn / @print",
                    "name": "The Build-Time Messengers",
                    "syntax": "@[level] \"[message]\"",
                    "description": "Allows the blueprint to speak directly to the Architect during the parsing phase. `@error` is a heresy that halts the symphony. `@warn` proclaims a non-critical paradox. `@print` proclaims simple Gnosis.",
                    "example": {
                        "scripture": '@if not {{ project_name }}\n    @error "A sacred name must be proclaimed!"\n@endif',
                        "proclamation": "The creation rite will fail with a luminous error if the `project_name` variable is a void."
                    }
                }
            ]
        },
        "automation": {
            "description": "The system for inscribing executable Will into a blueprint, allowing for fully automated, one-command project setup.",
            "pantheon": [
                {
                    "token": "%% post-run",
                    "name": "The Maestro's Edicts",
                    "syntax": "%% post-run\n\t[command_1]\n\t[command_2]",
                    "description": "Begins a block of shell commands that will be conducted sequentially inside the newly forged project's root directory, but only if the entire symphony of creation completes without heresy. This is the sacred rite for initializing Git, installing dependencies, and conducting initial builds.",
                    "example": {
                        "scripture": "%% post-run\n\tgit init\n\tnpm install",
                        "proclamation": "After all files are created, `git init` and `npm install` will be executed."
                    }
                },
                {
                    "token": "%% weave",
                    "name": "The Master Weave",
                    "syntax": "%% weave [archetype_name] [target_dir] --set [key=value]",
                    "description": "A divine edict within an Orchestration Blueprint. It summons the `weave` artisan to conduct a sub-symphony, weaving another archetype into the reality being forged. This is the key to composing complex realities from simpler, reusable patterns.",
                    "example": {
                        "scripture": "%% weave api-resource src/domains --set name=User",
                        "proclamation": "Summons the `weave` artisan to inject the `api-resource` pattern into the `src/domains` directory."
                    }
                }
            ]
        },
        "alchemist_grimoire": {
            "description": "The sacred Grimoire of the Divine Alchemist, revealing all known rites (filters and functions) for transmuting Gnosis within a `{{ ... }}` vessel.",
            "filters": filters,
            "functions": functions
        },
        "semantic_cortex": {
            "description": "The Pantheon of Semantic Directives, a collection of hyper-intelligent, generative artisans that can be summoned with a single `@` plea to forge complex, production-grade realities from a high-level intent.",
            "domains": sorted(list(semantic_domains.keys())),
            "directives": sorted(semantic_directives)
        }
    }