"""
Code generator for SCR100 conversion - generates actual COBOL code.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from app.models.schemas import FieldMapping


class SCR100CodeGenerator:
    """Generates actual SCR100 COBOL code from templates."""

    def __init__(self):
        """Initialize the code generator."""
        pass

    def extract_screen_name(self, code: str) -> Optional[str]:
        """
        Extract screen name from MOVE statements like:
        MOVE "OES143A" TO OES143A-NEXT-PANEL

        Args:
            code: COBOL source code

        Returns:
            Screen name or None
        """
        # Pattern: MOVE "SCREENNAME" TO SCREENNAME-...
        pattern = re.compile(
            r'MOVE\s+["\'](\w+)["\']\s+TO\s+\1-(?:NEXT-PANEL|NEXT-FLD-ID)',
            re.IGNORECASE
        )
        match = pattern.search(code)
        if match:
            return match.group(1)

        # Alternative: Look for COPY "SCREENNAME.SP2"
        pattern2 = re.compile(r'COPY\s+["\'](\w+)\.SP2["\']', re.IGNORECASE)
        match2 = pattern2.search(code)
        if match2:
            return match2.group(1)

        return None

    def extract_occurs_fields(self, code: str, sp2_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Extract OCCURS field definitions from Working Storage or SP2 file.

        Args:
            code: COBOL source code
            sp2_code: Optional SP2 file content

        Returns:
            List of field definitions with name, level, pic, occurs count
        """
        fields = []

        # Search in SP2 file first if provided
        search_code = sp2_code if sp2_code else code

        # Pattern for OCCURS structures:
        # 03  PGM-ENTRIES OCCURS 24 TIMES.
        #     05  PGM-PROGRAM          PIC X(09).
        #     05  PGM-SWITCHES         PIC X(10).

        lines = search_code.split('\n')
        in_occurs_block = False
        occurs_name = None
        occurs_count = 0
        occurs_level = 0

        for i, line in enumerate(lines):
            # Find OCCURS clause
            occurs_match = re.match(
                r'\s*(\d+)\s+(\w+[-\w]*)\s+OCCURS\s+(\d+)\s+TIMES',
                line,
                re.IGNORECASE
            )
            if occurs_match:
                occurs_level = int(occurs_match.group(1))
                occurs_name = occurs_match.group(2)
                occurs_count = int(occurs_match.group(3))
                in_occurs_block = True
                continue

            # Extract fields within OCCURS block
            if in_occurs_block:
                field_match = re.match(
                    r'\s*(\d+)\s+(\w+[-\w]*)\s+PIC\s+([\w\(\)]+)',
                    line,
                    re.IGNORECASE
                )
                if field_match:
                    field_level = int(field_match.group(1))
                    field_name = field_match.group(2)
                    pic_clause = field_match.group(3)

                    # Check if still in occurs block (higher level number)
                    if field_level > occurs_level:
                        fields.append({
                            'occurs_parent': occurs_name,
                            'occurs_count': occurs_count,
                            'field_name': field_name,
                            'level': field_level,
                            'pic_clause': pic_clause
                        })
                    else:
                        in_occurs_block = False
                elif re.match(r'\s*\d+\s+\w+', line):
                    # Different level field - end of occurs block
                    in_occurs_block = False

        return fields

    def generate_scr100_copy(self) -> str:
        """Generate COPY \"SCR100.WS\" statement."""
        return '       COPY "SCR100.WS".'

    def generate_grid_rec_structure(
        self,
        field_mappings: List[FieldMapping],
        occurs_fields: List[Dict[str, Any]]
    ) -> str:
        """
        Generate GRID-REC structure from field mappings.

        Args:
            field_mappings: User-provided field mappings (if any)
            occurs_fields: Auto-detected OCCURS fields

        Returns:
            GRID-REC structure as COBOL code
        """
        lines = ["       01  GRID-REC."]

        if field_mappings:
            # Use user-provided mappings
            for mapping in field_mappings:
                lines.append(f"           05 {mapping.grid_field:20s} PIC {mapping.pic_clause}.")
        elif occurs_fields:
            # Auto-generate from occurs fields
            for field in occurs_fields:
                grid_field_name = f"GRID-{field['field_name']}"
                lines.append(f"           05 {grid_field_name:20s} PIC {field['pic_clause']}.")
        else:
            # Placeholder if nothing detected
            lines.append("           05 GRID-FIELD-1      PIC X(10).  *TODO-SCR100: Define grid fields")

        return '\n'.join(lines)

    def generate_grid_rec_len(self) -> str:
        """Generate GRID-REC-LEN variable."""
        return "       01  GRID-REC-LEN          PIC 9(09) VALUE ZEROES."

    def generate_grid_counter(self) -> str:
        """Generate GRID-COUNTER variable."""
        return "       01  GRID-COUNTER          PIC 9(2)."

    def generate_initialize_grid_paragraph(
        self,
        screen_name: str,
        field_mappings: List[FieldMapping],
        occurs_fields: List[Dict[str, Any]]
    ) -> str:
        """
        Generate INITIALIZE-GRID paragraph.

        Args:
            screen_name: Screen name (e.g., "OES143A")
            field_mappings: Field mappings for columns
            occurs_fields: Auto-detected fields

        Returns:
            Complete INITIALIZE-GRID paragraph
        """
        # Determine column count
        num_cols = len(field_mappings) if field_mappings else len(occurs_fields) if occurs_fields else 2

        # Build header IDs
        header_ids = []
        for i, mapping in enumerate(field_mappings or [], 1):
            trans_id = mapping.translation_id or f'"Column {i}"'
            header_ids.append(f'               {trans_id} GRID-DELIM')

        if not header_ids and occurs_fields:
            for i, field in enumerate(occurs_fields, 1):
                header_ids.append(f'               "TODO-Header-{i}" GRID-DELIM  *TODO-SCR100: Set translation ID')

        if not header_ids:
            header_ids = [
                '               "TODO-Header-1" GRID-DELIM  *TODO-SCR100: Set translation IDs',
                '               "TODO-Header-2" GRID-DELIM'
            ]

        # Build column widths
        col_widths = []
        for mapping in (field_mappings or []):
            width = mapping.column_width or self._infer_width_from_pic(mapping.pic_clause)
            col_widths.append(f'               "{width}" GRID-DELIM')

        if not col_widths and occurs_fields:
            for field in occurs_fields:
                width = self._infer_width_from_pic(field['pic_clause'])
                col_widths.append(f'               "{width}" GRID-DELIM')

        if not col_widths:
            col_widths = ['               "10" GRID-DELIM  *TODO-SCR100: Set column widths']

        # Build column formats
        col_formats = []
        for mapping in (field_mappings or []):
            fmt = mapping.column_format or mapping.pic_clause
            col_formats.append(f'               "{fmt}" GRID-DELIM')

        if not col_formats and occurs_fields:
            for field in occurs_fields:
                col_formats.append(f'               "{field["pic_clause"]}" GRID-DELIM')

        if not col_formats:
            col_formats = ['               "X(10)" GRID-DELIM  *TODO-SCR100: Set column formats']

        return f"""      **************************************************
       INITIALIZE-GRID.
      **************************************************
           INITIALIZE  SCR100-LINKS
                       GRID-DELIMITED-DATA
           SET SCR100-INITIALIZE-GRID  TO TRUE
           MOVE 1                      TO SCR100-FIXED-ROWS
           MOVE 30                     TO SCR100-TOTAL-ROWS
           MOVE {num_cols}                      TO SCR100-TOTAL-COLS
           MOVE 500                    TO SCR100-HEADER-IDS-LEN
                                          SCR100-COL-WIDTHS-LEN
                                          SCR100-COL-FORMATS-LEN
                                          SCR100-ADDL-PROPERTIES-LEN
           MOVE 1 TO SCR100-HEADER-IDS-LEN
           STRING
{chr(10).join(header_ids)}
               DELIMITED BY SIZE
               INTO GRID-HEADER-IDS
               WITH POINTER SCR100-HEADER-IDS-LEN
           END-STRING
           SET SCR100-HEADER-IDS TO ADDRESS OF GRID-HEADER-IDS

           MOVE 1 TO SCR100-COL-WIDTHS-LEN
           STRING
{chr(10).join(col_widths)}
               DELIMITED BY SIZE INTO GRID-COL-WIDTHS
               WITH POINTER SCR100-COL-WIDTHS-LEN
           END-STRING
           SET SCR100-COL-WIDTHS TO ADDRESS OF GRID-COL-WIDTHS

           MOVE 1 TO SCR100-COL-FORMATS-LEN
           STRING
{chr(10).join(col_formats)}
               DELIMITED BY SIZE INTO GRID-COL-FORMATS
               WITH POINTER SCR100-COL-FORMATS-LEN
           END-STRING
           SET SCR100-COL-FORMATS TO ADDRESS OF GRID-COL-FORMATS

           STRING
               GRID-MIN-WIDTH-PROP "8500"  *TODO-SCR100: Adjust min width
               DELIMITED BY SIZE
               INTO GRID-ADDL-PROPERTIES
               WITH POINTER SCR100-ADDL-PROPERTIES-LEN
           END-STRING
           SET SCR100-ADDL-PROPERTIES TO ADDRESS OF GRID-ADDL-PROPERTIES

           PERFORM CALL-SCR100

           COMPUTE GRID-REC-LEN =
               COMPROC-ZERO + FUNCTION LENGTH(GRID-REC)
           MOVE 0                         TO SCR100-HEADER-IDS-LEN
                                             SCR100-COL-WIDTHS-LEN
                                             SCR100-COL-FORMATS-LEN
                                             SCR100-ADDL-PROPERTIES-LEN."""

    def generate_load_grid_paragraph(self) -> str:
        """Generate LOAD-GRID paragraph."""
        return """      **************************************************
       LOAD-GRID.
      **************************************************
           INITIALIZE SCR100-LINKS
           SET SCR100-CLEAR-ROWS        TO TRUE
           PERFORM CALL-SCR100
           PERFORM LOAD-GRID-ROWS
           SET SCR100-REDRAW-GRID       TO TRUE
           PERFORM CALL-SCR100."""

    def generate_load_grid_rows_paragraph(
        self,
        field_mappings: List[FieldMapping],
        occurs_fields: List[Dict[str, Any]],
        screen_name: str
    ) -> str:
        """Generate LOAD-GRID-ROWS paragraph with field mappings."""

        # Build field moves
        field_moves = []
        if field_mappings:
            for mapping in field_mappings:
                field_moves.append(
                    f"              MOVE {mapping.occurs_field}(GRID-COUNTER) TO {mapping.grid_field}"
                )
        elif occurs_fields:
            for field in occurs_fields:
                grid_field = f"GRID-{field['field_name']}"
                occurs_array = f"{field['occurs_parent']}"
                field_moves.append(
                    f"              MOVE {field['field_name']}(GRID-COUNTER) TO {grid_field}  *TODO-SCR100: Verify field reference"
                )
        else:
            field_moves = ["              *TODO-SCR100: Add field mappings here"]

        counter_name = f"{field_mappings[0].occurs_field.split('(')[0]}-COUNTER" if field_mappings else "WS-COUNTER"

        return f"""      **************************************************
       LOAD-GRID-ROWS.
      **************************************************
           INITIALIZE SCR100-LINKS
           SET SCR100-ROW-DATA          TO ADDRESS OF GRID-REC
           MOVE GRID-REC-LEN            TO SCR100-ROW-DATA-LEN
           MOVE {screen_name}-GRID-I  TO SCR100-GRID-ID
           SET SCR100-ADD-ROW           TO TRUE

           PERFORM VARYING GRID-COUNTER FROM 1 BY 1
                   UNTIL GRID-COUNTER > 24  *TODO-SCR100: Set max rows

              INITIALIZE GRID-REC
{chr(10).join(field_moves)}

              PERFORM CALL-SCR100
           END-PERFORM."""

    def generate_call_scr100_paragraph(self, screen_name: str, grid_id: Optional[int] = None) -> str:
        """Generate CALL-SCR100 paragraph with error handling."""
        grid_id_str = str(grid_id) if grid_id else "9900  *TODO-SCR100: Set unique grid ID"

        return f"""      **************************************************
       CALL-SCR100.
      **************************************************
      **  CALLS SCR100 TO PROCESS GRID
           MOVE CP-CMPNY        TO SCR100-CMPNY
           MOVE COMPROC-TRMNL   TO SCR100-TRMNL
           MOVE PROGRAM-NAME-77 TO SCR100-CALLING-PGM
           MOVE {screen_name}-GRID-I  TO SCR100-GRID-ID
           MOVE "{screen_name}"       TO SCR100-SCREEN
           CALL "GSSERP.SCR100"
                         USING SCR100-LINKS
              ON OVERFLOW
               MOVE SPACES              TO CP-WS-MSG-WORKAREA
               INITIALIZE CP-WS-MSG-WORKAREA
               MOVE 264                 TO CP-WS-MSG-NUMBER
               MOVE "SCR100"            TO CP-WS-MSG-PARAM-1
               MOVE "CSCR100"           TO CP-WS-MSG-REF
               MOVE "Grid module not found"
                                        TO CP-WS-MSG-TEXT(1)
               PERFORM COMPROC-SHOW-MESSAGE
               SET SCR100-FAILED        TO TRUE
           END-CALL."""

    def generate_get_row_data_paragraph(self) -> str:
        """Generate GET-ROW-DATA paragraph."""
        return """      **************************************************
       GET-ROW-DATA.
      **************************************************
           SET SCR100-GET-ROW-DATA     TO TRUE
           SET SCR100-ROW-DATA         TO ADDRESS OF GRID-REC
           MOVE GRID-REC-LEN           TO SCR100-ROW-DATA-LEN
           PERFORM CALL-SCR100."""

    def generate_vbx_event_handler(self, screen_name: str) -> str:
        """
        Generate VBX event handler skeleton for P1000-CONVERSE.

        Args:
            screen_name: Screen name

        Returns:
            VBX event handler code
        """
        return f"""           IF {screen_name}-KEY = SP2-KEY-VBX
              AND {screen_name}-MENU-ID = {screen_name}-GRID-I
              INITIALIZE SCR100-LINKS
              MOVE {screen_name}-MENU-OPTION TO SCR100-PROPERTY-NAME
              PERFORM WITH TEST AFTER
                 UNTIL NOT SCR100-MORE-EVENTS
                 SET SCR100-PROCESS-EVENTS TO TRUE
                 MOVE {screen_name}-MENU-ID TO SCR100-GRID-ID
                 PERFORM CALL-SCR100
                 IF SCR100-EVENT-FIELD-CHG
                    PERFORM GET-ROW-DATA
                    MOVE SCR100-SEL-ROW-START TO {screen_name}-LAST-OCCURS
                    SUBTRACT 1 FROM {screen_name}-LAST-OCCURS
                    *TODO-SCR100: Add field change validation logic here
                    IF {screen_name}-LAST-OCCURS > 0
                       IF SCR100-RET-COL = 1
                          *TODO-SCR100: Add column 1 validation
                          CONTINUE
                       END-IF
                       IF SCR100-RET-COL = 2
                          *TODO-SCR100: Add column 2 validation
                          CONTINUE
                       END-IF
                    END-IF
                 END-IF
                 IF SCR100-EVENT-SELECT
                    PERFORM GET-ROW-DATA
                    MOVE SCR100-SEL-ROW-START TO {screen_name}-LAST-OCCURS
                    SUBTRACT 1 FROM {screen_name}-LAST-OCCURS
                    *TODO-SCR100: Add row selection logic here
                 END-IF
              END-PERFORM
              GO TO P1000-EXIT  *TODO-SCR100: Adjust exit label if needed
           END-IF"""

    def generate_grid_close(self, screen_name: str) -> str:
        """Generate grid close logic."""
        return f"""           INITIALIZE SCR100-LINKS
           MOVE {screen_name}-GRID-I TO SCR100-GRID-ID
           SET SCR100-CLOSE-GRID TO TRUE
           PERFORM CALL-SCR100."""

    def generate_sp2_grid_field(self, screen_name: str, grid_id: int = 9900) -> str:
        """Generate grid field definition for SP2 file."""
        return f"       05  {screen_name}-GRID-I       PIC S9(4) COMP-5 VALUE +{grid_id}."

    def _infer_width_from_pic(self, pic_clause: str) -> int:
        """Infer column width from PIC clause."""
        # Extract number from PIC X(10) or PIC 9(5)
        match = re.search(r'\((\d+)\)', pic_clause)
        if match:
            return int(match.group(1))
        # No parentheses, assume single char
        return 1
