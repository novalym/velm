from .base import BaseMutator, Logger


class TextualMutator(BaseMutator):
    """
    =================================================================================
    == THE TEXTUAL ALCHEMIST (V-Ω-SMART-IO)                                        ==
    =================================================================================
    Master of Append and Prepend operations.
    """

    @staticmethod
    def append(original: str, fragment: str) -> str:
        """
        [FACULTY 1] The Smart Append.
        Ensures exactly one newline separation.
        Checks fuzzy idempotency.
        """
        if not original:
            return fragment

        if fragment.strip() in original:
            Logger.verbose("Append skipped: Content soul already present.")
            return original

        clean_original = original.rstrip()
        clean_fragment = fragment.lstrip()

        return f"{clean_original}\n\n{clean_fragment}\n"

    @staticmethod
    def prepend(original: str, fragment: str) -> str:
        """
        [FACULTY 6] The Shebang-Aware Smart Prepend.
        Inserts content at the top, but respects `#!` and encoding declarations.
        """
        if not fragment:
            return original

        if fragment.strip() in original:
            Logger.verbose("Prepend skipped: Content soul already present.")
            return original

        lines = original.splitlines(keepends=True)
        insert_idx = 0

        # Gnostic Gaze: Scan for headers to skip
        for i, line in enumerate(lines[:5]):  # Check first 5 lines
            if line.startswith("#!") or "coding:" in line or "encoding=" in line or "xml version" in line:
                insert_idx = i + 1
            else:
                break

        head = "".join(lines[:insert_idx])
        tail = "".join(lines[insert_idx:])

        if head and not head.endswith("\n"): head += "\n"
        if tail and not fragment.endswith("\n"): fragment += "\n"

        return f"{head}{fragment}{tail}"