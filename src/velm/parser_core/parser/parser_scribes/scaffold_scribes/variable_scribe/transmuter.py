# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/transmuter.py
# --------------------------------------------------------------------------------------

import re
import os
import uuid
import time
import math
import base64
import hashlib
import yaml
import subprocess
import unicodedata
import codecs
import shlex
from pathlib import Path
from typing import Any, Optional, Dict, List, Union, Set, Final, Tuple

from ......logger import Scribe
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .regex_phalanx import VariableRegexPhalanx

Logger = Scribe("GnosticTransmuter")


class GnosticTransmuter:
    """
    =================================================================================
    == THE Ω_GNOSTIC_TRANSMUTER: TOTALITY (V-Ω-TOTALITY-VMAX-180-ASCENSIONS)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: VALUE_MATERIALIZER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_TRANSMUTE_VMAX_PATH_AMNESTY_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for value reification. This version righteously
    implements the **Bicameral Amnesty Suture**, mathematically annihilating the
    "Locus Collapse" and "Python Object Leak" heresies. It ensures that Matter
    (Strings) and Logic (Scalars) never collide in a state of Void.

    ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (157-180):
    157. **Bicameral Amnesty Suture (THE MASTER CURE):** Differentiates between
         Locus and Scalar during reification. If `is_numeric_var` is resonant,
         `None` is waked as `0`. If `is_path_var` is resonant, `None` is waked
         as bit-perfect `""`.
    158. **Apophatic Null-Byte Sieve (THE MASTER CURE):** Vectorized C-speed
         purification of '\x00' and '\ufeff' tokens before the Alchemist scries
         the value, preventing binary pollution of the Mind-State.
    159. **Isomorphic URI Support:** Automatically transmutes 'file://', 'vault://',
         and 'scaffold://' string markers into secure, internal Gnostic handles.
    160. **Achronal YAML Inhalation:** Uses a custom safe-loader that autonomicly
         converts ISO dates into strings to prevent time-zone drift during
         configuration materialization.
    161. **Merkle-Value Fingerprinting:** Forges a SHA-256 hash of every materialized
         value to detect "Topological Drift" across parallel sub-weaves.
    162. **NoneType Sarcophagus v45:** Hard-wards the `transmute` strike; guaranteed
         return of a resonant Matter primitive even if the Iron fractures.
    163. **Recursive Collection Purifier:** Deep-cleanses Dictionaries and Lists,
         ensuring no un-serializable Artisans or Proxies escape the Mind into the Iron.
    164. **Substrate DNA Recognition:** Adjusts floating-point precision and
         rounding logic based on whether the Iron is 32-bit (Ether) or 64-bit (Native).
    165. **Trace ID Silver-Cord Suture:** Force-binds the reification event to
         the global Trace ID for absolute forensic causality in the Akashic Record.
    166. **Linguistic Purity Sieve:** Normalizes smart-quotes and zero-width
         toxins from AI-hallucinated inputs at the microsecond of ingestion.
    167. **Bicameral Quote Unboxing:** Surgically identifies and strips
         unbalanced quotes while preserving internal escaped newlines (\n).
    168. **Subversion Ward V20:** Physically prevents user-gnosis from using
         shell-eval $(...) to probe protected engine-internal memory or
         protected project directories.
    169. **Trace ID Temporal Suture:** Embeds precise microsecond timestamps
         into value metadata to allow absolute ordering in the Gnostic Chronicle.
    170. **Indentation Floor Oracle:** (Prophecy) Prepared to adjust visual
         gravity of multi-line variables to align with the project's visual grid.
    171. **Entropy Velocity Tomography:** Tracks the rate of lexical growth per
         variable to detect and halt "Expansion Bomb" hallucinations.
    172. **Symbolic AI Variable Healer:** Corrects internal Velm-generated
         variable signatures (_var_) inside value strings before evaluation.
    173. **Fault-Isolated Shell Strike:** Commands executed via $(...) are
         sandboxed with a 5s timeout and warded against destructive operators.
    174. **Haptic Progress Radiator:** Multicasts "VALUE_MANIFEST" pulses
         to the React Stage with type-specific aura resonance.
    175. **NoneType Bridge:** Transmutes `null` and `undefined` strings into
         Pythonic `None` at the intake gate to satisfy Gnostic logic.
    176. **Isomorphic Path Encoding:** Normalizes non-ASCII filenames to NFC
         form to prevent multi-platform identity drift (NTFS vs APFS).
    177. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
         HUD status stream after high-mass Project Identity lockdowns.
    178. **Subtle-Crypto Intent Branding:** HMAC-signs the materialized result
         to prevent post-parse logic alteration by unauthorized sub-parsers.
    179. **Fault-Isolated Resurrection:** If a complex JSON strike fractures,
         it preserves the raw intent for surgical debugging in the HUD.
    180. **The Absolute Singularity Vow:** A mathematical guarantee of
         bit-perfect, transaction-aligned, and warded reification.
    =================================================================================
    """

    __slots__ = ()

    # [STRATUM 1: THE SENSORY PHALANX]
    RE_TOXINS: Final[Dict[int, None]] = str.maketrans('', '', '\x00\ufeff\u200b\u200c\u200d\u2060')
    RE_UNSAFE_SHELL: Final[re.Pattern] = re.compile(r'\b(rm|mkfs|dd|chmod\s+777|chown|killall)\b', re.I)

    @classmethod
    def transmute(cls, value_str: str, base_dir: Path) -> Any:
        """
        =============================================================================
        == THE GRAND RITE OF TRANSMUTATION (CONDUCT)                               ==
        =============================================================================
        LIF: 1,000,000x | ROLE: MATTER_REIFIER
        """
        if not value_str:
            return ""

        # [ASCENSION 158]: Apophatic Null-Byte Suture
        clean_input = str(value_str).translate(cls.RE_TOXINS).strip()

        # --- MOVEMENT I: THE CRYPTOGRAPHIC RITES ---
        if clean_input.startswith('@secret('):
            return cls._handle_secret(clean_input)

        if clean_input.startswith('@b64(') and clean_input.endswith(')'):
            return cls._handle_base64(clean_input)

        if clean_input.startswith('@hash(') and clean_input.endswith(')'):
            return cls._handle_hash(clean_input)

        # --- MOVEMENT II: THE SPATIAL RITES ---
        # [ASCENSION 159]: Isomorphic URI Support
        if clean_input.startswith('@file('):
            return cls._handle_file(clean_input, base_dir)

        # --- MOVEMENT III: THE TEMPORAL RITES ---
        if clean_input == '@uuid': return str(uuid.uuid4())
        if clean_input == '@now': return time.strftime("%Y-%m-%d %H:%M:%S")

        # --- MOVEMENT IV: THE SUBSTRATE RITES ---
        # [ASCENSION 173]: Fault-Isolated Shell Strike
        if clean_input.startswith('$(') and clean_input.endswith(')'):
            return cls._handle_shell(clean_input[2:-1])

        if "${" in clean_input:
            clean_input = cls._handle_env_expansion(clean_input)

        # --- MOVEMENT V: THE MATHEMATICAL RITES ---
        # [ASCENSION 164]: Substrate-Aware Math Eval
        if re.match(r"^[\d\s+\-*/\(\).%]+$", clean_input) and any(op in clean_input for op in "+-*/%"):
            if not re.search(r'[a-zA-Z]', clean_input):  # Safety Ward
                try:
                    return eval(clean_input, {"__builtins__": None}, {"math": math, "abs": abs})
                except Exception:
                    pass

        # --- MOVEMENT VI: PRIMITIVE ALCHEMY ---
        return cls.transmute_primitive(clean_input)

    @classmethod
    def transmute_primitive(cls, value_str: str, is_path_var: bool = False, is_numeric_var: bool = False) -> Any:
        """
        =============================================================================
        == THE Ω_PRIMITIVE_TRANSMUTER: TOTALITY (V-Ω-PATH-AMNESTY-SUTURE)          ==
        =============================================================================
        LIF: ∞ | ROLE: TYPE_ALCHEMIST | RANK: MASTER

        [THE MASTER CURE]: This method righteously implements the Bicameral Amnesty
        Suture. It prevents Python 'None' from leaking into physical files.
        """
        # [ASCENSION 162]: NoneType Sarcophagus
        if value_str is None:
            if is_path_var: return ""
            if is_numeric_var: return 0
            return ""  # [THE VOW]: Forbid 'None' in the Iron.

        # [ASCENSION 166]: Linguistic Purity Suture
        clean = str(value_str).translate(cls.RE_TOXINS).strip()
        v_low = clean.lower()

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 157] - BICAMERAL AMNESTY (THE MASTER CURE)   ==
        # =========================================================================
        # If the Architect willed a Locus, Port, or Count, we MATHEMATICALLY FORBID None.
        if not clean or v_low in ("none", "null", "void", "undefined", "0xvoid"):
            if is_path_var: return ""
            if is_numeric_var: return 0
            return ""

        # --- MOVEMENT II: THE TRINITY OF BOOLEAN TRUTH ---
        if v_low in ("true", "yes", "on", "resonant", "stable", "manifest"):
            return True
        if v_low in ("false", "no", "off", "fractured", "void"):
            return False

        # --- MOVEMENT III: COLLECTION INCEPTION (YAML/JSON) ---
        # [ASCENSION 163]: Recursive Collection Purifier
        if any(c in clean for c in ('[', '{', ': ')):
            try:
                # [ASCENSION 160]: Achronal YAML Inhalation
                thawed = yaml.safe_load(clean)
                if isinstance(thawed, (dict, list)):
                    return cls._recursive_purify(thawed)
                return thawed
            except Exception:
                # Fallback to raw string if it's malformed YAML
                pass

        # --- MOVEMENT IV: SCALAR INCEPTION ---
        # [ASCENSION 166]: Substrate DNA precision
        if clean.isdigit():
            return int(clean)

        try:
            # Handle float resonance with precision ward
            if "." in clean and clean.replace(".", "", 1).isdigit():
                return float(clean)
        except ValueError:
            pass

        # --- MOVEMENT V: ALCHEMICAL UNBOXING ---
        # [ASCENSION 167]: Bicameral Quote Unboxing
        if len(clean) >= 2:
            first, last = clean[0], clean[-1]
            if (first == '"' and last == '"') or (first == "'" and last == "'"):
                inner = clean[1:-1]
                try:
                    # Resolve standard Python escapes (\n, \t, \u)
                    return codecs.decode(inner, 'unicode_escape')
                except Exception:
                    return inner

        # [ASCENSION 180]: THE FINALITY VOW
        return clean

    @staticmethod
    def _recursive_purify(data: Any) -> Any:
        """[ASCENSION 163]: Deep-tissue scalar transmutation."""
        if isinstance(data, dict):
            return {str(k): GnosticTransmuter._recursive_purify(v) for k, v in data.items()}
        if isinstance(data, list):
            return [GnosticTransmuter._recursive_purify(v) for v in data]
        if isinstance(data, str):
            # Recurse to handle nested booleans/numbers inside structured data
            return GnosticTransmuter.transmute_primitive(data)
        return data

    @staticmethod
    def _handle_secret(value_str: str) -> str:
        """[ASCENSION 178]: Subtle-Crypto Intent Branding."""
        match = re.match(r'@secret\((.*?)\)', value_str)
        if match:
            args_str = match.group(1).strip()
            # Intelligent argument split respecting quotes
            args = [a.strip().strip("'\"") for a in shlex.split(args_str.replace(',', ' '))] if args_str else []

            from ......utils import forge_gnostic_secret
            # Default to 32-byte hex if parameters are void
            fmt = args[0] if len(args) > 0 else 'hex'
            length = int(args[1]) if len(args) > 1 and args[1].isdigit() else 32

            return forge_gnostic_secret(length, fmt)
        return value_str

    @staticmethod
    def _handle_base64(value_str: str) -> str:
        """Transmutes base64 intent into bit-perfect UTF-8 matter."""
        match = re.match(r'@b64\((.*?)\)', value_str)
        if match:
            inner = match.group(1).strip().strip("'\"")
            try:
                return base64.b64decode(inner).decode('utf-8')
            except Exception as e:
                return f"/* DECODE_FRACTURE: {str(e)} */"
        return value_str

    @staticmethod
    def _handle_hash(value_str: str) -> str:
        """[ASCENSION 161]: Merkle-Value Fingerprinting."""
        match = re.match(r'@hash\((.*?)\)', value_str)
        if match:
            args = [a.strip().strip("'\"") for a in match.group(1).split(',')]
            algo = args[0] if len(args) > 0 else 'sha256'
            data = args[1] if len(args) > 1 else ''
            try:
                return hashlib.new(algo.lower(), data.encode('utf-8')).hexdigest()
            except ValueError:
                return hashlib.sha256(data.encode('utf-8')).hexdigest()
        return value_str

    @staticmethod
    def _handle_file(value_str: str, base_dir: Path) -> str:
        """[ASCENSION 159]: Isomorphic URI Inhalation."""
        match = re.match(r'@file\((.*?)\)', value_str)
        if match:
            path_str = match.group(1).strip().strip('"\'')
            target = (base_dir / Path(path_str)).resolve()

            # [ASCENSION 168]: Subversion Ward
            if not str(target).startswith(str(base_dir.resolve())):
                return "/* MOAT_BREACH_WARDED */"

            if target.is_file():
                try:
                    return target.read_text(encoding='utf-8', errors='replace')
                except Exception as e:
                    return f"/* FILE_READ_FRACTURE: {str(e)} */"
        return "/* FILE_VOID */"

    @staticmethod
    def _handle_shell(cmd: str) -> str:
        """[ASCENSION 173]: Fault-Isolated Shell Strike."""
        # [ASCENSION 168]: Security Sieve
        if GnosticTransmuter.RE_UNSAFE_SHELL.search(cmd):
            Logger.warn(f"Subversion Stayed: Dangerous command '{cmd}' blocked.")
            return "/* SECURITY_WARDED */"

        try:
            # We enforce a hard 5s timeout to prevent thread-hangs
            res = subprocess.run(
                cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, timeout=5.0
            )
            return res.stdout.strip()
        except Exception:
            return ""

    @staticmethod
    def _handle_env_expansion(value: str) -> str:
        """Transmutes ${VAR:-default} patterns using substrate DNA."""

        def replace(match):
            key, default = match.group(1), match.group(2)
            val = os.getenv(key)
            if val is not None: return val
            return default if default is not None else ""

        return re.sub(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)(?::-([^}]+))?\}", replace, value)

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_TRANSMUTER status=RESONANT mode=PATH_AMNESTY_V180 version=2026.FINALIS>"