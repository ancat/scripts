import angr, logging, sys, claripy

#logging.basicConfig()
#logging.getLogger('angr.surveyors.explorer').setLevel(logging.WARNING)

counter = 0
def scanf(state):
    global counter
    print counter
    #bitvector = state.se.BVS('int{0}'.format(counter), 32)
    bitvector = claripy.BVS('int{0}'.format(counter), 32)
    #state.add_constraints(bitvector > 0x1f)
    #state.add_constraints(bitvector < 0x7f)
    counter += 1
    state.memory.store(state.regs.rsi, bitvector)

start_addr = 0x4006C6
#dest_addr  = 0x4025CC
#dest_addr  = 0x402911
dest_addr = 0x4028E0 # right before CheckSolution
dest_addr = 0x402917 # at positive answer

proj = angr.Project('baby-re')
#proj.hook(0x4005B0, scanf)
for i in [0x402634, 0x40266C, 0x4026A4, 0x4026DC, 0x402714, 0x40274C, 0x402784, 0x4027BC, 0x4027F4, 0x40282C, 0x402864, 0x40289C, 0x4028D4]:
    proj.hook(i, scanf, length=5)
#state = proj.factory.blank_state(addr=start_addr)
state = proj.factory.full_init_state()
path = proj.factory.path(state=state)
ex = proj.surveyors.Explorer(start=path, find=(dest_addr,))
ex.run()
print ex.found
if not ex.found:
    print "fail"
    sys.exit(1)

found = ex.found[0]
print hex(found.state.se.any_int(found.state.regs.rip))

buf = ''
for i in range(13):
    memory = found.state.se.any_int(found.state.memory.load(found.state.se.any_int(found.state.regs.rbp-0x30-i*4), 1))
    buf = chr(memory) + buf
    #memory = (memory & 0xFF00000000000000) >> 56

print buf
sys.exit(0)
import readline # optional, will allow Up/Down/History in the console
import code
vars = globals().copy()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()

sys.exit(0)
