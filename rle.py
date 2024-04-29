from PIL import Image
import numpy as np


def run_length_encoding(string):
    encoded_string = ''
    count = 1
    flag = chr(65535)
    for i in range(1, len(string)):
        if string[i] == string[i-1]:
            count += 1
        else:
            if count < 4:
                encoded_string += count * string[i-1]
            else:
                encoded_string += flag + chr(count) + string[i-1]
            count = 1
    if count < 4:
        encoded_string += count * string[len(string)-1]
    else:
        encoded_string += flag + chr(count) + string[len(string)-1]

    return encoded_string

# преобразование картинки в собственный формат

def MakeRawRGBImage(link: str, channels: int):
    img = np.asarray(Image.open(link)).copy()
    f = open('./texts/RawImage.txt', 'w', encoding='utf-8')
    if (channels == 3):
        for i in range(len(img)):
            for j in range(len(img[0])):
                for k in range(3):
                    f.write(chr(int(img[i][j][k])))
    else:
        for i in range(len(img)):
            for j in range(len(img[0])):
                f.write(chr(int(img[i][j])))

# сжатие RGB картинки с помощью RLE
def CompressRGBImage():
    rd = open('./texts/RawImage.txt', 'r', encoding='utf-8')
    wr = open('./texts/CompressedImage.txt', 'w', encoding='utf-8')
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

# распаковка сжатой картинки
def ShowCompressed(x: int, y: int, channels: int):
    comp = []
    i = 0
    rd = open('./texts/CompressedImage.txt', 'r', encoding='utf-8')
    st = ''
    while True:
        st = ''
        st += rd.read(1)
        if (st == ''):
                break
        if (channels == 3):
            if (ord(st[0]) < 256):
                st = chr(1 + 256) + st + rd.read(2)
            else:
                st += rd.read(3)
            comp.append([ord(st[0])-256, ord(st[1]), ord(st[2]), ord(st[3])])
        else:
            if (ord(st[0]) < 256):
                st = chr(1 + 256) + st
            else:
                st += rd.read(1)
            comp.append([ord(st[0])-256, ord(st[1]), ord(st[1]), ord(st[1])])

    img = []
    
    for i in comp:
        for j in range(i[0]):
            img.append(i[1:])
    
    new_img = []

    for i in range(0, len(img), y):
        new_img.append(img[i : (i + y)])
    img = np.array(new_img).astype(np.uint8)
    Image.fromarray(img).show()

# сжатие черно-белой картинки с помощью RLE
def CompressWBImage():
    rd = open('./texts/RawImage.txt', 'r', encoding='utf-8')
    wr = open('./texts/CompressedImage.txt', 'w', encoding='utf-8')
    sumstr = ''
    n = 0
    s = ''
    while True:
        st = ''
        st = rd.read(1)
        if (st == ''):
            break
        s += st
    for i in range(0, len(s)):
        run = s[i]
        if (sumstr == '' or sumstr[0] == run):
            sumstr += run
        else:
            if (len(sumstr) > 1):
                wr.write(chr(len(sumstr) + 256) + sumstr[0])
            else:
                wr.write(sumstr[0])
            n += len(sumstr)
            sumstr = run
        if (i == len(s) - 1):
            if (len(sumstr) > 1):
                wr.write(chr(len(sumstr) + 256) + sumstr[0])
            else:
                wr.write(sumstr[0])
            n += len(sumstr)

# сжатие текста
def CompressText(link: str, enc: str):
    rd = open(link, 'r', encoding=enc)
    wr = open('./texts/CompressedText.txt', 'w', encoding='utf-8')
    fl = ''
    j = 0
    sumstr = ''
    while True:
        st = ''
        st = rd.read(1)
        if (j % 50000 == 0):
            print(st)
        if (st == ''):
            break
        j += 1
        fl += st
    for i in range(len(fl)):
        if (i % 50000 == 0):
            print(int((i/len(fl)) * 100))
        if (sumstr == '' or sumstr[0] == fl[i]):
            sumstr += fl[i]
        else:
            if(len(sumstr) > 2):
                wr.write(chr(len(sumstr) + 16) + '\x00' + sumstr[0])
            else:
                wr.write(sumstr)
            sumstr = fl[i]
        if (i == len(fl) - 1):
            if(len(sumstr) > 2):
                wr.write(chr(len(sumstr) + 16) + '\x00' + sumstr[0])
            else:
                wr.write(sumstr)

# распаковка сжатого текста
def DecompressText():
    rd = open('./texts/CompressedText.txt', 'r', encoding='utf-8')
    wr = open('./texts/DecompressedText.txt', 'w', encoding='utf-8')
    fl = ''
    j = 0
    sumstr = ''
    while True:
        st = ''
        st = rd.read(1)
        if (j % 50000 == 0):
            print(st)
        if (st == ''):
            break
        j += 1
        fl += st
    i = 0
    while i < len(fl) - 1:
        if (i % 50000 == 0):
            print(int((i/len(fl)) * 100))
        if (fl[i+1] != '\x00'):
            wr.write(fl[i])
            i += 1
        else:
            wr.write((ord(fl[i]) - 16) * fl[i+2])
            i += 3
    wr.write(fl[len(fl) - 1])
    
def IsEqual():
    com = open('./texts/текст.txt', 'r', encoding='ansi')
    dec = open('./texts/DecompressedText.txt', 'r', encoding='utf-8')
    j = 0
    while True:
        st = ''
        std = ''
        st = com.read(1)
        std = dec.read(1)
        if (not st == std):
            print(j)
            print(ord(st), ord(std))
            break
        if (st == ''):
            break
        j += 1


#MakeRawRGBImage('./images/IMG_20210730_111202.jpg', 3)
#MakeRawRGBImage('Cat03.jpg', 3)
#MakeRawRGBImage('lowresRGB.jpg', 3)
#MakeRawRGBImage('istockphoto-1337005456-612x612.jpg', 1)
#MakeRawRGBImage('Без имени.jpg', 3)
#print(1)
#CompressRGBImage()

#CompressWBImage()
#print(2)
#ShowCompressed(3472, 4624,3)
#ShowCompressed(144, 144,3)
#ShowCompressed(1024, 1025,3)
#ShowCompressed(321, 612,1)
#ShowCompressed(256, 256,3)
'''
CompressText('текст.txt', 'ansi')
DecompressText()
IsEqual()

'''

def RLE_IMAGE_DEMO():
    MakeRawRGBImage('./images/istockphoto-1337005456-612x612.jpg', 1)
    CompressWBImage()
    ShowCompressed(321, 612,1)