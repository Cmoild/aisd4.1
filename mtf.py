
def mtf_encode(data: str, dictionary: list):
    encoded = []
    ind = 0
    for i in range(len(data)):
        ind = dictionary.index(data[i])
        encoded.append(ind)
        dictionary.pop(ind)
        dictionary.insert(0, data[i])
    return ''.join([chr(i) for i in encoded])

def mtf_decode(encoded: str, dictionary: list):
    data = ''
    enc = [ord(i) for i in encoded]
    for i in range(len(encoded)):
        data += dictionary[enc[i]]
        dictionary.pop(enc[i])
        dictionary.insert(0, data[i])
    return data

#abc = [chr(c) for c in range(0, 255)]
#enc_list = mtf_encode('_BBEBDE__CD_A___AA__E_AEEEAAABDBCDDBDDEDAAADDA', abc.copy())
#print(enc_list)
#dec = mtf_decode(enc_list, abc.copy())
#print(dec)