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
@16384
D=A
@pix        // reserve memory for pix and point A to it
M=D         // store 0 pixel location in pix variable

@24575
D=A
@endpix     // reserve memory for endpix and point A to it
M=D         // stor 512*256=131072 (i.e. screensize) in endpix location

(KBDCHECK)
  @KBD       // point A at KBD location
  D=M        // store keyboard value in D register
  @BLACK     // point A to BLACK instruction
  D;JGT      // if D > 0, goto BLACK
  @WHITE     // point A to WHITE instruction
  D;JEQ      // if D == 0, goto WHITE

(BLACK)
  @pix
  A=M
  M=-1
  @pix
  M=M+1
  D=M
  @endpix
  D=D-M
  @RESETPIX
  D;JGE
  @KBDCHECK
  0;JMP

(WHITE)
  @pix
  A=M
  M=0
  @pix
  M=M+1
  D=M
  @endpix
  D=D-M
  @RESETPIX
  D;JGE
  @KBDCHECK
  0;JMP

(RESETPIX)
  @16384
  D=A
  @pix
  M=D
  @KBDCHECK
  0;JMP
