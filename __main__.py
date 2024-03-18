import bwt
import huffman
import mtf

alph = [chr(c) for c in range(0, 256)]

s = 'Both of these mechanisms are related to Python modules; how users interact with them and how they interact with each other. They are explained in detail below. If you\'re new to Python modules, see the tutorial section Modules for an introduction.'
print(len(bwt.BWT(s)[0]))
print(huffman.EncodeHuffman(mtf.mtf_encode(bwt.BWT(s)[0], alph.copy()), alph))