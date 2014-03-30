import idc
import idautils
import idaapi

BASIC_FUNCTION_TRACE = 1
SPECIFIC_FUNCTION_TRACE = 2
FULL_FUNCTION_TRACE = 3
function_name = "phase_3"

current_mode = FULL_FUNCTION_TRACE

def get_basic_blocks(ea):
    basic_blocks = [block.startEA for block in idaapi.FlowChart(idaapi.get_func(ea))]
    return basic_blocks

def get_function_name(function_name):
    start = idc.BeginEA()
    for funcea in idautils.Functions(idc.SegStart(ea), idc.SegEnd(ea)):
        if function_name == idc.GetFunctionName(funcea):
            return funcea

def trace_specific_function(function_name):
    target = get_function_name(function_name)
    return get_basic_blocks(target)

def trace_all_functions():
    blocks = []
    start = idc.BeginEA()
    for funcea in idautils.Functions(idc.SegStart(ea), idc.SegEnd(ea)):
        blocks += get_basic_blocks(funcea)
    return blocks

def trace_function_calls():
    blocks = []
    start = idc.BeginEA()
    for funcea in idautils.Functions(idc.SegStart(ea), idc.SegEnd(ea)):
        blocks.append(funcea)
    return blocks

if current_mode == SPECIFIC_FUNCTION_TRACE:
    traces = trace_specific_function(function_name)
elif current_mode == FULL_FUNCTION_TRACE:
    traces = trace_all_functions()
elif current_mode == BASIC_FUNCTION_TRACE:
    traces = trace_function_calls()

buf = "python trace_file = open('traces.txt', 'w')\n"
for trace in traces:
    buf += "break *"+hex(trace)+"\n"
    buf += "commands\n"
    buf += "    python trace_file.write('%d\\n')\n"%trace
    buf += "    continue\n"
    buf += "end\n"

output_file = idc.AskFile(1, "*", "Save gdbinit file?")
if output_file:
    handle = open(output_file, "w")
    handle.write(buf)
    handle.close()

