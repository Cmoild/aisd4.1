import bwt
import huffman
import mtf
import time
import random
from matplotlib import pyplot as plt

def main():
    alph = [chr(c) for c in range(33, 256)]

    s = ''
    for i in range(0, 3000):
        s += random.choice(alph)
        start = time.time()
        bwt.BWT(s)
        end = time.time()
        plt.plot(i, end - start, 'ro', ms = 0.75)
        start = time.time()
        bwt.BWT_tim(s)
        end = time.time()
        plt.plot(i, end - start, 'bo', ms = 0.75)
        print(i)
    plt.show()
    return 0

if __name__ == '__main__':
    main()