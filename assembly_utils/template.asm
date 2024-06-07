.MODEL SMALL


.STACK 100H

.DATA

.CODE

MAIN1 PROC
	
    MOV DX, 0 ; DX counts the characters
    MOV AH, 1 ; read char function
    INT 21h ; read a char in AL
WHILE_:
    CMP AL, 0DH ; CR?
    JE END_WHILE
    INC DX
    INT 21h
    JMP WHILE_
END_WHILE:

MAIN1 ENDP
END MAIN1
