# Path: scaffold/parser_core/parser/engine.py
# -------------------------------------------
import re
import argparse
import logging
import uuid
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union

# --- THE DIVINE SUMMONS OF THE NEW MODULES ---
from .ast_weaver import GnosticASTWeaver
from .parser_scribes import SCRIBE_PANTHEON, FormScribe
from ..block_consumer import GnosticBlockConsumer

# --- CONTRACTS & GNOSIS ---
from ...contracts.data_contracts import (
    ScaffoldItem, GnosticVessel, GnosticDossier, GnosticLineType, _GnosticNode, GnosticContract
)
from ...contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ...contracts.symphony_contracts import Edict, EdictType
from ...core.alchemist import get_alchemist
from ...jurisprudence_core.gnostic_type_system import GnosticTypeParser

try:
    from ...logger import Scribe

    Logger = Scribe("ApotheosisParser")
except ImportError:
    Logger = logging.getLogger("ApotheosisParser")


class ApotheosisParser:
    """
    =================================================================================
    == THE APOTHEOSIS PARSER (V-Ω-LIVING-GRIMOIRE-ULTIMA)                          ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The central intelligence that transmutes raw text into Gnostic Truth.
    It has been ascended with a Living Grimoire, allowing it to distinguish between
    the grand symphony and the individual movements (`@task`, `@macro`) within it.
    """

    def __init__(self, grammar_key: str = 'scaffold'):
        """[ELEVATION 1] The Gnostic Triage of Tongues."""
        if grammar_key not in SCRIBE_PANTHEON:
            raise ArtisanHeresy(f"Unknown Grammar Key: {grammar_key}")

        self.Logger = Logger
        self.grammar_key = grammar_key
        self.parse_session_id = str(uuid.uuid4())[:8]

        self._reset_parser_state()

        self.scribes: Dict[str, Any] = self._forge_scribe_pantheon()
        self.alchemist = get_alchemist()

    def _forge_scribe_key(self, key: Any) -> str:
        """
        [ASCENSION 3] The Polyglot Key Smith.
        A divine, sentient artisan that transmutes any Gnostic Key (Enum or str)
        into its one true, lowercase string form for the Pantheon's registry.
        """
        if hasattr(key, 'name'):
            return key.name.lower()
        return str(key).lower()

    def _forge_scribe_pantheon(self) -> Dict[str, Any]:
        """
        =================================================================================
        == THE GOD-ENGINE OF SCRIBE FORGING (V-Ω-ETERNALLY-PURIFIED)                   ==
        =================================================================================
        The divine foundry, its Gaze now pure. It instantiates the Scribes for the
        active grammar. The `scribe_name` heresy is annihilated by the Self-Aware
        base class.
        """
        from .parser_scribes import SCRIBE_PANTHEON, FormScribe

        pantheon: Dict[str, FormScribe] = {}

        grimoire_for_grammar = SCRIBE_PANTHEON.get(self.grammar_key)
        if not grimoire_for_grammar:
            raise ArtisanHeresy(f"META-HERESY: The Grimoire holds no Gnosis for the '{self.grammar_key}' tongue.")

        self.Logger.verbose(f"The Scribe Foundry awakens for the '{self.grammar_key}' tongue...")

        unique_scribe_classes = set(grimoire_for_grammar.values())

        for ScribeClass in unique_scribe_classes:
            # We ensure the soul is pure before giving it form.
            if not issubclass(ScribeClass, FormScribe):
                self.Logger.error(
                    f"META-HERESY: '{ScribeClass.__name__}' does not honor the sacred FormScribe contract.")
                continue

            instance_key = ScribeClass.__name__.lower()
            if instance_key in pantheon:
                continue

            try:
                # === THE RITE OF PURE CONSECRATION ===
                # The Scribe is born. It is passed the Parser (self).
                # If it has a custom __init__, it uses it.
                # If it inherits FormScribe.__init__, it now accepts the single argument
                # and divines its own name.
                pantheon[instance_key] = ScribeClass(self)
                # === THE APOTHEOSIS IS COMPLETE ===
            except TypeError as te:
                # [DIAGNOSTIC] Catch signature mismatches explicitly
                self.Logger.error(
                    f"Signature Heresy forging '{ScribeClass.__name__}': {te}. Ensure __init__ accepts (self, parser).",
                    exc_info=True
                )
                raise
            except Exception as e:
                self.Logger.error(
                    f"A catastrophic paradox occurred while forging the '{ScribeClass.__name__}' scribe: {e}",
                    exc_info=True
                )
                raise

        forged_names = sorted(pantheon.keys())
        self.Logger.success(
            f"The Scribe Pantheon is whole. {len(pantheon)} artisans forged: [dim cyan]{', '.join(forged_names)}[/dim cyan]"
        )
        return pantheon

    def _forge_scribe_name(self, class_name: str) -> str:
        """
        [ASCENSION 11] The Heuristic Name Smith.
        Transmutes a Scribe's class name (e.g., `StructuralScribe`) into its
        luminous, human-readable form (e.g., `Structural Scribe`).
        """
        # Remove "Scribe" suffix and add spaces before capital letters
        base_name = class_name.replace("Scribe", "")
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', base_name)

    def _reset_parser_state(self):
        """[ELEVATION 8] The Polyglot Reset."""
        self.items_by_path: Dict[str, ScaffoldItem] = {}
        self.raw_items: List[ScaffoldItem] = []
        # === THE DIVINE HEALING ===
        # The vessel's soul is ascended. It now honors the sacred 3-tuple contract.
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]]]] = []
        # === THE APOTHEOSIS IS COMPLETE ===

        # --- [THE FIX & ELEVATION 3] The Living Grimoire ---
        self.edicts: List[Edict] = []
        self.tasks: Dict[str, List[Edict]] = {}
        self.macros: Dict[str, Dict[str, Any]] = {}
        # --- THE HERESY IS ANNIHILATED ---

        self.heresies: List[Heresy] = []
        self.all_rites_are_pure: bool = True
        self.file_path: Optional[Path] = None
        self.line_offset: int = 0
        self.variables: Dict[str, Any] = {}
        self.blueprint_vars: Dict[str, str] = {}
        self.dossier: GnosticDossier = GnosticDossier()
        self.gnostic_ast: Optional[_GnosticNode] = None
        self.contracts: Dict[str, GnosticContract] = {}
        self.variable_contracts: Dict[str, str] = {}
        self.pending_permissions: Optional[str] = None
        self.imported_files: set[Path] = set()

    def parse_string(
            self,
            content: str,
            file_path_context: Optional[Path] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            line_offset: int = 0,
            overrides: Optional[Dict[str, Any]] = None
    ) -> Tuple[
        'ApotheosisParser',
        List[ScaffoldItem],
        List[Tuple[str, int, Optional[List[str]]]],  # The one true, sacred 3-tuple contract
        List[Edict],
        Dict[str, Any],
        GnosticDossier
    ]:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF PERCEPTION (V-Ω-ETERNALLY-PURIFIED)                   ==
        =================================================================================
        The main parsing loop is now pure. It no longer proclaims items itself. It
        delegates the Rite of Proclamation to the Scribes, honoring their sovereignty
        and ensuring no line is misinterpreted.
        =================================================================================
        """
        self.file_path = file_path_context
        self.line_offset = line_offset
        self.base_path = file_path_context.parent if file_path_context else Path.cwd()

        if pre_resolved_vars: self.variables.update(pre_resolved_vars)
        if overrides: self.variables.update(overrides)

        lines = content.splitlines()
        i = 0
        self.Logger.info(f"[{self.parse_session_id}] Parsing begins. Total lines: {len(lines)}")

        try:
            while i < len(lines):
                line = lines[i]
                original_indent = self._calculate_original_indent(line)

                from ...parser_core.lexer_core.inquisitor import GnosticLineInquisitor
                vessel = GnosticLineInquisitor.inquire(
                    raw_line=line, line_num=i + 1 + self.line_offset,
                    parser=self, grammar_codex_key=self.grammar_key,
                    original_indent=original_indent
                )

                scribe = self._get_scribe_for_vessel(vessel)
                prev_i = i

                if scribe:
                    # The Scribe is now responsible for consuming all its relevant lines
                    # AND for calling `_proclaim_final_item` if it wants an item created.
                    i = scribe.conduct(lines, i, vessel)
                else:
                    # If no scribe, we just advance past the line. Heresy was already logged.
                    i += 1

                # Safety valve against infinite loops
                if i <= prev_i:
                    self.Logger.error(
                        f"PARSING PARADOX: Cursor stuck at L{i + 1} on '{line.strip()}'. Forcing advance.")
                    i += 1

        except Exception as e:
            self._proclaim_heresy(
                "META_HERESY_INQUISITOR_FRACTURED",
                f"Catastrophic failure during main parsing loop at line {i + 1}",
                details=f"The Parser's core symphony was shattered by an unhandled paradox.",
                exception_obj=e
            )

        self.Logger.info(
            f"[{self.parse_session_id}] Parsing Complete. Raw Items: {len(self.raw_items)}. Edicts: {len(self.edicts)}. Tasks: {len(self.tasks)}.")

        all_gnosis = {**self.blueprint_vars, **self.variables}
        self._adjudicate_contracts(all_gnosis)

        from ...utils.gnosis_discovery import discover_required_gnosis

        self.dossier = discover_required_gnosis(
            execution_plan=self.raw_items,
            post_run_commands=self.post_run_commands,
            blueprint_vars=all_gnosis
        )
        self.dossier.heresies.extend(self.heresies)

        return (self, self.raw_items, self.post_run_commands, self.edicts, all_gnosis, self.dossier)

    def _adjudicate_contracts(self, all_gnosis):
        """Validates variables against registered contracts."""
        for var_name, type_sig in self.variable_contracts.items():
            if var_name in all_gnosis:
                value = all_gnosis[var_name]
                if isinstance(value, str) and ("{{" in value or "{%" in value):
                    continue
                try:
                    gnostic_type = GnosticTypeParser.parse(type_sig)
                    gnostic_type.validate(value, f"$$ {var_name}", self.contracts)
                except ValueError as e:
                    heresy = Heresy(
                        message=f"Contract Violation for '$$ {var_name}'",
                        details=f"Value: {value}\nContract: {type_sig}\nError: {str(e)}",
                        severity=HeresySeverity.CRITICAL, line_num=0,
                        line_content=f"$$ {var_name}: {type_sig} = {value}",
                        suggestion="Ensure the variable value matches the Gnostic Contract."
                    )
                    self.heresies.append(heresy)
                    self.all_rites_are_pure = False
                except Exception as e:
                    self.Logger.error(f"Type System Paradox for '$$ {var_name}': {e}")

    def _proclaim_final_item(self, vessel: GnosticVessel):
        if not vessel.is_valid or vessel.line_type == GnosticLineType.VOID:
            return
        item = ScaffoldItem.model_validate(vessel.model_dump())
        if self.pending_permissions:
            item.permissions = self.pending_permissions
            self.pending_permissions = None
        if item.line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT):
            self.raw_items.append(item)
            return
        if item.line_type == GnosticLineType.FORM and item.path:
            self.items_by_path[item.path.as_posix()] = item
        self.raw_items.append(item)

    def _get_scribe_for_vessel(self, vessel: GnosticVessel) -> Optional[FormScribe]:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC TRIAGE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)          ==
        =================================================================================
        LIF: ∞ (ETERNAL & DIVINE)

        This is the divine artisan in its final, eternal form. It is a pure, declarative
        Conductor whose mind is the `SCRIBE_PANTHEON`. It no longer thinks; it perceives
        and summons with absolute Gnostic certainty. The heresy of the `if/elif` chain has
        been annihilated from all timelines.

        ### THE PANTHEON OF 12 ASCENDED FACULTIES:

        1.  **The Gnostic Grimoire (Declarative Mind):** The profane `if/elif` chain is
            annihilated. Its mind is now a single, sacred map lookup, making perception
            instantaneous and infinitely extensible.
        2.  **The Law of Gnostic Triage:** Its logic is a pure, two-stage Gaze. It first
            perceives the `grammar_key`, then the `line_type` or `edict_type`.
        3.  **The Annihilation of the Fallback:** The separate, profane "fallback" block
            has been absorbed into the core Gaze, ensuring a single, unified path of logic.
        4.  **The Polyglot Soul:** The Grimoire architecture makes the Inquisitor a true
            Polyglot. To teach it a new rite, one must only inscribe a new verse in the
            `SCRIBE_PANTHEON` scripture.
        5.  **The Scribe of the Void:** The initial Gaze for `is_valid` and `VOID` remains
            the unbreakable first law.
        6.  **The Unbreakable Ward of Grace:** If a Scribe is not found in the Grimoire,
            it proclaims a luminous, helpful warning without shattering the symphony.
        7.  **The Luminous Voice:** Its proclamation of a missing Scribe is now a rich,
            diagnostic message revealing the full Gnostic context of the failure.
        8.  **The Pure Gnostic Contract:** Its signature and return value are eternally pure.
        9.  **The Sovereign Mind:** Its purpose is pure dispatch. It contains no business
            logic; it is the telephone exchange of the Parser.
        10. **The Symphony's Dual Gaze:** For the Language of Will (`symphony`), it now
            performs a sacred, two-fold Gaze, checking first for the specific `EdictType`
            and then falling back to the general `GnosticLineType` (for comments).
        11. **The Form's Singular Gaze:** For the Language of Form (`scaffold`), its Gaze
            is one of singular purpose, using `GnosticLineType` as the one true key.
        12. **The Final Word:** This is the apotheosis of the Parser's dispatch logic. It
            is faster, purer, and infinitely more maintainable. The Great Work is eternal.
        """
        # FACULTY 5: The Scribe of the Void
        if not vessel.is_valid or vessel.line_type == GnosticLineType.VOID:
            return None

        # FACULTY 2: The Law of Gnostic Triage
        from .parser_scribes import SCRIBE_PANTHEON  # Just-in-time summons

        scribe_map = SCRIBE_PANTHEON.get(self.grammar_key)
        if not scribe_map:
            self.Logger.error(f"META-HERESY: No Scribe Pantheon defined for grammar '{self.grammar_key}'.")
            return None

        ScribeClass = None

        # FACULTY 11 & 10: The Dual & Singular Gaze
        if self.grammar_key == 'scaffold':
            # The Gaze is pure. It seeks the soul of the LineType directly in the Grimoire.
            ScribeClass = scribe_map.get(vessel.line_type)
        elif self.grammar_key == 'symphony':
            # The Gaze is dual. It seeks the Edict's soul first, for it is more specific.
            ScribeClass = scribe_map.get(vessel.edict_type)
            # If the Edict's soul is a void, it falls back to the general LineType.
            if not ScribeClass:
                ScribeClass = scribe_map.get(vessel.line_type)

        if ScribeClass:
            # The Scribe is summoned from the parser's own living Pantheon of instances.
            # We find it by its class name, its one true, immutable identity.
            instance_key = ScribeClass.__name__.lower()
            scribe_instance = self.scribes.get(instance_key)

            if scribe_instance:
                return scribe_instance
            else:
                # This is a meta-heresy: the law exists in the Grimoire, but the Scribe was not forged.
                # This is a paradox that should be architecturally impossible with the new Forge.
                self.Logger.error(
                    f"META-HERESY: The Scribe '{ScribeClass.__name__}' is in the Grimoire but not the Pantheon. Gaze averted."
                )
                return None

        # FACULTY 6 & 7: The Unbreakable Ward & Luminous Voice
        self.Logger.warn(
            f"Gnostic Adjudication: No Scribe is consecrated for this Gnosis. The line will be treated as a void.\n"
            f"   [dim]Locus:[/dim] [yellow]L{vessel.line_num}[/yellow]\n"
            f"   [dim]Grammar:[/dim] [cyan]{self.grammar_key}[/cyan]\n"
            f"   [dim]LineType:[/dim] [magenta]{vessel.line_type.name if vessel.line_type else 'None'}[/magenta]\n"
            f"   [dim]EdictType:[/dim] [green]{vessel.edict_type.name if vessel.edict_type else 'None'}[/green]"
        )
        return None

    def _calculate_original_indent(self, line: str) -> int:
        """[ELEVATION 11] The Indentation Auditor."""
        consumer = GnosticBlockConsumer([])
        return consumer._measure_visual_depth(line)

    def _consume_indented_block_with_context(self, lines: List[str], start_index: int, parent_indent: int) -> Tuple[
        List[str], int]:
        consumer = GnosticBlockConsumer(lines)
        return consumer.consume_indented_block(start_index, parent_indent)

    def _proclaim_heresy(self, key: str, item: Union[GnosticVessel, ScaffoldItem, str], **kwargs):
        """[ELEVATION 10] The Universal Heresy Proclamation."""
        from ...jurisprudence_core.jurisprudence import forge_heresy_vessel
        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', 0) or self.line_offset
        heresy = forge_heresy_vessel(key=key, line_num=line_num, line_content=raw_scripture,
                                     details=kwargs.get('details'))
        if severity := kwargs.get('severity'): heresy.severity = severity
        if suggestion := kwargs.get('suggestion'): heresy.suggestion = suggestion
        self.heresies.append(heresy)
        if heresy.severity == HeresySeverity.CRITICAL:
            if hasattr(item, 'is_valid'): item.is_valid = False
            self.all_rites_are_pure = False

    def resolve_reality(self) -> List[ScaffoldItem]:
        """[ELEVATION 9] The Bridge of Realization."""
        weaver = GnosticASTWeaver(self)
        self.gnostic_ast = weaver.weave_gnostic_ast()
        merged_vars = {**self.variables, **self.blueprint_vars}
        if hasattr(self.alchemist, 'resolve_gnostic_graph'):
            resolved_vars = self.alchemist.resolve_gnostic_graph(merged_vars)
            self.variables.update(resolved_vars)

        # This is where the magic happens for symphony files. The weaver resolves the AST
        # into a final list of edicts, tasks, and macros. For scaffold files, it resolves
        # logic into a flat list of file items.
        final_items = weaver.resolve_paths_from_ast(self.gnostic_ast)
        return final_items