def BWT(data):
    BWT_list = []
    for i in range(len(data)):
        BWT_list.append(data[i:] + data[:i])
    print(RadixSort(BWT_list))
    BWT_list.sort()
    print("-----------------")
    print(BWT_list)
    return
    transformed_data = "".join([BWT_list[i][-1] for i in range(len(data))])
    ind = BWT_list.index(data)
    return transformed_data, ind

def inverse_BWT(data, ind):
    
    L = [(data[i], i) for i in range(len(data))]
    
    L.sort()
    s = ''
    P = list(zip(*L))[1]
    
    for i in range(len(data)):
        ind = P[ind]
        s = s + data[ind]
    return s

def RadixSort(strings: list):
    from ctypes import CDLL, c_wchar_p, POINTER
    lib = CDLL("C:\\Users\\cold1\\vscpr\\aisd\\aisd4.1\\mylib.so")
    c_arr = (c_wchar_p * len(strings))()
    c_arr[:] = strings
    lib.radix_sort.restype = POINTER(c_wchar_p)
    ret = []
    for i in range(len(strings)):
        ret.append(c_arr[i])
    return ret


