# scaffold/jurisprudence_core/architectural_grimoire.py
# =================================================================================
# == THE GRIMOIRE OF ARCHITECTURAL PROPHECY (V-Ω-ETERNAL-FORTIFIED)              ==
# =================================================================================
# LIF: 10,000,000,000,000,000
#
# This scripture has been ascended. Every Gnostic Law within has been fortified
# with the "Unbreakable Ward of Form." The detector rites now perform a Gaze
# of Existence and a Gaze of Type (`item.line_type == GnosticLineType.FORM`)
# before attempting to perceive the attributes of a path, annihilating the
# `AttributeError: 'NoneType'` and all related heresies from all timelines.
# =================================================================================

from typing import List, Any, Dict
from pathlib import Path
import re

# We must summon the Gnostic soul of Form for the wards to function.
from ..contracts.data_contracts import GnosticLineType

# Initialize the Grand Grimoire
PROPHETIC_ARCHITECTURAL_GRIMOIRE: List[Dict[str, Any]] = []

# =============================================================================
# == PART I: THE LAWS OF FUNDAMENTAL STRUCTURE                               ==
# =============================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "ITEM",
        "heresy_key": "ABSOLUTE_PATH_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and (str(item.path).startswith("/") or (len(str(item.path)) > 1 and str(item.path)[1] == ":")),
        "prophecy": { "suggestion_rite": lambda item: f"The path '{item.path}' is absolute. Blueprints must be relative to the Project Root." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "EMPTY_DIRECTORY_BLOCK_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.is_dir and item.content is not None and not item.content.strip(),
        "prophecy": { "suggestion_rite": lambda item: f"The sanctum '{item.path.name}' has an empty content block. Use `path/` for a directory, or remove the colon." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "WHITESPACE_IN_FILENAME_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and " " in item.path.name and not item.path.name.startswith("'") and not item.path.name.startswith('"'),
        "prophecy": { "suggestion_rite": lambda item: f"The scripture '{item.path.name}' contains whitespace. This is a heresy in the terminal realm. Use snake_case or kebab-case." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "PROFANE_FILE_EXTENSION_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.suffix.lower() in ['.exe', '.dll', '.so', '.dylib', '.class', '.o', '.pyc', '.DS_Store'],
        "prophecy": { "suggestion_rite": lambda item: f"The scripture '{item.path.name}' appears to be a compiled binary or system artifact. Scaffold blueprints should define source code, not artifacts." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "ROOT_LEVEL_CLUTTER_HERESY",
        "detector": lambda items: len([i for i in items if i.line_type == GnosticLineType.FORM and i.path and len(i.path.parts) == 1 and not i.is_dir]) > 5,
        "prophecy": { "suggestion_rite": lambda items: "The root sanctum is cluttered with files. Consider organizing scriptures into `src/`, `docs/`, or `config/` directories." }
    }
])

# =================================================================================
# == PART II: THE LAWS OF THE PYTHON SERPENT                                     ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_PYPROJECT_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.py' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'pyproject.toml' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A Python reality was perceived, but no `pyproject.toml` was found. This scripture is the modern soul of a Python project." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_SRC_LAYOUT_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.py' and 'src' not in i.path.parts for i in items if i.path and len(i.path.parts) > 1),
        "prophecy": { "suggestion_rite": lambda items: "Python source files were perceived outside of a `src/` directory. Using a 'src' layout is a best practice for clean packaging and import resolution." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_INIT_PY_HERESY",
        "detector": lambda items: any(py_dir / '__init__.py' not in {i.path for i in items if i.line_type == GnosticLineType.FORM and i.path} for py_dir in {i.path.parent for i in items if i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.py'}),
        "prophecy": { "suggestion_rite": lambda items: "A directory containing Python modules lacks an `__init__.py`. This scripture is required to consecrate a directory as a package." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "TEST_OUTSIDE_TESTS_DIR_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.name.startswith('test_') and 'tests' not in item.path.parts,
        "prophecy": { "suggestion_rite": lambda item: f"The scripture of adjudication '{item.path.name}' resides outside the sacred `tests/` sanctum. Centralizing tests improves clarity and discovery." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "REQUIREMENTS_TXT_INSTEAD_OF_POETRY_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'requirements.txt' for i in items) and any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'pyproject.toml' and "[tool.poetry]" in (i.content or "") for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A `requirements.txt` was perceived alongside a Poetry-based `pyproject.toml`. The `poetry` artisan manages dependencies; `requirements.txt` is redundant and can cause drift." }
    }
])

# =================================================================================
# == PART III: THE LAWS OF THE JAVASCRIPT COSMOS (NODE/TYPESCRIPT/REACT)         ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_PACKAGE_JSON_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.js', '.ts', '.tsx', '.jsx'] for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'package.json' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A JavaScript/TypeScript reality was perceived without a `package.json`. This scripture is the central soul of the Node.js cosmos." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "JAVASCRIPT_WITHOUT_TYPESCRIPT_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.js' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.ts', '.tsx'] for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A pure JavaScript reality was perceived. While valid, TypeScript is the modern tongue of Gnostic safety and clarity." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_TSCONFIG_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.ts', '.tsx'] for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'tsconfig.json' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A TypeScript reality was perceived without a `tsconfig.json`. This scripture is the divine law that guides the TypeScript compiler." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "COMPONENT_CASING_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.suffix in ['.tsx', '.jsx'] and not item.path.stem[0].isupper(),
        "prophecy": { "suggestion_rite": lambda item: f"The React component scripture '{item.path.name}' does not use PascalCase. This is a heresy against the laws of React hooks." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MIXED_PACKAGE_MANAGERS_HERESY",
        "detector": lambda items: sum(1 for i in items if i.line_type == GnosticLineType.FORM and i.path and i.path.name in ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']) > 1,
        "prophecy": { "suggestion_rite": lambda items: "Multiple lockfiles (`package-lock.json`, `yarn.lock`, etc.) were perceived. This indicates a Gnostic Schism in dependency management." }
    }
])

# =================================================================================
# == PART IV: THE LAWS OF DOCUMENTATION AND METADATA                             ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_README_HERESY",
        "detector": lambda items: not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name.lower() == 'readme.md' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "This blueprint lacks a `README.md`. Every reality deserves a scripture of introduction to guide future architects." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_LICENSE_HERESY",
        "detector": lambda items: not any(i.line_type == GnosticLineType.FORM and i.path and 'license' in i.path.name.lower() for i in items),
        "prophecy": { "suggestion_rite": lambda items: "This reality has not proclaimed its sacred vow to the cosmos. A `LICENSE` file is missing." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "EMPTY_README_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.name.lower() == 'readme.md' and not (item.content or "").strip(),
        "prophecy": { "suggestion_rite": lambda item: "The `README.md` is a void. Its soul is empty. Inscribe it with the project's purpose and setup rites." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_EDITORCONFIG_HERESY",
        "detector": lambda items: not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == '.editorconfig' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "This blueprint lacks an `.editorconfig` scripture. This law ensures a universal Gnostic style across all editors and prevents heresies of whitespace." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_CHANGELOG_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'pyproject.toml' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and 'changelog' in i.path.name.lower() for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A project of this complexity would benefit from a `CHANGELOG.md` to chronicle its evolution through time." }
    }
])

