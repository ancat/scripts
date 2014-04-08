/*
    A ghetto strace based on pin. Probably won't work for multithreaded programs.
    pin makes errythang easy.
*/

#include "pin.H"
#include <iostream>
#include <fstream>
#include <stdio.h>

VOID trace_syscall_entry(THREADID threadIndex, CONTEXT *ctxt, SYSCALL_STANDARD std, VOID *v) {
    printf("syscall0x%lx(0x%lx, 0x%lx, 0x%lx, 0x%lx) = ",
        PIN_GetSyscallNumber(ctxt, std),
        PIN_GetSyscallArgument(ctxt, std, 0),
        PIN_GetSyscallArgument(ctxt, std, 1),
        PIN_GetSyscallArgument(ctxt, std, 2),
        PIN_GetSyscallArgument(ctxt, std, 3)
    );
}

VOID trace_syscall_exit(THREADID threadIndex, CONTEXT *ctxt, SYSCALL_STANDARD std, VOID* v) {
    printf("0x%lx\n", PIN_GetSyscallReturn(ctxt, std));
}

int main(int argc, char** argv) {
    if(PIN_Init(argc,argv)) {
        return 1;
    }

    PIN_AddSyscallEntryFunction(trace_syscall_entry, 0);
    PIN_AddSyscallExitFunction(trace_syscall_exit, 0);
    // Start the program, never returns
    PIN_StartProgram();
    
    return 0;
}

