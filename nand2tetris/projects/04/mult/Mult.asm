// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
(START)
@R2 // initialize final store value as 0
M = 0
@R0 // if R0 is zero, END
D = M; JEQ
@R1 // if R1 is zero, END
D = M; JEQ

@R0 // initalize loop variable i
D = M
@i
M = D

(LOOP)
@R1
D = M
@R2
M = D + M
@i // save value of R0 - 1
M = M - 1
@i //check value of i
D = M; 
@LOOP
D;JGT

(END)
@END
0;JMP