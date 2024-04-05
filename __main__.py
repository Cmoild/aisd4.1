import bwt
import huffman
import mtf
import lz77
import huffman_c
import utils
import lz77_huffman

def LZ77_Huffman_DEMO():
    lz77_huffman.LZ77_Huffman_COMPRESS('./texts/enwik7.txt', 'C:/MyGames/enwik7.bin')

    
    s = lz77_huffman.LZ77_Huffman_DECOMPRESS('C:/MyGames/enwik7.bin')
    with open('./texts/enwik7cpy.txt', 'w', encoding='utf-8') as f:
        f.write(s.encode('utf-8').decode('utf-8'))
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

def main():

    
    
    LZ77_Huffman_DEMO()




    return

if __name__ == '__main__':
    main()