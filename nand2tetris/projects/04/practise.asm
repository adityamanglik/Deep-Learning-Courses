// program to add 2 numbers
// RAM[2] = RAM[0] + RAM[1]
// Usage: place operators in RAM[1] and RAM[0]

@0
D = M

@1
D = D + M

@2
M = D

@6
0;JEQ