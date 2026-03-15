# Path: core/alchemist/elara/library/string/collections.py
# --------------------------------------------------------

from typing import Any, List, Dict, Tuple, Set
from collections import defaultdict
import itertools
import random
from ..registry import register_rite


@register_rite("length")
@register_rite("count")
@register_rite("len")
def length_rite(value: Any) -> int:
    try:
        return len(value)
    except TypeError:
        return 0


@register_rite("first")
def first_rite(value: Any) -> Any:
    try:
        return next(iter(value))
    except (TypeError, StopIteration):
        return None


@register_rite("last")
def last_rite(value: Any) -> Any:
    try:
        return list(value)[-1]
    except (TypeError, IndexError):
        return None


@register_rite("sort")
def sort_rite(value: Any, reverse: bool = False, attribute: str = None) -> List[Any]:
    """[ASCENSION 30]: Dynamic Sorting with optional Attribute Access."""
    try:
        if attribute:
            return sorted(list(value),
                          key=lambda x: x.get(attribute) if isinstance(x, dict) else getattr(x, attribute, None),
                          reverse=reverse)
        return sorted(list(value), reverse=reverse)
    except TypeError:
        return value


@register_rite("reverse")
def reverse_rite(value: Any) -> List[Any]:
    try:
        return list(reversed(list(value)))
    except TypeError:
        return value


@register_rite("map")
@register_rite("pluck")
def map_rite(value: Any, attribute: str) -> List[Any]:
    if not isinstance(value, (list, tuple, set)): return value
    res = []
    for item in value:
        if isinstance(item, dict):
            res.append(item.get(attribute))
        elif hasattr(item, attribute):
            res.append(getattr(item, attribute))
    return res


@register_rite("groupby")
def groupby_rite(value: Any, attribute: str) -> Dict[Any, List[Any]]:
    if not isinstance(value, (list, tuple, set)): return {}
    grouped = defaultdict(list)
    for item in value:
        val = item.get(attribute) if isinstance(item, dict) else getattr(item, attribute, "None")
        grouped[val].append(item)
    return dict(grouped)


@register_rite("unique")
def unique_rite(value: Any, attribute: str = None) -> List[Any]:
    """[ASCENSION 31]: Attribute-Aware Unique Sieve."""
    try:
        seen = set()
        result = []
        for x in value:
            cmp_val = x.get(attribute) if (attribute and isinstance(x, dict)) else getattr(x, attribute,
                                                                                           None) if attribute else x
            if not (cmp_val in seen or seen.add(cmp_val)):
                result.append(x)
        return result
    except Exception:
        return value


@register_rite("flatten")
def flatten_rite(value: Any) -> List[Any]:
    """[ASCENSION 6]: Recursively flattens nested lists."""
    if not isinstance(value, list): return [value]
    result = []
    for item in value:
        if isinstance(item, list):
            result.extend(flatten_rite(item))
        else:
            result.append(item)
    return result


@register_rite("intersect")
def intersect_rite(value: Any, other: Any) -> List[Any]:
    """[ASCENSION 7]: Returns the overlap of two iterables."""
    try:
        return list(set(value).intersection(set(other)))
    except Exception:
        return []


@register_rite("diff")
def diff_rite(value: Any, other: Any) -> List[Any]:
    """[ASCENSION 7]: Returns items in value that are NOT in other."""
    try:
        return list(set(value).difference(set(other)))
    except Exception:
        return []


@register_rite("zip_to_dict")
def zip_to_dict(keys: Any, values: Any) -> Dict[Any, Any]:
    """[ASCENSION 8]: Zips two lists into a dictionary."""
    try:
        return dict(zip(keys, values))
    except Exception:
        return {}


@register_rite("cartesian")
def cartesian_rite(value: Any, other: Any) -> List[Tuple[Any, Any]]:
    """[ASCENSION 5]: Generates combinations. Essential for CI/CD matrices."""
    try:
        return list(itertools.product(list(value), list(other)))
    except Exception:
        return []


@register_rite("batch")
@register_rite("chunk")
def batch_rite(value: Any, linecount: int, fill_with: Any = None) -> List[List[Any]]:
    """[ASCENSION 32]: The Chunking Matrix. Divides flat arrays into sub-arrays."""
    if not isinstance(value, (list, tuple, set)): return [value]

    lst = list(value)
    n = int(linecount)
    if n <= 0: return [lst]

    result = []
    for i in range(0, len(lst), n):
        chunk = lst[i:i + n]
        if fill_with is not None and len(chunk) < n:
            chunk.extend([fill_with] * (n - len(chunk)))
        result.append(chunk)
    return result


