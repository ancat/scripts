# python writestego.py targetimage.bmp stringtowrite
# text is null terminated automagically

import Image
import sys

bmp = Image.open(sys.argv[1])
pix = bmp.load()
lsb = []
size = bmp.size
ordrex = range(size[0])
ordrey = range(size[1])
rs = ""
gs = ""
bs = ""
buf = "0b"
rtemp = 0
gtemp = 0
btemp = 0
count = 0
strbuf = ""
target = [int(y) for y in ''.join([bin(ord(x))[2:].rjust(8,"0") for x in sys.argv[2]+"\x00"])]
print target
for x in ordrex:
    if x >= len(target):
        break
    r,g,b = pix[(x,0)]
    r = r >> 1 << 1
    g = g >> 1 << 1
    b = b >> 1 << 1
    r = r|target[x]
    g = g|target[x]
    b = b|target[x]
    pix[(x,0)] = (r,g,b)
    bmp.putpixel((x,0), (r,g,b))
    buf += str(g&1)
    count += 1
    if count == 8:
        strbuf += chr(int(buf,2))
        buf = "0b"
        count = 0
bmp.save('lol.bmp')
sys.exit()
print strbuf
lsb = "".join(lsb)
lsb = "".join(chr(int(lsb[i:i+8][::-1],2)) for i in range(0,len(lsb),8))
print lsb
print rs,gs,bs
