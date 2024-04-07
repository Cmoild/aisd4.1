import bwt
import huffman
import mtf
import lz77
import huffman_c
import utils
import lz77_huffman
from rle import RLE_IMAGE_DEMO, run_length_encoding
import bwt_mtf_ha

def LZ77_Huffman_DEMO():
    lz77_huffman.LZ77_Huffman_COMPRESS('./texts/test.txt', 'C:/MyGames/testlzh.bin')

    
    s = lz77_huffman.LZ77_Huffman_DECOMPRESS('C:/MyGames/testlzh.bin')
    with open('./texts/testcpy.txt', 'w', encoding='utf-8') as f:
        f.write(s.encode('utf-8').decode('utf-8'))
        f.close()

    
    with open('./texts/test.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    with open('./texts/testcpy.txt', 'r', encoding='utf-8') as f:
        copy = f.read()
        f.close()

    print(len(orig), len(copy))
    if orig == copy:
        print("OK")

def LZ77_DEMO():
    lz77.LZ77_COMPRESS('./texts/test.txt', 'C:/MyGames/test.bin')
    decoded = lz77.LZ77_DECOMPRESS('C:/MyGames/test.bin')
    with open('./texts/testcpy.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
        f.close()

    with open('./texts/test.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    with open('./texts/testcpy.txt', 'r', encoding='utf-8') as f:
        copy = f.read()
        f.close()

    print(len(orig), len(copy))
    if orig == copy:
        print("OK")

def BWT_MTF_HA_DEMO():
    bwt_mtf_ha.BWT_MTF_HA_COMPRESS('./texts/enwik7.txt', 'C:/MyGames/enwik7bmh.bin')


    decoded = bwt_mtf_ha.BWT_MTF_HA_DECOMPRESS('C:/MyGames/enwik7bmh.bin')
    
    with open('./texts/enwik7cpy.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
        f.close()
    
    with open('./texts/enwik7.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    if orig == decoded:
        print("OK")

def main():
    
    BWT_MTF_HA_DEMO()


    return

if __name__ == '__main__':
    main()