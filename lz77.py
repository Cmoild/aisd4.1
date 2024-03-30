from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar
class LZ77_struct(Structure):
    _fields_ = [
        ('offset', c_int),
        ('length', c_int),
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
    c_res = lib.lz77_encode(c_data)
    return [(c_res.out[i].offset, c_res.out[i].length, c_res.out[i].symbol) for i in range(c_res.numberOfElements)]

