       @OPTIONS BINARY(BYTE)                                                       
000100 IDENTIFICATION DIVISION.                                                    
000200 PROGRAM-ID. ORD143 AS "GSSERP.ORD143"                             *>FUJITSU 
                         .                                               *>FUJITSU 
000300                                                                             
000310******************************************************************           
000400* TITLE - Setup Job Stream                                                   
000500* DESCRIPTION - Add and Maintain Invoice Job Stream                          
000600******************************************************************           
      ** Must Be Parsed to Fujitsu: YES                                            
      ** CallWrapper Support: YES                                                  
000600******************************************************************           
000700**          P R O G R A M   R E Q U I R E M E N T S             **           
000800**--------------------------------------------------------------**           
000900**  No - Requires SMITH Precompile                              **           
001000**  No - Has A Parallel GUI Version                             **           
001100**  No - Has A Parallel Acucobol 3.0 Version                    **           
      ** Must Be Parsed To Fujitsu: Yes                            DDP**           
      ******************************************************************           
      **      Panel Working Storage  Panel File Name                  **           
      **      Y     OES143A.SP2      ORD143.PNL                       **           
001200******************************************************************           
001300**           M A I N T E N A N C E   H I S T O R Y              **           
001400**--------------------------------------------------------------**           
001500**    DATE    ----------DESCRIPTION---------------------     BY **           
001600**  09/22/98  Corrected protect of ord151 program and        CW **           
001700**            switches.                                         **           
001800**   9/12/00  Make callable                                  BD **           
001900**   4/20/01  Needs to be tested for callable later          BD **           
001910**   4/23/01  Change ORD300GI to ORD035 for building         AM **           
001920**            the initial job stream.                           **           
001910**   9/11/03  Corrected new-window for new sp2.dll.          CW **           
      **  01/28/09  Add JB0067GI and JB0068GI to the job stream    EB **           
      **  04/20/09  RASH - panels in working storage               EW **           
000010**  12/18/09  Create default laser form IDs and Invoice     CWC **           
000020**            Job Stream, Issue 1743                            **           
      **  06/13/14  Issue 9247.  Add CallWrapper support.          EW **           
002000******************************************************************           
      ***************************************************************   FJ120702   
      **  AUTOMATED COMMENTS SECTION                                    FJ120702   
      **  AUTOMATED CHANGES WILL BE DOCUMENTED BELOW                    FJ120702   
      **  07/02/12  Prepare program for Fujitsu NetCOBOL                FJ120702   
      **                                                                FJ120702   
      **  07/10/14 MAKE CODE ANSI STANDARD TO USE NEW COMPILER           *>FUJITSU 
      **  END 0F AUT0MATED C0MMENTS SECTI0N                             FJ120702   
      **********************************************                    FJ120702   
002100                                                                             
                                                                                   
       ENVIRONMENT DIVISION.                                             *>FUJITSU 
       CONFIGURATION SECTION.                                            *>FUJITSU 
       SPECIAL-NAMES.                                                    *>FUJITSU 
           COPY "COMMONSN.CPY".                                          *>FUJITSU 
       REPOSITORY.                                                       *>DTLAYER
           COPY "Common.rep".                                            *>DTLAYER
           COPY "Support.rep".                                           *>DTLAYER
           COPY "SalesInvoicingInvoiceJobstream.rep".                    *>DTLAYER
           PROPERTY pGoGSS As "GoGSS".                                   *>DTLAYER
       INPUT-OUTPUT SECTION.                                             *>FUJITSU 
002700 FILE-CONTROL.                                                               
002800*    COPY "LINK.SL".                                              FJ120702   
003000*    SELECT TMPJOBS-FILE                                           *>FUJITSU 
003010*       ASSIGN DISK TMPJOBS-NAME                                   *>FUJITSU 
003100*       ORGANIZATION INDEXED                                       *>FUJITSU 
003200*       ACCESS DYNAMIC                                             *>FUJITSU 
003300*       RECORD KEY IS TMPJOBS-KEY                                  *>FUJITSU 
003400*       STATUS IS TMPJOBS-STATUS.                                  *>FUJITSU 
           SELECT TMPJOBS-FILE                                           *>FUJITSU 
               ASSIGN TO TMPJOBS-NAME                                    *>FUJITSU 
               ORGANIZATION IS INDEXED                                   *>FUJITSU 
               ACCESS IS DYNAMIC                                         *>FUJITSU 
               LOCK MODE IS MANUAL WITH LOCK ON MULTIPLE RECORDS         *>FUJITSU 
                                                                         *>FUJITSU 
      **  PRIMARY KEY  KEY NAME: TMPJOBS-KEY                             *>FUJITSU 
               RECORD KEY                                                *>FUJITSU 
                   TMPJOBS-KEY                                           *>FUJITSU 
                                                                         *>FUJITSU 
               STATUS IS TMPJOBS-STATUS.                                 *>FUJITSU 
TSU                                                                                
003500                                                                             
003600 DATA DIVISION.                                                              
003700 FILE SECTION.                                                               
003800*    COPY "LINK.FD".                                              FJ120702   
004000 FD  TMPJOBS-FILE                                                            
004100     LABEL RECORDS ARE STANDARD                                              
004200     DATA RECORD IS TMPJOBS-REC.                                             
004300 01  TMPJOBS-REC.                                                            
004400      05  TMPJOBS-KEY.                                                       
004500       10 TMPJOBS-ORDER            PIC 9(02).                                
004600       10 TMPJOBS-PGM              PIC X(09).                                
004700      05  TMPJOBS-SWITCHES         PIC X(10).                                
004800                                                                             
                                                                                   
                                                                                   
004900 WORKING-STORAGE SECTION.                                                    
005000                                                                             
       COPY "COMMONWS.CPY".                                              *>EW140613
       COPY "COMMONOB.WS".                                               *>DTLAYER
                                                                                   
005100 77  PROGRAM-NAME-77     PIC X(08) VALUE "ORD143".                           
       77  VERSION-77          PIC X(13) VALUE "071014.1252FU".          *>FUJITSU 
000110***************************************************************              
005600 77  INV-BATCH           PIC X(05) VALUE SPACES.                             
005700 77  OES143A-EXIT        PIC X(01) VALUE SPACES.                             
005800 77  WS-END-OF-STREAM    PIC X(09) VALUE "MENU     ".                        
005900 77  NEXTPROG            PIC X(08).                                          
006000 77  WAIT9               PIC 9     VALUE 3.                                  
006100 01  WS-BAD-JOBSTREAM    PIC X.                                              
006200     88  BAD-JOBSTREAM         VALUE "Y".                                    
006300 01  WS-WINDOW-IS-ACTIVE               PIC X.                                
006400     88  WINDOW-IS-ACTIVE                    VALUE "Y".                      
006500 01  ENV-GUI                PIC X.                                           
006600     88  ENV-IS-GUI             VALUE "A".                                   
006700 01  WS-COUNTER                  PIC 99 COMP-5.                              
006800 01  WS-SUB                      PIC 99 COMP-5.                              
006900 01  WS-MISC.                                                                
007000     05  WS-SUB-PGM          PIC S9(5)  COMP-5.                              
007100     05  WS-SUB-BLOCK        PIC S9(5)  COMP-5.                              
007200     05  WS-PGM-CNT          PIC S9(5)  COMP-5  VALUE +0.                    
007300     05  WS-LAST-PGM         PIC S9(5)  COMP-5  VALUE +0.                    
007400     05  WS-RECORD-PGM       PIC S9(5)  COMP-5.                              
007500     05  WS-SAVE-PGM         PIC S9(5)  COMP-5.                              
007600     05  WS-EXIT-PGM         PIC X.                                          
007700                                                                             
007800 01  PGM-TABLE.                                                              
007900     05  PGM-KEY OCCURS 99.                                                  
008000         10 PGM-ORDER    PIC 9(02).                                          
008100         10 PGM-NAME     PIC X(09).                                          
008200                                                                             
008300 01  PGM-BLOCK.                                                              
008400      03  PGM-ENTRIES OCCURS 24 TIMES.                                       
008500          05  PGM-PROGRAM          PIC X(09).                                
008600          05  PGM-SWITCHES         PIC X(10).                                
008700                                                                             
008800 01  PGM-BLOCK-T.                                                            
008900      03  PGM-ENTRIES-T OCCURS 24 TIMES.                                     
009000          05  PGM-PROGRAM-T        PIC X.                                    
009100          05  PGM-SWITCHES-T       PIC X.                                    
009200                                                                             
009400*************************************************************                
009500*COPY "LINK.WS".                                                  MC120702   
009700 01  TMPJB-WS-DATA.                                                *>MC120702
           05  TMPJOBS-NAME.                                                       
                                                                                   
009800         10 FILLER            PIC X(5)   VALUE "TMPJB".                      
                                                                                   
009900         10 TMPJOBS-SUFFIX    PIC X(3)   VALUE SPACES.                       
                                                                                   
               10 TMPJOBS-FILLER    PIC X(248) VALUE SPACES.                       
           05  TMPJOBS-DISP-NAME    PIC X(80)  VALUE SPACES.                       
010000     05  TMPJOBS-STATUS       PIC XX     VALUE SPACES.                       
                                                                                   
