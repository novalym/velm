# scaffold/parser_core/parser_scribes/symphony_scribes/symphony_base_scribe.py

import shlex

from ..base_scribe import FormScribe
from .....contracts.symphony_contracts import Edict


class SymphonyBaseScribe(FormScribe):
    """
    The Ancestral Scribe for the Language of Will (.symphony).
    Holds shared Gnosis for parsing command metadata.
    """

    def _parse_action_metadata(self, raw_command: str, edict: Edict):
        """
        [THE SHARED GAZE]
        Parses a command string for 'as <var>' and 'using <adj>'.
        Populates the Edict in-place.
        """
        try:
            # Use shlex to respect quotes (e.g., >> cmd --msg "as value")
            tokens = shlex.split(raw_command)
        except ValueError:
            # Fallback for malformed quotes, though Inquisitor usually catches this
            tokens = raw_command.split()

        command_parts = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == 'as':
                if i + 1 < len(tokens):
                    edict.capture_as = tokens[i + 1]
                    i += 2;
                    continue
            elif token == 'using':
                if i + 1 < len(tokens):
                    edict.adjudicator_type = tokens[i + 1]
                    i += 2;
                    continue

            command_parts.append(token)
            i += 1

        # Reassemble the core command without the metadata tokens
        # We use shlex.join if available (Python 3.8+), else simple join
        try:
            edict.command = shlex.join(command_parts)
        except AttributeError:
            edict.command = " ".join(command_parts)