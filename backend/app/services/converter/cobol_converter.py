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
        Apply default transformation rules.

        Args:
            code: Source code

        Returns:
            Tuple of (converted code, applied rules)
        """
        converted = code
        applied_rules = []

        # Rule 1: Convert REPEAT GROUP to GRID structure
        converted, rule1_applied = self._convert_repeat_to_grid(converted)
        if rule1_applied:
            applied_rules.append({
                "rule_id": "REPEAT_TO_GRID",
                "description": "Converted REPEAT n TIMES to GRID structure",
                "confidence": 0.85
            })

        # Rule 2: Convert SP2-RX- fields to GRID fields
        converted, rule2_applied = self._convert_sp2_to_grid_fields(converted)
        if rule2_applied:
            applied_rules.append({
                "rule_id": "SP2_TO_GRID_FIELDS",
                "description": "Converted SP2-RX- fields to GRID structure",
                "confidence": 0.8
            })

        # Rule 3: Add SCR100 calls
        converted, rule3_applied = self._add_scr100_calls(converted)
        if rule3_applied:
            applied_rules.append({
                "rule_id": "ADD_SCR100_CALLS",
                "description": "Added SCR100 initialization and calls",
                "confidence": 0.75
            })

        # Rule 4: Convert PERFORM VARYING loops
        converted, rule4_applied = self._convert_perform_varying(converted)
        if rule4_applied:
            applied_rules.append({
                "rule_id": "PERFORM_TO_SCR100",
                "description": "Converted PERFORM VARYING to SCR100 operations",
                "confidence": 0.7
            })

        return converted, applied_rules

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
