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
