import bwt
import huffman
import mtf
import lz77
import huffman_c

def run_length_encoding(string):
    encoded_string = ''
    count = 1
    for i in range(1, len(string)):
        if string[i] == string[i-1]:
            count += 1
        else:
            encoded_string += str(count) + string[i-1]
            count = 1
    encoded_string+=chr(count)+string[-1]
    return encoded_string

import math

def calculate_entropy(string):
    if not string:
        return 0
    
    char_counts = {}
    for char in string:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    total_chars = len(string)
    entropy = 0
    for count in char_counts.values():
        prob = count / total_chars
        entropy -= prob * math.log2(prob)
    
    return entropy

def main():
    abc = [chr(c) for c in range(0, 65535)]
    
    with open('.\\texts\\test.txt', 'r', encoding='utf-8') as f:
        _data = f.read()
        f.close()

    print(len(_data.encode('utf-8')))

    _res = lz77.LZ77_encode(_data)
    
    new_data = "".join([c[2] for c in _res])
    nums = [(14 - len(bin(c[0])[2:])) * '0' + bin(c[0])[2:] + (8 - len(bin(c[1])[2:])) * '0' + bin(c[1])[2:] for c in _res]
    #nums = [(14 - len(bin(c[0])[2:])) * '0' + bin(c[0])[2:] for c in _res]#
    #offsets = "".join([chr(c[0]) for c in _res])

    #lengths = "".join([chr(c[1]) for c in _res])#

    codes = huffman.CanonicalHuffmanCodes(huffman_c.huffman_encode(new_data, abc))
    dictionary = {c[0] : c[2] for c in codes}

    #codeslen = [([ord(c), len(bin(ord(c))[2:]), bin(ord(c))[2:]]) for c in lengths]
    #dictionarylens = {c[0] : c[2] for c in codeslen}#
    
    #codesoffs = [([ord(c), len(bin(ord(c))[2:]), bin(ord(c))[2:]]) for c in offsets]
    #dictionaryoffs = {c[0] : c[2] for c in codesoffs}

    new_data = "".join([nums[i] + dictionary[new_data[i]] for i in range(len(new_data))])
    #new_data = "".join([dictionaryoffs[ord(offsets[i])] + dictionarylens[ord(lengths[i])] + dictionary[new_data[i]] for i in range(len(new_data))])#

    print(sum([c[1] for c in codes]) + len(new_data))
    print(new_data[:100])
    # + sum([c for c in dictionarylens.values()]) + sum([c for c in dictionaryoffs.values()]))
    from ctypes import CDLL, c_char_p, c_int, c_wchar_p
    lib = CDLL(".\mylib.so")
    j = 0
    for i in range(0, len(new_data), 65536):
        lib.WriteBinaryIntoFile(c_char_p("C:/MyGames/test.bin".encode('utf-8')), c_char_p(new_data[i:i+65536].encode('utf-8')))
        j += 1
        if (j % 100 == 0):
            print(j)
    #c_in = c_char_p(new_data.encode('utf-8'))
    #c_path = c_char_p("C:/MyGames/test.bin".encode('utf-8'))
    #lib.WriteBinaryIntoFile(c_path, c_in)
    eof = ''
    i = 0
    s = ''
    lib.GetBinaryCodeFromFile.restype = c_char_p
    print(lib.GetBinaryCodeFromFile(c_char_p("C:/MyGames/test.bin".encode('utf-8')), c_int(i), c_int(65536))[:100])
    '''
    while not eof:
        eof = lib.GetBinaryCodeFromFile(c_char_p("C:/MyGames/test.bin".encode('utf-8')), c_int(i), c_int(65536))
        i += 65536
        s += eof
        print(i)
    print(s)
    '''
    
    return 0

if __name__ == '__main__':
    main()