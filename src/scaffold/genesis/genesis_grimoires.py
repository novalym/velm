# Path: scaffold/genesis_grimoires.py

"""
=================================================================================
== THE SACRED GRIMOIRE OF GENESIS PROPHECY (V-Ω-ULTRA-DEFINITIVE. THE LAW)      ==
=================================================================================
This is the living, eternal soul of the Genesis Prophet. It is the sacred,
declarative, and infinitely extensible Grimoire that contains all Gnostic laws
for prophesying the architectural form of a new reality based on the Architect's
will.

The Gnosis is prioritized: Directories first, then Core Artifacts, then specific
integration scripts.
=================================================================================
"""

# =================================================================================
# == I. THE SACRED CONTRACT OF A GNOSTIC PROPHECY                                ==
# =================================================================================
#   "key": A unique identifier for the prophecy.
#   "path": The scripture of the path to be forged, with `{{slug}}` as a vessel.
#   "is_dir": (Optional) Explicitly proclaims the scripture as a Sanctum.
#   "adjudicator": A divine lambda that receives the `gnosis` dict and returns
#                  True if this prophecy should be made manifest.
#   "content_rite": (Optional) An alchemical lambda that forges the soul of the
#                   scripture from the Architect's will.
#   "review": A vessel of Gnosis for the Rite of Final Review.
# =================================================================================

