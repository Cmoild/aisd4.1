import huffman_c
import numpy as np
import math
from matplotlib import pyplot as plt

# вычисление энтропии
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

def my_func(x, a, b):
    return a*(np.power(np.e, b * (-x + 3)))

def my_func3(x, a, b):
    return a*(np.power(np.e, b * (-x)))

def my_func2(x, a, b):
    return a * x + b

def graph(func, x_range):
   x = np.arange(*x_range)
   y = func(x)
   plt.plot(x, y)

# возвращает список кодов хаффмана на основе заранее вычесленных констант, используется в LZ77_Huffman
def getLenCodes(__dataLen: int):
    '''
    dictionarylens = {c[1] : 0 for c in _res}#
    for c in _res:
        dictionarylens[c[1]] += 1
    lens = [[c[0], c[1]] for c in dictionarylens.items()]
    lens2 = [c[0] for c in lens]
    lensnot = []
    for i in range(256):
        if i not in lens2:
            lensnot.append([i, 1])
    lens += lensnot
    probs = [c[1] for c in lens]
    chars = [chr(c[0]) for c in lens]
    codeslen = huffman_c.huffman_encode_with_probs(probs, chars)
    huffman_c.free_codes()
    codeslen = [(ord(c[0]), c[1], c[2]) for c in codeslen]
    codeslen.sort(key=lambda x: x[0])

    x = [c[0] for c in codeslen]
    y = [c[1] for c in codeslen]

    max_x = y.index(max(y))
    from scipy.optimize import curve_fit
    xe = np.array([x[i] for i in range(max_x, len(x))])
    ye = np.array([y[i] for i in range(max_x, len(y))])

    popt, _ = curve_fit(my_func, xe, ye)

    #xl = np.array([x[i] for i in range(0, max_x + 1)])
    #yl = np.array([y[i] for i in range(0, max_x + 1)])
    #popt2, _ = curve_fit(my_func2, xl, yl)
    print(popt)
    '''
    y = [__dataLen/800, __dataLen/150 , __dataLen/45]
    probs = [max(int((3.30333703e+05)*(np.power(np.e, (1/3.3) * (-i+3))) + (y[0])/4.5),1) if i >= 3 else max(int(y[i]),1) for i in range(0, 61)]
    probs += [1 for i in range(61, 257)]
    probs[256] = max(int(probs[3] / 4500), 1)
    chars = [chr(i) for i in range(0, 257)]
    return huffman_c.huffman_encode_with_probs(probs, chars)

def count_substrings_with_duplicates(input_string):
    count = 0
    list_of_substrings = []
    i = 0
    while i < len(input_string):
        j = i + 1
        l = 0
        while j <= len(input_string):
            substring = input_string[i:j]
            if substring.count(substring[0]) == len(substring) and j != len(input_string):
                l += 1
            else:
                if substring.count(substring[0]) == len(substring) and j == len(input_string):
                    l += 1
                if l > 1:
                    count += 1
                    list_of_substrings.append(substring[0:l])
                    i += l - 1
                break
            j += 1
        i += 1

    mid_len = sum([len(c) for c in list_of_substrings]) / len(list_of_substrings)

    formula = (sum([len(c) for c in list_of_substrings]) - 2 * len(list_of_substrings)) / len(input_string)

    return mid_len, formula