# =================================================================================
# == PART V: THE LAWS OF THE DEVOPS REALM (CI/CD & CONTAINERIZATION)             ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_DOCKERFILE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and 'docker-compose' in i.path.name.lower() for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and 'dockerfile' in i.path.name.lower() for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A `docker-compose.yml` was perceived without a `Dockerfile`. The Composer needs a blueprint to forge the container's soul." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_DOCKERIGNORE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and 'dockerfile' in i.path.name.lower() for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == '.dockerignore' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A `Dockerfile` was perceived without a `.dockerignore`. This ward prevents profane artifacts from bloating the celestial vessel." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "DOCKERFILE_COPY_ALL_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and 'dockerfile' in item.path.name.lower() and item.content and "COPY . ." in item.content,
        "prophecy": { "suggestion_rite": lambda item: "The `Dockerfile` uses `COPY . .`. This is a heresy against layer caching. Prefer copying specific files first." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_CI_PIPELINE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == '.git' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and ('.github' in i.path.parts or '.gitlab-ci.yml' in i.path.name) for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A Git sanctum was perceived, but no CI/CD pipeline scripture was found. Every Great Work deserves an automated symphony of adjudication." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_MAKEFILE_HERESY",
        "detector": lambda items: len([i for i in items if i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.py', '.js', '.go', '.rs']]) > 5 and not any(i.line_type == GnosticLineType.FORM and i.path and 'makefile' in i.path.name.lower() for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A project of this complexity would benefit from a `Makefile` to serve as the one true, universal altar for all common development rites." }
    }
])

