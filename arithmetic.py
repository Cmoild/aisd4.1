from huffman_c import get_probs

from decimal import *

BLOCK_SIZE = 125

class ArithmeticEncoding:
    """
    ArithmeticEncoding is a class for building the arithmetic encoding.
    """

    def __init__(self, frequency_table, save_stages=False):
        """
        frequency_table: Frequency table as a dictionary where key is the symbol and value is the frequency.
        save_stages: If True, then the intervals of each stage are saved in a list. Note that setting save_stages=True may cause memory overflow if the message is large
        """
        if save_stages:
            self.save_stages = True
        else:
            self.save_stages = False

        self.probability_table = self.get_probability_table(frequency_table)

    def get_probability_table(self, frequency_table):
        """
        Calculates the probability table out of the frequency table.

        frequency_table: A table of the term frequencies.

        Returns the probability table.
        """
        total_frequency = sum(list(frequency_table.values()))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = value/total_frequency

        return probability_table

    def get_encoded_value(self, last_stage_probs):
        """
        After encoding the entire message, this method returns the single value that represents the entire message.

        last_stage_probs: A list of the probabilities in the last stage.
        
        Returns the minimum and maximum probabilites in the last stage in addition to the value encoding the message.
        """
        last_stage_probs = list(last_stage_probs.values())
        last_stage_values = []
        for sublist in last_stage_probs:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)
        encoded_value = (last_stage_min + last_stage_max)/2

        return last_stage_min, last_stage_max, encoded_value

    def process_stage(self, probability_table, stage_min, stage_max):
        """
        Processing a stage in the encoding/decoding process.

        probability_table: The probability table.
        stage_min: The minumim probability of the current stage.
        stage_max: The maximum probability of the current stage.
        
        Returns the probabilities in the stage.
        """

        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(probability_table.items())):
            term = list(probability_table.keys())[term_idx]
            term_prob = Decimal(probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs

    def encode(self, msg, probability_table):
        """
        Encodes a message using arithmetic encoding.

        msg: The message to be encoded.
        probability_table: The probability table.

        Returns the encoder, the floating-point value representing the encoded message, and the maximum and minimum values of the interval in which the floating-point value falls.
        """
        
        msg = list(msg)

        encoder = []
        getcontext().prec = 250
        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for msg_term_idx in range(len(msg)):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)

            msg_term = msg[msg_term_idx]
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            if self.save_stages:
                encoder.append(stage_probs)

        last_stage_probs = self.process_stage(probability_table, stage_min, stage_max)
        
        if self.save_stages:
            encoder.append(last_stage_probs)

        interval_min_value, interval_max_value, encoded_msg = self.get_encoded_value(last_stage_probs)

        return encoded_msg, encoder, interval_min_value, interval_max_value

    def decode(self, encoded_msg, msg_length, probability_table):
        """
        Decodes a message from a floating-point number.
        
        encoded_msg: The floating-point value that encodes the message.
        msg_length: Length of the message.
        probability_table: The probability table.

        Returns the decoded message.
        """

        decoder = []

        decoded_msg = []
        getcontext().prec = 250
        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)

            for msg_term, value in stage_probs.items():
                if encoded_msg >= value[0] and encoded_msg <= value[1]:
                    break

            decoded_msg.append(msg_term)

            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            if self.save_stages:
                decoder.append(stage_probs)

        if self.save_stages:
            last_stage_probs = self.process_stage(probability_table, stage_min, stage_max)
            decoder.append(last_stage_probs)

        return decoded_msg, decoder


def AE_compress(__data: str, __freq: dict):
    s = __data
    
    encoder = ArithmeticEncoding(__freq)
    pr = ArithmeticEncoding.get_probability_table(encoder, __freq)
    encoded = []
    for i in range(0, len(s), BLOCK_SIZE):
        print(i)
        enc = ArithmeticEncoding.encode(encoder, s[i:i+BLOCK_SIZE], pr)
        encoded.append(enc[0])
    '''
    ret = []
    for i in encoded:
        ret.append((100 - len(bin(int('1' + str(i)[2:])))) * '0' + bin(int('1' + str(i)[2:]))[2:])
        #j = (100 - len(bin(int('1' + str(i)[2:])))) * '0' + bin(int('1' + str(i)[2:]))[2:]
        #print(i,  Decimal('0.' + str(int(j, 2))[1:]) if (i == Decimal('0.' + str(int(j, 2))[1:])) == False else '')
        
    return ret
    '''
    s = ''
    encoder = ArithmeticEncoding(__freq)
    pr = ArithmeticEncoding.get_probability_table(encoder, __freq)
    for i in range(len(encoded)):
        #print(encoded[i])
        dec = encoder.decode(encoded[i], BLOCK_SIZE, pr)
        #print(len(bin(int(str(encoded[i])[2:]))))
        print("".join(dec[0]), end="")
        s += "".join(dec[0])
    return s

def AE_decompress(__data: str, __freq: dict):
    encoded = [Decimal('0.' + str(int(i, 2))[1:]) for i in __data]
    '''
    for i in range(0, len(__data)//95, 95):
        encoded.append(Decimal('0.' + str(int(__data[i:i+95], 2))))
    '''
    encoder = ArithmeticEncoding(__freq)
    pr = ArithmeticEncoding.get_probability_table(encoder, __freq)
    for i in range(len(encoded)):
        dec = encoder.decode(encoded[i], BLOCK_SIZE, pr)
        #print(len(bin(int(str(encoded[i])[2:]))))
        print("".join(dec[0]), end="")


