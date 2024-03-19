import bwt
import huffman
import mtf

alph = [chr(c) for c in range(0, 256)]

s = 'aaaaaaaaaabcccccccccccccccddddddd'

print(huffman.CanonicalHuffmanCodes(huffman.HuffmanCodes(s, alph)))

