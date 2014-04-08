/*
    basic pin tool for printing out basic blocks executed in the main executable
    warning: pin has a different definition of basic blocks so it might not
    match up with what ida says.
*/

#include "pin.H"
#include <iostream>
#include <fstream>
#include <stdio.h>

std::ostream * out = &cerr;
ADDRINT image_low;
ADDRINT image_high;
USIZE image_size;

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE,  "pintool",
    "o", "", "specify file name for MyPinTool output");

INT32 Usage() {
    cerr << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

VOID Image(IMG img, VOID * v) {
    if (IMG_IsMainExecutable(img)) {
	printf(
		"LowAddress: %lx HighAddress: %lx ImageBase: %lx: %s\n",
		IMG_LowAddress(img),
		IMG_HighAddress(img),
		IMG_StartAddress(img),
		IMG_Name(img).c_str()
	);
        image_low  = IMG_LowAddress(img);
	image_high = IMG_HighAddress(img);
    }
}

VOID Fini(INT32 code, VOID* v) {
    *out <<  "===============================================" << endl;
}

VOID PIN_FAST_ANALYSIS_CALL handle_basic_block(UINT32 number_instruction_in_bb, ADDRINT address_bb) {
	if (image_low <= address_bb && image_high > address_bb) {
		printf("handling basic block %p (%d instrs)\n", (void*) address_bb, number_instruction_in_bb);
	}
}

VOID trace_instrumentation(TRACE trace, VOID *v)
{
    for(BBL bbl = TRACE_BblHead(trace); BBL_Valid(bbl); bbl = BBL_Next(bbl)) {
        BBL_InsertCall(
            bbl,
            IPOINT_ANYWHERE,
            (AFUNPTR)handle_basic_block,
            IARG_FAST_ANALYSIS_CALL, 
            IARG_UINT32,
            BBL_NumIns(bbl),

            IARG_ADDRINT,
            BBL_Address(bbl),

            IARG_END
        );
    }
}

int main(int argc, char** argv) {
    if(PIN_Init(argc,argv)) {
        return Usage();
    }

    string fileName = KnobOutputFile.Value();

    if (!fileName.empty()) { out = new std::ofstream(fileName.c_str());}

    // trace image loading
    IMG_AddInstrumentFunction(Image, 0);
    TRACE_AddInstrumentFunction(trace_instrumentation, 0);
    // Start the program, never returns
    PIN_StartProgram();
    
    return 0;
}

