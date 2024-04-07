from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar, c_ushort
class LZ77_struct(Structure):
    _fields_ = [
        ('offset', c_ushort),
        ('length', c_ushort),
        ('symbol', c_wchar)
    ]

class LZ77_result(Structure):
    _fields_ = [
        ('out', POINTER(LZ77_struct)),
        ('numberOfElements', c_int)
    ]

def LZ77_encode(data: str):
    lib = CDLL(".\mylib.so")
    c_data = c_wchar_p(data)
    lib.lz77_encode.restype = LZ77_result
    c_res = lib.lz77_encode(c_data, len(data))
    return [(c_res.out[i].offset, c_res.out[i].length, c_res.out[i].symbol) for i in range(c_res.numberOfElements)]

def LZ77_decode(data: list, old_len: int):
    lib = CDLL(".\mylib.so")
    c_data = (LZ77_struct * len(data))()
    for i in range(len(data)):
        c_data[i].offset = c_ushort(data[i][0])
        c_data[i].length = c_ushort(data[i][1])
        c_data[i].symbol = c_wchar(data[i][2])
    lib.lz77_decode.restype = c_wchar_p
    c_res = lib.lz77_decode(c_data, len(data), old_len)
    return c_res

def lz77_decode(in_tuples, numOfTuples, numOldLen):
    result = ''
    pos = 0
    k = 0
    
    for cur in in_tuples:
        
        for j in range(cur[1]):
            if (pos - cur[0] >= 0 and pos - cur[0] < len(result)):
                result += result[pos - cur[0]]
                pos += 1
        
        result += cur[2]
        pos += 1
        if k % 100000 == 0:
            print(result[len(result)-10:len(result)])
        k += 1
    
    return result

def LZ77_COMPRESS(__path: str, __newPath: str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    res = LZ77_encode(data)
    s = "".join([chr(x[0]) + chr(x[1]) + x[2] for x in res])
    with open(__newPath, 'wb') as f:
        f.write(bytes(s.encode('utf-8')))
        f.close()
    
def LZ77_DECOMPRESS(__path: str):
    with open(__path, 'rb') as f:
        data = f.read()
        f.close()
    data = data.decode('utf-8')
    data = [(ord(data[i]), ord(data[1 + i]), data[2 + i]) for i in range(0, len(data), 3)]
    old_len = 0
    for i in data:
        old_len += i[1] + 1
    return LZ77_decode(data, old_len)




