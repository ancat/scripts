import idc
import idautils
import idaapi

traces = open(idc.AskFile(0, "*", "Where the traces at?"), 'r').read()
traces = [int(trace) for trace in traces.split()]
unique_traces = {}
for trace in traces:
    if trace not in unique_traces:
        unique_traces[trace] = 1
    else:
        unique_traces[trace] += 1

def get_basic_block(ea):
    basic_blocks = idaapi.FlowChart(idaapi.get_func(ea))
    for block in basic_blocks:
        if block.startEA == ea:
            return block

def color_block (bb, color):
    for ea in idautils.Heads(bb.startEA, bb.endEA):
        idc.SetColor(ea, idc.CIC_ITEM, color)

for trace in unique_traces:
    idc.MakeComm(trace, "Hit %d times"%unique_traces[trace])
    color_block(get_basic_block(trace), 0xc8ffc8)
