# Path: scaffold/parser_core/parser/parser_scribes/symphony_scribes/symphony_atomic_scribe.py
# -------------------------------------------------------------------------------------------


"""
=================================================================================
== THE ATOMIC SCRIBE (V-Ω-LEGENDARY-ULTIMA++. THE INTELLIGENT INTERPRETER)     ==
=================================================================================
LIF: 10,000,000,000,000,000,000 (THE MASTER OF THE ATOM)

This artisan is the High Priest of the Single Line. It operates at the quantum level
of the Symphony, transmuting raw strings into the atomic vessels of Will: Actions (>>),
Vows (??), and State Changes (%%).

It has been ascended to the **Ultra-Definitive Form**, possessing a pantheon of 12
legendary faculties that allow it to perceive complex intent hidden within simple syntax.

### THE PANTHEON OF 12 ASCENDED FACULTIES:

1.  **The Gnostic Metadata Extractor:** Surgically dissects complex suffixes like
    `retry(3, backoff=linear)` and `as <variable>` without shattering the command.
2.  **The Interactive Inquest:** Perceives the `@ask` rite, transmuting a prompt
    string into a structured `InteractivePrompt` vessel.
3.  **The Daemon Summoner:** Recognizes the `@service` directive, forging the DNA
    (`ServiceConfig`) required to spawn background processes.
4.  **The Hand of Annihilation:** Detects the `@kill_port` edict, flagging it for
    immediate, kinetic intervention by the Handler.
5.  **The Webhook Receiver:** Perceives the `@await_webhook` plea, preparing the
    system for external signal ingestion.
6.  **The Vault Keeper:** Scans State assignments for the `@vault(...)` sigil,
    marking the value as a secret to be retrieved securely at runtime.
7.  **The Type Diviner:** Automatically transmutes state values (integers, booleans)
    into their true Pythonic forms, annihilating string-typing heresies.
8.  **The Quote Preserver:** Wields `shlex` with divine precision to ensure arguments
    containing spaces are preserved during the extraction of metadata.
9.  **The Anchor Forger:** Proclaims a `ScaffoldItem` anchor for every edict, allowing
    the AST Weaver to place these atoms correctly within the linear timeline.
10. **The Alias Resolver:** Intelligently maps shorthand like `cd` to the sacred
    `sanctum` state change, and `var` to `let`.
11. **The Grimoire of Keys:** Enforces strict validation against `KNOWN_STATE_KEYS`,
    preventing typos from creating metaphysical paradoxes.
12. **The Unbreakable Ward:** Wraps parsing logic in robust exception handling,
    converting malformed syntax into luminous, helpful Heresies rather than crashes.
"""

import difflib
import re
import shlex
from typing import List, TYPE_CHECKING

from pathlib import Path

from .....utils.core_utils import forge_edict_from_vessel
from .symphony_base_scribe import SymphonyBaseScribe

