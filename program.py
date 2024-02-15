from PIL import Image
import numpy as np

def MakeRawRGBImage(link: str):
    img = np.asarray(Image.open(link)).copy()
    f = open('RawImage.txt', 'w', encoding='utf-8')
    for i in range(len(img)):
        for j in range(len(img[0])):
            for k in range(3):
                f.write(chr(int(img[i][j][k])))

def CompressRGBImage():
    rd = open('RawImage.txt', 'r', encoding='utf-8')
    wr = open('CompressedImage.txt', 'w', encoding='utf-8')
    sumstr = ''
    n = 0
    s = ''
    while True:
        st = ''
        st = rd.read(3)
        if (st == ''):
            break
        s += st
    for i in range(0, len(s), 3):
        run = s[i] + s[i+1] + s[i+2]
        if (sumstr == '' or sumstr[:3] == run):
            sumstr += run
        else:
            if (len(sumstr)//3 > 1):
                wr.write(chr(len(sumstr)//3 + 256) + sumstr[:3])
            else:
                wr.write(sumstr[:3])
            n += len(sumstr)//3
            sumstr = run
        if (i == len(s) - 3):
            if (len(sumstr)//3 > 1):
                wr.write(chr(len(sumstr)//3 + 256) + sumstr[:3])
            else:
                wr.write(sumstr[:3])
            n += len(sumstr)//3

def ShowCompressedRGB(x: int, y: int):
    comp = []
    i = 0
    rd = open('CompressedImage.txt', 'r', encoding='utf-8')
    st = ''
    while True:
        st = ''
        st += rd.read(1)
        if (st == ''):
            break
        if (ord(st[0]) < 256):
            st = chr(1 + 256) + st + rd.read(2)
        else:
            st += rd.read(3)
        comp.append([ord(st[0])-256, ord(st[1]), ord(st[2]), ord(st[3])])

    img = []
    
    for i in comp:
        for j in range(i[0]):
            img.append(i[1:])
    
    new_img = []

    for i in range(0, len(img), y):
        new_img.append(img[i : (i + y)])
    img = np.array(new_img).astype(np.uint8)
    Image.fromarray(img).show()




#MakeRawRGBImage('IMG_20210730_111202.jpg')
#MakeRawRGBImage('Cat03.jpg')
MakeRawRGBImage('lowresRGB.jpg')
#print(1)
CompressRGBImage()
#print(2)
#ShowCompressedRGB(3472, 4624)
ShowCompressedRGB(144, 144)
#ShowCompressedRGB(1024, 1025)

#компресс корректный? тогда обратный алгоритм