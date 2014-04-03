import argparse
import Image
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("file", help="File to process", type=str)
parser.add_argument("-x", "--hex", dest="hex", action="store_true", help="Display hex dump instead")
parser.add_argument("-n", "--lines", dest="lines", type=int, help="How many lines of the hex dump to display")
parser.add_argument("-z", "--nulls", dest="nulls", type=int, help="How many null bytes until processing stops", default=0)
parser.add_argument("-c", "--color", dest="color", help="Which color to look at (r/g/b), only for some formats", default="r")
parser.add_argument("-m", "--msb", dest="msb", action="store_true", help="Look at MSB instead of LSB", default=False)
args = parser.parse_args()

def hexdump(data, columns, lines=0):
    printable = range(0x21, 0x7f)
    buf = ""
    num_lines = 0
    for i, byte in enumerate(data):
        if i%columns == 0:
            offset_buf = format(i, '08x')+":"
            hex_buf = ""
            byte_buf = ""

        hex_buf += byte.encode('hex')+" "
        if ord(byte) in printable:
            byte_buf += byte
        else:
            byte_buf += "."

        if i%columns == columns-1 or i == len(data)-1:
            buf += offset_buf + " " + hex_buf.ljust(columns*3, ' ') + " " + byte_buf + "\n"
            num_lines += 1

        if num_lines == lines:
            break

    return buf

def extract_bmp(image_data, color, bit, max_null_bytes):
    pix = image_data.load()
    buf = "0b"
    count = 0
    strbuf = ""
    nulls = 0
    size = image_data.size
    for y in range(size[1]):
        for x in range(size[0]):
            r,g,b = pix[(x,y)]
            if color == "r":
                buf += str(r&1)
            elif color == "g":
                buf += str(g&1)
            else:
                buf += str(b&1)
            count += 1
            if count == 8:
                char = chr(int(buf,2))
                strbuf += char
                if max_null_bytes != 0:
                    if char == "\x00":
                        nulls += 1
                    else:
                        nulls = 0
                    if nulls == max_null_bytes:
                        return strbuf
                buf = "0b"
                count = 0
    return strbuf

def extract_png(image_data, color, bit, max_null_bytes):
    pix = image_data.load()
    buf = "0b"
    count = 0
    strbuf = ""
    nulls = 0
    size = image_data.size
    for y in range(size[1]):
        for x in range(size[0]):
            r = pix[(x,y)]
            buf += str(r&1)
            count += 1
            if count == 8:
                char = chr(int(buf,2))
                strbuf += char
                if max_null_bytes != 0:
                    if char == "\x00":
                        nulls += 1
                    else:
                        nulls = 0
                    if nulls == max_null_bytes:
                        return strbuf
                buf = "0b"
                count = 0
    return strbuf

image = Image.open(args.file)
if image.format == 'BMP':
    if args.color not in "rgb":
        args.color = "r"
    data = extract_bmp(image, args.color, args.msb, args.nulls)
elif image.format == 'PNG':
    data = extract_png(image, None, args.msb, args.nulls)
else:
    sys.stderr.write("Only BMP/PNG supported!\n")
    sys.exit()

if args.hex:
    print hexdump(data, 16, lines=args.lines)
else:
    print data