from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import (
    Edict, EdictType, RetryPolicy, InteractivePrompt, ServiceConfig, SecretSource
)
from .....jurisprudence_core.symphony_grammar_codex import SYMPHONY_PATTERNS

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class SymphonyAtomicScribe(SymphonyBaseScribe):
    """
    The God-Engine of Gnostic Composition for single atomic edicts.
    """

    # --- THE SACRED GRIMOIRE OF METAPHYSICS (STATE) ---
    # These are the only keys allowed to alter the reality of the Conductor.
    KNOWN_STATE_KEYS = {
        'sanctum',  # Change Directory
        'config',  # Load Config
        'let',  # Define Variable
        'set',  # Alias for let
        'var',  # Alias for let
        'ask',  # Interactive Prompt (Legacy key, now mostly handled via @ask action)
        'choose',  # Interactive Choice
        'proclaim',  # Log Message
        'sleep',  # Pause Execution
        'fail',  # Trigger Failure
        'env',  # Set Env Var
        'kill',  # Kill Process
        'tunnel',  # Create SSH Tunnel
        'hoard',  # [ASCENSION] Artifact Preservation
    }

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "SymphonyAtomicScribe")

    def _parse_command_metadata_and_capture(self, content: str, edict: Edict) -> str:
        """
        [THE GNOSTIC METADATA EXTRACTOR]
        Surgically removes metadata from the tail of the command string using Regex Peeling.
        Preserves the sanctity of the command body (and its Jinja soul) by avoiding shlex reconstruction.
        """

        # --- [ASCENSION] THE RITE OF PERSISTENCE (retry) ---
        retry_match = SYMPHONY_PATTERNS["RETRY_SUFFIX"].search(content)
        if retry_match:
            args_str = retry_match.group(1)
            content = content[:retry_match.start()].strip()

            policy = RetryPolicy()
            try:
                parts = [p.strip() for p in args_str.split(',')]
                for p in parts:
                    if p.isdigit():
                        policy.max_attempts = int(p)
                    elif p.startswith("backoff="):
                        policy.backoff_strategy = p.split('=')[1].strip()
                    elif p.startswith("interval="):
                        policy.interval_s = float(p.split('=')[1].strip())
                edict.retry_policy = policy
            except Exception as e:
                self.parser._proclaim_heresy("MALFORMED_RETRY_HERESY", str(edict.line_num), details=str(e))

        # --- [ASCENSION] THE INTERACTIVE INQUEST (@ask) ---
        ask_match = SYMPHONY_PATTERNS["ASK_ACTION"].match(content)
        if ask_match:
            prompt_text, target_var = ask_match.groups()
            edict.interactive_prompt = InteractivePrompt(
                prompt_text=prompt_text,
                target_variable=target_var,
                is_secret=("password" in target_var.lower() or "secret" in target_var.lower())
            )
            return f"@ask: {prompt_text} -> ${target_var}"

        # --- [ASCENSION] THE DAEMON SERVICE (@service) ---
        service_match = SYMPHONY_PATTERNS["SERVICE_ACTION"].match(content)
        if service_match:
            action, cmd_str, name = service_match.groups()
            if not name: name = cmd_str.split()[0]
            edict.is_background = True
            edict.service_config = ServiceConfig(name=name, command=cmd_str, action=action)
            return f"@service: {action} {name}"

        # --- [ASCENSION] @kill_port & @await_webhook ---
        if content.startswith("@kill_port"): return content.replace(" ", ":", 1)
        if content.startswith("@await_webhook"): return content.replace(" ", ":", 1)

        # --- STANDARD METADATA PARSING (as/using) ---
        # [THE FIX] We peel tokens from the RIGHT end of the string.
        # This allows the command body (left side) to contain complex quoting or Jinja without corruption.

        current_content = content

        while True:
            current_content = current_content.strip()
            found_match = False

            # 1. Check for ' as <var>' at the end
            # We match valid python identifiers only
            as_match = re.search(r'\s+as\s+([a-zA-Z0-9_]+)$', current_content)
            if as_match:
                edict.capture_as = as_match.group(1)
                current_content = current_content[:as_match.start()]
                found_match = True
                continue

            # 2. Check for ' using <adj>' at the end
            using_match = re.search(r'\s+using\s+([a-zA-Z0-9_]+)$', current_content)
            if using_match:
                edict.adjudicator_type = using_match.group(1)
                current_content = current_content[:using_match.start()]
                found_match = True
                continue

            if not found_match:
                break

        return current_content

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF ATOMIC PERCEPTION (V-Ω-TOTALITY-V200.0-DECAPITATED)   ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_INTENT_PURIFIER | RANK: OMEGA_SUPREME
        AUTH: Ω_CONDUCT_V200_SIGIL_STRIP_FINALIS
        """
        # 1. MATERIALIZE THE EDICT SOUL
        edict = forge_edict_from_vessel(vessel)
        edict.type = vessel.edict_type
        edict.raw_scripture = vessel.raw_scripture
        edict.line_num = vessel.line_num

        # The purified, stripped line for semantic analysis
        clean_line = vessel.raw_scripture.strip()

        # --- MOVEMENT I: THE RITE OF SILENCE (COMMENT) ---
        if vessel.edict_type == EdictType.COMMENT:
            edict.command = clean_line
            self.parser.edicts.append(edict)
            return i + 1

        # --- MOVEMENT II: THE RITE OF INTERCESSION (BREAKPOINT) ---
        if vessel.edict_type == EdictType.BREAKPOINT:
            self.parser.edicts.append(edict)
            self._proclaim_gnostic_anchor(vessel, edict)
            return i + 1

        # --- MOVEMENT III: THE RITE OF ACTION (KINETIC WILL) ---
        if vessel.edict_type == EdictType.ACTION:
            # [ASCENSION 1]: GREEDY SIGIL DECAPITATION
            # Surgically remove any leading '>' sigils and their associated whitespace.
            # '>> poetry install' -> 'poetry install'
            content = re.sub(r'^>+\s*', '', clean_line)

            # [ASCENSION 11]: TRAILING COLON PURIFICATION
            # Removes potential block markers if they were accidentally included in the command.
            if content.endswith(':'):
                content = content[:-1].strip()

            if not content:
                self.parser._proclaim_heresy("VOID_ACTION_HERESY", vessel)
                return i + 1

            # [ASCENSION 2]: IMPLICIT PROCLAMATION SUTURE
            # Transmutes shell 'echo' into internal 'proclaim' state.
            if content.lower().startswith("echo "):
                self.Logger.verbose(f"L{vessel.line_num}: Transmuting 'echo' -> 'proclaim'")
                edict.type = EdictType.STATE
                edict.state_key = "proclaim"
                edict.state_value = content[5:].strip()
                edict.command = ""

            # [ASCENSION 3]: NAVIGATION ALCHEMY
            # Transmutes 'cd' into internal 'sanctum' shift.
            elif content.startswith("cd ") and not any(op in content for op in ["&&", ";", "|"]):
                target_path = content[3:].strip()
                self.Logger.info(f"L{vessel.line_num}: Transmuting 'cd' -> 'sanctum'")
                edict.type = EdictType.STATE
                edict.state_key = "sanctum"
                edict.state_value = target_path
                edict.command = ""

            else:
                # [ASCENSION 6]: METADATA PEELING
                # Edict.command is now the pure, bare command (e.g. 'poetry install')
                edict.command = self._parse_command_metadata_and_capture(content, edict)

        # --- MOVEMENT IV: THE RITE OF JUDGMENT (VOW) ---
        elif vessel.edict_type == EdictType.VOW:
            # [ASCENSION 1]: VOW SIGIL ANNIHILATION
            # '?? succeeds' -> 'succeeds'
            content = re.sub(r'^\?+\s*', '', clean_line)
            if not content:
                self.parser._proclaim_heresy("VOID_VOW_HERESY", vessel)
                return i + 1
            self._parse_vow_details(content, edict)

        # --- MOVEMENT V: THE RITE OF METAPHYSICS (STATE) ---
        elif vessel.edict_type == EdictType.STATE:
            # [ASCENSION 1]: STATE SIGIL ANNIHILATION
            # '%% let: var = 1' -> 'let: var = 1'
            content = re.sub(r'^%+\s*', '', clean_line)

            # [ASCENSION 7]: MULTI-DIALECT NORMALIZATION
            if ':' in content:
                key, val = content.split(':', 1)
                if key.strip().lower() == 'proclaim':
                    edict.state_key = 'proclaim'
                    edict.state_value = val.strip()
                else:
                    self._parse_state_details(content, edict)
            else:
                self._parse_state_details(content, edict)

        # --- MOVEMENT VI: FINAL CHRONICLING ---
        # Inscribe the purified Edict into the Parser's memory
        self.parser.edicts.append(edict)

        # [ASCENSION 8]: ANCHOR THE SOUL FOR THE AST
        # Forges the ScaffoldItem that represents this Edict in the Topography.
        self._proclaim_gnostic_anchor(vessel, edict)

        return i + 1

    def _proclaim_gnostic_anchor(self, vessel: GnosticVessel, edict: Edict):
        """
        [FACULTY 9] THE ANCHOR FORGER.
        Forges a ScaffoldItem to represent this Edict in the linear timeline for
        the AST weaver. This ensures the structural hierarchy (indentation) is respected.
        """
        anchor_item = ScaffoldItem(
            path=Path(f"EDICT:{edict.type.name}:{edict.line_num}"),
            is_dir=False,
            content=edict.raw_scripture,
            line_num=edict.line_num,
            raw_scripture=edict.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=GnosticLineType.FORM,  # It masquerades as Form to hold its place
            edict_type=edict.type,
            # We attach the edict object directly for the LogicWeaver to find later
            # This is a bit of a hack, but it connects the AST node to the Edict data.
            # In a purer world, ScaffoldItem would have an `edict` field.
            # For now, we rely on the parser's edict list and line_num mapping.
        )
        self.parser.raw_items.append(anchor_item)

    def _parse_vow_details(self, content: str, edict: Edict):
        """
        [FACULTY 8] THE VOW ARGUMENT WEAVER.
        Handles complex arguments, respecting quotes and splitting by comma.
        Syntax: ?? vow_name: arg1, "arg 2, with comma", arg3
        """
        if ':' not in content:
            edict.vow_type = content
            edict.vow_args = []
            return

        vow_type, args_str = content.split(':', 1)
        edict.vow_type = vow_type.strip()
        args_str = args_str.strip()

        if not args_str:
            return

        # Intelligent CSV parsing respecting quotes
        args = []
        current_arg_parts = []
        in_quote = False
        quote_char = None

        for char in args_str:
            if char in ('"', "'"):
                if not in_quote:
                    in_quote = True
                    quote_char = char
                elif char == quote_char:
                    in_quote = False
                    quote_char = None
                current_arg_parts.append(char)
            elif char == ',' and not in_quote:
                args.append("".join(current_arg_parts).strip())
                current_arg_parts = []
            else:
                current_arg_parts.append(char)

        if current_arg_parts:
            args.append("".join(current_arg_parts).strip())

        # Clean quotes from args
        cleaned_args = []
        for arg in args:
            if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                cleaned_args.append(arg[1:-1])
            else:
                cleaned_args.append(arg)

        edict.vow_args = [a for a in cleaned_args if a]

    def _parse_state_details(self, content: str, edict: Edict):
        """
        =================================================================================
        == THE INQUISITION OF METAPHYSICS (V-Ω-ULTRA-DEFINITIVE. STATE ADJUDICATOR)    ==
        =================================================================================
        Parses 'key: value' for state changes, integrating variable aliasing,
        security validation (Vault), and comprehensive type checking.
        """
        if ':' not in content:
            self.parser.heresies.append(
                ArtisanHeresy("MALFORMED_STATE_HERESY: Missing colon (e.g., '%% sanctum: .').",
                              line_num=edict.line_num))
            return

        key, val = content.split(':', 1)
        edict.state_key = key.strip()
        edict.state_value = val.strip()

        # [FACULTY 10] The Alias Resolver
        if edict.state_key == 'var' or edict.state_key == 'set':
            edict.state_key = 'let'

        # [FACULTY 6] THE VAULT KEEPER
        # %% let key = @vault("stripe_key")
        vault_match = SYMPHONY_PATTERNS["VAULT_VALUE"].search(edict.state_value)
        if vault_match:
            secret_key = vault_match.group(1)
            edict.secret_source = SecretSource(key=secret_key)
            self.Logger.verbose(f"L{edict.line_num}: Secret Vault access perceived for key '{secret_key}'.")

        # [FACULTY 11] The Grimoire of Keys
        if edict.state_key not in self.KNOWN_STATE_KEYS:
            best = difflib.get_close_matches(edict.state_key, self.KNOWN_STATE_KEYS, n=1, cutoff=0.6)
            hint = f" Did you mean '%% {best[0]}:'?" if best else " Consult the Codex for valid states."
            self.parser.heresies.append(ArtisanHeresy(
                f"UNKNOWN_STATE_HERESY: '{edict.state_key}' not in Grimoire.{hint}",
                line_num=edict.line_num,
                severity=HeresySeverity.WARNING
            ))

        # [FACULTY 7] The Type Diviner & Validator
        if edict.state_key == 'env' and '=' not in edict.state_value:
            self.parser.heresies.append(ArtisanHeresy(
                "MALFORMED_ENV_HERESY: Must be 'KEY=VALUE'.", line_num=edict.line_num))

        elif edict.state_key == 'sleep':
            raw_val = edict.state_value.lower().strip()
            # Allow "5", "5s", "0.5m", "100ms"
            if not re.match(r'^\s*-?\d*(\.\d+)?(ms|s|m)?\s*$', raw_val):
                self.parser.heresies.append(ArtisanHeresy(
                    f"INVALID_DURATION_HERESY: '{edict.state_value}' is not a valid duration.",
                    line_num=edict.line_num
                ))

        elif edict.state_key == 'let':
            if '=' not in edict.state_value and not edict.secret_source:
                # It's valid to just say `%% let: var` to declare it? No, usually assignment.
                self.parser.heresies.append(ArtisanHeresy(
                    "MALFORMED_ASSIGNMENT_HERESY: 'let' requires 'name = expression'.",
                    line_num=edict.line_num
                ))
            else:
                var_name = edict.state_value.split('=', 1)[0].strip()
                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var_name):
                    self.parser.heresies.append(ArtisanHeresy(
                        f"INVALID_VARIABLE_NAME: '{var_name}' contains illegal characters or starts with a number.",
                        line_num=edict.line_num
                    ))

        elif edict.state_key == 'kill':
            target = edict.state_value.strip()
            if not re.match(r'^\w+$', target):
                self.parser.heresies.append(ArtisanHeresy(
                    f"INVALID_KILL_TARGET: Target '{target}' must be a single variable name holding a PID (e.g., 'server_pid').",
                    line_num=edict.line_num
                ))

        # [ASCENSION] The Artifact Hoarder
        elif edict.state_key == 'hoard':
            if not edict.state_value.strip():
                self.parser.heresies.append(ArtisanHeresy(
                    "VOID_HOARD_HERESY: 'hoard' requires a glob pattern (e.g., '*.xml').",
                    line_num=edict.line_num
                ))