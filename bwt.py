def BWT(data):
    BWT_list = []
    for i in range(len(data)):
        BWT_list.append(data[i:] + data[:i])
    BWT_list.sort()
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

#d, i = BWT('A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED')
#print(d)
#print(inverse_BWT(d, i))


#import ctypes

#lib = ctypes.CDLL("C:\\Users\\cold1\\vscpr\\aisd\\aisd4.1\\radix_sort.so")


