import bwt
import huffman
import mtf

alph = [chr(c) for c in range(0, 256)]

s = '^BANANA$'

print(bwt.BWT(s))