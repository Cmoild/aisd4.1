import huffman_c
import bwt
import mtf
import lz77_huffman
from time import time
import rle

LENGTH_OF_RUN = 65535
LENGTH_OF_RUN = 110000000
NUMBER_OF_DIGITS = 27

from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar, c_ushort, c_uint16
class BWT_MTF(Structure):
    _fields_ = [
        ('arr', POINTER(c_ushort)),
        ('index', c_int)
    ]

def BWT_MTF_c(data):
    lib = CDLL("./bwtlib.so")
    c_data = c_wchar_p(data)
    lib.BWT_MTF.restype = BWT_MTF
    res = lib.BWT_MTF(c_data, len(data))
    return res.arr, res.index

# компрессор на основе BWT+MTF+Huffman
def BWT_MTF_RLE_HA_COMPRESS(__path: str, __newPath: str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    '''
    with open('./texts/RawImage.bin', 'rb') as f:
        data = f.read()
        f.close()
    data = "".join([chr(c) for c in data])
    print(len(data))
    '''
    d = [chr(c) for c in range(0, 65535)]
    i = 0
    new_data = ''
    inds = []
    print(len(data))
    while i < len(data):
        start1 = time()
        s = data[i:i + LENGTH_OF_RUN]
        res, ind = BWT_MTF_c(s)
        inds.append(ind)
        new_data += ''.join([chr(res[c]) for c in range(len(s))])
        i += LENGTH_OF_RUN
        #print(time() - start1)
        #print(i)
    
    new_data = rle.run_length_encoding(new_data)
    print([ord(i) for i in new_data[24830:24850]])
    print("Making huffman codes")
    codes = huffman_c.huffman_encode(new_data, d.copy())
    #print(codes)
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
def BWT_MTF_RLE_HA_DECOMPRESS(__path: str):
    print("Reading")
    d = [chr(c) for c in range(0, 65535)]
    data = lz77_huffman.binaryDataFromFile(__path)
    print(data[0:50])
    i = 0
    num_of_inds = int(data[0:16], 2)
    print(num_of_inds)
    i += 16
    inds = []
    for j in range(num_of_inds):
        inds.append(int(data[i:i+NUMBER_OF_DIGITS], 2))
        i += NUMBER_OF_DIGITS
    print(inds)
    num_of_codes = int(data[i:i+14], 2)
    i += 14
    codes = {}
    for j in range(num_of_codes):
        codes[data[i+22:i+22+int(data[i+16:i+22], 2)]] = chr(int(data[i:i+16], 2))
        i += 22 + int(data[i+16:i+22], 2)
    print(num_of_codes)
    
    old_len = int(data[i:i+32],2)
    i += 32
    data = data[i:]
    i = 0
    n = 0
    new_data = ''
    print("Decoding")
    while n < old_len:
        j = 1
        char = ''
        while True:
            #print(j)
            if (data[i:i+j] in codes.keys()):
                char = codes[data[i:i+j]]
                #print(char)
                break
            else:
                j += 1
        i += j
        n += 1
        if (n % 50000 == 0):
            print(n)
        new_data += char

    n = 0
    decoded = ''
    print(old_len)
    print(len(new_data))
    new_data = rle.run_length_decoding(new_data)
    for i in range(0, old_len, LENGTH_OF_RUN):
        s = new_data[i:i+LENGTH_OF_RUN]
        print(len(s))
        s = mtf.mtf_decode(s, d.copy())
        print(len(s))
        #s = bwt.inverse_BWT(s, inds[n])
        s = bwt.inverse_BWT_c(s, inds[n])
        print("after bwt", len(s))
        n += 1
        decoded += s
        print(i)

    return decoded