010100                                                                             
010200*************************************************************                
010210 COPY "sp2.cpy".                                                             
010220 COPY "OES143A.SP2".                                                         
010300                                                                             
010400 77 PUT-MSG-1                      PIC S9(4) COMP-5 VALUE +48.               
010500 01  MSG-BOX-1.                                                              
010600     03  MBX-RET-CODE    PIC S9(4) COMP-5.                                   
010700     03  FILLER          PIC S9(4) COMP-5 VALUE +12.                         
010800     03  FILLER          PIC S9(4) COMP-5 VALUE +2.                          
010900     03  FILLER          PIC S9(4) COMP-5 VALUE +4.                          
011000     03  FILLER          PIC S9(4) COMP-5 VALUE +42.                         
011100     03  FILLER          PIC S9(4) COMP-5 VALUE +80.                         
011200     03  FILLER          PIC S9(4) COMP-5 VALUE +80.                         
011300     03  FILLER          PIC S9(4) COMP-5 VALUE +1.                          
011400     03  MBX-2-ICON          PIC X VALUE "i".                                
011500     03  MBX-2-BTN           PIC X VALUE "o".                                
011600     03  MBX-2-CNCL          PIC X VALUE LOW-VALUE.                          
011700     03  MBX-2-RPLY          PIC X VALUE LOW-VALUE.                          
011800     03  MBX-2-TITLE         PIC X(80).                                      
011900     03  WS-MSG-TXT          PIC X(80).                                      
012000 01  ss-cmpny               pic x(3) EXTERNAL.                     *>FUJITSU 
012300                                                                             
012301 01  WS-SWITCH                     PIC X.                          *>CC091218
012302     88  SWITCH-INSTALL                  VALUE "I".                *>CC091218
012303     88  SWITCH-WALKTHRU                 VALUE "W".                *>CC091218
012304 77  WS-TBL-LOAD-FLAG    PIC X.                                    *>CC091218
       77  NUM-PARAM           PIC S9(2)  COMP-5                         *>FUJITSU 
                                               .                         *>FUJITSU 
012306 77  WS-CALLING-PGM      PIC X(08).                                *>CC091218
012307 77  WS-RETURN-CODE      PIC S9(9) COMP.                           *>CC091218
012308 77  WS-VERSION          PIC X(20).                                *>CC091218
012309***  Variables for C$ERR                                          CC091218   
012310 01  EXTENDED-STATUS-AREA.                                         *>CC091218
012311     05 EXTD-STAT.                                                 *>CC091218
012312        10  EXTD-CODE                 PIC X(02) VALUE SPACES.      *>CC091218
012313        10  EXTD-SYS                  PIC X(05) VALUE SPACES.      *>CC091218
012314     05 EXTD-TEXT                     PIC X(50) VALUE SPACES.      *>CC091218
012315     05 EXTD-TYPE                     PIC 9     VALUE 1.           *>CC091218
012316        88 COBOL-ERROR                VALUE 1.                     *>CC091218
012317        88 TRANSACTION-ERROR          VALUE 2.                     *>CC091218
012318 77  WS-FILE-NAME           PIC X(80).                             *>CC091218
012319 77  WS-MSG-TITLE           PIC X(80).                             *>CC091218
012320*** Messaging module                                              CC091218   
012321     COPY "MSG100.LK".                                             *>CC091218
012322     COPY "MSG100.WS".                                             *>CC091218

***********************************************************************  *>DTLAYER
******** Data Layer Variables                                            *>DTLAYER
       COPY "SalesInvoicingInvoiceJobstream.eop" REPLACING ==()== BY ====. *>DTLAYER
      
******** RD's used for partial plugin                                    *>DTLAYER
       COPY "INVJB.RD".                                                  *>DTLAYER
      
***********************************************************************  *>DTLAYER

                                                                                   
012323******************************************************************CC091218   
012324 LINKAGE SECTION.                                                  *>CC091218
012325******************************************************************CC091218   
012326 COPY "ORD143.LK".                                                 *>EW140613
012330******************************************************************CC091218   
                                                                                   
012331 PROCEDURE DIVISION USING ORD143-LINKS.                            *>EW140613
012332******************************************************************CC091218   
012500 DECLARATIVES.                                                     *>DTLAYER
013820 TMPJB-FILE-ERR SECTION.                                           *>CC091218
013821     USE AFTER STANDARD ERROR PROCEDURE ON TMPJOBS-FILE.           *>CC091218
013822 TMPJB-ERR.                                                        *>CC091218
013823     PERFORM GET-ERROR-STATUS.                                     *>CC091218
013824 TMPJB-ERR-EXIT.                                                   *>CC091218
013825     EXIT.                                                         *>CC091218
013900 END DECLARATIVES.                                                           
013910******************************************************************CC091218   
013911 MAIN-PROGRAM SECTION.                                             *>CC091218
013912******************************************************************CC091218   
013922                                                                             
013932******************                                                           
013942* MAINLINE LOGIC *                                                           
013952******************                                                           
014000 MAINLINE.                                                                   
014010     PERFORM INIT-PGM-VARIABLES THRU INIT-VAR-EXIT.                *>CC091218
014011     IF NUM-PARAM > 0                                              *>CC091218
014012     OR SWITCH-INSTALL                                             *>CC091218
014013        PERFORM SET-DEFAULTS                                       *>CC091218
014014     ELSE                                                          *>CC091218
014015        PERFORM PROCESS-JOB-STREAM                                 *>CC091218
014016        MOVE SP2-END-SESSION TO CP-SP2-P1                          *>FUJITSU 
              SET CP-SP2-P2 TO ADDRESS OF SP2-NULL-PARM                  *>FUJITSU 
              PERFORM COMPROC-CALL-SP2                                   *>FUJITSU 
014017     END-IF.                                                       *>CC091218
014018 MAIN-EXIT.                                                        *>CC091218
014019     IF NUM-PARAM > 0                                              *>CC091218
014020     OR SWITCH-INSTALL                                             *>CC091218
014021                                                                   *>FUJITSU 
              PERFORM COMPROC-EXIT-PROGRAM                               *>FUJITSU 
              GOBACK                                                     *>FUJITSU 
014022     ELSE                                                          *>CC091218
014023     if ss-cmpny = low-value                                       *>CC091218
014024                                                                   *>FUJITSU 
               MOVE nextprog TO CP-NEXT-PGM                              *>FUJITSU 
               PERFORM COMPROC-EXIT-PROGRAM                              *>FUJITSU 
               GOBACK                                                    *>FUJITSU 
014025         stop run                                                  *>CC091218
014026     ELSE                                                          *>CC091218
014027                                                                   *>FUJITSU 
              PERFORM COMPROC-EXIT-PROGRAM                               *>FUJITSU 
              GOBACK                                                     *>FUJITSU 
014028     end-if.                                                       *>CC091218
014038                                                                             
014048*************************                                         CC091218   
014049 INIT-PGM-VARIABLES.                                               *>CC091218
014050*************************                                         CC091218   
           MOVE 1 TO NUM-PARAM.                                          *>MC120702
FUJADD     COMPUTE COMPROC-CTR =                                         *>FUJITSU 
FUJADD         COMPROC-ZERO +                                            *>FUJITSU 
FUJADD         FUNCTION LENGTH (ORD143-LINKS)                            *>FUJITSU 
           EVALUATE TRUE                                                 *>EW140613
FUJREM*      WHEN ADDRESS OF ORD143-LINKS NOT = NULL                     *>FUJITSU 
FUJADD       WHEN ORD143-LINKS NOT = COMPROC-NULL-PARM(1 : COMPROC-CTR)  *>FUJITSU 
014061          MOVE ORD143-CMPNY       TO CP-CMPNY                      *>EW140613
014063          MOVE ORD143-SWITCH      TO WS-SWITCH                     *>EW140613
             WHEN SS-CMPNY NOT EQUAL LOW-VALUE                           *>EW140613
                MOVE SS-CMPNY           TO CP-CMPNY                      *>EW140613
             WHEN OTHER                                                  *>EW140613
                MOVE ZEROES             TO NUM-PARAM                     *>MC120702
                SET COMPROC-GET-LINKER TO TRUE                           *>MC120702
                                                                                   
           END-EVALUATE                                                  *>EW140613
                                                                                   
           MOVE VERSION-77 TO CP-PGM-VERSION                             *>EW140613
           PERFORM COMPROC-START-PROGRAM
           SET Company OF cCommonUtilities TO CP-CMPNY                   *>DTLAYER
           SET CODB TO Database OF cCommonUtilities                      *>DTLAYER
           SET COIntDBInd TO ConnectionIndex OF cCommonUtilities         *>DTLAYER
           MOVE 2 TO EOInvJobstreamIntMode.                           *>DTLAYER
           MOVE CP-CALLER TO WS-CALLING-PGM                              *>EW140613
           IF NUM-PARAM = 0                                              *>EW140613
      **?? How to set WS-SWITCH from linker - not in comproc            EW140613   
      *       MOVE SW-I TO WS-SWITCH                                    CC091218   
                                                                                   
              MOVE CP-NEXT-PGM TO NEXTPROG                               *>EW140613
              IF NEXTPROG = "MENU"                                       *>EW140613
                 MOVE "MENUB" TO NEXTPROG                                *>EW140613
              END-IF                                                     *>EW140613
           END-IF.                                                       *>EW140613
                                                                                   
014054     STRING PROGRAM-NAME-77 DELIMITED BY SPACE                     *>CC091218
014055            '-'             DELIMITED BY SIZE                      *>CC091218
014056            VERSION-77(1:11) DELIMITED BY SIZE                     *>CC091218
014057                   INTO WS-VERSION.                                *>CC091218
           MOVE "INFGUI"                                                 *>FUJITSU 
             TO COMPROC-PARM-NAME                                        *>FUJITSU 
           PERFORM COMPROC-GET-ENV-VAR                                   *>FUJITSU 
           MOVE COMPROC-PARM-VALUE                                       *>FUJITSU 
             TO ENV-GUI                                                  *>FUJITSU 
                                                   .                     *>FUJITSU 
                                                                                   
           SET CP-FILE-NAME-PTR TO ADDRESS OF TMPJB-WS-DATA              *>MC120702
           SET CP-SHARED-TEMP-FILE TO TRUE                               *>MC120702
           PERFORM COMPROC-GEN-TEMP-FILE-NAMES.                          *>MC120702
