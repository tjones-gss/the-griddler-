# Sample COBOL Programs

This directory contains sample COBOL programs demonstrating the transformation from REPEAT GROUPS to SCR100 grid logic.

## Directory Structure

- `pre/` - Programs using traditional REPEAT GROUP logic
- `post/` - Programs converted to use SCR100 grid logic

## Sample Programs

### Customer Grid (`customer_grid_*.cbl`)

A typical customer maintenance program that displays a grid of customer records.

**PRE Conversion Features:**
- Uses `REPEAT n TIMES` syntax for grid definition
- Field names prefixed with `SP2-RX-`
- Uses `PERFORM VARYING` loops to iterate through grid rows
- Traditional INDEXED BY with numeric subscripts

**POST Conversion Features:**
- Uses `OCCURS n TIMES INDEXED BY` with SCR100
- Field names suffixed with `-COL` (columns)
- Uses SCR100 API calls (`CALL 'SCR100'`)
- SCR100 operations: INIT, LOAD, SHOW, EDIT, SAVE
- Cleaner index management with `SET ... UP BY`

## Key Transformation Patterns

### 1. Grid Structure Definition

**PRE:**
```cobol
01  CUSTOMER-ENTRY REPEAT 15 TIMES.
    10  SP2-RX-CUST-ID      PIC X(10).
    10  SP2-RX-CUST-NAME    PIC X(30).
```

**POST:**
```cobol
01  CUSTOMER-GRID.
    05  CUSTOMER-ROW OCCURS 15 TIMES
        INDEXED BY CUST-IDX.
        10  CUST-ID-COL     PIC X(10).
        10  CUST-NAME-COL   PIC X(30).
```

### 2. Grid Initialization

**PRE:**
```cobol
PERFORM VARYING WS-INDEX FROM 1 BY 1
    UNTIL WS-INDEX > 15
    MOVE SPACES TO SP2-RX-CUST-ID (WS-INDEX)
END-PERFORM.
```

**POST:**
```cobol
MOVE 'INIT' TO SCR100-FUNCTION
MOVE 15 TO SCR100-ROW-COUNT
CALL 'SCR100' USING SCR100-PARAMS

SET CUST-IDX TO 1
PERFORM UNTIL CUST-IDX > 15
    MOVE SPACES TO CUST-ID-COL (CUST-IDX)
    SET CUST-IDX UP BY 1
END-PERFORM.
```

### 3. Grid Operations

**PRE:**
```cobol
PERFORM VARYING WS-INDEX FROM 1 BY 1
    UNTIL WS-INDEX > 15
    PERFORM READ-CUSTOMER-RECORD
END-PERFORM.
```

**POST:**
```cobol
MOVE 'LOAD' TO SCR100-FUNCTION
SET CUST-IDX TO 1
PERFORM UNTIL CUST-IDX > 15
    CALL 'SCR100' USING SCR100-PARAMS CUSTOMER-ROW (CUST-IDX)
    SET CUST-IDX UP BY 1
END-PERFORM.
```

## Using These Samples

1. **Compare**: Upload both PRE and POST versions to the Compare tab to see detected patterns
2. **Convert**: Upload the PRE version to the Convert tab to test automatic conversion
3. **Learn**: Study the differences to understand transformation patterns

## Notes

- These are simplified examples for demonstration purposes
- Real programs may have additional complexity
- The converter handles common patterns; edge cases may require manual review
