import bwt
import rle

def BWT_RLE_COMPRESSOR(__path:str, __newPath:str):
    with open(__path, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    
    data, ind = bwt.FastBWT_c(data)
    data = rle.run_length_encoding(data)
    data = data.encode('utf-8')

    data = ind.to_bytes(4, 'big') + data
    print(data)
    with open(__newPath, 'wb') as f:
        f.write(data)
        f.close()
    
def BWT_RLE_DECOMPRESSOR(__path:str):
    with open(__path, 'rb') as f:
        data = f.read()
        f.close()
    index = int.from_bytes(data[:4], 'big')
    data = data[4:]
    data = data.decode('utf-8')
    data = "".join([c for c in data])
    data = rle.run_length_decoding(data)
    
    data = bwt.inverse_BWT_c(data, index)

    return data