014068 INIT-VAR-EXIT.                                                    *>CC091218
014069     EXIT.                                                         *>CC091218
014079                                                                             
018911**************************                                        CC091218   
018912 SET-DEFAULTS.                                                     *>CC091218
018913**************************                                        CC091218   
018914*    DELETE FILE TMPJOBS-FILE.                                    CC091218   
           PERFORM EIOInvJobstreamNew                                    *>DTLAYER
018916     OPEN OUTPUT TMPJOBS-FILE.                                     *>CC091218
018917     PERFORM P0500-READ-JOBS THRU P0500-EXIT.                      *>CC091218
018918     MOVE WS-COUNTER TO WS-PGM-CNT.                                *>CC091218
           PERFORM EIOInvJobstreamDispose                                *>DTLAYER
018919     CLOSE                                                         *>DTLAYER
018920           TMPJOBS-FILE.                                           *>CC091218
018921     OPEN I-O TMPJOBS-FILE.                                        *>CC091218
018922     IF WS-TBL-LOAD-FLAG NOT = 'Y'                                 *>CC091218
018923        PERFORM P2000-LOAD-JOBS THRU P2000-EXIT.                   *>CC091218
           
           
           SET COOAArgs TO NULL
           MOVE 4 TO EOInvJobstreamsIntMode
           PERFORM EIOInvJobstreamsLoad
           
           PERFORM VARYING EOInvJobstreamOb THRU EOInvJobstreamsOb
               PERFORM EIOInvJobstreamDelete
           END-PERFORM 
           
           PERFORM EIOInvJobstreamNew.                                   *>DTLAYER
           
           MOVE LOW-VALUES TO INVJB-NEXT

018926     PERFORM VARYING WS-SUB FROM 1 BY 1                            *>CC091218
018927       UNTIL WS-SUB > WS-PGM-CNT                                   *>CC091218
018928          OR INVJB-NEXT = WS-END-OF-STREAM                         *>CC091218
018929        MOVE PGM-ORDER(WS-SUB)    TO TMPJOBS-ORDER                 *>CC091218
018930        MOVE PGM-NAME(WS-SUB)     TO TMPJOBS-PGM                   *>CC091218
018931        READ TMPJOBS-FILE                                          *>CC091218
018932        INVALID                                                    *>CC091218
018933           CONTINUE                                                *>CC091218
018934        NOT INVALID                                                *>CC091218
018935           INITIALIZE INVJB-REC                                    *>CC091218
018936           MOVE CP-CMPNY             TO INVJB-CMPNY                *>FJ120702
018937           MOVE PGM-NAME(WS-SUB)     TO INVJB-PGM                  *>CC091218
018938           MOVE PGM-NAME(WS-SUB + 1) TO INVJB-NEXT                 *>CC091218
018939           MOVE TMPJOBS-SWITCHES     TO INVJB-SWITCHES             *>CC091218
                 PERFORM RecordToInvJobstream                            *>DTLAYER
                 PERFORM EIOInvJobstreamInsert                           *>DTLAYER
018944        END-READ                                                   *>CC091218
018945     END-PERFORM.                                                  *>CC091218
018946     CLOSE TMPJOBS-FILE.                                           *>CC091218
           PERFORM EIOInvJobstreamDispose.                               *>DTLAYER
018948*    DELETE FILE TMPJOBS-FILE.                                    CC091218   
018949                                                                             
018950**************************                                                   
018951 PROCESS-JOB-STREAM.                                               *>CC091218
018952**************************                                                   
018962                                                                             
           PERFORM EIOInvJobstreamNew                                    *>DTLAYER
           CALL "GSSERP.GSDELETE"                                        *>FUJITSU 
                           USING TMPJOBS-NAME                            *>FUJITSU 
                                   .                                     *>FUJITSU 
019200     OPEN OUTPUT TMPJOBS-FILE.                                               
019300     PERFORM P0500-READ-JOBS THRU P0500-EXIT.                                
           PERFORM EIOInvJobstreamDispose                                *>DTLAYER
019400     CLOSE                                                         *>DTLAYER
019500           TMPJOBS-FILE.                                                     
019600     OPEN I-O TMPJOBS-FILE.                                                  
019700     MOVE SPACES TO PGM-BLOCK                                                
019800                    WS-EXIT-PGM.                                             
019900     MOVE ZEROES TO WS-PGM-CNT                                               
020000                    WS-LAST-PGM                                              
020100                    WS-RECORD-PGM                                            
020200                    WS-SAVE-PGM.                                             
020300     MOVE WS-COUNTER TO WS-PGM-CNT.                                          
020700     MOVE LOW-VALUES TO SP2-WD-DATA.                                         
020800     MOVE "OES143A"  TO SP2-WD-PANEL-NAME.                                   
           MOVE SP2-SET-RECORD TO CP-SP2-P1                              *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF OES143A-PANEL-RECORD              *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                            .         *>FUJITSU 
020900     MOVE SP2-OPEN-WINDOW TO CP-SP2-P1                             *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-WINDOW-DEF                    *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                       .              *>FUJITSU 
021000     MOVE LOW-VALUES TO SP2-RX-DATA.                                         
021100     MOVE 1          TO SP2-RX-ID.                                           
021200     MOVE 1          TO SP2-RX-BLOCK-SW.                                     
021300     MOVE 0          TO SP2-RX-BLOCK-DISP.                                   
021400     MOVE 24         TO SP2-RX-BLOCK-OCCS.                                   
021500     MOVE 1          TO SP2-RX-TOTAL-SW.                                     
021600     MOVE WS-COUNTER TO SP2-RX-TOTAL-OCCS.                                   
021700     SET SP2-RX-FIELD-PTR TO ADDRESS OF PGM-BLOCK.                           
021800     SET SP2-RX-TYPE-PTR  TO ADDRESS OF PGM-BLOCK-T.                         
021900     IF WS-COUNTER > ZEROES                                                  
022000         PERFORM P1200-PROC-GET-BLOCK THRU P1200-EXIT.                       
022100     MOVE SP2-SET-REPEAT-EXT TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-REPEAT-EXT                    *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                                .     *>FUJITSU 
022200     MOVE SP2-DISPLAY-WINDOW TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-NULL-PARM                     *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                               .      *>FUJITSU 
022300     MOVE LOW-VALUES   TO OES143A-DATA.                                      
022400     MOVE SP2-KEY-MORE TO OES143A-KEY.                                       
022500     MOVE "OES143A"    TO OES143A-NEXT-PANEL.                                
022700     MOVE LOW-VALUES   TO OES143A-FIELDS                                     
022800                          OES143A-COLRS                                      
022900                          OES143A-TYPES.                                     
023000     MOVE WS-VERSION   TO OES143A-VERSION-77.                      *>CC091218
023100     MOVE "N" TO OES143A-EXIT.                                               
023200     MOVE "N" TO WS-WINDOW-IS-ACTIVE.                                        
023300     PERFORM P1000-CONVERSE THRU P1000-EXIT                                  
023400         UNTIL OES143A-KEY = SP2-KEY-ESCAPE                                  
023500         OR    OES143A-KEY = SP2-KEY-CLOSE                                   
023600         OR    OES143A-EXIT = "Y".                                           
023700     PERFORM PROC-CLOSE-WINDOW THRU PROC-CLOSE-WINDOW-EXIT.                  
023900     MOVE SP2-END-SESSION TO CP-SP2-P1                             *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-NULL-PARM                     *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                      .               *>FUJITSU 
024000                                                                             
024100     if ss-cmpny = low-value                                                 
024200                                                                   *>FUJITSU 
               MOVE nextprog TO CP-NEXT-PGM                              *>FUJITSU 
               PERFORM COMPROC-EXIT-PROGRAM                              *>FUJITSU 
               GOBACK                                                    *>FUJITSU 
024300         stop run                                                            
024400     end-if                                                                  
024500                                                                   *>FUJITSU 
           PERFORM COMPROC-EXIT-PROGRAM                                  *>FUJITSU 
           GOBACK                                                        *>FUJITSU 
024600     .                                                                       
024700                                                                             
024800 P0500-READ-JOBS.                                                            
024900     MOVE ZEROES     TO WS-COUNTER.                                          
025000     MOVE SPACES      TO INVJB-KEY.                                          
025100     MOVE CP-CMPNY    TO INVJB-CMPNY.                              *>FJ120702
025200     MOVE "ORD151   " TO INVJB-PGM.                                          
           PERFORM KeysToInvJobstream                                    *>DTLAYER
           PERFORM EIOInvJobstreamLoad                                   *>DTLAYER
           PERFORM InvJobstreamToRecord                                  *>DTLAYER
           IF EOInvJobstreamOb::"ObjectStatus"() NOT = Successful OF cObjectStatusCodes *>DTLAYER
025500         MOVE ZEROES     TO WS-COUNTER                                       
025600         PERFORM P0550-LOAD-INITIAL THRU P0550-EXIT                          
025700         GO TO P0500-EXIT
           END-IF.                                                       *>DTLAYER
