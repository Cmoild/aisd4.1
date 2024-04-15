import huffman_c
import bwt
import mtf
import lz77_huffman
from time import time

LENGTH_OF_RUN = 65535
#LENGTH_OF_RUN = 10
NUMBER_OF_DIGITS = 16

from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar, c_ushort
class BWT_MTF(Structure):
    _fields_ = [
        ('arr', (c_ushort * LENGTH_OF_RUN)),
        ('index', c_int)
    ]

def BWT_MTF_c(data):
    lib = CDLL("./bwtlib.so")
    c_data = c_wchar_p(data)
    lib.BWT_MTF.restype = BWT_MTF
    res = lib.BWT_MTF(c_data, len(data))
    return res.arr, res.index

# компрессор на основе BWT+MTF+Huffman
def BWT_MTF_HA_COMPRESS(__path: str, __newPath: str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    d = [chr(c) for c in range(0, 65535)]
    i = 0
    new_data = ''
    inds = []
    '''
    while i < len(data):
        start1 = time()
        s = data[i:i + LENGTH_OF_RUN]
        s, ind = bwt.BWT_tim(s)
        inds.append(ind)
        start2 = time()
        s = mtf.mtf_encode(s, d.copy())
        new_data += s
        i += LENGTH_OF_RUN
        print(start2 - start1, time() - start2)
        print(i)
    '''
    
    while i < len(data):
        start1 = time()
        s = data[i:i + LENGTH_OF_RUN]
        res, ind = BWT_MTF_c(s)
        inds.append(ind)
        new_data += ''.join([chr(res[c]) for c in range(len(s))])
        i += LENGTH_OF_RUN
        print(time() - start1)
        print(i)
    
    
    print("Making huffman codes")
    codes = huffman_c.huffman_encode(new_data, d.copy())
    huffman_c.free_codes()
    print("Encoding")
    new_data = huffman_c.get_encoded(new_data, codes)

    inds_in_binary = "".join([(NUMBER_OF_DIGITS - len(bin(c)[2:])) * '0' + bin(c)[2:] for c in inds])
    num_of_inds = (16 - len(bin(len(inds))[2:])) * '0' + bin(len(inds))[2:]
    num_of_codes = (14 - len(bin(len(codes))[2:])) * '0' + bin(len(codes))[2:]
    codes_in_binary = ''.join([(16 - len(bin(ord(c[0]))[2:])) * '0' + bin(ord(c[0]))[2:] + (6 - len(bin(len(c[2]))[2:])) * '0' + bin(len(c[2]))[2:] + c[2] for c in codes])
    old_len = (32 - len(bin(len(data))[2:])) * '0' + bin(len(data))[2:]
    new_data = num_of_inds + inds_in_binary + num_of_codes + codes_in_binary + old_len + new_data
    print("Saving")
    lz77_huffman.binaryDataToFile(new_data, __newPath)

# декомпрессор на основе BWT+MTF+Huffman
def BWT_MTF_HA_DECOMPRESS(__path: str):
    d = [chr(c) for c in range(0, 65535)]
    data = lz77_huffman.binaryDataFromFile(__path)
    i = 0
    num_of_inds = int(data[0:16], 2)
    i += 16
    inds = []
    for j in range(num_of_inds):
        inds.append(int(data[i:i+NUMBER_OF_DIGITS], 2))
        i += NUMBER_OF_DIGITS
    
    num_of_codes = int(data[i:i+14], 2)
    i += 14
    codes = {}
    for j in range(num_of_codes):
        codes[data[i+22:i+22+int(data[i+16:i+22], 2)]] = chr(int(data[i:i+16], 2))
        i += 22 + int(data[i+16:i+22], 2)
    
    old_len = int(data[i:i+32],2)
    i += 32
    data = data[i:]
    i = 0
    n = 0
    new_data = ''
    while n < old_len:
        j = 1
        char = ''
        while True:
            if (data[i:i+j] in codes.keys()):
                char = codes[data[i:i+j]]
                break
            else:
                j += 1
        i += j
        n += 1
        if (n % LENGTH_OF_RUN == 0):
            print(n)
        new_data += char

    n = 0
    decoded = ''
    for i in range(0, old_len, LENGTH_OF_RUN):
        s = new_data[i:i+LENGTH_OF_RUN]
        s = mtf.mtf_decode(s, d.copy())
        s = bwt.inverse_BWT(s, inds[n])
        n += 1
        decoded += s
        print(i)

    return decoded