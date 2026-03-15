# Path: core/alchemist/elara/library/string/text.py
# -------------------------------------------------

import re
import textwrap
import unicodedata
import html
from typing import Any, List, Optional
from ..registry import register_rite

RE_WHITESPACE = re.compile(r'\s+')
RE_MARKDOWN_CLEAN = re.compile(r'([\#\*\_\~`]|\[.*?\]\(.*?\))')
RE_URL = re.compile(r'(https?://[^\s]+)')

# [ASCENSION 1]: The Pluralization Dictionary
IRREGULAR_PLURALS = {
    "child": "children", "person": "people", "man": "men", "woman": "women",
    "mouse": "mice", "goose": "geese", "tooth": "teeth", "foot": "feet",
    "datum": "data", "analysis": "analyses", "index": "indices"
}
IRREGULAR_SINGULARS = {v: k for k, v in IRREGULAR_PLURALS.items()}


@register_rite("pluralize")
def pluralize_rite(value: Any) -> str:
    """[ASCENSION 1]: The Pluralization Oracle."""
    word = str(value).strip()
    if not word: return ""
    lower_word = word.lower()

    if lower_word in IRREGULAR_PLURALS:
        return IRREGULAR_PLURALS[lower_word] if word.islower() else IRREGULAR_PLURALS[lower_word].capitalize()

    if lower_word.endswith(('s', 'x', 'z', 'sh', 'ch')):
        return word + "es"
    if lower_word.endswith('y') and len(word) > 1 and lower_word[-2] not in "aeiou":
        return word[:-1] + "ies"

    return word + "s"


@register_rite("singularize")
def singularize_rite(value: Any) -> str:
    """[ASCENSION 1]: The Singularization Oracle."""
    word = str(value).strip()
    if not word: return ""
    lower_word = word.lower()

    if lower_word in IRREGULAR_SINGULARS:
        return IRREGULAR_SINGULARS[lower_word] if word.islower() else IRREGULAR_SINGULARS[lower_word].capitalize()

    if lower_word.endswith("ies") and len(word) > 3 and lower_word[-4] not in "aeiou":
        return word[:-3] + "y"
    if lower_word.endswith("es") and lower_word[-3:-2] in ('s', 'x', 'z', 'h'):
        return word[:-2]
    if lower_word.endswith("s") and not lower_word.endswith("ss"):
        return word[:-1]

    return word


@register_rite("ascii")
def ascii_rite(value: Any) -> str:
    """[ASCENSION 2]: The Diacritic Exorcist."""
    try:
        s = str(value)
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    except Exception:
        return str(value)


@register_rite("truncate_words")
def truncate_words_rite(value: Any, words: int = 10, suffix: str = "...") -> str:
    """[ASCENSION 3]: The Substrate-Aware Truncator."""
    s = str(value)
    parts = s.split()
    if len(parts) <= int(words): return s
    return " ".join(parts[:int(words)]) + str(suffix)


@register_rite("truncate")
def truncate_rite(value: Any, length: int = 255, killwords: bool = False, end: str = "...") -> str:
    """[ASCENSION 4]: Strict Character-Bound Truncator."""
    s = str(value)
    if len(s) <= length: return s
    if killwords:
        return s[:length - len(end)] + end
    else:
        truncated = s[:length - len(end)]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            return truncated[:last_space] + end
        return truncated + end


@register_rite("trim")
@register_rite("strip")
def trim_rite(value: Any, chars: Optional[str] = None) -> str:
    return str(value).strip(chars) if value is not None else ""


@register_rite("split")
def split_rite(value: Any, separator: str = " ", maxsplit: int = -1) -> List[str]:
    return str(value).split(separator, maxsplit) if value is not None else[]


@register_rite("join")
def join_rite(value: Any, separator: str = "") -> str:
    if not isinstance(value, (list, tuple, set)): return str(value)
    return separator.join(str(v) for v in value)


@register_rite("replace")
def replace_rite(value: Any, old: str, new: str, count: int = -1) -> str:
    return str(value).replace(str(old), str(new), count)


@register_rite("regex_replace")
def regex_replace(value: Any, pattern: str, replacement: str) -> str:
    try:
        return re.sub(str(pattern), str(replacement), str(value))
    except Exception:
        return str(value)


@register_rite("regex_findall")
def regex_findall(value: Any, pattern: str) -> List[str]:
    """[ASCENSION 5]: Extracts all matching regex instances into an array."""
    try:
        return re.findall(str(pattern), str(value))
    except Exception:
        return[]


@register_rite("collapse")
def collapse_whitespace(value: Any) -> str:
    return RE_WHITESPACE.sub(' ', str(value)).strip()


@register_rite("strip_markdown")
def strip_markdown_rite(value: Any) -> str:
    return RE_MARKDOWN_CLEAN.sub('', str(value)).strip()


@register_rite("wordwrap")
def wordwrap_rite(value: Any, width: int = 79, break_long_words: bool = True, wrapstring: str = "\n") -> str:
    """[ASCENSION 8]: String-Wrap Geometer."""
    if not value: return ""
    lines = str(value).splitlines()
    wrapped_lines =[]
    for line in lines:
        if not line.strip():
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(textwrap.wrap(line, width=int(width), break_long_words=break_long_words))
    return wrapstring.join(wrapped_lines)


@register_rite("striptags")
def striptags_rite(value: Any) -> str:
    """[ASCENSION 23]: The Semantic Strip-Tags."""
    if not value: return ""
    return re.sub(r'<[^>]+>', '', str(value))


@register_rite("escape")
@register_rite("e")
def escape_html(value: Any) -> str:
    """[ASCENSION 24]: HTML Content Encapsulation."""
    return html.escape(str(value))


@register_rite("unescape")
def unescape_html(value: Any) -> str:
    """[ASCENSION 25]: HTML Content Decapsulation."""
    return html.unescape(str(value))


@register_rite("urlize")
def urlize_rite(value: Any) -> str:
    """[ASCENSION 26]: Autonomic Link Generation."""
    return RE_URL.sub(r'<a href="\1" rel="noopener">\1</a>', str(value))


@register_rite("nl2br")
def nl2br_rite(value: Any) -> str:
    """[ASCENSION 27]: Physical Newline to HTML Transmutator."""
    return str(value).replace('\n', '<br>\n')


@register_rite("center")
def center_rite(value: Any, width: int = 80, fillchar: str = " ") -> str:
    """[ASCENSION 28]: Center-Alignment Gravity."""
    return str(value).center(int(width), str(fillchar))


@register_rite("ljust")
def ljust_rite(value: Any, width: int = 80, fillchar: str = " ") -> str:
    return str(value).ljust(int(width), str(fillchar))


@register_rite("rjust")
def rjust_rite(value: Any, width: int = 80, fillchar: str = " ") -> str:
    return str(value).rjust(int(width), str(fillchar))


@register_rite("wordcount")
def wordcount_rite(value: Any) -> int:
    """[ASCENSION 29]: Word Density Tomography."""
    if not value: return 0
    return len(re.findall(r'\b\w+\b', str(value)))