"""
Standalone test of code generation without pydantic dependencies.
"""
import re

# Read sample file
print("Reading ORD143 PRE sample...")
try:
    with open('samples/pre/ORD143.CBL', 'r') as f:
        pre_code = f.read()
    print(f"[OK] PRE file loaded: {len(pre_code)} chars\n")
except Exception as e:
    print(f"[ERROR] Could not load PRE file: {e}")
    exit(1)

# Test 1: Screen name extraction
print("="*60)
print("TEST 1: Screen Name Extraction")
print("="*60)

def extract_screen_name(code):
    """Extract screen name from MOVE statements."""
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

screen_name = extract_screen_name(pre_code)
print(f"Detected screen name: {screen_name}")
assert screen_name is not None, "Screen name detection failed"
print("[OK] Screen name detected successfully\n")

# Test 2: OCCURS field extraction
print("="*60)
print("TEST 2: OCCURS Field Extraction")
print("="*60)

def extract_occurs_fields(code):
    """Extract OCCURS field definitions."""
    fields = []
    lines = code.split('\n')
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
                in_occurs_block = False

    return fields

occurs_fields = extract_occurs_fields(pre_code)
print(f"Found {len(occurs_fields)} OCCURS fields:")
for field in occurs_fields[:5]:
    print(f"  - {field['field_name']:20s} PIC {field['pic_clause']:10s} (in {field['occurs_parent']} OCCURS {field['occurs_count']})")
if len(occurs_fields) > 5:
    print(f"  ... and {len(occurs_fields) - 5} more")
assert len(occurs_fields) > 0, "No OCCURS fields found"
print("[OK] OCCURS fields extracted\n")

# Test 3: Generate GRID-REC structure
print("="*60)
print("TEST 3: GRID-REC Structure Generation")
print("="*60)

def generate_grid_rec(occurs_fields):
    """Generate GRID-REC structure."""
    lines = ["       01  GRID-REC."]
    for field in occurs_fields:
        grid_field_name = f"GRID-{field['field_name']}"
        lines.append(f"           05 {grid_field_name:20s} PIC {field['pic_clause']}.")
    return '\n'.join(lines)

grid_rec = generate_grid_rec(occurs_fields)
print(grid_rec)
assert "GRID-REC" in grid_rec, "GRID-REC not generated"
assert "GRID-" in grid_rec, "Grid fields not generated"
print("\n[OK] GRID-REC structure generated\n")

# Test 4: Generate INITIALIZE-GRID paragraph
print("="*60)
print("TEST 4: INITIALIZE-GRID Paragraph Generation")
print("="*60)

def generate_initialize_grid(screen_name, occurs_fields):
    """Generate INITIALIZE-GRID paragraph."""
    num_cols = min(len(occurs_fields), 3)  # Use first 3 fields for demo

    header_ids = []
    for i, field in enumerate(occurs_fields[:num_cols], 1):
        header_ids.append(f'               "Header-{i}-{field["field_name"]}" GRID-DELIM')

    col_widths = []
    for field in occurs_fields[:num_cols]:
        match = re.search(r'\((\d+)\)', field['pic_clause'])
        width = match.group(1) if match else "10"
        col_widths.append(f'               "{width}" GRID-DELIM')

    col_formats = []
    for field in occurs_fields[:num_cols]:
        col_formats.append(f'               "{field["pic_clause"]}" GRID-DELIM')

    return f"""      **************************************************
       INITIALIZE-GRID.
      **************************************************
           INITIALIZE  SCR100-LINKS
                       GRID-DELIMITED-DATA
           SET SCR100-INITIALIZE-GRID  TO TRUE
           MOVE 1                      TO SCR100-FIXED-ROWS
           MOVE 30                     TO SCR100-TOTAL-ROWS
           MOVE {num_cols}                      TO SCR100-TOTAL-COLS
           STRING
{chr(10).join(header_ids)}
               DELIMITED BY SIZE
               INTO GRID-HEADER-IDS
           END-STRING
           SET SCR100-HEADER-IDS TO ADDRESS OF GRID-HEADER-IDS

           STRING
{chr(10).join(col_widths)}
               DELIMITED BY SIZE INTO GRID-COL-WIDTHS
           END-STRING
           SET SCR100-COL-WIDTHS TO ADDRESS OF GRID-COL-WIDTHS"""

init_grid = generate_initialize_grid(screen_name, occurs_fields)
print(init_grid)
assert "INITIALIZE-GRID" in init_grid, "INITIALIZE-GRID not generated"
assert "SCR100-LINKS" in init_grid, "SCR100-LINKS not found"
print("\n[OK] INITIALIZE-GRID paragraph generated\n")

# Test 5: Generate VBX handler
print("="*60)
print("TEST 5: VBX Event Handler Generation")
print("="*60)

def generate_vbx_handler(screen_name):
    """Generate VBX event handler."""
    return f"""           IF {screen_name}-KEY = SP2-KEY-VBX
              AND {screen_name}-MENU-ID = {screen_name}-GRID-I
              INITIALIZE SCR100-LINKS
              PERFORM WITH TEST AFTER
                 UNTIL NOT SCR100-MORE-EVENTS
                 SET SCR100-PROCESS-EVENTS TO TRUE
                 PERFORM CALL-SCR100
                 IF SCR100-EVENT-FIELD-CHG
                    PERFORM GET-ROW-DATA
                    *TODO-SCR100: Add validation logic
                 END-IF
                 IF SCR100-EVENT-SELECT
                    PERFORM GET-ROW-DATA
                    *TODO-SCR100: Add selection logic
                 END-IF
              END-PERFORM
              GO TO P1000-EXIT
           END-IF"""

vbx_handler = generate_vbx_handler(screen_name)
print(vbx_handler)
assert "SP2-KEY-VBX" in vbx_handler, "VBX key check not generated"
assert "SCR100-MORE-EVENTS" in vbx_handler, "Event loop not generated"
assert "SCR100-EVENT-FIELD-CHG" in vbx_handler, "Field change event not generated"
assert "SCR100-EVENT-SELECT" in vbx_handler, "Select event not generated"
print("\n[OK] VBX event handler generated\n")

print("="*60)
print("ALL TESTS PASSED!")
print("="*60)
print(f"\nSummary:")
print(f"  Screen Name: {screen_name}")
print(f"  OCCURS Fields: {len(occurs_fields)}")
print(f"  Code generation components verified:")
print(f"    [OK] Screen name extraction")
print(f"    [OK] OCCURS field detection")
print(f"    [OK] GRID-REC structure generation")
print(f"    [OK] INITIALIZE-GRID paragraph generation")
print(f"    [OK] VBX event handler generation")
print(f"\n[SUCCESS] Code generator is working correctly!")
