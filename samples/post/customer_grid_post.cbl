       IDENTIFICATION DIVISION.
       PROGRAM-ID. CUSTGRID.
       AUTHOR. MODERNIZED SYSTEMS.
      *================================================================*
      * POST CONVERSION EXAMPLE - USING SCR100                         *
      * This program uses SCR100 grid logic                            *
      *================================================================*

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-370.
       OBJECT-COMPUTER. IBM-370.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Customer Grid using SCR100 structure
       01  CUSTOMER-GRID.
           05  CUSTOMER-ROW OCCURS 15 TIMES
               INDEXED BY CUST-IDX.
               10  CUST-ID-COL          PIC X(10).
               10  CUST-NAME-COL        PIC X(30).
               10  CUST-AMOUNT-COL      PIC 9(7)V99.
               10  CUST-STATUS-COL      PIC X(1).

      * SCR100 Control Structure
       01  SCR100-PARAMS.
           05  SCR100-FUNCTION          PIC X(4).
           05  SCR100-GRID-NAME         PIC X(20).
           05  SCR100-ROW-COUNT         PIC 99.
           05  SCR100-CURRENT-ROW       PIC 99.
           05  SCR100-STATUS            PIC X(2).

      * Working variables
       01  WS-INDEX                     PIC 99.
       01  WS-TOTAL-AMOUNT              PIC 9(9)V99.
       01  WS-CUSTOMER-COUNT            PIC 99.

       SCREEN SECTION.
       01  CUSTOMER-SCREEN.
           05  BLANK SCREEN.
           05  LINE 01 COL 25 VALUE "CUSTOMER GRID MAINTENANCE".
           05  LINE 03 COL 01 VALUE "ID".
           05  LINE 03 COL 15 VALUE "CUSTOMER NAME".
           05  LINE 03 COL 50 VALUE "AMOUNT".
           05  LINE 03 COL 65 VALUE "STATUS".

       PROCEDURE DIVISION.

       MAIN-LOGIC.
           PERFORM INIT-PROGRAM
           PERFORM LOAD-CUSTOMER-DATA
           PERFORM DISPLAY-GRID
           PERFORM PROCESS-UPDATES
           PERFORM SAVE-CUSTOMER-DATA
           STOP RUN.

       INIT-PROGRAM.
           MOVE ZEROS TO WS-TOTAL-AMOUNT
           MOVE ZEROS TO WS-CUSTOMER-COUNT

      * Initialize SCR100 grid
           MOVE 'INIT' TO SCR100-FUNCTION
           MOVE 'CUSTOMER-GRID' TO SCR100-GRID-NAME
           MOVE 15 TO SCR100-ROW-COUNT
           CALL 'SCR100' USING SCR100-PARAMS

           SET CUST-IDX TO 1
           PERFORM UNTIL CUST-IDX > 15
               MOVE SPACES TO CUST-ID-COL (CUST-IDX)
               MOVE SPACES TO CUST-NAME-COL (CUST-IDX)
               MOVE ZEROS TO CUST-AMOUNT-COL (CUST-IDX)
               MOVE SPACES TO CUST-STATUS-COL (CUST-IDX)
               SET CUST-IDX UP BY 1
           END-PERFORM.

       LOAD-CUSTOMER-DATA.
      * Load customer data using SCR100
           MOVE 'LOAD' TO SCR100-FUNCTION
           MOVE 1 TO SCR100-CURRENT-ROW

           SET CUST-IDX TO 1
           PERFORM UNTIL CUST-IDX > 15
               CALL 'SCR100' USING SCR100-PARAMS CUSTOMER-ROW (CUST-IDX)

               IF SCR100-STATUS = '00'
                   ADD 1 TO WS-CUSTOMER-COUNT
                   ADD CUST-AMOUNT-COL (CUST-IDX) TO WS-TOTAL-AMOUNT
               END-IF

               SET CUST-IDX UP BY 1
               ADD 1 TO SCR100-CURRENT-ROW
           END-PERFORM.

       DISPLAY-GRID.
      * Display grid using SCR100
           MOVE 'SHOW' TO SCR100-FUNCTION
           CALL 'SCR100' USING SCR100-PARAMS CUSTOMER-GRID
           DISPLAY CUSTOMER-SCREEN.

       PROCESS-UPDATES.
      * Process updates using SCR100
           MOVE 'EDIT' TO SCR100-FUNCTION

           SET CUST-IDX TO 1
           PERFORM UNTIL CUST-IDX > 15
               IF CUST-STATUS-COL (CUST-IDX) = 'U'
                   MOVE CUST-IDX TO SCR100-CURRENT-ROW
                   CALL 'SCR100' USING SCR100-PARAMS
                        CUSTOMER-ROW (CUST-IDX)
                   PERFORM UPDATE-CUSTOMER-RECORD
               END-IF
               SET CUST-IDX UP BY 1
           END-PERFORM.

       SAVE-CUSTOMER-DATA.
      * Save customer data using SCR100
           MOVE 'SAVE' TO SCR100-FUNCTION

           SET CUST-IDX TO 1
           PERFORM UNTIL CUST-IDX > 15
               IF CUST-ID-COL (CUST-IDX) NOT = SPACES
                   MOVE CUST-IDX TO SCR100-CURRENT-ROW
                   CALL 'SCR100' USING SCR100-PARAMS
                        CUSTOMER-ROW (CUST-IDX)
                   PERFORM WRITE-CUSTOMER-RECORD
               END-IF
               SET CUST-IDX UP BY 1
           END-PERFORM.

       READ-CUSTOMER-RECORD.
      * Stub for reading customer records
           CONTINUE.

       UPDATE-CUSTOMER-RECORD.
      * Stub for updating customer records
           CONTINUE.

       WRITE-CUSTOMER-RECORD.
      * Stub for writing customer records
           CONTINUE.
