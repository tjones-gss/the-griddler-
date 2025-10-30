# SCR100 Grid Conversion Complete Guide

## Table of Contents
1. [Quick Start Checklist](#quick-start-checklist)
2. [Boilerplate Code Templates](#boilerplate-code-templates)
3. [Step-by-Step Conversion Process](#step-by-step-conversion-process)
4. [Common Patterns & Solutions](#common-patterns--solutions)
5. [Troubleshooting Guide](#troubleshooting-guide)

---

## Quick Start Checklist

### Pre-Conversion Analysis ✓
- [ ] Identify all REPEAT GROUP / OCCURS clauses in SP2 file
- [ ] Count number of columns in repeat group
- [ ] Note field types and sizes for each column
- [ ] Document any special formatting or validation rules
- [ ] Check for paging logic (SP2-RX-* variables)
- [ ] Identify translation IDs for column headers

### SP2 File Changes ✓
- [ ] Remove all OCCURS clause definitions
- [ ] Add grid control field: `XXX-GRID-I PIC S9(4) COMP-5 VALUE +[UNIQUE_ID]`
- [ ] Add grid hit field (optional): `XXX-GRID-HIT PIC 9(1) VALUE 0`
- [ ] Update field/color/type lengths (typically 90%+ reduction)
- [ ] Remove repeat group field definitions

### Working Storage Updates ✓
- [ ] Add `COPY "SCR100.WS"`
- [ ] Create GRID-REC structure matching repeat group fields
- [ ] Add GRID-REC-LEN variable
- [ ] Add counter variables (e.g., INO-COUNTER, VNO-COUNTER)
- [ ] Add symbol variables for currency display if needed
- [ ] Keep original OCCURS structures for compatibility (optional)

### Procedure Division Changes ✓
- [ ] Add INITIALIZE-GRID paragraph
- [ ] Add LOAD-GRID and LOAD-GRID-ROWS paragraphs
- [ ] Add CALL-SCR100 paragraph with error handling
- [ ] Replace repeat group loading with grid calls
- [ ] Add VBX key event handling
- [ ] Remove manual paging logic (P2200-GET-MORE-LINES, etc.)
- [ ] Add GET-ROW-DATA paragraph for selections
- [ ] Close grid when switching screens

### Testing Verification ✓
- [ ] Grid displays all data correctly
- [ ] Column headers appear with proper labels
- [ ] Date fields display in correct format
- [ ] Numeric fields align properly
- [ ] Currency symbols display correctly
- [ ] Row selection works
- [ ] Event handling responds to clicks/keys
- [ ] No memory leaks or performance issues

---

## Boilerplate Code Templates

### 1. Working Storage Additions

```cobol
      *================================================================
      * SCR100 Grid Support - Add after other COPY statements
      *================================================================
           COPY "SCR100.WS".
      
      *================================================================
      * Grid Record Structure - Customize fields to match your data
      *================================================================
       01  GRID-REC.
           05  GRID-[FIELD1]        PIC [datatype] VALUE [initial].
           05  GRID-[FIELD2]        PIC [datatype] VALUE [initial].
           05  GRID-[FIELD3]        PIC [datatype] VALUE [initial].
           05  GRID-[FIELD4]        PIC [datatype] VALUE [initial].
           * TODO: Add all fields from your repeat group here
           
       01  GRID-REC-LEN            PIC 9(09) VALUE ZERO.
       
      *================================================================
      * Grid Control Variables
      *================================================================
       01  WS-COUNTER              PIC S9(4) COMP-5.
       01  [PREFIX]-COUNTER        PIC 9(4) VALUE 0.
       * TODO: Add counters for each data type being displayed
       
       01  WS-USERID               PIC X(8) VALUE SPACES.
       01  [SCREEN]-SYMBOL-1       PIC X(10).
       * TODO: Add symbol variables if displaying currency
```

### 2. INITIALIZE-GRID Paragraph

```cobol
      *================================================================
       INITIALIZE-GRID.
      *================================================================
           INITIALIZE SCR100-LINKS
                      GRID-DELIMITED-DATA
                      
           SET SCR100-INITIALIZE-GRID TO TRUE
           
      *    Basic grid setup
           MOVE 1 TO SCR100-FIXED-ROWS              * Header row
           MOVE 1 TO SCR100-TOTAL-ROWS               * Start with header only
           MOVE [N] TO SCR100-TOTAL-COLS             * TODO: Set number of columns
           
      *    Set buffer sizes
           MOVE 500 TO SCR100-HEADER-IDS-LEN
                       SCR100-COL-WIDTHS-LEN
                       SCR100-COL-FORMATS-LEN
                       SCR100-ADDL-PROPERTIES-LEN
                       
      *    Build column headers with translation IDs
           STRING
      *        TODO: Replace with your translation IDs
               "[TRANS_ID_1]" GRID-DELIM    * [Column 1 Description]
               "[TRANS_ID_2]" GRID-DELIM    * [Column 2 Description]
               "[TRANS_ID_3]" GRID-DELIM    * [Column 3 Description]
      *        For currency columns with symbols:
      *        "[TRANS_ID]" X"08" " " [SCREEN]-SYMBOL-1 GRID-DELIM
               DELIMITED BY SIZE
               INTO GRID-HEADER-IDS
      *        Note: WITH POINTER is optional - both patterns work
           END-STRING
           SET SCR100-HEADER-IDS TO ADDRESS OF GRID-HEADER-IDS
           
      *    Build column widths
           STRING
      *        TODO: Set appropriate widths for each column
               "[WIDTH1]" GRID-DELIM        * e.g., "3" for 3 chars
               "[WIDTH2]" GRID-DELIM        * e.g., "15" for 15 chars
               "[WIDTH3]" GRID-DELIM        * e.g., "8" for dates
               DELIMITED BY SIZE
               INTO GRID-COL-WIDTHS
      *        Note: WITH POINTER is optional - both patterns work
           END-STRING
           SET SCR100-COL-WIDTHS TO ADDRESS OF GRID-COL-WIDTHS
           
      *    Build column formats
           STRING
      *        TODO: Set format for each column
               "[FORMAT1]" GRID-DELIM       * e.g., "9(3)" for numeric
               "[FORMAT2]" GRID-DELIM       * e.g., "X(30)" for text
               "[FORMAT3]" GRID-DELIM       * e.g., "DATE" for dates
               "[FORMAT4]" GRID-DELIM       * e.g., "S9(9)V99" for amounts
               DELIMITED BY SIZE
               INTO GRID-COL-FORMATS
      *        Note: WITH POINTER is optional - both patterns work
           END-STRING
           SET SCR100-COL-FORMATS TO ADDRESS OF GRID-COL-FORMATS
           
      *    Set additional properties (optional)
           STRING
               GRID-MIN-WIDTH-PROP "[MIN_WIDTH]"    * TODO: e.g., "8500"
      *        Add other properties as needed:
      *        GRID-DELIM "EditableColumn[N]"      * Make column N editable
               DELIMITED BY SIZE
               INTO GRID-ADDL-PROPERTIES
      *        Note: WITH POINTER is optional - both patterns work
           END-STRING
           SET SCR100-ADDL-PROPERTIES TO ADDRESS OF GRID-ADDL-PROPERTIES
           
           PERFORM CALL-SCR100
           
      *    Calculate grid record length and reset
           COMPUTE GRID-REC-LEN = FUNCTION LENGTH(GRID-REC)
           MOVE 0 TO SCR100-HEADER-IDS-LEN
                     SCR100-COL-WIDTHS-LEN
                     SCR100-COL-FORMATS-LEN
                     SCR100-ADDL-PROPERTIES-LEN
                     
      *    Optional: Set header row formatting (height, word wrap)
      *    This enables multi-line headers if needed
           MOVE 1 TO SCR100-DELIM-DATA-LEN(1)
           MOVE SPACE TO GRID-ROW-FORMAT
           STRING
               GRID-ROW-HEIGHT-PROP
               "450"                    * Height in twips (1/20th point)
               GRID-WORD-WRAP-PROP
               GRID-PROP-ON
               DELIMITED BY SIZE INTO GRID-ROW-FORMAT
               WITH POINTER SCR100-DELIM-DATA-LEN(1)
           END-STRING
           SET SCR100-SET-PROPERTY TO TRUE
           SET SCR100-DELIM-DATA(1) TO ADDRESS OF GRID-ROW-FORMAT
           
      *    Optional: Set selection properties (which rows/columns selectable)
           MOVE 1 TO SCR100-SEL-ROW-START
                     SCR100-SEL-ROW-END
           MOVE 1 TO SCR100-SEL-COL-START
           MOVE SCR100-TOTAL-COLS TO SCR100-SEL-COL-END
           PERFORM CALL-SCR100.
```

### 3. LOAD-GRID Paragraphs (Batch Loading Pattern)

**Pattern A: Batch Loading** - Use when you have all data ready before displaying

```cobol
      *================================================================
       LOAD-GRID.
      *================================================================
           INITIALIZE SCR100-LINKS
           SET SCR100-CLEAR-ROWS TO TRUE
           PERFORM CALL-SCR100
           
           PERFORM LOAD-GRID-ROWS
           
           SET SCR100-REDRAW-GRID TO TRUE
           PERFORM CALL-SCR100.
           
      *================================================================
       LOAD-GRID-ROWS.
      *================================================================
           INITIALIZE SCR100-LINKS
           SET SCR100-ROW-DATA TO ADDRESS OF GRID-REC
           MOVE GRID-REC-LEN TO SCR100-ROW-DATA-LEN
           MOVE [SCREEN]-GRID-I TO SCR100-GRID-ID    * TODO: Use your grid ID field
           SET SCR100-ADD-ROW TO TRUE
           
           PERFORM VARYING WS-COUNTER FROM 1 BY 1
                   UNTIL WS-COUNTER > [PREFIX]-COUNTER
                   
               INITIALIZE GRID-REC
               
      *        TODO: Map your data to grid fields
      *        Example mappings:
               MOVE [SOURCE-FIELD1](WS-COUNTER) TO GRID-[FIELD1]
               MOVE [SOURCE-FIELD2](WS-COUNTER) TO GRID-[FIELD2]
               
      *        For date conversion from 6 to 8 digits:
      *        MOVE [SOURCE-DATE](WS-COUNTER) TO COMPROC-MMDDYY
      *        PERFORM COMPROC-MMDDYY-TO-DATE
      *        MOVE COMPROC-DATE-NUM TO GRID-[DATE-FIELD]
               
               PERFORM CALL-SCR100
           END-PERFORM.
```

### 3A. Alternative Pattern: Inline Row Loading

**Pattern B: Inline Loading** - Use when adding rows during data processing loop

```cobol
      *================================================================
      * Clear grid before loading new data
      *================================================================
           INITIALIZE SCR100-LINKS
           SET SCR100-CLEAR-ROWS TO TRUE
           PERFORM CALL-SCR100
           
      *================================================================
      * Process data and add rows one at a time
      *================================================================
           PERFORM VARYING WS-COUNTER FROM 1 BY 1
                   UNTIL WS-COUNTER > [PREFIX]-COUNTER
                   
               * TODO: Your data processing logic here
               INITIALIZE GRID-REC
               
      *        Map data to grid fields
               MOVE [SOURCE-FIELD1](WS-COUNTER) TO GRID-[FIELD1]
               MOVE [SOURCE-FIELD2](WS-COUNTER) TO GRID-[FIELD2]
               
      *        Add this row to the grid
               PERFORM ADD-ROW-TO-GRID
           END-PERFORM
           
      *    Redraw grid after all rows are added
           SET SCR100-REDRAW-GRID TO TRUE
           PERFORM CALL-SCR100
           
      *================================================================
       ADD-ROW-TO-GRID.
      *================================================================
           INITIALIZE SCR100-LINKS
           SET SCR100-ROW-DATA TO ADDRESS OF GRID-REC
           MOVE GRID-REC-LEN TO SCR100-ROW-DATA-LEN
           SET SCR100-ADD-ROW TO TRUE
           PERFORM CALL-SCR100.
```

**When to use Pattern A vs Pattern B:**
- **Pattern A (Batch)**: Better when you have a fixed array/table to load all at once
- **Pattern B (Inline)**: Better when processing records from files/databases and adding as you process

### 4. CALL-SCR100 Paragraph

**Note**: Error handling patterns may vary by program. Both approaches shown below are valid.

```cobol
      *================================================================
       CALL-SCR100.
      *================================================================
           MOVE CP-CMPNY TO SCR100-CMPNY
           MOVE CP-TRMNL TO SCR100-TRMNL         * or TRMNL-NUMBER
           MOVE CP-USER-ID TO SCR100-USER-ID      * or WS-USERID - use your program's pattern
           MOVE PROGRAM-NAME-77 TO SCR100-CALLING-PGM
           MOVE [SCREEN]-GRID-I TO SCR100-GRID-ID    * TODO: Use your grid ID
           MOVE "[SCREEN]" TO SCR100-SCREEN          * TODO: Set screen name
           
           CALL "GSSERP.SCR100" USING SCR100-LINKS
               ON OVERFLOW
      *        Pattern 1: Using CP-WS-MSG-WORKAREA (Common)
                   MOVE SPACES TO CP-WS-MSG-WORKAREA
                   INITIALIZE CP-WS-MSG-WORKAREA
                   MOVE 264 TO CP-WS-MSG-NUMBER
                   MOVE "SCR100" TO CP-WS-MSG-PARAM-1
                   MOVE "CSCR100" TO CP-WS-MSG-REF
                   MOVE "Grid module not found" TO CP-WS-MSG-TEXT(1)
                   PERFORM COMPROC-SHOW-MESSAGE
                   SET SCR100-FAILED TO TRUE
      *        Pattern 2: Using WS-MSG-WORKAREA (Alternative)
      *            MOVE SPACES TO WS-MSG-WORKAREA
      *            INITIALIZE WS-MSG-WORKAREA
      *            MOVE 264 TO WS-MSG-NUMBER
      *            MOVE "SCR100" TO WS-MSG-PARAM-1
      *            MOVE "CALL-SCR100" TO WS-MSG-REF
      *            MOVE "Grid module not found" TO WS-MSG-TEXT(1)
      *            PERFORM DISPLAY-SP2-MESSAGE
      *            SET SCR100-FAILED TO TRUE
           END-CALL.
```

### 5. Event Handling (VBX Key Pattern)

```cobol
      *================================================================
      * Add this to your main event processing loop
      *================================================================
           IF [SCREEN]-KEY = SP2-KEY-VBX
              AND [SCREEN]-MENU-ID = [SCREEN]-GRID-I
              
              INITIALIZE SCR100-LINKS
              MOVE [SCREEN]-MENU-OPTION TO SCR100-PROPERTY-NAME
              
              PERFORM WITH TEST AFTER
                 UNTIL NOT SCR100-MORE-EVENTS
                 
                 SET SCR100-PROCESS-EVENTS TO TRUE
                 MOVE [SCREEN]-MENU-ID TO SCR100-GRID-ID
                 PERFORM CALL-SCR100
                 
                 IF SCR100-SUCCESSFUL
                    EVALUATE TRUE
                    WHEN SCR100-EVENT-DRILL
                        PERFORM GET-ROW-DATA
                        * TODO: Add your drill-down logic here
                        
                    WHEN SCR100-EVENT-SELECT
                        PERFORM GET-ROW-DATA
                        * TODO: Add your selection logic here
                        
                    WHEN SCR100-EVENT-FIELD-CHG
                        * TODO: Add field change logic if needed
                        CONTINUE
                        
                    WHEN OTHER
                        CONTINUE
                    END-EVALUATE
                 END-IF
              END-PERFORM
              
              GO TO [EXIT-PARAGRAPH]    * TODO: Set appropriate exit
           END-IF.
           
      *================================================================
       GET-ROW-DATA.
      *================================================================
           SET SCR100-GET-ROW-DATA TO TRUE
           SET SCR100-ROW-DATA TO ADDRESS OF GRID-REC
           MOVE GRID-REC-LEN TO SCR100-ROW-DATA-LEN
           PERFORM CALL-SCR100
           
           IF SCR100-SUCCESSFUL
              * TODO: Process the selected row data
              * Data is now in GRID-REC fields
              MOVE SCR100-RET-ROW TO WS-SELECTED-ROW
           END-IF.
```

### 6. Grid Cleanup

```cobol
      *================================================================
      * Add when closing screen or switching to another screen
      *================================================================
           INITIALIZE SCR100-LINKS
           MOVE [SCREEN]-GRID-I TO SCR100-GRID-ID
           SET SCR100-CLOSE-GRID TO TRUE
           PERFORM CALL-SCR100.
```

---

## Step-by-Step Conversion Process

### Phase 1: Analysis (30 minutes)
1. **Open the old program** and locate all repeat group references
2. **Document the structure**:
   ```
   Field Name | Type | Size | Format | Translation ID
   ---------|------|------|--------|---------------
   [TODO: Fill in your fields]
   ```
3. **Find paging logic** - Search for:
   - SP2-RX-BLOCK-DISP
   - SP2-RX-TOTAL-OCCS
   - SP2-RX-BLOCK-OCCS
   - PROC-GET-MORE-LINES

### Phase 2: SP2 File Updates (15 minutes)
1. **Backup the original SP2 file**
2. **Remove OCCURS definitions**
3. **Add grid fields**:
   ```cobol
   05  [SCREEN]-GRID-I PIC S9(4) COMP-5 VALUE +[UNIQUE_ID].
   ```
4. **Update lengths** (expect 90%+ reduction)

### Phase 3: Working Storage (30 minutes)
1. **Add SCR100.WS copy statement**
2. **Create GRID-REC structure**
3. **Add control variables**
4. **Calculate GRID-REC-LEN**

### Phase 4: Procedure Division (45 minutes)
1. **Add initialization after screen open**:
   ```cobol
   PERFORM INITIALIZE-GRID
   PERFORM LOAD-GRID
   ```
2. **Replace repeat group loading**
3. **Add event handling**
4. **Remove paging paragraphs**

### Phase 5: Testing (30 minutes)
1. **Compile and check for errors**
2. **Test grid display**
3. **Verify data loading**
4. **Test user interactions**
5. **Check memory usage**

---

## Common Patterns & Solutions

### Pattern 1: Date Conversion (6 to 8 digits)
```cobol
* Old format: YYMMDD
MOVE OLD-DATE-FIELD TO COMPROC-MMDDYY
PERFORM COMPROC-MMDDYY-TO-DATE
MOVE COMPROC-DATE-NUM TO GRID-DATE-FIELD  * Now YYYYMMDD
```

### Pattern 2: Currency Symbol Display
```cobol
* In header definition:
STRING
    "31300"           * Translation ID for amount
    X"08"             * Special separator
    " "               * Space
    CURRENCY-SYMBOL   * Your currency symbol variable
    GRID-DELIM
    DELIMITED BY SIZE
    INTO GRID-HEADER-IDS
    WITH POINTER SCR100-HEADER-IDS-LEN
END-STRING
```

### Pattern 3: Multiple Grids in One Program
```cobol
* Separate procedures for each grid:
PERFORM INITIALIZE-GRID-A
PERFORM INITIALIZE-GRID-B

* Separate CALL-SCR100 procedures:
CALL-SCR100-A.
    MOVE GRID-A-ID TO SCR100-GRID-ID
    MOVE "SCREENA" TO SCR100-SCREEN
    * ... rest of call

CALL-SCR100-B.
    MOVE GRID-B-ID TO SCR100-GRID-ID
    MOVE "SCREENB" TO SCR100-SCREEN
    * ... rest of call
```

### Pattern 4: Row Selection and Highlighting
```cobol
* Set selection properties during grid initialization:
MOVE 1 TO SCR100-SEL-ROW-START
          SCR100-SEL-ROW-END
MOVE 1 TO SCR100-SEL-COL-START
MOVE SCR100-TOTAL-COLS TO SCR100-SEL-COL-END
PERFORM CALL-SCR100

* Use SCR100-SEL-ROW-START/END for selection ranges
* Use grid properties for color coding individual cells
```

### Pattern 5: Editable Grid Cells
```cobol
* In INITIALIZE-GRID, add to properties:
STRING
    "EditableColumn9"    * Make column 9 editable
    DELIMITED BY SIZE
    INTO GRID-ADDL-PROPERTIES
    WITH POINTER SCR100-ADDL-PROPERTIES-LEN
END-STRING
```

---

## Troubleshooting Guide

### Issue: Grid Not Displaying
- **Check**: SCR100-GRID-ID matches SP2 field value
- **Check**: INITIALIZE-GRID called before LOAD-GRID
- **Check**: GRID-REC-LEN calculated correctly
- **Check**: Screen name in CALL-SCR100 matches actual screen

### Issue: Data Not Loading
- **Check**: SCR100-ROW-DATA points to GRID-REC
- **Check**: Counter variable incremented correctly
- **Check**: PERFORM loop range is correct
- **Check**: SCR100-ADD-ROW set before each call

### Issue: Events Not Processing
- **Check**: VBX key comparison: `IF [SCREEN]-KEY = SP2-KEY-VBX`
- **Check**: Grid ID comparison in event handler
- **Check**: SCR100-PROCESS-EVENTS loop implemented
- **Check**: MENU-ID matches GRID-I field

### Issue: Dates Display Incorrectly
- **Check**: Converting 6-digit to 8-digit format
- **Check**: Using "DATE" format in column formats
- **Check**: Date conversion routine called

### Issue: Performance Problems
- **Check**: Not calling REDRAW-GRID in loop
- **Check**: Clearing rows before reload
- **Check**: Grid closed when switching screens
- **Check**: Memory limits not exceeded

---

## Final Notes

### Critical Success Factors
1. **STRING statements**: Both `WITH POINTER` and `INTO` patterns work for grid setup. Use whichever fits your coding style.
2. **VBX key pattern is mandatory** for events
3. **Date conversion is required** (6 to 8 digits)
4. **Close grids** when switching screens
5. **Test with realistic data volumes**
6. **Choose loading pattern appropriately**: Batch loading for arrays, inline loading for file/database processing

### Common Mistakes to Avoid
- ❌ Forgetting to calculate GRID-REC-LEN
- ❌ Missing GRID-DELIM between values
- ❌ Wrong grid ID in event handling
- ❌ Not initializing SCR100-LINKS
- ❌ Keeping old paging logic
- ❌ Not calling REDRAW-GRID after adding rows (inline pattern)
- ❌ Forgetting to clear rows before reloading data

### When to Ask for Help
- Translation IDs not documented
- Complex business logic in repeat groups
- Custom formatting requirements
- Performance issues with large datasets
- Integration with other systems

---

**Document Version**: 1.1  
**Last Updated**: Updated with PUR100C.CBL implementation patterns  
**Status**: Ready for developer use with TODO placeholders  

**Version 1.1 Changes:**
- Added header row formatting section (height, word wrap)
- Added alternative inline row loading pattern (ADD-ROW-TO-GRID)
- Clarified STRING patterns (WITH POINTER is optional)
- Updated error handling to show both common patterns
- Added selection properties configuration
- Updated common mistakes and patterns 