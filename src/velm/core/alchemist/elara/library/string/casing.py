# Path: core/alchemist/elara/library/string_rites/casing.py
# ---------------------------------------------------------

import re
import unicodedata
from typing import Any, List, Union, Final
from ..registry import register_rite

RE_SNAKE_1: Final[re.Pattern] = re.compile(r'(.)([A-Z][a-z]+)')
RE_SNAKE_2: Final[re.Pattern] = re.compile(r'([a-z0-9])([A-Z])')
RE_ACRONYM: Final[re.Pattern] = re.compile(r'([A-Z]+)([A-Z][a-z])') # [ASCENSION 4]

@register_rite("snake")
def to_snake_case(value: Any) -> Union[str, List[str]]:
    if isinstance(value, list): return [to_snake_case(v) for v in value]
    if value is None: return ""
    s = str(value).replace('-', '_')
    # Handle acronyms safely: parseXMLData -> parse_xml_data
    s = RE_ACRONYM.sub(r'\1_\2', s)
    s = RE_SNAKE_1.sub(r'\1_\2', s)
    s = RE_SNAKE_2.sub(r'\1_\2', s)
    return s.lower().replace(" ", "_").strip('_')

@register_rite("pascal")
def to_pascal_case(value: Any) -> Union[str, List[str]]:
    if isinstance(value, list): return[to_pascal_case(v) for v in value]
    s = str(to_snake_case(value))
    return "".join(word.capitalize() for word in s.split("_") if word)

@register_rite("camel")
def to_camel_case(value: Any) -> Union[str, List[str]]:
    if isinstance(value, list): return[to_camel_case(v) for v in value]
    s = to_pascal_case(value)
    return s[0].lower() + s[1:] if s else ""

@register_rite("kebab")
@register_rite("slug")
def to_kebab_case(value: Any) -> Union[str, List[str]]:
    if isinstance(value, list): return[to_kebab_case(v) for v in value]
    s = str(value).lower()
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

@register_rite("screaming")
def to_screaming_snake_case(value: Any) -> Union[str, List[str]]:
    if isinstance(value, list): return[to_screaming_snake_case(v) for v in value]
    return to_snake_case(value).upper()

@register_rite("lower")
def lower_rite(value: Any) -> str: return str(value).lower() if value is not None else ""

@register_rite("upper")
def upper_rite(value: Any) -> str: return str(value).upper() if value is not None else ""

@register_rite("capitalize")
def capitalize_rite(value: Any) -> str: return str(value).capitalize() if value is not None else ""

@register_rite("swapcase")
def swapcase_rite(value: Any) -> str: return str(value).swapcase() if value is not None else ""