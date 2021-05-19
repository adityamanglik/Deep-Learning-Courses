// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(START)
@24576
D = M
@FILLSCREEN
D;JNE //if any key press is detected, fill screen
@EMPTYSCREEN
D;JEQ //if no key pressed, empty screen

(FILLSCREEN)
//initialize variables
@i
M = 0
@8192
D = A
@n // assign 8192 as number of loop iterations
M = D

//begin loop
(LOOP)
@i
D = M
@n
D = D - M // i = i - n
@START // TODO: change to START
D; JEQ
//screen[i] = -1
@SCREEN
D = A
@i
A = D + M // address = 16384 + i
M = -1 // set value in memory to -1
@i //increment i
M = M + 1
@LOOP
0;JMP

(EMPTYSCREEN)
//initialize variables
@i
M = 0
@8192
D = A
@n // assign 8192 as number of loop iterations
M = D

//begin loop
(LOOP1)
@i
D = M
@n
D = D - M // i = i - n
@START // TODO: change to START
D; JEQ
//screen[i] = -1
@SCREEN
D = A
@i
A = D + M // address = 16384 + i
M = 0 // set value in memory to -1
@i //increment i
M = M + 1
@LOOP1
0;JMP

(END)
@END
0; JMP
