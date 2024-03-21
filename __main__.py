import bwt
import huffman
import mtf

def main():
    alph = [chr(c) for c in range(0, 256)]

    s = '^BANANA$'

    print(bwt.BWT(s))

    return 0

if __name__ == '__main__':
    main()