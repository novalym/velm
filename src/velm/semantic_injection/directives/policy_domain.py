# scaffold/semantic_injection/directives/policy_domain.py

"""
=================================================================================
== THE GUARDIAN OF GOVERNANCE (V-Ω-POLICY-DOMAIN)                              ==
=================================================================================
LIF: 25,000,000,000

This artisan implements the `@policy` namespace. It generates standard
governance documents to ensure project health, security, and contribution
standards.

Usage:
    SECURITY.md :: @policy/security(email="sec@example.com")
    CODE_OF_CONDUCT.md :: @policy/coc(email="conduct@example.com")
    docs/adr/0001-init.md :: @policy/adr(title="Use Python", status="Accepted")
=================================================================================
"""
from datetime import datetime
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("policy")
class PolicyDomain(BaseDirectiveDomain):
    """
    The Scribe of Law and Order.
    """

    @property
    def namespace(self) -> str:
        return "policy"

    def help(self) -> str:
        return "Generates governance docs (security, code of conduct, ADRs)."

    def _directive_security(self, context: Dict[str, Any], email: str = "security@example.com", *args, **kwargs) -> str:
        """
        @policy/security
        Generates a standard SECURITY.md (RFC 9116 inspired).
        """
        return dedent(f"""
            # Security Policy

            ## Supported Versions

            | Version | Supported          |
            | ------- | ------------------ |
            | 1.0.x   | :white_check_mark: |
            | < 1.0   | :x:                |

            ## Reporting a Vulnerability

            We take the security of our software seriously. If you believe you have found a security vulnerability, please report it to us as described below.

            **Please do not report security vulnerabilities through public GitHub issues.**

            Instead, please send an email to {email}.

            You should receive a response within 24 hours. If for some reason you do not, please follow up via email to ensure we received your original message.
        """).strip()

    def _directive_coc(self, context: Dict[str, Any], email: str = "community@example.com", *args, **kwargs) -> str:
        """
        @policy/coc
        Generates the Contributor Covenant Code of Conduct.
        """
        return dedent(f"""
            # Contributor Covenant Code of Conduct

            ## Our Pledge

            We as members, contributors, and leaders pledge to make participation in our
            community a harassment-free experience for everyone, regardless of age, body
            size, visible or invisible disability, ethnicity, sex characteristics, gender
            identity and expression, level of experience, education, socio-economic status,
            nationality, personal appearance, race, religion, or sexual identity
            and orientation.

            ... [Truncated for brevity, in a real file this would be the full text] ...

            ## Enforcement

            Instances of abusive, harassing, or otherwise unacceptable behavior may be
            reported to the community leaders responsible for enforcement at
            {email}.
        """).strip()

    def _directive_adr(self, context: Dict[str, Any], title: str = "Record Architecture Decision",
                       status: str = "Proposed", *args, **kwargs) -> str:
        """
        @policy/adr(title="Use Postgres", status="Accepted")
        Generates an Architecture Decision Record (ADR) template.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")

        return dedent(f"""
            # {title}

            * Status: {status}
            * Date: {date_str}

            ## Context and Problem Statement

            [Describe the context and problem statement, e.g., in free form using two or three sentences. You may want to articulate the problem in form of a question.]

            ## Decision Drivers

            * [driver 1, e.g., a force, facing concern, ...]
            * [driver 2, e.g., a force, facing concern, ...]

            ## Considered Options

            * [option 1]
            * [option 2]
            * [option 3]

            ## Decision Outcome

            Chosen option: "[option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | ... | comes out best (see below)].

            ## Pros and Cons of the Options

            ### [option 1]

            * Good, because [argument a]
            * Good, because [argument b]
            * Bad, because [argument c]
        """).strip()