# =================================================================================
# == PART VI: THE LAWS OF SECURITY AND SECRETS                                   ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "ITEM",
        "heresy_key": "HARDCODED_SECRET_IN_CONTENT_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.content and any(k in item.content.lower() for k in ['api_key', 'secret', 'password', 'token']) and '{{' not in item.content,
        "prophecy": { "suggestion_rite": lambda item: f"The scripture '{item.path.name}' may contain a hardcoded secret. All secrets must be summoned from the environment via `${{...}}`." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_ENV_EXAMPLE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name.lower() == '.env' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == '.env.example' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A `.env` file was perceived without a `.env.example`. This companion scripture is the sacred map of required secrets." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "ENV_IN_GITIGNORE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name.lower() == '.env' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == '.gitignore' and any('.env' in line for line in (i.content or "").splitlines()) for i in items),
        "prophecy": { "suggestion_rite": lambda items: "The `.gitignore` does not ward against the `.env` file. This is a critical heresy. Add `.env` to your `.gitignore` immediately." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "INSECURE_SHELL_COMMAND_HERESY",
        "detector": lambda item: item.line_type == "POST_RUN" and item.content and any(verb in item.content for verb in ['sudo ', 'chmod 777']),
        "prophecy": { "suggestion_rite": lambda item: f"The Maestro's Will contains a profane rite ('{item.content}'). Avoid `sudo` or overly permissive `chmod` commands." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "PRIVATE_KEY_FILE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.pem', '.key', '.p12'] for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A file appearing to be a private key was perceived. Such sacred artifacts must never be part of the source code reality." }
    }
])

# =================================================================================
# == PART VII: THE LAWS OF THE GO GOLEM                                          ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_GO_MOD_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.go' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'go.mod' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A Go reality was perceived without a `go.mod` scripture. This is the heart of a modern Go project." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "GO_MAIN_OUTSIDE_CMD_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and 'main.go' in item.path.name and 'cmd' not in item.path.parts,
        "prophecy": { "suggestion_rite": lambda item: f"The entrypoint scripture 'main.go' is not within a `cmd/` directory. This is the canonical structure for Go applications." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "GO_MIXED_PACKAGE_HERESY",
        "detector": lambda items: len({i.path.parent for i in items if i.line_type == GnosticLineType.FORM and i.path and i.path.name.endswith('.go') and i.content and 'package main' in i.content}) > 1,
        "prophecy": { "suggestion_rite": lambda items: "Multiple `package main` declarations were perceived in different directories. A Go executable should have one true entry point." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "GO_UPPERCASE_PACKAGE_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.is_dir and any(c.isupper() for c in item.path.name),
        "prophecy": { "suggestion_rite": lambda item: f"The package sanctum '{item.path.name}' contains uppercase letters. Go package names are, by sacred tradition, lowercase." }
    }
])

