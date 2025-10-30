"""
Quick test of the refined parser patterns against ORD143 samples.
"""
import re

# Test PRE patterns
pre_patterns = {
    "occurs_clause": r"OCCURS\s+(\d+)\s+TIMES",
    "working_storage_occurs": r"^\s*\d+\s+(\w+[-\w]*)\s+OCCURS\s+(\d+)",
    "perform_varying": r"PERFORM\s+.*VARYING\s+(\w+)\s+FROM\s+(\d+)\s+BY\s+(\d+)\s+UNTIL",
    "converse_paragraph": r"^\s*P1000-CONVERSE\.",
    "perform_converse": r"PERFORM\s+P1000-CONVERSE\s+THRU\s+P1000-EXIT",
}

# Test POST patterns
post_patterns = {
    "scr100_copy": r"COPY\s+['\"]SCR100\.WS['\"]",
    "grid_rec_definition": r"^\s*\d+\s+GRID-REC\.",
    "grid_rec_len": r"GRID-REC-LEN\s+PIC\s+9",
    "grid_field_sp2": r"(\w+-GRID-I)\s+PIC\s+S9\(4\)\s+COMP-5",
    "vbx_key_check": r"IF\s+\w+-KEY\s*=\s*SP2-KEY-VBX",
    "vbx_grid_check": r"AND\s+\w+-MENU-ID\s*=\s*\w+-GRID-I",
    "scr100_event_loop": r"UNTIL\s+NOT\s+SCR100-MORE-EVENTS",
    "scr100_process_events": r"SET\s+SCR100-PROCESS-EVENTS\s+TO\s+TRUE",
    "scr100_event_field_chg": r"IF\s+SCR100-EVENT-FIELD-CHG",
    "scr100_event_select": r"IF\s+SCR100-EVENT-SELECT",
    "initialize_grid_para": r"^\s*INITIALIZE-GRID\.",
    "load_grid_para": r"^\s*LOAD-GRID\.",
    "call_scr100_para": r"^\s*CALL-SCR100\.",
    "get_row_data_para": r"^\s*GET-ROW-DATA\.",
    "scr100_call": r"CALL\s+['\"]GSSERP\.SCR100['\"]",
}

# Read sample files
print("Reading ORD143 sample files...")
try:
    with open('samples/pre/ORD143.CBL', 'r') as f:
        pre_code = f.read()
    print(f"[OK] PRE file loaded: {len(pre_code)} chars")
except Exception as e:
    print(f"[ERROR] Could not load PRE file: {e}")
    pre_code = ""

try:
    with open('samples/post/ORD143.CBL', 'r') as f:
        post_code = f.read()
    print(f"[OK] POST file loaded: {len(post_code)} chars")
except Exception as e:
    print(f"[ERROR] Could not load POST file: {e}")
    post_code = ""

print("\n" + "="*60)
print("TESTING PRE PATTERNS")
print("="*60)

for name, pattern in pre_patterns.items():
    regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    matches = regex.findall(pre_code)
    print(f"{name:30s} : {len(matches):3d} matches")
    if matches and len(matches) <= 3:
        print(f"  Examples: {matches[:3]}")

print("\n" + "="*60)
print("TESTING POST PATTERNS")
print("="*60)

for name, pattern in post_patterns.items():
    regex = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    matches = regex.findall(post_code)
    print(f"{name:30s} : {len(matches):3d} matches")
    if matches and len(matches) <= 3:
        print(f"  Examples: {matches[:3]}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)

pre_count = sum(len(re.compile(p, re.IGNORECASE | re.MULTILINE).findall(pre_code)) for p in pre_patterns.values())
post_count = sum(len(re.compile(p, re.IGNORECASE | re.MULTILINE).findall(post_code)) for p in post_patterns.values())

print(f"Total PRE pattern matches: {pre_count}")
print(f"Total POST pattern matches: {post_count}")
print("\n[OK] Parser pattern testing complete!")
