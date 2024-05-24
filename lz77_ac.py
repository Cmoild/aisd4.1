import lz77
import arithmetic


def LZ77_AC_COMPRESS(__path: str, __newPath: str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    res = lz77.LZ77_encode(data)
    s = "".join([chr(x[0]//255) + chr(x[0]%255) + chr(x[1]) + x[2] for x in res])
    print("S LENGTH", len(s))
    b = arithmetic.GetCompressedBytes(s)
    
    with open(__newPath, 'wb') as f:
        f.write(b)
        f.close()

# декомпрессор на основе LZ77
def LZ77_AC_DECOMPRESS(__path: str):
    with open(__path, 'rb') as f:
        data = f.read()
        f.close()
    data = arithmetic.GetOriginalFromBytes(data)
    print(len(data))
    #data = data.decode('utf-8', 'surrogatepass')
    data = [((ord(data[i])*255 + ord(data[1 + i])), ord(data[2 + i]), data[3 + i]) for i in range(0, int(len(data)/4)*4, 4)]
    old_len = 0
    for i in data:
        old_len += i[1] + 1
    return lz77.LZ77_decode(data, old_len)
