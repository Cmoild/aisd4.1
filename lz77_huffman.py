import lz77
import huffman_c
import utils

NUMBER_OF_DIGITS = 16

def getBinaryCode(__path: str):

    abc = [chr(c) for c in range(0, 65535)]

    with open(__path, 'r', encoding='utf-8') as f:
        _data = f.read()
        f.close()
    print(len(_data))
    #print(len(_data.encode('utf-8')))
    _data = _data.encode('utf-8').decode('utf-8')
    old_len = len(_data)
    _res = lz77.LZ77_encode(_data)
    #print(_res[len(_res)-10:len(_res)])
    #print(utils.calculate_entropy(_data))
    new_data = "".join([c[2] for c in _res])

    codes = huffman_c.huffman_encode(new_data, abc)
    dictionary = {c[0] : c[2] for c in codes}
    huffman_c.free_codes()

    huffman_for_lens = utils.getLenCodes(len(_data))
    huffman_c.free_codes()
    
    dictionarylens = {ord(c[0]) : c[2] for c in huffman_for_lens}
    
    #dictlendec = {c[2] : c[0] for c in huffman_for_lens}
    

    new_data = "".join([(NUMBER_OF_DIGITS - len(bin(c[0])[2:])) * '0' + bin(c[0])[2:] + dictionarylens[c[1]] + dictionary[c[2]] for c in _res])

    return new_data, codes, old_len

def getLZ77Code(__binaryCode: str, __huffmanCodes: list, __oldLen: int):
    huffman_for_lens = utils.getLenCodes(__oldLen)
    dictlendec = {c[2] : c[0] for c in huffman_for_lens}
    dictchars = {c[2] : c[0] for c in __huffmanCodes}
    new_data = __binaryCode
    old_data = []
    i = 0
    while i != len(new_data):
        if (len(new_data) - i < NUMBER_OF_DIGITS):
            break
        numoffs = int(new_data[i:i+NUMBER_OF_DIGITS], 2)
        i += NUMBER_OF_DIGITS
        numlens = 0
        j = 1
        while True:
            if (new_data[i:i+j] in dictlendec.keys()):
                numlens = dictlendec[new_data[i:i+j]]
                break
            else:
                j += 1
                #print(new_data[i:i+j-1])
        i +=j
        j = 1
        char = ''
        while True:
            if (new_data[i:i+j] in dictchars.keys()):
                char = dictchars[new_data[i:i+j]]
                break
            else:
                j += 1
        i += j
        old_data.append((numoffs, ord(numlens), char))
    return old_data

def binaryDataToFile(__data: str, __path: str):
    from ctypes import CDLL, c_char_p
    lib = CDLL(".\mylib.so")
    for i in range(0, len(__data), 65536):
        lib.WriteBinaryIntoFile(c_char_p(__path.encode('utf-8')), c_char_p(__data[i:i+65536].encode('utf-8')))

def binaryDataFromFile(__path: str):
    from ctypes import CDLL, c_char_p, c_int
    lib = CDLL(".\mylib.so")
    eof = ''
    i = 0
    s = ''
    lib.GetBinaryCodeFromFile.restype = c_char_p
    #print(lib.GetBinaryCodeFromFile(c_char_p("C:/MyGames/test.bin".encode('utf-8')), c_int(i), c_int(65536))[:100])
    
    while True:
        eof = lib.GetBinaryCodeFromFile(c_char_p(__path.encode('utf-8')), c_int(i), c_int(65536))
        if eof == None:
            break
        i += 65536
        s += eof.decode('utf-8')
        #print(i)
    #print(s)
    
    #print(len(s))
    return s

def LZ77_Huffman_COMPRESS(__path: str, __newPath: str):
    print("Getting binary code...")
    new_data, codes, len_old = getBinaryCode(__path)
    
    #print(len(new_data))

    str_len_old = (32 - len(bin(len_old)[2:])) * '0' + bin(len_old)[2:]
    num_of_codes = (14 - len(bin(len(codes))[2:])) * '0' + bin(len(codes))[2:]
    codes_in_binary = ''.join([(16 - len(bin(ord(c[0]))[2:])) * '0' + bin(ord(c[0]))[2:] + (6 - len(bin(len(c[2]))[2:])) * '0' + bin(len(c[2]))[2:] + c[2] for c in codes])
    new_data = str_len_old + num_of_codes + codes_in_binary + new_data
    #print("old",len_old, len(codes))
    #print(codes)
    print("Exporting...")
    binaryDataToFile(new_data, __newPath)
    print("Done")

def LZ77_Huffman_DECOMPRESS(__path: str):
    print("Importing...")
    data = binaryDataFromFile(__path)
    len_old = int(data[0:32], 2)
    num_of_codes = int(data[32:32+14], 2)
    #print("new",len_old, num_of_codes)
    codes = []
    i = 32+14
    print("Getting huffman codes...")
    while i < len(data):
        codes.append((chr(int(data[i:i+16], 2)), int(data[i+16:i+22], 2), data[i+22:i+22+int(data[i+16:i+22], 2)]))
        if (len(codes) == num_of_codes - 1):
            i += 0
        i += 22+int(data[i+16:i+22], 2)
        if (len(codes) == num_of_codes):
            break
    print("Getting LZ77 codes...")
    _res = getLZ77Code(data[i:len(data)], codes, len_old)
    #print(_res[len(_res)-10:len(_res)])
    print("Decoding...")
    decoded = lz77.LZ77_decode(_res, len_old)
    #decoded = lz77.lz77_decode(_res, len(_res) , len_old)
    print("Done")
    return decoded