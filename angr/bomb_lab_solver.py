import angr, logging

logging.basicConfig()
logging.getLogger('angr.surveyors.explorer').setLevel(logging.WARNING)

def phase2():
    proj = angr.Project('bomb', load_options={'auto_load_libs':False})

    def read_six_numbers(state):
        print "read_six_numbers"
        state.memory.store(state.regs.ebp-0x18, 1)

    proj.hook(0x8048fd8, read_six_numbers)
    start_addr = 0x08048b60 # after read_six_numbers

    dest_addr  = 0x08048b6e # branch=true; mov ebx, 1
    dest_addr = 0x08048b8e

    state = proj.factory.blank_state(addr=start_addr)
    state.memory.store(state.regs.ebp-0x18, state.se.BVS('test', 32))
    path = proj.factory.path(state=state)
    ex = proj.surveyors.Explorer(start=path, find=(dest_addr,), enable_veritesting=True)
    ex.run()

    numbers = []

    if ex.found:
        found = ex.found[0].state
        for i in xrange(6):
            numbers.append(int(found.se.any_int( found.memory.load(found.regs.ebp-0x18+4*i,4).reversed )))

        return numbers

    return False

def phase3():
    proj = angr.Project('bomb', load_options={'auto_load_libs':False})

    start_addr = 0x8048bc9
    dest_addr = 0x8048c99

    state = proj.factory.blank_state(addr=start_addr)

    state.memory.store(state.regs.ebp-0xc, state.se.BVS('byte1', 32))
    state.memory.store(state.regs.ebp-0x5, state.se.BVS('char',   4))
    state.memory.store(state.regs.ebp-0x4, state.se.BVS('byte2', 32))


    path = proj.factory.path(state=state)
    ex = proj.surveyors.Explorer(start=path, find=(dest_addr,), enable_veritesting=True)
    ex.run()

    numbers = []

    if ex.found:
        found = ex.found[0].state
        numbers.append(int(found.se.any_int( found.memory.load(found.regs.ebp-0xc, 4).reversed )))
        numbers.append(chr(found.se.any_int( found.memory.load(found.regs.ebp-0x5, 1).reversed )))
        numbers.append(int(found.se.any_int( found.memory.load(found.regs.ebp-0x4, 4).reversed )))

        return numbers

    return False

def phase4():
    proj = angr.Project('bomb', load_options={'auto_load_libs':False})
    #proj.hook(0x08048d15, sym4)

    start_addr = 0x08048d03
    dest_addr  = (0x08048d0e,0x08048d09)

    state = proj.factory.blank_state(addr=start_addr)
    #state.regs.eax = state.se.BVS('dong', 32)

    state.memory.store(state.regs.ebp-0x4, state.se.BVS('byte1', 32))
    #state.memory.store(state.regs.ebp-0x4, 9)


    path = proj.factory.path(state=state)
    ex = proj.surveyors.Explorer(start=path, find=dest_addr, enable_veritesting=True)
    ex.run()

    numbers = []

    if ex.found:
        found = ex.found[0].state
        numbers.append(int(found.se.any_int(found.regs.eax)))
        #numbers.append(int(found.se.any_int( found.memory.load(found.regs.ebp-0x4, 4).reversed )))

    return False


if __name__ == '__main__':
    print phase2()
    print phase3()
    print phase4()
