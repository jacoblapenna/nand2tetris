// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@EQUAL0
D;JEQ
@NOT_EQUAL0
0;JMP
(EQUAL0)
@SP
A=M
M=-1
@EQ_FINISH0
0;JMP
(NOT_EQUAL0)
@SP
A=M
M=0
@EQ_FINISH0
0;JMP
(EQ_FINISH0)
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@EQUAL1
D;JEQ
@NOT_EQUAL1
0;JMP
(EQUAL1)
@SP
A=M
M=-1
@EQ_FINISH1
0;JMP
(NOT_EQUAL1)
@SP
A=M
M=0
@EQ_FINISH1
0;JMP
(EQ_FINISH1)
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@EQUAL2
D;JEQ
@NOT_EQUAL2
0;JMP
(EQUAL2)
@SP
A=M
M=-1
@EQ_FINISH2
0;JMP
(NOT_EQUAL2)
@SP
A=M
M=0
@EQ_FINISH2
0;JMP
(EQ_FINISH2)
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@LESS_THAN3
D;JLT
@NOT_LESS_THAN3
0;JMP
(LESS_THAN3)
@SP
A=M
M=-1
@LT_FINISH3
0;JMP
(NOT_LESS_THAN3)
@SP
A=M
M=0
@LT_FINISH3
0;JMP
(LT_FINISH3)
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@LESS_THAN4
D;JLT
@NOT_LESS_THAN4
0;JMP
(LESS_THAN4)
@SP
A=M
M=-1
@LT_FINISH4
0;JMP
(NOT_LESS_THAN4)
@SP
A=M
M=0
@LT_FINISH4
0;JMP
(LT_FINISH4)
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@LESS_THAN5
D;JLT
@NOT_LESS_THAN5
0;JMP
(LESS_THAN5)
@SP
A=M
M=-1
@LT_FINISH5
0;JMP
(NOT_LESS_THAN5)
@SP
A=M
M=0
@LT_FINISH5
0;JMP
(LT_FINISH5)
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@GREATER_THAN6
D;JGT
@NOT_GREATER_THAN6
0;JMP
(GREATER_THAN6)
@SP
A=M
M=-1
@GT_FINISH6
0;JMP
(NOT_GREATER_THAN6)
@SP
A=M
M=0
@GT_FINISH6
0;JMP
(GT_FINISH6)
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@GREATER_THAN7
D;JGT
@NOT_GREATER_THAN7
0;JMP
(GREATER_THAN7)
@SP
A=M
M=-1
@GT_FINISH7
0;JMP
(NOT_GREATER_THAN7)
@SP
A=M
M=0
@GT_FINISH7
0;JMP
(GT_FINISH7)
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
A=M
D=M
@GREATER_THAN8
D;JGT
@NOT_GREATER_THAN8
0;JMP
(GREATER_THAN8)
@SP
A=M
M=-1
@GT_FINISH8
0;JMP
(NOT_GREATER_THAN8)
@SP
A=M
M=0
@GT_FINISH8
0;JMP
(GT_FINISH8)
@SP
M=M+1
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1// neg
@SP
M=M-1
@SP
A=M
M=-M
@SP
M=M+1// and
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=D&M
@SP
M=M+1// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=D|M
@SP
M=M+1// not
@SP
M=M-1
@SP
A=M
M=!M
@SP
M=M+1