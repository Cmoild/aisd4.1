# прямое преобразование BWT с использованием Radix Sort
def BWT(data):
    BWT_list = []
    for i in range(len(data)):
        BWT_list.append(data[i:] + data[:i])
    BWT_list = RadixSort(BWT_list)
    transformed_data = "".join([BWT_list[i][-1] for i in range(len(data))])
    ind = BWT_list.index(data)
    return transformed_data, ind

# прямое преобразование BWT с использованием стандартной библиотеки
def BWT_tim(data):
    BWT_list = []
    for i in range(len(data)):
        BWT_list.append(data[i:] + data[:i])
    BWT_list.sort()
    transformed_data = "".join([BWT_list[i][-1] for i in range(len(data))])
    ind = BWT_list.index(data)
    return transformed_data, ind

# обратное преобразование BWT
def inverse_BWT(data, ind):
    
    L = [(data[i], i) for i in range(len(data))]
    
    L.sort()
    s = ''
    P = list(zip(*L))[1]
    
    for i in range(len(data)):
        ind = P[ind]
        s = s + data[ind]
    return s

# сортировка Radix Sort
def RadixSort(strings: list):
    from ctypes import CDLL, c_wchar_p, POINTER
    lib = CDLL(".\mylib.so")
    c_arr = (c_wchar_p * len(strings))()
    c_arr[:] = strings
    #lib.radix_sort.restype = POINTER(c_wchar_p)
    #lib.radix_sort(c_arr, len(strings))
    lib.sort.restype = POINTER(c_wchar_p)
    lib.sort(c_arr, len(strings))
    return [i for i in c_arr]

from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar, c_uint16
class bwt(Structure):
    _fields_ = [
        ('str', c_wchar_p),
        ('index', c_int)
    ]

def BWT_c(__data):
    lib = CDLL("./bwtlib.so")
    c_data = c_wchar_p(__data)
    lib.BWT.restype = bwt
    res = lib.BWT(c_data, len(__data))
    return res.str, res.index

def inverse_BWT_c(__data, __ind):
    lib = CDLL("./bwtlib.so")
    c_data = (c_uint16 * len(__data))()
    c_data[:] = [ord(i) for i in __data]
    c_ind = c_int(__ind)
    lib.UNBWT.restype = c_wchar_p
    res = lib.UNBWT(c_data, len(__data), c_ind)
    return res

def MakeSuffixArray(__data):
    '''Создание суффиксного массива'''
    suffix_list = []
    for i in range(len(__data)):
        suffix_list.append(__data[i:])
    suffix_list.sort()

    suffix_array = []
    for suffix in suffix_list:
        offset = len(__data) - len(suffix)
        suffix_array.append(offset)

    return suffix_array

def buildTypeMap(__data):
    ''' Возвращает типы суффиксов строки '''
    res = bytearray(len(__data) + 1)
    res[-1] = ord('S')
    if not len(__data):
        return res
    res[-2] = ord('L')
    for i in range(len(__data)-2, -1, -1):
        if __data[i] > __data[i+1]:
            res[i] = ord('L')
        elif __data[i] == __data[i+1] and res[i+1] == ord('L'):
            res[i] = ord('L')
        else:
            res[i] = ord('S')
    return res.decode('utf-8')


def BWT_withSA(__data: str, __suffArr: list):
    '''Прямое преобразование BWT с использованием суффиксного массива'''
    return "".join([__data[i - 1] for i in __suffArr]), __suffArr.index(0)

