from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar, addressof


class huffman_tuple(Structure):
    _fields_ = [
        ('symbol', c_wchar),
        ('length', c_int),
        ('code', c_wchar_p)
    ]

class huffman_return(Structure):
    _fields_ = [
        ('out', POINTER(huffman_tuple)),
        ('numberOfElements', c_int)
    ]

class get_probs_and_chars_return(Structure):
    _fields_ = [
            ('chars', (c_wchar * 65535)),
            ('probs', (c_int * 65535)),
    ]

def huffman_encode(data: str, alph : list):
    lib = CDLL(".\huffmanlib.so")
    probs, chars = get_probs(data, alph)
    c_probs = (c_int * len(probs))()
    c_probs[:] = probs
    c_chars = (c_wchar * len(chars))()
    c_chars[:] = chars
    lib.GetHuffmanCodes.restype = huffman_return
    
    c_res = lib.GetHuffmanCodes(c_chars, c_probs, len(probs))
    del c_probs, c_chars, lib
    return [(c_res.out[i].symbol, c_res.out[i].length, c_res.out[i].code) for i in range(c_res.numberOfElements)]

def huffman_encode_with_probs(probs : list, chars : list):
    lib = CDLL(".\huffmanlib.so")
    c_probs = (c_int * len(probs))()
    c_probs[:] = probs
    c_chars = (c_wchar * len(chars))()
    c_chars[:] = chars
    lib.GetHuffmanCodes.restype = huffman_return
    
    c_res = lib.GetHuffmanCodes(c_chars, c_probs, len(probs))
    del c_probs, c_chars, lib
    return [(c_res.out[i].symbol, c_res.out[i].length, c_res.out[i].code) for i in range(c_res.numberOfElements)]

def get_probs(data : str, alph : list):
    lib = CDLL(".\huffmanlib.so")
    lib.get_probs_and_chars.restype = POINTER(c_int * 65535)
    c_data = c_wchar_p(data)

    c_res = lib.get_probs_and_chars(c_data, len(data))

    res = [i for i in c_res.contents]
    chars = [chr(i) for i in range(65535) if res[i] != 0]
    probs = [res[i] for i in range(65535) if res[i] != 0]

    return probs, chars

def get_encoded(__data : str ,__codes : list):
    ret = ''
    code_list = {__codes[i][0] : __codes[i][2] for i in range(len(__codes))}
    for i in range(0, len(__data)):
        ret += code_list[__data[i]]
    return ret

def free_codes():
    lib = CDLL(".\huffmanlib.so")
    lib.free_codes()