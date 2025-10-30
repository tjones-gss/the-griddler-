"""
COBOL Parser for identifying REPEAT GROUP and SCR100 patterns.
"""

import re
from typing import List, Dict, Any, Tuple
from app.models.schemas import PatternMatch


class CobolParser:
    """Parser for COBOL code focusing on grid logic patterns."""

    # Patterns for REPEAT GROUP (PRE conversion) - Based on ORD143.CBL analysis
    REPEAT_GROUP_PATTERNS = {
        # Data structures with OCCURS (line 130: PGM-ENTRIES OCCURS 24 TIMES)
        "occurs_clause": r"OCCURS\s+(\d+)\s+TIMES",
        # Field references in working storage
        "working_storage_occurs": r"^\s*\d+\s+(\w+[-\w]*)\s+OCCURS\s+(\d+)",
        # PERFORM VARYING loops that iterate over arrays
        "perform_varying": r"PERFORM\s+.*VARYING\s+(\w+)\s+FROM\s+(\d+)\s+BY\s+(\d+)\s+UNTIL",
        # P1000-CONVERSE paragraph (main event loop)
        "converse_paragraph": r"^\s*P1000-CONVERSE\.",
        # PERFORM P1000-CONVERSE THRU P1000-EXIT pattern
        "perform_converse": r"PERFORM\s+P1000-CONVERSE\s+THRU\s+P1000-EXIT",
    }

    # Patterns for SCR100 (POST conversion) - Based on ORD143.CBL SCR100 implementation
    SCR100_PATTERNS = {
        # SCR100 copybook (line 199: COPY "SCR100.WS")
        "scr100_copy": r"COPY\s+['\"]SCR100\.WS['\"]",
        # GRID-REC structure (line 205-207)
        "grid_rec_definition": r"^\s*\d+\s+GRID-REC\.",
        # GRID-REC-LEN variable (line 208)
        "grid_rec_len": r"GRID-REC-LEN\s+PIC\s+9",
        # Grid field in SP2 (OES143A-GRID-I PIC S9(4) COMP-5)
        "grid_field_sp2": r"(\w+-GRID-I)\s+PIC\s+S9\(4\)\s+COMP-5",
        # VBX key event handling (line 642: IF [SCREEN]-KEY = SP2-KEY-VBX)
        "vbx_key_check": r"IF\s+\w+-KEY\s*=\s*SP2-KEY-VBX",
        # Grid ID check in VBX handler (line 643: AND [SCREEN]-MENU-ID = [SCREEN]-GRID-I)
        "vbx_grid_check": r"AND\s+\w+-MENU-ID\s*=\s*\w+-GRID-I",
        # SCR100 event processing loop (line 646-647: PERFORM WITH TEST AFTER UNTIL NOT SCR100-MORE-EVENTS)
        "scr100_event_loop": r"UNTIL\s+NOT\s+SCR100-MORE-EVENTS",
        # SET SCR100-PROCESS-EVENTS (line 648)
        "scr100_process_events": r"SET\s+SCR100-PROCESS-EVENTS\s+TO\s+TRUE",
        # SCR100 event types (lines 651, 664)
        "scr100_event_field_chg": r"IF\s+SCR100-EVENT-FIELD-CHG",
        "scr100_event_select": r"IF\s+SCR100-EVENT-SELECT",
        # INITIALIZE-GRID paragraph (line 1254)
        "initialize_grid_para": r"^\s*INITIALIZE-GRID\.",
        # LOAD-GRID paragraph (line 1328)
        "load_grid_para": r"^\s*LOAD-GRID\.",
        # CALL-SCR100 paragraph (line 1355)
        "call_scr100_para": r"^\s*CALL-SCR100\.",
        # GET-ROW-DATA paragraph (line 1320)
        "get_row_data_para": r"^\s*GET-ROW-DATA\.",
        # SET SCR100-INITIALIZE-GRID (line 1258)
        "scr100_initialize": r"SET\s+SCR100-INITIALIZE-GRID\s+TO\s+TRUE",
        # SET SCR100-CLEAR-ROWS (line 1331)
        "scr100_clear_rows": r"SET\s+SCR100-CLEAR-ROWS\s+TO\s+TRUE",
        # SET SCR100-ADD-ROW (line 1342)
        "scr100_add_row": r"SET\s+SCR100-ADD-ROW\s+TO\s+TRUE",
        # SET SCR100-REDRAW-GRID (line 1334)
        "scr100_redraw_grid": r"SET\s+SCR100-REDRAW-GRID\s+TO\s+TRUE",
        # SET SCR100-CLOSE-GRID (line 1178)
        "scr100_close_grid": r"SET\s+SCR100-CLOSE-GRID\s+TO\s+TRUE",
        # SET SCR100-GET-ROW-DATA (line 1322)
        "scr100_get_row_data": r"SET\s+SCR100-GET-ROW-DATA\s+TO\s+TRUE",
        # CALL "GSSERP.SCR100" (line 1363)
        "scr100_call": r"CALL\s+['\"]GSSERP\.SCR100['\"]",
        # SCR100-LINKS usage
        "scr100_links": r"USING\s+SCR100-LINKS",
        # INITIALIZE SCR100-LINKS (line 644, 1256, etc.)
        "initialize_scr100_links": r"INITIALIZE\s+SCR100-LINKS",
    }

    def __init__(self):
        """Initialize the COBOL parser."""
        self.compiled_pre_patterns = {
            name: re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for name, pattern in self.REPEAT_GROUP_PATTERNS.items()
        }
        self.compiled_post_patterns = {
            name: re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for name, pattern in self.SCR100_PATTERNS.items()
        }

    def parse_pre_program(self, code: str) -> List[PatternMatch]:
        """
        Parse a PRE conversion program and extract REPEAT GROUP patterns.

        Args:
            code: COBOL source code

        Returns:
            List of detected patterns
        """
        patterns = []
        lines = code.split('\n')

        for line_num, line in enumerate(lines, start=1):
            # Check each pattern
            for pattern_name, compiled_pattern in self.compiled_pre_patterns.items():
                matches = compiled_pattern.finditer(line)
                for match in matches:
                    patterns.append(PatternMatch(
                        pattern_type=f"PRE_{pattern_name.upper()}",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        context=self._get_context(lines, line_num)
                    ))

        return patterns

    def parse_post_program(self, code: str) -> List[PatternMatch]:
        """
        Parse a POST conversion program and extract SCR100 patterns.

        Args:
            code: COBOL source code

        Returns:
            List of detected patterns
        """
        patterns = []
        lines = code.split('\n')

        for line_num, line in enumerate(lines, start=1):
            # Check each pattern
            for pattern_name, compiled_pattern in self.compiled_post_patterns.items():
                matches = compiled_pattern.finditer(line)
                for match in matches:
                    patterns.append(PatternMatch(
                        pattern_type=f"POST_{pattern_name.upper()}",
                        line_number=line_num,
                        code_snippet=line.strip(),
                        context=self._get_context(lines, line_num)
                    ))

        return patterns

    def extract_data_structures(self, code: str) -> Dict[str, Any]:
        """
        Extract data structure definitions from COBOL code.

        Args:
            code: COBOL source code

        Returns:
            Dictionary containing data structure information
        """
        structures = {
            "working_storage": [],
            "screen_section": [],
            "procedure_division": []
        }

        lines = code.split('\n')
        current_section = None
        current_structure = []

        for line in lines:
            line_upper = line.upper().strip()

            # Detect sections
            if "WORKING-STORAGE SECTION" in line_upper:
                current_section = "working_storage"
            elif "SCREEN SECTION" in line_upper:
                current_section = "screen_section"
            elif "PROCEDURE DIVISION" in line_upper:
                current_section = "procedure_division"

            # Collect structures
            if current_section and line.strip():
                structures[current_section].append(line.strip())

        return structures

    def identify_grid_logic(self, code: str) -> Dict[str, Any]:
        """
        Identify grid-related logic in COBOL code.

        Args:
            code: COBOL source code

        Returns:
            Dictionary with grid logic information
        """
        grid_info = {
            "has_repeat_groups": False,
            "has_scr100": False,
            "repeat_groups": [],
            "scr100_calls": [],
            "grid_size": None,
        }

        # Check for REPEAT GROUP
        repeat_pattern = re.compile(r"REPEAT\s+(\d+)\s+TIMES", re.IGNORECASE)
        repeat_matches = repeat_pattern.finditer(code)
        for match in repeat_matches:
            grid_info["has_repeat_groups"] = True
            grid_info["repeat_groups"].append({
                "size": int(match.group(1)),
                "context": match.group(0)
            })

        # Check for SCR100
        scr100_pattern = re.compile(r"CALL\s+['\"]SCR100['\"]", re.IGNORECASE)
        scr100_matches = scr100_pattern.finditer(code)
        for match in scr100_matches:
            grid_info["has_scr100"] = True
            grid_info["scr100_calls"].append(match.group(0))

        # Estimate grid size
        if grid_info["repeat_groups"]:
            grid_info["grid_size"] = max(
                rg["size"] for rg in grid_info["repeat_groups"]
            )

        return grid_info

    def _get_context(self, lines: List[str], line_num: int, context_size: int = 2) -> str:
        """
        Get surrounding context for a line.

        Args:
            lines: All lines of code
            line_num: Target line number (1-indexed)
            context_size: Number of lines before and after

        Returns:
            Context string
        """
        start = max(0, line_num - context_size - 1)
        end = min(len(lines), line_num + context_size)
        context_lines = lines[start:end]
        return '\n'.join(context_lines)

    def calculate_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate similarity between two COBOL programs.

        Args:
            code1: First COBOL program
            code2: Second COBOL program

        Returns:
            Similarity score between 0 and 1
        """
        # Simple line-based similarity
        lines1 = set(line.strip() for line in code1.split('\n') if line.strip())
        lines2 = set(line.strip() for line in code2.split('\n') if line.strip())

        if not lines1 or not lines2:
            return 0.0

        intersection = len(lines1 & lines2)
        union = len(lines1 | lines2)

        return intersection / union if union > 0 else 0.0

    def extract_field_names(self, code: str, pattern_prefix: str = "SP2-RX-") -> List[str]:
        """
        Extract field names with a specific prefix.

        Args:
            code: COBOL source code
            pattern_prefix: Prefix to search for

        Returns:
            List of field names
        """
        pattern = re.compile(rf"(\b{re.escape(pattern_prefix)}\w+)", re.IGNORECASE)
        matches = pattern.findall(code)
        return list(set(matches))  # Remove duplicates
