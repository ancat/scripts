import idautils, idc

gdbinit = ""
for name_address in idautils.Names():
    addr = name_address[0]
    name = name_address[1]

    name = name.replace('.', '_')
    gdbinit += "set $%s=0x%x\n"%(name, addr)

if gdbinit:
    output_file = idc.AskFile(1, "*", "Save gdbinit file?")
    if output_file:
        handle = open(output_file, "w")
        handle.write(gdbinit)
        handle.close()
    else:
        idc.Warning("gdbinit file not saved")
else:
    idc.Warning("no gdbinit generated")