025800 P0500-LOOP.                                                                 
025900     ADD 1 TO WS-COUNTER.                                                    
026000     MOVE WS-COUNTER     TO TMPJOBS-ORDER.                                   
026100     MOVE INVJB-PGM      TO TMPJOBS-PGM.                                     
026200     MOVE INVJB-SWITCHES TO TMPJOBS-SWITCHES.                                
026300     WRITE TMPJOBS-REC                                                       
026400       INVALID                                                               
026500         PERFORM DO-NOTHING                                                  
026600       NOT INVALID                                                           
026700         MOVE TMPJOBS-ORDER TO PGM-ORDER(WS-COUNTER)                         
026800         MOVE TMPJOBS-PGM   TO PGM-NAME(WS-COUNTER).                         
026900     IF INVJB-NEXT = "MENU"                                                  
027000         ADD 1 TO WS-COUNTER                                                 
027100         MOVE WS-COUNTER TO TMPJOBS-ORDER                                    
027200         MOVE INVJB-NEXT TO TMPJOBS-PGM                                      
027300         WRITE TMPJOBS-REC                                                   
027400           INVALID                                                           
027500             PERFORM DO-NOTHING                                              
027600           NOT INVALID                                                       
027700             MOVE TMPJOBS-ORDER TO PGM-ORDER(WS-COUNTER)                     
027800             MOVE TMPJOBS-PGM   TO PGM-NAME(WS-COUNTER)                      
027900         END-WRITE                                                           
028000         GO TO P0500-EXIT.                                                   
028100     MOVE CP-CMPNY     TO INVJB-CMPNY.                             *>FJ120702
028200     MOVE INVJB-NEXT   TO INVJB-PGM.                                         
           PERFORM KeysToInvJobstream                                    *>DTLAYER
           PERFORM EIOInvJobstreamLoad                                   *>DTLAYER
           PERFORM InvJobstreamToRecord                                  *>DTLAYER
           IF EOInvJobstreamOb::"ObjectStatus"() NOT = Successful OF cObjectStatusCodes *>DTLAYER
028500         GO TO P0500-EXIT
           END-IF.                                                       *>DTLAYER
028600     GO TO P0500-LOOP.                                                       
028700 P0500-EXIT.                                                                 
028800     EXIT.                                                                   
028900                                                                             
029000 P0550-LOAD-INITIAL.                                                         
029100     ADD 1 TO WS-COUNTER.                                                    
029200     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
029300     MOVE "ORD151   " TO TMPJOBS-PGM.                                        
029400     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
029500     WRITE TMPJOBS-REC                                                       
029600       INVALID                                                               
029700         PERFORM DO-NOTHING.                                                 
029800     ADD 1 TO WS-COUNTER.                                                    
029900     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
030000     MOVE "ORD140GI " TO TMPJOBS-PGM.                                        
030100     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
030200     WRITE TMPJOBS-REC                                                       
030300       INVALID                                                               
030400         PERFORM DO-NOTHING.                                                 
030500     ADD 1 TO WS-COUNTER.                                                    
030600     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
030700     MOVE "ORD130GI " TO TMPJOBS-PGM.                                        
030800     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
030900     WRITE TMPJOBS-REC                                                       
031000       INVALID                                                               
031100         PERFORM DO-NOTHING.                                                 
031200     ADD 1 TO WS-COUNTER.                                                    
031300     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
031400     MOVE "ORD500GI "  TO TMPJOBS-PGM.                                       
031500     MOVE "D        "  TO TMPJOBS-SWITCHES.                                  
031600     WRITE TMPJOBS-REC                                                       
031700       INVALID                                                               
031800         PERFORM DO-NOTHING.                                                 
031900     ADD 1 TO WS-COUNTER.                                                    
032000     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
032100     MOVE "AR0060GI " TO TMPJOBS-PGM.                                        
032200     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
032300     WRITE TMPJOBS-REC                                                       
032400       INVALID                                                               
032500         PERFORM DO-NOTHING.                                                 
032600     ADD 1 TO WS-COUNTER.                                                    
032000     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                           *>EB090128
032100     MOVE "JB0067GI " TO TMPJOBS-PGM.                              *>EB090128
032200     MOVE SPACES      TO TMPJOBS-SWITCHES.                         *>EB090128
032300     WRITE TMPJOBS-REC                                             *>EB090128
032400       INVALID                                                     *>EB090128
032500         PERFORM DO-NOTHING.                                       *>EB090128
032600     ADD 1 TO WS-COUNTER.                                          *>EB090128
032000     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                           *>EB090128
032100     MOVE "JB0068GI " TO TMPJOBS-PGM.                              *>EB090128
032200     MOVE SPACES      TO TMPJOBS-SWITCHES.                         *>EB090128
032300     WRITE TMPJOBS-REC                                             *>EB090128
032400       INVALID                                                     *>EB090128
032500         PERFORM DO-NOTHING.                                       *>EB090128
032600     ADD 1 TO WS-COUNTER.                                          *>EB090128
032700     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
032800     MOVE "ORD035   " TO TMPJOBS-PGM.                                        
032810*    MOVE "ORD300GI " TO TMPJOBS-PGM.                                        
032900     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
033000     WRITE TMPJOBS-REC                                                       
033100       INVALID                                                               
033200         PERFORM DO-NOTHING.                                                 
033300     ADD 1 TO WS-COUNTER.                                                    
033400     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
033500     MOVE "ORD135GI " TO TMPJOBS-PGM.                                        
033600     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
033700     WRITE TMPJOBS-REC                                                       
033800       INVALID                                                               
033900         PERFORM DO-NOTHING.                                                 
034000     ADD 1 TO WS-COUNTER.                                                    
034100     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
034200     MOVE "OEPS41GI " TO TMPJOBS-PGM.                                        
034300     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
034400     WRITE TMPJOBS-REC                                                       
034500       INVALID                                                               
034600         PERFORM DO-NOTHING.                                                 
034700     ADD 1 TO WS-COUNTER.                                                    
034800     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
034900     MOVE "OEPS42GI " TO TMPJOBS-PGM.                                        
035000     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
035100     WRITE TMPJOBS-REC                                                       
035200       INVALID                                                               
035300         PERFORM DO-NOTHING.                                                 
035400     ADD 1 TO WS-COUNTER.                                                    
035500     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
035600     MOVE "ORD142GI " TO TMPJOBS-PGM.                                        
035700     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
035800     WRITE TMPJOBS-REC                                                       
035900       INVALID                                                               
036000         PERFORM DO-NOTHING.                                                 
036100     ADD 1 TO WS-COUNTER.                                                    
036200     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
036300     MOVE "ORD081GI " TO TMPJOBS-PGM.                                        
036400     MOVE SPACES      TO TMPJOBS-SWITCHES.                                   
036500     WRITE TMPJOBS-REC                                                       
036600       INVALID                                                               
036700         PERFORM DO-NOTHING.                                                 
036800     ADD 1 TO WS-COUNTER.                                                    
036900     MOVE WS-COUNTER   TO TMPJOBS-ORDER.                                     
037000     MOVE "MENU     " TO TMPJOBS-PGM.                                        
037100     WRITE TMPJOBS-REC                                                       
037200       INVALID                                                               
037300         PERFORM DO-NOTHING.                                                 
037400     CLOSE TMPJOBS-FILE.                                                     
037500     OPEN I-O TMPJOBS-FILE.                                                  
037600     PERFORM P2000-LOAD-JOBS THRU P2000-EXIT.                                
037700 P0550-EXIT.                                                                 
037800     EXIT.                                                                   
037900                                                                             
038000 P1000-CONVERSE.                                                             
038100     PERFORM PROC-CON-OES143A.                                               
038200     MOVE "o" TO OES143A-MOUSE-SW.                                           
038300*    PERFORM P1300-PROTECT-ORD151 THRU P1300-EXIT.                CW980922   
038400     IF OES143A-KEY = SP2-KEY-ESCAPE                                         
038500         GO TO P1000-EXIT.                                                   
038600     IF OES143A-KEY = SP2-KEY-ALT-F1                                         
038700         MOVE 1 TO WS-SUB                                                    
038800         MOVE "N" TO WS-BAD-JOBSTREAM                                        
038900         IF PGM-NAME(WS-SUB) = WS-END-OF-STREAM                              
039000             MOVE "Y" TO WS-BAD-JOBSTREAM                                    
039100         END-IF                                                              
039200         PERFORM UNTIL PGM-NAME(WS-SUB) =                                    
039300                        WS-END-OF-STREAM   OR                                
039400                        BAD-JOBSTREAM      OR                                
039500                        WS-SUB > WS-COUNTER                                  
039600             IF PGM-NAME(WS-SUB) = SPACES OR                                 
039700                PGM-NAME(WS-SUB) = LOW-VALUES OR                             
039800                PGM-NAME(WS-SUB) = ">"                                       
039900                 MOVE "Y" TO WS-BAD-JOBSTREAM                                
040000                 MOVE 1   TO WS-SUB                                          
040100             END-IF                                                          
040200             ADD 1 TO WS-SUB                                                 
040300         END-PERFORM                                                         
040400         IF BAD-JOBSTREAM OR WS-SUB > 99                                     
040500             PERFORM P3100-BAD-JOBSTREAM-MSG                                 
040600         ELSE                                                                
040700             PERFORM P4000-DELETE-EXISTING-RECS THRU P4000-EXIT              
                   PERFORM EIOInvJobstreamDispose                        *>DTLAYER
