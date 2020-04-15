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
@8192
D=A
@limit
M=D
(LOOP)
  @i
  M=0
  @KBD
  D=M
  @FILL-WHITE
  D;JEQ
  (FILL-BLACK)
    @i
    D=M
    @limit
    D=M-D
    @LOOP
    D;JEQ //if i=8192, jump to LOOP
    @i
    D=M
    @SCREEN
    A=A+D //current position = screen + i
    M=-1  // fill black, 0xFF
    @i
    M=M+1
    @FILL-BLACK
    0; JMP
  (FILL-WHITE)
    @i
    D=M
    @limit
    D=M-D
    @LOOP
    D;JEQ //if i=8192, jump to LOOP
    @i
    D=M
    @SCREEN
    A=A+D //current position = screen + i
    M=0  // fill white, 0x00
    @i
    M=M+1
    @FILL-WHITE
    0; JMP
