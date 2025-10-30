"""
COBOL Parser for identifying REPEAT GROUP and SCR100 patterns.
"""

import re
from typing import List, Dict, Any, Tuple
from app.models.schemas import PatternMatch


class CobolParser:
    """Parser for COBOL code focusing on grid logic patterns."""

    # Patterns for REPEAT GROUP (PRE conversion)
    REPEAT_GROUP_PATTERNS = {
        "repeat_group_def": r"^\s*\d+\s+(\w+[-\w]*)\s+REPEAT\s+(\d+)\s+TIMES",
        "sp2_rx_field": r"^\s*\d+\s+(SP2-RX-\w+)",
        "occurs_clause": r"OCCURS\s+(\d+)\s+TIMES",
        "indexed_by": r"INDEXED\s+BY\s+(\w+)",
        "perform_varying": r"PERFORM\s+.*VARYING\s+(\w+)\s+FROM\s+(\d+)\s+BY\s+(\d+)\s+UNTIL",
    }

    # Patterns for SCR100 (POST conversion)
    SCR100_PATTERNS = {
        "scr100_call": r"CALL\s+['\"]SCR100['\"]",
        "grid_definition": r"^\s*\d+\s+(\w+[-\w]*-GRID)",
        "grid_row": r"^\s*\d+\s+(\w+[-\w]*-ROW)",
        "grid_column": r"^\s*\d+\s+(\w+[-\w]*-COL)",
        "scr100_init": r"MOVE\s+['\"]INIT['\"].*SCR100",
        "scr100_load": r"MOVE\s+['\"]LOAD['\"].*SCR100",
        "scr100_save": r"MOVE\s+['\"]SAVE['\"].*SCR100",
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
