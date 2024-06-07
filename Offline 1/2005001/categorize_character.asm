.MODEL SMALL

.STACK 100H

.DATA
    CR EQU 0DH
    LF EQU 0AH
    
    CHAR DB ?
    PROMPT DB 'Please input a single printable character: $'
    NEW_LINE DB CR, LF, '$'
    MSG_UPPER DB 'Uppercase letter$'
    MSG_LOWER DB 'Lowercase letter$'
    MSG_NUMBER DB 'Number$'
    MSG_OTHERS DB 'Not an alphanumeric value$'

.CODE

MAIN PROC
;initialize DS
    MOV AX, @DATA
    MOV DS, AX

;prompt the user
    LEA DX, PROMPT
    MOV AH, 9
    INT 21H

;read a character
    MOV AH, 1
    INT 21H
    MOV CHAR, AL

;categorize the character
CHECK_UPPER:
    CMP CHAR, 'A'
    JNAE CHECK_LOWER
    CMP CHAR, 'Z'
    JNBE CHECK_LOWER
    
    LEA CX, MSG_UPPER
    JMP END_CHECK
    
CHECK_LOWER:
    CMP CHAR, 'a'
    JNAE CHECK_NUMBER
    CMP CHAR, 'z'
    JNBE CHECK_NUMBER
    
    LEA CX, MSG_LOWER
    JMP END_CHECK

CHECK_NUMBER:
    CMP CHAR, '0'
    JNAE OTHERS
    CMP CHAR, '9'
    JNBE OTHERS
    
    LEA CX, MSG_NUMBER
    JMP END_CHECK

OTHERS:
    LEA CX, MSG_OTHERS    
            
END_CHECK:
    
    MOV AH, 9
    
    LEA DX, NEW_LINE
    INT 21H
    
    MOV DX, CX
    INT 21H
        
;DOX exit
    MOV AH, 4CH
    INT 21H
  
MAIN ENDP

    END MAIN