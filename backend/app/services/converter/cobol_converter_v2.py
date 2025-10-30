"""
COBOL converter for transforming PRE programs to SCR100 - Version 2 with actual code generation.
"""

import re
from typing import List, Dict, Any, Optional
from app.models.schemas import ConversionResult, ConversionStatus, FieldMapping
from app.services.parser.cobol_parser import CobolParser
from app.services.converter.code_generator import SCR100CodeGenerator


class CobolConverterV2:
    """Converter that generates actual SCR100 code using templates."""

    def __init__(self):
        """Initialize the converter."""
        self.parser = CobolParser()
        self.generator = SCR100CodeGenerator()

    def convert(
        self,
        pre_code: str,
        sp2_code: Optional[str] = None,
        field_mappings: Optional[List[FieldMapping]] = None,
        screen_name: Optional[str] = None,
        grid_id: Optional[int] = None,
    ) -> ConversionResult:
        """
        Convert PRE program to POST with actual SCR100 code generation.

        Args:
            pre_code: PRE conversion COBOL code
            sp2_code: Optional SP2 file for OCCURS detection
            field_mappings: Optional field mappings from user
            screen_name: Optional screen name (auto-detected if not provided)
            grid_id: Optional grid ID (default 9900)

        Returns:
            Conversion result with generated code
        """
        warnings = []
        applied_rules = []

        try:
            # Step 1: Auto-detect screen name if not provided
            if not screen_name:
                screen_name = self.generator.extract_screen_name(pre_code)
                if not screen_name:
                    warnings.append("Could not auto-detect screen name. Using placeholder.")
                    screen_name = "SCREEN"
                else:
                    applied_rules.append({
                        "rule_id": "AUTO_DETECT_SCREEN",
                        "description": f"Auto-detected screen name: {screen_name}",
                        "confidence": 1.0
                    })

            # Step 2: Extract OCCURS fields if no mappings provided
            occurs_fields = []
            if not field_mappings:
                occurs_fields = self.generator.extract_occurs_fields(pre_code, sp2_code)
                if occurs_fields:
                    applied_rules.append({
                        "rule_id": "AUTO_DETECT_OCCURS",
                        "description": f"Auto-detected {len(occurs_fields)} OCCURS fields",
                        "confidence": 0.9
                    })
                    warnings.append(f"Auto-detected {len(occurs_fields)} fields. Review field mappings for accuracy.")
                else:
                    warnings.append("No OCCURS fields detected. Manual field mapping recommended.")

            # Step 3: Find insertion points
            insertion_points = self._find_insertion_points(pre_code)

            # Step 4: Generate code sections
            generated_code = {
                'scr100_copy': self.generator.generate_scr100_copy(),
                'grid_rec': self.generator.generate_grid_rec_structure(field_mappings or [], occurs_fields),
                'grid_rec_len': self.generator.generate_grid_rec_len(),
                'grid_counter': self.generator.generate_grid_counter(),
                'initialize_grid': self.generator.generate_initialize_grid_paragraph(
                    screen_name, field_mappings or [], occurs_fields
                ),
                'load_grid': self.generator.generate_load_grid_paragraph(),
                'load_grid_rows': self.generator.generate_load_grid_rows_paragraph(
                    field_mappings or [], occurs_fields, screen_name
                ),
                'call_scr100': self.generator.generate_call_scr100_paragraph(screen_name, grid_id),
                'get_row_data': self.generator.generate_get_row_data_paragraph(),
                'vbx_handler': self.generator.generate_vbx_event_handler(screen_name),
                'grid_close': self.generator.generate_grid_close(screen_name),
            }

            # Step 5: Insert generated code into PRE program
            converted_code = self._insert_generated_code(
                pre_code,
                insertion_points,
                generated_code,
                screen_name
            )

            # Step 6: Track what was applied
            applied_rules.extend([
                {
                    "rule_id": "ADD_SCR100_COPY",
                    "description": "Added COPY \"SCR100.WS\" to Working Storage",
                    "confidence": 1.0
                },
                {
                    "rule_id": "ADD_GRID_REC",
                    "description": f"Added GRID-REC structure with {len(field_mappings or occurs_fields)} fields",
                    "confidence": 0.95 if field_mappings else 0.8
                },
                {
                    "rule_id": "ADD_GRID_PARAGRAPHS",
                    "description": "Added INITIALIZE-GRID, LOAD-GRID, CALL-SCR100, GET-ROW-DATA paragraphs",
                    "confidence": 1.0
                },
                {
                    "rule_id": "ADD_VBX_HANDLER",
                    "description": "Added VBX event handler to P1000-CONVERSE",
                    "confidence": 0.9
                },
            ])

            # Calculate confidence
            confidence_score = self._calculate_confidence(applied_rules, warnings)

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

    def _find_insertion_points(self, code: str) -> Dict[str, int]:
        """
        Find insertion points in the code for various sections.

        Returns:
            Dictionary mapping section names to line positions
        """
        points = {}
        lines = code.split('\n')

        for i, line in enumerate(lines):
            line_upper = line.upper().strip()

            # Find Working Storage Section
            if 'WORKING-STORAGE' in line_upper and 'SECTION' in line_upper:
                # Find end of COPY statements
                for j in range(i + 1, min(i + 50, len(lines))):
                    if 'COPY' not in lines[j].upper():
                        points['after_copy_statements'] = j
                        break

            # Find P1000-CONVERSE paragraph
            if 'P1000-CONVERSE' in line_upper and line.strip().endswith('.'):
                points['p1000_converse_start'] = i + 1

            # Find end of PROCEDURE DIVISION (before last paragraph)
            if 'PROCEDURE' in line_upper and 'DIVISION' in line_upper:
                points['procedure_division_start'] = i

        # Find end of procedure division for new paragraphs
        # Look for last paragraph before potential STOP RUN or program end
        for i in range(len(lines) - 1, max(0, len(lines) - 100), -1):
            if re.match(r'\s*\w+.*\.\s*$', lines[i]) and 'EXIT' in lines[i].upper():
                points['end_of_procedures'] = i + 1
                break

        if 'end_of_procedures' not in points:
            points['end_of_procedures'] = len(lines) - 10

        return points

    def _insert_generated_code(
        self,
        original_code: str,
        insertion_points: Dict[str, int],
        generated_code: Dict[str, str],
        screen_name: str
    ) -> str:
        """
        Insert generated code sections into the original program.

        Args:
            original_code: Original PRE code
            insertion_points: Insertion point map
            generated_code: Generated code sections
            screen_name: Screen name

        Returns:
            Modified code with insertions
        """
        lines = original_code.split('\n')

        # Insert in reverse order to preserve line numbers
        insertions = []

        # 1. Add grid paragraphs at end
        if 'end_of_procedures' in insertion_points:
            insertions.append((insertion_points['end_of_procedures'], [
                "",
                "      *================================================================",
                "      * SCR100 GRID MANAGEMENT PARAGRAPHS",
                "      *================================================================",
                "",
                generated_code['initialize_grid'],
                "",
                generated_code['load_grid'],
                "",
                generated_code['load_grid_rows'],
                "",
                generated_code['call_scr100'],
                "",
                generated_code['get_row_data'],
                ""
            ]))

        # 2. Add VBX handler to P1000-CONVERSE
        if 'p1000_converse_start' in insertion_points:
            insertions.append((insertion_points['p1000_converse_start'], [
                "      *TODO-SCR100: Add this VBX handler before other key checks",
                generated_code['vbx_handler'],
                ""
            ]))

        # 3. Add grid variables to Working Storage
        if 'after_copy_statements' in insertion_points:
            insertions.append((insertion_points['after_copy_statements'], [
                "",
                "      *================================================================",
                "      * SCR100 Grid Support",
                "      *================================================================",
                generated_code['scr100_copy'],
                "",
                generated_code['grid_rec'],
                generated_code['grid_rec_len'],
                generated_code['grid_counter'],
                ""
            ]))

        # Sort insertions by line number (descending) and apply
        insertions.sort(key=lambda x: x[0], reverse=True)
        for line_num, new_lines in insertions:
            lines[line_num:line_num] = new_lines

        return '\n'.join(lines)

    def _calculate_confidence(self, applied_rules: List[Dict[str, Any]], warnings: List[str]) -> float:
        """Calculate confidence score based on rules applied and warnings."""
        if not applied_rules:
            return 0.0

        avg_confidence = sum(r.get('confidence', 0.5) for r in applied_rules) / len(applied_rules)

        # Reduce confidence for warnings
        warning_penalty = min(0.2, len(warnings) * 0.05)
        confidence = max(0.0, avg_confidence - warning_penalty)

        return min(1.0, confidence)
