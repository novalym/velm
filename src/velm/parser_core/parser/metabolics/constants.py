# Path: parser_core/parser/metabolics/constants.py
# ------------------------------------------------

"""
=================================================================================
== THE GRIMOIRE OF ANCESTORS: TOTALITY (V-Ω-TOTALITY-VMAX-PURITY-SUTURE)       ==
=================================================================================
LIF: ∞ | ROLE: IMMUTABLE_STANDARD_LIBRARY_ORACLE | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_CONSTANTS_VMAX_ANOMALY_238_ANNIHILATOR_2026_FINALIS_!#()@()@#)(

[THE MANIFESTO]
This scripture defines the 'Primordial Matter' of the Python and Node.js
substrates. It is the absolute boundary of the 'Self'. Matter identified
within these sets is mathematically forbidden from being treated as
External Debt (PIP/NPM), righteously annihilating Anomaly 238.
=================================================================================
"""

from typing import Set, Final

# =============================================================================
# == PYTHON STANDARD LIBRARY: THE TOTAL CENSUS (3.8 - 3.13)                  ==
# =============================================================================
# [ASCENSION 1]: Comprehensive multiversal coverage including OS-specific iron.
PYTHON_STDLIB: Final[frozenset[str]] = frozenset({
    # --- STRATUM 0: THE KERNEL & CORE ---
    "abc", "argparse", "array", "ast", "asyncio", "base64", "binascii", "bisect",
    "builtins", "bz2", "calendar", "collections", "colorsys", "compileall",
    "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg",
    "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
    "difflib", "dis", "distutils", "doctest", "email", "enum", "errno", "faulthandler",
    "fcntl", "filecmp", "fileinput", "fnmatch", "formatter", "fractions", "ftplib",
    "functools", "gc", "getopt", "getpass", "gettext", "glob", "grp", "gzip",
    "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr", "imp",
    "importlib", "inspect", "io", "ipaddress", "itertools", "json", "keyword",
    "lib2to3", "linecache", "locale", "logging", "lzma", "mailbox", "mailcap",
    "marshal", "math", "mimetypes", "mmap", "modulefinder", "msilib", "msvcrt",
    "multiprocessing", "netrc", "nis", "nntplib", "ntpath", "numbers", "operator",
    "optparse", "os", "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil",
    "platform", "plistlib", "poplib", "posix", "posixpath", "pprint", "profile",
    "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc", "queue", "quopri",
    "random", "re", "readline", "resource", "rlcompleter", "runpy", "sched",
    "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal",
    "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "sqlite3",
    "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symbol", "symtable", "sys", "sysconfig", "syslog", "tabnanny",
    "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap", "threading",
    "time", "timeit", "token", "tokenize", "trace", "traceback", "tracemalloc",
    "tty", "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid",
    "venv", "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound",
    "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zlib", "_ast",
    "_thread", "_dummy_thread", "_markupbase", "posix", "nt", "genericpath"
})

# =============================================================================
# == NODE.JS STANDARD LIBRARY: THE TOTAL CENSUS (v16 - v22+)                 ==
# =============================================================================
# [ASCENSION 2]: Support for modern 'node:' URI prefixing and new internal logic.
NODE_STDLIB: Final[frozenset[str]] = frozenset({
    # --- LEGACY & MODERN ALIASES ---
    "assert", "async_hooks", "buffer", "child_process", "cluster", "console",
    "constants", "crypto", "dgram", "diagnostics_channel", "dns", "domain",
    "events", "fs", "fs/promises", "http", "http2", "https", "inspector",
    "module", "net", "os", "path", "path/posix", "path/win32", "perf_hooks",
    "process", "punycode", "querystring", "readline", "repl", "stream",
    "stream/consumers", "stream/promises", "stream/web", "string_decoder",
    "sys", "timers", "timers/promises", "tls", "trace_events", "tty", "url",
    "util", "util/types", "v8", "vm", "wasi", "worker_threads", "zlib",
    # --- MODERN node: PREFIXED STRATUM ---
    "node:assert", "node:assert/strict", "node:async_hooks", "node:buffer",
    "node:child_process", "node:cluster", "node:console", "node:constants",
    "node:crypto", "node:dgram", "node:diagnostics_channel", "node:dns",
    "node:dns/promises", "node:domain", "node:events", "node:fs",
    "node:fs/promises", "node:http", "node:http2", "node:https",
    "node:inspector", "node:module", "node:net", "node:os", "node:path",
    "node:path/posix", "node:path/win32", "node:perf_hooks", "node:process",
    "node:punycode", "node:querystring", "node:readline", "node:repl",
    "node:stream", "node:stream/consumers", "node:stream/promises",
    "node:stream/web", "node:string_decoder", "node:sys", "node:test",
    "node:timers", "node:timers/promises", "node:tls", "node:trace_events",
    "node:tty", "node:url", "node:util", "node:util/types", "node:v8",
    "node:vm", "node:wasi", "node:worker_threads", "node:zlib", "node:sqlite",
    "node:sea"
})


# =============================================================================
# == THE OMEGA VERIFIER                                                      ==
# =============================================================================

def is_standard_library(name: str, ecosystem: str) -> bool:
    """
    =============================================================================
    == THE RITE OF ANCESTRAL RECOGNITION                                       ==
    =============================================================================
    LIF: 1,000,000x | ROLE: IDENTITY_VERIFIER
    O(1) adjudication of whether a module name belongs to the Primordial Iron.
    """
    if not name: return False

    clean_name = name.lower().strip()

    if ecosystem.lower() == "python":
        # Python stdlib often uses underscores internally
        return clean_name in PYTHON_STDLIB or clean_name.replace('-', '_') in PYTHON_STDLIB

    if ecosystem.lower() == "node":
        # Check both prefixed and non-prefixed variants
        if clean_name.startswith('node:'):
            return clean_name in NODE_STDLIB
        return clean_name in NODE_STDLIB or f"node:{clean_name}" in NODE_STDLIB

    return False