040900         END-IF                                                              
041000         GO TO P1000-EXIT.                                                   
041100     IF OES143A-KEY = SP2-KEY-ALT-F2                                         
041200         PERFORM P1400-INSERT-BEFORE THRU P1400-EXIT                         
041300         GO TO P1000-EXIT.                                                   
041400     IF OES143A-KEY = SP2-KEY-ALT-F3                                         
041500         PERFORM P1600-INSERT-AFTER THRU P1600-EXIT                          
041600         GO TO P1000-EXIT.                                                   
041700     IF OES143A-KEY = SP2-KEY-ALT-F4 AND                                     
041800        OES143A-PROGRAM(OES143A-LAST-OCCURS) NOT =                           
041900                           WS-END-OF-STREAM                                  
042000         PERFORM P1700-DELETE THRU P1700-EXIT                                
042100         GO TO P1000-EXIT.                                                   
042200     IF OES143A-KEY = SP2-KEY-MORE                                           
042300         PERFORM P1100-MORE-LINES                                            
042400         GO TO P1000-EXIT.                                                   
042500     IF OES143A-LAST-FLD-ID = OES143A-PROGRAM-I AND                          
042600        OES143A-KEY         = SP2-KEY-CTRL-FIELD                   *>CW980922
042700         PERFORM P1500-CHK-PROGRAM THRU P1500-EXIT.                          
042800     IF OES143A-LAST-FLD-ID = OES143A-SWITCHES-I AND               *>CW980922
042900        OES143A-KEY         = SP2-KEY-CTRL-FIELD                   *>CW980922
043000         PERFORM P1550-CHK-SWITCHES THRU P1550-EXIT.               *>CW980922
043100 P1000-EXIT.                                                                 
043200     EXIT.                                                                   
043300                                                                             
043400 P1100-MORE-LINES.                                                           
043500     IF SP2-RX-TOTAL-OCCS = ZEROES                                           
043600         EXIT PARAGRAPH.                                                     
043700     MOVE OES143A-NEXT-VERT TO SP2-RX-BLOCK-DISP.                            
043800     IF OES143A-NEXT-VERT LESS THAN SP2-CD-LAST-VERT                         
043900         SUBTRACT 11 FROM SP2-RX-BLOCK-DISP                                  
044000         IF SP2-RX-BLOCK-DISP LESS THAN 0                                    
044100             MOVE 0 TO SP2-RX-BLOCK-DISP.                                    
044200     PERFORM P1200-PROC-GET-BLOCK      THRU  P1200-EXIT.                     
044300     MOVE SP2-SET-REPEAT-EXT TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-REPEAT-EXT                    *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                           .          *>FUJITSU 
044400     MOVE 0 TO SP2-RX-DISP-SW.                                               
044500                                                                             
044600 P1200-PROC-GET-BLOCK.                                                       
044700     MOVE SPACES TO PGM-BLOCK.                                               
044800     COMPUTE WS-RECORD-PGM =                                       *>FUJITSU 
               COMPROC-ZERO +      SP2-RX-BLOCK-DISP + 1.                *>FUJITSU 
044900     MOVE 1 TO WS-SUB-PGM.                                                   
045000     PERFORM P1210-GET-PGM-RECORD THRU P1210-EXIT                            
045100       UNTIL WS-SUB-PGM GREATER THAN SP2-RX-BLOCK-OCCS.                      
045200 P1200-EXIT.                                                                 
045300     EXIT.                                                                   
045400 P1210-GET-PGM-RECORD.                                                       
045500     IF WS-RECORD-PGM NOT = WS-LAST-PGM + 1                                  
045600         PERFORM P1220-POSITION-PGM-FILE THRU P1220-EXIT.                    
045700     IF WS-EXIT-PGM NOT = "Y"                                                
045800         PERFORM P1240-READ-PGM-FILE THRU P1240-EXIT.                        
045900     IF WS-EXIT-PGM = "Y"                                                    
046000         IF WS-SUB-PGM = 1                                                   
046100             MOVE 0 TO WS-SUB-PGM                                            
046200             MOVE WS-PGM-CNT TO WS-RECORD-PGM                                
046300             COMPUTE SP2-RX-BLOCK-DISP =                           *>FUJITSU 
                       COMPROC-ZERO +          WS-RECORD-PGM - 1         *>FUJITSU 
046400             MOVE 1 TO SP2-RX-DISP-SW                                        
046500             MOVE SP2-RX-BLOCK-DISP TO SP2-RX-NEW-DISP                       
046600         ELSE                                                                
046700             MOVE SP2-RX-BLOCK-OCCS TO WS-SUB-PGM.                           
046800     ADD 1 TO WS-SUB-PGM.                                                    
046900 P1210-EXIT.                                                                 
047000     EXIT.                                                                   
047100                                                                             
047200 P1220-POSITION-PGM-FILE.                                                    
047300     MOVE SPACE TO WS-EXIT-PGM.                                              
047400                                                                             
047500     IF WS-RECORD-PGM GREATER THAN WS-PGM-CNT                                
047600         MOVE WS-RECORD-PGM TO WS-SAVE-PGM                                   
047700         MOVE WS-PGM-CNT    TO WS-RECORD-PGM                                 
047800         PERFORM P1230-START-PGM-FILE THRU P1230-EXIT                        
047900         PERFORM P1240-READ-PGM-FILE  THRU P1240-EXIT                        
048000             UNTIL WS-PGM-CNT = WS-SAVE-PGM                                  
048100               OR WS-EXIT-PGM = "Y"                                          
048200         MOVE WS-SAVE-PGM TO WS-RECORD-PGM.                                  
048300     IF WS-EXIT-PGM NOT = "Y"                                                
048400         PERFORM P1230-START-PGM-FILE THRU P1230-EXIT.                       
048500 P1220-EXIT.                                                                 
048600     EXIT.                                                                   
048700                                                                             
048800 P1230-START-PGM-FILE.                                                       
048900     MOVE PGM-KEY(WS-RECORD-PGM) TO TMPJOBS-KEY.                             
049000 P1230-EXIT.                                                                 
049100     EXIT.                                                                   
049200                                                                             
049300 P1240-READ-PGM-FILE.                                                        
049400     PERFORM P1250-READ-NEXT-PGM-RECORD THRU P1250-EXIT.                     
049500     IF WS-EXIT-PGM NOT = "Y"                                                
049600     AND WS-RECORD-PGM GREATER THAN WS-PGM-CNT                               
049700         MOVE WS-RECORD-PGM TO WS-PGM-CNT.                                   
049800     IF WS-EXIT-PGM = "Y"                                                    
049900         GO TO P1240-EXIT.                                                   
050000     MOVE WS-RECORD-PGM TO WS-LAST-PGM.                                      
050100     ADD 1 TO WS-RECORD-PGM.                                                 
050200 P1240-EXIT.                                                                 
050300     EXIT.                                                                   
050400                                                                             
050500 P1250-READ-NEXT-PGM-RECORD.                                                 
050600     MOVE SPACE TO WS-EXIT-PGM.                                              
050700     IF WS-RECORD-PGM > SP2-RX-TOTAL-OCCS                                    
050800         MOVE "Y" TO WS-EXIT-PGM                                             
050900         GO TO P1250-EXIT.                                                   
051000     MOVE PGM-KEY(WS-RECORD-PGM) TO TMPJOBS-KEY.                             
051100     READ TMPJOBS-FILE                                                       
051200       INVALID KEY                                                           
051300         MOVE "Y" TO WS-EXIT-PGM                                             
051400         GO TO P1250-EXIT.                                                   
051500     MOVE TMPJOBS-PGM         TO PGM-PROGRAM(WS-SUB-PGM).                    
051600     MOVE TMPJOBS-SWITCHES    TO PGM-SWITCHES(WS-SUB-PGM).                   
051700     IF TMPJOBS-PGM = "ORD151  "                                   *>CW980922
051800         MOVE SP2-GREYED-OUT  TO PGM-PROGRAM-T(WS-SUB-PGM)         *>CW980922
051900                                 PGM-SWITCHES-T(WS-SUB-PGM).       *>CW980922
052000 P1250-EXIT.                                                                 
052100     EXIT.                                                                   
052200                                                                             
052300*P1300-PROTECT-ORD151.                                                       
052400*    MOVE 1 TO WS-SUB.                                                       
052500*P1300-LOOP.                                                                 
052600*    IF PGM-PROGRAM(WS-SUB) = "ORD151   "                                    
052700*        MOVE "o" TO PGM-PROGRAM-T(WS-SUB)                                   
052800*    ELSE                                                                    
052900*        MOVE "i" TO PGM-PROGRAM-T(WS-SUB).                                  
053000*    ADD 1 TO WS-SUB.                                                        
053100*    IF WS-SUB > 24                                                          
053200*        GO TO P1300-EXIT.                                                   
053300*    GO TO P1300-LOOP.                                                       
053400*P1300-EXIT.                                                                 
053500*    EXIT.                                                                   
053600                                                                             
053700 P1400-INSERT-BEFORE.                                                        
053800     MOVE OES143A-LAST-OCCURS TO WS-SUB-PGM.                       *>MC120702
      *    SET WS-SUB-PGM        TO OES143A-LAST-OCCURS.                MC120702   
053900     COMPUTE WS-SUB-BLOCK  =                                       *>FUJITSU 
               COMPROC-ZERO +       OES143A-LAST-OCCURS -                *>FUJITSU 
054000                              SP2-RX-BLOCK-DISP.                             
054100     MOVE PGM-KEY(WS-SUB-PGM) TO TMPJOBS-KEY.                                
054200     READ TMPJOBS-FILE                                                       
054300       INVALID KEY                                                           
054400         GO TO P1400-EXIT.                                                   
054500                                                                             
054600     IF WS-COUNTER = 99                                                      
054700         PERFORM P3000-NO-MORE-ROOM-MSG                                      
054800     ELSE                                                                    
054900         MOVE WS-COUNTER TO WS-SUB                                           
055000         PERFORM UNTIL WS-SUB < OES143A-LAST-OCCURS                          
055100             MOVE PGM-KEY(WS-SUB) TO TMPJOBS-KEY                             
055200             READ TMPJOBS-FILE                                               
055300               INVALID                                                       
055400                 STRING "Can't Insert Line. " DELIMITED BY SIZE              
055500                     INTO WS-MSG-TXT                                         
055600                 END-STRING                                                  
055700                 MOVE "Invalid Read"   TO MBX-2-TITLE                        
055800                 MOVE "o" TO MBX-2-BTN                                       
055900                 MOVE PUT-MSG-1 TO CP-SP2-P1                       *>FUJITSU 
                       SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1             *>FUJITSU 
                       PERFORM COMPROC-CALL-SP2                          *>FUJITSU 
                                                                         *>FUJITSU 