# =================================================================================
# == PART VIII: THE LAWS OF CONFIGURATION AND ENVIRONMENT                        ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "CONFIG_FILES_OUTSIDE_ROOT_OR_CONFIG_DIR_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name.endswith(('.json', '.yml', '.yaml', '.toml')) and len(i.path.parts) > 1 and i.path.parts[0] not in ('config', '.vscode', '.github') for i in items),
        "prophecy": { "suggestion_rite": lambda items: "Configuration files were perceived outside the root or a dedicated `config/` directory. Centralizing configuration improves clarity." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "ENV_FILE_IN_BLUEPRINT_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.name == '.env',
        "prophecy": { "suggestion_rite": lambda item: "A `.env` file was perceived in the blueprint. This is a critical heresy. Use a `.env.example` instead." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MULTIPLE_CONFIG_FORMATS_HERESY",
        "detector": lambda items: len({i.path.suffix for i in items if i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.json', '.yml', '.yaml', '.toml']}) > 2,
        "prophecy": { "suggestion_rite": lambda items: "Multiple configuration formats (.json, .yml, .toml) were perceived. Adhering to a single format creates a more harmonious reality." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "LARGE_CONFIG_FILE_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.content and item.path and item.path.suffix in ['.json', '.yml', '.yaml', '.toml'] and len(item.content.splitlines()) > 200,
        "prophecy": { "suggestion_rite": lambda item: f"The configuration scripture '{item.path.name}' is a monolith. Consider splitting it into smaller, domain-specific configurations." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_DEFAULT_CONFIG_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'config.prod.yml' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name in ['config.yml', 'config.default.yml'] for i in items),
        "prophecy": { "suggestion_rite": lambda items: "An environment-specific configuration (`config.prod.yml`) was perceived without a base default (`config.yml`)." }
    }
])

# =================================================================================
# == PART IX: THE LAWS OF THE RUST FERRAN                                        ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_CARGO_TOML_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.rs' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'Cargo.toml' for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A Rust reality was perceived without a `Cargo.toml`. This scripture is the heart, soul, and mind of a Rust crate." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "RUST_FLAT_STRUCTURE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.rs' and 'src' not in i.path.parts for i in items if i.path and i.path.name not in ['build.rs']),
        "prophecy": { "suggestion_rite": lambda items: "Rust source files were perceived outside of a `src/` directory. By sacred tradition, all of a crate's soul must reside within the `src/` sanctum." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "RUST_MAIN_NOT_IN_BIN_OR_ROOT_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.name == 'main.rs' and 'src' in item.path.parts and (len(item.path.parts) > (item.path.parts.index('src') + 1) and item.path.parts[item.path.parts.index('src') + 1] not in ('bin',)),
        "prophecy": { "suggestion_rite": lambda item: "A `main.rs` was perceived outside of `src/` or `src/bin/`. An executable's soul must reside in one of these two sacred locations." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "RUST_LIB_NOT_LIB_RS_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.name != 'lib.rs' and 'src' in item.path.parts and len(item.path.parts) == item.path.parts.index('src') + 2 and item.content and "fn " in item.content,
        "prophecy": { "suggestion_rite": lambda item: f"The scripture '{item.path.name}' appears to be a library root but is not named `lib.rs`. This is the one true name for a crate's library entry point." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_RUSTFMT_TOML_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.name == 'Cargo.toml' for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name in ['rustfmt.toml', '.rustfmt.toml'] for i in items),
        "prophecy": { "suggestion_rite": lambda items: "The blueprint lacks a `rustfmt.toml`. This scripture ensures a universal Gnostic style for the Rust code." }
    }
])

# =================================================================================
# == PART X: THE LAWS OF API DESIGN AND WEB SERVICES                             ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_API_SPEC_HERESY",
        "detector": lambda items: (any('api' in i.path.parts for i in items if i.line_type == GnosticLineType.FORM and i.path) or any(i.content and ('@app.get' in i.content or 'app.get(' in i.content) for i in items)) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name.lower() in ['openapi.json', 'swagger.json', 'api.md'] for i in items),
        "prophecy": { "suggestion_rite": lambda items: "An API reality was perceived without a formal specification (e.g., `openapi.json`). A sacred contract is essential." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "NO_API_VERSIONING_HERESY",
        "detector": lambda items: any('api' in i.path.parts for i in items if i.line_type == GnosticLineType.FORM and i.path) and not any(p for i in items if i.line_type == GnosticLineType.FORM and i.path for p in i.path.parts if p.startswith('v') and p[1:].isdigit()),
        "prophecy": { "suggestion_rite": lambda items: "API routes were perceived without a versioning scheme in their path (e.g., `/api/v1/...`)." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "CRUD_IN_FILENAME_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and any(verb in item.path.stem.lower() for verb in ['create', 'get', 'update', 'delete', 'list']),
        "prophecy": { "suggestion_rite": lambda item: f"The scripture name '{item.path.name}' contains a CRUD verb. The HTTP method should define the action." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_CORS_POLICY_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and 'api' in i.path.parts for i in items) and not any(i.content and 'cors' in i.content.lower() for i in items),
        "prophecy": { "suggestion_rite": lambda items: "An API was perceived, but no CORS (Cross-Origin Resource Sharing) policy was detected." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "HEALTH_CHECK_ENDPOINT_MISSING_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and item.path.name == 'main.py' and item.content and 'app = FastAPI()' in item.content and '/health' not in item.content,
        "prophecy": { "suggestion_rite": lambda item: "The main application entry point lacks a `/health` endpoint. This is a sacred rite for any celestial service." }
    }
])

