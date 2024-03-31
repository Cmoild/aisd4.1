import bwt
import huffman
import mtf
import lz77
import huffman_c

def main():
    alph = [chr(c) for c in range(0, 65535)]
    
    with open('.\\texts\\enwik7.txt', 'r', encoding='utf-8') as f:
        _data = f.read()
        f.close()

    print(len(_data))

    
    
    #codes = huffman_c.huffman_encode(_data, alph)
    #print(codes)
    
    #_data = huffman_c.get_encoded(_data, codes)
    #_data = huffman.EncodeHuffman(_data, alph)

    _res = lz77.LZ77_encode(_data)

    print(len(_res))
    

    
    return 0

if __name__ == '__main__':
    main()