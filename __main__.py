import bwt
import huffman
import mtf
import lz77
import huffman_c
import utils
import lz77_huffman
from rle import RLE_IMAGE_DEMO, run_length_encoding
import bwt_mtf_ha
import bwt_rle

def LZ77_Huffman_DEMO():
    lz77_huffman.LZ77_Huffman_COMPRESS('./compressed/enwik8bmhNEW.bin', './compressed/enwik8bmhNEW.bin')

    
    s = lz77_huffman.LZ77_Huffman_DECOMPRESS('./compressed/enwik8lzhANOTHER.bin')
    with open('./texts/enwik8cpy.txt', 'w', encoding='utf-8') as f:
        f.write(s.encode('utf-8').decode('utf-8'))
        f.close()

    
    with open('C:\\Users\\cold1\\Downloads\\enwik8\\enwik8', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    with open('./texts/enwik8cpy.txt', 'r', encoding='utf-8') as f:
        copy = f.read()
        f.close()

    print(len(orig), len(copy))
    print(orig[len(orig)-100:len(orig)])
    print(copy[len(copy)-100:len(copy)])

    if orig == copy:
        print("OK")

def LZ77_DEMO():
    lz77.LZ77_COMPRESS('./texts/enwik7.txt', 'C:/MyGames/enwik7lz.bin')
    
    decoded = lz77.LZ77_DECOMPRESS('C:/MyGames/enwik7lz.bin')
    with open('./texts/enwik7cpy.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
        f.close()

    with open('./texts/enwik7.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    with open('./texts/enwik7cpy.txt', 'r', encoding='utf-8') as f:
        copy = f.read()
        f.close()

    print(len(orig), len(copy))
    if orig == copy:
        print("OK")

def BWT_MTF_HA_DEMO():
    

    bwt_mtf_ha.BWT_MTF_HA_COMPRESS('./texts/enwik7.txt', './compressed/enwik7bmh.bin')
    
    return
    decoded = bwt_mtf_ha.BWT_MTF_HA_DECOMPRESS('./compressed/enwik7bmh.bin')
    
    
    with open('./texts/testcpy.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
        f.close()
    
    with open('./texts/tolstoy.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    if orig == decoded:
        print("OK")

def Huffman_DEMO():
    huffman.Huffman_COMPRESSOR('./texts/tolstoy.txt', './compressed/testh.bin')

    decoded = huffman.Huffman_DECOMPRESS('./compressed/testh.bin')

    with open('./texts/testcpy.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
        f.close()
    
    with open('./texts/tolstoy.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    
    if orig == decoded:
        print("OK")

def BWT_RLE_DEMO():
    bwt_rle.BWT_RLE_COMPRESSOR('./texts/tolstoy.txt', './compressed/testrle.bin')

    decoded = bwt_rle.BWT_RLE_DECOMPRESSOR('./compressed/testrle.bin')
    
    with open('./texts/testcpy.txt', 'w', encoding='utf-8') as f:
        f.write(decoded)
        f.close()
    
    with open('./texts/tolstoy.txt', 'r', encoding='utf-8') as f:
        orig = f.read()
        f.close()
    print(len(orig), len(decoded))
    if orig == decoded[:len(orig)]:
        print("OK")

def main():
    
    BWT_RLE_DEMO()
    return

if __name__ == '__main__':
    main()