056100               NOT INVALID                                                   
056200                 DELETE TMPJOBS-FILE RECORD                                  
056300                   INVALID                                                   
056400                    STRING "Can't Insert Line. " DELIMITED BY SIZE           
056500                        INTO WS-MSG-TXT                                      
056600                    END-STRING                                               
056700                    MOVE "Invalid Delete"  TO MBX-2-TITLE                    
056800                    MOVE "o" TO MBX-2-BTN                                    
056900                    MOVE PUT-MSG-1 TO CP-SP2-P1                    *>FUJITSU 
                          SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1          *>FUJITSU 
                          PERFORM COMPROC-CALL-SP2                       *>FUJITSU 
                                                                         *>FUJITSU 
057100                   NOT INVALID                                               
057200                     ADD 1 TO TMPJOBS-ORDER                                  
057300                     WRITE TMPJOBS-REC                                       
057400                       INVALID                                               
057500                    STRING "Can't Insert Line. " DELIMITED BY SIZE           
057600                        INTO WS-MSG-TXT                                      
057700                    END-STRING                                               
057800                    MOVE "Invalid Write"   TO MBX-2-TITLE                    
057900                    MOVE "o" TO MBX-2-BTN                                    
058000                    MOVE PUT-MSG-1 TO CP-SP2-P1                    *>FUJITSU 
                          SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1          *>FUJITSU 
                          PERFORM COMPROC-CALL-SP2                       *>FUJITSU 
                                                                         *>FUJITSU 
058200                       NOT INVALID                                           
058300                       MOVE TMPJOBS-KEY TO PGM-KEY(TMPJOBS-ORDER)            
058400                     END-WRITE                                               
058500                 END-DELETE                                                  
058600             END-READ                                                        
058700             SUBTRACT 1 FROM WS-SUB                                          
058800         END-PERFORM                                                         
058900         MOVE ">" TO TMPJOBS-PGM                                             
059000         MOVE OES143A-LAST-OCCURS TO TMPJOBS-ORDER                           
059100         WRITE TMPJOBS-REC                                                   
059200           INVALID                                                           
059300             STRING "Can't Insert Line. " DELIMITED BY SIZE                  
059400                INTO WS-MSG-TXT                                              
059500             END-STRING                                                      
059600             MOVE "Invalid Write"   TO MBX-2-TITLE                           
059700             MOVE "o" TO MBX-2-BTN                                           
059800             MOVE PUT-MSG-1 TO CP-SP2-P1                           *>FUJITSU 
                   SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                 *>FUJITSU 
                   PERFORM COMPROC-CALL-SP2                              *>FUJITSU 
                                                                         *>FUJITSU 
060000           NOT INVALID                                                       
060100             MOVE TMPJOBS-KEY TO PGM-KEY(TMPJOBS-ORDER)                      
060200         END-WRITE.                                                          
060300     PERFORM P2000-LOAD-JOBS THRU P2000-EXIT.                                
060400     MOVE WS-COUNTER TO SP2-RX-TOTAL-OCCS.                                   
060500     MOVE 1 TO SP2-RX-TOTAL-SW.                                              
060600     PERFORM P1200-PROC-GET-BLOCK THRU P1200-EXIT.                           
060700     MOVE SP2-SET-REPEAT-EXT TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-REPEAT-EXT                    *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                          .           *>FUJITSU 
060800     MOVE 0 TO SP2-RX-DISP-SW.                                               
060900     MOVE WS-SUB-BLOCK TO OES143A-NEXT-FLD-ID.                               
061000 P1400-EXIT.                                                                 
061100     EXIT.                                                                   
061200                                                                             
061300 P1500-CHK-PROGRAM.                                                          
061400     MOVE OES143A-LAST-OCCURS TO WS-SUB-PGM.                       *>MC120702
      *    SET WS-SUB-PGM        TO OES143A-LAST-OCCURS.                MC120702   
061500     COMPUTE WS-SUB-BLOCK  =                                       *>FUJITSU 
               COMPROC-ZERO +       OES143A-LAST-OCCURS -                *>FUJITSU 
061600                              SP2-RX-BLOCK-DISP.                             
061700     MOVE PGM-KEY(WS-SUB-PGM) TO TMPJOBS-KEY.                                
061800     READ TMPJOBS-FILE                                                       
061900       INVALID KEY                                                           
062000         STRING "Can't Modify Program. " DELIMITED BY SIZE                   
062100             INTO WS-MSG-TXT                                                 
062200         END-STRING                                                          
062300         MOVE "Invalid Read"   TO MBX-2-TITLE                                
062400         MOVE "o" TO MBX-2-BTN                                               
062500         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
062600         GO TO P1500-EXIT.                                                   
062700                                                                             
062800     DELETE TMPJOBS-FILE RECORD                                              
062900       INVALID                                                               
063000         STRING "Can't Insert Program. " DELIMITED BY SIZE                   
063100            INTO WS-MSG-TXT                                                  
063200         END-STRING                                                          
063300         MOVE "Invalid Delete"  TO MBX-2-TITLE                               
063400         MOVE "o" TO MBX-2-BTN                                               
063500         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
063600         GO TO P1500-EXIT.                                                   
063700     MOVE PGM-PROGRAM(WS-SUB-BLOCK)  TO TMPJOBS-PGM.                         
063800     MOVE PGM-SWITCHES(WS-SUB-BLOCK) TO TMPJOBS-SWITCHES.                    
063900     WRITE TMPJOBS-REC                                                       
064000       INVALID                                                               
064100         STRING "Can't Insert Program " DELIMITED BY SIZE                    
064200            INTO WS-MSG-TXT                                                  
064300         END-STRING                                                          
064400         MOVE "Invalid Write"   TO MBX-2-TITLE                               
064500         MOVE "o" TO MBX-2-BTN                                               
064600         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
064700         GO TO P1500-EXIT.                                                   
064800     MOVE TMPJOBS-KEY TO PGM-KEY(TMPJOBS-ORDER).                             
064900 P1500-EXIT.                                                                 
065000     EXIT.                                                                   
065100                                                                             
065200 P1550-CHK-SWITCHES.                                               *>CW980922
065300     MOVE OES143A-LAST-OCCURS TO WS-SUB-PGM.                       *>MC120702
      *    SET WS-SUB-PGM        TO OES143A-LAST-OCCURS.                MC120702   
065400     COMPUTE WS-SUB-BLOCK  =                                       *>FUJITSU 
               COMPROC-ZERO +       OES143A-LAST-OCCURS -                *>FUJITSU 
065500                              SP2-RX-BLOCK-DISP.                   *>CW980922
065600     MOVE PGM-KEY(WS-SUB-PGM) TO TMPJOBS-KEY.                      *>CW980922
065700     READ TMPJOBS-FILE                                             *>CW980922
065800       INVALID KEY                                                 *>CW980922
065900         STRING "Can't Modify Switches." DELIMITED BY SIZE         *>CW980922
066000             INTO WS-MSG-TXT                                       *>CW980922
066100         END-STRING                                                *>CW980922
066200         MOVE "Invalid Read"   TO MBX-2-TITLE                      *>CW980922
066300         MOVE "o" TO MBX-2-BTN                                     *>CW980922
066400         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
066500         GO TO P1550-EXIT.                                         *>CW980922
066600                                                                             
066700     MOVE PGM-SWITCHES(WS-SUB-BLOCK) TO TMPJOBS-SWITCHES.          *>CW980922
066800     REWRITE TMPJOBS-REC                                           *>CW980922
066900       INVALID                                                     *>CW980922
067000         STRING "Can't Update Switches." DELIMITED BY SIZE         *>CW980922
067100            INTO WS-MSG-TXT                                        *>CW980922
067200         END-STRING                                                *>CW980922
067300         MOVE "Invalid Rewrite" TO MBX-2-TITLE                     *>CW980922
067400         MOVE "o" TO MBX-2-BTN                                     *>CW980922
067500         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
067600         GO TO P1550-EXIT.                                         *>CW980922
067700 P1550-EXIT.                                                       *>CW980922
067800     EXIT.                                                                   
067900                                                                             
068000 P1600-INSERT-AFTER.                                                         
068100     MOVE OES143A-LAST-OCCURS TO WS-SUB-PGM.                       *>MC120702
      *    SET WS-SUB-PGM        TO OES143A-LAST-OCCURS.                MC120702   
068200     COMPUTE WS-SUB-BLOCK  =                                       *>FUJITSU 
               COMPROC-ZERO +       OES143A-LAST-OCCURS -                *>FUJITSU 
068300                              SP2-RX-BLOCK-DISP.                             
068400     MOVE PGM-KEY(WS-SUB-PGM) TO TMPJOBS-KEY.                                
068500     READ TMPJOBS-FILE                                                       
068600       INVALID KEY                                                           
068700         GO TO P1600-EXIT.                                                   
068800                                                                             
068900     IF TMPJOBS-PGM = WS-END-OF-STREAM                                       
069000         STRING "Can't Insert Prgm after MENU" DELIMITED BY SIZE             
069100             INTO WS-MSG-TXT                                                 
069200         END-STRING                                                          
069300         MOVE "Invalid Insert"   TO MBX-2-TITLE                              
069400         MOVE "o" TO MBX-2-BTN                                               
069500         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
069600         GO TO P1600-EXIT.                                                   
069700                                                                             
069800     IF WS-COUNTER = 99                                                      
069900         PERFORM P3000-NO-MORE-ROOM-MSG                                      
070000     ELSE                                                                    
070100         MOVE WS-COUNTER TO WS-SUB                                           
070200         PERFORM UNTIL WS-SUB = OES143A-LAST-OCCURS                          
070300             MOVE PGM-KEY(WS-SUB) TO TMPJOBS-KEY                             
070400             READ TMPJOBS-FILE                                               
070500               INVALID                                                       
070600                 STRING "Can't Insert Line. " DELIMITED BY SIZE              
070700                     INTO WS-MSG-TXT                                         
070800                 END-STRING                                                  
070900                 MOVE "Invalid Read"   TO MBX-2-TITLE                        
071000                 MOVE "o" TO MBX-2-BTN                                       
071100                 MOVE PUT-MSG-1 TO CP-SP2-P1                       *>FUJITSU 
                       SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1             *>FUJITSU 
                       PERFORM COMPROC-CALL-SP2                          *>FUJITSU 
                                                                         *>FUJITSU 