GENESIS_GRIMOIRE = [
    # -------------------------------------------------------------------------
    # --- I. FOUNDATIONAL SANCTUMS ---
    # -------------------------------------------------------------------------
    {"key": "root_dir", "path": "{{project_slug}}/", "is_dir": True, "adjudicator": lambda g: True},
    {"key": "src_dir", "path": "{{project_slug}}/src/", "is_dir": True, "adjudicator": lambda g: True,
     "review": {"description": "The sacred sanctum for all core source code."}},
    {"key": "tests_dir", "path": "{{project_slug}}/tests/", "is_dir": True, "adjudicator": lambda g: True,
     "review": {"description": "The sanctum for all scriptures of adjudication."}},

    # Tooling Sanctums
    {"key": "vscode_dir", "path": "{{project_slug}}/.vscode/", "is_dir": True, "adjudicator": lambda g: g.get('use_vscode')},
    {"key": "github_dir", "path": "{{project_slug}}/.github/workflows/", "is_dir": True,
     "adjudicator": lambda g: g.get('use_ci') == 'github'},

    # Feature Sanctums (Conditional)
    {"key": "db_dir", "path": "{{project_slug}}/src/database/", "is_dir": True,
     "adjudicator": lambda g: g.get('database_type') != 'none',
     "review": {"description": "Sanctum for data access logic."}},
    {"key": "db_migrations_dir", "path": "{{project_slug}}/src/database/migrations/", "is_dir": True,
     "adjudicator": lambda g: g.get('database_type') in ['postgres', 'mysql', 'sqlite'],
     "review": {"description": "Sanctum for database schema migration history."}},
    {"key": "auth_dir", "path": "{{project_slug}}/src/auth/", "is_dir": True,
     "adjudicator": lambda g: g.get('auth_method') != 'none',
     "review": {"description": "Sanctum for authentication and authorization logic."}},
    {"key": "frontend_dir", "path": "{{project_slug}}/frontend/", "is_dir": True,
     "adjudicator": lambda g: g.get('frontend_framework') not in ['none', 'vanilla-js'],
     "review": {"description": "Dedicated sanctum for frontend source code."}},

    # --- II. CORE ARTIFACTS (Universal Gnosis) ---
    {"key": "readme", "path": "{{project_slug}}/README.md", "adjudicator": lambda g: True,
     "review": {"description": "The luminous gateway scripture for the project."}},
    {"key": "editorconfig", "path": "{{project_slug}}/.editorconfig", "adjudicator": lambda g: True,
     "review": {"description": "Ensures a universal Gnostic style.", "severity": "guidance"}},
    {"key": "license", "path": "{{project_slug}}/LICENSE", "adjudicator": lambda g: g.get('license'),
     "review": {"description": "The project's sacred vow to the cosmos."}},
    {"key": "gitignore", "path": "{{project_slug}}/.gitignore", "adjudicator": lambda g: g.get('use_git'),
     "review": {"description": "The Sentinel's ward against profane artifacts."}},
    {"key": "contributing", "path": "{{project_slug}}/CONTRIBUTING.md", "adjudicator": lambda g: g.get('use_git'),
     "review": {"description": "The scroll of guidance.", "severity": "guidance"}},

    # --- III. PYTHON-SPECIFIC PROPHECIES ---
    {"key": "pyproject", "path": "{{project_slug}}/pyproject.toml",
     "adjudicator": lambda g: g.get('project_type') in ['python', 'poetry'],
     "review": {"description": "The soul of the Python project."}},
    {"key": "py_init", "path": "{{project_slug}}/src/__init__.py",
     "adjudicator": lambda g: g.get('project_type') in ['python', 'poetry']},
    {"key": "py_main", "path": "{{project_slug}}/src/main.py",
     "adjudicator": lambda g: g.get('project_type') in ['python', 'poetry']},
    {"key": "pytest_ini", "path": "{{project_slug}}/pytest.ini",
     "adjudicator": lambda g: g.get('testing_framework') == 'pytest' and g.get('project_type') in ['python', 'poetry']},

    # --- IV. NODE.JS/FRONTEND PROPHECIES ---
    {"key": "package_json", "path": "{{project_slug}}/package.json",
     "adjudicator": lambda g: g.get('project_type') == 'node' or g.get('frontend_framework') != 'none',
     "review": {"description": "The core manifest of the Node/Frontend reality."}},
    {"key": "js_main", "path": "{{project_slug}}/src/index.js", "adjudicator": lambda g: g.get('project_type') == 'node'},
    {"key": "jest_config", "path": "{{project_slug}}/jest.config.js",
     "adjudicator": lambda g: g.get('testing_framework') == 'jest' and g.get('project_type') == 'node'},
    {"key": "prettierrc", "path": "{{project_slug}}/.prettierrc",
     "adjudicator": lambda g: g.get('project_type') == 'node' or g.get('frontend_framework') != 'none'},
    {"key": "eslintrc", "path": "{{project_slug}}/.eslintrc.json",
     "adjudicator": lambda g: g.get('project_type') == 'node' or g.get('frontend_framework') != 'none'},
    {"key": "vite_config", "path": "{{project_slug}}/vite.config.ts",
     "adjudicator": lambda g: g.get('frontend_framework') == 'react',
     "review": {"description": "Frontend bundler configuration."}},

    # --- V. TOOLING & INTEGRATION PROPHECIES ---
    {"key": "vscode_settings", "path": "{{project_slug}}/.vscode/settings.json",
     "adjudicator": lambda g: g.get('use_vscode')},
    {"key": "dockerfile", "path": "{{project_slug}}/Dockerfile",
     "adjudicator": lambda g: g.get('use_docker')},
    {"key": "dockerignore", "path": "{{project_slug}}/.dockerignore",
     "adjudicator": lambda g: g.get('use_docker')},
    {"key": "ci_workflow", "path": "{{project_slug}}/.github/workflows/main.yml",
     "adjudicator": lambda g: g.get('use_ci') == 'github'},

    # --- VI. DATA SCIENCE PROPHECIES ---
    {"key": "ds_data_raw", "path": "{{project_slug}}/data/raw/", "is_dir": True,
     "adjudicator": lambda g: g.get('project_type') == 'python-datasci'},
    {"key": "ds_data_processed", "path": "{{project_slug}}/data/processed/", "is_dir": True,
     "adjudicator": lambda g: g.get('project_type') == 'python-datasci'},
    {"key": "ds_notebooks", "path": "{{project_slug}}/notebooks/", "is_dir": True,
     "adjudicator": lambda g: g.get('project_type') == 'python-datasci'},
    {"key": "ds_preprocessing", "path": "{{project_slug}}/src/preprocessing.py",
     "adjudicator": lambda g: g.get('project_type') == 'python-datasci'},
    {"key": "ds_model", "path": "{{project_slug}}/src/train_model.py",
     "adjudicator": lambda g: g.get('project_type') == 'python-datasci'},

    # --- VII. ALCHEMICAL CONTENT RITES ---
    {
        "key": "env_example",
        "path": "{{project_slug}}/.env.example",
        "adjudicator": lambda g: g.get('env_vars_setup'),
        "content_rite": lambda g, p_slug: "\n".join(filter(None, [
            "# Essential Environment Variables",
            f"DATABASE_URL=postgres://user:password@host:port/{p_slug}_db" if g.get('database_type') != 'none' else None,
            "JWT_SECRET=supersecretjwtkey" if g.get('auth_method') == 'jwt' else None,
            "AI_API_KEY=your_ai_api_key" if g.get('ai_code_generation_consent') else None,
            f"PORT={g.get('default_port', 8000)}" if g.get('default_port') else None
        ])),
        "review": {"description": "A scripture of required environment variables."}
    },

    # --- VIII. FULL STACK & OBSERVABILITY ---
    {"key": "react_app", "path": "{{project_slug}}/frontend/src/App.tsx",
     "adjudicator": lambda g: g.get('frontend_framework') == 'react'},
    {"key": "auth_files", "path": "{{project_slug}}/src/auth/auth_middleware.py",
     "adjudicator": lambda g: g.get('auth_method') != 'none',
     "review": {"description": "Files for the authentication middleware."}},
    {"key": "docker_compose_obs", "path": "{{project_slug}}/docker-compose.obs.yml",
     "adjudicator": lambda g: g.get('observability_setup') and g.get('use_docker')},
]