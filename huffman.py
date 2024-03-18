#f = open('test.txt', 'wb')
#незначащие нули в начале (запоминать первый символ)

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

def EncodeHuffman(data : str, alph : list):
    codes = HuffmanCodes(data, alph)
    #codes.index(value = lambda x: x[0])
    ret = ''
    for i in range(0, len(data)):
        #ret += codes[codes.index(lambda x: x[0] == data[i])][2]
        code = ''
        for j in range(0, len(codes)):
            if (codes[j][0] == data[i]):
                code = codes[j][2]
                break
        ret += code
    return HexToChar(BinaryToHex(ret))

#abc = [chr(c) for c in range(0, 128)]
#print(HuffmanCodes('_CF☺F☻♥F♥☻F☺☺☺♦☺☻☻☺♣♦☺♣☻☻☺♦☺♦☺☺', abc))
#print(len(EncodeHuffman('_CF☺F☻♥F♥☻F☺☺☺♦☺☻☻☺♣♦☺♣☻☻☺♦☺♦☺☺', abc)))
