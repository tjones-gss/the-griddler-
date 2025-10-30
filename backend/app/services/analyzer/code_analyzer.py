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
        Detect SCR100 grid conversion transformation rules based on ORD143.CBL patterns.

        Args:
            pre_code: PRE conversion code
            post_code: POST conversion code
            pre_patterns: Detected PRE patterns
            post_patterns: Detected POST patterns

        Returns:
            List of transformation rules
        """
        rules = []

        # Rule 1: Add COPY "SCR100.WS" to Working Storage
        has_scr100_copy = any("SCR100_COPY" in p.pattern_type for p in post_patterns)
        if has_scr100_copy and "WORKING-STORAGE" in pre_code.upper():
            rules.append({
                "rule_id": "ADD_SCR100_COPY",
                "description": "Add COPY \"SCR100.WS\" to Working Storage Section",
                "from_pattern": "No SCR100 copybook",
                "to_pattern": "COPY \"SCR100.WS\"",
                "location": "After COPY statements in Working Storage",
                "confidence": 1.0
            })

        # Rule 2: OCCURS to GRID-REC structure
        has_occurs = any("OCCURS_CLAUSE" in p.pattern_type for p in pre_patterns)
        has_grid_rec = any("GRID_REC_DEFINITION" in p.pattern_type for p in post_patterns)
        if has_occurs and has_grid_rec:
            rules.append({
                "rule_id": "OCCURS_TO_GRID_REC",
                "description": "Convert OCCURS arrays to GRID-REC structure",
                "from_pattern": "03 [NAME]-ENTRIES OCCURS n TIMES\n   05 [FIELD]  PIC X",
                "to_pattern": "01 GRID-REC\n   05 GRID-[FIELD]  PIC X\n01 GRID-REC-LEN PIC 9(09)",
                "location": "Working Storage Section",
                "confidence": 0.95
            })

        # Rule 3: Add Grid ID field to SP2 file
        has_grid_field = any("GRID_FIELD_SP2" in p.pattern_type for p in post_patterns)
        if has_grid_field:
            rules.append({
                "rule_id": "ADD_GRID_FIELD_SP2",
                "description": "Add grid control field to SP2 screen file",
                "from_pattern": "No grid field",
                "to_pattern": "05 [SCREEN]-GRID-I PIC S9(4) COMP-5 VALUE +[UNIQUE_ID]",
                "location": "SP2 file (screen definition)",
                "confidence": 1.0
            })

        # Rule 4: Add VBX event handling in P1000-CONVERSE
        has_vbx_check = any("VBX_KEY_CHECK" in p.pattern_type for p in post_patterns)
        has_converse = any("CONVERSE_PARAGRAPH" in p.pattern_type for p in pre_patterns)
        if has_vbx_check and has_converse:
            rules.append({
                "rule_id": "ADD_VBX_EVENT_HANDLER",
                "description": "Add VBX event handling logic to P1000-CONVERSE paragraph",
                "from_pattern": "IF [SCREEN]-KEY = ...",
                "to_pattern": "IF [SCREEN]-KEY = SP2-KEY-VBX\n   AND [SCREEN]-MENU-ID = [SCREEN]-GRID-I\n   [event processing loop]",
                "location": "P1000-CONVERSE paragraph",
                "confidence": 0.95
            })

        # Rule 5: Add SCR100 event processing loop
        has_event_loop = any("SCRE100_EVENT_LOOP" in p.pattern_type for p in post_patterns)
        if has_event_loop:
            rules.append({
                "rule_id": "ADD_SCR100_EVENT_LOOP",
                "description": "Add SCR100 event processing loop",
                "from_pattern": "No event loop",
                "to_pattern": "PERFORM WITH TEST AFTER\n   UNTIL NOT SCR100-MORE-EVENTS\n   SET SCR100-PROCESS-EVENTS TO TRUE",
                "location": "VBX event handler in P1000-CONVERSE",
                "confidence": 1.0
            })

        # Rule 6: Add INITIALIZE-GRID paragraph
        has_init_grid = any("INITIALIZE_GRID_PARA" in p.pattern_type for p in post_patterns)
        if has_init_grid:
            rules.append({
                "rule_id": "ADD_INITIALIZE_GRID",
                "description": "Add INITIALIZE-GRID paragraph with grid setup",
                "from_pattern": "No grid initialization",
                "to_pattern": "INITIALIZE-GRID paragraph with:\n- SET SCR100-INITIALIZE-GRID TO TRUE\n- Grid dimensions, headers, widths, formats\n- PERFORM CALL-SCR100",
                "location": "New paragraph after screen open",
                "confidence": 1.0
            })

        # Rule 7: Add LOAD-GRID paragraphs
        has_load_grid = any("LOAD_GRID_PARA" in p.pattern_type for p in post_patterns)
        if has_load_grid:
            rules.append({
                "rule_id": "ADD_LOAD_GRID",
                "description": "Add LOAD-GRID and LOAD-GRID-ROWS paragraphs",
                "from_pattern": "PERFORM VARYING loop to populate array",
                "to_pattern": "LOAD-GRID:\n- SET SCR100-CLEAR-ROWS\n- PERFORM LOAD-GRID-ROWS\n- SET SCR100-REDRAW-GRID",
                "location": "Replace array population logic",
                "confidence": 0.9
            })

        # Rule 8: Add CALL-SCR100 paragraph
        has_call_scr100 = any("CALL_SCR100_PARA" in p.pattern_type for p in post_patterns)
        if has_call_scr100:
            rules.append({
                "rule_id": "ADD_CALL_SCR100",
                "description": "Add CALL-SCR100 paragraph with error handling",
                "from_pattern": "No SCR100 call wrapper",
                "to_pattern": "CALL-SCR100:\n- Move screen/grid identifiers\n- CALL \"GSSERP.SCR100\" USING SCR100-LINKS\n- ON OVERFLOW error handling",
                "location": "New utility paragraph",
                "confidence": 1.0
            })

        # Rule 9: Add GET-ROW-DATA paragraph
        has_get_row = any("GET_ROW_DATA_PARA" in p.pattern_type for p in post_patterns)
        if has_get_row:
            rules.append({
                "rule_id": "ADD_GET_ROW_DATA",
                "description": "Add GET-ROW-DATA paragraph for row selection",
                "from_pattern": "Direct array access",
                "to_pattern": "GET-ROW-DATA:\n- SET SCR100-GET-ROW-DATA TO TRUE\n- SET SCR100-ROW-DATA TO ADDRESS OF GRID-REC\n- PERFORM CALL-SCR100",
                "location": "Event handler support paragraph",
                "confidence": 1.0
            })

        # Rule 10: Add grid close logic
        has_close_grid = any("SCR100_CLOSE_GRID" in p.pattern_type for p in post_patterns)
        if has_close_grid:
            rules.append({
                "rule_id": "ADD_GRID_CLOSE",
                "description": "Add grid cleanup when closing screen",
                "from_pattern": "No grid cleanup",
                "to_pattern": "SET SCR100-CLOSE-GRID TO TRUE\nPERFORM CALL-SCR100",
                "location": "PROC-CLOSE-WINDOW or screen exit paragraph",
                "confidence": 1.0
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