@register_rite("slice")
def slice_rite(value: Any, slices: int, fill_with: Any = None) -> List[List[Any]]:
    """[ASCENSION 33]: Slice Matrix. Divides arrays into N arrays."""
    if not isinstance(value, (list, tuple, set)): return [value]

    seq = list(value)
    length = len(seq)
    slices = int(slices)
    if slices <= 0: return [seq]

    items_per_slice = length // slices
    slices_with_extra = length % slices
    offset = 0
    result = []

    for i in range(slices):
        start = offset + i * items_per_slice
        if i < slices_with_extra:
            offset += 1
        end = offset + (i + 1) * items_per_slice
        chunk = seq[start:end]
        if fill_with is not None and len(chunk) < items_per_slice + (1 if i < slices_with_extra else 0):
            chunk.append(fill_with)
        result.append(chunk)

    return result


@register_rite("dictsort")
def dictsort_rite(value: Any, case_sensitive: bool = False, by: str = 'key', reverse: bool = False) -> List[
    Tuple[Any, Any]]:
    """[ASCENSION 6]: Deterministic Dict-Sort."""
    if not isinstance(value, dict): return value

    idx = 1 if by == 'value' else 0

    def sort_key(item):
        val = item[idx]
        if not case_sensitive and isinstance(val, str):
            return val.lower()
        return val

    return sorted(value.items(), key=sort_key, reverse=reverse)


@register_rite("selectattr")
@register_rite("where")
def selectattr_rite(value: Any, attr: str, test_name: str = None, test_val: Any = None) -> List[Any]:
    """[ASCENSION 34]: Object-Attribute Sieve (Select)."""
    if not isinstance(value, (list, tuple, set)): return []
    from ..tests import test_oracle

    result = []
    for item in value:
        val = item.get(attr) if isinstance(item, dict) else getattr(item, attr, None)

        if test_name:
            args = [test_val] if test_val is not None else []
            if test_oracle.evaluate(val, test_name, *args):
                result.append(item)
        else:
            if val: result.append(item)

    return result


@register_rite("rejectattr")
def rejectattr_rite(value: Any, attr: str, test_name: str = None, test_val: Any = None) -> List[Any]:
    """[ASCENSION 34]: Object-Attribute Sieve (Reject)."""
    if not isinstance(value, (list, tuple, set)): return []
    from ..tests import test_oracle

    result = []
    for item in value:
        val = item.get(attr) if isinstance(item, dict) else getattr(item, attr, None)

        if test_name:
            args = [test_val] if test_val is not None else []
            if not test_oracle.evaluate(val, test_name, *args):
                result.append(item)
        else:
            if not val: result.append(item)

    return result


@register_rite("select")
def select_rite(value: Any, test_name: str, test_val: Any = None) -> List[Any]:
    """[ASCENSION 35]: Flat Array Sieve (Select)."""
    if not isinstance(value, (list, tuple, set)): return []
    from ..tests import test_oracle

    args = [test_val] if test_val is not None else []
    return [item for item in value if test_oracle.evaluate(item, test_name, *args)]


@register_rite("reject")
def reject_rite(value: Any, test_name: str, test_val: Any = None) -> List[Any]:
    """[ASCENSION 35]: Flat Array Sieve (Reject)."""
    if not isinstance(value, (list, tuple, set)): return []
    from ..tests import test_oracle

    args = [test_val] if test_val is not None else []
    return [item for item in value if not test_oracle.evaluate(item, test_name, *args)]


@register_rite("random")
def random_rite(value: Any) -> Any:
    """[ASCENSION 36]: Stochastic Extractor."""
    try:
        return random.choice(list(value))
    except Exception:
        return None


@register_rite("shuffle")
def shuffle_rite(value: Any) -> List[Any]:
    """[ASCENSION 36]: Entropy Shuffler."""
    try:
        lst = list(value)
        random.shuffle(lst)
        return lst
    except Exception:
        return value


@register_rite("keys")
def dict_keys(value: Any) -> List[Any]:
    """[ASCENSION 37]: Object Key Harvester."""
    if isinstance(value, dict): return list(value.keys())
    return []


@register_rite("values")
def dict_values(value: Any) -> List[Any]:
    """[ASCENSION 37]: Object Value Harvester."""
    if isinstance(value, dict): return list(value.values())
    return []


@register_rite("contains")
def contains_rite(value: Any, target: Any) -> bool:
    """[ASCENSION 38]: Structural Presence Adjudicator."""
    try:
        return target in value
    except TypeError:
        return False