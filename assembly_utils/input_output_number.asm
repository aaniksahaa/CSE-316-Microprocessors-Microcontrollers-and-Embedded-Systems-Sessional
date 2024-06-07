; Input a decimal number and output the same number
.MODEL SMALL

.STACK 100H

.DATA
    CR EQU 0DH
    LF EQU 0AH
    NEW_LINE DB CR, LF, '$'
    MSG1 DB 'ENTER A DECIMAL NUMBER: $'
    MSG2 DB CR, LF, 'THE NUMBER IS: $'
    IS_VALID DB ?
    DIGIT DB ?
    TNUM DW ?

.CODE

; IS_VALID DB ?
; check whether numeric and store in IS_VALID
CHECK_NUMERIC PROC
    PUSH BP
    MOV BP, SP
    MOV IS_VALID, 1   ; assume valid
    
    ;MOV DL, BYTE PTR [BP+4]
    
    CMP BYTE PTR [BP+4], '0'
    JB INVALID
    CMP BYTE PTR [BP+4], '9'
    JA INVALID
    JMP RETURN_CHECK
    
INVALID:
    MOV IS_VALID, 0
    
RETURN_CHECK:
    POP BP
    RET 2 
     
CHECK_NUMERIC ENDP

; DIGIT DB ?,TNUM DW ? 
; manipulates AX, DX, BX 
; takes input while digits are pressed; stores the input number in BX
INPUT_NUMBER PROC
    PUSH BP
    MOV BP, SP
    
    MOV BX, 0
    
    MOV AH, 1
    INT 21H
    
WHILE_VALID_DIGIT:
    MOV DIGIT, AL
    MOV AH, 0    
    PUSH AX
    CALL CHECK_NUMERIC
    
    CMP IS_VALID, 0
    JE  END_WHILE_VALID_DIGIT
    
    MOV AX, BX
    MOV BX, 10
    MUL BX
    MOV BX, AX
    SUB DIGIT, '0'
    MOV AX, 0
    MOV AL, DIGIT
    ADD BX, AX
     
    MOV AH, 1
    INT 21H
    
    JMP WHILE_VALID_DIGIT
    
END_WHILE_VALID_DIGIT:
    
    
RETURN_INPUT_NUMBER:
    MOV TNUM, BX
    POP BP
    RET
    
INPUT_NUMBER ENDP

; TNUM DW ? 
; manipulates AX, BX, CX, DX 
; outputs the number that is stored in TNUM
PRINT_NUMBER PROC
    PUSH BP
    MOV BP, SP
    
    MOV BX, TNUM
    
    MOV AH, 0
    MOV AL, '#'
    PUSH AX; marker

WHILE_NONZERO:
    CMP BX, 0
    JE END_WHILE_NONZERO
    
    MOV DX, 0
    MOV AX, BX
    MOV CX, 10
    DIV CX
    
    MOV BX, AX
    
    ADD DL, '0'
    PUSH DX
    
    JMP WHILE_NONZERO    
    
END_WHILE_NONZERO:   
    
WHILE_NOT_HASH:
    POP CX
    CMP CL, '#'
    JE END_WHILE_NOT_HASH
    
    MOV AH, 2
    MOV DL, CL
    INT 21H
    
    JMP WHILE_NOT_HASH
    
END_WHILE_NOT_HASH:
    
RETURN_PRINT_NUMBER:
    POP BP
    RET
PRINT_NUMBER ENDP

MAIN PROC
;initialize DS
    MOV AX, @DATA
    MOV DS, AX
    
    MOV AH, 9
    LEA DX, MSG1
    INT 21H
    
    CALL INPUT_NUMBER
    
    MOV AH, 9
    LEA DX, MSG2
    INT 21H    
    
    CALL PRINT_NUMBER
    
;DOX exit
    MOV AH, 4CH
    INT 21H
  
MAIN ENDP

    END MAIN