       IDENTIFICATION DIVISION.
       PROGRAM-ID. CUSTGRID.
       AUTHOR. LEGACY SYSTEMS.
      *================================================================*
      * PRE CONVERSION EXAMPLE - USING REPEAT GROUPS                   *
      * This program uses traditional REPEAT GROUP logic               *
      *================================================================*

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-370.
       OBJECT-COMPUTER. IBM-370.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      * Customer Grid using REPEAT GROUP
       01  CUSTOMER-GRID-AREA.
           05  CUSTOMER-ENTRY REPEAT 15 TIMES.
               10  SP2-RX-CUST-ID       PIC X(10).
               10  SP2-RX-CUST-NAME     PIC X(30).
               10  SP2-RX-CUST-AMOUNT   PIC 9(7)V99.
               10  SP2-RX-CUST-STATUS   PIC X(1).

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

           05  CUSTOMER-DISPLAY-LINE REPEAT 15 TIMES.
               10  LINE PLUS 1 COL 01 PIC X(10)
                   FROM SP2-RX-CUST-ID.
               10  LINE SAME COL 15 PIC X(30)
                   FROM SP2-RX-CUST-NAME.
               10  LINE SAME COL 50 PIC Z,ZZZ,ZZ9.99
                   FROM SP2-RX-CUST-AMOUNT.
               10  LINE SAME COL 65 PIC X(1)
                   FROM SP2-RX-CUST-STATUS.

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

           PERFORM VARYING WS-INDEX FROM 1 BY 1
               UNTIL WS-INDEX > 15
               MOVE SPACES TO SP2-RX-CUST-ID (WS-INDEX)
               MOVE SPACES TO SP2-RX-CUST-NAME (WS-INDEX)
               MOVE ZEROS TO SP2-RX-CUST-AMOUNT (WS-INDEX)
               MOVE SPACES TO SP2-RX-CUST-STATUS (WS-INDEX)
           END-PERFORM.

       LOAD-CUSTOMER-DATA.
      * Load customer data from file
           PERFORM VARYING WS-INDEX FROM 1 BY 1
               UNTIL WS-INDEX > 15
               PERFORM READ-CUSTOMER-RECORD
               IF NOT EOF
                   ADD 1 TO WS-CUSTOMER-COUNT
                   ADD SP2-RX-CUST-AMOUNT (WS-INDEX)
                       TO WS-TOTAL-AMOUNT
               END-IF
           END-PERFORM.

       DISPLAY-GRID.
           DISPLAY CUSTOMER-SCREEN.

       PROCESS-UPDATES.
      * Process user updates to grid
           PERFORM VARYING WS-INDEX FROM 1 BY 1
               UNTIL WS-INDEX > 15
               IF SP2-RX-CUST-STATUS (WS-INDEX) = 'U'
                   PERFORM UPDATE-CUSTOMER-RECORD
               END-IF
           END-PERFORM.

       SAVE-CUSTOMER-DATA.
      * Save customer data to file
           PERFORM VARYING WS-INDEX FROM 1 BY 1
               UNTIL WS-INDEX > 15
               IF SP2-RX-CUST-ID (WS-INDEX) NOT = SPACES
                   PERFORM WRITE-CUSTOMER-RECORD
               END-IF
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
