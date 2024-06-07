.MODEL SMALL

.STACK 100H

.DATA
    CR EQU 0DH
    LF EQU 0AH
    IS_VALID DB ?
    DIGIT DB ?
    PROMPT DB '... $'
    LEN EQU 3
    ARR DW 3, 2, 2 
    ASC DW 1
    DESC DW 1
    MSG1 DB 'Ascending$'
    MSG2 DB 'Descending$'
    MSG3 DB 'Not sorted$'
.CODE

MAIN PROC
;initialize DS
    MOV AX, @DATA
    MOV DS, AX
    
    MOV CX, LEN
    DEC CX
    
    MOV AX, [ARR] ; prev
    
    LEA SI, ARR
    ADD SI, 2
    
HERE:
    MOV BX, [SI]
    
    CMP BX, AX
    JG GREATER 
    JL LOWER
    
GREATER:
    MOV DESC, 0
    JMP AGAIN 
     
LOWER:
    MOV ASC, 0

AGAIN:
    ADD SI, 2
    ;DEC CX
    MOV AX, BX
    
    LOOP HERE
    
    MOV AX, ASC
    MOV BX, DESC
    
    CMP AX, 1
    JE ASCENDING
    CMP BX, 1
    JE DESCENDING
    LEA DX, MSG3
    JMP PRINT
    
ASCENDING:
    LEA DX, MSG1
    JMP PRINT
    
DESCENDING:
    LEA DX, MSG2
    
PRINT:
    MOV AH, 9
    INT 21H
    
    
    
    
;DOS exit
    MOV AH, 4CH
    INT 21H
  
MAIN ENDP

    END MAIN