071300               NOT INVALID                                                   
071400                 DELETE TMPJOBS-FILE RECORD                                  
071500                   INVALID                                                   
071600                    STRING "Can't Insert Line. " DELIMITED BY SIZE           
071700                        INTO WS-MSG-TXT                                      
071800                    END-STRING                                               
071900                    MOVE "Invalid Delete"  TO MBX-2-TITLE                    
072000                    MOVE "o" TO MBX-2-BTN                                    
072100                    MOVE PUT-MSG-1 TO CP-SP2-P1                    *>FUJITSU 
                          SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1          *>FUJITSU 
                          PERFORM COMPROC-CALL-SP2                       *>FUJITSU 
                                                                         *>FUJITSU 
072300                   NOT INVALID                                               
072400                     ADD 1 TO TMPJOBS-ORDER                                  
072500                     WRITE TMPJOBS-REC                                       
072600                       INVALID                                               
072700                    STRING "Can't Insert Line. " DELIMITED BY SIZE           
072800                        INTO WS-MSG-TXT                                      
072900                    END-STRING                                               
073000                    MOVE "Invalid Write"   TO MBX-2-TITLE                    
073100                    MOVE "o" TO MBX-2-BTN                                    
073200                    MOVE PUT-MSG-1 TO CP-SP2-P1                    *>FUJITSU 
                          SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1          *>FUJITSU 
                          PERFORM COMPROC-CALL-SP2                       *>FUJITSU 
                                                                         *>FUJITSU 
073400                       NOT INVALID                                           
073500                       MOVE TMPJOBS-KEY TO PGM-KEY(TMPJOBS-ORDER)            
073600                     END-WRITE                                               
073700                 END-DELETE                                                  
073800             END-READ                                                        
073900             SUBTRACT 1 FROM WS-SUB                                          
074000         END-PERFORM                                                         
074100         MOVE ">" TO TMPJOBS-PGM                                             
074200         ADD 1 TO WS-SUB GIVING TMPJOBS-ORDER                                
074300         WRITE TMPJOBS-REC                                                   
074400           INVALID                                                           
074500             STRING "Can't Insert Line. " DELIMITED BY SIZE                  
074600                INTO WS-MSG-TXT                                              
074700             END-STRING                                                      
074800             MOVE "Invalid Write"   TO MBX-2-TITLE                           
074900             MOVE "o" TO MBX-2-BTN                                           
075000             MOVE PUT-MSG-1 TO CP-SP2-P1                           *>FUJITSU 
                   SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                 *>FUJITSU 
                   PERFORM COMPROC-CALL-SP2                              *>FUJITSU 
                                                                         *>FUJITSU 
075200           NOT INVALID                                                       
075300             MOVE TMPJOBS-KEY TO PGM-KEY(TMPJOBS-ORDER)                      
075400         END-WRITE.                                                          
075500     PERFORM P2000-LOAD-JOBS THRU P2000-EXIT.                                
075600     MOVE WS-COUNTER TO SP2-RX-TOTAL-OCCS.                                   
075700     MOVE 1 TO SP2-RX-TOTAL-SW.                                              
075800     PERFORM P1200-PROC-GET-BLOCK THRU P1200-EXIT.                           
075900     MOVE SP2-SET-REPEAT-EXT TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-REPEAT-EXT                    *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                          .           *>FUJITSU 
076000     MOVE 0 TO SP2-RX-DISP-SW.                                               
076100     ADD 1 TO WS-SUB-BLOCK.                                                  
076200     MOVE WS-SUB-BLOCK TO OES143A-NEXT-FLD-ID.                               
076300 P1600-EXIT.                                                                 
076400     EXIT.                                                                   
076500                                                                             
076600 P1700-DELETE.                                                               
076700     MOVE OES143A-LAST-OCCURS TO WS-SUB-PGM.                       *>MC120702
      *    SET WS-SUB-PGM        TO OES143A-LAST-OCCURS.                MC120702   
076800     MOVE PGM-KEY(WS-SUB-PGM) TO TMPJOBS-KEY.                                
076900     READ TMPJOBS-FILE                                                       
077000       INVALID KEY                                                           
077100         STRING "Can't Delete Program" DELIMITED BY SIZE                     
077200             INTO WS-MSG-TXT                                                 
077300         END-STRING                                                          
077400         MOVE "Invalid Read"   TO MBX-2-TITLE                                
077500         MOVE "o" TO MBX-2-BTN                                               
077600         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
077700         GO TO P1700-EXIT.                                                   
077800                                                                             
077900     IF TMPJOBS-PGM = WS-END-OF-STREAM                                       
078000         STRING "Can't Delete MENU" DELIMITED BY SIZE                        
078100             INTO WS-MSG-TXT                                                 
078200         END-STRING                                                          
078300         MOVE "Use Insert Above to Add Programs"   TO MBX-2-TITLE            
078400         MOVE "o" TO MBX-2-BTN                                               
078500         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
078600         GO TO P1700-EXIT.                                                   
078700                                                                             
078800     DELETE TMPJOBS-FILE RECORD                                              
078900       INVALID                                                               
079000        STRING "Can't Delete Progam." DELIMITED BY SIZE                      
079100            INTO WS-MSG-TXT                                                  
079200        END-STRING                                                           
079300        MOVE "Invalid Delete"  TO MBX-2-TITLE                                
079400        MOVE "o" TO MBX-2-BTN                                                
079500        MOVE PUT-MSG-1 TO CP-SP2-P1                                *>FUJITSU 
              SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                      *>FUJITSU 
              PERFORM COMPROC-CALL-SP2             .                     *>FUJITSU 
079600     PERFORM P2000-LOAD-JOBS THRU P2000-EXIT.                                
079700     MOVE WS-COUNTER TO SP2-RX-TOTAL-OCCS.                                   
079800     MOVE 1 TO SP2-RX-TOTAL-SW.                                              
079900     PERFORM P1200-PROC-GET-BLOCK THRU P1200-EXIT.                           
080000     MOVE SP2-SET-REPEAT-EXT TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-REPEAT-EXT                    *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                          .           *>FUJITSU 
080100     MOVE 0 TO SP2-RX-DISP-SW.                                               
080200     MOVE OES143A-PROGRAM-I TO OES143A-NEXT-FLD-ID.                          
080300 P1700-EXIT.                                                                 
080400     EXIT.                                                                   
080500                                                                             
080600 P2000-LOAD-JOBS.                                                            
080610     MOVE 'N' TO WS-TBL-LOAD-FLAG.                                 *>CC091218
080700     INITIALIZE PGM-TABLE.                                                   
080800     MOVE ZEROES     TO WS-COUNTER.                                          
080900     MOVE SPACES      TO TMPJOBS-KEY.                                        
081000     MOVE 1           TO TMPJOBS-ORDER.                                      
081100     MOVE "ORD151   " TO TMPJOBS-PGM.                                        
081200     READ TMPJOBS-FILE                                                       
081300       INVALID                                                               
081400         GO TO P2000-EXIT.                                                   
081500 P2000-LOOP.                                                                 
081510     MOVE 'Y' TO WS-TBL-LOAD-FLAG.                                 *>CC091218
081600     ADD 1 TO WS-COUNTER.                                                    
081700     MOVE TMPJOBS-ORDER TO PGM-ORDER(WS-COUNTER)                             
081800     MOVE TMPJOBS-PGM   TO PGM-NAME(WS-COUNTER).                             
081900     IF TMPJOBS-PGM = WS-END-OF-STREAM                                       
082000         GO TO P2000-EXIT.                                                   
082100     READ TMPJOBS-FILE NEXT RECORD                                           
082200       AT END                                                                
082300         GO TO P2000-EXIT.                                                   
082400     GO TO P2000-LOOP.                                                       
082500 P2000-EXIT.                                                                 
082600     EXIT.                                                                   
082700                                                                             
082800 P3000-NO-MORE-ROOM-MSG.                                                     
082900     MOVE                                                                    
083000      "No more room to add to jobstream!!"                                   
083100      TO WS-MSG-TXT.                                                         
083200     MOVE "Invoice Job Stream"   TO MBX-2-TITLE.                             
083300     MOVE "o" TO MBX-2-BTN.                                                  
083400     MOVE PUT-MSG-1 TO CP-SP2-P1                                   *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                         *>FUJITSU 
           PERFORM COMPROC-CALL-SP2             .                        *>FUJITSU 
083500                                                                             
083600 P3100-BAD-JOBSTREAM-MSG.                                                    
083700     MOVE                                                                    
083800      "You have formed an invalid Jobstrean - Please fix"                    
083900      TO WS-MSG-TXT.                                                         
084000     MOVE "Invoice Job Stream Error"    TO MBX-2-TITLE.                      
084100     MOVE "o" TO MBX-2-BTN.                                                  
084200     MOVE PUT-MSG-1 TO CP-SP2-P1                                   *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                         *>FUJITSU 
           PERFORM COMPROC-CALL-SP2             .                        *>FUJITSU 
084300                                                                             
084400 P4000-DELETE-EXISTING-RECS.                                                 
           SET COOAArgs TO NULL 
           MOVE 4 TO EOInvJobstreamsIntMode
           PERFORM EIOInvJobstreamsLoad
           
           PERFORM VARYING EOInvJobstreamOb THRU EOInvJobstreamsOb
               PERFORM EIOInvJobstreamDelete
           END-PERFORM 
           
