# coding:utf-8
from PIL import Image


class CharImage:
    charset = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def __init__(self, file, outpath=None, width=None, hight=None, autoscale_hight=None):
        self.img = Image.open(file)
        self.outpath = outpath
        self.width = width
        self.hight = hight
        self.autoscale_hight = autoscale_hight

    def gray2char(self, *args):
        if len(args) == 1:
            gray = args[0]
        else:
            r, g, b = args
            gray = int(0.2126*r + 0.7152*g + 0.0722*b)
        return self.charset[gray * 70 // 255]

    def save(self, char_img):
        with open(self.outpath, 'w', encoding='utf-8') as f:
            f.write(char_img)

    def img_resize(self):
        if self.autoscale_hight:
            width, hight = self.img.size
            scale = (self.autoscale_hight / hight)
            img = self.img.resize((int(width*scale*2), int(hight*scale)))
        elif self.width and self.hight:
            img = self.img.resize((self.width, self.hight))
        else:
            img = self.img
        return img

    def get_charimg(self):
        img = self.img_resize()
        char_img = ''
        width, hight = img.size
        for y in range(hight):
            for x in range(width):
                pixel = img.getpixel((x, y))
                char_img += self.gray2char(*pixel)
            char_img += '\n'

        if self.outpath:
            self.save(char_img)
        return char_img


if __name__ == '__main__':
    char_img = CharImage('test2.png', 'test.txt', autoscale_hight=95)
    ci = char_img.get_charimg()
