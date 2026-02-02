# Path: jurisprudence_core/heresy_codex/infra.py
# ----------------------------------------------

"""
=================================================================================
== THE CELESTIAL ARCHITECT (INFRASTRUCTURE & DEVOPS HERESIES)                  ==
=================================================================================
These laws govern the containerization, deployment pipelines, and operational
configuration of the project.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

INFRA_LAWS: Dict[str, GnosticLaw] = {

    # --- DOCKER HERESIES ---

    "DOCKER_LATEST_TAG_HERESY": GnosticLaw(
        key="DOCKER_LATEST_TAG_HERESY",
        validator=NULL_VALIDATOR,
        title="The Shifting Sand: 'latest' Tag Detected",
        message="A Docker vessel uses the unstable 'latest' tag.",
        elucidation="The 'latest' tag is a moving target. Relying on it prevents reproducible builds and can lead to silent, catastrophic updates in production.",
        severity="CRITICAL",
        suggestion="Use a specific version tag or a content hash (digest) for the base image."
    ),

    "ROOT_USER_CONTAINER_HERESY": GnosticLaw(
        key="ROOT_USER_CONTAINER_HERESY",
        validator=NULL_VALIDATOR,
        title="The Tyrant's Privilege",
        message="The Docker vessel is willed to run as the 'root' user.",
        elucidation="Operating as root inside a container provides an escape path for malicious spirits to compromise the host machine. Purity requires the lowest possible privilege.",
        severity="WARNING",
        suggestion="Add a `USER` directive to the Dockerfile to run as a non-privileged user."
    ),

    "DOCKER_ADD_HERESY": GnosticLaw(
        key="DOCKER_ADD_HERESY",
        validator=NULL_VALIDATOR,
        title="The Magic Portal: Docker ADD Detected",
        message="The `ADD` directive is used instead of `COPY`.",
        elucidation="The `ADD` rite is unpredictable; it can auto-extract archives and fetch remote URLs. `COPY` is the pure, transparent way to transmute local files into the vessel.",
        severity="INFO",
        suggestion="Replace `ADD` with `COPY` unless you explicitly require archive auto-extraction."
    ),

    "DOCKERFILE_COPY_ALL_HERESY": GnosticLaw(
        key="DOCKERFILE_COPY_ALL_HERESY",
        validator=NULL_VALIDATOR,
        title="The Bloated Vessel",
        message="The `Dockerfile` uses `COPY . .`.",
        elucidation="Copying the entire context invalidates the build cache for any file change. This makes the forge slow and the vessel impure.",
        severity="WARNING",
        suggestion="Copy `requirements.txt` or `package.json` first, install dependencies, and THEN copy the rest."
    ),

    "MISSING_DOCKERFILE_HERESY": GnosticLaw(
        key="MISSING_DOCKERFILE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Spirit Without a Body",
        message="A `docker-compose.yml` was perceived without a `Dockerfile`.",
        elucidation="The Composer needs a blueprint to forge the container's soul. Referencing external images is valid, but building locally usually requires a Dockerfile.",
        severity="WARNING",
        suggestion="Create a `Dockerfile` to define the container's build process."
    ),

    "MISSING_DOCKERIGNORE_HERESY": GnosticLaw(
        key="MISSING_DOCKERIGNORE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unfiltered Context",
        message="A `Dockerfile` was perceived without a `.dockerignore`.",
        elucidation="Without this ward, profane artifacts (git history, local envs, node_modules) bloat the build context, slowing the forge and leaking secrets.",
        severity="WARNING",
        suggestion="Create a `.dockerignore` to exclude local artifacts."
    ),

    # --- CI/CD HERESIES ---

    "MISSING_CI_PIPELINE_HERESY": GnosticLaw(
        key="MISSING_CI_PIPELINE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Unchronicled Symphony",
        message="A Git sanctum was perceived, but no CI/CD pipeline scripture was found.",
        elucidation="Every Great Work deserves an automated symphony of adjudication (GitHub Actions, GitLab CI) to ensure its purity persists across time.",
        severity="INFO",
        suggestion="Add a workflow file (e.g., `.github/workflows/ci.yml`)."
    ),

    # --- AUTOMATION HERESIES ---

    "MISSING_MAKEFILE_HERESY": GnosticLaw(
        key="MISSING_MAKEFILE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Missing Altar",
        message="A project of this complexity lacks a `Makefile` (or `Justfile`).",
        elucidation="Standardizing common development rites (install, test, run) reduces cognitive load for new Architects.",
        severity="INFO",
        suggestion="Create a `Makefile` to serve as the universal altar for development rites."
    ),

    "ENV_IN_GITIGNORE_HERESY": GnosticLaw(
        key="ENV_IN_GITIGNORE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Exposed Secret",
        message="The `.gitignore` does not ward against the `.env` file.",
        elucidation="This is a critical heresy. Committing secrets to the chronicle allows them to be seen by profane eyes.",
        severity="CRITICAL",
        suggestion="Add `.env` to your `.gitignore` immediately."
    ),

    "MISSING_ENV_EXAMPLE_HERESY": GnosticLaw(
        key="MISSING_ENV_EXAMPLE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Hidden Map",
        message="A `.env` file was perceived without a `.env.example`.",
        elucidation="The `.env.example` is the map of required configuration. Without it, other Architects cannot know what secrets to provide.",
        severity="WARNING",
        suggestion="Create a `.env.example` with placeholder values."
    ),
}