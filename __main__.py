import bwt
import huffman
import mtf
import lz77

def main():
    alph = [chr(c) for c in range(0, 65535)]

    with open('.\\texts\\enwik7.txt', 'r', encoding='utf-8') as f:
        _data = f.read()
    print(len(_data))
    #print(huffman.HuffmanCodes(_data, alph.copy()))
    _data = huffman.EncodeHuffman(_data, alph)
    print(lz77.LZ77_encode(_data))
    return 0

if __name__ == '__main__':
    main()