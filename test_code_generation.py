"""
Test the new code generation converter with ORD143 samples.
"""
import sys
sys.path.insert(0, 'backend')

from app.services.converter.code_generator import SCR100CodeGenerator
from app.services.converter.cobol_converter_v2 import CobolConverterV2

# Read sample file
print("Reading ORD143 PRE sample...")
try:
    with open('samples/pre/ORD143.CBL', 'r') as f:
        pre_code = f.read()
    print(f"[OK] PRE file loaded: {len(pre_code)} chars\n")
except Exception as e:
    print(f"[ERROR] Could not load PRE file: {e}")
    sys.exit(1)

# Test 1: Screen name extraction
print("="*60)
print("TEST 1: Screen Name Extraction")
print("="*60)

generator = SCR100CodeGenerator()
screen_name = generator.extract_screen_name(pre_code)
print(f"Detected screen name: {screen_name}")
print()

# Test 2: OCCURS field extraction
print("="*60)
print("TEST 2: OCCURS Field Extraction")
print("="*60)

occurs_fields = generator.extract_occurs_fields(pre_code)
print(f"Found {len(occurs_fields)} OCCURS fields:")
for field in occurs_fields[:5]:  # Show first 5
    print(f"  - {field['field_name']:20s} PIC {field['pic_clause']:10s} (in {field['occurs_parent']} OCCURS {field['occurs_count']})")
if len(occurs_fields) > 5:
    print(f"  ... and {len(occurs_fields) - 5} more")
print()

# Test 3: Generate GRID-REC structure
print("="*60)
print("TEST 3: GRID-REC Structure Generation")
print("="*60)

grid_rec = generator.generate_grid_rec_structure([], occurs_fields)
print(grid_rec)
print()

# Test 4: Generate INITIALIZE-GRID paragraph
print("="*60)
print("TEST 4: INITIALIZE-GRID Paragraph Generation")
print("="*60)

if screen_name and occurs_fields:
    init_grid = generator.generate_initialize_grid_paragraph(
        screen_name, [], occurs_fields[:3]  # Use first 3 fields for demo
    )
    print(init_grid[:500] + "...")  # Show first 500 chars
    print()

# Test 5: Full conversion
print("="*60)
print("TEST 5: Full Conversion")
print("="*60)

converter = CobolConverterV2()
result = converter.convert(
    pre_code=pre_code,
    sp2_code=None,
    field_mappings=None,
    screen_name=None,  # Let it auto-detect
    grid_id=9900
)

print(f"Status: {result.status}")
print(f"Confidence: {result.confidence_score:.2f}")
print(f"Applied Rules: {len(result.applied_rules)}")
for rule in result.applied_rules:
    print(f"  - {rule['rule_id']}: {rule['description']}")
print(f"\nWarnings: {len(result.warnings)}")
for warning in result.warnings:
    print(f"  ! {warning}")

# Check if code was generated
if len(result.converted_code) > len(pre_code):
    added_lines = len(result.converted_code.split('\n')) - len(pre_code.split('\n'))
    print(f"\n[OK] Code generated! Added {added_lines} lines")

    # Check for key additions
    checks = {
        'COPY "SCR100.WS"': 'COPY "SCR100.WS"' in result.converted_code,
        'GRID-REC structure': 'GRID-REC.' in result.converted_code,
        'INITIALIZE-GRID': 'INITIALIZE-GRID.' in result.converted_code,
        'LOAD-GRID': 'LOAD-GRID.' in result.converted_code,
        'CALL-SCR100': 'CALL-SCR100.' in result.converted_code,
        'GET-ROW-DATA': 'GET-ROW-DATA.' in result.converted_code,
        'VBX handler': 'SP2-KEY-VBX' in result.converted_code,
    }

    print("\nGenerated Code Verification:")
    for check_name, found in checks.items():
        status = "[OK]" if found else "[MISSING]"
        print(f"  {status} {check_name}")
else:
    print("\n[ERROR] No code was generated!")

print("\n" + "="*60)
print("CODE GENERATION TEST COMPLETE")
print("="*60)
