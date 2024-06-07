.MODEL SMALL

.STACK 100H

.DATA
    CR EQU 0DH
    LF EQU 0AH
    
    NEW_LINE DB CR, LF, '$'
    PROMPT DB 'Please enter three characters: $'
    P DB ?
    Q DB ?
    R DB ?
    MSG_ERROR DB CR,LF,'Sorry! Please input only lowercase letters ',CR,LF,'$'
    MSG_RESULT DB 'Second highest character: $'
    MSG_EQUAL DB 'All letters are equal$'

.CODE

; check the character stored in AL and write corresponding validity check in CX
CHECK PROC    
    CMP AL, 'a'
    JB INVALID
    CMP AL, 'z'
    JA INVALID
    
    MOV CX, 1                  ; valid
    RET 
    
INVALID:
    MOV CX, 0                  ; invalid
    RET

    
CHECK ENDP


MAIN PROC
;initialize DS
    MOV AX, @DATA
    MOV DS, AX
    
START:
   
;print user prompt
    LEA DX, PROMPT
    MOV AH, 9
    INT 21H
    
    MOV AH, 1
    
;input first character
    INT 21H
    
    CALL CHECK
    CMP CX, 0
    JNZ VALID_FIRST
    
    MOV AH, 9
    LEA DX, MSG_ERROR
    INT 21H
    JMP START 

VALID_FIRST:    
    MOV P, AL                ; store the first character
    INT 21H                  ; skip space
   
;input second character
    INT 21H
    
    CALL CHECK
    CMP CX, 0
    JNZ VALID_SECOND
    
    MOV AH, 9
    LEA DX, MSG_ERROR
    INT 21H
    JMP START 

VALID_SECOND:    
    MOV Q, AL                ; store the second character
    INT 21H                  ; skip space

;input third character
    INT 21H
    
    CALL CHECK
    CMP CX, 0
    JNZ VALID_THIRD
    
    MOV AH, 9
    LEA DX, MSG_ERROR
    INT 21H
    JMP START
    
VALID_THIRD:    
    MOV R, AL                ; store the third character
    
;print new line
    MOV AH, 9
    LEA DX, NEW_LINE         ; print new line
    INT 21H
    
;performing comparisons    
    MOV BL, P
    CMP BL, Q                ; compare P and Q
    
    JB P_BELOW_Q             ; P < Q
    JE P_EQUAL_Q             ; P = Q
    JA P_ABOVE_Q             ; P > Q

P_BELOW_Q:
    MOV BL, R
    CMP BL, Q                ; compare R and Q
    
    JA R_ABOVE_Q             ; R < Q
    JE R_EQUAL_Q             ; R = Q
    JB R_BELOW_Q             ; R > Q
    
    R_ABOVE_Q:
        MOV DL, Q            ; answer is Q
        JMP END_SUBCASE_1
    R_EQUAL_Q:
        MOV DL, P            ; answer is P
        JMP END_SUBCASE_1
    R_BELOW_Q:
        MOV BL, R
        CMP BL, P            ; compare R and P
        
        JNA R_LEQ_P
        MOV DL, R            ; answer is R
        JMP END_SUBCASE_1
        
        R_LEQ_P:
            MOV DL, P        ; answer is P
            
    END_SUBCASE_1:
        JMP END_CASE
        
P_EQUAL_Q:
    MOV BL, R
    CMP BL, P                ; compare R and P
    
    JA R_ABOVE_P             ; R < P
    JE R_EQUAL_P             ; R = Q
    JB R_BELOW_P             ; R > Q
    
    R_ABOVE_P:
        MOV DL, P            ; answer is P
        JMP END_SUBCASE_2
        
    R_EQUAL_P:
        MOV AH, 9
        LEA DX, MSG_EQUAL    ; show equal message and exit
        INT 21H
        JMP EXIT
        
    R_BELOW_P:              
        MOV DL, R            ; answer is R
        JMP END_SUBCASE_2
            
    END_SUBCASE_2:
        JMP END_CASE
    
P_ABOVE_Q:
    MOV BL, Q
    XCHG P, BL
    XCHG Q, BL               ; exchanging P and Q to convert into the first case
    JMP P_BELOW_Q
    
END_CASE:
    MOV BL, DL               ; keeping the value at DL into BL, since it will be needed later
    
    MOV AH, 9
    LEA DX, MSG_RESULT       ; printing message on output
    INT 21H
    
    MOV DL, BL    
    MOV AH, 2                ; printing output character
    INT 21H

EXIT:    
;DOX exit
    MOV AH, 4CH
    INT 21H
  
MAIN ENDP

    END MAIN