"""
COBOL converter for transforming REPEAT GROUP logic to SCR100.
"""

import re
from typing import List, Dict, Any, Optional
from app.models.schemas import ConversionResult, ConversionStatus
from app.services.parser.cobol_parser import CobolParser


class CobolConverter:
    """Converter for transforming PRE programs to use SCR100."""

    def __init__(self):
        """Initialize the converter."""
        self.parser = CobolParser()

    def convert(
        self,
        pre_code: str,
        rules: Optional[List[Dict[str, Any]]] = None,
        auto_detect_rules: bool = True
    ) -> ConversionResult:
        """
        Convert PRE program to use SCR100 logic.

        Args:
            pre_code: PRE conversion COBOL code
            rules: Custom conversion rules (optional)
            auto_detect_rules: Auto-detect rules from code

        Returns:
            Conversion result
        """
        warnings = []
        applied_rules = []
        converted_code = pre_code

        try:
            # Auto-detect patterns if requested
            if auto_detect_rules:
                detected_patterns = self.parser.parse_pre_program(pre_code)
                grid_info = self.parser.identify_grid_logic(pre_code)

                if not grid_info["has_repeat_groups"]:
                    warnings.append("No REPEAT GROUP patterns detected in source code")

            # Apply transformation rules
            if rules:
                # Use custom rules
                for rule in rules:
                    converted_code, rule_applied = self._apply_rule(
                        converted_code, rule
                    )
                    if rule_applied:
                        applied_rules.append(rule)
            else:
                # Use default transformation rules
                converted_code, default_rules = self._apply_default_transformations(
                    converted_code
                )
                applied_rules = default_rules

            # Calculate confidence score
            confidence_score = self._calculate_confidence(
                pre_code, converted_code, applied_rules
            )

            # Validate the conversion
            validation_warnings = self._validate_conversion(converted_code)
            warnings.extend(validation_warnings)

            status = ConversionStatus.COMPLETED if confidence_score > 0.5 else ConversionStatus.FAILED

            return ConversionResult(
                converted_code=converted_code,
                applied_rules=applied_rules,
                warnings=warnings,
                status=status,
                confidence_score=confidence_score
            )

        except Exception as e:
            return ConversionResult(
                converted_code=pre_code,
                applied_rules=[],
                warnings=[f"Conversion failed: {str(e)}"],
                status=ConversionStatus.FAILED,
                confidence_score=0.0
            )

    def _apply_default_transformations(
        self, code: str
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Apply SCR100 grid conversion transformations based on ORD143.CBL patterns.
        NOTE: This provides guidance markers, not full automatic conversion.

        Args:
            code: Source code

        Returns:
            Tuple of (converted code, applied rules)
        """
        converted = code
        applied_rules = []

        # Rule 1: Mark OCCURS clauses for GRID-REC conversion
        converted, rule1_applied = self._mark_occurs_for_grid_rec(converted)
        if rule1_applied:
            applied_rules.append({
                "rule_id": "MARK_OCCURS_TO_GRID_REC",
                "description": "Marked OCCURS clauses for GRID-REC structure conversion",
                "action_required": "Create GRID-REC with fields matching OCCURS structure",
                "confidence": 0.95
            })

        # Rule 2: Mark Working Storage for SCR100.WS addition
        converted, rule2_applied = self._mark_working_storage_for_scr100(converted)
        if rule2_applied:
            applied_rules.append({
                "rule_id": "MARK_ADD_SCR100_COPY",
                "description": "Marked location to add COPY \"SCR100.WS\"",
                "action_required": "Add COPY \"SCR100.WS\" after other COPY statements",
                "confidence": 1.0
            })

        # Rule 3: Mark P1000-CONVERSE for VBX handler
        converted, rule3_applied = self._mark_converse_for_vbx(converted)
        if rule3_applied:
            applied_rules.append({
                "rule_id": "MARK_ADD_VBX_HANDLER",
                "description": "Marked P1000-CONVERSE for VBX event handling",
                "action_required": "Add VBX key check and SCR100 event processing loop",
                "confidence": 0.95
            })

        # Rule 4: Mark locations for new grid paragraphs
        converted, rule4_applied = self._mark_for_grid_paragraphs(converted)
        if rule4_applied:
            applied_rules.append({
                "rule_id": "MARK_ADD_GRID_PARAGRAPHS",
                "description": "Marked locations for INITIALIZE-GRID, LOAD-GRID, CALL-SCR100, GET-ROW-DATA",
                "action_required": "Add grid management paragraphs at end of program",
                "confidence": 1.0
            })

        # Rule 5: Identify screen open location for INITIALIZE-GRID call
        converted, rule5_applied = self._mark_screen_open_for_init(converted)
        if rule5_applied:
            applied_rules.append({
                "rule_id": "MARK_CALL_INITIALIZE_GRID",
                "description": "Marked location to call INITIALIZE-GRID and LOAD-GRID",
                "action_required": "Add PERFORM INITIALIZE-GRID and PERFORM LOAD-GRID after screen open",
                "confidence": 0.9
            })

        # Rule 6: Identify PERFORM VARYING loops for grid loading
        converted, rule6_applied = self._mark_perform_varying_for_grid(converted)
        if rule6_applied:
            applied_rules.append({
                "rule_id": "MARK_PERFORM_TO_LOAD_GRID",
                "description": "Marked PERFORM VARYING loops that should call LOAD-GRID",
                "action_required": "Replace array population loops with PERFORM LOAD-GRID",
                "confidence": 0.85
            })

        return converted, applied_rules

    def _mark_occurs_for_grid_rec(self, code: str) -> tuple[str, bool]:
        """Mark OCCURS clauses that need GRID-REC conversion."""
        pattern = re.compile(
            r'(\s*)(\d+\s+\w+[-\w]*\s+OCCURS\s+\d+\s+TIMES)',
            re.IGNORECASE | re.MULTILINE
        )

        def mark_func(match):
            indent = match.group(1)
            original = match.group(2)
            return (
                f"{indent}      *TODO-SCR100: Convert this OCCURS to GRID-REC structure\n"
                f"{indent}{original}"
            )

        converted = pattern.sub(mark_func, code)
        return converted, converted != code

    def _mark_working_storage_for_scr100(self, code: str) -> tuple[str, bool]:
        """Mark Working Storage section to add SCR100.WS."""
        pattern = re.compile(
            r'(WORKING-STORAGE\s+SECTION\.\s*\n)',
            re.IGNORECASE
        )

        if pattern.search(code):
            converted = pattern.sub(
                r'\1\n      *TODO-SCR100: Add COPY "SCR100.WS" after other COPY statements\n',
                code,
                count=1
            )
            return converted, True
        return code, False

    def _mark_converse_for_vbx(self, code: str) -> tuple[str, bool]:
        """Mark P1000-CONVERSE paragraph for VBX handler addition."""
        pattern = re.compile(
            r'(\s*P1000-CONVERSE\.\s*\n)',
            re.IGNORECASE
        )

        if pattern.search(code):
            converted = pattern.sub(
                r'\1      *TODO-SCR100: Add VBX key check (IF [SCREEN]-KEY = SP2-KEY-VBX)\n'
                r'      *TODO-SCR100: Add grid ID check (AND [SCREEN]-MENU-ID = [SCREEN]-GRID-I)\n'
                r'      *TODO-SCR100: Add SCR100 event processing loop\n',
                code,
                count=1
            )
            return converted, True
        return code, False

    def _mark_for_grid_paragraphs(self, code: str) -> tuple[str, bool]:
        """Mark end of program for grid paragraph additions."""
        # Find end of procedure division (before last period or END PROGRAM)
        if re.search(r'PROCEDURE\s+DIVISION', code, re.IGNORECASE):
            marker = (
                "\n      *TODO-SCR100: Add these paragraphs at end of program:\n"
                "      *TODO-SCR100: - INITIALIZE-GRID (grid setup with headers, widths, formats)\n"
                "      *TODO-SCR100: - LOAD-GRID (clear rows, load rows, redraw)\n"
                "      *TODO-SCR100: - LOAD-GRID-ROWS (loop through data, add rows)\n"
                "      *TODO-SCR100: - CALL-SCR100 (wrapper for SCR100 calls with error handling)\n"
                "      *TODO-SCR100: - GET-ROW-DATA (retrieve selected row data)\n"
            )
            converted = code + marker
            return converted, True
        return code, False

    def _mark_screen_open_for_init(self, code: str) -> tuple[str, bool]:
        """Mark location after screen open for grid initialization."""
        # Look for COMPROC-CALL-SP2 or similar screen open patterns
        pattern = re.compile(
            r'(PERFORM\s+COMPROC-CALL-SP2.*?\.\s*\n)',
            re.IGNORECASE | re.DOTALL
        )

        if pattern.search(code):
            converted = pattern.sub(
                r'\1      *TODO-SCR100: Add PERFORM INITIALIZE-GRID here\n'
                r'      *TODO-SCR100: Add PERFORM LOAD-GRID here\n',
                code,
                count=1
            )
            return converted, True
        return code, False

    def _mark_perform_varying_for_grid(self, code: str) -> tuple[str, bool]:
        """Mark PERFORM VARYING loops that populate arrays."""
        pattern = re.compile(
            r'(\s*PERFORM\s+VARYING\s+\w+\s+FROM\s+\d+.*?END-PERFORM)',
            re.IGNORECASE | re.DOTALL
        )

        def mark_func(match):
            original = match.group(1)
            return (
                f"      *TODO-SCR100: Replace this array population loop with PERFORM LOAD-GRID\n"
                f"{original}\n"
                f"      *TODO-SCR100: End of loop to be replaced\n"
            )

        converted = pattern.sub(mark_func, code)
        return converted, converted != code

    def _convert_repeat_to_grid(self, code: str) -> tuple[str, bool]:
        """
        Convert REPEAT GROUP definitions to GRID structures.

        Args:
            code: Source code

        Returns:
            Tuple of (converted code, was_applied)
        """
        # Pattern: 05 FIELD-NAME REPEAT 10 TIMES
        pattern = re.compile(
            r'(\s*)(\d+)\s+(\w+[-\w]*)\s+REPEAT\s+(\d+)\s+TIMES',
            re.IGNORECASE
        )

        def replace_func(match):
            indent = match.group(1)
            level = match.group(2)
            field_name = match.group(3)
            times = match.group(4)

            # Generate GRID structure
            return (
                f"{indent}{level} {field_name}-GRID.\n"
                f"{indent}   {int(level)+1:02d} {field_name}-ROW OCCURS {times} TIMES.\n"
                f"{indent}      {int(level)+2:02d} {field_name}-COL PIC X(20)."
            )

        converted = pattern.sub(replace_func, code)
        return converted, converted != code

    def _convert_sp2_to_grid_fields(self, code: str) -> tuple[str, bool]:
        """
        Convert SP2-RX- field references to GRID field references.

        Args:
            code: Source code

        Returns:
            Tuple of (converted code, was_applied)
        """
        # Pattern: SP2-RX-FIELDNAME(INDEX)
        pattern = re.compile(
            r'\bSP2-RX-(\w+)\s*\(\s*(\w+)\s*\)',
            re.IGNORECASE
        )

        def replace_func(match):
            field_name = match.group(1)
            index = match.group(2)
            return f"{field_name}-COL ({index})"

        converted = pattern.sub(replace_func, code)

        # Also convert simple SP2-RX- references
        simple_pattern = re.compile(r'\bSP2-RX-(\w+)\b', re.IGNORECASE)
        converted = simple_pattern.sub(r'\1-COL', converted)

        return converted, converted != code

    def _add_scr100_calls(self, code: str) -> tuple[str, bool]:
        """
        Add SCR100 initialization and calls.

        Args:
            code: Source code

        Returns:
            Tuple of (converted code, was_applied)
        """
        # Check if SCR100 is already present
        if re.search(r"CALL\s+['\"]SCR100['\"]", code, re.IGNORECASE):
            return code, False

        # Find PROCEDURE DIVISION
        proc_pattern = re.compile(r'(PROCEDURE\s+DIVISION.*?\n)', re.IGNORECASE)
        match = proc_pattern.search(code)

        if match:
            insert_pos = match.end()
            scr100_init = (
                "\n"
                "      * Initialize SCR100 grid\n"
                "           MOVE 'INIT' TO SCR100-FUNCTION.\n"
                "           CALL 'SCR100' USING SCR100-PARAMS.\n"
                "\n"
            )
            converted = code[:insert_pos] + scr100_init + code[insert_pos:]
            return converted, True

        return code, False

    def _convert_perform_varying(self, code: str) -> tuple[str, bool]:
        """
        Convert PERFORM VARYING loops to SCR100 operations.

        Args:
            code: Source code

        Returns:
            Tuple of (converted code, was_applied)
        """
        # This is a complex transformation that requires context
        # For now, add a comment indicating manual review needed
        pattern = re.compile(
            r'(PERFORM\s+.*VARYING\s+\w+.*UNTIL.*?\n)',
            re.IGNORECASE | re.DOTALL
        )

        def replace_func(match):
            original = match.group(1)
            return (
                f"{original}"
                f"      * TODO: Review for SCR100 LOAD/SAVE operation\n"
            )

        converted = pattern.sub(replace_func, code)
        return converted, converted != code

    def _apply_rule(
        self, code: str, rule: Dict[str, Any]
    ) -> tuple[str, bool]:
        """
        Apply a custom transformation rule.

        Args:
            code: Source code
            rule: Transformation rule

        Returns:
            Tuple of (converted code, was_applied)
        """
        rule_id = rule.get("rule_id", "")

        if rule_id == "REPEAT_TO_GRID":
            return self._convert_repeat_to_grid(code)
        elif rule_id == "SP2_TO_GRID_FIELDS":
            return self._convert_sp2_to_grid_fields(code)
        elif rule_id == "ADD_SCR100_CALLS":
            return self._add_scr100_calls(code)
        elif rule_id == "PERFORM_TO_SCR100":
            return self._convert_perform_varying(code)

        return code, False

    def _calculate_confidence(
        self, original: str, converted: str, rules: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate confidence score for the conversion.

        Args:
            original: Original code
            converted: Converted code
            rules: Applied rules

        Returns:
            Confidence score (0-1)
        """
        if not rules:
            return 0.0

        # Base confidence on rules applied
        avg_confidence = sum(r.get("confidence", 0.5) for r in rules) / len(rules)

        # Adjust based on code changes
        if original == converted:
            return 0.0

        # Check if SCR100 is now present
        if re.search(r"CALL\s+['\"]SCR100['\"]", converted, re.IGNORECASE):
            avg_confidence += 0.1

        return min(1.0, avg_confidence)

    def _validate_conversion(self, code: str) -> List[str]:
        """
        Validate the converted code and generate warnings.

        Args:
            code: Converted code

        Returns:
            List of warnings
        """
        warnings = []

        # Check for TODO comments
        if "TODO" in code:
            warnings.append("Manual review required: TODO comments present")

        # Check for remaining SP2-RX- references
        sp2_pattern = re.compile(r'\bSP2-RX-\w+', re.IGNORECASE)
        if sp2_pattern.search(code):
            warnings.append("Some SP2-RX- fields may not have been converted")

        # Check for SCR100 presence
        if not re.search(r"CALL\s+['\"]SCR100['\"]", code, re.IGNORECASE):
            warnings.append("No SCR100 calls detected in converted code")

        return warnings
