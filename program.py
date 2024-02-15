from PIL import Image
import numpy as np

def MakeRawRGBImage(link: str):
    #img = np.asarray(Image.open("istockphoto-1337005456-612x612.jpg")).copy()
    img = np.asarray(Image.open(link)).copy()
    #print(img)
    f = open('RawImage.txt', 'w', encoding='utf-8')
    for i in range(len(img)):
        for j in range(len(img[0])):
            for k in range(3):
                #print(img[i][j][k])
                f.write(chr(int(img[i][j][k])))
    print(len(img), len(img[0]))
    #new_img = Image.fromarray(img)
    #new_img.show()

def CompressRGBImage():
    rd = open('RawImage.txt', 'r', encoding='utf-8')
    wr = open('CompressedImage.txt', 'w', encoding='utf-8')
    #wr2 = open('wr2.txt', 'w', encoding='utf-8')
    #wr3 = open('wr3.txt', 'w', encoding='utf-8')
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
            wr.write(chr(len(sumstr)//3 + 256) + sumstr[:3])
            n += len(sumstr)//3
            #wr2.write(chr(len(sumstr)//3 + 256))
            #wr3.write(str(len(sumstr)//3)+'\n')
            sumstr = run
        if (i == len(s) - 3):
            wr.write(chr(len(sumstr)//3 + 256) + sumstr[:3])
            n += len(sumstr)//3
            #wr2.write(chr(len(sumstr)//3 + 256))
            #wr3.write(str(len(sumstr)//3)+'\n')
    print('pix enc file', len(s)//3, n)

def ShowCompressedRGB(x: int, y: int):
    comp = []
    i = 0
    print('num of pix', x * y)
    k = 0
    rd = open('CompressedImage.txt', 'r', encoding='utf-8')
    st = ''
    final = ''
    straw = ''
    while True:
        st = ''
        st += rd.read(4)
        
        if (st == ''):
            break
        #final = (ord(st[0])-256) * st[1:]
        #straw = ''
        
        #print(i, end='')
        comp.append([ord(st[0])-256, ord(st[1]), ord(st[2]), ord(st[3])])
    
    #print(len(comp))
    
    k = 0
    img = []
    
    for i in comp:
        k += i[0]
        for j in range(i[0]):
            img.append(i[1:])
    print('pix', k)
    
    for i in range(len(comp)):
        k += comp[i][0]
    print(k)
    new_img = []
    for i in range(0, len(img), y):
        new_img.append(img[i : (i + y)])
    
    #print(len(new_img), len(new_img[x-1]), len(new_img[0][0]))
    for i in range(y):
        for j in range(x):
            try:
                if (len(new_img[j][i]) != 3):
                    print(new_img[j][i])
            except IndexError:
                #print(j , i)
                new_img[j].append([0,0,0])
    img = np.array(new_img).astype(np.uint8)
    #print(img)
    Image.fromarray(img).show()




MakeRawRGBImage('IMG_20210730_111202.jpg')
#MakeRawRGBImage('Cat03.jpg')
#MakeRawRGBImage('lowresRGB.jpg')
#print(1)
CompressRGBImage()
#print(2)
ShowCompressedRGB(3472, 4624)
#ShowCompressedRGB(144, 144)
#ShowCompressedRGB(1024, 1025)

#компресс корректный? тогда обратный алгоритм