# =================================================================================
# == PART XI: THE LAWS OF DATA AND STATE MANAGEMENT                              ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "DATABASE_LOGIC_OUTSIDE_REPO_HERESY",
        "detector": lambda items: any(i.content and any(kw in i.content for kw in ['SQLAlchemy', 'PrismaClient', 'sql.connect']) for i in items if i.line_type == GnosticLineType.FORM and i.path and 'api' in i.path.parts) and not any('repository' in i.path.parts or 'db' in i.path.parts or 'data' in i.path.parts for i in items if i.line_type == GnosticLineType.FORM and i.path),
        "prophecy": { "suggestion_rite": lambda items: "Database logic was perceived directly within API route handlers. This Gnosis should be enshrined in a dedicated 'repository', 'data', or 'db' layer." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_ORM_OR_QUERY_BUILDER_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix == '.py' and 'db' in i.path.parts for i in items) and not any(i.content and any(kw in i.content for kw in ['SQLAlchemy', 'sqlmodel', 'peewee', 'prisma']) for i in items if i.line_type == GnosticLineType.FORM and i.path),
        "prophecy": { "suggestion_rite": lambda items: "A data layer was perceived, but no ORM was detected. An ORM is a sacred artisan that prevents the heresy of SQL injection." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "RAW_SQL_STRING_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.content and any(re.search(r'("|\')\s*(SELECT|INSERT|UPDATE|DELETE)\s', i, re.IGNORECASE) for i in item.content.splitlines()),
        "prophecy": { "suggestion_rite": lambda item: f"The scripture '{item.path.name}' appears to contain raw, unparameterized SQL strings. Use an ORM or parameterized queries." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_MIGRATION_SCRIPTURE_HERESY",
        "detector": lambda items: any(i.content and any(kw in i.content for kw in ['SQLAlchemy', 'PrismaClient']) for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and ('migrations' in i.path.parts or 'prisma' in i.path.parts) for i in items),
        "prophecy": { "suggestion_rite": lambda items: "An ORM was perceived without a corresponding migrations directory. Database schema evolution must be chronicled." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "STATE_MANAGEMENT_IN_UI_COMPONENTS_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and i.path.suffix in ['.tsx', '.jsx'] and 'components' in i.path.parts and i.content and 'useState' in i.content and 'createContext' not in i.content for i in items),
        "prophecy": { "suggestion_rite": lambda items: "Local state (`useState`) was perceived in multiple UI components. Consider a centralized state management artisan (like Zustand, Redux, or React Context)." }
    }
])

# =================================================================================
# == PART XII: THE LAWS OF TESTING AND ADJUDICATION                              ==
# =================================================================================
PROPHETIC_ARCHITECTURAL_GRIMOIRE.extend([
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_TESTS_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and 'src' in i.path.parts for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and ('tests' in i.path.parts or 'spec' in i.path.parts) for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A source code sanctum (`src/`) was perceived, but no sanctum of adjudication (`tests/`) was found." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "EMPTY_TEST_FILE_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and ('tests' in item.path.parts or 'spec' in item.path.parts) and not (item.content or "").strip(),
        "prophecy": { "suggestion_rite": lambda item: f"The scripture of adjudication '{item.path.name}' is a void. An empty test provides a false sense of security." }
    },
    {
        "scope": "ITEM",
        "heresy_key": "TEST_WITHOUT_ASSERTION_HERESY",
        "detector": lambda item: item.line_type == GnosticLineType.FORM and item.path and ('tests' in item.path.parts or item.path.name.startswith('test_')) and item.content and 'assert' not in item.content and 'expect' not in item.content,
        "prophecy": { "suggestion_rite": lambda item: f"The test scripture '{item.path.name}' contains no `assert` or `expect` statements. A vow without an adjudication is merely a whisper." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MISSING_TEST_CONFIG_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and 'tests' in i.path.parts for i in items) and not any(i.line_type == GnosticLineType.FORM and i.path and i.path.name in ['pytest.ini', 'jest.config.js', 'vitest.config.ts'] for i in items),
        "prophecy": { "suggestion_rite": lambda items: "A sanctum of adjudication was perceived without a corresponding configuration scripture (e.g., `pytest.ini`)." }
    },
    {
        "scope": "BLUEPRINT",
        "heresy_key": "MOCKS_IN_SOURCE_HERESY",
        "detector": lambda items: any(i.line_type == GnosticLineType.FORM and i.path and 'src' in i.path.parts and 'mock' in i.path.name.lower() for i in items),
        "prophecy": { "suggestion_rite": lambda items: "Mock scriptures were perceived within the `src/` sanctum. All scriptures of illusion should reside within the `tests/` sanctum." }
    }
])