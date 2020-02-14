// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

  // create a sum counter
  @i    // reserve memory for i
  M=1   // set i=1

  @R2   // point A to R2's location
  M=0   // set R2 to 0

// start "mul" loop by addition
(LOOP)
  @i    // grab i
  D=M   // store i in D register
  @R1   // get R1
  D=D-M // D=i-R1
  @END  // point A to end of loop
  D;JGT // if D > 0, goto end of loop
  @R0   // point A at R1
  D=M   // set D=mul+R0
  @R2   // point A to R2
  M=D+M // set R2=D
  @i    // point A to i
  M=M+1 // i=i+1
  @LOOP // point A to beginning of loop
  0;JMP // jump to beginning of loop
(END)
  @END  // point A to end of program
  0;JMP // jump to end of program
