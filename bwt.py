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

from ctypes import CDLL, c_wchar_p, POINTER, Structure, c_int, c_wchar
class bwt(Structure):
    _fields_ = [
        ('str', c_wchar_p),
        ('index', c_int)
    ]

def BWT_c(data):
    lib = CDLL("./bwtlib.so")
    c_data = c_wchar_p(data)
    lib.BWT.restype = bwt
    res = lib.BWT(c_data)
    return res.str, res.index

