"""
Code-based analyzer for comparing PRE and POST COBOL programs.
"""

from typing import List, Dict, Any
from app.models.schemas import ComparisonResult, PatternMatch, AnalysisMethod
from app.services.parser.cobol_parser import CobolParser


class CodeAnalyzer:
    """Code-based analyzer using pattern matching and diff analysis."""

    def __init__(self):
        """Initialize the code analyzer."""
        self.parser = CobolParser()

    def analyze(self, pre_code: str, post_code: str) -> ComparisonResult:
        """
        Analyze PRE and POST programs using code-based pattern matching.

        Args:
            pre_code: PRE conversion COBOL code
            post_code: POST conversion COBOL code

        Returns:
            Comparison result with detected patterns and transformation rules
        """
        # Parse both programs
        pre_patterns = self.parser.parse_pre_program(pre_code)
        post_patterns = self.parser.parse_post_program(post_code)

        # Extract grid logic information
        pre_grid_info = self.parser.identify_grid_logic(pre_code)
        post_grid_info = self.parser.identify_grid_logic(post_code)

        # Detect transformation rules
        transformation_rules = self._detect_transformation_rules(
            pre_code, post_code, pre_patterns, post_patterns
        )

        # Calculate differences
        differences = self._calculate_differences(pre_grid_info, post_grid_info)

        # Calculate similarity
        similarity_score = self.parser.calculate_similarity(pre_code, post_code)

        return ComparisonResult(
            pre_patterns=pre_patterns,
            post_patterns=post_patterns,
            transformation_rules=transformation_rules,
            differences=differences,
            similarity_score=similarity_score,
            analysis_method=AnalysisMethod.CODE_BASED
        )

    def _detect_transformation_rules(
        self,
        pre_code: str,
        post_code: str,
        pre_patterns: List[PatternMatch],
        post_patterns: List[PatternMatch]
    ) -> List[Dict[str, Any]]:
        """
        Detect transformation rules by comparing PRE and POST patterns.

        Args:
            pre_code: PRE conversion code
            post_code: POST conversion code
            pre_patterns: Detected PRE patterns
            post_patterns: Detected POST patterns

        Returns:
            List of transformation rules
        """
        rules = []

        # Rule 1: REPEAT GROUP to SCR100 GRID
        if any(p.pattern_type == "PRE_REPEAT_GROUP_DEF" for p in pre_patterns):
            if any(p.pattern_type == "POST_SCR100_CALL" for p in post_patterns):
                rules.append({
                    "rule_id": "REPEAT_TO_SCR100",
                    "description": "Convert REPEAT GROUP to SCR100 CALL",
                    "from_pattern": "REPEAT n TIMES",
                    "to_pattern": "CALL 'SCR100'",
                    "confidence": 0.9
                })

        # Rule 2: SP2-RX- fields to GRID structure
        pre_sp2_fields = self.parser.extract_field_names(pre_code, "SP2-RX-")
        if pre_sp2_fields and any("GRID" in p.code_snippet for p in post_patterns):
            rules.append({
                "rule_id": "SP2_TO_GRID",
                "description": "Convert SP2-RX- fields to GRID structure",
                "from_pattern": "SP2-RX-*",
                "to_pattern": "*-GRID / *-ROW / *-COL",
                "affected_fields": pre_sp2_fields,
                "confidence": 0.85
            })

        # Rule 3: PERFORM VARYING to SCR100 operations
        if any("PERFORM_VARYING" in p.pattern_type for p in pre_patterns):
            if any("SCR100_LOAD" in p.pattern_type or "SCR100_SAVE" in p.pattern_type for p in post_patterns):
                rules.append({
                    "rule_id": "PERFORM_TO_SCR100_OPS",
                    "description": "Convert PERFORM VARYING loops to SCR100 LOAD/SAVE",
                    "from_pattern": "PERFORM VARYING",
                    "to_pattern": "SCR100 LOAD/SAVE operations",
                    "confidence": 0.8
                })

        # Rule 4: OCCURS clause transformation
        if any("OCCURS_CLAUSE" in p.pattern_type for p in pre_patterns):
            rules.append({
                "rule_id": "OCCURS_TO_GRID_DEF",
                "description": "Convert OCCURS clause to GRID definition",
                "from_pattern": "OCCURS n TIMES",
                "to_pattern": "Grid structure with rows",
                "confidence": 0.75
            })

        return rules

    def _calculate_differences(
        self,
        pre_grid_info: Dict[str, Any],
        post_grid_info: Dict[str, Any]
    ) -> List[str]:
        """
        Calculate high-level differences between PRE and POST programs.

        Args:
            pre_grid_info: PRE grid information
            post_grid_info: POST grid information

        Returns:
            List of difference descriptions
        """
        differences = []

        if pre_grid_info["has_repeat_groups"] and not post_grid_info["has_repeat_groups"]:
            differences.append(
                f"REPEAT GROUPS removed: {len(pre_grid_info['repeat_groups'])} found in PRE"
            )

        if post_grid_info["has_scr100"] and not pre_grid_info["has_scr100"]:
            differences.append(
                f"SCR100 calls added: {len(post_grid_info['scr100_calls'])} found in POST"
            )

        if pre_grid_info["grid_size"] and post_grid_info["grid_size"]:
            if pre_grid_info["grid_size"] != post_grid_info["grid_size"]:
                differences.append(
                    f"Grid size changed: {pre_grid_info['grid_size']} -> {post_grid_info['grid_size']}"
                )
        elif pre_grid_info["grid_size"]:
            differences.append(
                f"Grid size in PRE: {pre_grid_info['grid_size']} rows"
            )

        return differences
