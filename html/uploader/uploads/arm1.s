;-VIPUL KOHLI
;-CSE 2240
;-PROGRAM 5
;-returns address of search key number

sram_base EQU 0x40000000
numvals EQU 11
keyval EQU 17

 AREA prog1, CODE, READONLY
 ENTRY
foundpos rn 0
arraybase rn 1
size rn 3
lb rn 4
ub rn 5
var1 rn 6
halfindex rn 7
 adr arraybase, array
 LDR sp, =sram_base
 mov var1, #5
 mov lb, #0
 mov var1, #numvals
 SUB ub, var1, #1
 stmia sp!, {lb, ub}
 BL search ;after link convert index to address
 LSL r0, r0, #2
 ADD r0, r0, arraybase
stop BAL stop 

array DCD 3,6,8,12,17,22,45,67,99,2089,30001
	
search
 STMIA sp!, {lr}
 ldr lb, [sp, #-12]
 ldr ub, [sp, #-8]
 cmp lb, ub
 movgt foundpos, #-1
 bgt return
 add halfindex, lb, ub ;lb is r4 ub is r5
 asr halfindex, #1
 ldr var1, [arraybase, halfindex, LSL #2]
 cmp var1, #keyval ;=17
 moveq foundpos, halfindex
 beq return
 subgt ub, halfindex, #1 
 addlt lb, halfindex, #1
 stmia sp!, {lb, ub}
 BL search
  add sp, sp, #-8
return
 ldmdb sp!, {pc}
;END OF PROGRAM
  end