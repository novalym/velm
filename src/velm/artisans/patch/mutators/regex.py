import re
from .base import BaseMutator, Logger
from ....contracts.heresy_contracts import ArtisanHeresy


class RegexMutator(BaseMutator):
    """
    =================================================================================
    == THE REGEX SURGEON (V-Ω-PATTERN-MASTER)                                      ==
    =================================================================================
    Master of Subtraction and Transfiguration.
    """

    @staticmethod
    def subtract(original: str, pattern: str) -> str:
        """[FACULTY 3] Removes content matching a pattern."""
        try:
            flags = re.MULTILINE | re.DOTALL
            if pattern.startswith("literal:"):
                target = pattern[8:]
                if target not in original:
                    Logger.warn(f"Subtraction target '{target[:20]}...' not found.")
                    return original
                return original.replace(target, "")

            regex = re.compile(pattern, flags)
            if not regex.search(original):
                Logger.warn(f"Subtraction pattern '{pattern}' not found in scripture.")
                return original

            return regex.sub("", original)
        except re.error as e:
            raise ArtisanHeresy(f"Invalid Regex for subtraction: {pattern} ({e})")

    @staticmethod
    def transfigure(original: str, command: str, replacement_block: str = None) -> str:
        """[FACULTY 3] Replaces content based on regex or literal match."""
        # Strategy A: Literal Block Swap
        if command.startswith("literal:"):
            find_str = command[8:]
            if find_str not in original:
                Logger.warn(f"Literal target '{find_str[:20]}...' not found.")
                return original
            payload = replacement_block if replacement_block is not None else ""
            return original.replace(find_str, payload)

        # Strategy B: Legacy Inline s/find/replace/
        if not replacement_block and command.startswith("s/"):
            try:
                match = re.match(r"s/(.*)/(.*)/([gims]*)", command)
                if not match:
                    raise ArtisanHeresy(f"Malformed inline transfiguration: {command}")
                find, replace, flags_str = match.groups()
                flags = 0
                if 'i' in flags_str: flags |= re.IGNORECASE
                if 'm' in flags_str: flags |= re.MULTILINE
                if 's' in flags_str: flags |= re.DOTALL
                count = 0 if 'g' in flags_str else 1
                return re.sub(find, replace, original, count=count, flags=flags)
            except re.error as e:
                raise ArtisanHeresy(f"Invalid Regex: {e}")

        # Strategy C: Split-Brain Surgery (Regex Locator + Content Payload)
        elif replacement_block is not None:
            find_pattern = command.strip()
            flags = re.MULTILINE | re.DOTALL
            try:
                regex = re.compile(find_pattern, flags)
                if not regex.search(original):
                    Logger.warn(f"Transfiguration pattern '{find_pattern}' not found.")
                    return original
                return regex.sub(replacement_block, original, count=1)
            except re.error as e:
                raise ArtisanHeresy(f"Invalid Regex Pattern: {find_pattern} ({e})")

        return original
