// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

@R2
M = 0 // Clear the output

(LOOP)
    @R1
    D = M     // Load R1 (our multiplier) into the D register
    @END
    D;JEQ     // Jump to END if R1 = 0

    @R0
    D = M     // Load R0 (our multiplicand) into the D register

    @R2       // Point the A register at the result
    M = D + M // Add the D value to our result

    @R1
    M = M - 1 // Subtract 1 from our multiplier

    @LOOP
    0;JMP     // Jump to LOOP. Note that we exit the loop when R1 = 0 above!

(END)
	@END
	0;JMP