'''
probs, chars = get_probs(data, None)
freq = {chars[i]: probs[i] for i in range(len(chars))}

#print(AE_compress(data[:1000], freq))
a = AE_compress(data[:20000], freq)
if a[:len(data[:20000])] == data[:20000]:
    print("\nOK")
#print(len(a))
#AE_decompress(a, freq)
'''
from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar, addressof, c_uint32, c_ubyte, c_char

class prob(Structure):
    _fields_ = [
        ('lower', c_uint32),
        ('upper', c_uint32),
        ('denominator', c_uint32),
        ('character', c_ubyte)
    ]

BLOCK_SIZE = 4

def GetModel():
    lib = CDLL('./arithmetic.so')
    lib.PopulateModel.restype = POINTER(prob)
    model = lib.PopulateModel()
    m = model[:256]
    return [(i.lower, i.upper, i.denominator, chr(i.character)) for i in m if i.character != 0] 


def AEdecodeNumbers(nums: list, dict: list):
    res = []
    c_dic = (c_ubyte * len(dict))()
    c_dic[:] = dict
    #print(dict)
    lib = CDLL('./arithmetic.so')
    lib.ArithmeticDecoding.restype = POINTER(c_ubyte)
    for i in nums:
        arr = lib.ArithmeticDecoding(i, c_dic, BLOCK_SIZE)
        res += bytes(arr[:BLOCK_SIZE])
    return bytes(res).decode('utf-8'), nums

def IntArithmeticEncoding(__data: str):
    lib = CDLL('./arithmetic.so')
    lib.ArithmeticEncoding.restype = c_uint32
    lib.get_freqs.restype = POINTER(c_int)
    __data = __data.encode('utf-8')
    c_data = (c_ubyte * len(__data))()
    c_data[:] = __data
    lib.InitModel(c_data, len(__data))
    #print(GetModel())
    dic = list(set(__data))
    #print(dic)
    nums = []
    freqs = lib.get_freqs(c_data, len(__data))[:256]
    for i in range(0, len(__data), BLOCK_SIZE):
        c_data = (c_ubyte * len(__data[i:i+BLOCK_SIZE]))()
        c_data[:] = __data[i:i+BLOCK_SIZE]
        nums.append(lib.ArithmeticEncoding(c_data, BLOCK_SIZE))
    return nums, dic, freqs

def GetEncodedIntsInBytes(nums: list):
    return b''.join([i.to_bytes(4, 'big') for i in nums])

def GetNumsFromBytes(byt: bytes):
    return [int.from_bytes(byt[i:i+4], 'big') for i in range(0, len(byt), 4)]

def GetCompressedBytes(__data: str):
    nums, dic, freqs = IntArithmeticEncoding(__data)
    bytenums = GetEncodedIntsInBytes(nums)
    #print(freqs)
    new_data = b''.join([bytes([i]) + freqs[i].to_bytes(4, 'big') for i in dic])
    #print(new_data)
    #print(len(b''.join([bytes([i]) * freqs[i] for i in dic])))
    #print(len(dic))
    new_data = len(dic).to_bytes(1, 'big') + len(nums).to_bytes(4, 'big') + new_data + bytenums
    return new_data

def GetOriginalFromBytes(__data: bytes):
    #numOfChars = int.from_bytes(__data[0], 'big')
    numOfChars = __data[0]
    #print(numOfChars)
    numOfNums = int.from_bytes(__data[1:5], 'big')
    __data = __data[5:]
    old_data = b''.join([int.from_bytes(__data[i+1:i+5], 'big') * bytes([__data[i]]) for i in range(0, numOfChars*5, 5)])
    #print([int.from_bytes(__data[i+1:i+5], 'big') for i in range(0, numOfChars*5, 5)])
    #print(len(old_data))
    dic = [__data[i] for i in range(0, numOfChars*5, 5)]
    __data = __data[5*numOfChars:]
    lib = CDLL('./arithmetic.so')
    c_data = (c_ubyte * len(old_data))()
    c_data[:] = old_data
    lib.InitModel(c_data, len(old_data))
    #print(GetModel())
    nums = GetNumsFromBytes(__data)
    orig, _ = AEdecodeNumbers(nums, dic)
    return orig

def AEint_COMPRESS(__path:str, __newPath:str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    b = GetCompressedBytes(data)
    
    with open(__newPath, 'wb') as f:
        f.write(b)
        f.close()

def AEint_DECOMPRESS(__path:str):
    with open(__path, 'rb') as f:
        data = f.read()
        f.close()
    new_data = GetOriginalFromBytes(data)
    return new_data


#data = 'hello world'
#new_data, nums = IntArithmeticEncoding(data)
#b = GetEncodedIntsInBytes(nums)
#new_nums = GetNumsFromBytes(b)
#b = GetCompressedBytes(data)
#print(b)
#new_data = GetOriginalFromBytes(b)
'''
with open('./texts/test.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    f.close()

print(len(data.encode('utf-8')))
AEint_COMPRESS('./texts/test.txt', './compressed/testae.bin')
new_data = AEint_DECOMPRESS('./compressed/testae.bin')


if new_data == data:
    print("OK")
'''