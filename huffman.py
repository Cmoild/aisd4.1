

def BinaryToHex(data):
    n = len(data) % 4
    data = '0' * (4 - n) + data
    return ''.join([hex(int(data[i:i+4], 2))[2:] for i in range(0, len(data), 4)])

def HexToChar(data):
    return ''.join([chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2)])

def CharToHex(data):
    return ''.join([hex(ord(data[i]))[2:] for i in range(0, len(data))])

def HexToBinary(data):
    ret = ''
    for i in range(0, len(data)):
        ret += '0' * (4 - len(bin(int(data[i], 16))[2:])) + bin(int(data[i], 16))[2:]
    return ret

# возвращает список кодов для каждого символа
def HuffmanCodes(data : str, alph : list):
    prob = [(alph[i], data.count(alph[i]), '') for i in range(len(alph))]
    prob.sort(key = lambda x: x[1])
    i = 0
    for i in range(len(prob) - 1, -1, -1):
        if (prob[i][1] == 0):
            prob.pop(i)
    for i in range(1, len(prob)):
        for j in range(0, i):
            prob[j] = (prob[j][0], prob[j][1], '1' + prob[j][2])
        prob[i] = (prob[i][0], prob[i][1], '0' + prob[i][2])
    return prob

# возвращает закодированную строку
def EncodeHuffman(data : str, alph : list):
    codes = HuffmanCodes(data, alph)
    set = {}
    for i in codes:
        set[i[0]] = i[2]
    #codes.index(value = lambda x: x[0])
    ret = ''
    for i in range(0, len(data)):
        #ret += codes[codes.index(lambda x: x[0] == data[i])][2]
        code = set[data[i]]
        ret += code
        if (i % 10000 == 0):
            print(i)
    return ret

# возвращает список канонических кодов
def CanonicalHuffmanCodes(codes: list):
    ret = []
    for i in codes:
        ret.append([i[0], len(i[2])])
    ret.sort(key = lambda x: x[0])
    ret.sort(key = lambda x: x[1])
    ret[0].append('0')
    for i in range(1, len(ret)):
        num = int(ret[i-1][2], 2)
        num += 1
        ret[i].append('')
        ret[i][2] = bin(num)[2:] + (ret[i][1] - len(bin(num)[2:])) * '0'
    return ret

import huffman_c
import lz77_huffman

def Huffman_COMPRESSOR(__path:str, __newPath:str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    d = [chr(c) for c in range(0, 65535)]
    codes = huffman_c.huffman_encode(data, d.copy())
    huffman_c.free_codes()
    new_data = huffman_c.get_encoded(data, codes)
    num_of_codes = (14 - len(bin(len(codes))[2:])) * '0' + bin(len(codes))[2:]
    codes_in_binary = ''.join([(16 - len(bin(ord(c[0]))[2:])) * '0' + bin(ord(c[0]))[2:] + (6 - len(bin(len(c[2]))[2:])) * '0' + bin(len(c[2]))[2:] + c[2] for c in codes])
    old_len = (32 - len(bin(len(data))[2:])) * '0' + bin(len(data))[2:]
    new_data = num_of_codes + codes_in_binary + old_len + new_data
    lz77_huffman.binaryDataToFile(new_data, __newPath)

#Huffman_COMPRESSOR('./texts/test.txt', './compressed/testh.bin')

def Huffman_DECOMPRESS(__path: str):
    d = [chr(c) for c in range(0, 65535)]
    data = lz77_huffman.binaryDataFromFile(__path)
    i = 0
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
    return new_data


