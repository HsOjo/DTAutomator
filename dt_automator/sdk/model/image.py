from io import BytesIO
from typing import List

from PIL.Image import new as img_new, Image

from dt_automator.base.model import BaseModel


class ImageModel(BaseModel):
    def __init__(self):
        self.w = 0
        self.h = 0
        self.pxs = []  # type: List[int]

    def load_image(self, img: Image, x=0, y=0, w=None, h=None):
        if w is None:
            w = img.width - x
        if h is None:
            h = img.height - y

        pxs = []
        for py in range(h):
            py = y + py
            for px in range(w):
                px = x + px
                pixel = img.getpixel((px, py))  # type: List[int]
                for v in pixel:
                    pxs.append(v)

        self.pxs, self.w, self.h = pxs, w, h

    def dump_image(self):
        if self.w == 0 or self.h == 0:
            return b''
        img = img_new('RGBA', (self.w, self.h))
        for y in range(self.h):
            for x in range(self.w):
                img.putpixel((x, y), self.pixel(x, y))
        with BytesIO() as io:
            img.save(io, 'png')
            io.seek(0)
            data = io.read()
        return data

    def pixel(self, x, y):
        index = (y * self.w + x) * 4
        [r, g, b, a] = self.pxs[index:index + 4]
        return r, g, b, a