084700     MOVE 1 TO  WS-SUB.                                                      
084800 P4000-LOOP.                                                                 
084900     MOVE CP-CMPNY    TO INVJB-CMPNY.                              *>FJ120702
085000     MOVE PGM-NAME(WS-SUB) TO INVJB-PGM.                                     
085100     MOVE PGM-NAME(WS-SUB + 1) TO INVJB-NEXT.                                
085200     MOVE PGM-ORDER(WS-SUB) TO TMPJOBS-ORDER.                      *>CW980922
085300     MOVE PGM-NAME(WS-SUB)  TO TMPJOBS-PGM.                                  
085400     READ TMPJOBS-FILE                                                       
085500       INVALID                                                               
085600         STRING "Switch Field was not Read" DELIMITED BY SIZE                
085700             INTO WS-MSG-TXT                                                 
085800         END-STRING                                                          
085900         MOVE "Invalid Read - TMPJOBS"  TO MBX-2-TITLE                       
086000         MOVE "o" TO MBX-2-BTN                                               
086100         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
                                                                         *>FUJITSU 
086300       NOT INVALID                                                           
086400         MOVE TMPJOBS-SWITCHES TO INVJB-SWITCHES.                            
           PERFORM RecordToInvJobstream                                  *>DTLAYER
           PERFORM EIOInvJobstreamInsert                                 *>DTLAYER
           IF EOInvJobstreamOb::"ObjectStatus"() NOT = Successful OF cObjectStatusCodes *>DTLAYER
086700         STRING "Invalid Write of Jobstream. " DELIMITED BY SIZE             
086800                "Please Re-enter"              DELIMITED BY SIZE             
086900             INTO WS-MSG-TXT                                                 
087000         END-STRING                                                          
087100         MOVE "Invalid Write"   TO MBX-2-TITLE                               
087200         MOVE "o" TO MBX-2-BTN                                               
087300         MOVE PUT-MSG-1 TO CP-SP2-P1                               *>FUJITSU 
               SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                     *>FUJITSU 
               PERFORM COMPROC-CALL-SP2                                  *>FUJITSU 
087400         GO TO P4000-EXIT
           END-IF.                                                       *>DTLAYER
087600     IF INVJB-NEXT = WS-END-OF-STREAM                                        
087700         MOVE "Y" TO OES143A-EXIT                                            
087800         GO TO P4000-EXIT.                                                   
087900     ADD 1 TO WS-SUB.                                                        
088000     GO TO P4000-LOOP.                                                       
088100 P4000-EXIT.                                                                 
088200     EXIT.                                                                   
088300                                                                             
090200 PROC-CON-OES143A.                                                           
090300******************                                                           
090400* CONVERSE PANEL *                                                           
090500******************                                                           
090600     MOVE SP2-CONVERSE-PANEL TO CP-SP2-P1                          *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF OES143A-CONVERSE-DATA             *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                                 .    *>FUJITSU 
090700     MOVE LOW-VALUE TO OES143A-NEW-WINDOW.                                   
090800     MOVE "Y"       TO WS-WINDOW-IS-ACTIVE.                                  
090900                                                                             
091000 PROC-CON-OES143A-EXIT.                                                      
091100     EXIT.                                                                   
091200                                                                             
091300 PROC-CLOSE-WINDOW.                                                          
091400************************                                                     
091500* CLOSE CURRENT WINDOW *                                                     
091600************************                                                     
091700     MOVE SP2-CLOSE-WINDOW TO CP-SP2-P1                            *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF SP2-NULL-PARM                     *>FUJITSU 
           PERFORM COMPROC-CALL-SP2                       .              *>FUJITSU 
091800 PROC-CLOSE-WINDOW-EXIT.                                                     
091900     EXIT.                                                                   
092000                                                                             
092100 DO-NOTHING.                                                                 
092200     EXIT.                                                                   
092210************************                                                     
092224 GET-ERROR-STATUS.                                                 *>CC091218
092225************************                                                     
           PERFORM COMPROC-GET-ERROR-DETAIL                              *>FUJITSU 
           MOVE COMPROC-ED-DISPLAY-NAME                                  *>FUJITSU 
             TO WS-FILE-NAME                                             *>FUJITSU 
                                               .                         *>FUJITSU 
092230     SET COBOL-ERROR TO TRUE.                                      *>CC091218
           PERFORM COMPROC-GET-ERROR-DETAIL                              *>FUJITSU 
           MOVE COMPROC-ED-STATUS                                        *>FUJITSU 
             TO EXTD-STAT(1:2)                                           *>FUJITSU 
           MOVE COMPROC-ED-EXTD-STATUS(12:)                              *>FUJITSU 
             TO EXTD-STAT(3:)                                            *>FUJITSU 
           MOVE COMPROC-ED-MSG                                           *>FUJITSU 
             TO EXTD-TEXT                                                *>FUJITSU 
                                                              .          *>FUJITSU 
092250     IF EXTD-CODE NOT = "10"                                       *>CC091218
092260        INITIALIZE WS-MSG-WORKAREA                                 *>CC091218
092270        MOVE 361  TO WS-MSG-NUMBER                                 *>CC091218
092280        MOVE "INPUT-ERROR       " TO WS-MSG-REF                    *>CC091218
092290        MOVE WS-FILE-NAME         TO WS-MSG-PARAM-1                *>CC091218
092300        MOVE EXTD-STAT            TO WS-MSG-PARAM-2                *>CC091218
092310        STRING "File Error on "   DELIMITED BY SIZE                *>CC091218
092320               WS-FILE-NAME       DELIMITED BY SPACE               *>CC091218
092330               "; STS="           DELIMITED BY SIZE                *>CC091218
092340               EXTD-CODE DELIMITED BY SIZE                         *>CC091218
092350               ','       DELIMITED BY SIZE                         *>CC091218
092360               EXTD-SYS  DELIMITED BY SIZE                         *>CC091218
092370               ' '       DELIMITED BY SIZE                         *>CC091218
092380               EXTD-TEXT DELIMITED BY SIZE                         *>CC091218
092390          INTO WS-MSG-TEXT(1)                                      *>CC091218
092400        END-STRING                                                 *>CC091218
092410        MOVE WS-FILE-NAME TO WS-MSG-FILE-NAME                      *>CC091218
092420        MOVE EXTD-STAT    TO WS-MSG-FILE-STATUS                    *>CC091218
092430        PERFORM CALL-BUSINESS-MSG                                  *>CC091218
092440     END-IF.                                                       *>CC091218
092450                                                                   *>CC091218
092460*********************************                                 CC091218   
092470 CALL-BUSINESS-MSG.                                                *>CC091218
092480*********************************                                 CC091218   
092490     MOVE SPACE TO WS-MSG-REPLY.                                   *>CC091218
092500     COPY "BMSGMOVE.PR"                                            *>CC091218
092510          REPLACING =='CMPNY'==   BY ==CP-CMPNY   ==               *>FJ120702
092520                    =='PROGRAM'== BY ==PROGRAM-NAME-77==           *>CC091218
092530                    =='VERSION'== BY ==VERSION-77(1:11)==.         *>CC091218
092540                                                                   *>CC091218
092550     COPY "BMSGCALL.PR".                                           *>CC091218
092560     IF MSG100-SUCCESSFUL                                          *>CC091218
092570        MOVE MSG100-RESPONSE TO WS-MSG-REPLY.                      *>CC091218
092580 MSG-EXIT.                                                         *>CC091218
092590     EXIT.                                                         *>CC091218
092600                                                                             
092610 IN-ERR-DISP.                                                                
092620     MOVE "o" TO MBX-2-BTN.                                                  
092630     MOVE PUT-MSG-1 TO CP-SP2-P1                                   *>FUJITSU 
           SET CP-SP2-P2 TO ADDRESS OF MSG-BOX-1                         *>FUJITSU 
           PERFORM COMPROC-CALL-SP2             .                        *>FUJITSU 
092640     IF WINDOW-IS-ACTIVE                                                     
092650       PERFORM PROC-CLOSE-WINDOW THRU PROC-CLOSE-WINDOW-EXIT                 
092660     END-IF.                                                                 
092670                                                                   *>FUJITSU 
           PERFORM COMPROC-EXIT-PROGRAM                                  *>FUJITSU 
           GOBACK      .                                                 *>FUJITSU 
092680                                                                             
      *************************************************************                
       COPY "COMPROC.CPY".                                               *>EW140613
       RecordToInvJobstream.                                             *>DTLAYER
           PERFORM KeysToInvJobstream                                    *>DTLAYER
                                                                         *>DTLAYER
           SET ShortName OF Information OF ProgramCD OF pNext OF EOInvJobstreamOb TO INVJB-NEXT 
           SET ProgramSwitch OF Information OF EOInvJobstreamOb TO INVJB-SWITCHES. 

       KeysToInvJobstream.                                               *>DTLAYER
           PERFORM EIOInvJobstreamNew                                    *>DTLAYER
           SET CompanyCode OF EOInvJobstreamOb TO INVJB-CMPNY            *>DTLAYER
           SET ShortProgramName OF EOInvJobstreamOb TO INVJB-PGM         *>DTLAYER
           .                                                             *>DTLAYER

       InvJobstreamToRecord.                                             *>DTLAYER
           MOVE SPACES TO INVJB-REC                                      *>DTLAYER
           INITIALIZE INVJB-REC                                          *>DTLAYER
           SET INVJB-CMPNY TO CompanyCode OF EOInvJobstreamOb            *>DTLAYER
           SET INVJB-PGM TO ShortProgramName OF EOInvJobstreamOb         *>DTLAYER
                                                                         *>DTLAYER
           SET INVJB-NEXT TO ShortName OF Information OF ProgramCD OF pNext OF EOInvJobstreamOb *>DTLAYER
           SET INVJB-SWITCHES TO ProgramSwitch OF Information OF EOInvJobstreamOb *>DTLAYER
           .                                                             *>DTLAYER

       COPY "SalesInvoicingInvoiceJobstream.eiop" REPLACING ==()== BY ====. *>DTLAYER
      *************************************************************                
                                                                                   
